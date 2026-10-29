from PIL import Image, ImageDraw, ImageFilter
import random, math

random.seed(8)
S = 2
W, H = 1440, 1080
im = Image.new('RGB', (W*S, H*S), '#f3e6cb')
d = ImageDraw.Draw(im)

def poly(pts, fill, outline=None, width=2):
    p = [(int(x*S), int(y*S)) for x,y in pts]
    d.polygon(p, fill=fill)
    if outline: d.line(p+[p[0]], fill=outline, width=width*S, joint='curve')
def line(pts, fill, width=2):
    d.line([(int(x*S), int(y*S)) for x,y in pts], fill=fill, width=max(1,int(width*S)), joint='curve')
def rect(box, fill, outline=None, width=2, radius=0):
    b = tuple(int(v*S) for v in box)
    if radius: d.rounded_rectangle(b, radius=int(radius*S), fill=fill, outline=outline, width=width*S)
    else: d.rectangle(b, fill=fill, outline=outline, width=width*S)
def ellipse(box, fill, outline=None, width=2):
    d.ellipse(tuple(int(v*S) for v in box), fill, outline, width=width*S)
def curve(pts, color, width=2):
    # Cubic Bezier, with any number of consecutive segments.
    out=[pts[0]]
    p0=pts[0]
    for i in range(1,len(pts),3):
        a,b,c=pts[i:i+3]
        for j in range(1,41):
            t=j/40; u=1-t
            out.append((u**3*p0[0]+3*u*u*t*a[0]+3*u*t*t*b[0]+t**3*c[0],u**3*p0[1]+3*u*u*t*a[1]+3*u*t*t*b[1]+t**3*c[1]))
        p0=c
    line(out,color,width)
def leaf(x,y,dx,dy,color):
    L=math.hypot(dx,dy); nx=-dy/L*7; ny=dx/L*7
    pts=[]
    for j in range(25):
        t=j/24; w=math.sin(math.pi*t)
        pts.append((x+dx*t+nx*w,y+dy*t+ny*w))
    for j in range(24,-1,-1):
        t=j/24; w=math.sin(math.pi*t)
        pts.append((x+dx*t-nx*w,y+dy*t-ny*w))
    poly(pts,color)

# Cream plaster, subtle warm variation.
for y in range(H):
    t=y/H
    line([(0,y),(W,y)],(int(247-17*t),int(235-23*t),int(211-26*t)),1)
rect((0,0,1440,39),'#dcc5a1')
rect((0,39,1440,52),'#fff1d5')
rect((0,53,1440,57),'#d7bf99')

