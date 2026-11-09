"""Fabricated mapping/raw workbook fixtures only; never copies real records."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from scientific_experiment_selection.raw_label_join import audit_join, read_mapping, run_audit
from scientific_experiment_selection.nes_protocol import SPECIES
from test_dataset_contract import workbook


def mapping():
    rows=[]
    for exp,order,nrep in [('Exp3',SPECIES,4),('Exp5',tuple(reversed(SPECIES)),3)]:
        for ri,p in enumerate(order):
            for col in range(1,13):
                individual=col<=3*nrep
                level=(5,10,20)[(col-1)//nrep] if individual else None
                # Exp3 synthetic row layouts are nominal public rules; Exp5 is
                # deliberately reversed (not the actual plate's hidden mapping).
                condition=f'{p}_{level}' if individual else 'synthetic_control'
                qc='exclude' if exp=='Exp5' and ri==1 and col==7 else 'include'
                row=dict(experiment_id=exp,well=f'{chr(65+ri)}{col}',sample_type='individual_pfas' if individual else 'qc',
                    condition_code=condition,model_partition='individual_train' if exp=='Exp3' else 'individual_external_test',
                    qc_status=qc,has_spectrum='True',analysis_group_id=f'{exp}:{condition}',
                    tfa_present=str(individual and p=='TFA'))
                row.update({f'{name}_ppm':str(level if individual and name==p else 0) for name in SPECIES})
                rows.append(row)
        for r in 'GH':
            for col in range(1,13):
                rows.append(dict(experiment_id=exp,well=f'{r}{col}',sample_type='qc',condition_code='synthetic_control',
                    model_partition='qc',qc_status='include',has_spectrum='True',analysis_group_id='control',tfa_present='False',
                    **{f'{name}_ppm':'0' for name in SPECIES}))
    # Synthetic expected exclusion B7 must be a TFA20 condition; swap entire Exp5
    # nominal rows to make the public exclusion shape fit without real input.
    exp5=[r for r in rows if r['experiment_id']=='Exp5']
    tfa_row=next(r['well'][0] for r in exp5 if r['condition_code']=='TFA_5')
    for r in exp5:
        if r['well'].startswith(tfa_row):r['well']='B'+r['well'][1:]
        elif r['well'].startswith('B'):r['well']=tfa_row+r['well'][1:]
        r['qc_status']='exclude' if r['well']=='B7' else 'include'
    return rows


def raw_metadata():
    return {exp:{f'{r}{c}':{'values':[1.]*176,'point_count':176} for r in 'ABCDEFGH' for c in range(1,13)} for exp in ('Exp3','Exp5')}


def write_mapping(path,rows):
    ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    def col(i):
        out=''
        while i:i,r=divmod(i-1,26);out=chr(65+r)+out
        return out
    fields=list(rows[0]);xml=[]
    for n,values in enumerate([fields]+[[r.get(k,'') for k in fields] for r in rows],1):
        cells=''.join(f'<c r="{col(i)}{n}" t="inlineStr"><is><t>{v}</t></is></c>' for i,v in enumerate(values,1))
        xml.append(f'<row r="{n}">{cells}</row>')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('xl/workbook.xml',f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Well_Metadata" sheetId="1" r:id="rId1"/><sheet name="Private_Forbidden" sheetId="2" r:id="rId2"/></sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels','<Relationships><Relationship Id="rId1" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Target="worksheets/forbidden.xml"/></Relationships>')
        z.writestr('xl/worksheets/sheet1.xml',f'<worksheet xmlns="{ns}"><sheetData>'+''.join(xml)+'</sheetData></worksheet>')
        z.writestr('xl/worksheets/forbidden.xml','PRIVATE_CANARY_INVALID_XML')


class JoinTests(unittest.TestCase):
    def test_mapping_source_unchanged_aggregate_contract_and_exclusions(self):
        rows=mapping();before=copy.deepcopy(rows)
        result=audit_join(rows,raw_metadata())
        self.assertEqual(result['mismatches'],{})
        self.assertEqual(result['counts']['training_wells'],70)
        self.assertEqual(result['counts']['acquisition_wells'],35)
        self.assertEqual(result['counts']['holdout_wells'],18)
        self.assertEqual(result['counts']['excluded_wells'],3)
        self.assertEqual(rows,before)
        self.assertFalse(result['training_permission'])

    def test_duplicate_missing_raw_and_condition_or_role_errors_report_categories(self):
        for mutate in [lambda r:r.append(copy.deepcopy(r[0])),lambda r:r.pop(0),
                       lambda r:r[0].update(condition_code='PRIVATE_CANARY'),
                       lambda r:r[0].update(model_partition='qc'),
                       lambda r:r[0].update(TFA_ppm='20')]:
            rows=mapping();mutate(rows)
            out=audit_join(rows,raw_metadata())
            self.assertEqual(out['status'],'review-needed');self.assertTrue(out['mismatches'])
            self.assertNotIn('PRIVATE_CANARY',json.dumps(out))
        raw=raw_metadata();raw['Exp3'].pop('A1')
        self.assertIn('raw_column_absent',audit_join(mapping(),raw)['mismatches'])
        raw=raw_metadata();raw['Exp3']['A1']['point_count']=175
        self.assertIn('raw_presence_or_shape',audit_join(mapping(),raw)['mismatches'])

    def test_nonindividual_never_promoted_by_model_use_flag(self):
        rows=mapping();rows[0].update(sample_type='qc',use_in_model='Yes')
        out=audit_join(rows,raw_metadata())
        self.assertTrue(out['mismatches'])

    def test_foreign_rows_ignored_before_diagnostics(self):
        rows=mapping()+[{'experiment_id':'Exp8','well':'PRIVATE_CANARY'}]
        self.assertEqual(audit_join(rows,raw_metadata()),audit_join(mapping(),raw_metadata()))

    def test_mapping_sheet_only_no_forbidden_sheets_and_foreign_rows(self):
        rows=mapping()+[dict(mapping()[0],experiment_id='Exp8',condition_code='PRIVATE_CANARY')]
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'mapping.xlsx';write_mapping(p,rows)
            before=p.read_bytes();got=read_mapping(p)
            self.assertEqual(len(got),192);self.assertEqual(p.read_bytes(),before)
            self.assertNotIn('PRIVATE_CANARY',json.dumps(audit_join(got,raw_metadata())))

    def test_cli_path_and_raw_schema_errors_are_redacted(self):
        import os,subprocess,sys
        with tempfile.TemporaryDirectory(prefix='PRIVATE_CANARY') as tmp:
            p=Path(tmp)/'missing.xlsx'
            r=subprocess.run([sys.executable,'-m','scientific_experiment_selection.raw_label_join','--mapping',str(p),
                '--raw-root',tmp,'--raw-checksums',str(p),'--mapping-checksums',str(p)],capture_output=True,text=True,
                env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
            self.assertEqual(r.returncode,2);self.assertNotIn('PRIVATE_CANARY',r.stdout+r.stderr)
            self.assertEqual(json.loads(r.stdout)['status'],'review-needed')

    def test_end_to_end_checksums_raw_grid_and_no_exp8_open(self):
        import hashlib,csv
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);raw=root/'raw';raw.mkdir()
            evidence=root/'evidence';evidence.mkdir()
            m=evidence/'mapping.xlsx';write_mapping(m,mapping())
            mc=evidence/'SHA256SUMS.csv'
            with mc.open('w',newline='') as f:
                w=csv.writer(f);w.writerow(['zip_relative_path','size_bytes','sha256'])
                w.writerow([m.name,m.stat().st_size,hashlib.sha256(m.read_bytes()).hexdigest()])
            def populate(cells):
                from test_dataset_contract import column
                for col in range(3,99):
                    for row in range(2,178):cells[f'{column(col)}{row}']=1.
            checks=[]
            for exp in ('Exp3','Exp5'):
                p=raw/f'{exp} Plt{exp[3:]}.xlsx';workbook(p,populate)
                checks.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p))
            # This unreadable sentinel would break the audited parser if opened.
            (raw/'Exp8 Plt8.xlsx').write_bytes(b'PRIVATE_CANARY_NOT_A_WORKBOOK')
            rc=root/'raw_hashes.txt';rc.write_text('\n'.join(checks)+'\n')
            before={p:p.read_bytes() for p in (m,mc,rc,raw/'Exp3 Plt3.xlsx',raw/'Exp5 Plt5.xlsx')}
            out=run_audit(m,raw,rc,mc)
            self.assertEqual(out['mismatches'],{})
            self.assertEqual(out['counts']['joined_wells'],123)
            self.assertTrue(out['source_bytes_unchanged'])
            self.assertTrue(all(p.read_bytes()==v for p,v in before.items()))
            rc.write_text('0'*64+'  Exp3 Plt3.xlsx\n'+checks[1]+'\n')
            self.assertIn('raw_provenance_mismatch',run_audit(m,raw,rc,mc)['mismatches'])
            def bad_grid(cells):
                populate(cells);cells['A2']=351
            p=raw/'Exp3 Plt3.xlsx';workbook(p,bad_grid)
            rc.write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n'+checks[1]+'\n')
            self.assertIn('raw_schema_or_numeric_error',run_audit(m,raw,rc,mc)['mismatches'])
            self.assertNotIn('PRIVATE_CANARY',json.dumps(out))
