/**
 * AI Code Masker - Core Client-Side Logic
 * (c) 2026 Privacy-First Developer Tools
 */

const KEYWORDS = {
    java: new Set(['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null', 'String', 'System', 'out', 'print', 'println']),
    python: new Set(['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield', 'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'bool', 'self', 'cls']),
    js: new Set(['break', 'case', 'catch', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'else', 'export', 'extends', 'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void', 'while', 'with', 'yield', 'let', 'static', 'enum', 'await', 'async', 'true', 'false', 'null', 'undefined', 'NaN', 'Infinity', 'require', 'module', 'exports', 'from'])
};

const SENSITIVE_PATTERNS = [
    { name: 'EMAIL', regex: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g },
    { name: 'AWS_KEY', regex: /AKIA[0-9A-Z]{16}/g },
    { name: 'SECRET_TOKEN', regex: /(?:token|secret|key|password|auth|api)[-_]?(?:key|token|id)?\s*[:=]\s*["']([^"']+)["']/gi },
    { name: 'IP_ADDRESS', regex: /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g }
];

const TOKEN_REGEX = {
    python: /(?<string>"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(?<comment>#[^\n]*)|(?<identifier>\b[a-zA-Z_]\w*\b)/g,
    java: /(?<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(?<comment>\/\/[^\n]*|\/\*[\s\S]*?\*\/)|(?<identifier>\b[a-zA-Z_]\w*\b)/g,
    js: /(?<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[\s\S]*?`)|(?<comment>\/\/[^\n]*|\/\*[\s\S]*?\*\/)|(?<identifier>\b[a-zA-Z_]\w*\b)/g
};

const METHOD_LOOKAHEAD = /\s*\(/;

/**
 * Main Masking Function
 */
function maskContent(content, lang = 'python', customRules = []) {
    const mapping = {};
    const counters = { var: 1, Class: 1, method: 1, CONST: 1, CUSTOM: 1, SECRET: 1 };
    
    // 1. Initial pass for sensitive patterns (entire content)
    let processedContent = content;
    
    SENSITIVE_PATTERNS.forEach(pattern => {
        processedContent = processedContent.replace(pattern.regex, (match, group1) => {
            const secret = group1 || match; // Group 1 if captured (for key=value), else full match
            if (!mapping[secret]) {
                const masked = `${pattern.name}_${counters.SECRET++}`;
                mapping[secret] = masked;
            }
            return match.replace(secret, mapping[secret]);
        });
    });

    // 2. Main pass for code structure
    const regex = TOKEN_REGEX[lang] || TOKEN_REGEX.js;
    const finalResult = processedContent.replace(regex, (match, string, comment, identifier, offset) => {
        if (string !== undefined) return string;
        if (comment !== undefined) return comment;
        if (identifier === undefined) return match;

        const ident = identifier;

        // Skip keywords
        if (KEYWORDS[lang]?.has(ident)) return ident;
        
        // Already masked in pass 1 or previously
        if (mapping[ident]) return mapping[ident];

        // Determine type heuristic
        let type = 'var';
        if (ident.toUpperCase() === ident && ident.length > 1 && !/^\d/.test(ident)) {
            type = 'CONST';
        } else if (ident[0].toUpperCase() === ident[0]) {
            type = 'Class';
        } else {
            const nextSlice = processedContent.slice(offset + match.length);
            if (METHOD_LOOKAHEAD.test(nextSlice)) {
                type = 'method';
            }
        }

        const masked = `${type}_${counters[type]++}`;
        mapping[ident] = masked;
        return masked;
    });

    return { maskedCode: finalResult, mapping };
}

/**
 * Restoration Function
 */
function unmaskContent(content, mapping, lang = 'python') {
    const invMapping = {};
    Object.entries(mapping).forEach(([original, masked]) => {
        invMapping[masked] = original;
    });

    const regex = TOKEN_REGEX[lang] || TOKEN_REGEX.js;
    return content.replace(regex, (match, string, comment, identifier) => {
        if (string !== undefined) return string;
        if (comment !== undefined) return comment;
        if (identifier === undefined) return match;

        return invMapping[identifier] || identifier;
    });
}

// Export for use in UI or Node (if needed)
if (typeof module !== 'undefined') {
    module.exports = { maskContent, unmaskContent };
}
