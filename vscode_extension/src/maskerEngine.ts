/**
 * AI Code Masker — Core Masking Engine
 * TypeScript port of masker.js for VS Code extension
 * (c) 2026 Privacy-First Developer Tools
 */

/** Language keyword sets — identifiers in these sets are never masked */
const KEYWORDS: Record<string, Set<string>> = {
    java: new Set([
        'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
        'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
        'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
        'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new',
        'package', 'private', 'protected', 'public', 'return', 'short', 'static',
        'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
        'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null',
        'String', 'System', 'out', 'print', 'println', 'Override', 'Deprecated',
        'SuppressWarnings'
    ]),
    python: new Set([
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
        'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
        'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
        'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set',
        'tuple', 'bool', 'self', 'cls'
    ]),
    js: new Set([
        'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
        'default', 'delete', 'do', 'else', 'export', 'extends', 'finally', 'for',
        'function', 'if', 'import', 'in', 'instanceof', 'new', 'return', 'super',
        'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void', 'while', 'with',
        'yield', 'let', 'static', 'enum', 'await', 'async', 'true', 'false', 'null',
        'undefined', 'NaN', 'Infinity', 'require', 'module', 'exports', 'from',
        'document', 'window', 'console', 'log', 'React', 'useState', 'useEffect',
        'useCallback', 'useMemo', 'useRef', 'useContext', 'useReducer'
    ])
};

/** Sensitive data patterns for automatic secret detection */
interface SensitivePattern {
    name: string;
    regex: RegExp;
}

const SENSITIVE_PATTERNS: SensitivePattern[] = [
    { name: 'EMAIL',        regex: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g },
    { name: 'AWS_KEY',      regex: /AKIA[0-9A-Z]{16}/g },
    { name: 'SECRET_TOKEN', regex: /(?:token|secret|key|password|auth|api)[-_]?(?:key|token|id)?\s*[:=]\s*["']([^"']+)["']/gi },
    { name: 'IP_ADDRESS',   regex: /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g }
];

/** Token regex per language — captures strings, comments, and identifiers */
const TOKEN_REGEX: Record<string, RegExp> = {
    python: /(?<string>"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(?<comment>#[^\n]*)|(?<identifier>\b[a-zA-Z_]\w*\b)/g,
    java:   /(?<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(?<comment>\/\/[^\n]*|\/\*[\s\S]*?\*\/)|(?<identifier>\b[a-zA-Z_]\w*\b)/g,
    js:     /(?<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[\s\S]*?`)|(?<comment>\/\/[^\n]*|\/\*[\s\S]*?\*\/)|(?<identifier>\b[a-zA-Z_]\w*\b)/g
};

/** Lookahead for method detection */
const METHOD_LOOKAHEAD = /\s*\(/;

/** Result of a masking operation */
export interface MaskResult {
    maskedCode: string;
    mapping: Record<string, string>;
}

/**
 * Maps VS Code language IDs to internal engine language keys.
 */
export function detectLanguage(languageId: string): string {
    const langMap: Record<string, string> = {
        'python': 'python',
        'java': 'java',
        'javascript': 'js',
        'javascriptreact': 'js',
        'typescript': 'js',
        'typescriptreact': 'js',
        'vue': 'js',
        'svelte': 'js'
    };
    return langMap[languageId] || 'js';
}

/**
 * Mask code content — replaces identifiers with generic placeholders.
 *
 * @param content   The source code to mask
 * @param lang      Language key: 'python' | 'java' | 'js'
 * @param customRules  Optional list of identifiers to always mask first
 * @param detectSecrets  Whether to run sensitive pattern detection
 * @returns MaskResult with maskedCode and mapping
 */
export function maskContent(
    content: string,
    lang: string = 'python',
    customRules: string[] = [],
    detectSecrets: boolean = true
): MaskResult {
    const mapping: Record<string, string> = {};
    const counters: Record<string, number> = {
        var: 1, Class: 1, method: 1, CONST: 1, CUSTOM: 1, SECRET: 1
    };

    // Pre-register custom rules
    for (const rule of customRules) {
        if (rule && !mapping[rule]) {
            mapping[rule] = `CUSTOM_${counters.CUSTOM++}`;
        }
    }

    let processedContent = content;

    // Pass 1: Detect and mask sensitive patterns
    if (detectSecrets) {
        for (const pattern of SENSITIVE_PATTERNS) {
            // Reset regex state for each run
            pattern.regex.lastIndex = 0;
            processedContent = processedContent.replace(pattern.regex, (match: string, group1?: string) => {
                const secret = group1 || match;
                if (!mapping[secret]) {
                    mapping[secret] = `${pattern.name}_${counters.SECRET++}`;
                }
                return match.replace(secret, mapping[secret]);
            });
        }
    }

    // Pass 2: Tokenize and mask identifiers
    const regex = TOKEN_REGEX[lang] || TOKEN_REGEX.js;
    regex.lastIndex = 0;

    const maskedCode = processedContent.replace(regex, (match: string, ...args: any[]) => {
        const groups = args[args.length - 1] as Record<string, string | undefined>;

        if (groups.string !== undefined) { return match; }
        if (groups.comment !== undefined) { return match; }
        if (groups.identifier === undefined) { return match; }

        const ident = groups.identifier;

        // Skip language keywords
        const keywordSet = KEYWORDS[lang];
        if (keywordSet && keywordSet.has(ident)) { return ident; }

        // Already mapped (custom rule or sensitive pattern)
        if (mapping[ident]) { return mapping[ident]; }

        // Heuristic type classification
        let type = 'var';
        if (ident.toUpperCase() === ident && ident.length > 1 && !/^\d/.test(ident)) {
            type = 'CONST';
        } else if (ident[0] === ident[0].toUpperCase() && ident[0] !== ident[0].toLowerCase()) {
            type = 'Class';
        } else {
            // Check for method call heuristic
            const offset = args[args.length - 2] as number;
            const nextSlice = processedContent.slice(offset + match.length);
            if (METHOD_LOOKAHEAD.test(nextSlice)) {
                type = 'method';
            }
        }

        const masked = `${type}_${counters[type]++}`;
        mapping[ident] = masked;
        return masked;
    });

    return { maskedCode, mapping };
}

/**
 * Unmask code content — restores original identifiers from a mapping.
 *
 * @param content   The masked source code
 * @param mapping   The original→masked mapping (will be inverted internally)
 * @param lang      Language key
 * @returns Restored source code string
 */
export function unmaskContent(
    content: string,
    mapping: Record<string, string>,
    lang: string = 'python'
): string {
    // Invert: masked_name → original_name
    const invMapping: Record<string, string> = {};
    for (const [original, masked] of Object.entries(mapping)) {
        invMapping[masked] = original;
    }

    const regex = TOKEN_REGEX[lang] || TOKEN_REGEX.js;
    regex.lastIndex = 0;

    return content.replace(regex, (match: string, ...args: any[]) => {
        const groups = args[args.length - 1] as Record<string, string | undefined>;

        if (groups.string !== undefined) { return match; }
        if (groups.comment !== undefined) { return match; }
        if (groups.identifier === undefined) { return match; }

        const ident = groups.identifier;
        return invMapping[ident] || ident;
    });
}
