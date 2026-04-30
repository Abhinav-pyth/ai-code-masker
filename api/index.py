import sys
import os
import json
import socket
import ipaddress
import requests
from flask import Flask, request, jsonify, render_template
from urllib.parse import urlparse

# Local directory addition for module discovery
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    import masker_logic
except ImportError:
    # Handle Vercel's package structure variant
    from . import masker_logic

app = Flask(__name__)

ALLOWED_PROXY_METHODS = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}
BLOCKED_PROXY_HEADERS = {
    'host',
    'content-length',
    'transfer-encoding',
    'connection',
    'accept-encoding'
}
MAX_PROXY_BODY_BYTES = 200_000
MAX_PROXY_RESPONSE_BYTES = 1_000_000
PROXY_TIMEOUT_SECONDS = 15


def _is_public_target(hostname):
    if not hostname:
        return False

    normalized = hostname.strip().lower().strip('[]')
    if normalized in {'localhost', 'localhost.localdomain'} or normalized.endswith('.local'):
        return False

    try:
        addresses = [ipaddress.ip_address(normalized)]
    except ValueError:
        try:
            infos = socket.getaddrinfo(normalized, None, type=socket.SOCK_STREAM)
        except socket.gaierror:
            return False

        addresses = []
        for info in infos:
            try:
                addresses.append(ipaddress.ip_address(info[4][0]))
            except ValueError:
                return False

    return bool(addresses) and all(address.is_global for address in addresses)


def _validate_proxy_url(url):
    parsed = urlparse(url or '')
    if parsed.scheme not in {'http', 'https'} or not parsed.netloc:
        return None, 'Only absolute http:// or https:// URLs are supported.'

    if not _is_public_target(parsed.hostname):
        return None, 'Private, local, and reserved network targets are not allowed through the public proxy.'

    return parsed.geturl(), None


def _clean_proxy_headers(headers):
    if not isinstance(headers, dict):
        return {}

    cleaned = {}
    for key, value in headers.items():
        if not isinstance(key, str):
            continue

        header_name = key.strip()
        if not header_name or '\n' in header_name or '\r' in header_name:
            continue

        if header_name.lower() in BLOCKED_PROXY_HEADERS:
            continue

        cleaned[header_name] = str(value)

    return cleaned

@app.route('/')
def index():
    return render_template('index.html', active_page='masker')

@app.route('/robots.txt')
def robots():
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/google0118da07594017cd.html')
def google_verification():
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.root_path, 'static'), 'google0118da07594017cd.html')

# Commented out other tool routes as per user request to focus on Masker
@app.route('/json-editor')
def json_editor():
    return render_template('json_editor.html', active_page='json_editor')

@app.route('/base64')
def base64_tool():
    return render_template('base64.html', active_page='base64')

@app.route('/base64-to-pdf')
def base64_to_pdf():
    return render_template('base64_to_pdf.html', active_page='base64_to_pdf')

@app.route('/base64-to-image')
def base64_to_image():
    return render_template('base64_to_image.html', active_page='base64_to_image')

@app.route('/image-resize')
def image_resize():
    return render_template('image_resize.html', active_page='image_resize')

@app.route('/pixel-editor')
def pixel_editor():
    return render_template('image_pixels.html', active_page='image_pixels')

@app.route('/image-converter')
def image_converter():
    return render_template('image_converter.html', active_page='image_converter')

@app.route('/hex-rgb')
def hex_rgb():
    return render_template('hex_rgb.html', active_page='hex_rgb')

@app.route('/spell-checker')
def spell_checker():
    return render_template('spell_checker.html', active_page='spell_checker')

@app.route('/translator')
def translator():
    return render_template('translator.html', active_page='translator')

@app.route('/email-formation')
def email_formation():
    return render_template('email_formation.html', active_page='email_formation')

@app.route('/sentence-formation')
def sentence_formation():
    return render_template('sentence_formation.html', active_page='sentence_formation')

@app.route('/naming-suggestions')
def naming_suggestions():
    return render_template('naming_suggestions.html', active_page='naming_suggestions')

@app.route('/sql-optimizer')
def sql_optimizer():
    return render_template('sql_optimizer.html', active_page='sql_optimizer')

@app.route('/my-ip')
def my_ip():
    return render_template('my_ip.html', active_page='my_ip')

@app.route('/domain-to-ip')
def domain_to_ip():
    return render_template('domain_to_ip.html', active_page='domain_to_ip')

