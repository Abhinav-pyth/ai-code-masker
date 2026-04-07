package com.aimasker.eclipse;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * AI Code Masker — Core Masking Engine (Java port of masker.js)
 * Masks code identifiers before sharing with AI tools.
 */
public class MaskerEngine {

    // ─── Language Keywords ────────────────────────────────────────────────────

    private static final Map<String, Set<String>> KEYWORDS = new HashMap<>();

    static {
        Set<String> javaKw = new HashSet<>();
        javaKw.addAll(Set.of(
            "abstract","assert","boolean","break","byte","case","catch","char","class","const",
            "continue","default","do","double","else","enum","extends","final","finally","float",
            "for","goto","if","implements","import","instanceof","int","interface","long","native",
            "new","package","private","protected","public","return","short","static","strictfp",
            "super","switch","synchronized","this","throw","throws","transient","try","void",
            "volatile","while","true","false","null","String","System","out","print","println",
            "Override","Deprecated","SuppressWarnings"
        ));
        KEYWORDS.put("java", javaKw);

        Set<String> pyKw = new HashSet<>();
        pyKw.addAll(Set.of(
            "False","None","True","and","as","assert","async","await","break","class","continue",
            "def","del","elif","else","except","finally","for","from","global","if","import","in",
            "is","lambda","nonlocal","not","or","pass","raise","return","try","while","with",
            "yield","print","len","range","str","int","float","list","dict","set","tuple","bool",
            "self","cls"
        ));
        KEYWORDS.put("python", pyKw);

        Set<String> jsKw = new HashSet<>();
        jsKw.addAll(Set.of(
            "break","case","catch","class","const","continue","debugger","default","delete","do",
            "else","export","extends","finally","for","function","if","import","in","instanceof",
            "new","return","super","switch","this","throw","try","typeof","var","void","while",
            "with","yield","let","static","enum","await","async","true","false","null","undefined",
            "NaN","Infinity","require","module","exports","from","document","window","console","log",
            "React","useState","useEffect","useCallback","useMemo","useRef","useContext","useReducer"
        ));
        KEYWORDS.put("js", jsKw);
    }

    // ─── Regex Patterns ───────────────────────────────────────────────────────

    private static final Map<String, Pattern> TOKEN_PATTERNS = new HashMap<>();

    static {
        TOKEN_PATTERNS.put("python", Pattern.compile(
            "(?<string>\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?'''|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*')" +
            "|(?<comment>#[^\\n]*)" +
            "|(?<identifier>\\b[a-zA-Z_]\\w*\\b)"
        ));
        TOKEN_PATTERNS.put("java", Pattern.compile(
            "(?<string>\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*')" +
            "|(?<comment>//[^\\n]*|/\\*[\\s\\S]*?\\*/)" +
            "|(?<identifier>\\b[a-zA-Z_]\\w*\\b)"
        ));
        TOKEN_PATTERNS.put("js", Pattern.compile(
            "(?<string>\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|`[\\s\\S]*?`)" +
            "|(?<comment>//[^\\n]*|/\\*[\\s\\S]*?\\*/)" +
            "|(?<identifier>\\b[a-zA-Z_]\\w*\\b)"
        ));
    }

