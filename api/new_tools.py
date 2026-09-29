# New tools added during the UI/UX audit. Each entry carries full programmatic-SEO
# metadata (title/desc/intro/faqs) plus catalog display metadata (name/short/icon/svg).
# Imported and merged into TOOLS by api/tools_data.py.

def _faq(*pairs):
    return {q: a for q, a in pairs}

def _svg(d):
    return ('<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">'
            f'<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{d}"/></svg>')

NEW_TOOLS = {
    # ── Suggested additions (high-value, fully client-side) ─────────────
    "regex-tester": {
        "template": "regex_tester.html", "active": "tools", "cat": "Developer Utilities",
        "title": "Regex Tester Online — Build, Test & Debug JavaScript Regular Expressions",
        "desc": "Test regex patterns against sample text with live match highlighting, capture groups, flags and replacement preview — entirely in your browser.",
        "intro": "Debug regular expressions without opening a terminal. Type a pattern and test string to see every match highlighted in real time, inspect numbered and named capture groups, toggle global/ignore-case/multiline flags, and preview a replacement result. Perfect for validating the regex you are about to paste into code.",
        "faqs": _faq(
            ("Does this regex tester use JavaScript or PCRE?", "It uses the JavaScript (ECMAScript) regex engine, matching what runs in browsers and Node.js. Minor syntax differences from Python/PCRE exist, notably lookbehind support."),
            ("Why does my regex not match anything?", "Common causes are unescaped special characters, wrong flags (missing `i` for case-insensitivity), or greedy quantifiers swallowing too much. Live highlighting shows exactly where matching stops."),
        ),
        "aliases": ["/regex-tester"],
        "name": "Regex Tester", "short": "Test and debug regular expressions with live match highlighting.",
        "icon": "bg-rose-500/15 text-rose-600 dark:text-rose-400",
        "svg": _svg("M4 17l6-6-6-6M12 19h8"),
    },
    "uuid-generator": {
        "template": "uuid_generator.html", "active": "tools", "cat": "Generators",
        "title": "UUID Generator Online — Create v4 UUIDs in Bulk, 100% Local",
        "desc": "Generate random RFC-4122 version 4 UUIDs by the hundred locally in your browser. Copy, export or format them as SQL inserts instantly.",
        "intro": "Create cryptographically random v4 UUIDs using the browser's Web Crypto API — no server round-trip, so nothing is logged. Generate up to 1,000 at once, copy them all, or wrap them in quotes and SQL INSERT statements for quick prototyping.",
        "faqs": _faq(
            ("Are these UUIDs really random?", "Yes — they come from window.crypto.getRandomValues(), a cryptographically secure source inside your browser."),
            ("Can two UUIDs collide?", "A v4 UUID has 122 random bits; you would need to generate billions before a collision becomes statistically plausible."),
        ),
        "aliases": ["/uuid-generator"],
        "name": "UUID Generator", "short": "Generate cryptographically random v4 UUIDs in bulk.",
        "icon": "bg-violet-500/15 text-violet-600 dark:text-violet-400",
        "svg": _svg("M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"),
    },
    "timestamp-converter": {
        "template": "timestamp_converter.html", "active": "tools", "cat": "Developer Utilities",
        "title": "Unix Timestamp Converter Online — Epoch Seconds to Date & Back",
        "desc": "Convert Unix timestamps (seconds or milliseconds) to human-readable dates in any timezone, and turn dates back into epoch values instantly.",
        "intro": "Paste an epoch value like 1727085600 and see it rendered as local time, UTC and ISO-8601 simultaneously, with relative descriptions such as “3 hours ago”. The reverse direction lets you pick a date and copy its timestamp for logs, databases and JWT claims.",
        "faqs": _faq(
            ("Is my timestamp in seconds or milliseconds?", "The converter auto-detects: 10-digit numbers are treated as seconds, 13-digit as milliseconds."),
            ("Why does the converted date look wrong?", "Browsers display timestamps in your local timezone by default. Check the UTC line if you expected midnight-aligned values."),
        ),
        "aliases": ["/timestamp-converter"],
        "name": "Timestamp Converter", "short": "Convert Unix epoch timestamps to dates and back.",
        "icon": "bg-sky-500/15 text-sky-600 dark:text-sky-400",
        "svg": _svg("M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"),
    },
    "markdown-preview": {
        "template": "markdown_preview.html", "active": "tools", "cat": "Developer Utilities",
        "title": "Markdown Preview & Converter Online — Write, Render & Export HTML",
        "desc": "Live markdown editor with instant GitHub-flavoured rendering and one-click export to clean HTML.",
        "intro": "Write markdown on the left and watch it render on the right in real time. Supports headings, tables, task lists, fenced code blocks and strikethrough, then exports the result as standalone HTML you can paste into a CMS or README.",
        "faqs": _faq(
            ("Which markdown flavour is supported?", "GitHub Flavored Markdown basics: ATX headings, pipe tables, task lists, strikethrough, autolinks and fenced code blocks."),
            ("Is my document saved anywhere?", "No. Rendering happens locally and nothing is uploaded; the draft persists only in your browser storage."),
        ),
        "aliases": ["/markdown-preview"],
        "name": "Markdown Preview", "short": "Live markdown editor with instant HTML rendering and export.",
        "icon": "bg-teal-500/15 text-teal-600 dark:text-teal-400",
        "svg": _svg("M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"),
    },
    "csv-to-json": {
        "template": "csv_to_json.html", "active": "tools", "cat": "Data & Encoding",
        "title": "CSV to JSON Converter Online — Upload-Free Spreadsheet to JSON",
        "desc": "Paste CSV text or drop a spreadsheet export and get clean, typed JSON arrays with headers as keys. Delimiter, quote and type inference options included.",
        "intro": "Turn any comma, semicolon or tab-separated table into a JSON array of objects in one step. The parser handles quoted fields with embedded delimiters, infers numbers and booleans, and lets you keep everything as strings when you need exact fidelity.",
        "faqs": _faq(
            ("Does large CSV data slow it down?", "Parsing runs in-browser via JavaScript, so files of tens of megabytes convert in under a second on typical hardware."),
            ("How are headers used?", "The first row becomes JSON keys by default; you can supply custom keys or emit arrays-of-arrays instead."),
        ),
        "aliases": ["/csv-to-json"],
        "name": "CSV → JSON", "short": "Convert CSV spreadsheets into typed JSON arrays.",
        "icon": "bg-lime-500/15 text-lime-600 dark:text-lime-400",
        "svg": _svg("M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"),
    },
    "json-to-csv": {
        "template": "json_to_csv.html", "active": "tools", "cat": "Data & Encoding",
        "title": "JSON to CSV Converter Online — Flatten Arrays Into Spreadsheets",
        "desc": "Convert an array of JSON objects into a downloadable CSV file with automatic header detection and nested-key flattening.",
        "intro": "Drop in an API response or JSON export and receive a spreadsheet-ready CSV. Nested objects are flattened with dot notation (address.city), arrays become delimited cells, and column order follows first-seen keys.",
        "faqs": _faq(
            ("How are nested objects handled?", "They are flattened into dotted column names, e.g. user.address.zipcode, so every record keeps a consistent shape."),
            ("Will numbers lose precision?", "No conversion happens beyond serialisation — values are written exactly as parsed from the JSON source."),
        ),
        "aliases": ["/json-to-csv"],
        "name": "JSON → CSV", "short": "Flatten JSON object arrays into downloadable CSV.",
        "icon": "bg-green-500/15 text-green-600 dark:text-green-400",
        "svg": _svg("M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"),
    },
    "cron-expression": {
        "template": "cron_expression.html", "active": "tools", "cat": "Developer Utilities",
        "title": "Cron Expression Parser & Explainer Online",
        "desc": "Translate crontab expressions like 0 9 * * 1-5 into plain English and preview the next ten run times instantly.",
        "intro": "Type (or click together) a five- or six-field cron expression and instantly read it in human language, see which minute/hour/day fields drive the schedule, and list upcoming execution times so you can sanity-check a job before deploying it.",
        "faqs": _faq(
            ("What do the five cron fields mean?", "Minute, hour, day-of-month, month and day-of-week, evaluated in that order; an optional sixth leading field adds seconds."),
            ("Does it support */5 and L style syntax?", "Step values (*/5), ranges (1-5) and lists (1,3,5) are fully explained; some vendor extensions like `L` are flagged as unsupported."),
        ),
        "aliases": ["/cron-expression"],
        "name": "Cron Expression Explainer", "short": "Read crontab schedules in plain English with next-run previews.",
        "icon": "bg-amber-500/15 text-amber-600 dark:text-amber-400",
        "svg": _svg("M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"),
    },
    "http-status-codes": {
        "template": "http_status_codes.html", "active": "tools", "cat": "Developer Utilities",
        "title": "HTTP Status Codes Reference — Meanings, Examples & Fixes",
        "desc": "Searchable reference of every HTTP status code from 100 Continue to 508 Loop Detected with plain-English meanings and common fixes.",
        "intro": "Look up any status code in seconds: what it signals, which response headers matter, why a client might receive it, and the standard debugging steps for the most frequent offenders (401, 403, 404, 429, 500, 502).",
        "faqs": _faq(
            ("What is the difference between 401 and 403?", "401 means authentication is missing or invalid; 403 means you are authenticated but not allowed to access the resource."),
            ("When should an API return 429?", "When a client exceeds its rate limit. The response should include a Retry-After header telling the caller how long to wait."),
        ),
        "aliases": ["/http-status-codes"],
        "name": "HTTP Status Codes", "short": "Searchable reference of every HTTP code with meanings and fixes.",
        "icon": "bg-cyan-500/15 text-cyan-600 dark:text-cyan-400",
        "svg": _svg("M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.946a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"),
    },
    "base32-encoder": {
        "template": "base32_encoder.html", "active": "tools", "cat": "Data & Encoding",
        "title": "Base32 Encoder & Decoder Online — RFC 4648 Alphabet",
        "desc": "Encode text to Base32 and decode it back using the standard RFC 4648 alphabet, with padding options, entirely in your browser.",
        "intro": "Base32 is the encoding of choice where only uppercase letters and digits are safe (legacy mainframes, TOTP secret provisioning). This tool encodes UTF-8 text to Base32 and back with correct '=' padding handling.",
        "faqs": _faq(
            ("Where is Base32 actually used?", "Most commonly in authenticator app secret URIs (otpauth://) and email attachment filenames where case must be preserved safely."),
            ("Is Base32 encryption?", "No — like Base64 it is reversible encoding, not security. Never treat encoded secrets as protected ones."),
        ),
        "aliases": ["/base32-encoder"],
        "name": "Base32 Encoder / Decoder", "short": "RFC 4648 Base32 encoding and decoding with padding control.",
        "icon": "bg-fuchsia-500/15 text-fuchsia-600 dark:text-fuchsia-400",
        "svg": _svg("M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"),
    },
    "gzip-string": {
        "template": "gzip_string.html", "active": "tools", "cat": "Data & Encoding",
        "title": "Gzip / Deflate String Compressor Online",
        "desc": "Compress text to gzip or deflate and decompress binary-encoded payloads directly in the browser to inspect sizes and content.",
        "intro": "Paste a string, compress it with gzip or zlib deflate, and immediately see the byte-size savings and a Base64 view of the compressed payload — useful when debugging Content-Encoding issues or hand-building compressed fixtures.",
        "faqs": _faq(
            ("Why is my short string bigger after gzipping?", "Gzip adds roughly 18 bytes of header/footer overhead; tiny inputs rarely benefit until compression pays that cost back."),
            ("Which algorithms are available?", "Standard gzip (RFC 1952) and zlib-wrapped deflate, implemented with the browser Compression Streams API where available."),
        ),
        "aliases": ["/gzip-string"],
        "name": "Gzip String Compressor", "short": "Compress and decompress text with gzip/zlib locally.",
        "icon": "bg-orange-500/15 text-orange-600 dark:text-orange-400",
        "svg": _svg("M19 14l-7 7m0 0l-7-7m7 7V3"),
    },
    "html-entity": {
        "template": "html_entity.html", "active": "tools", "cat": "Data & Encoding",
        "title": "HTML Entity Encoder & Decoder — Escape Special Characters Safely",
        "desc": "Escape <, >, &, quotes and accented symbols into HTML entities, or decode entities back to plain text instantly.",
        "intro": "Prevent broken markup and injection bugs by entity-encoding snippets before embedding them in HTML source, or decode pages full of &nbsp; and &copy; back into readable text with one click.",
        "faqs": _faq(
            ("When must I encode HTML entities?", "Whenever user-generated text is inserted into HTML without templating escaping — it prevents both layout breakage and XSS."),
            ("Numeric vs named entities — which should I use?", "Named entities (&amp;, &euro;) are readable; numeric ones (&#8364;) cover every Unicode codepoint regardless of DTD support."),
        ),
        "aliases": ["/html-entity"],
        "name": "HTML Entity Encode / Decode", "short": "Escape and unescape HTML special characters safely.",
        "icon": "bg-indigo-500/15 text-indigo-600 dark:text-indigo-400",
        "svg": _svg("M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"),
    },
    "color-contrast-checker": {
        "template": "color_contrast_checker.html", "active": "tools", "cat": "Colour Tools",
        "title": "WCAG Color Contrast Checker — Pass AA & AAA Instantly",
        "desc": "Measure the contrast ratio between any two colors, check WCAG 2.1 AA/AAA compliance and get auto-adjusted color suggestions.",
        "intro": "Enter foreground and background colors to see the exact contrast ratio, whether normal and large text pass AA or AAA, and a lightness slider that nudges one color until it clears the required threshold — keeping designs both pretty and accessible.",
        "faqs": _faq(
            ("What contrast ratio do I need?", "WCAG AA requires 4.5:1 for normal body text and 3:1 for large text (18pt+); AAA raises those to 7:1 and 4.5:1."),
            ("Do images and icons count?", "Non-text elements like form borders and meaningful icons need at least 3:1 against adjacent colors under WCAG 1.4.11."),
        ),
        "aliases": ["/color-contrast-checker"],
        "name": "Contrast Checker (WCAG)", "short": "Verify color-pair contrast against WCAG AA/AAA thresholds.",
        "icon": "bg-yellow-500/15 text-yellow-600 dark:text-yellow-400",
        "svg": _svg("M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707.707M6.343 17.657l-.707.707M16.95 16.95l.707.707M7.05 7.05l.707-.707M15 12a3 3 0 11-6 0 3 3 0 016 0z"),
    },
    "password-strength-tester": {
        "template": "password_strength_tester.html", "active": "tools", "cat": "Security & Hashing",
        "title": "Password Strength Tester — Check Entropy Without Sending Anything",
        "desc": "Evaluate how long it would take to crack a password offline, see its entropy in bits, and get concrete improvement tips — processed 100% locally.",
        "intro": "Unlike most testers, this one never transmits your input: it estimates entropy, detects dictionary words, repeats and keyboard walks, and shows realistic crack-time scenarios for GPU attackers so you know exactly what “strong” means.",
        "faqs": _faq(
            ("Is it safe to type my real password here?", "Yes for this page — evaluation runs entirely in JavaScript and no network request carries your input. Still, avoid testing passwords you reuse elsewhere."),
            ("What makes a password hard to crack?", "Length beats complexity: 16+ random characters dwarf any symbol trick, because offline attackers brute-force by search space, not character classes."),
        ),
        "aliases": ["/password-strength-tester"],
        "name": "Password Strength Tester", "short": "Estimate entropy and crack-time locally, zero upload.",
        "icon": "bg-red-500/15 text-red-600 dark:text-red-400",
        "svg": _svg("M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"),
    },
    "binary-text": {
        "template": "binary_text.html", "active": "tools", "cat": "Data & Encoding",
        "title": "Binary ⇄ Text Translator Online — ASCII Bit Conversion",
        "desc": "Convert text to binary (ASCII bit strings) and binary back to text with live previews, spacing options and byte grouping.",
        "intro": "Type words to see their 01 representation grouped per byte, or paste a bit string to recover the text. Handy for networking homework, encoding experiments and understanding exactly how characters become bytes.",
        "faqs": _faq(
            ("Which character set does it use?", "UTF-8 bytes by default, which matches ASCII for all standard English characters and extends gracefully to emoji."),
            ("Why do my binary groups have eight digits?", "Each group is one byte; classic 7-bit ASCII simply leaves the leading zero in place."),
        ),
        "aliases": ["/binary-text"],
        "name": "Binary ⇄ Text", "short": "Translate between characters and 01 bit strings.",
        "icon": "bg-slate-500/15 text-slate-600 dark:text-slate-400",
        "svg": _svg("M4 6h16M4 12h16m-7 6h7"),
    },
    "morse-code": {
        "template": "morse_code.html", "active": "tools", "cat": "Text Tools",
        "title": "Morse Code Translator — Text to Dots & Dashes and Back",
        "desc": "Translate sentences into International Morse code and back, with adjustable tone speed for listening practice.",
        "intro": "Instant two-way conversion plus an audio playback option that beeps messages at selectable speed so you can train your ear — all synthesized locally with the Web Audio API.",
        "faqs": _faq(
            ("Is Morse code still used?", "Yes, primarily by amateur radio operators and as a low-bandwidth fallback in emergencies; the ITU standard has been stable since 1938."),
            ("How fast is standard sending?", "Around 18–20 words per minute is fluent operator speed; beginners start near 5 WPM."),
        ),
        "aliases": ["/morse-code"],
        "name": "Morse Code Translator", "short": "Two-way text ⇄ Morse conversion with audio playback.",
        "icon": "bg-pink-500/15 text-pink-600 dark:text-pink-400",
        "svg": _svg("M5.586 15H4a1 1 0 01-1-1V4a1 1 0 011-1h11a1 1 0 011 1v1.586M15 7h4a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1v-4"),
    },
    "text-reversal": {
        "template": "text_reversal.html", "active": "tools", "cat": "Text Tools",
        "title": "Reverse Text Online — Flip Strings, Words or Lines",
        "desc": "Backwards text generator for styling, puzzle-making and debugging: reverse characters, whole words or line order instantly.",
        "intro": "Three modes in one tool — character reversal (“dlrow olleh”), word-order reversal and line-order reversal — with Unicode-safe handling so emoji and accents survive the flip.",
        "faqs": _faq(
            ("Why do some emoji break when reversed?", "Grapheme clusters (emoji with modifiers) must be reversed as units; this tool splits on graphemes rather than raw code points."),
            ("Can I mirror text for social bios?", "Yes — character mode produces the popular backwards-bio effect while keeping spaces intact."),
        ),
        "aliases": ["/text-reversal"],
        "name": "Reverse Text", "short": "Flip characters, words or lines — Unicode-safe.",
        "icon": "bg-purple-500/15 text-purple-600 dark:text-purple-400",
        "svg": _svg("M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"),
    },
}

for _s, _t in NEW_TOOLS.items():
    _t.setdefault("url", f"/tools/{_s}")
