from visualinux import *
from visualinux.lang import Parser
from visualinux.model import View
from visualinux.runtime import State
from visualinux.model.symtable import *
from visualinux.runtime.gdb.adaptor import gdb_adaptor

import threading
import json
import shutil

import time
import cProfile, pstats, io
from pstats import SortKey

TMP_DIR = VL_DIR / 'tmp'

class Engine:
    '''Note that there should be only one Engine instance existing.
    '''
    def __init__(self, dsl_grammar: Path) -> None:

        self.dsl_parser = Parser(dsl_grammar)
        self.model = View()
        self.history: list[State] = []

        self.lock = threading.Lock()

    def update(self, dsl_program: Path):
        if vl_debug_on(): printd(f'vl_update({dsl_program})')
        with self.lock:
            self.model = self.dsl_parser.parse(dsl_program)
            if vl_debug_on(): printd(str(self.model))
        if vl_debug_on(): printd(f'vl_update() OK')
        self.sync()

    def sync(self) -> State:
        if vl_debug_on(): printd(f'vl_sync()')
        TMP_DIR.mkdir(exist_ok=True)
        gdb_adaptor.reset()
        KValue.reset()
        SymTable.reset()
        pr = cProfile.Profile()
        pr.disable()
        if vl_perf_on():
            pr.enable()
        with self.lock:
            try:
                state = self.model.sync()
            except Exception as e:
                print(f'vl_sync() unhandled exception: ' + str(e))
                state = State()
        self.history.append(state)
        if vl_debug_on(): printd(f'vl_sync(): view sync OK')
        if vl_perf_on():
            pr.disable()
            s = io.StringIO()
            sortby = SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            ps.dump_stats(TMP_DIR / 'visualinux-sync.perf')
            # print(s.getvalue())

        for name, subview in state.subviews.items():
            self.export_for_debug(subview.to_json(), TMP_DIR / f'{name}.json')

        # DUMP_DIR = VL_DIR / 'visualizer' / 'public' / 'statedump'
        # def export():
        #     print(f'vl_sync(): data export')
        #     full_json_data = {}
        #     for name, subview in state.subviews.items():
        #         full_json_data[name] = subview.to_json()
        #     if (DUMP_DIR / 'latest.json').is_file():
        #         shutil.copy(DUMP_DIR / 'latest.json', DUMP_DIR / 'old.json')
        #     self.export_for_debug(full_json_data, DUMP_DIR / 'latest.json')
        #     print(f'vl_sync(): data export OK')
        # export()

        DUMP_DIR = VL_DIR / 'visualizer' / 'public' / 'statedump'
        DUMP_DIR.mkdir(exist_ok=True)
        def reload_and_reexport():
            print(f'vl_sync(): data export')
            full_json_data = {}
            for path in (TMP_DIR).glob('**/*.json'):
                full_json_data[path.stem] = self.import_for_debug(path)
            if (DUMP_DIR / 'latest.json').is_file():
                shutil.copy(DUMP_DIR / 'latest.json', DUMP_DIR / 'old.json')
            self.export_for_debug(full_json_data, DUMP_DIR / 'latest.json')
            print(f'vl_sync(): data export OK')
        reload_and_reexport()

        return state

    def curr_state(self) -> State:
        assert self.history
        return self.history[-1]

    # def send(self, json_data: dict):
    #     url = f'{self.server_url}/newstate'
    #     headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    #     print(f'POST send data to {url!s}')
    #     response = requests.post(url, headers=headers, json=json_data)
    #     print(f'POST send data {response = }')

    def export_for_debug(self, json_data: dict, path: Path):
        with open(path, 'w') as f:
            json.dump(json_data, f, indent=4)

    def import_for_debug(self, path: Path) -> dict:
        with open(path, 'r') as f:
            return json.load(f)
