from PIL import Image, ImageDraw, ImageFilter
import math, random
random.seed(14)
S=2; W,H=1200,900
im=Image.new('RGB',(W*S,H*S)); p=im.load()
for y in range(H*S):
    t=y/(H*S)
    for x in range(W*S):
        glow=max(0,1-math.hypot((x/S-700)/950,(y/S-290)/1000))
        p[x,y]=(int(237+13*glow-13*t),int(219+14*glow-17*t),int(184+13*glow-17*t))
d=ImageDraw.Draw(im)
def pts(v): return [(round(x*S),round(y*S)) for x,y in v]
def box(v): return tuple(round(x*S) for x in v)
def rect(v,fill,outline=None,width=2,r=0):
    if r: d.rounded_rectangle(box(v),r*S,fill,outline,width*S)
    else: d.rectangle(box(v),fill,outline,width*S)
def ellipse(v,fill,outline=None,width=2):d.ellipse(box(v),fill,outline,width*S)
def line(v,fill='#705841',width=2):d.line(pts(v),fill,width*S,joint='curve')
def poly(v,fill,outline=None,width=2):
    d.polygon(pts(v),fill)
    if outline: line(v+[v[0]],outline,width)
def arc(v,start,end,fill,width=2): d.arc(box(v),start,end,fill,width*S)
ink='#735b42'; cream='#f7eac9'; wood='#b87542'; darkwood='#8d5737'
# wall and quiet wallpaper details
for x in range(35,1200,54):
    for y in range(30,630,72):
        line([(x,y-3),(x,y+3)],'#d8c7a4',1)
        line([(x-3,y),(x+3,y)],'#d8c7a4',1)
rect((0,623,1200,635),'#bc996a')
# sunlit window surround
rect((425,95,930,594),'#d6b483',r=12)
rect((438,104,919,581),'#805e40',r=8)
rect((450,117,907,569),'#c9ddd5',r=3)
# glass gradient
for y in range(120,568):
    t=(y-120)/448
    line([(452,y),(905,y)],(int(194+36*t),int(217+15*t),int(212-14*t)),1)
ellipse((756,157,837,238),'#fff5cd')
# distant hills
poly([(452,421),(508,389),(562,404),(630,364),(712,392),(784,371),(849,402),(905,379),(905,568),(452,568)],'#b2bf96')
poly([(452,467),(527,433),(605,461),(706,418),(809,452),(905,426),(905,568),(452,568)],'#98aa83')
# garden trees
for x,y,sz in [(502,447,35),(853,432,40),(809,473,25),(565,470,24)]:
    line([(x,y),(x,y+65)],'#82936e',4)
    ellipse((x-sz,y-sz*1.4,x+sz,y+sz*.7),'#91a37c')
# sun rays in glass
poly([(808,124),(867,124),(531,567),(463,567)],'#e7e6c7')
poly([(883,124),(899,124),(566,567),(549,567)],'#edead0')
# window framing
rect((670,116,684,569),'#f5e8ca',ink,2)
rect((449,333,906,347),'#f5e8ca',ink,2)
rect((446,111,911,123),cream,ink,2)
rect((446,558,911,576),cream,ink,2)
rect((445,119,457,568),cream,ink,2)
rect((895,119,908,568),cream,ink,2)
rect((418,578,938,596),'#f7e8c5',ink,2,r=3)
rect((428,596,932,605),'#c89c67',r=2)
# curtains, rods
line([(403,89),(951,89)],ink,6)
ellipse((395,81,410,97),wood,ink)
ellipse((946,81,961,97),wood,ink)
poly([(415,99),(515,99),(498,190),(480,267),(482,383),(460,489),(408,489),(427,295)],'#f1d99e',ink)
poly([(836,99),(935,99),(922,290),(947,489),(896,489),(874,386),(878,277),(852,191)],'#f1d99e',ink)
for x in [425,448,471,494]: line([(x,104),(x-8,200),(x-13,270)],'#d5b77e',2)
for x in [850,874,897,920]: line([(x,104),(x+10,200),(x+14,270)],'#d5b77e',2)
line([(414,340),(483,340)],'#b38755',6)
line([(875,340),(933,340)],'#b38755',6)
for x in range(422,510,19):arc((x,81,x+9,106),10,350,ink,2)
for x in range(842,937,19):arc((x,81,x+9,106),10,350,ink,2)
# upper-left open shelf
rect((51,173,343,190),wood,ink,2,r=2)
rect((70,190,82,217),darkwood,r=2);rect((306,190,318,217),darkwood,r=2)
# ceramic plate stacks
for y in [161,156,151]:
    ellipse((91,y,177,y+14),'#ece6c9',ink,1)
