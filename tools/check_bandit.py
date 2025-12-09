import json
import sys

file_path = sys.argv[1]

with open(file_path, 'r') as f:
    report = json.load(f)

high_issues = [i for i in report['results'] if i['issue_severity'] == 'HIGH']

if high_issues:
    print("❌ Найдены уязвимости HIGH! Merge запрещён.")
    for i in high_issues:
        print(f"{i['filename']}:{i['line_number']} - {i['issue_text']}")
    sys.exit(1)  # <- вот это блокирует merge
else:
    print("✅ Уязвимостей HIGH не найдено")
    sys.exit(0)
