import sys
import os
import json
import socket
import ipaddress
import requests
import re
from flask import Flask, request, jsonify, render_template, redirect, make_response
from urllib.parse import urlparse

# Add project root to sys.path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Local directory addition for module discovery
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    import masker_logic
except ImportError:
    # Handle Vercel's package structure variant
    from . import masker_logic

# Import platform configurations and SEO helper
from api.config import TIERS, BRAND_NAME, BRAND_SHORT, CANONICAL_HOST, BRAND_SLOGAN
from api.seo_utils import generate_page_metadata

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

# Helper: Render simple technical markdown to stylized clean HTML
def render_simple_markdown(md_text):
    # Strip frontmatter if present
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        if len(parts) >= 3:
            md_text = parts[2]
            
    # Escape some basic elements or parse headings/lists
    # Code blocks
    md_text = re.sub(r'```(\w*)\n(.*?)```', r'<pre class="code-font bg-black/40 p-4 rounded-xl border border-white/5 text-xs text-indigo-200 overflow-x-auto my-6"><code class="language-\1">\2</code></pre>', md_text, flags=re.DOTALL)
    # Headings
    md_text = re.sub(r'^## (.*?)$', r'<h2 class="text-xl font-black dark:text-white uppercase tracking-tight mt-8 mb-4">\1</h2>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^### (.*?)$', r'<h3 class="text-base font-black dark:text-white uppercase tracking-tight mt-6 mb-3">\1</h3>', md_text, flags=re.MULTILINE)
    # Bold
    md_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-extrabold dark:text-white">\1</strong>', md_text)
    # Bullet points
    md_text = re.sub(r'^\* (.*?)$', r'<li class="ml-4 list-disc text-slate-600 dark:text-slate-300 mb-2">\1</li>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^\d+\. (.*?)$', r'<li class="ml-4 list-decimal text-slate-600 dark:text-slate-300 mb-2">\1</li>', md_text, flags=re.MULTILINE)
    
    # Paragraphs (excluding tags already processed)
    paragraphs = []
    for line in md_text.split('\n\n'):
        line_strip = line.strip()
        if not line_strip:
            continue
        if line_strip.startswith('<pre') or line_strip.startswith('<h') or line_strip.startswith('<li'):
            paragraphs.append(line_strip)
        else:
            paragraphs.append(f'<p class="text-slate-600 dark:text-slate-300 text-xs md:text-sm leading-relaxed mb-4">{line_strip}</p>')
    return '\n'.join(paragraphs)

# Helper: Parse local markdown files inside api/blog_posts
def get_blog_posts():
    posts = []
    blog_dir = os.path.join(os.path.dirname(__file__), 'blog_posts')
    if not os.path.exists(blog_dir):
        return []
    for fname in os.listdir(blog_dir):
        if fname.endswith('.md'):
            slug = fname[:-3]
            with open(os.path.join(blog_dir, fname), 'r', encoding='utf-8') as f:
                content = f.read()
            # Simple frontmatter extractor
            parts = content.split('---')
            if len(parts) >= 3:
                fm_text = parts[1]
                body = parts[2]
                metadata = {}
                for line in fm_text.strip().split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        metadata[k.strip()] = v.strip().strip('"')
                posts.append({
                    'slug': slug,
                    'title': metadata.get('title', slug.replace('-', ' ').title()),
                    'date': metadata.get('date', '2026-05-19'),
                    'category': metadata.get('category', 'Security'),
                    'reading_time': metadata.get('reading_time', '5 min read'),
                    'summary': metadata.get('summary', ''),
                    'body': body,
                    'rendered_body': render_simple_markdown(body)
                })
    return sorted(posts, key=lambda x: x['date'], reverse=True)