arc((109,91,167,152),0,180,'#ece6c9',14)
# lidded jars
for x,h,c in [(205,48,'#e9cf98'),(260,62,'#cda373')]:
    rect((x,173-h,x+41,173),c,ink,2,r=6)
    rect((x-2,168-h,x+43,177-h),'#a4764b',ink,2,r=2)
    rect((x+9,148,x+33,163),'#f4e6bc',r=2)
# hanging rail and utensils
line([(83,255),(338,255)],ink,5)
for x in [117,177,237,299]: arc((x-6,247,x+6,267),10,280,ink,2)
line([(118,268),(118,319)],ink,5);ellipse((104,312,132,356),'#b78c53',ink,2)
line([(178,268),(178,327)],ink,5);rect((164,322,192,363),'#be9562',ink,2,r=9)
for x in [171,178,185]:line([(x,329),(x,353)],'#785b3f',2)
line([(237,268),(237,320)],ink,5);ellipse((215,310,259,358),'#7d8475',ink,3);ellipse((222,317,252,351),'#505f53',ink,1)
line([(299,269),(299,320)],ink,4);arc((287,311,310,354),0,360,ink,3)
# right wall shelves
rect((996,192,1190,207),wood,ink,2,r=2)
rect((1010,207,1021,228),darkwood);rect((1168,207,1179,228),darkwood)
for x,c,h in [(1013,'#8b9c80',41),(1061,'#e2b775',52),(1111,'#bd7958',36)]:
    rect((x,192-h,x+34,191),c,ink,2,r=5)
    rect((x-2,187-h,x+36,194-h),'#c29b63',ink,2,r=2)
# herbs hanging
line([(1018,290),(1177,290)],ink,4)
for x in [1050,1133]:
    arc((x-5,280,x+5,302),0,290,ink,2)
    line([(x,300),(x-3,370)],'#82784c',3)
    for dx,dy in [(-17,16),(16,22),(-22,38),(18,44),(-15,58),(11,62)]:
        line([(x,306),(x+dx,306+dy)],'#768260',2)
        ellipse((x+dx-7,300+dy,x+dx+7,321+dy),'#7d8b60')
# backsplash tile
rect((0,433,392,636),'#e9dec0')
for y in [433,484,535,586,636]:line([(0,y),(392,y)],'#c9bea2',2)
for row,y in enumerate(range(433,636,51)):
    for x in range(-30+(row%2)*51,393,102):line([(x,y),(x,y+51)],'#c9bea2',2)
# floor below furniture
rect((0,729,1200,900),'#bd8d5c')
for y in [766,809,859]:line([(0,y),(1200,y)],'#a5764b',2)
for x in range(-150,1300,200):line([(x,730),(x+110,900)],'#a5764b',2)
# lower cabinetry
rect((394,641,1200,797),'#8b9e83',ink,3)
rect((406,781,1200,810),'#687e69',ink,2)
for x,w in [(411,168),(591,178),(783,180),(979,204)]:
    rect((x,657,x+w,773),'#9eaf91',ink,2,r=3)
    rect((x+12,669,x+w-12,760),'#9eaf91','#7d9277',2,r=2)
    line([(x+w/2-15,679),(x+w/2+15,679)],'#5e6550',4)
