


class SymbolTable:
    

    def __init__(self):
        self._class_table: dict[str, dict] = {}
        self._sub_table:   dict[str, dict] = {}
        self._counts = {'static': 0, 'field': 0, 'argument': 0, 'local': 0}

    def start_subroutine(self):
        
        self._sub_table = {}
        self._counts['argument'] = 0
        self._counts['local'] = 0

    def define(self, name: str, sym_type: str, kind: str):
        
        entry = {'type': sym_type, 'kind': kind, 'index': self._counts[kind]}
        self._counts[kind] += 1
        if kind in ('static', 'field'):
            self._class_table[name] = entry
        else:
            self._sub_table[name] = entry

    def var_count(self, kind: str) -> int:
        return self._counts[kind]

    def _lookup(self, name: str) -> dict | None:
        return self._sub_table.get(name) or self._class_table.get(name)

    def kind_of(self, name: str) -> str | None:
        e = self._lookup(name)
        return e['kind'] if e else None

    def type_of(self, name: str) -> str | None:
        e = self._lookup(name)
        return e['type'] if e else None

    def index_of(self, name: str) -> int | None:
        e = self._lookup(name)
        return e['index'] if e else None

    #

    def dump(self) -> str:
        lines = ['=== Symbol Table ===', '-- Class scope --']
        for name, e in self._class_table.items():
            lines.append(f"  {name:20s} type={e['type']:10s} kind={e['kind']:10s} idx={e['index']}")
        lines.append('-- Subroutine scope --')
        for name, e in self._sub_table.items():
            lines.append(f"  {name:20s} type={e['type']:10s} kind={e['kind']:10s} idx={e['index']}")
        return '\n'.join(lines)