# Register Dynamic URL schema objects mapped to standard legacy components
DYNAMIC_TOOLS = {
    "code-masker": {
        "template": "index.html",
        "title": "AI Code Masker — Privacy-First Secret Sanitizer for ChatGPT & Claude",
        "description": "Scrub environment secrets, passwords, and private identifiers locally before copy-pasting your code blocks into AI models.",
        "active": "masker"
    },
    "json-formatter": {
        "template": "json_editor.html",
        "title": "JSON Formatter & Validator Online",
        "description": "Format, beautify, inspect, validate, and compare raw JSON trees completely locally in your browser.",
        "active": "tools"
    },
    "jwt-decoder": {
        "template": "jwt_tool.html",
        "title": "JWT JSON Web Token Inspector & Decoder",
        "description": "Decode and analyze cryptographically signed JWT header and payload contents inside your browser.",
        "active": "tools"
    },
    "api-tester": {
        "template": "api_tester.html",
        "title": "REST API Request Tester & Mock Client",
        "description": "Send GET, POST, and PUT HTTP requests dynamically with custom header sets and payloads.",
        "active": "tools"
    },
    "sql-optimizer": {
        "template": "sql_optimizer.html",
        "title": "SQL Query Performance Heuristics Optimizer",
        "description": "Format and optimize databases query layouts with visual indexing indicators.",
        "active": "tools"
    },
    "css-gradient-generator": {
        "template": "css_gradient_generator.html",
        "title": "Sleek CSS Gradient Designer",
        "description": "Design custom multi-layered CSS background gradients with live CSS style copies.",
        "active": "tools"
    },
    "css-glassmorphism": {
        "template": "css_glassmorphism.html",
        "title": "Transparent CSS Glassmorphism Backdrop Blurs",
        "description": "Instantly render glassmorphism style rules with custom blur percentages.",
        "active": "tools"
    },
    "color-palette": {
        "template": "color_palette.html",
        "title": "Harmonious CSS Color Palette Explorer",
        "description": "Discover sleek modern HSL color palettes with copy-to-clipboard code clicks.",
        "active": "tools"
    },
    "font-pair-finder": {
        "template": "font_pair_finder.html",
        "title": "Modern Google Font Pairing Finder",
        "description": "Find harmoniously matched serif and sans-serif Google typography.",
        "active": "tools"
    },
    "letter-counter": {
        "template": "letter_counter.html",
        "title": "Advanced Word and Letter Character Counter",
        "description": "Count letters, words, reading duration, and content size instantly as you type.",
        "active": "tools"
    },
    "tweet-generator": {
        "template": "tweet_generator.html",
        "title": "Visual X / Twitter Tweet Sandbox Simulator",
        "description": "Preview your tweets in actual light or dark UI formats before publishing online.",
        "active": "tools"
    },
    "whatsapp-generator": {
        "template": "whatsapp_generator.html",
        "title": "Interactive WhatsApp Chat UI Simulator",
        "description": "Mock chat bubbles and profile bubbles in full high-fidelity preview styles.",
        "active": "tools"
    },
    "image-resize": {
        "template": "image_resize.html",
        "title": "Browser-Based Image Resizer & Scaler",
        "description": "Scale and compress PNG, JPG, and WEBP image files without uploading them to any servers.",
        "active": "tools"
    },
    "qr-generator": {
        "template": "qr_generator.html",
        "title": "Instant QR Code Scanner & Generator",
        "description": "Turn URLs and texts into custom downloadable vectors or high-res PNG images.",
        "active": "tools"
    }
}

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

# 301 Permanent SEO Redirect rules consolidating link equity into /tools/<slug>
@app.before_request
def check_legacy_redirects():
    path = request.path
    legacy_redirects = {
        "/json-editor": "/tools/json-formatter",
        "/jwt-tool": "/tools/jwt-decoder",
        "/api-tester": "/tools/api-tester",
        "/sql-optimizer": "/tools/sql-optimizer",
        "/css-gradient-generator": "/tools/css-gradient-generator",
        "/css-glassmorphism": "/tools/css-glassmorphism",
        "/color-palette": "/tools/color-palette",
        "/font-pair-finder": "/tools/font-pair-finder",
        "/letter-counter": "/tools/letter-counter",
        "/tweet-generator": "/tools/tweet-generator",
        "/whatsapp-generator": "/tools/whatsapp-generator",
        "/image-resize": "/tools/image-resize",
        "/qr-generator": "/tools/qr-generator"
    }
    if path in legacy_redirects:
        return redirect(legacy_redirects[path], code=301)

# Dynamic XML Sitemap Builder
@app.route('/sitemap.xml')
def dynamic_sitemap():
    base_pages = ["", "tools", "clinical-parser", "blog", "pricing", "privacy"]
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add main pages
    for page in base_pages:
        url = f"{CANONICAL_HOST}/{page}" if page else CANONICAL_HOST
        sitemap_xml += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
    
    # Add dynamic tools
    for slug in DYNAMIC_TOOLS.keys():
        sitemap_xml += f'  <url>\n    <loc>{CANONICAL_HOST}/tools/{slug}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
        
    # Add blog posts
    for post in get_blog_posts():
        sitemap_xml += f'  <url>\n    <loc>{CANONICAL_HOST}/blog/{post["slug"]}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'
        
    sitemap_xml += '</urlset>'
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

# Dynamic robots.txt
@app.route('/robots.txt')
def dynamic_robots():
    robots_text = f"User-agent: *\nAllow: /\n\nSitemap: {CANONICAL_HOST}/sitemap.xml\n"
    response = make_response(robots_text)
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/google0118da07594017cd.html')
def google_verification():
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.root_path, 'static'), 'google0118da07594017cd.html')