@app.route('/api-tester')
def api_tester():
    return render_template('api_tester.html', active_page='api_tester')

@app.route('/clinical-parser')
def clinical_parser():
    return render_template('clinical_parser.html', active_page='clinical_parser')

@app.route('/url-encoder')
def url_encoder():
    return render_template('url_encoder.html', active_page='url_encoder')

@app.route('/case-converter')
def case_converter():
    return render_template('case_converter.html', active_page='case_converter')

@app.route('/qr-generator')
def qr_generator():
    return render_template('qr_generator.html', active_page='qr_generator')

@app.route('/jwt-tool')
def jwt_tool():
    return render_template('jwt_tool.html', active_page='jwt_tool')

@app.route('/html-preview')
def html_preview():
    return render_template('html_preview.html', active_page='html_preview')

@app.route('/js-executor')
def js_executor():
    return render_template('js_executor.html', active_page='js_executor')

@app.route('/lorem-ipsum')
def lorem_ipsum():
    return render_template('lorem_ipsum.html', active_page='lorem_ipsum')

@app.route('/dummy-data')
def dummy_data():
    return render_template('dummy_data.html', active_page='dummy_data')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', active_page='privacy')

# API routes for masking are now moved to client-side JS for 100% privacy.
# The server no longer processes or sees any code content.

@app.route('/api/resolve-domain', methods=['POST'])
def api_resolve_domain():
    data = request.json
    domain = data.get('domain', '').strip()

    if not domain:
        return jsonify({"error": "No domain provided"}), 400

    try:
        ip = socket.gethostbyname(domain)
        return jsonify({"ip": ip, "domain": domain})
    except socket.gaierror:
        return jsonify({"error": f"Could not resolve domain: {domain}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/universal-converter')
def universal_converter():
    return render_template('universal_converter.html', active_page='universal_converter')

@app.route('/java-to-json')
def java_to_json():
    return render_template('java_to_json.html', active_page='java_to_json')

@app.route('/aws-cloudwatch')
def aws_cloudwatch():
    return render_template('aws_cloudwatch.html', active_page='aws_cloudwatch')

@app.route('/dfd-creator')
def dfd_creator():
    return render_template('dfd_creator.html', active_page='dfd_creator')

@app.route('/hql-to-sql')
def hql_to_sql():
    return render_template('hql_to_sql.html', active_page='hql_to_sql')

@app.route('/timezone-converter')
def timezone_converter():
    return render_template('timezone_converter.html', active_page='timezone_converter')

@app.route('/workflow-engine')
def workflow_engine():
    return render_template('workflow_engine.html', active_page='workflow_engine')

@app.route('/json-compare')
def json_compare():
    return render_template('json_compare.html', active_page='json_compare')

@app.route('/tools')
def tools():
    return render_template('tools.html', active_page='tools')

@app.route('/api/proxy', methods=['POST'])
def api_proxy():
    try:
        data = request.get_json(silent=True) or {}
        url, url_error = _validate_proxy_url(data.get('url'))
        method = (data.get('method') or 'GET').upper()
        headers = _clean_proxy_headers(data.get('headers', {}))
        body = data.get('body')

        if url_error:
            return jsonify({"error": url_error}), 400

        if method not in ALLOWED_PROXY_METHODS:
            return jsonify({"error": f"Unsupported method {method}"}), 400

        if body and len(str(body).encode('utf-8')) > MAX_PROXY_BODY_BYTES:
            return jsonify({"error": "Request body is too large for the public proxy."}), 413

        resp = requests.request(
            method,
            url,
            headers=headers,
            data=body if method in {'POST', 'PUT', 'PATCH'} else None,
            timeout=PROXY_TIMEOUT_SECONDS,
            allow_redirects=False
        )

        resp_headers = dict(resp.headers)
        resp_headers.pop('Content-Encoding', None)
        resp_headers.pop('Transfer-Encoding', None)

        content = resp.content or b''
        truncated = len(content) > MAX_PROXY_RESPONSE_BYTES
        if truncated:
            content = content[:MAX_PROXY_RESPONSE_BYTES]

        text = content.decode(resp.encoding or 'utf-8', errors='replace')
        if truncated:
            text += "\n\n[Response truncated by AI Code Masker proxy.]"

        return jsonify({
            "status": resp.status_code,
            "statusText": resp.reason,
            "headers": resp_headers,
            "text": text
        })
    except requests.exceptions.Timeout:
        return jsonify({"error": "Proxy request timed out."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Proxy request failed: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
