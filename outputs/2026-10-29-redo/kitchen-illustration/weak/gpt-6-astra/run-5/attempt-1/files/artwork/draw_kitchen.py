from PIL import Image, ImageDraw, ImageFilter
import random, math
from pathlib import Path

random.seed(11)
S=2
im=Image.new('RGB',(1400*S,1120*S),'#f3e5cb')
d=ImageDraw.Draw(im)
def xy(points): return [(int(x*S),int(y*S)) for x,y in points]
def box(b): return tuple(int(v*S) for v in b)
def rect(b,c,r=0,outline=None,w=2):
    d.rounded_rectangle(box(b),radius=r*S,fill=c,outline=outline,width=w*S)
def ellipse(b,c,outline=None,w=2): d.ellipse(box(b),fill=c,outline=outline,width=w*S)
def poly(p,c): d.polygon(xy(p),fill=c)
def line(p,c,w=3): d.line(xy(p),fill=c,width=w*S,joint='curve')
def arc(b,start,end,c,w=3): d.arc(box(b),start,end,fill=c,width=w*S)
cream='#f8edcf'; ink='#78553d'; wood='#bb7b48'; sage='#879b80'; darksage='#617962'

# Soft plaster, a terracotta floor, and golden sunlight.
rect((0,0,1400,785),'#f0dfbf')
rect((0,785,1400,1120),'#c48a64')
for y in [817,890,985,1103]: line([(0,y),(1400,y)],'#b47b58',3)
for row,(a,b) in enumerate([(785,817),(817,890),(890,985),(985,1120)]):
    for x in range(-300,1800,240): line([(x+row*65,a),(x+row*65-90,b)],'#b47b58',3)
poly([(275,380),(554,380),(1240,1120),(682,1120)],'#e8b87c')
poly([(316,398),(337,398),(929,1120),(886,1120)],'#cfa16e')
poly([(211,540),(546,540),(600,600),(251,600)],'#e4c99c')

# Arched window and the sleepy garden outside.
rect((122,123,585,580),'#bf9e72',150)
rect((135,136,572,570),cream,143)
rect((155,155,552,548),'#b7d0c4',131)
rect((155,300,552,548),'#b7d0c4')
ellipse((401,208,474,281),'#fff0b9')
poly([(155,461),(224,416),(297,435),(375,392),(464,425),(552,390),(552,548),(155,548)],'#91af91')
poly([(155,496),(223,467),(308,491),(412,450),(552,480),(552,548),(155,548)],'#74957d')
line([(351,161),(351,550)],cream,13)
line([(155,344),(552,344)],cream,13)
rect((128,546,584,567),'#e0c79c',5)
rect((113,566,599,585),'#b78e60',5)

# Linen curtains, gathered loosely at either side.
line([(99,131),(608,131)],ink,6)
ellipse((87,123,104,140),ink); ellipse((605,123,622,140),ink)
poly([(109,140),(203,140),(191,263),(164,394),(181,526),(101,526),(114,378)],'#fff3d7')
poly([(501,140),(593,140),(587,376),(607,526),(526,526),(545,394),(517,272)],'#fff3d7')
for x in [122,145,171]: line([(x,147),(x-3,272),(139+(x-145)*.3,394),(x-6,515)],'#e4cda9',2)
for x in [520,545,571]: line([(x,147),(x+7,272),(557+(x-545)*.3,394),(x+13,515)],'#e4cda9',2)
line([(106,394),(167,394)],'#c89c65',7); line([(541,394),(591,394)],'#c89c65',7)

# The backsplash has softly imperfect grout lines.
rect((648,382,1350,586),'#efe6ce')
for y in range(389,586,48): line([(648,y),(1350,y)],'#d9cbb0',2)
for row in range(4):
    for x in range(650+row%2*47,1370,94): line([(x,389+row*48),(x,437+row*48)],'#d9cbb0',2)

# Shelf, stacked ceramics, jars, and trailing leaves.
rect((675,270,1315,285),wood,3)
poly([(705,285),(735,285),(705,327)],'#a46942'); poly([(1258,285),(1288,285),(1288,327)],'#a46942')
for x,h,c in [(703,63,'#c58b60'),(766,79,'#b5b99a'),(831,57,'#d6b775')]:
    rect((x,270-h,x+44,269),c,10); rect((x-2,266-h,x+46,277-h),'#896545',4)
    rect((x+9,240-h/2,x+35,257-h/2),'#f5e8c9',3)
for y in [259,251,243]:
    arc((922,y-12,1003,y+10),0,180,'#7f9691',7)
    line([(926,y),(998,y)],'#e8e4cf',5)
