#!/usr/bin/env python3
"""Generate WorkAdventure office map based on the PDF layout."""
import json

W = 40  # map width in tiles
H = 30  # map height in tiles

# Tile IDs (from existing tilesets)
FLOOR = 201       # standard corridor floor (tileset1)
ROOM_FLOOR = 223  # room floor - different shade
WALL = 443        # collision wall tile (Special_Zones, has collides=true)
START = 444       # start position marker
JITSI = 454       # jitsi zone marker

# Wall decoration tiles (tileset5_export, firstgid=1)
CORNER_TL = 49
CORNER_TR = 50
CORNER_BL = 59
CORNER_BR = 60
WALL_H_TOP = 58   # horizontal wall top
WALL_V = 45       # vertical wall
WALL_H_MID = 63   # horizontal wall middle
WALL_H_BOT = 73   # horizontal wall bottom
WALL_H_TOP2 = 57  # horizontal wall top variant


def make_layer():
    return [0] * (W * H)


def idx(x, y):
    return y * W + x


def set_tile(layer, x, y, tile_id):
    if 0 <= x < W and 0 <= y < H:
        layer[idx(x, y)] = tile_id


def fill_rect(layer, x1, y1, x2, y2, tile_id):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            set_tile(layer, x, y, tile_id)


def draw_wall_border(coll, decor, x1, y1, x2, y2):
    """Draw collision walls + decorative walls around a rectangle."""
    # Collision layer
    for x in range(x1, x2 + 1):
        set_tile(coll, x, y1, WALL)
        set_tile(coll, x, y2, WALL)
    for y in range(y1, y2 + 1):
        set_tile(coll, x1, y, WALL)
        set_tile(coll, x2, y, WALL)

    # Decorative wall layer
    # Corners
    set_tile(decor, x1, y1, CORNER_TL)
    set_tile(decor, x2, y1, CORNER_TR)
    set_tile(decor, x1, y2, CORNER_BL)
    set_tile(decor, x2, y2, CORNER_BR)
    # Top/bottom horizontal walls
    for x in range(x1 + 1, x2):
        set_tile(decor, x, y1, WALL_H_TOP)
        set_tile(decor, x, y2, WALL_H_TOP)
    # Left/right vertical walls
    for y in range(y1 + 1, y2):
        set_tile(decor, x1, y, WALL_V)
        set_tile(decor, x2, y, WALL_V)


def add_door(coll, decor, x, y):
    """Remove wall at position to create a door."""
    set_tile(coll, x, y, 0)
    set_tile(decor, x, y, 0)


def make_jitsi_layer(room_rect, room_name, jitsi_value, layer_id, trigger=None):
    """Create a Jitsi layer for a specific room area."""
    x1, y1, x2, y2 = room_rect
    data = make_layer()
    # Fill interior with jitsi tile
    fill_rect(data, x1 + 1, y1 + 1, x2 - 1, y2 - 1, JITSI)

    props = [{"name": "jitsiRoom", "type": "string", "value": jitsi_value}]
    if trigger:
        props.append({"name": "jitsiTrigger", "type": "string", "value": trigger})

    return {
        "data": data,
        "height": H,
        "id": layer_id,
        "name": room_name,
        "opacity": 1,
        "properties": props,
        "type": "tilelayer",
        "visible": True,
        "width": W,
        "x": 0,
        "y": 0,
    }


# ── Room definitions (x1, y1, x2, y2) ──
ROOMS = {
    "lideranca":   (1,  1, 17,  8),   # LIDERANÇA - top left, large
    "individual2": (30, 1, 38,  5),   # INDIVIDUAL 2 - top right
    "individual":  (30, 7, 38, 11),   # INDIVIDUAL - right side
    "edicao":      (1, 12, 10, 19),   # EDIÇÃO - middle left
    "copy":        (12, 12, 21, 19),  # COPY - middle center
    "trafego":     (24, 12, 33, 19),  # TRÁFEGO - middle right
    "saguao":      (1, 21, 17, 28),   # Saguão (lobby) - bottom left
    "reuniao":     (19, 21, 38, 28),  # Sala de reunião - bottom right
}