# counter
rect((387,621,1200,643),'#956441',ink,2,r=3)
rect((390,620,1200,628),'#d1a16b',r=2)
# range
rect((16,627,387,802),'#eee2be',ink,3,r=5)
rect((21,628,382,668),'#e0d4b1',ink,2)
for x in [66,132,271,337]:ellipse((x-10,640,x+10,660),'#6f7467',ink,2);line([(x,643),(x,649)],cream,2)
rect((45,681,356,783),'#777b6a',ink,3,r=7)
rect((59,696,342,768),'#3e4f46',ink,2,r=5)
rect((73,704,329,754),'#596655',r=4)
line([(82,690),(321,690)],'#f0e1bc',7)
for y in [725,744]: line([(82,y),(319,y)],'#899078',2)
rect((16,609,387,632),'#505e50',ink,3,r=4)
for x in [91,295]:ellipse((x-55,601,x+55,623),'#838b75',ink,2);ellipse((x-38,604,x+38,617),'#3b4d41',ink,2)
# kettle on stove
arc((98,498,189,586),177,362,ink,9)
poly([(108,564),(84,549),(68,549),(88,578),(107,585)],'#bc815c',ink,2)
ellipse((103,540,192,613),'#bd7f59',ink,3)
ellipse((107,536,188,556),'#d59e72',ink,2)
rect((131,528,164,539),'#6c6751',ink,2,r=4)
line([(118,563),(114,583),(120,594)],'#e6b587',4)
# kettle steam
arc((68,474,105,528),270,440,'#faf1d4',3)
arc((80,445,117,497),100,250,'#faf1d4',3)
# towel from stove rail
rect((259,686,311,786),'#efd9a5',ink,1,r=2)
for x in [267,278,291,302]:line([(x,691),(x,782)],'#b97351',2)
for y in [765,774]:line([(262,y),(308,y)],'#b97351',2)
# sink
ellipse((586,610,786,632),'#b8b8a0',ink,2)
ellipse((603,614,770,627),'#7e9283',ink,2)
arc((681,524,735,588),180,360,'#798b7b',9)
line([(685,555),(685,609)],'#798b7b',9)
line([(731,555),(731,568)],'#798b7b',8)
line([(685,555),(685,604)],'#d0cfb1',2)
# plant on sill
rect((806,539,861,580),'#bd7655',ink,2,r=4)
rect((801,532,866,543),'#cf8b62',ink,2,r=3)
for dx,dy in [(-35,-42),(-20,-65),(0,-71),(26,-61),(40,-34),(14,-35)]:
    line([(833,534),(833+dx,534+dy)],'#667b4f',3)
    ellipse((822+dx,512+dy,842+dx,539+dy),'#778c58',ink,1)
# bowl and little fruit
ellipse((985,605,1132,630),'#776f51',ink,1)
for x,y,c in [(1010,596,'#d9a24c'),(1055,592,'#bd7152'),(1091,598,'#e2b858')]:
    ellipse((x-20,y-19,x+20,y+20),c,ink,1);line([(x,y-17),(x+3,y-25)],ink,3)
