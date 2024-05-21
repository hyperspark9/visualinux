#!/usr/bin/env python3

from pathlib import Path
import sys
import logging
import lief

addrmap_t = dict[str, dict[str, dict[str, str]]]

def parse(addrmaps: addrmap_t, path_elf: Path):

    # invariant check
    if not path_elf.is_file():
        raise FileNotFoundError(path_elf)

    # parse the elf
    binary = lief.parse(str(path_elf))

    # init
    logging.basicConfig(level=logging.INFO)
    curr_region = '__elf__'
    addrmaps.setdefault(curr_region, {'functions': {}, 'objects': {}})

    # fetch data from symbol table

    logging.info(f'+ parsing symbol table of elf {path_elf}...')

    def is_ignored(name: str):
        # for prefix in ['__gcov', '__tracepoint', '__SCK']:
        if name.startswith('__gcov'):
            return True
        return False

    for symbol in binary.symbols:
        symbol: lief.ELF.Symbol
        # if symbol.is_function:
        #     addrmaps[curr_region]['functions'][symbol.name] = f'{symbol.value:x}'
        if symbol.is_variable and not is_ignored(symbol.name):
            addrmaps[curr_region]['objects'][symbol.name] = f'{symbol.value:x}'

    logging.info('+ parsing symbol table of elf OK.')
