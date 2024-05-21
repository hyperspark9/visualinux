#!/usr/bin/env python3

# reference
# https://github.com/jpgvandijk/linker-map-viewer.git

from pathlib import Path
import sys
import logging
import re
# import json

# helpdoc = '''Usage: linkmap_parser.py <linkmap> <addrmap>
# Genearte <addrmap> from <linkmap> and kernel.lst(tbd) for each subject.
# '''

# regex patterns

title_begin = 'Linker script and memory map'
title_end   = 'OUTPUT('

pattern_uint    = r'(0x[0-9a-fA-F]+)'
pattern_secname = r'(\.[a-zA-Z_][\.\w]*|COMMON)'
pattern_name    = r'([\.\w]+)'

pattern_addr = pattern_uint
pattern_size = pattern_uint
pattern_filename   = pattern_name
pattern_identifier = pattern_name

pattern_section = \
    r'\s*' + pattern_secname + r'\s+' + pattern_addr + r'\s+' + \
    pattern_size + ' load address ' + pattern_addr

pattern_region  = \
    r'\s*' + pattern_secname + r'\s+' + pattern_addr + r'\s+' + \
    pattern_size + r'\s+' + pattern_filename

pattern_content = \
    r'\s+' + pattern_addr + r'\s+' + pattern_identifier + r'$'

pattern_fill = fr'FILL mask {pattern_uint}'

# parse

addrmap_t = dict[str, dict[str, dict[str, str]]]

def parse(addrmaps: addrmap_t, path_linkmap: Path):
# def parse(path_linkmap: Path, path_addrmap: Path):

    # invariant check
    if not path_linkmap.is_file():
        raise FileNotFoundError(path_linkmap)

    # read the link map

    with open(path_linkmap, 'r') as f:
        content = f.read()

    content = content.split(title_begin, maxsplit=1)[1]
    content = content.split(title_end, maxsplit=1)[0]
    lines = content.splitlines()

    # init
    logging.basicConfig(level=logging.INFO)
    # addrmaps: dict[str, dict[str, dict[str, str]]] = {}

    # regex match for each memory map entry

    logging.info(f'+ parsing linkmap {path_linkmap}...')

    curr_section: str = ''
    curr_region:  str = ''
    for line in lines:

        if matched := re.match(pattern_section, line):
            curr_section = matched.group(1)
            curr_region  = ''
            logging.debug(f'{curr_section = }')
            continue
        if not curr_section:
            continue

        if matched := re.match(pattern_region, line):
            sec, curr_region = matched.group(1), matched.group(4)
            logging.debug(f'{sec = }, {curr_region = }')
            continue

        if matched := re.match(pattern_content, line):
            addr, name = matched.groups()
            addr_x = f'{int(addr, base=16):#x}'
            assert int(addr, base=16) == int(addr_x, base=16)
            addr = addr_x
            addrmaps.setdefault(curr_region, {'functions': {}, 'objects': {}})
            if curr_section == '.text':
                addrmaps[curr_region]['functions'][name] = addr
            else:
                addrmaps[curr_region]['objects'][name]   = addr

    logging.info(f'+ parsing linkmap OK.')

#     # write in format

#     # for region, addrmap in addrmaps.items():
#     #     logging.debug(f'{region} {addrmap}')

#     tag = '__addrmap__'
#     assert tag not in addrmaps
#     addrmaps[tag] = None # type: ignore

#     with open(path_addrmap, 'w') as f:
#         json.dump(addrmaps, f, indent=4)
#         f.write('\n')

# # help

# def help():
#     print(helpdoc)
#     exit(0)

# # main

# if __name__ == '__main__':

#     logging.basicConfig(level=logging.INFO)

#     if len(sys.argv) != 3:
#         help()

#     path_linkmap, path_addrmap = Path(sys.argv[1]), Path(sys.argv[2])
#     parse(path_linkmap, path_addrmap)
