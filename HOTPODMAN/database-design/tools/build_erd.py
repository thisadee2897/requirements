"""Create readable, bounded-context Mermaid diagrams from the design catalog."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
tables={t['name']:t for t in json.loads((root/'model.catalog.json').read_text())['tables']}
groups=[
('10-addresses','ที่อยู่และรหัสพื้นที่',['geo.provinces','geo.districts','geo.subdistricts','geo.postal_codes','geo.subdistrict_postal_codes','org.companies','org.branches','catalog.supplier_addresses']),
('01-organization-access','องค์กร สมาชิก และสิทธิ์',['org.companies','org.branches','org.warehouses','security.users','security.memberships','security.access_scopes','security.membership_scopes','security.roles','security.permissions','security.role_assignments','security.role_permissions']),
('02-catalog','สินค้า หน่วย Supplier และราคา',['org.branches','catalog.products','catalog.categories','catalog.units','catalog.product_units','catalog.suppliers','catalog.supplier_products','catalog.supplier_prices','catalog.branch_products','catalog.branch_supplier_products']),
('03-purchasing','PO ที่มีรุ่นและการอนุมัติ',['platform.documents','platform.document_lines','purchasing.purchase_orders','purchasing.po_lines','purchasing.po_revisions','purchasing.po_revision_lines','purchasing.po_charges','platform.approval_requests','platform.approval_decisions','purchasing.po_closures','purchasing.po_dispatches','purchasing.delivery_schedules']),
('04-delivery','การยืนยันส่งมอบและปัญหา',['purchasing.purchase_orders','purchasing.po_revision_lines','delivery.confirmations','delivery.confirmation_lines','delivery.issues','delivery.acceptance_entries','delivery.issue_actions','delivery.line_progress','delivery.terminal_resolutions','receiving.receipt_lines']),
('05-receiving','ชั่งรับเข้าคลังและฉลาก',['delivery.confirmations','delivery.confirmation_lines','receiving.receipts','receiving.receipt_lines','receiving.receipt_lots','receiving.receipt_weighings','devices.weighings','devices.devices','inventory.lots','inventory.packages','org.locations','devices.print_jobs','devices.print_attempts']),
('06-ledger','Ledger ต้นทุน และยอดคงเหลือ',['platform.documents','platform.document_lines','inventory.lots','inventory.packages','org.locations','inventory.stock_accounts','inventory.postings','inventory.ledger_entries','inventory.balances','inventory.reservations','inventory.cost_layers','inventory.cost_allocations']),
('07-operations','โอน ตรวจนับ และเบิก',['inventory.stock_accounts','inventory.transfers','inventory.transfer_lines','inventory.transfer_receipts','inventory.count_sessions','inventory.count_lines','inventory.adjustment_lines','withdrawal.requests','withdrawal.request_lines','withdrawal.issue_lines','withdrawal.consumptions','inventory.return_lines']),
('08-processing-claims','แปรรูป คืน Trace และ Claim',['withdrawal.issue_lines','processing.jobs','processing.inputs','processing.outputs','processing.input_dispositions','inventory.return_lines','inventory.waste_lines','inventory.lots','inventory.lot_genealogy','delivery.issues','receiving.variances','purchasing.claims','purchasing.claim_lines','purchasing.claim_settlements','purchasing.supplier_return_lines']),
('09-platform','เอกสาร ไฟล์ Audit และระบบเบื้องหลัง',['platform.documents','platform.document_lines','platform.files','platform.document_files','platform.audit_events','integration.outbox_events','integration.inbox_events','integration.connections','integration.deliveries','reporting.export_jobs','notification.notifications','notification.attempts'])]
def ident(n):
    words=re.split('[._]',n)
    return words[0]+''.join(w.title() for w in words[1:])
(root/'erd').mkdir(exist_ok=True)
sections=[];manifest=[]
for file,title,names in groups:
    out=['erDiagram']
    for name in names:
        t=tables[name];out += [f'    {ident(name)}["{name}"] {{','        uuid id PK']
        chosen=[c for c in t['columns'] if c['name']!='id' and c['reference'] and c['reference'].rsplit('.',1)[0] in names]
        chosen=[c for c in chosen if c['name']!='company_id' or 'org.companies' in names][:(5 if file=='10-addresses' else 3)]
        for c in chosen:out += [f'        uuid {c["name"]} FK']
        out += ['    }']
    for name in names:
        for c in tables[name]['columns']:
            if c['reference']:
                parent=c['reference'].rsplit('.',1)[0]
                if parent in names and parent!=name:
                    parentcard='o|' if c['nullable'] else '||'
                    unique_child=bool(re.search(r'U\(company_id,'+re.escape(c['name'])+r'\)',tables[name]['keys']))
                    childcard='o|' if unique_child else 'o{'
                    out += [f'    {ident(parent)} {parentcard}..{childcard} {ident(name)} : "{c["name"]}"']
    source='\n'.join(out)+'\n';(root/'erd'/f'{file}.mmd').write_text(source)
    sections += [f'### {title}','',f'[เปิดแผนภาพ SVG](erd/{file}.svg) · [Mermaid source](erd/{file}.mmd)','', '```mermaid',source.rstrip(),'```','']
    manifest.append({'name':file,'tables':names})
p=root/'01-architecture-and-erd.md'
s=p.read_text()
start='<!-- GENERATED_DIAGRAMS -->';finish='<!-- END_GENERATED_DIAGRAMS -->'
if finish in s:
    a=s.index(start)+len(start);b=s.index(finish);s=s[:a]+'\n\n'+'\n'.join(sections)+'\n'+s[b:]
else:s=s.replace(start,start+'\n\n'+'\n'.join(sections)+'\n'+finish)
p.write_text(s)
(root/'erd/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'{len(groups)} diagrams generated')
