"""Strict, read-only reader for the audited SpectraMax Sheet1 export schema."""
import math
import posixpath
import re
import zipfile
from xml.etree import ElementTree as ET
from .spectral import GRID

NS = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
WELLS = tuple(f'{r}{c}' for r in 'ABCDEFGH' for c in range(1,13))


def _column(n):
    out = ''
    while n:
        n, remainder = divmod(n-1,26)
        out = chr(65+remainder)+out
    return out


def read_raw(path):
    """Return all 96 physical wells; empty columns have values=None, never zeros."""
    with zipfile.ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels = {x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheets = ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS)
        if sheets is None or len(sheets)!=1 or sheets[0].get('name')!='Sheet1':
            raise ValueError('Expected only Sheet1 in raw export')
        rid=sheets[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        target=rels[rid]
        member=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
        cells={}
        for c in ET.fromstring(z.read(member)).findall('s:sheetData/s:row/s:c',NS):
            ref=c.get('r')
            if ref in cells or not re.fullmatch(r'[A-Z]+[1-9][0-9]*',ref or ''):
                raise ValueError('Duplicate or invalid cell coordinate')
            if c.find('s:f',NS) is not None:
                raise ValueError('Raw formulas are unsupported; no cached-value inference')
            v=c.find('s:v',NS)
            value=v.text if v is not None and v.text is not None else ''
            if c.get('t')=='s': value=strings[int(value)]
            elif c.get('t')=='inlineStr': value=''.join(c.find('s:is',NS).itertext())
            elif c.get('t') in ('e','b') and value:
                raise ValueError('Error/boolean cell in raw export')
            cells[ref]=value
    allowed={f'{_column(col)}{row}' for col in range(1,99) for row in range(1,178)}
    if any(v!='' and k not in allowed for k,v in cells.items()):
        raise ValueError('Unexpected populated cell outside audited schema')
    headers=[cells.get(_column(i)+'1','') for i in range(3,99)]
    if headers!=list(WELLS):
        raise ValueError('Expected 96 ordered unique A1:H12 well headings')
    try:
        waves=tuple(float(cells.get(f'A{i}','')) for i in range(2,178))
    except ValueError as exc:
        raise ValueError('Missing/nonnumeric wavelength') from exc
    if waves!=GRID:
        raise ValueError('Unexpected wavelength grid')
    result={}
    for i,well in enumerate(WELLS,3):
        col=_column(i)
        values=[cells.get(f'{col}{r}','') for r in range(2,178)]
        count=sum(v!='' for v in values)
        if count not in (0,176): raise ValueError(f'Partial spectrum: {well}')
        if count:
            values=[float(v) for v in values]
            if not all(math.isfinite(v) for v in values):
                raise ValueError(f'Nonfinite spectrum: {well}')
        result[well]={'values':values if count else None,'point_count':count,
                      'raw_header_cell':f'{col}1','raw_value_range':f'{col}2:{col}177'}
    return result