    // ─── Sensitive Patterns ───────────────────────────────────────────────────

    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}");
    private static final Pattern AWS_KEY_PATTERN =
        Pattern.compile("AKIA[0-9A-Z]{16}");
    private static final Pattern SECRET_TOKEN_PATTERN =
        Pattern.compile("(?:token|secret|key|password|auth|api)[-_]?(?:key|token|id)?\\s*[:=]\\s*[\"']([^\"']+)[\"']",
            Pattern.CASE_INSENSITIVE);
    private static final Pattern IP_PATTERN =
        Pattern.compile("\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b");
    private static final Pattern METHOD_LOOKAHEAD =
        Pattern.compile("\\s*\\(");

    // ─── Public API ───────────────────────────────────────────────────────────

    /**
     * Detect engine language key from file extension.
     */
    public static String detectLanguage(String fileName) {
        if (fileName == null) return "js";
        String lower = fileName.toLowerCase();
        if (lower.endsWith(".py"))   return "python";
        if (lower.endsWith(".java")) return "java";
        if (lower.endsWith(".js") || lower.endsWith(".ts") ||
            lower.endsWith(".jsx")  || lower.endsWith(".tsx")) return "js";
        return "js";
    }

    /**
     * Mask code content — replaces identifiers with generic placeholders.
     *
     * @param content  Source code to mask
     * @param lang     Language key: "python" | "java" | "js"
     * @return MaskResult with maskedCode and mapping
     */
    public static MaskResult maskContent(String content, String lang) {
        Map<String, String> mapping = new HashMap<>();
        Map<String, Integer> counters = new HashMap<>();
        counters.put("var",    1);
        counters.put("Class",  1);
        counters.put("method", 1);
        counters.put("CONST",  1);
        counters.put("SECRET", 1);

        // Pass 1: Detect sensitive patterns
        String processed = maskSensitivePatterns(content, mapping, counters);

        // Pass 2: Tokenize and mask identifiers
        Pattern pattern = TOKEN_PATTERNS.getOrDefault(lang, TOKEN_PATTERNS.get("js"));
        Matcher m = pattern.matcher(processed);
        StringBuilder result = new StringBuilder();
        int lastEnd = 0;

        while (m.find()) {
            result.append(processed, lastEnd, m.start());
            lastEnd = m.end();

            String stringGroup     = m.group("string");
            String commentGroup    = m.group("comment");
            String identGroup      = m.group("identifier");

            if (stringGroup != null) {
                result.append(stringGroup);
            } else if (commentGroup != null) {
                result.append(commentGroup);
            } else if (identGroup != null) {
                Set<String> kw = KEYWORDS.getOrDefault(lang, new HashSet<>());
                if (kw.contains(identGroup)) {
                    result.append(identGroup);
                } else if (mapping.containsKey(identGroup)) {
                    result.append(mapping.get(identGroup));
                } else {
                    // Heuristic type classification
                    String type = classifyIdentifier(identGroup, processed, m.end());
                    int count = counters.get(type);
                    String masked = type + "_" + count;
                    counters.put(type, count + 1);
                    mapping.put(identGroup, masked);
                    result.append(masked);
                }
            } else {
                result.append(m.group());
            }
        }
        result.append(processed.substring(lastEnd));

        return new MaskResult(result.toString(), mapping);
    }

    /**
     * Unmask code content — restores original identifiers from mapping.
     *
     * @param content  Masked source code
     * @param mapping  Original→masked mapping (will be inverted internally)
     * @param lang     Language key
     * @return Restored source code
     */
    public static String unmaskContent(String content, Map<String, String> mapping, String lang) {
        // Invert mapping: masked_name → original_name
        Map<String, String> invMapping = new HashMap<>();
        for (Map.Entry<String, String> entry : mapping.entrySet()) {
            invMapping.put(entry.getValue(), entry.getKey());
        }

        Pattern pattern = TOKEN_PATTERNS.getOrDefault(lang, TOKEN_PATTERNS.get("js"));
        Matcher m = pattern.matcher(content);
        StringBuilder result = new StringBuilder();
        int lastEnd = 0;

        while (m.find()) {
            result.append(content, lastEnd, m.start());
            lastEnd = m.end();

            String stringGroup  = m.group("string");
            String commentGroup = m.group("comment");
            String identGroup   = m.group("identifier");

            if (stringGroup != null) {
                result.append(stringGroup);
            } else if (commentGroup != null) {
                result.append(commentGroup);
            } else if (identGroup != null) {
                result.append(invMapping.getOrDefault(identGroup, identGroup));
            } else {
                result.append(m.group());
            }
        }
        result.append(content.substring(lastEnd));

        return result.toString();
    }

    // ─── Private Helpers ──────────────────────────────────────────────────────

    private static String maskSensitivePatterns(
            String content,
            Map<String, String> mapping,
            Map<String, Integer> counters) {

        content = maskPattern(content, EMAIL_PATTERN,        "EMAIL",      mapping, counters, -1);
        content = maskPattern(content, AWS_KEY_PATTERN,      "AWS_KEY",    mapping, counters, -1);
        content = maskPattern(content, SECRET_TOKEN_PATTERN, "SECRET",     mapping, counters, 1);
        content = maskPattern(content, IP_PATTERN,           "IP_ADDRESS", mapping, counters, -1);
        return content;
    }

    private static String maskPattern(
            String content,
            Pattern pattern,
            String name,
            Map<String, String> mapping,
            Map<String, Integer> counters,
            int captureGroup) {

        Matcher m = pattern.matcher(content);
        StringBuffer sb = new StringBuffer();

        while (m.find()) {
            String secret;
            try {
                secret = (captureGroup > 0) ? m.group(captureGroup) : m.group();
                if (secret == null) secret = m.group();
            } catch (IndexOutOfBoundsException e) {
                secret = m.group();
            }

            if (!mapping.containsKey(secret)) {
                int count = counters.getOrDefault("SECRET", 1);
                mapping.put(secret, name + "_" + count);
                counters.put("SECRET", count + 1);
            }

            String replacement;
            if (captureGroup > 0 && m.groupCount() >= captureGroup) {
                replacement = m.group().replace(secret, mapping.get(secret));
            } else {
                replacement = mapping.get(secret);
            }
            m.appendReplacement(sb, Matcher.quoteReplacement(replacement));
        }
        m.appendTail(sb);
        return sb.toString();
    }

    private static String classifyIdentifier(String ident, String content, int afterEnd) {
        if (ident.equals(ident.toUpperCase()) && ident.length() > 1 && !Character.isDigit(ident.charAt(0))) {
            return "CONST";
        }
        if (Character.isUpperCase(ident.charAt(0))) {
            return "Class";
        }
        // Method lookahead: check if followed by '('
        String remaining = content.substring(Math.min(afterEnd, content.length()));
        if (METHOD_LOOKAHEAD.matcher(remaining).lookingAt()) {
            return "method";
        }
        return "var";
    }
}
