import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# global initialization

from visualinux import *
from visualinux.engine import Engine

dsl_grammar = VL_DIR / 'visualinux' / 'lang' / 'grammar.lark'
dsl_engine = Engine(dsl_grammar)

# definition of custom gdb commands

def do_vl_update(relpath: str):
    print(f'do_vl_update({relpath})')
    if not relpath:
        relpath = 'default.vl'
    if not relpath.endswith('.vl'):
        relpath = relpath + '.vl'
    path = DSL_PROGRAM_DIR / relpath
    dsl_engine.update(path)

class VlUpdate(gdb.Command):

    def __init__(self):
        super(VlUpdate, self).__init__("vl-update", gdb.COMMAND_USER)

    def invoke(self, arg: str, from_tty: bool) -> None:
        set_vl_debug(False)
        set_vl_perf(False)
        do_vl_update(arg)

VlUpdate()

class VlUpdateDEBUG(gdb.Command):

    def __init__(self):
        super(VlUpdateDEBUG, self).__init__("vl-update-debug", gdb.COMMAND_USER)

    def invoke(self, arg: str, from_tty: bool) -> None:
        set_vl_debug(True)
        set_vl_perf(False)
        do_vl_update(arg)

VlUpdateDEBUG()

class VlUpdatePerf(gdb.Command):

    def __init__(self):
        super(VlUpdatePerf, self).__init__("vl-update-perf", gdb.COMMAND_USER)

    def invoke(self, arg: str, from_tty: bool) -> None:
        set_vl_debug(False)
        set_vl_perf(True)
        do_vl_update(arg)

VlUpdatePerf()
