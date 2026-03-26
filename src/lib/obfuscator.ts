const KEYWORDS: Record<string, Set<string>> = {
  java: new Set(['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null', 'String', 'System', 'out', 'print', 'println', 'Override', 'Deprecated', 'SuppressWarnings']),
  python: new Set(['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield', 'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'bool', 'self', 'cls']),
  js: new Set(['break', 'case', 'catch', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'else', 'export', 'extends', 'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void', 'while', 'with', 'yield', 'let', 'static', 'enum', 'await', 'async', 'true', 'false', 'null', 'undefined', 'NaN', 'Infinity', 'document', 'window', 'console', 'log', 'React', 'useState', 'useEffect', 'useCallback', 'useMemo', 'useRef', 'useContext', 'useReducer', 'require', 'module', 'exports', 'from'])
};

const REGEXES: Record<string, RegExp> = {
  python: /("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(#.*)|(\b[a-zA-Z_]\w*\b)/g,
  java: /("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\/\/.*|\/\*[\s\S]*?\*\/)|(\b[a-zA-Z_]\w*\b)/g,
  js: /("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[\s\S]*?`)|(\/\/.*|\/\*[\s\S]*?\*\/)|(\b[a-zA-Z_]\w*\b)/g
};

export function getLanguage(filename: string): string {
  if (!filename) return 'js';
  const ext = filename.split('.').pop()?.toLowerCase();
  if (ext === 'py') return 'python';
  if (ext === 'java') return 'java';
  if (['js', 'jsx', 'ts', 'tsx'].includes(ext || '')) return 'js';
  return 'js';
}

export function obfuscateIdentifiers(content: string, lang = 'js') {
  const mapping: Record<string, string> = {};
  const counters = { var: 1, Class: 1, method: 1, CONST: 1 };
  const regex = REGEXES[lang] || REGEXES['js'];
  const keywords = KEYWORDS[lang] || KEYWORDS['js'];

  // Workaround for method detection using trailing parenthesis heuristic.
  // In JS regex we'll simulate the match replacer loop.
  let obfuscatedContent = "";
  let lastIndex = 0;
  
  // We need to match globally and manually construct the string to peek ahead
  let match;
  regex.lastIndex = 0;
  while ((match = regex.exec(content)) !== null) {
    obfuscatedContent += content.slice(lastIndex, match.index);
    const [fullMatch, str, comment, identifier] = match;

    if (str !== undefined) {
      obfuscatedContent += str;
    } else if (comment !== undefined) {
      obfuscatedContent += comment;
    } else if (identifier !== undefined) {
      if (keywords.has(identifier)) {
        obfuscatedContent += identifier;
      } else {
        if (!mapping[identifier]) {
          let t: keyof typeof counters = 'var';
          if (identifier.toUpperCase() === identifier && identifier.length > 1) {
            t = 'CONST';
          } else if (identifier[0] === identifier[0].toUpperCase()) {
            t = 'Class';
          } else {
            // Peek next characters ignoring whitespace
            const remainder = content.slice(regex.lastIndex);
            if (/^\s*\(/.test(remainder)) {
              t = 'method';
            }
          }
          const maskedName = `${t}_${counters[t]}`;
          counters[t]++;
          mapping[identifier] = maskedName;
        }
        obfuscatedContent += mapping[identifier];
      }
    }
    lastIndex = regex.lastIndex;
  }
  obfuscatedContent += content.slice(lastIndex);

  return { obfuscatedContent, mapping };
}

export function unmaskContent(content: string, mapping: Record<string, string>, lang = 'js') {
  const invMapping: Record<string, string> = {};
  for (const [k, v] of Object.entries(mapping)) {
    invMapping[v] = k;
  }

  const regex = REGEXES[lang] || REGEXES['js'];
  regex.lastIndex = 0;
  
  let unmaskedContent = "";
  let lastIndex = 0;
  let match;
  
  while ((match = regex.exec(content)) !== null) {
    unmaskedContent += content.slice(lastIndex, match.index);
    const [fullMatch, str, comment, identifier] = match;

    if (str !== undefined) {
      unmaskedContent += str;
    } else if (comment !== undefined) {
      unmaskedContent += comment;
    } else if (identifier !== undefined) {
      if (invMapping[identifier]) {
        unmaskedContent += invMapping[identifier];
      } else {
        unmaskedContent += identifier;
      }
    }
    lastIndex = regex.lastIndex;
  }
  unmaskedContent += content.slice(lastIndex);
  
  return unmaskedContent;
}
