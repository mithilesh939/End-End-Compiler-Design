

import re
import sys
import os


KEYWORDS = {
    'class', 'constructor', 'function', 'method', 'field', 'static',
    'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
    'this', 'let', 'do', 'if', 'else', 'while', 'return'
}

SYMBOLS = set('{}()[].,;+-*/&|<>=~')


XML_ESC = {
    '&': '&amp;',   
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
}


def xml_escape(s: str):
    return (
        s.replace('&', '&amp;')
         .replace('<', '&lt;')
         .replace('>', '&gt;')
         .replace('"', '&quot;')
    )


class JackTokenizer:
    

    def __init__(self, source_path: str):
        self.source_path = source_path
        self.tokens: list[tuple[str, str]] = []   # (type, value)
        self._raw = open(source_path, 'r', encoding='utf-8').read()

    

    def tokenize(self) -> list[tuple[str, str]]:
        """Strip comments, then scan tokens. Also writes <ClassName>T.xml."""
        cleaned = self._strip_comments(self._raw)
        self.tokens = list(self._scan(cleaned))
        self._write_xml()
        return self.tokens

    

    def _strip_comments(self, src: str) -> str:
        
        result = []
        i = 0
        n = len(src)
        IN_CODE   = 0
        IN_LINE   = 1   
        IN_BLOCK  = 2   
        IN_STRING = 3   

        state = IN_CODE
        while i < n:
            c = src[i]

            if state == IN_CODE:
                if c == '"':
                    result.append(c)
                    state = IN_STRING
                elif c == '/' and i + 1 < n and src[i+1] == '/':
                    state = IN_LINE
                    i += 2
                    continue
                elif c == '/' and i + 1 < n and src[i+1] == '*':
                    state = IN_BLOCK
                    i += 2
                    continue
                else:
                    result.append(c)

            elif state == IN_LINE:
                if c == '\n':
                    result.append('\n')
                    state = IN_CODE

            elif state == IN_BLOCK:
                if c == '*' and i + 1 < n and src[i+1] == '/':
                    state = IN_CODE
                    i += 2
                    continue
                elif c == '\n':
                    result.append('\n')   

            elif state == IN_STRING:
                result.append(c)
                if c == '"':
                    state = IN_CODE

            i += 1

        return ''.join(result)

    

    def _scan(self, src: str):
        
        i = 0
        n = len(src)
        while i < n:
            c = src[i]

            
            if c in ' \t\r\n':
                i += 1
                continue

            
            if c == '"':
                j = i + 1
                while j < n and src[j] != '"':
                    j += 1
                yield ('stringConstant', src[i+1:j])
                i = j + 1
                continue

            
            if c in SYMBOLS:
                yield ('symbol', c)
                i += 1
                continue

            
            if c.isdigit():
                j = i
                while j < n and src[j].isdigit():
                    j += 1
                val = int(src[i:j])
                if val > 32767:
                    raise ValueError(f"Integer constant {val} out of range [0,32767]")
                yield ('integerConstant', str(val))
                i = j
                continue

            
            if c.isalpha() or c == '_':
                j = i
                while j < n and (src[j].isalnum() or src[j] == '_'):
                    j += 1
                word = src[i:j]
                if word in KEYWORDS:
                    yield ('keyword', word)
                else:
                    yield ('identifier', word)
                i = j
                continue

            
            i += 1

    

    def _write_xml(self):

        base = os.path.splitext(os.path.basename(self.source_path))[0]

    # project root
        project_root = os.path.dirname(
           os.path.dirname(
                os.path.abspath(self.source_path)
            )
        )

    # create out folder
        out_dir = os.path.join(project_root, "out")
        os.makedirs(out_dir, exist_ok=True)

    # output path
        out_path = os.path.join(out_dir, base + 'T.xml')

        lines = ['<tokens>']
        for ttype, val in self.tokens:
            lines.append(f'  <{ttype}> {xml_escape(val)} </{ttype}>')
        lines.append('</tokens>')

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')

        print(f'[Tokenizer] Wrote {out_path}')



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python JackTokenizer.py <file.jack>")
        sys.exit(1)
    t = JackTokenizer(sys.argv[1])
    t.tokenize()
