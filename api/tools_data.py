# Central registry of ALL tool pages for programmatic SEO.
# Every entry renders at /tools/<slug> with a unique title, meta description,
# an on-page intro paragraph, and FAQs (which also emit FAQPage JSON-LD).
# Legacy bare paths (/md5-hash etc.) are 301-redirected here automatically.

def _faq(*pairs):
    return {q: a for q, a in pairs}

TOOLS = {
    # ── Flagship ────────────────────────────────────────────────────────
    "code-masker": {
        "template": "index.html", "active": "masker", "cat": "AI Privacy",
        "title": "AI Code Masker — Hide Secrets & Identifiers Before Pasting Code into ChatGPT or Claude",
        "desc": "Mask variable names, API keys, passwords and business logic identifiers locally in your browser before sharing code with any AI model, then restore the AI's answer with one click.",
        "intro": "The AI Code Masker replaces sensitive identifiers (class names, method names, variables, tokens, secrets) with generic placeholders like var_1 and method_2 before you paste code into ChatGPT, Claude, Gemini or Copilot. The mapping never leaves your device, and after the AI answers, a single click restores your real names — so you get AI help without leaking proprietary code.",
        "faqs": _faq(
            ("Is it safe to paste company code into ChatGPT?", "No — anything you paste may be retained and used for training unless your account opts out. Masking identifiers and scrubbing secrets first dramatically reduces exposure of proprietary logic."),
            ("Does my code ever leave my computer?", "No. All masking happens locally in your browser via JavaScript. No network request contains your source code or the identifier map."),
            ("Can the AI still understand masked code?", "Yes. Structure, control flow, algorithms and language syntax are untouched — only business-specific names become placeholders, which is usually enough for debugging and refactoring help."),
            ("How do I get my original names back?", "The masker exports a JSON map. Paste the AI's response plus that map into the Restore tab and your original identifiers are reconstructed exactly."),
        ),
    },
    "clinical-parser": {
        "template": "clinical_parser.html", "active": "clinical_parser", "cat": "HealthTech",
        "title": "HL7 v2 & FHIR Parser Online — Inspect Clinical Messages Locally",
        "desc": "Parse, pretty-print and validate HL7 v2 pipe-delimited messages and FHIR JSON resources entirely in your browser. PHI never leaves your machine.",
        "intro": "This free HL7 parser turns raw pipe-delimited v2 messages (ADT, ORM, ORU...) and FHIR JSON resources into a readable segment-by-segment tree. Because it runs 100% client-side, it is safe to use with live patient data — nothing is uploaded, logged, or stored.",
        "faqs": _faq(
            ("Is this HIPAA-safe for testing with real patient data?", "The tool itself is — processing happens in your browser and no data is transmitted. Your organisation remains responsible for its own compliance posture."),
            ("Which HL7 versions are supported?", "HL7 v2.x pipe-delimited messages (all standard segments) and FHIR R4 JSON resources."),
            ("What is the difference between HL7 v2 and FHIR?", "HL7 v2 is a decades-old pipe/segment messaging standard; FHIR is a modern REST/JSON standard built on the same clinical concepts. This parser handles both."),
        ),
    },
    # ── Developer utilities ─────────────────────────────────────────────
    "json-formatter": {
        "template": "json_editor.html", "active": "tools", "cat": "Data & Encoding",
        "title": "JSON Formatter & Validator Online — Beautify, Inspect & Validate JSON Instantly",
        "desc": "Format, beautify, collapse, inspect and validate raw JSON trees completely locally in your browser. Syntax error highlighting included.",
        "intro": "Paste any JSON payload and instantly get a formatted, collapsible, colour-coded tree view. Invalid documents produce a precise error message with line context, so you can debug API responses, config files and JWT claims in seconds — without uploading anything to a third-party server.",
        "faqs": _faq(
            ("What does a JSON formatter do?", "It takes compact or messy JSON text and re-prints it with consistent indentation, line breaks and key ordering so humans can read and review it."),
            ("Is it safe to format sensitive JSON here?", "Yes. Formatting runs entirely in your browser using JavaScript — your data is never sent over the network."),
            ("Why is my JSON invalid?", "Common causes are trailing commas, single quotes instead of double quotes, unquoted keys, or NaN values — all forbidden by RFC 8259. The validator points at the exact failure location."),
        ),
    },
    "json-compare": {
        "template": "json_compare.html", "active": "json_compare", "cat": "Data & Encoding",
        "title": "JSON Compare Tool — Diff Two JSON Files Side by Side",
        "desc": "Visually diff two JSON documents and highlight added, removed and changed keys instantly. 100% in-browser comparison.",
        "intro": "Drop two JSON payloads side by side and see exactly which keys were added, removed or modified — perfect for comparing API responses across environments, config revisions or database exports.",
        "faqs": _faq(
            ("Does JSON comparison care about key order?", "No — semantic comparison treats objects as unordered, while arrays remain order-sensitive, matching how JSON equality actually works."),
            ("Can I compare large JSON files?", "Yes, multi-megabyte documents compare locally in milliseconds because nothing is uploaded."),
        ),
    },
    "jwt-decoder": {
        "template": "jwt_tool.html", "active": "tools", "cat": "Security & Hashing",
        "title": "JWT Decoder Online — Decode JSON Web Tokens Without Sending Them Anywhere",
        "desc": "Paste any JWT to inspect its header, payload, claims and signature algorithm locally. exp/iat timestamps are humanised automatically.",
        "intro": "A JSON Web Token is signed, not encrypted — anyone holding one can read its payload. This decoder splits a token into its Base64URL header and claims set, humanises expiry dates, and flags common issues (expired tokens, alg=none), all inside your browser so tokens never touch a server.",
        "faqs": _faq(
            ("Can a JWT decoder verify signatures?", "Decoding reads the payload; verifying requires the signing secret or public key. This tool decodes and inspects structure and claims locally."),
            ("Is it safe to paste a JWT here?", "With this tool yes — decoding happens client-side and the token is never transmitted. Most online JWT sites upload your token; this one does not."),
            ("What do standard JWT claims mean?", "iss is the issuer, sub the subject/user, aud the audience, exp the expiry timestamp, iat the issued-at time."),
        ),
    },
    "api-tester": {
        "template": "api_tester.html", "active": "tools", "cat": "Developer Utilities",
        "title": "REST API Tester Online — Send GET, POST, PUT & DELETE Requests From Your Browser",
        "desc": "Build and fire HTTP requests with custom headers, query params and JSON bodies. Inspect status codes, headers and response times instantly.",
        "intro": "A lightweight, zero-install alternative to Postman. Craft any HTTP request, attach headers and payloads, and inspect the full response — status line, headers, timing and body — directly in a browser tab.",
        "faqs": _faq(
            ("Do I need to install anything?", "No. It runs entirely in your browser — no account, no download."),
            ("Why does my request fail with a CORS error?", "Browsers block cross-origin requests unless the target API sends Access-Control-Allow-Origin headers. This tester routes through a privacy-preserving proxy that rejects private-network targets."),
            ("Is it safe to test authenticated endpoints?", "Requests go directly to the target API; credentials are not stored server-side, and the proxy cannot see saved history."),
        ),
    },
    "sql-optimizer": {
        "template": "sql_optimizer.html", "active": "sql_optimizer", "cat": "Developer Utilities",
        "title": "SQL Formatter & Query Optimizer — Clean Up Slow-Looking Queries",
        "desc": "Format messy SQL, spot performance anti-patterns (SELECT *, missing indexes hints, functions on indexed columns) and rewrite for clarity.",
        "intro": "Paste any SQL statement and get a beautifully formatted version plus heuristic warnings about common performance traps — leading wildcards, implicit conversions, cartesian joins and SELECT * — so reviews catch problems before production does.",
        "faqs": _faq(
            ("Does it connect to my database?", "No. Analysis is static and local — your queries and schema never leave the page."),
            ("Can a formatter really optimize queries?", "Formatting improves readability, and the heuristic checks flag classic anti-patterns. Actual tuning still needs EXPLAIN plans, but this catches the low-hanging fruit."),
        ),
    },
    "hql-to-sql": {
        "template": "hql_to_sql.html", "active": "hql_to_sql", "cat": "Developer Utilities",
        "title": "HQL to SQL Converter — Translate Hibernate Queries to Plain SQL",
        "desc": "Convert HQL (Hibernate Query Language) statements into equivalent ANSI SQL online, with entity-to-table mapping notes.",
        "intro": "Paste an HQL query and receive the equivalent SQL translation, making it easy to sanity-check what Hibernate will actually send to your database.",
        "faqs": _faq(
            ("What is the difference between HQL and SQL?", "HQL queries object entities and their properties; SQL queries tables and columns. Hibernate translates HQL into dialect-specific SQL at runtime."),
        ),
    },
    "java-to-json": {
        "template": "java_to_json.html", "active": "java_to_json", "cat": "Developer Utilities",
        "title": "Java Object to JSON Converter Online",
        "desc": "Turn Java class definitions and POJOs into representative JSON structures to scaffold DTOs, mocks and API docs.",
        "intro": "Paste a Java class and generate a matching JSON skeleton — useful for building mock payloads, documenting REST APIs, or scaffolding TypeScript interfaces from backend models.",
        "faqs": _faq(
            ("Which Java types map to which JSON types?", "Strings and enums map to strings; numeric types to numbers; booleans to booleans; List/Set/arrays to arrays; Maps and nested objects to JSON objects."),
        ),
    },
    "dfd-creator": {
        "template": "dfd_creator.html", "active": "dfd_creator", "cat": "Developer Utilities",
        "title": "Data Flow Diagram Creator Online (DFD Maker)",
        "desc": "Draw level-0 and level-1 data flow diagrams in your browser with processes, data stores, external entities and labelled flows.",
        "intro": "Sketch DFDs fast: drag processes, stores and entities onto the canvas, connect them with labelled flows, and export the diagram for documentation or security reviews.",
        "faqs": _faq(
            ("What is a data flow diagram?", "A graphical representation of how information moves through a system: external entities, processes, data stores and the flows between them."),
        ),
    },
    "aws-cloudwatch": {
        "template": "aws_cloudwatch.html", "active": "aws_cloudwatch", "cat": "Developer Utilities",
        "title": "AWS CloudWatch Log Query Helper & Filter Pattern Builder",
        "desc": "Build CloudWatch Logs Insights queries and filter patterns visually, and parse pasted log samples into structured events.",
        "intro": "Stop guessing CloudWatch syntax. Compose filter patterns and Insights queries interactively, preview them against sample log lines, and copy the finished query straight into the AWS console.",
        "faqs": _faq(
            ("Does this tool access my AWS account?", "No. It is an offline query builder and log parser — credentials and logs never leave your browser."),
        ),
    },
    "workflow-engine": {
        "template": "workflow_engine.html", "active": "workflow_engine", "cat": "Developer Utilities",
        "title": "Visual Workflow Builder & Automation Designer Online",
        "desc": "Design automation workflows as connected steps with branches, then export the definition as JSON.",
        "intro": "Prototype automations visually — triggers, actions, conditions — and export a portable JSON workflow definition you can wire into any execution engine.",
        "faqs": _faq(
            ("Where are my workflows saved?", "Locally in your browser storage. Export JSON to move them anywhere."),
        ),
    },
    "timezone-converter": {
        "template": "timezone_converter.html", "active": "timezone_converter", "cat": "Developer Utilities",
        "title": "Time Zone Converter — Compare Times Across Cities Instantly",
        "desc": "Convert any date and time between world time zones with DST handled correctly. Perfect for scheduling global meetings.",
        "intro": "Pick a time in one zone and instantly see the equivalent everywhere else, including daylight-saving transitions — ideal for planning standups across offices.",
        "faqs": _faq(
            ("Does it account for daylight saving time?", "Yes. Conversions use the IANA tz database rules, so DST shifts are applied automatically."),
        ),
    },
    "universal-converter": {
        "template": "universal_converter.html", "active": "universal_converter", "cat": "Data & Encoding",
        "title": "Universal Unit Converter — Bytes, Data, Time, Length, Weight & More",
        "desc": "Convert between hundreds of units: digital storage, length, mass, temperature, area, volume and time — instantly and offline.",
        "intro": "One converter for every unit family — KB↔MiB, metres↔feet, °C↔°F and more — with sensible precision and copyable results.",
        "faqs": _faq(
            ("What is the difference between KB and KiB?", "A kilobyte (KB) is 1000 bytes; a kibibyte (KiB) is 1024 bytes. Binary prefixes avoid the ambiguity when measuring RAM and disk blocks."),
        ),
    },
    "domain-to-ip": {
        "template": "domain_to_ip.html", "active": "domain_to_ip", "cat": "Network",
        "title": "Domain to IP Lookup — DNS A/AAAA Record Checker Online",
        "desc": "Resolve any hostname to its IPv4 and IPv6 addresses and inspect basic DNS record information instantly.",
        "intro": "Enter a domain to see the IP addresses behind it — handy for debugging connectivity, checking CDN routing, or verifying DNS propagation.",
        "faqs": _faq(
            ("Why does one domain return multiple IPs?", "Load balancing and CDNs serve the same hostname from many addresses; round-robin DNS returns several A records deliberately."),
        ),
    },
    "my-ip": {
        "template": "my_ip.html", "active": "my_ip", "cat": "Network",
        "title": "What Is My IP Address? — Public IP & Connection Info Finder",
        "desc": "See your public IPv4 address, user agent and detected network details instantly, without installing anything.",
        "intro": "Instantly reveals the public IP address your device presents to the internet, along with browser and connection metadata.",
        "faqs": _faq(
            ("Why does my IP differ from my router's 192.168.x.x address?", "Private LAN addresses are translated to a single public IP by NAT. External services only ever see the public one."),
        ),
    },
    "api-proxy-note": None,  # placeholder removed below
}
# strip the accidental placeholder entry
TOOLS.pop("api-proxy-note", None)

