from visualinux.lang.parser import *
from visualinux.lang.parser.utils import *
from visualinux.lang.parser.converter     import Converter
from visualinux.lang.parser.translator    import Translator

from visualinux.model import *

from pathlib import Path

class Parser:
    '''Usage: Parser(grammar).parse(program).
    - The Lark library serves as the lexical + syntax analyzer.
      It generates a syntax tree (i.e. lark.ParseTree) from the DSL source code.
    - The Converter() converts the raw lark.ParseTree into a OO-style class representation, i.e. list[Assignment | Plot].
    - The Translator() serves as the semantic analyzer.
      It analyzes the instruction list and generates static representations for all to-be-plotted shapes.
    - The Interpreter() is used during each Engine.sync() to evaluate expressions.
      It generates shape representations with runtime data, and finally converts them to json format.
    '''

    def __init__(self, grammar: Path):
        # self.__parser = Lark(grammar, parser='lalr')
        # self.__parser = Lark(grammar.read_text(), keep_all_tokens=True)
        self.__parser = Lark(grammar.read_text(), strict=True)
        self.__imported: set[Path] = set()

    def parse(self, program: Path, silent: bool = False) -> View:

        # parsetree = self.__parser.parse(program.read_text())
        # if not silent: if VL_DEBUG_ON: printd(parsetree.pretty())
        try:
            parsetree = ParseTree('start', self.__parse(program, DSL_PROGRAM_DIR))
        finally:
            self.__imported.clear()

        insts = Converter().convert(parsetree)
        model = Translator().translate(insts)

        return model

    def __parse(self, program: Path, rootdir: Path) -> list[Token | Tree[Token]]:
        '''The inner parse procedure that handles imports first.
        '''
        try:
            parsetree = self.__parser.parse(program.read_text())
            self.__view_rename(parsetree, program.relative_to(rootdir))
        except Exception as e:
            raise fuck_exc(e.__class__, str(e))

        insts: list[Token | Tree[Token]] = []
        for inst in scan_children_as_tree(parsetree):
            if inst.data == 'import':
                import_path = serialize(inst.children[0]).replace('.', '/')
                import_program = rootdir / f'{import_path}.vl'
                if not import_program.is_file():
                    raise fuck_exc(FileNotFoundError, f'vl import error: failed to find {import_program}')
                if import_program in self.__imported:
                    continue
                self.__imported.add(import_program)
                insts += self.__parse(import_program, rootdir)
            elif inst.data == 'instruction':
                insts.append(inst)
            else:
                raise fuck_exc(AssertionError, f'dsl program must be the form of (import | inst)*, but {inst.data = } found.')

        return insts

    def __view_rename(self, parsetree: ParseTree, relpath: Path):
        if vl_debug_on(): printd(f'view_rename {relpath}')
        for node in scan_children_as_tree(parsetree):
            if node.data != 'instruction':
                continue
            inst = child_as_tree(node, 0)
            if inst.data == 'viewdef':
                token = child_as_tree(inst, 0).children[0]
                assert isinstance(token, Token)
                token.value = str(relpath.with_suffix('')).replace('/', '.') + '.' + token.value
                if vl_debug_on(): printd(f'  view_rename => {token.value!s}')
