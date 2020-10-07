from factorio.blueprints import *
import json
import math

true_tile="hazard-concrete-right"
false_tile="concrete"

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

def filled(x, y, radius):
    return fatfilled(x, y, radius) and not(fatfilled(x + 1, y, radius) and fatfilled(x, y + 1, radius))

def tiles(radius):
    tiles = []
    width_r = float(radius)
    maxblocks_x = math.ceil(width_r - .5) * 2 + 1

    y = 0.5
    while y <= maxblocks_x / 2 - 1:
        x = 0.5
        while x <= maxblocks_x / 2 - 1:
            if filled(x, y, radius):
                tiles.append({"position": {"x": int(x-0.5), "y": int(y-0.5)}, "name": true_tile})
            elif filled(x+1, y, radius) or filled(x+2, y, radius) or filled(x, y+1, radius) or filled(x, y+2, radius):
                tiles.append({"position": {"x": int(x-0.5), "y": int(y-0.5)}, "name": false_tile})
            x += 1
        y += 1
    return tiles

def icon(index,digit):
    return {"signal": {"type": "virtual", "name": "signal-%d" % digit}, "index": index+1}

def icons(radius):
    assert(radius <= 9999)
    digits=[int(d) for d in str(radius)]
    return [ icon(index, digit) for index,digit in enumerate(digits) ]

def fib(N):
    return fib(N-1) + fib(N-2) if N>2 else 1

def blueprint(N):
    radius = fib(N)

    json_object={"blueprint":{"icons":[],"tiles":[],"item":"blueprint","version":281474976710656}}
    blueprint = json_object["blueprint"]

    blueprint["icons"] = icons(radius)
    blueprint["tiles"] = tiles(radius)
    blueprint["label"] = "fib(%d)" % N

    return Blueprint(json_object)



book=BlueprintBook.from_exchange_file('init_blueprintbook.txt')
for N in range(6,7):
    bp = blueprint(N)
    book.add_blueprint(bp)

book.replace_indexes()
book.to_exchange_file('output/blueprintbook.txt')
book.to_json_file('output/blueprintbook.json')