rect((1040,218,1088,267),'#eee4ca',6); arc((1070,223,1109,255),270,90,'#eee4ca',7)
rect((1173,222,1237,270),'#bc7655',8)
for pts in [[(1203,226),(1200,188),(1165,169)],[(1204,230),(1230,185),(1260,177)],[(1207,227),(1226,249),(1282,290),(1276,363)],[(1201,226),(1171,197),(1148,210)]]:
    line(pts,'#657e50',4)
for x,y,flip in [(1170,171,0),(1183,188,1),(1212,199,0),(1240,182,1),(1260,282,0),(1278,302,1),(1279,329,0),(1276,350,1),(1154,204,0)]:
    ellipse((x-19 if flip else x,y-9,x+3 if flip else x+22,y+9),'#758c59')

# Lower cabinets, oak worktop and brass hardware.
rect((91,615,1349,829),'#526c59',3)
rect((100,612,1337,808),sage)
for x1,x2 in [(109,290),(304,485),(499,680),(1096,1324)]:
    rect((x1,633,x2,792),'#728b72',3)
    rect((x1+9,642,x2-9,781),'#94a587',3)
    ellipse((x2-28,698,x2-17,709),'#cfa35e')
for y in [629,684,739]:
    rect((697,y,860,y+47),'#95a688',3)
    rect((753,y+18,805,y+24),'#d8ad68',3)
rect((78,586,1360,610),'#c18b54',5)
rect((78,607,1360,618),'#9c673e',3)
line([(91,592),(1347,592)],'#dcac72',3)

# Sink, tap, soap, and a striped cotton towel.
ellipse((274,578,492,603),'#906e4e')
ellipse((287,582,479,599),'#b5b6a1')
arc((390,493,450,556),180,360,'#9b8459',9)
line([(394,524),(394,579)],'#9b8459',9)
line([(447,520),(447,540)],'#9b8459',8)
rect((522,553,549,587),'#dfc791',5); line([(535,554),(535,542),(549,542)],ink,4)
poly([(546,607),(626,607),(630,724),(615,734),(547,727)],'#f4e9cc')
for x in [560,567,603,610]: line([(x,611),(x+2,726)],'#ba775d',3)

# A cream stove with a kettle catching the light.
rect((882,600,1078,813),'#efe2bf',8)
rect((881,593,1078,606),'#62665a',3)
for x in [913,968,1025]: ellipse((x,621,x+15,636),'#877a60')
rect((898,650,1063,794),'#bcb498',8)
rect((909,672,1052,782),'#49524b',13)
rect((918,682,1043,772),'#60695d',9)
line([(926,694),(944,694),(1027,758)],'#7b8270',5)
rect((922,652,1041,660),'#7e725d',4)
arc((955,506,1028,583),180,360,'#555f52',9)
ellipse((947,534,1037,594),'#be8058',ink,2)
poly([(955,558),(931,540),(917,542),(931,572),(956,583)],'#be8058')
rect((965,533,1021,540),'#e0a573',4); ellipse((988,523,1000,535),ink)
arc((911,478,935,521),80,260,'#f8f0d9',4)
arc((920,452,941,491),250,430,'#f8f0d9',4)

# Wooden boards, a little vase of chamomile, and hanging utensils.
rect((1150,483,1246,585),'#a76f43',22); rect((1182,454,1211,504),'#a76f43',10)
ellipse((1191,462,1201,473),'#ead4ab')
rect((1120,516,1199,587),'#c7985f',19)
line([(1102,343),(1284,343)],ink,5)
for x in [1133,1194,1252]:
    arc((x-5,335,x+7,357),0,280,'#a78551',3)
    line([(x,356),(x,420)],'#9f7547',5)
ellipse((1122,408,1144,446),'#b98b54')
rect((1182,411,1206,442),'#9f7547',6)
for x in [1189,1199]: line([(x,416),(x,434)],'#eddfbf',2)
arc((1237,408,1267,452),0,360,'#8d8b73',3)
for x in [1244,1252,1260]: arc((x-7,408,x+7,452),0,360,'#8d8b73',2)
rect((1275,541,1311,586),'#ddd3ad',10)
for x,y in [(1261,504),(1293,486),(1320,510),(1296,523)]:
    line([(1292,548),(x,y)],'#7e8d59',3)
    for a in range(0,360,60):
        xx=x+math.cos(math.radians(a))*7; yy=y+math.sin(math.radians(a))*7
        ellipse((xx-5,yy-5,xx+5,yy+5),'#fff4d7')
    ellipse((x-4,y-4,x+4,y+4),'#d3a044')

