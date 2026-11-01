
import xml.etree.ElementTree as ET
from pathlib import Path
from html import escape
from datetime import datetime, timezone

REPORT_DIR = Path("reports")
OUTPUT_FILE = REPORT_DIR / "API-Quality-Hub-Complete-Report.html"

collection_names = {
    "authentication": "Authentication",
    "cart": "Cart Management",
    "integration": "Integration Testing",
    "product": "Product Management",
    "regression": "Regression Testing",
    "users": "User Management"
}

def parse_junit(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    suites = (
        list(root.iter("testsuite"))
        if root.tag == "testsuites"
        else [root]
    )

    result = {
        "tests": 0,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "duration": 0.0,
        "cases": []
    }

    for suite in suites:
        result["tests"] += int(suite.get("tests", 0))
        result["failures"] += int(suite.get("failures", 0))
        result["errors"] += int(suite.get("errors", 0))
        result["skipped"] += int(suite.get("skipped", 0))
        result["duration"] += float(suite.get("time", 0))

        for case in suite.findall("testcase"):
            failure = case.find("failure")
            error = case.find("error")
            skipped = case.find("skipped")

            status = "Passed"
            details = ""

            if failure is not None:
                status = "Failed"
                details = failure.get("message", "") or failure.text or ""
            elif error is not None:
                status = "Error"
                details = error.get("message", "") or error.text or ""
            elif skipped is not None:
                status = "Skipped"
                details = skipped.get("message", "") or ""

            result["cases"].append({
                "name": case.get("name", "Unnamed test"),
                "suite": case.get("classname", ""),
                "duration": float(case.get("time", 0)),
                "status": status,
                "details": details
            })

    return result


collections = []
missing_files = []

for key, name in collection_names.items():
    file_path = REPORT_DIR / f"{key}-results.xml"

    if not file_path.exists():
        missing_files.append(name)
        continue

    try:
        collections.append({
            "name": name,
            "data": parse_junit(file_path)
        })
    except (ET.ParseError, ValueError, OSError) as exc:
        print(f"Could not read {file_path}: {exc}")
        missing_files.append(name)

total_tests = sum(c["data"]["tests"] for c in collections)
total_failures = sum(c["data"]["failures"] for c in collections)
total_errors = sum(c["data"]["errors"] for c in collections)
total_skipped = sum(c["data"]["skipped"] for c in collections)
total_duration = sum(c["data"]["duration"] for c in collections)

total_passed = max(
    0,
    total_tests - total_failures - total_errors - total_skipped
)

pass_rate = (
    total_passed / total_tests * 100
    if total_tests else 0
)

rows = ""
details = ""

for collection in collections:
    data = collection["data"]
    passed = max(
        0,
        data["tests"] - data["failures"]
        - data["errors"] - data["skipped"]
    )

    rows += f"""
    <tr>
      <td>{escape(collection['name'])}</td>
      <td>{data['tests']}</td>
      <td class="passed">{passed}</td>
      <td class="failed">{data['failures']}</td>
      <td>{data['errors']}</td>
      <td>{data['skipped']}</td>
      <td>{data['duration']:.2f}s</td>
    </tr>
    """

    for case in data["cases"]:
        status_class = case["status"].lower()

        details += f"""
        <tr>
          <td>{escape(collection['name'])}</td>
          <td>{escape(case['suite'])}</td>
          <td>{escape(case['name'])}</td>
          <td class="{status_class}">{escape(case['status'])}</td>
          <td>{case['duration']:.3f}s</td>
          <td>{escape(case['details'])}</td>
        </tr>
        """

timestamp = datetime.now(timezone.utc).strftime(
    "%Y-%m-%d %H:%M:%S UTC"
)

missing_html = ""

if missing_files:
    missing_html = (
        "<p class='warning'>Missing reports: "
        + escape(", ".join(missing_files))
        + "</p>"
    )

if not collections:
    missing_html += (
        "<p class='warning'>No valid JUnit reports were found.</p>"
    )

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>API Quality Hub - Complete Report</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f4f6f9;
  color: #202938;
  margin: 0;
  padding: 25px;
}}
.container {{
  max-width: 1250px;
  margin: auto;
}}
header, .card, .panel {{
  background: white;
  padding: 22px;
  border-radius: 10px;
  margin-bottom: 20px;
}}
h1 {{ margin-bottom: 5px; }}
.muted {{ color: #687386; }}
.metrics {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}}
.metric {{
  background: white;
  padding: 20px;
  border-radius: 10px;
}}
.metric strong {{
  display: block;
  font-size: 28px;
  margin-top: 8px;
}}
.passed {{ color: #16834a; }}
.failed, .error {{ color: #c0392b; }}
.skipped {{ color: #9a6700; }}
.warning {{
  background: #fff4d6;
  padding: 12px;
  border-radius: 6px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
}}
th, td {{
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid #e5e8ed;
  vertical-align: top;
}}
th {{ background: #f0f3f7; }}
.table-wrap {{ overflow-x: auto; }}
</style>
</head>
<body>
<div class="container">
<header>
  <h1>API Quality Hub</h1>
  <h2>Consolidated API Test Execution Report</h2>
  <p class="muted">Generated: {timestamp}</p>
  <p class="muted">Collections with valid reports: {len(collections)}</p>
  {missing_html}
</header>

<div class="metrics">
  <div class="metric">Total Tests<strong>{total_tests}</strong></div>
  <div class="metric">Passed<strong class="passed">{total_passed}</strong></div>
  <div class="metric">Failed<strong class="failed">{total_failures}</strong></div>
  <div class="metric">Errors<strong>{total_errors}</strong></div>
  <div class="metric">Skipped<strong>{total_skipped}</strong></div>
  <div class="metric">Pass Rate<strong>{pass_rate:.2f}%</strong></div>
</div>

<section class="panel">
  <h2>Collection-wise Summary</h2>
  <div class="table-wrap">
  <table>
    <tr>
      <th>Collection</th><th>Tests</th><th>Passed</th>
      <th>Failed</th><th>Errors</th><th>Skipped</th>
      <th>Duration</th>
    </tr>
    {rows}
  </table>
  </div>
  <p><strong>Total reported collection duration:</strong>
  {total_duration:.2f} seconds</p>
</section>

<section class="panel">
  <h2>Individual Test Case Details</h2>
  <div class="table-wrap">
  <table>
    <tr>
      <th>Collection</th><th>Suite</th><th>Test Case</th>
      <th>Status</th><th>Duration</th><th>Failure Details</th>
    </tr>
    {details}
  </table>
  </div>
</section>

<footer class="muted">
  API Quality Hub | Automated report generated from JUnit XML results.
  Missing reports are not counted as passing tests.
</footer>
</div>
</body>
</html>
"""

REPORT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(html, encoding="utf-8")

print(f"Consolidated report created: {OUTPUT_FILE}")
print(f"Collections found: {len(collections)}")
print(f"Tests: {total_tests}")
print(f"Passed: {total_passed}")
print(f"Failed: {total_failures}")
print(f"Errors: {total_errors}")
print(f"Skipped: {total_skipped}")
print(f"Pass rate: {pass_rate:.2f}%")
