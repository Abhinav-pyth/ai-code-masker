import json

tools_data = [
    ('Text Tools', '📝 Text & Writing', [
        ('letter-counter', 'Letter Counter', 'Count letters, words, and sentences in text.', 'M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129'),
        ('bionic-reading', 'Bionic Reading', 'Convert text to bionic reading format for faster reading.', 'M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z'),
        ('whitespace-remover', 'Whitespace Remover', 'Remove extra spaces, tabs, and line breaks.', 'M4 6h16M4 12h16m-7 6h7'),
        ('font-pair-finder', 'Font Pair Finder', 'Find and preview Google font combinations.', 'M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z'),
        ('spell-checker', 'Spell Checker', 'Check and correct spelling mistakes in your text.', 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'),
        ('translator', 'Translator', 'Translate text across many languages.', 'M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129'),
        ('lorem-ipsum', 'Lorem Ipsum', 'Generate placeholder text for design and development.', 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'),
        ('dummy-data', 'Dummy Data', 'Generate realistic dummy data for testing and demos.', 'M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4'),
        ('email-formation', 'Email Formation', 'Compose and format professional email templates.', 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'),
        ('sentence-formation', 'Sentence Builder', 'Build well-structured sentences from words and phrases.', 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z'),
        ('naming-suggestions', 'Naming Helper', 'Get name suggestions for variables, functions, projects and more.', 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z')
    ]),
    ('Hash & Encode Tools', '🔒 Hash & Encoding', [
        ('md5-hash', 'MD5 Hash', 'Generate MD5 hash of any string.', 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'),
        ('sha1-hash', 'SHA1 Hash', 'Generate SHA1 hash of any string.', 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'),
        ('sha224-hash', 'SHA224 Hash', 'Generate SHA224 hash of any string.', 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'),
        ('sha256-hash', 'SHA256 Hash', 'Generate SHA256 hash of any string.', 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'),
        ('sha384-hash', 'SHA384 Hash', 'Generate SHA384 hash of any string.', 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'),
        ('sha512-hash', 'SHA512 Hash', 'Generate SHA512 hash of any string.', 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'),
        ('html-encoder', 'HTML Encoder', 'Encode and decode HTML entities.', 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'),
        ('base64', 'Base64 Tool', 'Encode and decode Base64 strings instantly.', 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'),
        ('base64-to-pdf', 'Base64 → PDF', 'Convert Base64 encoded strings to downloadable PDF files.', 'M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z'),
        ('base64-to-image', 'Base64 → Image', 'Preview and download images encoded as Base64 strings.', 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'),
        ('url-encoder', 'URL Encoder', 'Encode and decode URL components and query strings.', 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1')
    ]),
    ('Coding Tools', '💻 Coding Tools', [
        ('api-tester', 'API Tester', 'Test REST APIs with all HTTP methods. Localhost support included.', 'M13 10V3L4 14h7v7l9-11h-7z'),
        ('sql-optimizer', 'SQL Optimizer', 'Detect SQL anti-patterns and get optimization suggestions.', 'M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4'),
        ('hql-to-sql', 'HQL → SQL', 'Convert Hibernate HQL/JPQL to SQL with camelCase column mapping.', 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'),
        ('dfd-creator', 'DFD Creator', 'Draw Data Flow Diagrams with interactive canvas. Export PNG/SVG.', 'M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2v-2a2 2 0 012-2h2a2 2 0 012 2m0 0V9a2 2 0 012-2h2a2 2 0 012 2v2m0 0a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2'),
        ('json-compare', 'JSON Compare', 'Advanced JSON comparison with exclusions and node manipulation.', 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4'),
        ('json-editor', 'JSON Editor', 'Format, validate and edit JSON with tree view and diff.', 'M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z'),
        ('jwt-tool', 'JWT Inspector', 'Decode and inspect JWT tokens — header, payload, signature.', 'M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z'),
        ('html-preview', 'HTML Preview', 'Live preview HTML code in a sandboxed iframe.', 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'),
        ('js-executor', 'JS Executor', 'Run JavaScript snippets in a safe sandbox with console output.', 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z'),
        ('java-to-json', 'Java → JSON', 'Convert Java POJO class definitions to JSON schema.', 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4'),
        ('aws-cloudwatch', 'CloudWatch Fmt', 'Format and parse AWS CloudWatch log entries visually.', 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'),
        ('workflow-engine', 'Workflow Engine', 'Build conditional workflows with nested if-else logic and output validation.', 'M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2v-2a2 2 0 012-2h2a2 2 0 012 2m0 0V9a2 2 0 012-2h2a2 2 0 012 2v2m0 0a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2'),
        ('timezone-converter', 'Timezone Conv.', 'Convert datetime between EST, UTC, IST and 20+ timezones instantly.', 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'),
        ('html-minifier', 'HTML Minifier', 'Minify and compress HTML code.', 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'),
        ('css-minifier', 'CSS Minifier', 'Minify and compress CSS code.', 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'),
        ('js-minifier', 'JS Minifier', 'Minify and compress JavaScript code.', 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'),
        ('html-formatter', 'HTML Formatter', 'Beautify and format HTML code.', 'M4 6h16M4 12h16m-7 6h7'),
        ('css-formatter', 'CSS Formatter', 'Beautify and format CSS code.', 'M4 6h16M4 12h16m-7 6h7'),
        ('js-formatter', 'JS Formatter', 'Beautify and format JavaScript code.', 'M4 6h16M4 12h16m-7 6h7'),
        ('slug-generator', 'Slug Generator', 'Generate URL-friendly slugs from strings.', 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1'),
        ('code-to-image', 'Code to Image', 'Convert code snippets to beautiful images.', 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z')
    ]),
    ('CSS Tools', '🎨 CSS Tools', [
        ('css-gradient-generator', 'Gradient Gen.', 'Generate CSS linear and radial gradients.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'),
        ('css-box-shadow', 'Box Shadow', 'Generate CSS box-shadow properties.', 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z'),
        ('css-border-radius', 'Border Radius', 'Generate complex CSS border-radius shapes.', 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z'),
        ('css-glassmorphism', 'Glassmorphism', 'Generate CSS glassmorphism effects.', 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z'),
        ('css-triangle-generator', 'Triangle Gen.', 'Generate CSS triangles using borders.', 'M12 19l9 2-9-18-9 18 9-2zm0 0v-8'),
        ('css-glitch-generator', 'Glitch Effect', 'Generate CSS glitch text effects.', 'M13 10V3L4 14h7v7l9-11h-7z'),
        ('css-loader-generator', 'Loader Gen.', 'Generate CSS loading animations.', 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15'),
        ('css-bezier-generator', 'Cubic Bezier', 'Generate CSS cubic-bezier transition curves.', 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9'),
        ('css-clip-path-generator', 'Clip Path', 'Generate CSS clip-path polygons.', 'M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5'),
        ('css-pattern-generator', 'Pattern Gen.', 'Generate CSS background patterns.', 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z'),
        ('css-checkbox-generator', 'Checkbox Styles', 'Generate custom CSS checkboxes.', 'M5 13l4 4L19 7'),
        ('css-switch-generator', 'Switch/Toggle', 'Generate CSS switch toggles.', 'M8 7h8a4 4 0 110 8H8a4 4 0 110-8z M8 11a2 2 0 100-4 2 2 0 000 4z')
    ]),
    ('Color Tools', '🎨 Color Tools', [
        ('color-palette', 'Color Palette', 'Generate beautiful color palettes.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'),
        ('hex-to-rgba', 'HEX to RGBA', 'Convert HEX colors to RGBA format.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'),
        ('rgba-to-hex', 'RGBA to HEX', 'Convert RGBA colors to HEX format.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'),
        ('color-shades', 'Color Shades', 'Generate tints, shades, and tones for any color.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'),
        ('color-mixer', 'Color Mixer', 'Mix multiple colors and find the result.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01')
    ]),
    ('Image Tools', '🖼️ Image Tools', [
        ('image-resize', 'Image Resize', 'Resize images to any dimension without uploading to a server.', 'M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4'),
        ('image-converter', 'Image Converter', 'Convert images between PNG, JPEG, WebP and other formats.', 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'),
        ('pixel-editor', 'Pixel Editor', 'Edit images at pixel level with drawing tools and filters.', 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z'),
        ('image-cropper', 'Image Cropper', 'Crop images easily in your browser.', 'M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4'),
        ('image-filters', 'Image Filters', 'Apply CSS and canvas filters to images.', 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z'),
        ('image-color-picker', 'Color Picker', 'Extract colors directly from an image.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'),
        ('image-color-extractor', 'Color Extractor', 'Extract a full color palette from an image.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'),
        ('image-avg-color', 'Average Color', 'Calculate the average color of an image.', 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'),
        ('image-to-base64', 'Image to Base64', 'Convert an image file to Base64 string.', 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'),
        ('svg-blob-generator', 'SVG Blob Gen', 'Generate random SVG blobs for backgrounds.', 'M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5'),
        ('photo-censor', 'Photo Censor', 'Blur or pixelate faces and sensitive areas.', 'M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21')
    ]),
    ('Social Media Tools', '📱 Social Media', [
        ('tweet-generator', 'Tweet Gen.', 'Create fake tweet screenshots.', 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'),
        ('instagram-post-generator', 'IG Post Gen.', 'Create fake Instagram post screenshots.', 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'),
        ('whatsapp-generator', 'WhatsApp Chat', 'Create fake WhatsApp chat screenshots.', 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'),
        ('imessage-generator', 'iMessage Chat', 'Create fake iMessage chat screenshots.', 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'),
        ('yt-thumbnail', 'YT Thumbnail', 'Download YouTube video thumbnails.', 'M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z'),
        ('rn-shadow-generator', 'RN Shadow', 'Generate React Native shadow styles.', 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z')
    ]),
    ('Misc Tools & Network', '🔧 Misc Tools & Network', [
        ('password-generator', 'Password Gen.', 'Generate secure and random passwords.', 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'),
        ('list-randomizer', 'List Randomizer', 'Shuffle and randomize lists or names.', 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15'),
        ('barcode-generator', 'Barcode Gen.', 'Generate standard 1D barcodes.', 'M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h2M4 12h2m14 0h.01M5 4h2a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5a1 1 0 011-1zm12 0h2a1 1 0 011 1v2a1 1 0 01-1 1h-2a1 1 0 01-1-1V5a1 1 0 011-1zM5 16h2a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1v-2a1 1 0 011-1z'),
        ('og-meta-generator', 'OG Meta Gen.', 'Generate Open Graph meta tags.', 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'),
        ('case-converter', 'Case Converter', 'Convert text between camelCase, snake_case, etc.', 'M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129'),
        ('universal-converter', 'Universal Conv.', 'Convert units across length, weight, etc.', 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4'),
        ('qr-generator', 'QR Generator', 'Generate QR codes from any text or URL instantly.', 'M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h2M4 12h2m14 0h.01M5 4h2a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5a1 1 0 011-1zm12 0h2a1 1 0 011 1v2a1 1 0 01-1 1h-2a1 1 0 01-1-1V5a1 1 0 011-1zM5 16h2a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1v-2a1 1 0 011-1z'),
        ('my-ip', 'My IP Address', 'See your current public IP address and location details.', 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9'),
        ('domain-to-ip', 'Domain → IP', 'Resolve domain names to their IP addresses via DNS lookup.', 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01')
    ]),
    ('Healthcare & Clinical', '🏥 Healthcare & Clinical', [
        ('clinical-parser', 'Clinical Parser', 'Parse HL7 v2, C-CDA and FHIR clinical documents with patient summary.', 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z')
    ])
]

# Write tools.html insertion logic
html_blocks = []
for category_id, category_title, tools in tools_data:
    html_blocks.append(f'''
        <!-- ── {category_id} ── -->
        <div class="cat-section">
            <div class="cat-title">{category_title}</div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">''')
    for tool_id, title, desc, icon_path in tools:
        html_blocks.append(f'''
                <a href="/{tool_id}" class="tool-card">
                    <div class="tool-icon bg-indigo-500/15 text-indigo-400"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{icon_path}"/></svg></div>
                    <div>
                        <div class="flex items-center gap-1 mb-1"><div class="text-xs font-black text-white uppercase tracking-wider">{title}</div></div>
                        <p class="text-[11px] text-slate-500 leading-relaxed">{desc}</p>
                    </div>
                </a>''')
    html_blocks.append('''
            </div>
        </div>''')

with open('e:/ai-playground/devtool/ai-code-masker-main/api/templates/new_tools_section.html', 'w', encoding='utf-8') as f:
    f.write(''.join(html_blocks))

