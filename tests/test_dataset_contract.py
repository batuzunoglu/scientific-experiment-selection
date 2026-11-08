import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from scientific_experiment_selection import dataset_contract as d
from scientific_experiment_selection.raw_spectra import read_raw


def column(n):
    out=''
    while n:
        n,r=divmod(n-1,26); out=chr(65+r)+out
    return out


def workbook(path, change=None):
    cells={'A1':'Wavelength','B1':'Temperature'}
    for i,well in enumerate(d.WELLS,3): cells[column(i)+'1']=well
    for i,wave in enumerate(range(350,701,2),2):
        cells[f'A{i}']=wave
        cells[f'C{i}']=1.0  # only A1 populated; synthetic
    if change: change(cells)
    rows={}
    for ref,v in cells.items():
        n=''.join(c for c in ref if c.isdigit())
        xml=(f'<c r="{ref}" t="inlineStr"><is><t>{v}</t></is></c>' if isinstance(v,str)
             else f'<c r="{ref}"><v>{v}</v></c>')
        rows.setdefault(n,[]).append(xml)
    ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('xl/workbook.xml',f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels','<Relationships><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr('xl/worksheets/sheet1.xml',f'<worksheet xmlns="{ns}"><sheetData>'+''.join(f'<row r="{n}">'+''.join(v)+'</row>' for n,v in rows.items())+'</sheetData></worksheet>')


def evidence(exp='Exp5',well='A1',condition='PFHxA_5',qc='include',partition='individual_dataset'):
    return dict(experiment_id=exp,well=well,condition_claim=condition,
        historical_qc_status=qc,historical_qc_reason='',master_partition=partition,
        master_composition_ppm=json.dumps({'PFHxA':'5','TFA':''}),
        proposed_composition_ppm=json.dumps({'PFHxA':'5','TFA':''}),
        historical_variants=json.dumps([dict(replicate='1',preparation_status='reconstructed',
            reference='synthetic.csv#row=2',preparation_provenance={'preparation_source_file':'missing.xlsx'})]),
        findings='',draft_mapping_review_status='PROVISIONAL',identity_status='NOT_INDEPENDENTLY_VERIFIED',
        raw_file='synthetic.xlsx',sha256='a'*64,raw_header_cell='C1',raw_value_range='C2:C177',
        nonempty_points='176',numeric_points='176',resolved_label='',
        layout_source='plan.xlsx#A1',uploaded_master_reference='master.xlsx#row=2',draft_reference='draft.csv#row=2')


class ContractTests(unittest.TestCase):
    def test_provisional_claims_and_missing_components_preserved(self):
        row=evidence(); original=copy.deepcopy(row)
        out=d.candidate_row(row,True)
        self.assertTrue(out['candidate_included'])
        self.assertFalse(out['physical_label_verified'])
        self.assertEqual(out['label_status'],'provisional_reconstructed')
        self.assertEqual(out['component_claims_ppm']['TFA'],'')
        self.assertEqual(out['label_claim'],'PFHxA')
        self.assertEqual(out['concentration_claim_ppm'],'5')
        self.assertEqual(out['source_evidence'],original)
        self.assertEqual(row,original)
        self.assertEqual(out['preparation_group'],'UNKNOWN')
        self.assertIn('historically_exposed',out['proposed_role'])

    def test_exclusions_review_and_locked_roles(self):
        for condition,partition,qc in [('All6_QC','qc','include'),('M23','mixture_train','include'),
                                       ('TFA_20','individual_dataset','exclude')]:
            self.assertFalse(d.candidate_row(evidence(condition=condition,partition=partition,qc=qc),True)['candidate_included'])
        out=d.candidate_row(evidence(exp='Exp3',qc='review'),True)
        self.assertTrue(out['candidate_included'])
        self.assertIn('qc_review',out['warnings'])
        out=d.candidate_row(evidence(exp='Exp8'),True)
        self.assertTrue(out['locked'])
        self.assertIn('locked',out['proposed_role'])
        self.assertFalse(d.candidate_row(evidence(),False)['candidate_included'])

    def test_replicates_share_proxy_not_independent_preparations(self):
        a=d.candidate_row(evidence(well='A1'),True)
        b=d.candidate_row(evidence(well='A2'),True)
        self.assertEqual(a['technical_replicate_group'],b['technical_replicate_group'])
        self.assertFalse(a['group_independence_verified'])

    def test_raw_schema_and_source_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'raw.xlsx'; workbook(p)
            before=p.read_bytes(); raw=read_raw(p)
            self.assertEqual(raw['A1']['values'],[1.0]*176)
            self.assertIsNone(raw['A2']['values'])
            self.assertEqual(raw['A1']['raw_value_range'],'C2:C177')
            self.assertEqual(before,p.read_bytes())

    def test_bad_raw_grid_headers_partial_and_nonfinite(self):
        changes=[lambda c:c.update(A2=351),lambda c:c.update(D1='A1'),
                 lambda c:c.pop('C5'),lambda c:c.update(C5=float('nan'))]
        with tempfile.TemporaryDirectory() as tmp:
            for change in changes:
                p=Path(tmp)/'bad.xlsx'; workbook(p,change)
                with self.assertRaises(ValueError): read_raw(p)

    def test_hash_mismatch_and_duplicate_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'raw'; p.write_bytes(b'synthetic')
            self.assertEqual(d.verify_hash(p,hashlib.sha256(b'synthetic').hexdigest()),hashlib.sha256(b'synthetic').hexdigest())
            with self.assertRaises(ValueError): d.verify_hash(p,'0'*64)
        with self.assertRaises(ValueError): d.index_evidence([evidence(),evidence()])

    def test_output_safety(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'source'; root.mkdir()
            for out in [root,root/'output',Path(tmp)]:
                with self.assertRaises(ValueError): d.validate_output(out,[root])
            d.validate_output(Path(tmp)/'fresh',[root])

    def test_conflicting_individual_claims_are_flagged_not_adjudicated(self):
        row=evidence(); row['master_composition_ppm']=json.dumps({'PFHxA':'20','TFA':'0'})
        out=d.candidate_row(row,True)
        self.assertIn('condition_component_disagreement',out['warnings'])
        self.assertEqual(out['concentration_claim_ppm'],'5')
        self.assertEqual(out['component_claims_ppm']['PFHxA'],'20')
        self.assertFalse(out['candidate_included'])

    def test_manifest_end_to_end_determinism_and_count_stop(self):
        import csv
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); raw=root/'raw'; raw.mkdir()
            bundle=root/'bundle'; bundle.mkdir()
            records=root/'records'; records.mkdir()
            marker=bundle/'synthetic.txt'; marker.write_text('synthetic provenance')
            with (bundle/'SHA256SUMS.csv').open('w',newline='') as f:
                writer=csv.writer(f); writer.writerow(['zip_relative_path','size_bytes','sha256'])
                writer.writerow([marker.name,marker.stat().st_size,hashlib.sha256(marker.read_bytes()).hexdigest()])
            rows=[]; lines=[]
            for exp,n in [('Exp3',72),('Exp5',53),('Exp8',18)]:
                p=raw/f'{exp} Plt{exp[3:]}.xlsx'
                def populate(c):
                    for col in range(3,n+3):
                        for ri in range(2,178): c[f'{column(col)}{ri}']=1.0
                workbook(p,populate)
                digest=hashlib.sha256(p.read_bytes()).hexdigest(); lines.append(f'{digest}  {p}')
                for index,well in enumerate(d.WELLS):
                    row=evidence(exp=exp,well=well,partition='individual_dataset' if index<n else 'unused',qc='include' if index<n else 'unused')
                    row.update(raw_file=p.name,sha256=digest,raw_header_cell=column(index+3)+'1',
                        raw_value_range=f'{column(index+3)}2:{column(index+3)}177',
                        nonempty_points='176' if index<n else '0',numeric_points='176' if index<n else '0')
                    rows.append(row)
            checks=records/'sha.txt'; checks.write_text('\n'.join(lines)+'\n')
            evidence_path=records/'evidence.csv'
            def write_evidence():
                with evidence_path.open('w',newline='') as f:
                    writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
            write_evidence()
            before={str(p):p.read_bytes() for folder in (raw,bundle,records) for p in folder.iterdir()}
            for output in ('one','two'):
                summary=d.build_manifest(raw,evidence_path,checks,bundle,root/output)
                self.assertEqual(summary['candidate_counts'],{'Exp3':72,'Exp5':53,'Exp8':18})
                self.assertFalse(summary['models_trained'])
            for name in ('candidate_wells.json','candidate_wells.csv','summary.json'):
                self.assertEqual((root/'one'/name).read_bytes(),(root/'two'/name).read_bytes())
            self.assertTrue(all(Path(p).read_bytes()==b for p,b in before.items()))
            rows[0]['historical_qc_status']='exclude'; write_evidence()
            with self.assertRaisesRegex(ValueError,'count discrepancy'):
                d.build_manifest(raw,evidence_path,checks,bundle,root/'bad')
            self.assertFalse((root/'bad').exists())

    def test_preparation_status_is_evidence_not_batch_assumption(self):
        row=evidence(); row['historical_variants']='[]'
        out=d.candidate_row(row,True)
        self.assertEqual(out['preparation_status'],'unknown')
        self.assertIn('preparation_status_missing',out['warnings'])
        row['historical_variants']=json.dumps([{'preparation_status':'reconstructed'}, {'preparation_status':'original'}])
        out=d.candidate_row(row,True)
        self.assertEqual(out['preparation_status'],'conflicting_claims')
        self.assertIn('preparation_status_conflict',out['warnings'])
        self.assertFalse(out['physical_label_verified'])