# Home (renders index.html containing client-side Code Masker)
@app.route('/')
def index():
    meta = generate_page_metadata(
        "AI Code Masker - Privacy-First Secret Removal for AI Sharing",
        "Paste code templates securely to LLMs like Claude and ChatGPT by masking variables, credentials, and tokens completely locally in your browser.",
        path="/"
    )
    return render_template('index.html', active_page='masker', seo=meta)

# Tools Catalog
@app.route('/tools')
def tools():
    meta = generate_page_metadata(
        "All Developer Utilities & Platform Tools",
        "Access 55+ browser-based offline coding, clinical translation, and UI design utilities instantly.",
        path="/tools"
    )
    return render_template('tools.html', active_page='tools', seo=meta)

# SaaS Pricing plans
@app.route('/pricing')
def pricing():
    meta = generate_page_metadata(
        "Pricing Tiers & Professional Subscriptions",
        "Upgrade to Professional and Enterprise tiers for fast hosted clinical parses, unlimited saved tool settings, and premium security support.",
        path="/pricing"
    )
    return render_template('pricing.html', active_page='pricing', tiers=TIERS, seo=meta)

# Blog catalog
@app.route('/blog')
def blog():
    posts = get_blog_posts()
    meta = generate_page_metadata(
        "Developer Security & Local Optimization Blog",
        "Discover practical tutorials and safety strategies regarding secret management, API validations, and in-browser developer utilities.",
        path="/blog"
    )
    return render_template('blog.html', active_page='blog', posts=posts, seo=meta)

# Blog post detail page
@app.route('/blog/<slug>')
def blog_post(slug):
    posts = get_blog_posts()
    post = next((p for p in posts if p['slug'] == slug), None)
    if not post:
        return redirect('/blog')
        
    meta = generate_page_metadata(
        post['title'],
        post['summary'],
        path=f"/blog/{slug}"
    )
    return render_template('blog_post.html', active_page='blog', post=post, seo=meta)

# Dynamic Tools Slug Router
@app.route('/tools/<slug>')
def dynamic_tool_route(slug):
    tool = DYNAMIC_TOOLS.get(slug)
    if not tool:
        # Fallback to the main tools list if the slug doesn't exist
        return redirect('/tools')
        
    meta = generate_page_metadata(
        tool['title'],
        tool['description'],
        path=f"/tools/{slug}",
        is_tool=True
    )
    return render_template(tool['template'], active_page=tool['active'], seo=meta)

# Fallback Legacy Route mapping for all other 40+ offline pages to keep backwards compatibility fully active
@app.route('/base64-to-image')
def base64_to_image():
    return render_template('base64_to_image.html', active_page='base64_to_image')

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

@app.route('/domain-to-ip')
def domain_to_ip():
    return render_template('domain_to_ip.html', active_page='domain_to_ip')

@app.route('/url-encoder')
def url_encoder():
    return render_template('url_encoder.html', active_page='url_encoder')

@app.route('/case-converter')
def case_converter():
    return render_template('case_converter.html', active_page='case_converter')

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
    meta = generate_page_metadata(
        "Privacy Policy - 100% In-Browser Local Execution",
        "Understand our data handling model: all your variables and data remain fully on your local machine.",
        path="/privacy"
    )
    return render_template('privacy.html', active_page='privacy', seo=meta)

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

@app.route('/whitespace-remover')
def whitespace_remover():
    return render_template('whitespace_remover.html', active_page='whitespace_remover')

@app.route('/md5-hash')
def md5_hash():
    return render_template('md5_hash.html', active_page='md5_hash')

@app.route('/sha1-hash')
def sha1_hash():
    return render_template('sha1_hash.html', active_page='sha1_hash')

@app.route('/sha224-hash')
def sha224_hash():
    return render_template('sha224_hash.html', active_page='sha224_hash')

@app.route('/clinical-parser')
def clinical_parser():
    meta = generate_page_metadata(
        "Clinical Parser - Local HL7 v2 & FHIR Translator",
        "Inspect and format medical clinical documents locally. Your data remains fully secure on your host machine.",
        path="/clinical-parser"
    )
    return render_template('clinical_parser.html', active_page='clinical_parser', seo=meta)

@app.route('/imessage-generator')
def imessage_generator():
    return render_template('imessage_generator.html', active_page='imessage_generator')

@app.route('/yt-thumbnail')
def yt_thumbnail():
    return render_template('yt_thumbnail.html', active_page='yt_thumbnail')

@app.route('/rn-shadow-generator')
def rn_shadow_generator():
    return render_template('rn_shadow_generator.html', active_page='rn_shadow_generator')

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