# ── Build layers ──
floor = make_layer()
collisions = make_layer()
walls_decor = make_layer()
start = make_layer()

# 1. Fill entire map with corridor floor
fill_rect(floor, 0, 0, W - 1, H - 1, FLOOR)

# 2. Fill room interiors with room floor
for name, (x1, y1, x2, y2) in ROOMS.items():
    fill_rect(floor, x1 + 1, y1 + 1, x2 - 1, y2 - 1, ROOM_FLOOR)

# 3. Draw outer border walls
draw_wall_border(collisions, walls_decor, 0, 0, W - 1, H - 1)

# 4. Draw room walls
for name, (x1, y1, x2, y2) in ROOMS.items():
    draw_wall_border(collisions, walls_decor, x1, y1, x2, y2)

# 5. Add doors (2-tile wide openings)
# Liderança - door at bottom center
add_door(collisions, walls_decor, 9, 8)
add_door(collisions, walls_decor, 10, 8)

# Individual 2 - door at left
add_door(collisions, walls_decor, 30, 3)
add_door(collisions, walls_decor, 30, 4)

# Individual - door at left
add_door(collisions, walls_decor, 30, 9)
add_door(collisions, walls_decor, 30, 10)

# Edição - door at right side
add_door(collisions, walls_decor, 10, 15)
add_door(collisions, walls_decor, 10, 16)

# Copy - door at left side
add_door(collisions, walls_decor, 12, 15)
add_door(collisions, walls_decor, 12, 16)

# Tráfego - door at left side
add_door(collisions, walls_decor, 24, 15)
add_door(collisions, walls_decor, 24, 16)

# Saguão - door at top
add_door(collisions, walls_decor, 9, 21)
add_door(collisions, walls_decor, 10, 21)

# Sala de reunião - door at left side
add_door(collisions, walls_decor, 19, 24)
add_door(collisions, walls_decor, 19, 25)

# 6. Also open shared walls between rooms and outer border
# Where rooms touch the outer border, we don't need double walls.
# The outer border walls at room positions are already handled.

# Fix: Remove corridor floor tiles under walls (walls should not have floor showing)
# Actually walls render on top, so this is fine.

# 7. Set start position (in the Saguão/lobby)
fill_rect(start, 8, 24, 10, 25, START)

# ── Build Jitsi layers ──
jitsi_lideranca = make_jitsi_layer(
    ROOMS["lideranca"], "jitsiLideranca", "Lideranca", 10, trigger="onaction"
)
jitsi_edicao = make_jitsi_layer(
    ROOMS["edicao"], "jitsiEdicao", "Edicao", 11, trigger="onaction"
)
jitsi_copy = make_jitsi_layer(
    ROOMS["copy"], "jitsiCopy", "CopyTeam", 12, trigger="onaction"
)
jitsi_trafego = make_jitsi_layer(
    ROOMS["trafego"], "jitsiTrafego", "Trafego", 13, trigger="onaction"
)
jitsi_reuniao = make_jitsi_layer(
    ROOMS["reuniao"], "jitsiSalaReuniao", "SalaDeReuniao", 14
)

