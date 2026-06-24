
import os



KIND_TO_SEGMENT = {
    'static':   'static',
    'field':    'this',
    'argument': 'argument',
    'local':    'local',
    'var':      'local',
}


class VMWriter:
    def __init__(self, out_path: str):
        self._f = open(out_path, 'w', encoding='utf-8')

    

    def write_push(self, segment: str, index: int):
        self._emit(f'push {segment} {index}')

    def write_pop(self, segment: str, index: int):
        self._emit(f'pop {segment} {index}')

    

    ARITH_MAP = {
        '+': 'add', '-': 'sub', '*': 'call Math.multiply 2',
        '/': 'call Math.divide 2', '&': 'and', '|': 'or',
        '<': 'lt', '>': 'gt', '=': 'eq',
        '~': 'not', 'neg': 'neg','not': 'not',
    }

    def write_arithmetic(self, op: str):
        cmd = self.ARITH_MAP.get(op)
        if cmd is None:
            raise ValueError(f"Unknown op: {op}")
        self._emit(cmd)

    

    def write_label(self, label: str):
        self._emit(f'label {label}')

    def write_goto(self, label: str):
        self._emit(f'goto {label}')

    def write_if(self, label: str):
        self._emit(f'if-goto {label}')

    

    def write_function(self, name: str, n_locals: int):
        self._emit(f'function {name} {n_locals}')

    def write_call(self, name: str, n_args: int):
        self._emit(f'call {name} {n_args}')

    def write_return(self):
        self._emit('return')

    

    def _emit(self, line: str):
        self._f.write(line + '\n')

    def close(self):
        self._f.close()
