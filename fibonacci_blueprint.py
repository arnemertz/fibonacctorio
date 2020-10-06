from factorio.blueprints import *
import json
import math

true_tile="hazard-concrete-right"
false_tile="concrete"

def icon(index,digit):
    return {"signal": {"type": "virtual", "name": "signal-%d" % digit}, "index": index+1}

def inDistance(x, y, radius):
    return x*x + y*y <= radius*radius

def fatfilled( x, y, radius ):
    return inDistance(x, y, radius) and not(
        inDistance(x + 1, y, radius) and
        inDistance(x - 1, y, radius) and
        inDistance(x, y + 1, radius) and
        inDistance(x, y - 1, radius) and
        inDistance(x + 1, y + 1, radius) and
        inDistance(x + 1, y - 1, radius) and
        inDistance(x - 1, y - 1, radius) and
        inDistance(x - 1, y + 1, radius)
    )

def tiles(radius):
    tiles = []
    width_r = float(radius)
    maxblocks_x = math.ceil(width_r - .5) * 2 + 1

    y = 0.5
    while y <= maxblocks_x / 2 - 1:
        x = 0.5
        while x <= maxblocks_x / 2 - 1:
            filled = fatfilled(x, y, radius) and not(fatfilled(x + 1, y, radius) and fatfilled(x, y + 1, radius))
            if filled:
                tiles.append({"position": {"x": int(x-0.5), "y": int(y-0.5)}, "name": true_tile if filled else false_tile})
            x += 1
        y += 1
    return tiles


def blueprint(radius):
    assert(radius <= 9999)

    json_object={"blueprint":{"icons":[],"tiles":[],"item":"blueprint","version":281474976710656},"version_byte":"0"}
    blueprint = json_object["blueprint"]

    digits=[int(d) for d in str(radius)]
    blueprint["icons"] = [ icon(index, digit) for index,digit in enumerate(digits) ]

    blueprint["tiles"] = tiles(radius)

    return json_object

book=BlueprintBook.from_json_file('init_blueprintbook.json')
bp = Blueprint(blueprint(5), "0")
bp.to_exchange_file('output/blueprint5.txt')
book.to_exchange_file('output/blueprintbook.txt')
