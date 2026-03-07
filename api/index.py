from flask import Flask, request, jsonify, render_template
import sys
import os
import json

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
except NameError:
    # Fallback for Vercel/lambda execution where __file__ might not be properly  populated
    root_dir = os.getcwd()

# Add scripts dir to path to import the masker
masker_path = os.path.join(root_dir, '.agents', 'skills', 'ai-code-masker', 'scripts')
sys.path.append(masker_path)
try:
    from masker import mask_content, unmask_content
except ImportError as e:
    # Throwing specifically so we can see it in logs if the bundle missed the folder
    raise RuntimeError(f"Could not import masker from {masker_path}. sys.path is: {sys.path}") from e

app = Flask(__name__, template_folder=os.path.join(root_dir, 'templates'))

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
