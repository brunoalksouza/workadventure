#!/usr/bin/env python3
"""Generate improved WorkAdventure office map with proper visuals and furniture."""
import json

W = 40
H = 30

# ── Tile IDs ──
FLOOR = 201;  RFLOOR = 223  # tileset1
# Walls (tileset5, firstgid=1)
WTL=49; WTR=50; WBL=59; WBR=60; WH=58; WV=45
# Special (firstgid=443)
COLL=443; STRT=444; JITS=454
# Furniture (tileset1)
DTL=296; DTR=297; DBL=307; DBR=308; CHAIR=261; PLANT=282
# Meeting table (tileset1-repositioning)
MTL=325; MTR=326; MTE=340
FLIP_H=0x80000000

def L(): return [0]*(W*H)
def P(l,x,y,t):
    if 0<=x<W and 0<=y<H: l[y*W+x]=t
def F(l,x1,y1,x2,y2,t):
    for y in range(y1,y2+1):
        for x in range(x1,x2+1): P(l,x,y,t)

def draw_walls(c,d,x1,y1,x2,y2):
    for x in range(x1,x2+1):
        P(c,x,y1,COLL); P(c,x,y2,COLL)
        P(d,x,y1,WH);   P(d,x,y2,WH)
    for y in range(y1,y2+1):
        P(c,x1,y,COLL); P(c,x2,y,COLL)
        P(d,x1,y,WV);   P(d,x2,y,WV)
    P(d,x1,y1,WTL); P(d,x2,y1,WTR)
    P(d,x1,y2,WBL); P(d,x2,y2,WBR)

def door(c,d,x,y):
    P(c,x,y,0); P(d,x,y,0)

def desk(f,x,y):
    P(f,x,y,DTL); P(f,x+1,y,DTR)
    P(f,x,y+1,DBL); P(f,x+1,y+1,DBR)

def mtable(f,x,y,w,h):
    for j in range(h):
        P(f,x,y+j,MTL)
        for i in range(1,w-1): P(f,x+i,y+j,MTE)
        P(f,x+w-1,y+j,MTR)

def jlayer(room,name,val,lid,trig=None):
    x1,y1,x2,y2=room; d=L()
    F(d,x1+1,y1+1,x2-1,y2-1,JITS)
    p=[{"name":"jitsiRoom","type":"string","value":val}]
    if trig: p.append({"name":"jitsiTrigger","type":"string","value":trig})
    return {"data":d,"height":H,"id":lid,"name":name,"opacity":1,
            "properties":p,"type":"tilelayer","visible":True,"width":W,"x":0,"y":0}

def tl(data,lid,name):
    return {"data":data,"height":H,"id":lid,"name":name,"opacity":1,
            "type":"tilelayer","visible":True,"width":W,"x":0,"y":0}

# Room definitions
ROOMS = {
    "lideranca":   (1,1,17,8),
    "individual2": (30,1,38,5),
    "individual":  (30,7,38,11),
    "edicao":      (1,12,10,19),
    "copy":        (12,12,21,19),
    "trafego":     (24,12,33,19),
    "saguao":      (1,21,17,28),
    "reuniao":     (19,21,38,28),
}

# ── Create layers ──
start=L(); coll=L(); floor=L(); wdec=L(); furn=L()

# Floor
F(floor,0,0,W-1,H-1,FLOOR)
for _,(x1,y1,x2,y2) in ROOMS.items():
    F(floor,x1+1,y1+1,x2-1,y2-1,RFLOOR)

# Walls (outer + rooms)
draw_walls(coll,wdec,0,0,W-1,H-1)
for _,(x1,y1,x2,y2) in ROOMS.items():
    draw_walls(coll,wdec,x1,y1,x2,y2)

# Doors
for x,y in [(9,8),(10,8)]: door(coll,wdec,x,y)
for x,y in [(30,3),(30,4)]: door(coll,wdec,x,y)
for x,y in [(30,9),(30,10)]: door(coll,wdec,x,y)
for x,y in [(10,15),(10,16)]: door(coll,wdec,x,y)
for x,y in [(12,15),(12,16)]: door(coll,wdec,x,y)
for x,y in [(24,15),(24,16)]: door(coll,wdec,x,y)
for x,y in [(9,21),(10,21)]: door(coll,wdec,x,y)
for x,y in [(19,24),(19,25)]: door(coll,wdec,x,y)

# Start
F(start,8,24,10,25,STRT)

# ── Furniture ──
# LIDERANÇA
desk(furn,5,3); desk(furn,8,3); desk(furn,11,3)
for cx in [5,6,8,9,11,12]: P(furn,cx,5,CHAIR)
for px,py in [(2,2),(16,2),(2,7),(16,7)]: P(furn,px,py,PLANT)

# INDIVIDUAL 2 & INDIVIDUAL
desk(furn,33,2); P(furn,33,4,CHAIR); P(furn,34,4,CHAIR); P(furn,37,2,PLANT)
desk(furn,33,8); P(furn,33,10,CHAIR); P(furn,34,10,CHAIR); P(furn,37,8,PLANT)

