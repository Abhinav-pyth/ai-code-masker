from flask import Flask, request, jsonify, render_template
import os
import json
from .masker_logic import mask_content, unmask_content

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/mask', methods=['POST'])
def api_mask():
    data = request.json
    code = data.get('code', '')
    lang = data.get('lang', 'python')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
        
    try:
        masked_code, mapping = mask_content(code, lang)
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
        unmasked_code = unmask_content(code, mapping, lang)
        return jsonify({
            "unmasked_code": unmasked_code
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