TOOLS.update({
    # ── Text & writing ──────────────────────────────────────────────────
    "letter-counter": {
        "template": "letter_counter.html", "active": "letter_counter", "cat": "Text Tools",
        "title": "Character Counter Online — Letters, Words, Sentences & Reading Time",
        "desc": "Count characters, words, sentences, paragraphs and estimated reading time live as you type. Twitter, Google and essay limits highlighted.",
        "intro": "A precise character and word counter that updates as you type, with platform-aware limits (X/Twitter 280, meta descriptions 160, AdWords 90) and reading-time estimates.",
        "faqs": _faq(
            ("Do spaces count as characters?", "Both counts are shown separately: 'characters' excludes spaces, 'characters with spaces' includes them."),
        ),
    },
    "case-converter": {
        "template": "case_converter.html", "active": "case_converter", "cat": "Text Tools",
        "title": "Case Converter — UPPERCASE, lowercase, Title Case, camelCase, snake_case & kebab-case",
        "desc": "Convert text between 10+ letter cases instantly: upper, lower, title, sentence, camelCase, PascalCase, snake_case, kebab-case and more.",
        "intro": "Switch any text between programming and typographic cases in one click — perfect for normalising identifiers, headings or dataset column names.",
        "faqs": _faq(
            ("What is the difference between camelCase and PascalCase?", "camelCase starts with a lowercase letter (myVariableName); PascalCase capitalises every word (MyClassName), typically used for types."),
        ),
    },
    "bionic-reading": {
        "template": "bionic_reading.html", "active": "bionic_reading", "cat": "Text Tools",
        "title": "Bionic Reading Generator — Read Faster With Guided Word Fixation",
        "desc": "Convert any text into bionic-reading format, bolding the first letters of each word to guide your eyes and speed comprehension.",
        "intro": "Paste an article or document and regenerate it with bionic typography, letting you skim long texts faster.",
        "faqs": _faq(
            ("Does bionic reading actually work?", "Anecdotally many readers report faster skimming, especially with ADHD or dyslexia; controlled studies remain limited."),
        ),
    },
    "whitespace-remover": {
        "template": "whitespace_remover.html", "active": "whitespace_remover", "cat": "Text Tools",
        "title": "Whitespace Remover & Line Break Cleaner Online",
        "desc": "Remove extra spaces, tabs, blank lines and line breaks from text or code. Trim, dedent and minify whitespace instantly.",
        "intro": "Clean messy copied text: collapse repeated spaces, strip empty lines, remove trailing whitespace or join wrapped lines back together.",
        "faqs": _faq(
            ("How do I remove all line breaks?", "Choose the 'join lines' mode to replace newlines with spaces (or nothing) in one pass."),
        ),
    },
    "spell-checker": {
        "template": "spell_checker.html", "active": "spell_checker", "cat": "Text Tools",
        "title": "Spell Checker Online — Free Grammar & Spelling Correction",
        "desc": "Check spelling and grammar in essays, emails and code comments. Misspellings are highlighted with suggested corrections.",
        "intro": "Run an instant spell check over any text and review flagged words with alternatives — no signup, no uploads.",
        "faqs": _faq(
            ("Does it work offline?", "Core checking runs in the browser; results appear immediately as you paste text."),
        ),
    },
    "translator": {
        "template": "translator.html", "active": "translator", "cat": "Text Tools",
        "title": "Text Translator Online — Translate Between Languages Free",
        "desc": "Translate words, sentences and documents between dozens of languages quickly and easily.",
        "intro": "Fast multilingual translation with language detection, character counting and one-click copy.",
        "faqs": _faq(
            ("Which languages are supported?", "All major world languages, with automatic source-language detection."),
        ),
    },
    "sentence-formation": {
        "template": "sentence_formation.html", "active": "sentence_formation", "cat": "Text Tools",
        "title": "Sentence Formation Tool — Turn Fragments Into Complete Sentences",
        "desc": "Rebuild grammatically complete sentences from keywords or shuffled fragments for writing and language learning.",
        "intro": "Feed it loose phrases or keywords and get well-formed sentence options to polish your drafts.",
        "faqs": _faq(
            ("Can it reorder shuffled words?", "Yes — enter words separated by commas and the tool proposes natural sentence orderings."),
        ),
    },
    "email-formation": {
        "template": "email_formation.html", "active": "email_formation", "cat": "Text Tools",
        "title": "Professional Email Generator — Draft Polished Emails From Bullet Points",
        "desc": "Create courteous, professional email drafts from a few bullet points: outreach, follow-ups, apologies and thank-yous.",
        "intro": "Describe what you need to say in rough notes and get a ready-to-send professional email you can tweak and copy.",
        "faqs": _faq(
            ("Are generated emails stored anywhere?", "No. Drafts are produced in your browser and disappear when you close the tab."),
        ),
    },
    "naming-suggestions": {
        "template": "naming_suggestions.html", "active": "naming_suggestions", "cat": "Text Tools",
        "title": "Project & Variable Name Generator for Developers",
        "desc": "Brainstorm clean project names, repo slugs and variable identifiers. Hard-code 'data', 'info' and 'util' from your naming vocabulary.",
        "intro": "Get curated naming ideas for repos, functions and products — with rationale, so you stop debating whether to call it manager, handler or service.",
        "faqs": _faq(
            ("Why are names like 'data' and 'info' discouraged?", "They carry no meaning — fooService vs paymentGateway tells a reader nothing about responsibility. Specific names make codebases navigable."),
        ),
    },
    "lorem-ipsum": {
        "template": "lorem_ipsum.html", "active": "lorem_ipsum", "cat": "Text Tools",
        "title": "Lorem Ipsum Generator — Placeholder Text for Mockups & Demos",
        "desc": "Generate paragraphs, sentences or words of classic lorem ipsum dummy text with configurable length.",
        "intro": "Produce clean placeholder copy for designs and demos in one click, with fine-grained control over length.",
        "faqs": _faq(
            ("Why is placeholder text called lorem ipsum?", "It derives from Cicero's 'de Finibus Bonorum et Malorum' (45 BC), scrambled since the 1500s by typesetters."),
        ),
    },
    "dummy-data": {
        "template": "dummy_data.html", "active": "dummy_data", "cat": "Text Tools",
        "title": "Fake Data Generator — Names, Addresses, Emails, JSON & CSV",
        "desc": "Generate realistic mock users, addresses, credit-card-shaped numbers, JSON arrays and CSV rows for seeding databases and tests.",
        "intro": "Seed databases, populate tables and stress-test APIs with thousands of realistic fake records — exported as JSON or CSV.",
        "faqs": _faq(
            ("Are the generated emails real?", "No. They use reserved domains (example.com) so they can never reach a real inbox."),
        ),
    },
    # ── Data & encoding ─────────────────────────────────────────────────
    "base64": {
        "template": "base64.html", "active": "base64", "cat": "Data & Encoding",
        "title": "Base64 Encode & Decode Online — Text and Files",
        "desc": "Encode text or files to Base64 and decode Base64 back to text instantly, with UTF-8 safety and file drop support.",
        "intro": "Convert strings and binary files to and from Base64 in your browser — useful for data URIs, auth headers and embedding assets.",
        "faqs": _faq(
            ("Is Base64 encryption?", "No. It is a reversible encoding, not a security mechanism — never store secrets as Base64 and assume they're protected."),
            ("Why does Base64 increase size?", "Every 3 bytes become 4 ASCII characters, so output grows ~33%."),
        ),
    },
    "base64-to-image": {
        "template": "base64_to_image.html", "active": "base64_to_image", "cat": "Data & Encoding",
        "title": "Base64 to Image Converter — Save Data URIs as PNG/JPG Files",
        "desc": "Paste a Base64 string or data URI and preview it as an image, then download it as PNG, JPG or WEBP.",
        "intro": "Turn encoded image strings from CSS, JSON or logs back into downloadable image files instantly.",
        "faqs": _faq(
            ("How do I convert an image to Base64 instead?", "Use the companion Image → Base64 tool, which outputs a ready-to-paste data URI."),
        ),
    },
    "image-to-base64": {
        "template": "image_to_base64.html", "active": "image_to_base64", "cat": "Data & Encoding",
        "title": "Image to Base64 Converter — Generate Data URIs Online",
        "desc": "Upload any image and get its Base64 data URI for inline CSS, HTML or JSON embedding. Supports PNG, JPG, GIF, WEBP and SVG.",
        "intro": "Drag an image in, copy a data:image/... URI out — perfect for eliminating extra HTTP requests for small icons.",
        "faqs": _faq(
            ("When should I inline images as data URIs?", "For tiny icons and critical above-the-fold graphics; large inlined images bloat HTML and hurt caching."),
        ),
    },
    "base64-to-pdf": {
        "template": "base64_to_pdf.html", "active": "base64_to_pdf", "cat": "Data & Encoding",
        "title": "Base64 to PDF Converter Online",
        "desc": "Decode a Base64-encoded PDF string and download the working document instantly, entirely in your browser.",
        "intro": "Paste a Base64 PDF payload (from an API response or email attachment) and recover the original document.",
        "faqs": _faq(
            ("My decoded PDF won't open — why?", "Usually the input contained newlines, a data: prefix, or was URL-encoded first. The tool strips common wrappers automatically."),
        ),
    },
    "url-encoder": {
        "template": "url_encoder.html", "active": "url_encoder", "cat": "Data & Encoding",
        "title": "URL Encoder & Decoder — Percent-Encoding Made Easy",
        "desc": "Encode and decode URLs, query parameters and path segments with component or full-URI percent-encoding.",
        "intro": "Escape reserved characters like ?, &, # and spaces so links and query strings survive transport intact.",
        "faqs": _faq(
            ("What is the difference between %20 and + for spaces?", "%20 encodes a space in a URI path; + means space only inside application/x-www-form-urlencoded query strings."),
        ),
    },
    "html-encoder": {
        "template": "html_encoder.html", "active": "html_encoder", "cat": "Data & Encoding",
        "title": "HTML Entity Encoder & Decoder Online",
        "desc": "Escape HTML special characters into entities (&lt;, &amp;, &#39;) or decode entities back to text. Prevent XSS in templates.",
        "intro": "Safely embed markup snippets in content fields and CMS entries by converting < > & \" into their entity equivalents.",
        "faqs": _faq(
            ("Why encode HTML entities?", "To render literal markup in a page and to prevent injected tags from executing — the first line of defence against XSS."),
        ),
    },
    "html-formatter": {
        "template": "html_formatter.html", "active": "html_formatter", "cat": "Data & Encoding",
        "title": "HTML Formatter & Beautifier Online",
        "desc": "Indent and tidy messy HTML markup into readable, properly nested code in one click.",
        "intro": "Paste minified or sloppy HTML and get clean, indented markup you can actually review.",
        "faqs": _faq(
            ("Does formatting change behaviour?", "No. Whitespace-only reformatting preserves semantics for all standard markup."),
        ),
    },
    "html-minifier": {
        "template": "html_minifier.html", "active": "html_minifier", "cat": "Data & Encoding",
        "title": "HTML Minifier — Shrink Page Size & Speed Up Loading",
        "desc": "Compress HTML by removing comments, whitespace and optional tags. Reduce payload size before deployment.",
        "intro": "Cut kilobytes off your templates by stripping everything a browser doesn't need.",
        "faqs": _faq(
            ("Is minified HTML harder to attack?", "Marginally — it frustrates casual source reading, but real protection belongs on the server."),
        ),
    },
    "html-preview": {
        "template": "html_preview.html", "active": "html_preview", "cat": "Data & Encoding",
        "title": "Live HTML Preview Editor — See Your Code Render Instantly",
        "desc": "Write HTML, CSS and JS in a sandboxed editor and watch the rendered result update live.",
        "intro": "A scratchpad for testing snippets, reproducing bugs, or teaching HTML — output renders in an isolated frame.",
        "faqs": _faq(
            ("Is the preview sandboxed?", "Yes, output runs inside a sandboxed iframe so scripts cannot affect this page."),
        ),
    },
    "js-formatter": {
        "template": "js_formatter.html", "active": "js_formatter", "cat": "Data & Encoding",
        "title": "JavaScript Formatter & Beautifier Online",
        "desc": "Beautify and indent JavaScript code instantly, turning minified bundles back into readable source.",
        "intro": "Restore structure to compressed or messy JS with proper indentation and line breaks.",
        "faqs": _faq(
            ("Can I reverse webpack minification fully?", "You get readable layout back, but mangled short identifiers aren't recovered."),
        ),
    },
    "js-minifier": {
        "template": "js_minifier.html", "active": "js_minifier", "cat": "Data & Encoding",
        "title": "JavaScript Minifier Online — Compress & Obfuscate JS",
        "desc": "Minify JavaScript by stripping comments, whitespace and dead code to shrink file sizes.",
        "intro": "Reduce bandwidth and improve load times by compressing scripts right in the browser.",
        "faqs": _faq(
            ("Does minification break my code?", "Not if it stays syntactically valid; ASI-sensitive code is preserved by the transformer."),
        ),
    },
    "js-executor": {
        "template": "js_executor.html", "active": "js_executor", "cat": "Data & Encoding",
        "title": "Online JavaScript Executor — Run JS Code in the Browser",
        "desc": "Write and execute JavaScript instantly with console output capture. Zero setup, zero installs.",
        "intro": "Prototype functions, test regex or debug logic with an in-page REPL that shows console.log output.",
        "faqs": _faq(
            ("Can executed scripts access my machine?", "Code runs in a restricted worker context with no filesystem access and cannot touch this page's DOM."),
        ),
    },
    "slug-generator": {
        "template": "slug_generator.html", "active": "slug_generator", "cat": "Data & Encoding",
        "title": "URL Slug Generator — SEO-Friendly Slugs From Titles",
        "desc": "Convert titles into clean, lowercase, hyphen-separated SEO slugs with stop-word removal options.",
        "intro": "Paste an article title and get a canonical URL slug that follows search-engine best practices.",
        "faqs": _faq(
            ("Should slugs contain stopwords like 'the' and 'a'?", "Usually remove them — shorter, keyword-focused slugs perform better and look cleaner."),
        ),
    },
    "barcode-generator": {
        "template": "barcode_generator.html", "active": "barcode_generator", "cat": "Generators",
        "title": "Barcode Generator Online — Code128, EAN, UPC & More",
        "desc": "Create printable barcodes from any text or product code. Export as PNG or SVG instantly.",
        "intro": "Generate standard retail and logistics barcodes locally, sized for labels and scanners.",
        "faqs": _faq(
            ("What barcode type do I need for retail products?", "EAN-13 (globally) or UPC-A (North America). Use Code128 for internal asset tracking."),
        ),
    },
    "qr-generator": {
        "template": "qr_generator.html", "active": "tools", "cat": "Generators",
        "title": "QR Code Generator Online — Free, Customizable, No Watermark",
        "desc": "Create QR codes for URLs, Wi-Fi credentials, contacts and text. Custom colors and high-res PNG/SVG download.",
        "intro": "Point-and-scan codes generated entirely in your browser, with styling controls and print-ready export.",
        "faqs": _faq(
            ("Do generated QR codes expire?", "Static QR codes never expire. Only dynamic (redirect-service) codes can be revoked by their provider."),
            ("Can I change a QR code after printing?", "Not a static one. If you need editability, generate a dynamic QR through a redirect service you control."),
        ),
    },
    "og-meta-generator": {
        "template": "og_meta_generator.html", "active": "og_meta_generator", "cat": "Generators",
        "title": "Open Graph Meta Tag Generator — Perfect Social Previews",
        "desc": "Build og:title, og:description, og:image and Twitter Card tags with a live preview of how links appear on social media.",
        "intro": "Fill in your page details and copy a complete, validated Open Graph + Twitter Card head snippet.",
        "faqs": _faq(
            ("What image size does Open Graph recommend?", "1200×630 pixels, under 1 MB, with the aspect ratio matching the card style."),
        ),
    },
    "password-generator": {
        "template": "password_generator.html", "active": "password_generator", "cat": "Security & Hashing",
        "title": "Secure Password Generator — Strong Random Passwords Offline",
        "desc": "Generate cryptographically strong random passwords with adjustable length and symbol rules. Nothing is transmitted.",
        "intro": "Uses the browser's crypto-grade randomness (window.crypto) to build passwords resistant to brute force — and never sends them anywhere.",
        "faqs": _faq(
            ("How long should a password be?", "Length beats complexity: 16+ random characters from a wide alphabet is far stronger than 8 chars with symbols."),
            ("Are these passwords safe if generated online?", "Yes, because generation happens entirely in your browser — no server ever sees the result."),
        ),
    },
    "md5-hash": {
        "template": "md5_hash.html", "active": "md5_hash", "cat": "Security & Hashing",
        "title": "MD5 Hash Generator Online",
        "desc": "Compute the MD5 checksum of any text instantly in your browser.",
        "intro": "Generate MD5 digests for cache keys and integrity checks — with a clear warning that MD5 must not be used for security.",
        "faqs": _faq(
            ("Is MD5 secure?", "No. Collisions are trivial to forge; use SHA-256 or bcrypt for anything security-related. MD5 remains fine for non-adaptive checksums."),
        ),
    },
    "sha1-hash": {
        "template": "sha1_hash.html", "active": "sha1_hash", "cat": "Security & Hashing",
        "title": "SHA-1 Hash Generator Online",
        "desc": "Calculate SHA-1 digests of text locally in your browser.",
        "intro": "Quick SHA-1 checksums for legacy systems and git object IDs, computed entirely client-side.",
        "faqs": _faq(
            ("Is SHA-1 broken?", "Collision attacks are practical (SHAttered, 2017). Prefer SHA-256 for certificates and signatures."),
        ),
    },
    "sha224-hash": {
        "template": "sha224_hash.html", "active": "sha224_hash", "cat": "Security & Hashing",
        "title": "SHA-224 Hash Generator Online",
        "desc": "Generate SHA-224 checksums instantly in your browser.",
        "intro": "A truncated member of the SHA-2 family, useful in embedded and legacy protocols.",
        "faqs": _faq(
            ("When is SHA-224 used?", "Some IoT and telecom standards specify it; general-purpose apps should default to SHA-256."),
        ),
    },
    "sha256-hash": {
        "template": "sha256_hash.html", "active": "sha256_hash", "cat": "Security & Hashing",
        "title": "SHA-256 Hash Generator Online — Fast & Private",
        "desc": "Compute SHA-256 digests of any text locally. The current standard for signatures, certificates and integrity checks.",
        "intro": "SHA-256 underpins TLS certificates, blockchain addresses and package integrity — hash any string here without exposing it to a server.",
        "faqs": _faq(
            ("Can SHA-256 hashes be reversed?", "No. Hashing is one-way; attackers resort to brute force or rainbow tables, which salting defeats."),
            ("Should I hash passwords with SHA-256?", "No — use a slow, salted KDF like bcrypt, scrypt or Argon2. Fast hashes fall to GPU cracking."),
        ),
    },
    "sha384-hash": {
        "template": "sha384_hash.html", "active": "sha384_hash", "cat": "Security & Hashing",
        "title": "SHA-384 Hash Generator Online",
        "desc": "Generate SHA-384 checksums of text instantly, in-browser.",
        "intro": "Higher-strength SHA-2 variant used in some TLS suites and government standards.",
        "faqs": _faq(
            ("Why choose SHA-384 over SHA-256?", "Extra collision resistance margin; required by certain CNSA/FIPS profiles."),
        ),
    },
    "sha512-hash": {
        "template": "sha512_hash.html", "active": "sha512_hash", "cat": "Security & Hashing",
        "title": "SHA-512 Hash Generator Online",
        "desc": "Compute SHA-512 digests locally in your browser for maximum-integrity checksums.",
        "intro": "The widest SHA-2 digest — commonly published for software release integrity verification.",
        "faqs": _faq(
            ("How do I verify a downloaded file?", "Hash the file with sha512sum (Linux/macOS) or certutil -hashfile (Windows) and compare against the publisher's digest."),
        ),
    },
})

