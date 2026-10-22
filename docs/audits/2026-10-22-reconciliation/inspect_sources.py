import csv, hashlib, json, posixpath, re, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read_xlsx(p):
    out = {}
    with zipfile.ZipFile(p) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels = {x.attrib['Id']: x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets', NS):
            rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target = rels[rid]
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            rows = []
            for row in ET.fromstring(z.read(target)).findall('s:sheetData/s:row', NS):
                cells = {}
                for c in row:
                    v = c.find('s:v', NS)
                    val = v.text if v is not None else ''
                    if c.get('t') == 's': val = strings[int(val)]
                    if c.get('t') == 'inlineStr': val = ''.join(c.find('s:is', NS).itertext())
                    cells[c.get('r')] = val
                rows.append({'row': int(row.get('r')), 'cells': cells})
            out[sheet.get('name')] = rows
    return out

if __name__ == '__main__':
    raw, evidence, dest = map(Path, sys.argv[1:])
    dest.mkdir(parents=True, exist_ok=True)
    before = {str(p): sha(p) for root in (raw,evidence) for p in sorted(root.rglob('*')) if p.is_file()}
    manifest = list(csv.DictReader((evidence/'SHA256SUMS.csv').open()))
    checks = [{'path':r['zip_relative_path'], 'sha256':sha(evidence/r['zip_relative_path']), 'hash_match':sha(evidence/r['zip_relative_path'])==r['sha256'], 'size_match':(evidence/r['zip_relative_path']).stat().st_size==int(r['size_bytes'])} for r in manifest]
    (dest/'hash_checks.json').write_text(json.dumps({'inputs':before,'bundle_checks':checks},indent=2))
    print('Bundle hashes/sizes:',len(checks),all(r['hash_match'] and r['size_match'] for r in checks))
    books = {}
    for root in (raw,evidence):
        for p in sorted(root.rglob('*.xlsx')):
            books[str(p)] = read_xlsx(p)
    (dest/'extracted.json').write_text(json.dumps(books,indent=2))
    for path, sheets in books.items():
        print('\nFILE',path)
        for name, rows in sheets.items():
            print(name,len(rows),'rows',str(rows[:2])[:1200])
    assert before == {p:sha(Path(p)) for p in before}, 'Input changed during inspection'
