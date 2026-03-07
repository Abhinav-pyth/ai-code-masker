import sys
import os
import re
import json

KEYWORDS = {
    'java': {'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null', 'String', 'System', 'out', 'print', 'println', 'Override', 'Deprecated', 'SuppressWarnings'},
    'python': {'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield', 'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'bool', 'self', 'cls'},
    'js': {'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'else', 'export', 'extends', 'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'new', 'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void', 'while', 'with', 'yield', 'let', 'static', 'enum', 'await', 'async', 'true', 'false', 'null', 'undefined', 'NaN', 'Infinity', 'document', 'window', 'console', 'log', 'React', 'useState', 'useEffect', 'useCallback', 'useMemo', 'useRef', 'useContext', 'useReducer', 'require', 'module', 'exports', 'from'}
}

REGEXES = {
    'python': re.compile(
        r'(?P<string>"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')'
        r'|(?P<comment>#[^\n]*)'
        r'|(?P<identifier>\b[a-zA-Z_]\w*\b)'
    ),
    'java': re.compile(
        r'(?P<string>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')'
        r'|(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)'
        r'|(?P<identifier>\b[a-zA-Z_]\w*\b)'
    ),
    'js': re.compile(
        r'(?P<string>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`[\s\S]*?`)'
        r'|(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)'
        r'|(?P<identifier>\b[a-zA-Z_]\w*\b)'
    )
}

METHOD_REGEX = re.compile(r'\s*\(')

def get_language(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.py': return 'python'
    if ext == '.java': return 'java'
    if ext in ['.js', '.jsx', '.ts', '.tsx']: return 'js'
    return 'js' # fallback

def mask_content(content, lang='python'):
    mapping = {}
    counters = {'var': 1, 'Class': 1, 'method': 1, 'CONST': 1}
    
    def replacer(match):
        if match.group('string') is not None:
            return match.group('string')
        if match.group('comment') is not None:
            return match.group('comment')
        
        ident = match.group('identifier')
        if ident in KEYWORDS[lang]:
            return ident
            
        if ident not in mapping:
            # Determine type heuristic
            if ident.isupper() and len(ident) > 1:
                t = 'CONST'
            elif ident[0].isupper():
                t = 'Class'
            else:
                if METHOD_REGEX.match(content, match.end()):
                    t = 'method'
                else:
                    t = 'var'
                    
            masked_name = f"{t}_{counters[t]}"
            counters[t] += 1
            mapping[ident] = masked_name
            
        return mapping[ident]

    masked_content = REGEXES[lang].sub(replacer, content)
    return masked_content, mapping

def unmask_content(content, mapping, lang='python'):
    # Invert mapping: masked_name -> original_name
    inv_mapping = {v: k for k, v in mapping.items()}
    
    def replacer(match):
        if match.group('string') is not None:
            return match.group('string')
        if match.group('comment') is not None:
            return match.group('comment')
            
        ident = match.group('identifier')
        if ident in inv_mapping:
            return inv_mapping[ident]
        return ident

    unmasked_content = REGEXES[lang].sub(replacer, content)
    return unmasked_content

def mask_file(filepath):
    lang = get_language(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    masked_content, mapping = mask_content(content, lang)    
    with open(masked_filepath, 'w', encoding='utf-8') as f:
        f.write(masked_content)
        
    with open(map_filepath, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)
        
    print(f"Masked file saved to: {masked_filepath}")
    print(f"Mapping saved to: {map_filepath}")

def unmask_file(filepath):
    # Expects filepath ending with .masked
    if not filepath.endswith('.masked'):
        print("Error: For unmasking, please provide the .masked file.")
        sys.exit(1)
        
    base_filepath = filepath[:-7] # remove .masked
    map_filepath = base_filepath + '.map.json'
    
    if not os.path.exists(map_filepath):
        print(f"Error: Mapping file {map_filepath} not found.")
        sys.exit(1)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        masked_content = f.read()
        
    with open(map_filepath, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
        
    lang = get_language(base_filepath)
    unmasked_content = unmask_content(masked_content, mapping, lang)
    
    unmasked_filepath = base_filepath + '.unmasked'
    with open(unmasked_filepath, 'w', encoding='utf-8') as f:
        f.write(unmasked_content)
        
    print(f"Unmasked file saved to: {unmasked_filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python masker.py <mask|unmask> <filepath>")
        sys.exit(1)
        
    action = sys.argv[1]
    filepath = sys.argv[2]
    
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        sys.exit(1)
        
    if action == 'mask':
        mask_file(filepath)
    elif action == 'unmask':
        unmask_file(filepath)
    else:
        print("Unknown action. Use 'mask' or 'unmask'.")
        sys.exit(1)