TOOL_CATEGORIES = [
    "AI Privacy", "HealthTech", "Developer Utilities", "Text Tools",
    "Data & Encoding", "Security & Hashing", "Network", "CSS Tools",
    "Image Tools", "Generators", "Social Mockups",
]


TOOLS.update({
    'css-formatter': {"template": 'css_formatter.html', "active": 'css_formatter', "cat": 'CSS Tools',
        "title": 'CSS Formatter & Beautifier Online', "desc": 'Indent, organise and prettify messy CSS stylesheets instantly in your browser.',
        "intro": 'Paste tangled CSS and receive clean, consistently indented rulesets that are easy to review and maintain.',
        "faqs": _faq(('Does it reorder my selectors?', 'No - rule order is preserved because cascade order matters.'))},
    'css-minifier': {"template": 'css_minifier.html', "active": 'css_minifier', "cat": 'CSS Tools',
        "title": 'CSS Minifier Online - Compress Stylesheets for Production', "desc": 'Shrink CSS files by removing comments, whitespace and redundant syntax. Boost page speed instantly.',
        "intro": 'Cut stylesheet size before shipping - safe compression that never changes rendering behaviour.',
        "faqs": _faq(('How much smaller does CSS get?', 'Typically 20-40% from whitespace stripping alone; gzip on top compresses further.'))},
    'css-gradient-generator': {"template": 'css_gradient_generator.html', "active": 'tools', "cat": 'CSS Tools',
        "title": 'CSS Gradient Generator - Visual Linear & Radial Gradient Maker', "desc": 'Design multi-stop linear, radial and conic CSS gradients with a live preview and copy-ready code.',
        "intro": 'Drag colour stops to craft perfect gradients and export standard CSS (plus vendor prefixes) in one click.',
        "faqs": _faq(('Do I still need -webkit- prefixes for gradients?', 'Only for very old browsers; modern targets can ship unprefixed linear-gradient alone.'))},
    'css-glassmorphism': {"template": 'css_glassmorphism.html', "active": 'tools', "cat": 'CSS Tools',
        "title": 'Glassmorphism CSS Generator - Frosted Glass UI Effects', "desc": 'Generate frosted-glass card styles with backdrop blur, transparency and soft borders. Copy the CSS instantly.',
        "intro": 'Tune blur, opacity and tint sliders until the glass effect looks right, then paste the generated rules into your project.',
        "faqs": _faq(("Why doesn't backdrop-filter work everywhere?", 'It needs GPU compositing support; Safari requires the -webkit- prefix and some older Android browsers ignore it entirely.'))},
    'css-box-shadow': {"template": 'css_box_shadow.html', "active": 'css_box_shadow', "cat": 'CSS Tools',
        "title": 'Box Shadow CSS Generator With Live Preview', "desc": 'Create single or layered box-shadow effects visually and copy the exact CSS property.',
        "intro": 'Dial in offsets, blur, spread and inset shadows interactively - no more guessing values.',
        "faqs": _faq(('How do realistic soft shadows work?', 'Stack several low-opacity shadows with increasing blur instead of one harsh shadow.'))},
    'css-border-radius': {"template": 'css_border_radius.html', "active": 'css_border_radius', "cat": 'CSS Tools',
        "title": 'Border Radius Generator - Organic Blob & Squircle Shapes', "desc": 'Round corners per-side or create asymmetric blob shapes with a live preview and generated CSS.',
        "intro": 'Visualise every corner combination and copy the border-radius shorthand you need.',
        "faqs": _faq(('What makes a squircle?', 'A superellipse curve; approximate it in CSS with large radii plus overflow clipping.'))},
    'css-clip-path': {"template": 'css_clip_path_generator.html', "active": 'css_clip_path', "cat": 'CSS Tools',
        "title": 'CSS clip-path Generator - Polygon, Circle & Shape Masks', "desc": 'Build clip-path polygons, circles and ellipses visually and export the CSS masking function.',
        "intro": 'Place points on a grid to define any polygon mask, then copy the ready-made clip-path rule.',
        "faqs": _faq(('Can clip-path animate?', 'Yes - between compatible shape functions, e.g. polygon-to-polygon with equal point counts.'))},
    'css-bezier': {"template": 'css_bezier_generator.html', "active": 'css_bezier', "cat": 'CSS Tools',
        "title": 'Cubic Bezier Easing Curve Generator for CSS Animations', "desc": 'Draw custom cubic-bezier timing curves with a live animation preview and copyable transition-timing-function code.',
        "intro": 'Feel the easing before you ship it - drag control points and watch a sample element move.',
        "faqs": _faq(('What do the four bezier numbers mean?', 'Two control-point coordinates (x1,y1,x2,y2) inside a unit square defining acceleration and deceleration.'))},
    'css-loader': {"template": 'css_loader_generator.html', "active": 'css_loader', "cat": 'CSS Tools',
        "title": 'CSS Loading Spinner Generator - Pure CSS Preloaders', "desc": 'Design animated spinners and loaders with pure CSS and copy the keyframe code.',
        "intro": 'Pick a style, tune speed and colour, then paste lightweight CSS-only loaders - no images or JS required.',
        "faqs": _faq(('Are CSS spinners better than GIF loaders?', 'Yes: crisper on retina displays, infinitely themeable, and far smaller in bytes.'))},
    'css-glitch': {"template": 'css_glitch_generator.html', "active": 'css_glitch', "cat": 'CSS Tools',
        "title": 'Glitch Text Effect CSS Generator', "desc": 'Create cyberpunk glitch text animations with RGB-split layers and generate the full CSS.',
        "intro": 'Adjust intensity, colours and timing, then copy a self-contained glitch effect for headings.',
        "faqs": _faq(('Does glitch text hurt accessibility?', 'It can - respect prefers-reduced-motion and avoid glitching body copy.'))},
    'css-checkbox': {"template": 'css_checkbox_generator.html', "active": 'css_checkbox', "cat": 'CSS Tools',
        "title": 'Custom CSS Checkbox Generator', "desc": 'Style beautiful checkboxes with pure CSS - radio, toggle and animated variants - and export the code.',
        "intro": 'Hide the native input, style the label, keep keyboard accessibility. Generate it here instead of hand-writing it.',
        "faqs": _faq(('Are custom checkboxes accessible?', 'Yes if built on real inputs using :checked + label styling so focus and screen readers still work.'))},
    'css-switch': {"template": 'css_switch_generator.html', "active": 'css_switch', "cat": 'CSS Tools',
        "title": 'Toggle Switch CSS Generator (iOS & Material Styles)', "desc": 'Build animated on/off toggle switches in pure CSS and copy production-ready code.',
        "intro": 'Choose track colours, knob size and animation feel, then paste the finished switch component.',
        "faqs": _faq(('Checkbox or switch for settings?', 'Switches imply immediate effect; checkboxes imply saving a form. Use switches only for instant toggles.'))},
    'css-triangle': {"template": 'css_triangle_generator.html', "active": 'css_triangle', "cat": 'CSS Tools',
        "title": 'CSS Triangle Generator - Arrows & Pointers Without Images', "desc": 'Generate direction, size and colour variants of pure-CSS triangles using the border trick.',
        "intro": 'Tooltips, dropdown carets and play buttons without a single HTTP request.',
        "faqs": _faq(('How does a CSS triangle work?', 'Shrink an element to zero size and give two adjacent borders colour while opposite borders stay transparent.'))},
    'css-pattern': {"template": 'css_pattern_generator.html', "active": 'css_pattern', "cat": 'CSS Tools',
        "title": 'CSS Background Pattern Generator - Geometric Patterns', "desc": 'Create repeating dots, grids, zigzags and geometric backgrounds with pure CSS gradients.',
        "intro": 'Zero-image background textures that scale forever and load instantly.',
        "faqs": _faq(('Are CSS patterns better than SVG tiles?', 'For simple geometry yes - no extra file, resolution-independent, and trivially recolourable.'))},
    'rn-shadow': {"template": 'rn_shadow_generator.html', "active": 'rn_shadow_generator', "cat": 'CSS Tools',
        "title": 'React Native Shadow & Elevation Generator', "desc": 'Convert web-style shadows into React Native shadowColor/offset/radius/elevation props with iOS and Android output.',
        "intro": 'Design the shadow visually and copy platform-correct StyleSheet entries - ending the iOS-vs-Android elevation pain.',
        "faqs": _faq(('Why do RN shadows differ per platform?', 'iOS uses shadow* props (true blur); Android historically used z-index elevation, so both configs must be set.'))},
    'image-resize': {"template": 'image_resize.html', "active": 'tools', "cat": 'Image Tools',
        "title": 'Image Resizer Online - Free, No Upload, Unlimited', "desc": 'Resize PNG, JPG and WEBP images to exact pixel dimensions or percentages directly in your browser.',
        "intro": 'Because nothing uploads, this works on slow connections and keeps sensitive screenshots private.',
        "faqs": _faq(('Is it really unlimited and free?', 'Yes - processing uses your own CPU via the canvas API, so there is no server quota.'))},
    'image-converter': {"template": 'image_converter.html', "active": 'image_converter', "cat": 'Image Tools',
        "title": 'Image Format Converter - PNG, JPG, WEBP & GIF', "desc": 'Convert images between PNG, JPEG, WEBP and GIF locally without uploading anything.',
        "intro": 'Drop a file, choose an output format and quality, download the converted image in seconds.',
        "faqs": _faq(('Which format should I use?', 'WEBP/AVIF for photos on the web, PNG for transparency and line art, JPEG for maximum compatibility.'))},
    'image-cropper': {"template": 'image_cropper.html', "active": 'image_cropper', "cat": 'Image Tools',
        "title": 'Image Cropper Online - Crop Photos to Any Aspect Ratio', "desc": 'Crop and rotate images with preset ratios (1:1, 4:5, 16:9) or free selection, entirely in-browser.',
        "intro": 'Perfect social-media crops without installing Photoshop.',
        "faqs": _faq(('Will cropping reduce quality?', 'Only pixels outside the crop are lost; the retained area keeps its original resolution unless you resize.'))},
    'image-filters': {"template": 'image_filters.html', "active": 'image_filters', "cat": 'Image Tools',
        "title": 'Photo Filter Editor Online - Brightness, Contrast, Saturation', "desc": 'Apply CSS-style filters (blur, grayscale, sepia, hue-rotate, contrast) to images and export the result.',
        "intro": 'Non-destructive slider editing that runs on your device.',
        "faqs": _faq(('Are my edits saved?', 'Edits live only in the tab - download the output image to keep them.'))},
    'photo-censor': {"template": 'photo_censor.html', "active": 'photo_censor', "cat": 'Image Tools',
        "title": 'Photo Blur & Censor Tool - Pixelate Faces and Sensitive Areas', "desc": 'Blur or pixelate regions of photos to hide faces, plates and documents before sharing. Nothing is uploaded.',
        "intro": 'The privacy-conscious way to redact images: draw boxes over sensitive areas and export censored copies locally.',
        "faqs": _faq(('Is blurring a photo secure enough?', 'Strong pixelation/blurring applied at full resolution is generally irreversible; light blurs can sometimes be reconstructed - censor thoroughly.'))},
    'image-color-picker': {"template": 'image_color_picker.html', "active": 'image_color_picker', "cat": 'Image Tools',
        "title": 'Color Picker From Image - Extract Hex & RGB Codes', "desc": 'Upload any picture and click to grab exact HEX, RGB and HSL values from any pixel.',
        "intro": 'Pull palettes from screenshots, logos and photographs pixel-perfectly.',
        "faqs": _faq(('Why does the picked colour differ from what I see?', 'Display colour management and JPEG compression shift nearby pixels; zoom in and sample flat areas.'))},
    'image-color-extractor': {"template": 'image_color_extractor.html', "active": 'image_color_extractor', "cat": 'Image Tools',
        "title": 'Image Color Palette Extractor - Dominant Colors From Photos', "desc": 'Automatically extract the dominant colour palette from any image as HEX swatches.',
        "intro": 'Get theme-ready palettes from brand assets or photography in one click.',
        "faqs": _faq(('How are dominant colours calculated?', 'Pixels are quantised and clustered (k-means style) so representative hues survive anti-aliasing noise.'))},
    'image-avg-color': {"template": 'image_avg_color.html', "active": 'image_avg_color', "cat": 'Image Tools',
        "title": 'Average Color of Image Calculator', "desc": 'Compute the mean colour of any image - ideal for dynamic backdrops and placeholder tints.',
        "intro": 'One number summarising an entire picture, computed client-side.',
        "faqs": _faq(('Where is average colour useful?', "Generating matching blurred backgrounds behind album art or avatars, exactly like Spotify's player."))},
    'image-pixels': {"template": 'image_pixels.html', "active": 'image_pixels', "cat": 'Image Tools',
        "title": 'Pixel Editor & Grid Inspector - Edit Images Pixel by Pixel', "desc": 'Zoom into any image, inspect individual pixel values and paint edits on a pixel grid.',
        "intro": 'Fix tiny artefacts, design sprites and read RGBA values directly.',
        "faqs": _faq(('Can I make pixel-art sprites here?', 'Yes - small canvases with a magnified grid are exactly how sprite editors work.'))},
    'code-to-image': {"template": 'code_to_image.html', "active": 'code_to_image', "cat": 'Image Tools',
        "title": 'Code to Image - Beautiful Screenshots of Your Source Code', "desc": 'Turn code snippets into shareable, syntax-highlighted images with custom themes and padding.',
        "intro": 'The fastest way to make GitHub-gist-style cards for tweets, docs and slides.',
        "faqs": _faq(('Why not just screenshot my editor?', 'Generated images add consistent padding, themes and watermarks, and render identically regardless of your display.'))},
    'svg-blob': {"template": 'svg_blob_generator.html', "active": 'svg_blob', "cat": 'Image Tools',
        "title": 'SVG Blob Generator - Random Organic Background Shapes', "desc": 'Generate smooth random blob shapes as inline SVG for hero sections and card backgrounds.',
        "intro": 'Roll infinite organic shapes, tune complexity, and copy standalone SVG markup.',
        "faqs": _faq(('Are blobs better than stock illustrations?', 'For abstract backgrounds yes: a few hundred bytes versus hundreds of kilobytes, and fully recolourable.'))},
    'tweet-generator': {"template": 'tweet_generator.html', "active": 'tools', "cat": 'Social Mockups',
        "title": 'Tweet Generator & Previewer - Design & Export Tweet Images', "desc": 'Compose realistic X/Twitter post mockups in light or dark mode and export high-resolution PNGs.',
        "intro": 'Preview threads before posting, or create illustrative tweet graphics for articles and talks.',
        "faqs": _faq(('Is it legal to publish fake tweet images?', 'As obvious satire or illustration, usually yes - but presenting fabricated quotes as real to deceive can constitute defamation or fraud.'))},
    'instagram-generator': {"template": 'instagram_post_generator.html', "active": 'instagram_generator', "cat": 'Social Mockups',
        "title": 'Instagram Post & Story Mockup Generator', "desc": 'Compose Instagram feed and story previews with custom avatars, captions and engagement counts.',
        "intro": 'Mock up IG content for pitch decks and design reviews without touching your real account.',
        "faqs": _faq(('What size are Instagram story mockups?', '1080x1920 px (9:16), matching the native story canvas.'))},
    'whatsapp-generator': {"template": 'whatsapp_generator.html', "active": 'tools', "cat": 'Social Mockups',
        "title": 'WhatsApp Chat Simulator - Build Chat Screenshots', "desc": 'Build realistic WhatsApp conversation mockups with custom names, avatars, timestamps and status bar.',
        "intro": 'Create chat screenshots for demos, memes and UX storytelling.',
        "faqs": _faq(('Can people tell these chats are fake?', 'Careful inspection can (fonts, alignment artefacts). Never use fabricated chats to defame or scam anyone.'))},
    'imessage-generator': {"template": 'imessage_generator.html', "active": 'imessage_generator', "cat": 'Social Mockups',
        "title": 'iMessage Chat Generator - iPhone Conversation Mockups', "desc": 'Design believable iMessage thread screenshots with blue/green bubbles, reactions and carrier chrome.',
        "intro": "Prototype and illustrate conversations in Apple's Messages style.",
        "faqs": _faq(("Blue vs green bubbles - what's the difference?", 'Blue means both parties use Apple devices (rich iMessage); green is SMS/MMS fallback to Android.'))},
    'yt-thumbnail': {"template": 'yt_thumbnail.html', "active": 'yt_thumbnail', "cat": 'Social Mockups',
        "title": 'YouTube Thumbnail Downloader & Size Checker', "desc": "Fetch any YouTube video's thumbnail in full resolution and check it against the 1280x720 spec.",
        "intro": 'Grab maxresdefault thumbnails from any public video ID instantly.',
        "faqs": _faq(('What resolution should YouTube thumbnails be?', '1280x720 minimum, under 2 MB, JPG/GIF/PNG.'))},
})

