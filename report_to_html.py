import xml.etree.ElementTree as ET
from pathlib import Path

def escape_html(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;').replace("'", '&#39;'))

def main():
    xml_path = Path('report.xml')
    if not xml_path.exists():
        print('report.xml not found')
        return
    tree = ET.parse(xml_path)
    root = tree.getroot()

    title = root.attrib.get('name', 'Test Report')
    total = root.attrib.get('tests', '0')
    failures = root.attrib.get('failures', '0')
    timestamp = root.attrib.get('timestamp', '')

    rows = []
    for case in root.findall('testcase'):
        classname = case.attrib.get('classname', '')
        name = case.attrib.get('name', '')
        time = case.attrib.get('time', '0')
        failure = case.find('failure')
        status = 'failed' if failure is not None else 'passed'
        details = escape_html(failure.text) if failure is not None and failure.text else ''
        rows.append((classname, name, time, status, details))

    html = [
        '<!doctype html>',
        '<html lang="en">',
        '<head><meta charset="utf-8"><title>Test Report</title>',
        '<style>body{font-family:Arial,Helvetica,sans-serif;padding:20px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:8px;text-align:left}th{background:#f6f6f6}tr.fail td{background:#ffecec}</style>',
        '</head>',
        '<body>',
        f'<h1>{escape_html(title)}</h1>',
        f'<p><strong>Timestamp:</strong> {escape_html(timestamp)}</p>',
        f'<p><strong>Totals:</strong> {total} tests, {failures} failures</p>',
        '<table>',
        '<thead><tr><th>File</th><th>Test</th><th>Time (s)</th><th>Status</th><th>Details</th></tr></thead>',
        '<tbody>'
    ]

    for classname, name, time, status, details in rows:
        tr_class = ' class="fail"' if status == 'failed' else ''
        html.append(f'<tr{tr_class}><td>{escape_html(classname)}</td><td>{escape_html(name)}</td><td>{escape_html(time)}</td><td>{escape_html(status)}</td><td><pre>{details}</pre></td></tr>')

    html.extend(['</tbody>', '</table>', '</body>', '</html>'])

    out = Path('report.html')
    out.write_text('\n'.join(html), encoding='utf-8')
    print('Wrote report.html')

if __name__ == '__main__':
    main()