poly([(981,609),(1137,609),(1115,637),(1001,637)],'#e5c894',ink,2)
arc((985,598,1133,622),0,180,ink,2)
# chopping board and bread at counter
rect((434,607,560,621),'#b17d4c',ink,2,r=8)
ellipse((452,574,548,617),'#c99450',ink,2)
for x in [472,494,516]: line([(x,581),(x-11,599)],'#f5d59a',4)
# afternoon-like morning sunlight on floor
poly([(518,807),(722,807),(528,900),(217,900)],'#d8ae70')
poly([(743,807),(794,807),(691,900),(604,900)],'#d8ae70')
# foreground round farmhouse table and legs
poly([(257,810),(290,810),(277,900),(249,900)],darkwood,ink,2)
poly([(886,810),(919,810),(937,900),(910,900)],darkwood,ink,2)
ellipse((164,716,1028,902),'#925b39',ink,3)
ellipse((164,700,1028,881),'#c3925b',ink,3)
ellipse((178,705,1015,864),'#cea16b',None)
# wood grain on table, subtle
arc((201,737,1001,855),14,165,'#ba8a55',2)
arc((237,720,948,850),15,160,'#dcb37a',2)
arc((259,731,1019,866),12,146,'#ba8a55',1)
# table linen
poly([(621,712),(760,722),(793,867),(643,879)],'#efe4bf',ink,1)
for x in range(636,758,12):line([(x,720),(x+29,871)],'#d4c6a3',1)
line([(645,853),(786,843)],'#a6a88b',3)
line([(648,862),(789,852)],'#a6a88b',2)
# breakfast plate
ellipse((390,759,598,832),'#a58b5b')
ellipse((386,748,596,822),'#f6e9c8',ink,2)
ellipse((402,755,580,811),None,'#b5b897',2)
# croissant segments
poly([(423,787),(435,769),(457,759),(487,759),(517,770),(541,789),(525,800),(499,786),(470,782),(446,797)],'#c38a41',ink,2)
for v in [[(441,770),(449,795),(463,783),(459,761)],[(462,760),(471,785),(488,785),(484,759)],[(486,761),(492,786),(510,794),(506,769)]]:poly(v,'#e2b167',ink,1)
line([(450,769),(452,781)],'#f8d899',3);line([(475,765),(479,778)],'#f8d899',3)
# butter dish and jar
ellipse((729,759,816,786),'#f7e8c4',ink,2)
rect((746,746,796,771),'#e6c66c',ink,1,r=3)
rect((848,729,896,783),'#b86a46',ink,2,r=8)
rect((844,724,900,738),'#dfc59b',ink,2,r=3)
rect((852,746,893,771),'#efe1b8',r=3)
ellipse((867,751,878,762),'#b46b4b')
# coffee cup and saucer
ellipse((274,763,390,800),'#9b784e')
ellipse((271,758,389,790),'#eee0b8',ink,2)
arc((347,710,391,754),255,105,'#647d6a',10)
arc((350,714,384,749),265,98,'#c2d0ab',3)
rect((291,715,357,762),'#809983',ink,2,r=11)
ellipse((291,704,357,725),'#b8c3a0',ink,2)
ellipse((299,709,350,721),'#654a32')
arc((311,655,337,705),90,262,'#fff1d1',3)
arc((321,625,347,674),267,443,'#fff1d1',3)
# small vase with flowers
ellipse((903,707,974,727),'#aa8b56')
line([(935,697),(934,633)],'#7e8858',3)
line([(935,677),(913,646)],'#7e8858',2)
line([(935,679),(955,642)],'#7e8858',2)
ellipse((911,674,957,720),'#d3ad79',ink,2)
rect((925,666,943,681),'#d3ad79',ink,2,r=3)
for x,y in [(934,628),(911,641),(956,638)]:
    for a in range(0,360,72):
        xx=x+math.cos(math.radians(a))*8; yy=y+math.sin(math.radians(a))*8
        ellipse((xx-6,yy-6,xx+6,yy+6),'#f7e5b6',None)
    ellipse((x-4,y-4,x+4,y+4),'#be8d44')
# cat curled on the kitchen floor, lower-right
ellipse((1050,832,1195,880),'#ac8050')
ellipse((1060,815,1178,868),'#d6a366',ink,2)
ellipse((1100,806,1161,859),'#dfb27a',ink,2)
poly([(1104,819),(1104,797),(1122,809)],'#dfb27a',ink,2)
poly([(1138,809),(1157,796),(1157,823)],'#dfb27a',ink,2)
poly([(1109,813),(1109,805),(1117,811)],'#b67c5b')
poly([(1145,811),(1153,804),(1153,815)],'#b67c5b')
arc((1111,824,1124,833),0,160,ink,2);arc((1138,824,1151,833),0,160,ink,2)
poly([(1128,834),(1135,834),(1131,838)],'#9b6750')
arc((1064,825,1139,871),25,280,'#ba834f',10)
arc((1064,825,1139,871),25,280,ink,1)
for x in [1080,1095]:line([(x,818),(x+4,829)],'#b37d49',3)
# subtle illustration grain
noise=Image.effect_noise(im.size,9).convert('RGB')
im=Image.blend(im,noise,0.035)
im.resize((1500,1125),Image.Resampling.LANCZOS).save('/tmp/vellery-03jo3f9n/work/artifacts/cozy-kitchen-morning.png')
