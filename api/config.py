# Branding and platform settings for AI Code Masker + DevUtils AI
# Fully configurable by the site owner.

# Temporary/configurable branding
BRAND_NAME = "AI Code Masker + DevUtils AI"
BRAND_SHORT = "DevUtils AI"
BRAND_SLOGAN = "A privacy-first product suite for modern developer tools"

# Domain details (User can change this when they purchase their domain)
DOMAIN = "aicomdemasker.com"
CANONICAL_HOST = "https://ai-code-masker.vercel.app"  # Fallback Vercel URL or new domain

# Third-party configuration hooks (Ready for production activation)
ANALYTICS_GA_ID = "G-XXXXXXXXXX"  # Google Analytics ID
AD_SENSE_CLIENT_ID = "ca-pub-XXXXXXXXXXXXXXXX"  # Google AdSense Client ID

# Pricing and Tier config
TIERS = {
    "free": {
        "name": "Developer (Free)",
        "price": "$0",
        "features": [
            "Unlimited client-side masking",
            "Access to all 55+ browser tools",
            "100% data privacy guarantee",
            "Standard community support"
        ]
    },
    "pro": {
        "name": "Professional",
        "price": "$9",
        "period": "month",
        "features": [
            "Everything in Free",
            "Complete Ad-Free experience",
            "Saved tools history & preferences",
            "Custom identifier masking patterns",
            "Priority developer-focused support"
        ]
    },
    "enterprise": {
        "name": "Enterprise",
        "price": "$49",
        "period": "month",
        "features": [
            "Everything in Pro",
            "Team workspace sharing",
            "Hosted secure API endpoints",
            "Dedicated corporate support",
            "SOC2 compliance documentation"
        ]
    }
}