TOOLS.update({
    # ── Colour & typography tools ───────────────────────────────────────
    "color-palette": {"template": "color_palette.html", "active": "tools", "cat": "Colour Tools",
        "title": "Color Palette Generator - Harmonious CSS Colour Schemes", "desc": "Explore HSL-based harmonious colour palettes with one-click copy for every swatch.",
        "intro": "Build complementary, triadic and analogous palettes and export HEX/HSL values instantly.",
        "faqs": _faq(("What is a colour harmony?", "Geometric relationships on the colour wheel - complements (180 deg), triads (120 deg), analogues (30 deg) - that reliably look cohesive."))},
    "color-mixer": {"template": "color_mixer.html", "active": "color_mixer", "cat": "Colour Tools",
        "title": "Color Mixer Online - Blend Two Colours Into Any Ratio", "desc": "Mix two hex colours at any percentage in RGB or perceptual space and preview the blend live.",
        "intro": "Dial the exact tint you need between a brand colour and white/black/another hue.",
        "faqs": _faq(("Why does 50% RGB mixing look muddy for some pairs?", "RGB averages light additively; red+green gives muddy yellow. Use HSL interpolation for more intuitive blends."))},
    "color-shades": {"template": "color_shades.html", "active": "color_shades", "cat": "Colour Tools",
        "title": "Tints & Shades Generator - Full Colour Scale From One Hex", "desc": "Generate 50-950 style tint and shade scales from any base colour, ready for Tailwind or CSS variables.",
        "intro": "Turn one brand colour into a complete, evenly-stepped design-token scale.",
        "faqs": _faq(("What are tints and shades?", "Tints add white to a hue, shades add black. A 50-950 ramp spans both around your base colour."))},
    "hex-to-rgba": {"template": "hex_to_rgba.html", "active": "hex_to_rgba", "cat": "Colour Tools",
        "title": "HEX to RGBA Converter", "desc": "Convert #RRGGBB(AA) hex codes into rgba()/hsl() values with an alpha slider.",
        "intro": "Paste a hex code, get every CSS colour notation, copy what you need.",
        "faqs": _faq(("Can hex store transparency?", "Yes - 8-digit hex (#RRGGBBAA) supports alpha in all modern browsers."))},
    "rgba-to-hex": {"template": "rgba_to_hex.html", "active": "rgba_to_hex", "cat": "Colour Tools",
        "title": "RGBA to HEX Converter", "desc": "Convert rgb()/rgba() colour values back into compact or 8-digit hex notation.",
        "intro": "Round-trip any CSS colour function into hex form instantly.",
        "faqs": _faq(("How is alpha represented in hex?", "As the trailing pair of digits: rgba(0,0,0,.5) becomes #00000080."))},
    "hex-rgb": {"template": "hex_rgb.html", "active": "hex_rgb", "cat": "Colour Tools",
        "title": "Hex to RGB and RGB to Hex Color Converter With Picker", "desc": "Two-way conversion between hexadecimal and RGB colour values with a visual picker.",
        "intro": "The classic designer utility - convert hex to rgb and back without opening dev tools.",
        "faqs": _faq(("What does #FF5733 mean?", "Red=255, Green=87, Blue=51 - each byte written as two hex digits, brightest first."))},
    "list-randomizer": {"template": "list_randomizer.html", "active": "list_randomizer", "cat": "Text Tools",
        "title": "Random List Picker & Shuffle Tool - Spin Names or Items", "desc": "Paste a list of names or items and pick random winners, shuffle order, or split into groups.",
        "intro": "Raffle draws, team splits and question-order shuffling - fair, fast and shareable.",
        "faqs": _faq(("Is the shuffle truly random?", "It uses Fisher-Yates over crypto-grade randomness, so every permutation is equally likely."))},
    "font-pair-finder": {"template": "font_pair_finder.html", "active": "tools", "cat": "Text Tools",
        "title": "Google Font Pairings Finder - Matched Heading & Body Fonts", "desc": "Browse curated serif/sans font pairings with live preview and copy the import CSS.",
        "intro": "Stop guessing typography combinations - every pairing ships with ready-to-use Google Fonts links.",
        "faqs": _faq(("How many fonts should a site use?", "Two, occasionally three. One expressive heading face plus one highly readable body face beats novelty."))},
})

