import sys
import os
import json
import socket
from flask import Flask, request, jsonify, render_template

# Local directory addition for module discovery
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    import masker_logic
except ImportError:
    # Handle Vercel's package structure variant
    from . import masker_logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', active_page='masker')

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

@app.route('/api/mask', methods=['POST'])
def api_mask():
    data = request.json
    code = data.get('code', '')
    lang = data.get('lang', 'python')

    if not code:
        return jsonify({"error": "No code provided"}), 400

    try:
        masked_code, mapping = masker_logic.mask_content(code, lang)
        return jsonify({
            "masked_code": masked_code,
            "mapping": mapping
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/unmask', methods=['POST'])
def api_unmask():
    data = request.json
    code = data.get('code', '')
    mapping = data.get('mapping', {})
    lang = data.get('lang', 'python')

    if not code or not mapping:
        return jsonify({"error": "Code and mapping are required"}), 400

    try:
        unmasked_code = masker_logic.unmask_content(code, mapping, lang)
        return jsonify({
            "unmasked_code": unmasked_code
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

if __name__ == '__main__':
    app.run(debug=True, port=3000)
