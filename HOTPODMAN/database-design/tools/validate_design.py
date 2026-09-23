"""Documentation consistency checks only; not PostgreSQL/Prisma validation."""
from pathlib import Path
import ast,json,re,sys
R=Path(__file__).resolve().parents[1]
model=json.loads((R/'model.catalog.json').read_text())
assert model['status']=='DESIGN_ONLY_NOT_MIGRATION'
ts=model['tables'];by={t['name']:t for t in ts};assert len(ts)==len(by)
allowed=re.compile(r'^(uuid|text|jsonb|integer|bigint|boolean|timestamptz|date|inet|char\(3\)|numeric\(\d+,\d+\))$')
refs=0
for t in ts:
    assert re.match(r'^[a-z_]+\.[a-z_]+$',t['name']),t['name']
    assert t['phase'] in {'F','P','W','O','R'}
    assert t['mode'] in {'mutable','append'}
    cols={c['name']:c for c in t['columns']};assert len(cols)==len(t['columns'])
    assert cols['id']['type']=='uuid' and not cols['id']['nullable']
    for c in t['columns']:
        assert allowed.fullmatch(c['type']),c
        if c['reference']:
            parent,key=c['reference'].rsplit('.',1);assert parent in by,(t['name'],parent)
            pc=next(x for x in by[parent]['columns'] if x['name']==key)
            assert pc['type']==c['type'],(t['name'],c)
            refs+=1
    if t['mode']=='append':assert 'updated_at' not in cols and 'version' not in cols
    else:assert 'updated_at' in cols and 'version' in cols
    assert t['keys'] and t['rules'],t['name']
# Dictionary and machine-readable catalog must describe exactly the same tables.
d=(R/'02-data-dictionary.md').read_text()
assert set(re.findall(r'^## `([^`]+)`$',d,re.M))==set(by)
# Check Markdown local links and table shapes; code fences are balanced.
for p in R.glob('*.md'):
    s=p.read_text();assert len(re.findall(r'^```',s,re.M))%2==0,p
    for target in re.findall(r'\]\(([^)]+)\)',s):
        if target.startswith(('http:','https:','#')):continue
        target=target.split('#')[0]
        assert (p.parent/target).exists(),(p,target)
    for b in s.split('\n\n'):
        rows=[l for l in b.splitlines() if l.startswith('|')]
        if rows:assert len({l.count('|') for l in rows})==1,(p,rows[:2])
# Every ER alias names a real table; all diagrams have a rendered SVG.
manifest=json.loads((R/'erd/manifest.json').read_text())
for g in manifest:
    path=R/'erd'/f"{g['name']}.mmd";s=path.read_text()
    assert s.startswith('erDiagram\n')
    aliases=set(re.findall(r'\["([a-z_.]+)"\]',s))
    assert aliases==set(g['tables']) and aliases<=set(by)
    assert path.with_suffix('.svg').exists(),path
    assert '<svg' in path.with_suffix('.svg').read_text()
for p in (R/'tools').glob('*.py'):ast.parse(p.read_text())
# Important user-fixed scope boundaries remain explicit.
main=(R/'README.md').read_text();rules=(R/'03-invariants-and-transactions.md').read_text()
for token in ['Delivery Confirmation ไม่สร้าง Stock Movement','สำนักงานใหญ่','Warehouse Receipt']:
    assert token in main,token
assert 'phase1_work_plan_24-30_sep_2026.md' in (R/'04-migration-and-acceptance.md').read_text()
for table in ['inventory.cost_adjustment_lines','inventory.repack_lines','inventory.count_scope_locks','delivery.acceptance_entries','delivery.line_progress','receiving.receipts']:
    assert table in by
# Address master data must have typed references, not opaque JSON.
for name in ['org.companies','org.branches','catalog.supplier_addresses']:
    cols={c['name']:c for c in by[name]['columns']}
    assert 'address' not in cols
    assert not cols['address_line1']['nullable']
    for field,parent in [('province_id','provinces'),('district_id','districts'),('subdistrict_id','subdistricts'),('postal_code_id','postal_codes')]:
        assert cols[field]['reference']==f'geo.{parent}.id' and not cols[field]['nullable']
for t in ts:
    if t['name'].startswith('geo.'):
        assert not any(c['name']=='company_id' for c in t['columns'])
assert 'U(subdistrict_id,postal_code_id)' in by['geo.subdistrict_postal_codes']['keys']
# Every table and column must retain a Thai explanation and a SQL comment.
comments=(R/'comments.th.sql').read_text()
assert comments.count('COMMENT ON TABLE ')==len(ts)
assert comments.count('COMMENT ON COLUMN ')==sum(len(t['columns']) for t in ts)
for t in ts:
    assert t['primary_key']==['id']
    assert re.search('[ก-๙]',t['comment_th'])
    for c in t['columns']:
        assert re.search('[ก-๙]',c['comment_th']), (t['name'],c['name'])
        assert c['key_role']==('PK' if c['name']=='id' else 'FK' if c['reference'] else '—')
        if c['type']=='timestamptz': assert 'UTC' in c['comment_th'] and 'Asia/Bangkok' in c['comment_th']
        if c['type']=='date': assert 'ไม่มีเวลา' in c['comment_th']
        target='.'.join('"'+n+'"' for n in (t['name']+'.'+c['name']).split('.'))
        assert f'COMMENT ON COLUMN {target} IS ' in comments
assert 'timestamp' not in {c['type'] for t in ts for c in t['columns']}
print(f"PASS: Thai comments for {len(ts)} tables and {sum(len(t['columns']) for t in ts)} columns; PK/FK/type/timezone annotations and SQL comment coverage")
# These are explanatory arithmetic examples, not evidence of DB enforcement.
assert 10-8-0==2 and 8-0-0==8
assert 10-7-0==3 and 8-5-0==3
assert 7+2+1==10 and 7/10*100==70
print(f'PASS: {len(ts)} tables, {sum(len(t["columns"]) for t in ts)} columns, {refs} FK targets, {len(manifest)} rendered ERDs')
print('PASS: dictionary/catalog agreement, links, Markdown tables/fences, Python syntax, user scope anchors')
print('NOT RUN: PostgreSQL migrations, DB constraints, Prisma validation, concurrency/performance tests')
