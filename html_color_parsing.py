#!/usr/bin/env python3
import argparse
import logging
from typing import Dict

log = logging.getLogger(__name__)


class Color:

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return 'Color(#{:02X}{:02X}{:02X})'.format(self.r, self.g, self.b)


COLOR_MAP: Dict[str, Color] = {}


def is_hex(inputc: str):
    assert len(inputc) == 1
    inputc = inputc.lower()
    return inputc in ('a', 'b', 'c', 'd', 'e', 'f')


def allhex(inputstr: str):
    return all(is_hex(c) for c in inputstr)


def gethex(inputstr: str):
    return int(inputstr, 16)


# https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#rules-for-parsing-a-legacy-colour-value
def parse_color(inputstr: str):
    if len(inputstr) < 1:
        raise Exception('empty string supplied')
    inputstr = inputstr.strip()
    if inputstr.lower() == 'transparent':
        raise Exception('transparent is not a color!')
    if inputstr in COLOR_MAP:
        return COLOR_MAP[inputstr]
    if len(inputstr) == 4 and inputstr[0] == '#' and allhex(inputstr[1:]):
        ri = gethex(inputstr[1]) * 17
        gi = gethex(inputstr[2]) * 17
        bi = gethex(inputstr[3]) * 17
        return Color(ri, gi, bi)
    new_inputstr = ''
    for c in inputstr:
        if ord(c) > 0xFFFF:
            new_inputstr += '00'
        else:
            new_inputstr += c
    inputstr = new_inputstr
    if len(inputstr) > 128:
        inputstr = inputstr[:128]
    if inputstr[0] == '#':
        inputstr = inputstr[1:]
    new_inputstr = ''
    for c in inputstr:
        if not is_hex(c):
            new_inputstr += '0'
        else:
            new_inputstr += c
    inputstr = new_inputstr
    while len(inputstr) == 0 or len(inputstr) % 3 > 0:
        inputstr += '0'
    length = len(inputstr) // 3
    r = inputstr[0 * length:1 * length]
    g = inputstr[1 * length:2 * length]
    b = inputstr[2 * length:3 * length]
    components = [r, g, b]
    new_components = []
    if length > 8:
        for component in components:
            new_components.append(component[-8:])
        components = new_components
    while len(components[0]) > 2 and all(
        comp[0] == '0' for comp in components
    ):
        for i, component in enumerate(components):
            components[i] = component[1:]
    if len(components[0]) > 2:
        for i, component in enumerate(components):
            components[i] = component[:2]
    return Color(*map(gethex, components))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--loglevel', default='WARNING', help="Loglevel", action='store'
    )
    parser.add_argument('color', type=str, help='Color to parse')
    args = parser.parse_args()
    loglevel = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(loglevel, int):
        raise ValueError('Invalid log level: {}'.format(args.loglevel))
    logging.basicConfig(level=loglevel)
    print(parse_color(args.color))


if __name__ == '__main__':
    main()
