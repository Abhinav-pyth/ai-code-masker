import os

file_path = 'd:/mask-unmask/api/index.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Add requests if not there
if 'import requests\n' not in lines:
    lines.insert(4, 'import requests\n')

# Uncomment lines 21 to 121
for i in range(len(lines)):
    if 20 <= i <= 125: # safe range
        if lines[i].startswith('# @app.route'):
            lines[i] = lines[i][2:]
        elif lines[i].startswith('# def '):
            lines[i] = lines[i][2:]
        elif lines[i].startswith('#     return '):
            lines[i] = lines[i][2:]
        elif lines[i] == '# \n':
            lines[i] = '\n'

# Add new routes before if __name__ == '__main__':
new_routes = """
@app.route('/universal-converter')
def universal_converter():
    return render_template('universal_converter.html', active_page='universal_converter')

@app.route('/java-to-json')
def java_to_json():
    return render_template('java_to_json.html', active_page='java_to_json')

@app.route('/aws-cloudwatch')
def aws_cloudwatch():
    return render_template('aws_cloudwatch.html', active_page='aws_cloudwatch')

@app.route('/api/proxy', methods=['POST'])
def api_proxy():
    try:
        data = request.json
        url = data.get('url')
        method = data.get('method', 'GET')
        headers = data.get('headers', {})
        body = data.get('body')

        if not url:
            from flask import jsonify
            return jsonify({"error": "No URL provided"}), 400
        
        headers.pop('Host', None)
        headers.pop('host', None)
        
        if method.upper() == 'GET':
            resp = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            resp = requests.post(url, headers=headers, data=body)
        elif method.upper() == 'PUT':
            resp = requests.put(url, headers=headers, data=body)
        elif method.upper() == 'PATCH':
            resp = requests.patch(url, headers=headers, data=body)
        elif method.upper() == 'DELETE':
            resp = requests.delete(url, headers=headers)
        else:
            from flask import jsonify
            return jsonify({"error": f"Unsupported method {method}"}), 400

        resp_headers = dict(resp.headers)
        resp_headers.pop('Content-Encoding', None)
        resp_headers.pop('Transfer-Encoding', None)
        
        from flask import jsonify
        return jsonify({
            "status": resp.status_code,
            "statusText": resp.reason,
            "headers": resp_headers,
            "text": resp.text
        })
    except Exception as e:
        from flask import jsonify
        return jsonify({"error": str(e)}), 500

"""

# Insert new routes before if __name__ == '__main__':
for i, line in enumerate(lines):
    if line.startswith("if __name__ == '__main__':"):
        lines.insert(i, new_routes)
        break

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
