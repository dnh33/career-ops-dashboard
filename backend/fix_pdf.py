with open('/opt/career-ops-dashboard/backend/app/services/pdf/cv_pdf.py', 'r') as f:
    content = f.read()

# Fix the corrupted HTML entity escapes
content = content.replace('.replace("&", "&")', '.replace("&", "&")')
content = content.replace('.replace("<", "<")', '.replace("<", "<")')
content = content.replace('.replace(">", ">")', '.replace(">", ">")')
content = content.replace('.replace(\'"\', """")', '.replace(\'"\', """)')
content = content.replace('.replace("\'", "\'\'\'")', '.replace("\'", "\'")')

with open('/opt/career-ops-dashboard/backend/app/services/pdf/cv_pdf.py', 'w') as f:
    f.write(content)

print('Fixed')