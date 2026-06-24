
import os
from SymbolTable import SymbolTable
from VMWriter import VMWriter

XML_ESC = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}


def xml_escape(s: str):
    return (
        s.replace('&', '&amp;')
         .replace('<', '&lt;')
         .replace('>', '&gt;')
         .replace('"', '&quot;')
    )


OP_SYMBOLS   = set('+-*/&|<>=')
UNARY_OPS    = set('-~')
KEYWORD_CONSTS = {'true', 'false', 'null', 'this'}


class CompilationEngine:
    

    def __init__(self, tokens: list[tuple[str, str]], source_path: str):
        self._tokens   = tokens
        self._pos      = 0
        self._indent   = 0
        self._xml_lines: list[str] = []
        self._label_counter = 0

        base = os.path.splitext(source_path)[0]

        xml_path = base + '.xml'
        vm_path  = base + '.vm'

        self._xml_path   = xml_path
        self._class_name = base
        self._sym        = SymbolTable()
        self._vm         = VMWriter(vm_path)
        self._vm_path    = vm_path

    

    def _peek(self) -> tuple[str, str] | None:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _peek_val(self) -> str:
        t = self._peek()
        return t[1] if t else ''

    def _advance(self) -> tuple[str, str]:
        t = self._tokens[self._pos]
        self._pos += 1
        return t

    def _eat(self, value: str) -> tuple[str, str]:
        t = self._advance()
        if t[1] != value:
            raise SyntaxError(f"Expected '{value}', got '{t[1]}' (type={t[0]})")
        return t

    def _eat_type(self, ttype: str) -> tuple[str, str]:
        t = self._advance()
        if t[0] != ttype:
            raise SyntaxError(f"Expected token type '{ttype}', got '{t[0]}' (val={t[1]})")
        return t

    

    def _xml(self, line: str):
        self._xml_lines.append('  ' * self._indent + line)

    def _xml_token(self, ttype: str, val: str):
        self._xml(f'<{ttype}> {xml_escape(val)} </{ttype}>')

    def _xml_open(self, tag: str):
        self._xml(f'<{tag}>')
        self._indent += 1

    def _xml_close(self, tag: str):
        self._indent -= 1
        self._xml(f'</{tag}>')

    def _record(self, ttype: str, val: str):
        
        self._eat(val)
        self._xml_token(ttype, val)

    def _record_advance(self) -> tuple[str, str]:
       
        t = self._advance()
        self._xml_token(t[0], t[1])
        return t

    

    def _new_label(self, prefix: str = 'L') -> str:
        lbl = f'{prefix}_{self._label_counter}'
        self._label_counter += 1
        return lbl

    

    def compile_class(self):
        
        self._xml_open('class')
        self._record('keyword', 'class')
        self._class_name = self._peek_val()
        self._record_advance()          # className
        self._record('symbol', '{')

        while self._peek_val() in ('static', 'field'):
            self.compile_class_var_dec()

        while self._peek_val() in ('constructor', 'function', 'method'):
            self.compile_subroutine_dec()

        self._record('symbol', '}')
        self._xml_close('class')
        self._save_xml()
        self._vm.close()
        print(f'[Compiler] Wrote {self._xml_path}')
        print(f'[Compiler] Wrote {self._vm_path}')

    def _save_xml(self):
        with open(self._xml_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self._xml_lines) + '\n')

    

    def compile_class_var_dec(self):
        
        self._xml_open('classVarDec')
        _, kind = self._record_advance()          
        _, vtype = self._record_advance()         
        _, name = self._record_advance()          
        self._sym.define(name, vtype, kind)

        while self._peek_val() == ',':
            self._record('symbol', ',')
            _, name = self._record_advance()
            self._sym.define(name, vtype, kind)

        self._record('symbol', ';')
        self._xml_close('classVarDec')

    

    def compile_subroutine_dec(self):
        
        self._sym.start_subroutine()
        self._xml_open('subroutineDec')

        _, sub_kind = self._record_advance()    
        self._record_advance()                  
        _, sub_name = self._record_advance()    

        
        if sub_kind == 'method':
            self._sym.define('this', self._class_name, 'argument')

        self._record('symbol', '(')
        self.compile_parameter_list()
        self._record('symbol', ')')
        self.compile_subroutine_body(sub_name, sub_kind)
        self._xml_close('subroutineDec')

    def compile_parameter_list(self):
        
        self._xml_open('parameterList')
        if self._peek_val() != ')':
            _, vtype = self._record_advance()
            _, name  = self._record_advance()
            self._sym.define(name, vtype, 'argument')
            while self._peek_val() == ',':
                self._record('symbol', ',')
                _, vtype = self._record_advance()
                _, name  = self._record_advance()
                self._sym.define(name, vtype, 'argument')
        self._xml_close('parameterList')

    def compile_subroutine_body(self, sub_name: str, sub_kind: str):
        
        self._xml_open('subroutineBody')
        self._record('symbol', '{')

        while self._peek_val() == 'var':
            self.compile_var_dec()

        n_locals = self._sym.var_count('local')
        full_name = f'{self._class_name}.{sub_name}'
        self._vm.write_function(full_name, n_locals)

        
        if sub_kind == 'constructor':
            n_fields = self._sym.var_count('field')
            self._vm.write_push('constant', n_fields)
            self._vm.write_call('Memory.alloc', 1)
            self._vm.write_pop('pointer', 0)
        elif sub_kind == 'method':
            self._vm.write_push('argument', 0)
            self._vm.write_pop('pointer', 0)

        self.compile_statements()
        self._record('symbol', '}')
        self._xml_close('subroutineBody')

    def compile_var_dec(self):
        
        self._xml_open('varDec')
        self._record('keyword', 'var')
        _, vtype = self._record_advance()
        _, name  = self._record_advance()
        self._sym.define(name, vtype, 'local')

        while self._peek_val() == ',':
            self._record('symbol', ',')
            _, name = self._record_advance()
            self._sym.define(name, vtype, 'local')

        self._record('symbol', ';')
        self._xml_close('varDec')

    

    def compile_statements(self):
        self._xml_open('statements')
        while self._peek_val() in ('let', 'if', 'while', 'do', 'return'):
            v = self._peek_val()
            if   v == 'let':    self.compile_let()
            elif v == 'if':     self.compile_if()
            elif v == 'while':  self.compile_while()
            elif v == 'do':     self.compile_do()
            elif v == 'return': self.compile_return()
        self._xml_close('statements')

    def compile_let(self):
        
        self._xml_open('letStatement')
        self._record('keyword', 'let')
        _, var_name = self._record_advance()

        is_array = self._peek_val() == '['
        if is_array:
            
            self._push_var(var_name)
            self._record('symbol', '[')
            self.compile_expression()
            self._record('symbol', ']')
            self._vm.write_arithmetic('+')   

        self._record('symbol', '=')
        self.compile_expression()
        self._record('symbol', ';')

        if is_array:
            
            self._vm.write_pop('temp', 0)       
            self._vm.write_pop('pointer', 1)    
            self._vm.write_push('temp', 0)      
            self._vm.write_pop('that', 0)
        else:
            self._pop_var(var_name)

        self._xml_close('letStatement')

    def compile_if(self):
        
        self._xml_open('ifStatement')
        l_false = self._new_label('IF_FALSE')
        l_end   = self._new_label('IF_END')

        self._record('keyword', 'if')
        self._record('symbol', '(')
        self.compile_expression()
        self._record('symbol', ')')

        self._vm.write_arithmetic('not')
        self._vm.write_if(l_false)

        self._record('symbol', '{')
        self.compile_statements()
        self._record('symbol', '}')
        self._vm.write_goto(l_end)

        self._vm.write_label(l_false)
        if self._peek_val() == 'else':
            self._record('keyword', 'else')
            self._record('symbol', '{')
            self.compile_statements()
            self._record('symbol', '}')

        self._vm.write_label(l_end)
        self._xml_close('ifStatement')

    def compile_while(self):
        
        self._xml_open('whileStatement')
        l_top  = self._new_label('WHILE_TOP')
        l_end  = self._new_label('WHILE_END')

        self._record('keyword', 'while')
        self._vm.write_label(l_top)

        self._record('symbol', '(')
        self.compile_expression()
        self._record('symbol', ')')

        self._vm.write_arithmetic('not')
        self._vm.write_if(l_end)

        self._record('symbol', '{')
        self.compile_statements()
        self._record('symbol', '}')
        self._vm.write_goto(l_top)
        self._vm.write_label(l_end)
        self._xml_close('whileStatement')

    def compile_do(self):
        
        self._xml_open('doStatement')
        self._record('keyword', 'do')
        self._compile_subroutine_call()
        self._vm.write_pop('temp', 0)   
        self._record('symbol', ';')
        self._xml_close('doStatement')

    def compile_return(self):
        
        self._xml_open('returnStatement')
        self._record('keyword', 'return')
        if self._peek_val() != ';':
            self.compile_expression()
        else:
            self._vm.write_push('constant', 0)   # void return
        self._record('symbol', ';')
        self._vm.write_return()
        self._xml_close('returnStatement')

    

    def compile_expression(self):
        
        self._xml_open('expression')
        self.compile_term()
        while self._peek_val() in OP_SYMBOLS:
            _, op = self._record_advance()
            self.compile_term()
            self._vm.write_arithmetic(op)
        self._xml_close('expression')

    def compile_term(self):
        
        self._xml_open('term')
        ttype, val = self._peek()

        if ttype == 'integerConstant':
            self._record_advance()
            self._vm.write_push('constant', int(val))

        elif ttype == 'stringConstant':
            self._record_advance()
            
            self._vm.write_push('constant', len(val))
            self._vm.write_call('String.new', 1)
            for ch in val:
                self._vm.write_push('constant', ord(ch))
                self._vm.write_call('String.appendChar', 2)

        elif ttype == 'keyword' and val in KEYWORD_CONSTS:
            self._record_advance()
            if val == 'true':
                self._vm.write_push('constant', 0)
                self._vm.write_arithmetic('~')
            elif val in ('false', 'null'):
                self._vm.write_push('constant', 0)
            elif val == 'this':
                self._vm.write_push('pointer', 0)

        elif val == '(':
            self._record('symbol', '(')
            self.compile_expression()
            self._record('symbol', ')')

        elif val in UNARY_OPS:
            _, op = self._record_advance()
            self.compile_term()
            self._vm.write_arithmetic('~' if op == '~' else 'neg')

        elif ttype == 'identifier':
            
            if self._pos + 1 < len(self._tokens):
                next_val = self._tokens[self._pos + 1][1]
            else:
                next_val = ''

            if next_val == '[':                    
                _, arr_name = self._record_advance()
                self._push_var(arr_name)
                self._record('symbol', '[')
                self.compile_expression()
                self._record('symbol', ']')
                self._vm.write_arithmetic('+')
                self._vm.write_pop('pointer', 1)
                self._vm.write_push('that', 0)

            elif next_val in ('(', '.'):            
                self._compile_subroutine_call()

            else:                                   
                _, name = self._record_advance()
                self._push_var(name)

        self._xml_close('term')

    def _compile_subroutine_call(self):
        
        _, name = self._record_advance()   

        n_args  = 0
        if self._peek_val() == '.':
            self._record('symbol', '.')
            _, method_name = self._record_advance()

            
            kind = self._sym.kind_of(name)
            if kind is not None:
                
                obj_type = self._sym.type_of(name)
                self._push_var(name)
                n_args = 1
                call_name = f'{obj_type}.{method_name}'
            else:
                
                call_name = f'{name}.{method_name}'
        else:
            
            self._vm.write_push('pointer', 0)
            n_args    = 1
            call_name = f'{self._class_name}.{name}'

        self._record('symbol', '(')
        n_args += self.compile_expression_list()
        self._record('symbol', ')')
        self._vm.write_call(call_name, n_args)

    def compile_expression_list(self) -> int:
        
        self._xml_open('expressionList')
        count = 0
        if self._peek_val() != ')':
            self.compile_expression()
            count = 1
            while self._peek_val() == ',':
                self._record('symbol', ',')
                self.compile_expression()
                count += 1
        self._xml_close('expressionList')
        return count

    

    def _push_var(self, name: str):
        kind  = self._sym.kind_of(name)
        index = self._sym.index_of(name)
        if kind == 'field':
            self._vm.write_push('this', index)
        elif kind is not None:
            self._vm.write_push(kind, index)
        

    def _pop_var(self, name: str):
        kind  = self._sym.kind_of(name)
        index = self._sym.index_of(name)
        if kind == 'field':
            self._vm.write_pop('this', index)
        elif kind is not None:
            self._vm.write_pop(kind, index)
