import requests
import sys

endpoints = [
    {"path": "", "expected_status": 200, "expected_content": "AI Code Masker"},
    {"path": "pricing", "expected_status": 200, "expected_content": "Pricing"},
    {"path": "blog", "expected_status": 200, "expected_content": "Blog"},
    {"path": "blog/how-to-hide-api-keys-before-chatgpt", "expected_status": 200, "expected_content": "API Key"},
    {"path": "tools/json-formatter", "expected_status": 200, "expected_content": "JSON Formatter"},
    {"path": "sitemap.xml", "expected_status": 200, "expected_content": "<urlset"},
    {"path": "robots.txt", "expected_status": 200, "expected_content": "Sitemap:"}
]

failed = False
print("=== STARTING ENDPOINT VERIFICATION ===")
for ep in endpoints:
    url = f"http://127.0.0.1:3000/{ep['path']}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != ep["expected_status"]:
            print(f"[FAIL] {url} - Expected status {ep['expected_status']}, got {r.status_code}")
            failed = True
        elif ep["expected_content"] not in r.text:
            print(f"[FAIL] {url} - Expected keyword '{ep['expected_content']}' not found in response body")
            failed = True
        else:
            print(f"[OK]   {url} - Status: {r.status_code}, Verification string found!")
    except Exception as e:
        print(f"[FAIL] {url} - Request failed: {str(e)}")
        failed = True

print("=== VERIFICATION COMPLETE ===")
if failed:
    sys.exit(1)
else:
    sys.exit(0)