# A pendant lamp pools warm light above the breakfast table.
line([(733,0),(733,120)],'#826747',4)
ellipse((714,113,753,145),'#9f774c')
poly([(711,128),(755,128),(810,192),(656,192)],'#9aab87')
ellipse((656,180,810,207),'#728869')
ellipse((669,185,797,201),'#fce6ad')
ellipse((723,185,744,205),'#fff0bc')

# Woven rug and a sleeping marmalade cat.
ellipse((758,890,1290,1058),'#a6664d')
ellipse((771,897,1277,1048),'#d6b58c')
for i in range(5): arc((786+i*12,907+i*6,1261-i*12,1038-i*6),0,360,'#c49870',2)
ellipse((958,938,1196,1001),'#b88e68')
ellipse((970,906,1180,991),'#c98b50')
ellipse((1005,916,1162,981),'#d99c5b')
ellipse((962,930,1037,987),'#d99c5b')
poly([(967,944),(967,915),(991,933)],'#d99c5b'); poly([(1006,932),(1031,917),(1033,949)],'#d99c5b')
poly([(972,935),(972,925),(983,934)],'#b67858')
arc((975,947,990,959),0,170,'#6d513c',2); arc((1005,947,1020,959),0,170,'#6d513c',2)
poly([(992,960),(1002,960),(997,965)],'#8f654b')
arc((1039,936,1185,991),335,535,'#b67840',17)
for x in [1051,1080,1109]: line([(x,912),(x+8,927)],'#b67840',6)

# Rounded farmhouse table, a chair, and breakfast for a slow morning.
line([(196,810),(161,1030)],'#825737',19); line([(351,810),(381,1030)],'#825737',19)
rect((144,722,393,840),'#a87748',30)
rect((160,738,376,815),'#d4aa70',23)
for x in [195,238,281,324]: line([(x,748),(x,810)],'#af814d',5)
poly([(338,881),(363,881),(330,1119),(308,1119)],'#895d3b')
poly([(676,881),(699,881),(748,1119),(725,1119)],'#895d3b')
ellipse((217,778,815,949),'#95623e')
rect((217,851,815,875),'#95623e')
ellipse((217,760,815,929),'#d3a16a')
ellipse((229,768,803,915),'#ddb37b')
for y in [801,835,871,897]:
    a=math.sqrt(max(0,1-((y-841)/74)**2))*270
    line([(516-a,y),(516+a,y+2)],'#c79a63',2)
poly([(570,777),(657,789),(643,914),(558,908)],'#f0e4c7')
for x in [583,594,624,635]: line([(x,790),(x-11,907)],'#b8896a',2)
ellipse((332,802,540,881),'#b78c5c')
ellipse((327,794,535,873),'#f7eccc')
ellipse((344,802,519,861),'#dfd5b5')
ellipse((353,808,510,857),'#f4e9cb')
# Two flaky croissants.
for dx,dy in [(0,0),(65,12)]:
    poly([(366+dx,830+dy),(373+dx,812+dy),(393+dx,803+dy),(417+dx,809+dy),(438+dx,831+dy),(423+dx,837+dy),(408+dx,826+dy),(390+dx,822+dy),(381+dx,840+dy)],'#be7b3c')
    poly([(371+dx,826+dy),(378+dx,813+dy),(394+dx,808+dy),(411+dx,814+dy),(430+dx,830+dy),(413+dx,822+dy),(389+dx,817+dy),(380+dx,834+dy)],'#e5b25f')
    for x,y in [(385,809),(399,811),(413,817)]: line([(x+dx,y+dy),(x-3+dx,y+11+dy)],'#b87939',2)
ellipse((577,818,683,857),'#d4c6a2')
ellipse((582,815,679,849),'#f7edce')
arc((642,775,686,818),265,455,'#6f8b78',9)
rect((592,776,651,827),'#7f9a83',14)
ellipse((592,765,651,788),'#a9b8a0')
ellipse((598,770,645,784),'#6e4832')
arc((609,720,625,762),75,265,'#fff3d8',4)
arc((624,701,640,740),250,440,'#fff3d8',4)
# A small jar of marmalade and a butter knife.
rect((699,790,741,828),'#c39347',7); rect((697,785,743,797),'#f0ddb2',4)
rect((706,803,735,820),'#f3dfb8',3)
line([(548,843),(568,867)],'#9b8c6a',5); line([(568,867),(580,882)],'#7b593b',7)

# Fine paper grain keeps the illustration tactile.
im=im.resize((1400,1120),Image.Resampling.LANCZOS)
noise=Image.effect_noise(im.size,5).convert('RGB')
im=Image.blend(im,noise,.035)
out=Path(__file__).parent/'cozy-kitchen-morning.png'
im.save(out)
print(out)