# EDIÇÃO
desk(furn,3,14); desk(furn,6,14)
for cx in [3,4,6,7]: P(furn,cx,16,CHAIR)
P(furn,2,13,PLANT); P(furn,9,18,PLANT)

# COPY
desk(furn,14,14); desk(furn,17,14)
for cx in [14,15,17,18]: P(furn,cx,16,CHAIR)
P(furn,13,13,PLANT); P(furn,20,18,PLANT)

# TRÁFEGO
desk(furn,26,14); desk(furn,29,14)
for cx in [26,27,29,30]: P(furn,cx,16,CHAIR)
P(furn,25,13,PLANT); P(furn,32,18,PLANT)

# SAGUÃO - plants
for px,py in [(2,22),(16,22),(2,27),(16,27),(7,22),(11,22)]:
    P(furn,px,py,PLANT)

# SALA DE REUNIÃO - meeting table + chairs + plants
mtable(furn,26,23,6,3)
for cy in [23,24,25]:
    P(furn,25,cy,CHAIR|FLIP_H)
    P(furn,32,cy,CHAIR)
for cx in [27,28,29,30]:
    P(furn,cx,26,CHAIR)
for px,py in [(20,22),(37,22),(20,27),(37,27)]:
    P(furn,px,py,PLANT)

# ── Jitsi layers ──
jitsis = [
    jlayer(ROOMS["lideranca"],"jitsiLideranca","Lideranca",10,"onaction"),
    jlayer(ROOMS["edicao"],"jitsiEdicao","Edicao",11,"onaction"),
    jlayer(ROOMS["copy"],"jitsiCopy","CopyTeam",12,"onaction"),
    jlayer(ROOMS["trafego"],"jitsiTrafego","Trafego",13,"onaction"),
    jlayer(ROOMS["reuniao"],"jitsiSalaReuniao","SalaDeReuniao",14),
]

# ══ CRITICAL: Layer order ══
# collision/jitsi BELOW floor → hides BLOCK/JITSI text
# floor BELOW walls → walls render on top
# furniture on top of everything
tilemap = {
    "compressionlevel":-1,"height":H,"infinite":False,
    "layers":[
        tl(start,1,"start"),
        tl(coll,2,"collisions"),
        *jitsis,
        tl(floor,20,"floor"),
        tl(wdec,21,"walls"),
        tl(furn,22,"furniture"),
        {"draworder":"topdown","id":30,"name":"floorLayer",
         "objects":[{"class":"area","height":192,"id":1,"name":"lobby",
                     "properties":[{"name":"chatName","type":"string","value":"Saguao"}],
                     "rotation":0,"visible":True,"width":480,"x":64,"y":704}],
         "opacity":1,"type":"objectgroup","visible":True,"x":0,"y":0},
    ],
    "nextlayerid":31,"nextobjectid":2,
    "orientation":"orthogonal",
    "properties":[
        {"name":"mapName","type":"string","value":"Escritorio Virtual"},
        {"name":"mapDescription","type":"string","value":"Escritorio virtual com salas de equipe e sala de reuniao."},
    ],
    "renderorder":"right-down","tiledversion":"1.9.2","tileheight":32,
    "tilesets":[
        {"columns":10,"firstgid":1,"image":"../assets/tileset5_export.png",
         "imageheight":320,"imagewidth":320,"margin":0,"name":"tileset5_export",
         "spacing":0,"tilecount":100,"tileheight":32,"tilewidth":32},
        {"columns":10,"firstgid":101,"image":"../assets/tileset6_export.png",
         "imageheight":320,"imagewidth":320,"margin":0,"name":"tileset6_export",
         "spacing":0,"tilecount":100,"tileheight":32,"tilewidth":32},
        {"columns":11,"firstgid":201,"image":"../assets/tileset1.png",
         "imageheight":352,"imagewidth":352,"margin":0,"name":"tileset1",
         "spacing":0,"tilecount":121,"tileheight":32,"tilewidth":32},
        {"columns":11,"firstgid":322,"image":"../assets/tileset1-repositioning.png",
         "imageheight":352,"imagewidth":352,"margin":0,"name":"tileset1-repositioning",
         "spacing":0,"tilecount":121,"tileheight":32,"tilewidth":32},
        {"columns":6,"firstgid":443,"image":"../assets/Special_Zones.png",
         "imageheight":64,"imagewidth":192,"margin":0,"name":"Special_Zones",
         "spacing":0,"tilecount":12,"tileheight":32,
         "tiles":[{"id":0,"properties":[{"name":"collides","type":"bool","value":True}]}],
         "tilewidth":32},
    ],
    "tilewidth":32,"type":"map","version":"1.9","width":W,
}

with open("/Users/brunoalkmin/Documents/Programing/Workadventure/maps/office/map.json","w") as f:
    json.dump(tilemap,f,indent=1)
print("Map generated successfully!")
