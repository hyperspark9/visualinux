#!/usr/bin/env python3

import linkmap_parser
import elf_sym_parser

from pathlib import Path
import json

DIR_SCRIPTS = Path(__file__).absolute().parent
DIR_KERNEL  = DIR_SCRIPTS.parents[1] / 'kernel'

if __name__ == '__main__':
    
    path_linkmap = DIR_KERNEL / 'vmlinux.map'
    path_elf     = DIR_KERNEL / 'vmlinux'
    path_addrmap = DIR_KERNEL / 'addrmap.lst'

    if not path_linkmap.is_file():
        raise FileNotFoundError(path_linkmap)
    if not path_elf.is_file():
        raise FileNotFoundError(path_elf)

    addrmaps: dict[str, dict[str, dict[str, str]]] = {}
    linkmap_parser.parse(addrmaps, path_linkmap)
    elf_sym_parser.parse(addrmaps, path_elf)

    tag = '__addrmap__'
    assert tag not in addrmaps
    addrmaps[tag] = None # type: ignore

    with open(path_addrmap, 'w') as f:
        json.dump(addrmaps, f, indent=4)
        f.write('\n')
