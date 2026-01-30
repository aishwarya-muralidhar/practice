import glob
import importlib.util
import inspect
import traceback
import xml.etree.ElementTree as ET
from datetime import datetime

def load_module_from_path(path):
    name = path.replace('/', '.').rstrip('.py')
    spec = importlib.util.spec_from_file_location(path, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

results = []

for path in glob.glob('test_*.py'):
    mod = load_module_from_path(path)
    for name, func in inspect.getmembers(mod, inspect.isfunction):
        if name.startswith('test_'):
            start = datetime.now()
            try:
                func()
                elapsed = (datetime.now() - start).total_seconds()
                results.append((path, name, 'passed', '', elapsed))
                print(f"PASS: {path}::{name}")
            except Exception as e:
                elapsed = (datetime.now() - start).total_seconds()
                tb = traceback.format_exc()
                results.append((path, name, 'failed', tb, elapsed))
                print(f"FAIL: {path}::{name}\n{tb}")

# Write a simple JUnit XML report
tests = len(results)
failures = sum(1 for r in results if r[2] == 'failed')
testsuite = ET.Element('testsuite', attrib={
    'name': 'pytest_fallback',
    'tests': str(tests),
    'failures': str(failures),
    'timestamp': datetime.now().isoformat()
})

for path, name, status, tb, elapsed in results:
    case = ET.SubElement(testsuite, 'testcase', attrib={'classname': path, 'name': name, 'time': f"{elapsed:.3f}"})
    if status == 'failed':
        failure = ET.SubElement(case, 'failure')
        failure.text = tb

tree = ET.ElementTree(testsuite)
tree.write('report.xml', encoding='utf-8', xml_declaration=True)

print(f"\nRan {tests} tests: {tests-failures} passed, {failures} failed")
print('Wrote report.xml')
