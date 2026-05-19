import json
import sys
import os

# Add project root to sys.path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from api.config import BRAND_NAME, BRAND_SHORT, CANONICAL_HOST, BRAND_SLOGAN

def generate_page_metadata(title_suffix, description_content, path="", is_tool=False, faqs=None):
    """
    Generates semantic meta tags, canonical URLs, and JSON-LD schema blocks dynamically.
    """
    # Standard dynamic titles & descriptions
    title = f"{title_suffix} | {BRAND_SHORT}" if title_suffix else BRAND_NAME
    description = description_content or BRAND_SLOGAN
    canonical = f"{CANONICAL_HOST}{path}"
    
    # 1. Base WebSite Schema
    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BRAND_NAME,
        "url": CANONICAL_HOST,
        "description": BRAND_SLOGAN
    }
    
    schemas = [website_schema]
    
    # 2. Add SoftwareApplication Schema if the page is a specific tool
    if is_tool:
        tool_schema = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": title_suffix,
            "url": canonical,
            "description": description,
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "All",
            "offers": {
                "@type": "Offer",
                "price": "0.00",
                "priceCurrency": "USD"
            }
        }
        schemas.append(tool_schema)
        
    # 3. Add FAQPage Schema if FAQs are provided
    if faqs and len(faqs) > 0:
        faq_entities = []
        for q, a in faqs.items():
            faq_entities.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }
        schemas.append(faq_schema)

    # 4. Add BreadcrumbList Schema
    breadcrumbs = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": CANONICAL_HOST
        }
    ]
    if path and path != "/":
        parts = [p for p in path.split("/") if p]
        accumulated = ""
        for i, part in enumerate(parts):
            accumulated += f"/{part}"
            breadcrumbs.append({
                "@type": "ListItem",
                "position": i + 2,
                "name": part.replace("-", " ").title(),
                "item": f"{CANONICAL_HOST}{accumulated}"
            })
    
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumbs
    }
    schemas.append(breadcrumb_schema)

    # Convert schema dictionaries into safe script HTML tags
    schema_script_html = ""
    for s in schemas:
        schema_script_html += f'<script type="application/ld+json">\n{json.dumps(s, indent=2)}\n</script>\n'

    return {
        "title": title,
        "description": description,
        "canonical": canonical,
        "schema_html": schema_script_html
    }