# Legacy bare-path aliases: every old top-level URL 301-redirects to its canonical /tools/<slug> home.
_LEGACY_ALIASES = {
 '/json-editor': 'json-formatter', '/jwt-tool': 'jwt-decoder',
 '/css-bezier-generator': 'css-bezier', '/css-border-radius': 'css-border-radius',
 '/css-box-shadow': 'css-box-shadow', '/css-checkbox-generator': 'css-checkbox',
 '/css-clip-path-generator': 'css-clip-path', '/css-formatter': 'css-formatter',
 '/css-glassmorphism': 'css-glassmorphism', '/css-glitch-generator': 'css-glitch',
 '/css-gradient-generator': 'css-gradient-generator', '/css-loader-generator': 'css-loader',
 '/css-minifier': 'css-minifier', '/css-pattern-generator': 'css-pattern',
 '/css-switch-generator': 'css-switch', '/css-triangle-generator': 'css-triangle',
 '/font-pair-finder': 'font-pair-finder', '/image-avg-color': 'image-avg-color',
 '/image-color-extractor': 'image-color-extractor', '/image-color-picker': 'image-color-picker',
 '/image-converter': 'image-converter', '/image-cropper': 'image-cropper',
 '/image-filters': 'image-filters', '/image-resize': 'image-resize',
 '/imessage-generator': 'imessage-generator', '/instagram-post-generator': 'instagram-generator',
 '/photo-censor': 'photo-censor', '/pixel-editor': 'image-pixels',
 '/rn-shadow-generator': 'rn-shadow', '/svg-blob-generator': 'svg-blob',
 '/tweet-generator': 'tweet-generator', '/whatsapp-generator': 'whatsapp-generator',
 '/yt-thumbnail': 'yt-thumbnail', '/code-to-image': 'code-to-image',
}
for _p, _slug in _LEGACY_ALIASES.items():
    if _slug in TOOLS:
        TOOLS[_slug].setdefault("aliases", []).append(_p)