# ── Assemble the map ──
tilemap = {
    "compressionlevel": -1,
    "height": H,
    "infinite": False,
    "layers": [
        {
            "data": start,
            "height": H,
            "id": 1,
            "name": "start",
            "opacity": 1,
            "type": "tilelayer",
            "visible": True,
            "width": W,
            "x": 0,
            "y": 0,
        },
        {
            "data": floor,
            "height": H,
            "id": 2,
            "name": "floor",
            "opacity": 1,
            "type": "tilelayer",
            "visible": True,
            "width": W,
            "x": 0,
            "y": 0,
        },
        {
            "data": walls_decor,
            "height": H,
            "id": 3,
            "name": "walls",
            "opacity": 1,
            "type": "tilelayer",
            "visible": True,
            "width": W,
            "x": 0,
            "y": 0,
        },
        {
            "data": collisions,
            "height": H,
            "id": 4,
            "name": "collisions",
            "opacity": 1,
            "type": "tilelayer",
            "visible": True,
            "width": W,
            "x": 0,
            "y": 0,
        },
        jitsi_lideranca,
        jitsi_edicao,
        jitsi_copy,
        jitsi_trafego,
        jitsi_reuniao,
        # floorLayer (required objectgroup for WorkAdventure)
        {
            "draworder": "topdown",
            "id": 20,
            "name": "floorLayer",
            "objects": [
                {
                    "class": "area",
                    "height": (ROOMS["saguao"][3] - ROOMS["saguao"][1] - 1) * 32,
                    "id": 1,
                    "name": "lobby",
                    "properties": [
                        {"name": "chatName", "type": "string", "value": "Saguao"}
                    ],
                    "rotation": 0,
                    "visible": True,
                    "width": (ROOMS["saguao"][2] - ROOMS["saguao"][0] - 1) * 32,
                    "x": (ROOMS["saguao"][0] + 1) * 32,
                    "y": (ROOMS["saguao"][1] + 1) * 32,
                },
            ],
            "opacity": 1,
            "type": "objectgroup",
            "visible": True,
            "x": 0,
            "y": 0,
        },
    ],
    "nextlayerid": 21,
    "nextobjectid": 2,
    "orientation": "orthogonal",
    "properties": [
        {
            "name": "mapName",
            "type": "string",
            "value": "Escritorio Virtual",
        },
        {
            "name": "mapDescription",
            "type": "string",
            "value": "Escritorio virtual com salas de Lideranca, Edicao, Copy, Trafego, Individual e Sala de Reuniao.",
        },
    ],
    "renderorder": "right-down",
    "tiledversion": "1.9.2",
    "tileheight": 32,
    "tilesets": [
        {
            "columns": 10,
            "firstgid": 1,
            "image": "../assets/tileset5_export.png",
            "imageheight": 320,
            "imagewidth": 320,
            "margin": 0,
            "name": "tileset5_export",
            "spacing": 0,
            "tilecount": 100,
            "tileheight": 32,
            "tilewidth": 32,
        },
        {
            "columns": 10,
            "firstgid": 101,
            "image": "../assets/tileset6_export.png",
            "imageheight": 320,
            "imagewidth": 320,
            "margin": 0,
            "name": "tileset6_export",
            "spacing": 0,
            "tilecount": 100,
            "tileheight": 32,
            "tilewidth": 32,
        },
        {
            "columns": 11,
            "firstgid": 201,
            "image": "../assets/tileset1.png",
            "imageheight": 352,
            "imagewidth": 352,
            "margin": 0,
            "name": "tileset1",
            "spacing": 0,
            "tilecount": 121,
            "tileheight": 32,
            "tilewidth": 32,
        },
        {
            "columns": 11,
            "firstgid": 322,
            "image": "../assets/tileset1-repositioning.png",
            "imageheight": 352,
            "imagewidth": 352,
            "margin": 0,
            "name": "tileset1-repositioning",
            "spacing": 0,
            "tilecount": 121,
            "tileheight": 32,
            "tilewidth": 32,
        },
        {
            "columns": 6,
            "firstgid": 443,
            "image": "../assets/Special_Zones.png",
            "imageheight": 64,
            "imagewidth": 192,
            "margin": 0,
            "name": "Special_Zones",
            "spacing": 0,
            "tilecount": 12,
            "tileheight": 32,
            "tiles": [
                {
                    "id": 0,
                    "properties": [
                        {"name": "collides", "type": "bool", "value": True}
                    ],
                }
            ],
            "tilewidth": 32,
        },
    ],
    "tilewidth": 32,
    "type": "map",
    "version": "1.9",
    "width": W,
}

# Write the map
output_path = "/Users/brunoalkmin/Documents/Programing/Workadventure/maps/office/map.json"
with open(output_path, "w") as f:
    json.dump(tilemap, f, indent=1)

print(f"Map generated: {output_path}")
print(f"Size: {W}x{H} tiles ({W*32}x{H*32} pixels)")
print(f"Rooms: {', '.join(ROOMS.keys())}")