# Backsplash tiles.
rect((0,519,1440,713),'#e8ddbd')
for y in range(520,713,64):
    line([(0,y),(1440,y)],'#d4c6a7',2)
    for x in range(-70 if (y//64)%2 else 0,1440,122):
        line([(x,y+2),(x,y+62)],'#d4c6a7',2)
line([(0,518),(1440,518)],'#d3bea0',4)

# Arched window and a tiny waking landscape.
rect((211,278,730,602),'#c4af8c',radius=6)
ellipse((211,75,730,474),'#c4af8c')
rect((226,277,714,592),'#fff4d8')
ellipse((226,90,714,477),'#fff4d8')
rect((246,284,695,570),'#c8dbcc')
ellipse((246,111,695,467),'#c8dbcc')
ellipse((552,210,646,304),'#fff0ad')
ellipse((540,198,657,315),'#f9e5a4')
ellipse((550,208,647,305),'#fff3bd')
poly([(247,427),(314,396),(380,418),(449,383),(510,410),(579,389),(695,415),(695,571),(247,571)],'#aebda3')
poly([(247,487),(309,449),(362,465),(428,438),(486,461),(549,445),(619,469),(695,448),(695,571),(247,571)],'#8fa68c')
rect((351,449,410,523),'#e8cfab')
poly([(342,451),(379,424),(421,451)],'#b98265')
rect((373,478,386,502),'#9b9c85')
rect((589,454,658,529),'#eddbb9')
poly([(580,456),(622,428),(669,456)],'#bd9271')
rect((610,481,624,502),'#9ea58d')
for x,y in [(281,487),(460,508),(676,496)]:
    line([(x,y+57),(x,y-58)],'#7f947e',6)
    for a,b,c,e in [(x-32,y-30,x+25,y+30),(x-26,y-65,x+21,y-7),(x-19,y-88,x+17,y-40)]: ellipse((a,b,c,e),'#91aa8d')
curve([(403,286),(411,277),(421,279),(427,286)],'#879c90',2)
curve([(427,286),(432,277),(441,277),(446,282)],'#879c90',2)
curve([(339,326),(347,320),(354,321),(359,327)],'#879c90',2)
curve([(359,327),(364,321),(371,320),(377,324)],'#879c90',2)
rect((460,114,478,578),'#fff3d2')
rect((243,361,697,379),'#fff3d2')
line([(479,135),(479,566)],'#c3b38c',2)
line([(251,380),(693,380)],'#c3b38c',2)
rect((215,573,729,597),'#f9e9c7',radius=3)
rect((198,594,748,610),'#bfa280',radius=4)
rect((195,588,751,601),'#fff0ce',radius=4)

# Soft linen curtains, gathered at the sides.
curve([(191,139),(342,70),(596,73),(766,139)],'#927758',7)
ellipse((179,128,197,146),'#927758')
ellipse((760,128,778,146),'#927758')
poly([(204,139),(311,121),(285,203),(269,302),(257,424),(230,529),(192,528),(209,394),(216,273)],'#eee2c1')
poly([(209,143),(247,134),(236,248),(231,357),(215,497),(196,521),(212,375)],'#fcf0d3')
curve([(269,145),(243,263),(263,386),(225,521)],'#d1c2a0',3)
curve([(291,137),(263,251),(277,346),(245,456)],'#d1c2a0',2)
poly([(665,124),(734,140),(724,266),(735,390),(759,530),(713,532),(687,420),(685,284)],'#eee2c1')
poly([(692,134),(713,137),(703,265),(714,396),(739,527),(722,529),(697,405)],'#fff2d5')
curve([(678,140),(695,253),(676,343),(715,500)],'#cfc1a1',3)

# Upper cupboard with warm wood and sage doors.
rect((972,107,1365,465),'#bda583',radius=5)
rect((960,94,1353,449),'#839079',radius=4)
rect((970,105,1146,438),'#9aa38b',outline='#6c7c67',width=2,radius=3)
rect((1158,105,1341,438),'#9aa38b',outline='#6c7c67',width=2,radius=3)
rect((988,124,1128,416),'#aab199',outline='#8a977f',radius=2)
rect((1176,124,1323,416),'#aab199',outline='#8a977f',radius=2)
rect((1120,265,1127,303),'#b6965b',radius=3)
rect((1179,265,1186,303),'#b6965b',radius=3)
rect((948,84,1365,101),'#b8bd9e',radius=3)
line([(976,111),(1139,111)],'#c4c8aa',2)
line([(1165,111),(1336,111)],'#c4c8aa',2)

# Open shelf, ceramics, little clock.
ellipse((64,178,168,282),'#b69972')
ellipse((71,185,161,275),'#fff1cf')
for i in range(12):
    a=i*math.pi/6
    line([(116+35*math.sin(a),230-35*math.cos(a)),(116+39*math.sin(a),230-39*math.cos(a))],'#aa9575',2)
line([(116,230),(116,204)],'#786951',3)
line([(116,230),(135,240)],'#786951',3)
ellipse((112,226,120,234),'#a37e50')
rect((28,396,164,411),'#af8057',radius=3)
rect((28,394,164,400),'#c89d70')
rect((40,345,75,394),'#c79970',radius=5)
rect((36,339,79,351),'#b07e54',radius=3)
rect((91,361,143,394),'#f5dfb3',radius=5)
ellipse((91,353,143,368),'#a8b39a')
ellipse((100,354,134,363),'#ced0ac')
line([(48,412),(48,435),(70,412)],'#a98159',5)

# Hanging brass rail and kitchen tools.
line([(1014,492),(1351,492)],'#ac8954',7)
ellipse((1004,484,1020,500),'#b69664')
ellipse((1344,484,1360,500),'#b69664')
for x in [1044,1104,1165,1246,1302]:
    curve([(x,486),(x-12,482),(x-11,504),(x,505)],'#8b7450',3)
line([(1044,503),(1044,563)],'#a88254',8)
ellipse((1031,552,1058,595),'#b99564')
line([(1104,503),(1104,568)],'#a88254',7)
rect((1091,559,1118,592),'#b99564',radius=8)
for x in [1099,1107]: line([(x,566),(x,585)],'#8c704a',2)
ellipse((1140,531,1194,603),'#897d61',3)
ellipse((1147,538,1187,596),'#a69b7a',2)
line([(1166,503),(1166,534)],'#7d7159',9)
# Checked tea towel.
poly([(1217,506),(1270,506),(1283,642),(1212,642)],'#f5e8ca')
for y in range(520,640,19): line([(1216,y),(1271+(y-506)*.09,y)],'#c6a588',2)
for x in [1228,1247,1266]: line([(x,508),(x+2,639)],'#c6a588',2)
line([(1302,505),(1302,566)],'#a88254',6)
ellipse((1291,554,1313,592),None,'#8b7857',2)
line([(1302,556),(1302,591)],'#8b7857',2)

# Counter and lower cabinetry.
rect((0,719,1440,960),'#8e9b80')
rect((0,732,1440,753),'#728269')
for x0,x1 in [(19,222),(237,450),(467,691),(707,927),(942,1166),(1182,1420)]:
    rect((x0,768,x1,935),'#9daa8d',outline='#76866d',width=2,radius=3)
    rect((x0+15,785,x1-15,920),'#a7b298',outline='#8c9b7f',width=2,radius=2)
    rect(((x0+x1)/2-24,775,(x0+x1)/2+24,781),'#bc9d63',radius=3)
rect((0,939,1440,970),'#6d7a62')
rect((0,696,1440,724),'#a77c54')
rect((0,688,1440,703),'#d6ad78')
line([(0,691),(1440,691)],'#ebc58f',3)
for i in range(18):
    x=random.randrange(0,1440); y=random.randrange(705,719)
    line([(x,y),(min(x+random.randrange(40,200),1440),y+1)],'#b78d60',1)

# Sun falling through the window, across cupboards and floor.
light=Image.new('RGBA',im.size,(0,0,0,0)); ld=ImageDraw.Draw(light)
for pts,alpha in [([(292,380),(448,380),(840,968),(548,968)],24), ([(483,380),(668,380),(1339,1080),(984,1080)],30)]:
    ld.polygon([(int(x*S),int(y*S)) for x,y in pts],fill=(255,235,165,alpha))
im=Image.alpha_composite(im.convert('RGBA'),light).convert('RGB'); d=ImageDraw.Draw(im)

# Sink and curved brass tap.
ellipse((351,676,654,705),'#a88d67')
ellipse((373,680,634,701),'#c4c1a6')
ellipse((395,686,620,700),'#989f8b')
curve([(519,678),(519,620),(508,586),(477,587),(443,587),(443,610),(443,632)],'#866f48',12)
curve([(520,675),(520,622),(507,590),(479,591),(449,591),(449,612),(449,632)],'#ceb16b',7)
ellipse((434,626,455,634),'#bc9d62')
line([(540,673),(540,645),(560,640)],'#b4965c',7)

# Herbs in the sunny window.
poly([(619,550),(672,550),(665,587),(626,587)],'#bb7958')
ellipse((617,544,674,556),'#cc8d65')
ellipse((623,548,668,553),'#856347')
for x,y,dx,dy in [(645,549,-12,-68),(646,548,23,-62),(647,549,1,-83),(644,540,-30,-37),(649,538,36,-35)]:
    line([(x,y),(x+dx,y+dy)],'#768557',3)
    for t in [.4,.7,1.0]:
        bx=x+dx*t; by=y+dy*t
        leaf(bx,by,-17,-13,'#879b64'); leaf(bx,by,18,-13,'#9ba96e')

# Bread board and honey jar, left of the sink.
rect((53,654,278,683),'#b68858',outline='#9d754c',radius=10)
rect((124,642,159,668),'#b68858',radius=8)
ellipse((135,649,147,657),'#8f6c47')
ellipse((70,612,240,673),'#b67a43')
ellipse((74,606,239,663),'#d8a45e')
ellipse((84,607,224,644),'#e4b675')
for x in [111,148,184]: curve([(x,613),(x-17,621),(x-10,635),(x-20,642)],'#f4d297',7)
rect((272,635,314,685),'#c9a05c',radius=8)
rect((275,647,311,674),'#eddfac',radius=3)
rect((268,630,318,641),'#b08b55',radius=4)

# Enamel kettle and small stove.
rect((831,670,1046,689),'#ede4ca',radius=5)
ellipse((853,674,931,685),'#646a58')
ellipse((955,674,1027,685),'#646a58')
ellipse((872,675,971,690),'#6b765e')
curve([(880,613),(872,542),(968,542),(963,613)],'#626b56',10)
curve([(883,607),(877,553),(962,551),(960,609)],'#c2af80',4)
poly([(875,619),(852,604),(835,600),(843,618),(864,643)],'#d8bb7d',outline='#a89260')
ellipse((863,589,980,682),'#ddc68c')
ellipse((869,588,975,617),'#eedba3')
ellipse((886,581,958,600),'#b5a06c')
ellipse((893,577,952,589),'#e4ce90')
rect((914,567,930,580),'#6f7357',radius=4)
curve([(846,584),(830,563),(854,554),(845,535)],'#f7edd3',3)

# Pitcher with a few wildflowers.
ellipse((1247,621,1300,673),None,'#d9ccaa',9)
poly([(1196,609),(1241,609),(1253,680),(1190,680)],'#eee2bd')
ellipse((1190,658,1253,689),'#eee2bd')
ellipse((1196,603,1242,617),'#d3c5a0')
for x,y in [(1178,556),(1210,540),(1243,551),(1253,577),(1195,579)]:
    curve([(1218,613),(1215,587),(x,y+17),(x,y)],'#899367',2)
    leaf((x+1218)/2,(y+613)/2,18,-13,'#9fa576')
    for k in range(5):
        a=k*math.pi*2/5
        ellipse((x+math.cos(a)*8-6,y+math.sin(a)*8-6,x+math.cos(a)*8+6,y+math.sin(a)*8+6),'#f8edca')
    ellipse((x-4,y-4,x+4,y+4),'#cfaa55')

# Terracotta floor and woven mat.
rect((0,970,1440,1080),'#bb9171')
for x in range(-300,1800,220): line([(x,970),(x-100,1080)],'#a98062',2)
line([(0,1041),(1440,1041)],'#a98062',2)
ellipse((137,949,733,1032),'#d3bc8b')
for k in range(8):
    ellipse((148+k*12,954+k*3,722-k*12,1025-k*3),None,'#bca476',1)

# Foreground breakfast table.
ellipse((758,844,1494,1148),'#947254')
ellipse((748,824,1500,1110),'#c39565')
ellipse((753,822,1496,1090),'#dfbb86')
ellipse((767,830,1487,1080),'#e3c28f')
for y,x0,x1 in [(868,906,1350),(914,805,1449),(991,788,1470),(1043,863,1400)]:
    curve([(x0,y),(x0+160,y-7),(x1-130,y+8),(x1,y+3)],'#d5ad78',2)
# Soft striped runner.
poly([(1149,839),(1304,853),(1215,1080),(1015,1080)],'#ece0bf')
for a in [0,9,24,33]: line([(1167+a,844+a*.08),(1053+a,1080)],'#b1b59b',3)

# Breakfast plate and croissant.
ellipse((1134,900,1382,1012),'#c19b6e')
ellipse((1127,890,1380,1003),'#fbefd0',outline='#d8cbaa',width=3)
ellipse((1150,903,1359,986),None,'#dcd1ad',2)
poly([(1177,954),(1178,932),(1198,912),(1230,902),(1265,906),(1298,919),(1328,940),(1335,962),(1311,969),(1283,950),(1257,939),(1229,940),(1205,957)],'#bc8047')
poly([(1182,948),(1193,928),(1214,914),(1243,909),(1269,915),(1292,929),(1312,945),(1328,961),(1309,961),(1286,944),(1261,933),(1232,933),(1210,944),(1195,955)],'#e4ac5e')
for pts in [[(1206,920),(1222,920),(1225,930),(1223,938)],[(1233,912),(1246,917),(1252,922),(1253,931)],[(1261,916),(1274,924),(1277,930),(1278,940)],[(1285,928),(1294,935),(1299,944),(1298,950)]]:
    curve(pts,'#f6cd82',5)

# Coffee, saucer and rising steam.
ellipse((851,951,1043,1012),'#c49d6e')
ellipse((846,941,1037,1003),'#f5e8c5',outline='#d8c7a1',width=2)
ellipse((873,952,1013,990),None,'#dfd0ac',2)
ellipse((975,893,1034,952),None,'#efe0b9',13)
ellipse((979,902,1021,941),None,'#bfa77b',2)
rect((885,895,985,953),'#eee0b9')
ellipse((885,923,985,980),'#eee0b9')
ellipse((885,875,985,913),'#fcf0cf')
ellipse((894,882,976,906),'#805c3c')
ellipse((901,884,972,902),'#9f7449')
curve([(914,894),(928,882),(939,902),(959,891)],'#ddbd83',3)
curve([(925,861),(904,844),(940,826),(925,803)],'#f8efda',4)
curve([(950,866),(974,845),(944,826),(962,803)],'#f8efda',3)

# A small resting cat on a wooden chair in the lower left.
curve([(99,1078),(57,877),(65,824),(171,815),(259,809),(310,880),(294,1077)],'#9d714d',18)
curve([(102,1069),(74,882),(85,843),(174,838),(254,835),(282,885),(273,1071)],'#d0a16e',10)
for x in [117,163,209,250]: line([(x,848),(x+14,982)],'#b98b5b',9)
ellipse((64,991,323,1081),'#ad7c51')
ellipse((72,981,318,1060),'#d7ad77')
ellipse((104,949,298,1038),'#c28e62')
ellipse((116,937,294,1028),'#d4a474')
ellipse((106,930,195,1010),'#d6a779')
poly([(111,954),(109,917),(141,938)],'#d6a779')
poly([(163,939),(191,919),(190,964)],'#d6a779')
poly([(117,940),(116,927),(130,940)],'#c48a70')
poly([(174,939),(185,929),(184,948)],'#c48a70')
curve([(121,966),(127,973),(133,973),(139,967)],'#785c47',2)
curve([(155,967),(161,973),(168,973),(173,966)],'#785c47',2)
poly([(143,978),(151,978),(147,982)],'#9e705b')
curve([(273,973),(321,991),(290,1034),(243,1017),(212,1005),(227,984),(252,999)],'#b78359',16)
curve([(240,949),(230,959),(230,969),(234,976)],'#bb875f',4)
curve([(261,954),(250,964),(252,973),(257,978)],'#bb875f',4)
line([(128,981),(101,977)],'#94745a',1)
line([(129,986),(102,987)],'#94745a',1)
line([(165,982),(191,977)],'#94745a',1)

# Fine paper grain, barely visible, binds the illustration together.
noise=Image.new('RGBA',im.size)
nd=ImageDraw.Draw(noise)
for _ in range(85000):
    x=random.randrange(W*S); y=random.randrange(H*S)
    nd.point((x,y),fill=(99,73,42,random.randrange(3,13)))
im=Image.alpha_composite(im.convert('RGBA'),noise).convert('RGB')
im.resize((W,H),Image.Resampling.LANCZOS).save('cozy-kitchen.png')
