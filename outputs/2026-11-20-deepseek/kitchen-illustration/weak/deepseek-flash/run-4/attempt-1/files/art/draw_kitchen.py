from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps, ImageEnhance
import math, random

random.seed(41)
S = 2
W, H = 1600, 1200
CW, CH = W*S, H*S

def C(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), a)

def X(v): return int(round(v*S))
def B(x0,y0,x1,y1): return (X(x0),X(y0),X(x1),X(y1))
def P(pts): return [(X(x),X(y)) for x,y in pts]
def Lw(v): return max(1,int(round(v*S)))

def mix(c1,c2,t):
    return tuple(int(round(c1[i]+(c2[i]-c1[i])*t)) for i in range(3))

def rgb(c): return c[:3]

canvas = Image.new('RGBA', (CW,CH), C('#E9DCC5'))
D = ImageDraw.Draw(canvas)

def comp(layer, blur=0):
    """Composite an RGBA layer, optionally blurring a padded local crop."""
    bbox = layer.getbbox()
    if not bbox:
        return
    if blur:
        pad = int(blur*S*4)+2
        x0=max(0,bbox[0]-pad); y0=max(0,bbox[1]-pad)
        x1=min(CW,bbox[2]+pad); y1=min(CH,bbox[3]+pad)
        crop=layer.crop((x0,y0,x1,y1)).filter(ImageFilter.GaussianBlur(blur*S))
        canvas.alpha_composite(crop,(x0,y0))
    else:
        canvas.alpha_composite(layer)

def newlayer():
    return Image.new('RGBA',(CW,CH),(0,0,0,0))

def soft_ellipse(cx,cy,rx,ry,color,alpha=75,blur=8):
    l=newlayer(); d=ImageDraw.Draw(l)
    d.ellipse(B(cx-rx,cy-ry,cx+rx,cy+ry), fill=color[:3]+(alpha,))
    comp(l,blur)

def soft_poly(points,color,alpha=60,blur=5):
    l=newlayer(); d=ImageDraw.Draw(l)
    d.polygon(P(points), fill=color[:3]+(alpha,))
    comp(l,blur)

def grad_img(w,h,stops,horizontal=False):
    # stops: [(t,hex),...] sorted
    im=Image.new('RGB',(w,h))
    px=im.load()
    for y in range(h):
        for x in range(w):
            t=(x/(w-1)) if horizontal else (y/(h-1))
            col=stops[0][1]
            for i in range(len(stops)-1):
                t0,c0=stops[i]; t1,c1=stops[i+1]
                if t0<=t<=t1:
                    u=(t-t0)/(t1-t0) if t1>t0 else 0
                    col=mix(C(c0)[:3],C(c1)[:3],u)
                    break
            else:
                col=C(stops[-1][1])[:3]
            px[x,y]=col
    return im

def catmull(points, closed=False, samples=16):
    pts=list(points)
    if closed:
        ext=[pts[-1]]+pts+[pts[0],pts[1]]
    else:
        ext=[pts[0]]+pts+[pts[-1]]
    out=[]
    for i in range(len(ext)-3):
        p0,p1,p2,p3=ext[i:i+4]
        for j in range(samples):
            t=j/samples
            t2=t*t; t3=t2*t
            x=0.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y=0.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x,y))
    if not closed:
        out.append(pts[-1])
    return out

def smooth_line(points, color, width, closed=False, samples=12, alpha=255):
    pts=catmull(points,closed,samples)
    if closed:
        pts=pts+[pts[0]]
    D.line(P(pts), fill=color[:3]+(alpha,), width=Lw(width), joint='curve')
    if not closed:
        for q in (pts[0],pts[-1]):
            r=width/2
            D.ellipse(B(q[0]-r,q[1]-r,q[0]+r,q[1]+r), fill=color[:3]+(alpha,))

def bez(p0,p1,p2,p3,n=60):
    pts=[]
    for i in range(n+1):
        t=i/n; u=1-t
        x=u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0]
        y=u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]
        pts.append((x,y))
    return pts

# ============================================================
# WALL
# ============================================================
wall = grad_img(800,600,[(0,'#F1E6D3'),(0.55,'#EADCC4'),(1,'#DDC9AB')])
wall = wall.resize((CW,CH), Image.LANCZOS).convert('RGBA')
canvas.paste(wall,(0,0))

# subtle plaster mottling
rnd = random.Random(7)
mott = Image.new('RGBA',(800,600),(0,0,0,0))
md = ImageDraw.Draw(mott)
for _ in range(170):
    x=rnd.uniform(-20,820); y=rnd.uniform(-20,620)
    rx=rnd.uniform(8,60); ry=rnd.uniform(5,30)
    col=(255,245,225) if rnd.random()<.52 else (139,102,70)
    a=rnd.randint(2,7)
    md.ellipse((x-rx,y-ry,x+rx,y+ry), fill=col+(a,))
mott=mott.resize((CW,CH), Image.LANCZOS)
comp(mott)

# warm wash around window opening
wash = newlayer(); wd=ImageDraw.Draw(wash)
wd.ellipse(B(280,20,1250,820), fill=C('#FFDCA6', 18))
comp(wash, blur=60)

# ============================================================
# FLOOR (drawn behind cabinetry)
# ============================================================
floor = grad_img(700,260,[(0,'#C58A68'),(0.5,'#B87355'),(1,'#99573F')])
floor = floor.resize((CW, CH-X(960)), Image.LANCZOS).convert('RGBA')
canvas.paste(floor,(0,X(960)))

# terracotta tile grout, perspective fan
fl = newlayer(); fd=ImageDraw.Draw(fl)
# horizontal rows
for yy in [978,1004,1036,1075,1123,1180]:
    fd.line(P([(0,yy),(1600,yy)]), fill=C('#8C513C',90), width=Lw(1.6))
    fd.line(P([(0,yy+2.5),(1600,yy+2.5)]), fill=C('#E1A27F',55), width=Lw(1.1))
# lines converging above floor
vp=(800,620)
for xb in range(-500,2101,165):
    fd.line(P([vp,(xb,1200)]), fill=C('#8C513C',80), width=Lw(1.4))
comp(fl)
# broad morning sheen on the floor
soft_poly([(460,980),(900,980),(1160,1200),(500,1200)], C('#FFD79A'), 55, 28)

# ============================================================
# WINDOW: recess, garden, frame, curtains
# ============================================================
# shadow of window recess
box_outer=(402,78,1138,648)
soft_poly([(box_outer[0]-10,box_outer[1]+14),(box_outer[2]+12,box_outer[1]+14),
           (box_outer[2]+18,box_outer[3]+10),(box_outer[0]-14,box_outer[3]+10)],
          (48,29,18), 75, 13)

# outer casing
D.rounded_rectangle(B(402,80,1138,646), radius=X(8), fill=C('#8A5B3C'), outline=C('#4C3121'), width=Lw(2.5))
D.rounded_rectangle(B(410,88,1130,638), radius=X(6), fill=C('#6D472F'), outline=C('#9E6F4E'), width=Lw(2))
# deep reveal
D.rounded_rectangle(B(430,104,1110,614), radius=X(4), fill=C('#3B2A1C'))
# glass opening mask coordinates
gx0,gy0,gx1,gy1=452,126,1088,592
glass_mask=Image.new('L',(CW,CH),0)
ImageDraw.Draw(glass_mask).rectangle(B(gx0,gy0,gx1,gy1), fill=255)

# sky seen through window
sky=grad_img(500,360,[(0,'#F3C88C'),(0.38,'#F9DCA6'),(0.68,'#F4E2B2'),(1,'#DDE0A9')])
sky=sky.resize((CW,CH),Image.LANCZOS).convert('RGBA')
sky.putalpha(glass_mask)
canvas.alpha_composite(sky)

# sun glow and disc clipped to glass
glow=newlayer(); gd=ImageDraw.Draw(glow)
gd.ellipse(B(820,120,1060,360), fill=C('#FFEDC0',70))
gd.ellipse(B(865,170,1010,315), fill=C('#FFF2CF',115))
gd.ellipse(B(900,205,978,283), fill=C('#FFF9E7',235))
glow.putalpha(ImageChops.multiply(glow.getchannel('A'),glass_mask))
comp(glow, blur=7)
D.ellipse(B(917,222,963,268), fill=C('#FFF8DE'), outline=C('#F3D79D'), width=Lw(1.2))

# distant fields
land=newlayer(); ld=ImageDraw.Draw(land)
ld.ellipse(B(420,420,760,570), fill=C('#C7C18B'))
ld.ellipse(B(660,455,940,600), fill=C('#B7BB85'))
ld.ellipse(B(860,430,1120,600), fill=C('#C9C592'))
ld.ellipse(B(440,500,760,630), fill=C('#A9B47B'))
ld.ellipse(B(720,510,1040,640), fill=C('#98A972'))
ld.ellipse(B(930,505,1150,620), fill=C('#B0B97D'))
# meadow flecks
for i in range(65):
    x=rnd.uniform(455,1085); y=rnd.uniform(480,595)
    ld.ellipse(B(x,y,x+rnd.uniform(1,4),y+rnd.uniform(1,2)), fill=C('#E7D190', rnd.randint(60,140)))
land.putalpha(ImageChops.multiply(land.getchannel('A'),glass_mask))
comp(land, blur=2.5)

# trees and garden, layered for depth
trees=newlayer(); td=ImageDraw.Draw(trees)

# right-hand tree trunk and branches
trunk=[(1064,596),(1058,548),(1067,502),(1054,452),(1062,402),(1050,350),(1055,302)]
for w,col in [(13,'#5A422C'),(8,'#765538'),(3,'#9C7B50')]:
    td.line(P(trunk), fill=C(col), width=Lw(w), joint='curve')
# branches
for br in [[(1056,430),(1028,398),(995,382)],[(1056,392),(1082,360),(1104,338)],
           [(1050,352),(1012,330),(980,322)],[(1060,490),(1088,468),(1107,440)],
           [(1060,532),(1030,512),(1002,508)]]:
    td.line(P(br), fill=C('#6A4B31'), width=Lw(5), joint='curve')
    td.line(P(br), fill=C('#8C6844'), width=Lw(1.8), joint='curve')

# leafy canopy clusters
def leaf_cluster(cx,cy,rx,ry,dark,mid,light,fruit=True):
    td.ellipse(B(cx-rx,cy-ry,cx+rx,cy+ry), fill=C(dark,245))
    for i in range(24):
        a=rnd.uniform(0,math.tau); rad=rnd.uniform(0,1)**.55
        ex=cx+math.cos(a)*rx*.82*rad; ey=cy+math.sin(a)*ry*.82*rad
        rr=rnd.uniform(.14,.32)*rx
        col=light if (ex>cx and ey<cy and rnd.random()<.7) else (mid if rnd.random()<.72 else dark)
        td.ellipse(B(ex-rr,ey-rr*.72,ex+rr,ey+rr*.72), fill=C(col,230))
    # sunlit edge dabs
    for i in range(12):
        ex=cx+rnd.uniform(-.25,.85)*rx; ey=cy-rnd.uniform(.1,.85)*ry
        rr=rnd.uniform(2,6)
        td.ellipse(B(ex-rr,ey-rr*.7,ex+rr,ey+rr*.7), fill=C('#D7D291',rnd.randint(110,205)))

leaf_cluster(1015,315,112,88,'#536943','#718652','#91A466')
leaf_cluster(960,392,82,76,'#5B7148','#788C58','#9AAA6C')
leaf_cluster(1058,378,88,92,'#4E6541','#6A7F4D','#8FA467')
leaf_cluster(1070,480,74,82,'#516943','#6E8552','#8FA468')
leaf_cluster(995,505,60,54,'#5E7449','#7C9059','#A2B471')
leaf_cluster(1100,442,48,55,'#5C7247','#7B8F57','#A8B474')
# left side foliage
leaf_cluster(492,342,72,88,'#566B45','#778C57','#9AAD6C')
leaf_cluster(470,427,62,76,'#5C7248','#7A8F59','#A0B171')
leaf_cluster(540,465,52,50,'#647A4D','#81965E','#ABB878')
# low hedge across the garden
for i in range(20):
    hx=452+i*32.5
    hy=568+random.uniform(-8,7)
    rr=random.uniform(19,30)
    col=['#6F854F','#7F955B','#667C4A','#8CA063'][i%4]
    td.ellipse(B(hx-rr,hy-rr*.72,hx+rr,hy+rr*.72), fill=C(col,235))
    td.arc(B(hx-rr,hy-rr*.72,hx+rr,hy+rr*.72), 195, 315, fill=C('#B9BE80',90), width=Lw(2))
# meadow grasses
for i in range(80):
    gx=rnd.uniform(455,1085); gy=rnd.uniform(572,592)
    td.line(P([(gx,gy),(gx+rnd.uniform(-5,5),gy-rnd.uniform(3,12))]),
            fill=C(['#8C9B5D','#A9AF70','#778B50'][i%3],145), width=Lw(1))
# wildflowers near the sill
for i in range(11):
    fx=rnd.uniform(465,1080); fy=rnd.uniform(556,586)
    td.line(P([(fx,fy+7),(fx+rnd.uniform(-2,2),fy-4)]), fill=C('#6D8650',170), width=Lw(1))
    td.ellipse(B(fx-3,fy-7,fx+3,fy-1), fill=C(['#E9D8A7','#E6A07C','#F1E8CF'][i%3],220))
    td.ellipse(B(fx-1,fy-5,fx+1,fy-3), fill=C('#C8914F',200))

trees.putalpha(ImageChops.multiply(trees.getchannel('A'),glass_mask))
comp(trees, blur=1.7)

# foreground leaves crossing the sun, for depth
frontleaf=newlayer(); fld=ImageDraw.Draw(frontleaf)
fld.line(P([(1074,300),(1042,286),(1010,276),(976,266),(948,258)]), fill=C('#5A422C'), width=Lw(2.6), joint='curve')
# little twigs and irregular leaves along the branch
for tx,ty,ang in [(1048,286,-46),(1020,280,52),(992,272,-38),(968,264,60)]:
    a=math.radians(ang)
    fld.line(P([(tx,ty),(tx+math.cos(a)*14,ty+math.sin(a)*14)]), fill=C('#5A422C'), width=Lw(1.4))
leaf_spots=[(1054,282,-35),(1040,292,20),(1024,274,-60),(1014,286,55),(998,268,-15),
            (986,280,35),(972,258,-65),(960,270,50),(948,252,-20),(942,262,35)]
for li,(lx,ly,ang) in enumerate(leaf_spots):
    a=math.radians(ang)
    dx=math.cos(a); dy=math.sin(a)
    p0=(lx-dx*7,ly-dy*7); p1=(lx-dx*2-dy*5,ly-dy*2+dx*5)
    p2=(lx+dx*9,ly+dy*9); p3=(lx-dx*2+dy*5,ly-dy*2-dx*5)
    fld.polygon(P([p0,p1,p2,p3]), fill=C(['#5F7548','#788C55','#8FA363'][li%3],225))
    fld.line(P([p0,p2]), fill=C('#A7B476',70), width=Lw(.8))
frontleaf.putalpha(ImageChops.multiply(frontleaf.getchannel('A'),glass_mask))
comp(frontleaf, blur=.8)

# dappled leaf highlights
dap=newlayer(); dd=ImageDraw.Draw(dap)
for i in range(95):
    if i<42:
        x=rnd.uniform(455,700); y=rnd.uniform(310,560)
    else:
        x=rnd.uniform(900,1090); y=rnd.uniform(300,560)
    r=rnd.uniform(1.2,6.5)
    dd.ellipse(B(x-r,y-r*.7,x+r,y+r*.7), fill=C('#E8E2A8',rnd.randint(22,70)))
# a few bright glints in the left canopy
for x,y in [(505,300),(525,330),(475,370),(1000,290),(1030,330),(1050,420)]:
    dd.ellipse(B(x-7,y-3,x+7,y+3), fill=C('#F2E7B0',45))
dap.putalpha(ImageChops.multiply(dap.getchannel('A'),glass_mask))
comp(dap)

# two birds
for bx,by in [(560,168),(585,158)]:
    D.arc(B(bx-11,by-5,bx,by+4), 200, 340, fill=C('#5E5238',190), width=Lw(1.4))
    D.arc(B(bx,by-5,bx+11,by+4), 200, 340, fill=C('#5E5238',190), width=Lw(1.4))

# frame bars over glass
D.rectangle(B(452,202,1088,217), fill=C('#5B3A26'), outline=C('#8B6042'), width=Lw(1.2))
D.rectangle(B(762,126,778,592), fill=C('#5B3A26'), outline=C('#8B6042'), width=Lw(1.2))
# outer glass frame/beading
D.rectangle(B(452,126,1088,592), outline=C('#3F2A1D'), width=Lw(3))
D.rectangle(B(460,134,1080,584), outline=C('#9C6E4D'), width=Lw(1))
# bevel highlights
D.line(P([(410,90),(1130,90)]), fill=C('#B7865D',170), width=Lw(2))
D.line(P([(406,96),(406,638)]), fill=C('#B7865D',130), width=Lw(1.8))
D.line(P([(410,642),(1132,642)]), fill=C('#3C2718',160), width=Lw(2))

# glass reflection, soft diagonal sheen
refl=newlayer(); rd=ImageDraw.Draw(refl)
rd.polygon(P([(480,590),(610,126),(700,126),(560,590)]), fill=C('#FFF9E7',28))
rd.polygon(P([(606,590),(736,126),(772,126),(642,590)]), fill=C('#FFF9E7',20))
rd.polygon(P([(870,590),(1000,126),(1030,126),(900,590)]), fill=C('#FFF9E7',12))
refl.putalpha(ImageChops.multiply(refl.getchannel('A'),glass_mask))
comp(refl, blur=1.5)

# sill
D.rounded_rectangle(B(396,600,1144,632), radius=X(4), fill=C('#C08A5D'), outline=C('#5C3B26'), width=Lw(2))
D.rectangle(B(396,628,1144,642), fill=C('#8C5A39'), outline=C('#5C3B26'), width=Lw(1.8))
D.line(P([(400,608),(1140,608)]), fill=C('#E8B784',160), width=Lw(1.6))
soft_poly([(420,644),(1122,644),(1112,660),(432,660)], C('#4A2D1D'), 55, 6)

# ============================================================
# CURTAINS + ROD
# ============================================================
# rod
D.line(P([(376,84),(1164,84)]), fill=C('#5C4636'), width=Lw(5))
D.line(P([(378,82),(1162,82)]), fill=C('#A88663'), width=Lw(1.4))
for cx in (378,1162):
    D.ellipse(B(cx-9,76,cx+9,94), fill=C('#7A5A3E'), outline=C('#402F23'), width=Lw(1.4))

# left curtain
left_pts=[(388,92),(472,96),(458,170),(466,245),(444,320),(456,392),(434,470),(448,548),(424,610),(386,616)]
D.polygon(P(left_pts), fill=C('#E8D8B9'))
D.line(P(left_pts+[left_pts[0]]), fill=C('#8C6B4C'), width=Lw(1.8), joint='curve')
# folds
for pts,col,w in [([(408,100),(400,200),(412,300),(398,420),(410,520),(398,606)],'#C4A883',3),
                  ([(432,100),(442,210),(426,318),(440,426),(424,530),(436,608)],'#D5BC95',3),
                  ([(456,100),(452,200),(462,300),(448,410),(460,510),(450,606)],'#B79875',2)]:
    D.line(P(pts), fill=C(col,150), width=Lw(w))
D.line(P([(416,104),(410,300),(400,500),(392,610)]), fill=C('#F7EDD8',90), width=Lw(2))

# right curtain
right_pts=[(1152,92),(1068,96),(1082,170),(1074,245),(1096,320),(1084,392),(1106,470),(1092,548),(1116,610),(1154,616)]
D.polygon(P(right_pts), fill=C('#E5D3B3'))
D.line(P(right_pts+[right_pts[0]]), fill=C('#8C6B4C'), width=Lw(1.8), joint='curve')
for pts,col,w in [([(1132,100),(1142,200),(1128,300),(1142,420),(1130,520),(1142,606)],'#C4A883',3),
                  ([(1108,100),(1098,210),(1114,318),(1100,426),(1116,530),(1104,608)],'#D5BC95',3),
                  ([(1084,100),(1088,200),(1078,300),(1092,410),(1080,510),(1090,606)],'#B79875',2)]:
    D.line(P(pts), fill=C(col,150), width=Lw(w))
D.line(P([(1136,104),(1142,300),(1152,500),(1160,610)]), fill=C('#F7EDD8',80), width=Lw(2))

# sun catching the inner edges of the curtains
D.line(P([(466,104),(456,190),(438,300),(444,392),(432,480),(442,548),(424,606)]), fill=C('#FFF4D6',95), width=Lw(3.2), joint='curve')
D.line(P([(1086,104),(1076,190),(1094,300),(1088,392),(1100,480),(1090,548),(1116,606)]), fill=C('#FFF4D6',80), width=Lw(3), joint='curve')
D.line(P([(400,608),(444,604),(430,612),(398,615)]), fill=C('#B69975',140), width=Lw(1.5))
D.line(P([(1110,606),(1150,608),(1148,615),(1114,613)]), fill=C('#B69975',120), width=Lw(1.4))
soft_poly([(390,614),(470,610),(466,628),(392,632)], C('#4C3020'),25,4)

# ============================================================
# TILE BACKSPLASH
# ============================================================
D.rectangle(B(0,622,1600,690), fill=C('#E8D9BE'))
tl=newlayer(); tld=ImageDraw.Draw(tl)
tw,th=46,26
for row,yy in enumerate(range(622,692,th)):
    offset = -tw//2 if row%2 else 0
    for xx in range(offset-46,1601,tw):
        tld.rectangle(B(xx+1,yy+1,xx+tw-2,yy+th-2), outline=C('#C5AD8A',90), width=Lw(1))
    tld.line(P([(0,yy),(1600,yy)]), fill=C('#B99F7F',100), width=Lw(1.2))
comp(tl)
soft_poly([(0,688),(1600,688),(1600,696),(0,696)], C('#8B6A4B'),60,3)

# ============================================================
# LEFT SHELVES AND OBJECTS
# ============================================================
# framed little morning print
D.rounded_rectangle(B(150,150,304,274), radius=X(3), fill=C('#795239'), outline=C('#4A3120'), width=Lw(2))
D.rectangle(B(160,160,294,264), fill=C('#EBD8B3'))
D.rectangle(B(168,168,286,256), fill=C('#F3E4C4'))
# art: sun and fields
soft_ellipse(230,205,20,20,C('#F1C074'),220,5)
D.ellipse(B(214,189,246,221), fill=C('#E7A958'))
D.polygon(P([(168,240),(205,216),(242,238),(270,222),(286,232),(286,256),(168,256)]), fill=C('#9EAF7D'))
D.polygon(P([(168,248),(212,230),(254,249),(286,243),(286,256),(168,256)]), fill=C('#7E9365'))
D.line(P([(170,238),(206,216),(242,237),(271,222),(284,229)]), fill=C('#E9D7A8'), width=Lw(1.2))
D.line(P([(160,160),(160,264)]), fill=C('#C69A6A'), width=Lw(1))
# nail shadow
soft_ellipse(227,278,36,7,C('#4B2C1B'),55,5)

# shelf boards
for sy in (354,524):
    D.rectangle(B(48,sy,372,sy+16), fill=C('#A56C45'), outline=C('#553722'), width=Lw(2))
    D.rectangle(B(54,sy+3,366,sy+7), fill=C('#C99464'))
    D.line(P([(50,sy+16),(370,sy+16)]), fill=C('#6E472D'), width=Lw(2.5))
    # brackets
    for bx in (82,334):
        D.polygon(P([(bx,sy+16),(bx+13,sy+16),(bx+13,sy+52)]), fill=C('#4A382A'))
        D.line(P([(bx+1,sy+17),(bx+12,sy+50)]), fill=C('#8B745E'), width=Lw(1.2))
    soft_ellipse(210,sy+22,155,13,C('#4A2C1B'),45,8)

# top shelf: bowl stack
for i,(yy,ww) in enumerate([(343,80),(328,70),(313,60)]):
    cx=112
    D.ellipse(B(cx-ww/2,yy-13,cx+ww/2,yy+13), fill=C('#EBD9BC'), outline=C('#6A4A32'), width=Lw(1.4))
    D.arc(B(cx-ww/2,yy-13,cx+ww/2,yy+13), 0, 180, fill=C('#B7A083'), width=Lw(1.2))
D.ellipse(B(84,310,140,340), fill=C('#F0E2C9'), outline=C('#6A4A32'), width=Lw(1.4))
D.ellipse(B(90,312,134,330), fill=C('#D5BE9B'))
D.arc(B(88,322,136,344), 10, 170, fill=C('#B5A181'), width=Lw(1.2))
# jar of pasta
D.rounded_rectangle(B(178,274,238,354), radius=X(7), fill=C('#D8C2A0'), outline=C('#6A4A32'), width=Lw(1.7))
D.rounded_rectangle(B(184,300,232,350), radius=X(4), fill=C('#C89A54'))
for i in range(13):
    px=188+random.uniform(0,40); py=305+random.uniform(0,40)
    D.line(P([(px,py),(px+random.uniform(-4,4),py+random.uniform(6,14))]), fill=C('#E7C47D',180), width=Lw(1.2))
D.rectangle(B(182,283,234,299), fill=C('#F1E5CE'))
D.rectangle(B(185,285,231,291), fill=C('#C17852'))
D.rounded_rectangle(B(181,265,235,281), radius=X(3), fill=C('#9B6C42'), outline=C('#5D3C26'), width=Lw(1.3))
# teapot
D.ellipse(B(258,318,334,356), fill=C('#EFE0C6'), outline=C('#6B4A32'), width=Lw(1.6))
D.ellipse(B(280,306,316,328), fill=C('#F4E7D0'), outline=C('#6B4A32'), width=Lw(1.3))
D.ellipse(B(292,300,304,311), fill=C('#C79A68'), outline=C('#6B4A32'), width=Lw(1))
D.arc(B(318,320,348,346), 270, 90, fill=C('#6B4A32'), width=Lw(2.2))
D.line(P([(258,335),(244,323)]), fill=C('#6B4A32'), width=Lw(3))
D.ellipse(B(256,330,264,338), fill=C('#6B4A32'))
D.arc(B(270,330,322,352), 10, 170, fill=C('#C1A883'), width=Lw(1.2))

# lower shelf: trailing plant
# pot
D.polygon(P([(78,482),(140,482),(133,528),(86,528)]), fill=C('#B96D4B'), outline=C('#6D3E2A'), width=Lw(1.8))
D.rectangle(B(74,474,144,488), fill=C('#C97D58'), outline=C('#6D3E2A'), width=Lw(1.5))
D.ellipse(B(80,476,138,488), fill=C('#5A4130'))
# vines
vine_paths=[
 [(110,486),(102,530),(90,570),(96,610),(82,652)],
 [(120,486),(132,530),(148,568),(139,608),(154,646),(146,680)],
 [(104,486),(88,518),(80,552),(68,586)],
]
for vp in vine_paths:
    smooth_line(vp,C('#55724A'),3.2,samples=12)
# leaves
leaf_positions=[(98,540,-20),(86,566,-35),(96,598,10),(82,630,-20),(126,532,25),(144,558,40),(140,590,10),(154,626,-10),(76,558,-25),(70,586,20),(120,614,30),(146,662,5)]
for lx,ly,ang in leaf_positions:
    a=math.radians(ang)
    dx=math.cos(a); dy=math.sin(a)
    p0=(lx-dx*7,ly-dy*7); p1=(lx-dx*3-dy*6,ly-dy*3+dx*6)
    p2=(lx+dx*9,ly+dy*9); p3=(lx-dx*3+dy*6,ly-dy*3-dx*6)
    D.polygon(P([p0,p1,p2,p3]), fill=C('#6F8B58'), outline=C('#425B39'), width=Lw(1))
    D.line(P([p0,p2]), fill=C('#9AB67A'), width=Lw(.9))
soft_ellipse(112,536,40,9,C('#4A2C1B'),50,5)

# cookbooks
books=[(172,'#8D5A48',14,0),(187,'#D4B177',12,5),(200,'#71816A',15,-3),(216,'#B56B4C',10,4),(228,'#D9C59F',12,0)]
for x,col,ww,tilt in books:
    D.rectangle(B(x,470,x+ww,522), fill=C(col), outline=C('#5E4431'), width=Lw(1.2))
    D.line(P([(x+3,478),(x+ww-3,478)]), fill=C('#F0E0C2',100), width=Lw(1.2))
    D.line(P([(x+4,490),(x+ww-4,490)]), fill=C('#5A422F',80), width=Lw(1))
# copper canister
D.rounded_rectangle(B(296,468,352,524), radius=X(5), fill=C('#B66E43'), outline=C('#633925'), width=Lw(1.6))
D.rounded_rectangle(B(292,460,356,474), radius=X(4), fill=C('#C67C50'), outline=C('#633925'), width=Lw(1.5))
D.line(P([(302,478),(302,518)]), fill=C('#F0B57C',130), width=Lw(2))
D.line(P([(310,480),(348,480)]), fill=C('#7E432A',100), width=Lw(1))
D.ellipse(B(318,488,330,500), fill=C('#6D3E29'), outline=C('#A66A49'), width=Lw(1))

# ============================================================
# RIGHT WALL: POT RACK, COPPERWARE, CLOCK
# ============================================================
# soft wall shadow behind the hanging copperware
soft_poly([(1184,252),(1558,252),(1548,414),(1200,418)], C('#725A43'), 12, 18)
soft_ellipse(1372,404,195,20,C('#6B533D'),18,14)
# rail
D.line(P([(1178,246),(1568,246)]), fill=C('#3D3027'), width=Lw(6))
D.line(P([(1180,243),(1566,243)]), fill=C('#9A8166'), width=Lw(1.2))
for bx in (1206,1542):
    D.line(P([(bx,246),(bx,220)]), fill=C('#3D3027'), width=Lw(4))
    D.rectangle(B(bx-10,216,bx+10,225), fill=C('#4A392C'))
    D.ellipse(B(bx-4,221,bx+4,229), fill=C('#8E7358'))

def pot_hook(x, tip_y):
    # little S hook with a loop
    pts=catmull([(x,247),(x,262),(x+4,273),(x,283)],samples=10)
    D.line(P(pts), fill=C('#46372A'), width=Lw(2.6), joint='curve')
    D.arc(B(x-6,tip_y-2,x+6,tip_y+11), 180, 360, fill=C('#46372A'), width=Lw(2.3))

# copper saucepan, hung by its handle
pot_hook(1232,270)
D.line(P([(1276,335),(1262,314),(1248,294),(1235,277)]), fill=C('#4A3424'), width=Lw(10), joint='curve')
D.line(P([(1276,335),(1262,314),(1248,294),(1235,277)]), fill=C('#A86A42'), width=Lw(5.2), joint='curve')
D.ellipse(B(1231,276,1249,294), fill=C('#C1915D'), outline=C('#4B3422'), width=Lw(1.3))
D.ellipse(B(1236,281,1244,289), fill=C('#4A3424'))
body=[(1197,335),(1200,355),(1209,374),(1228,383),(1253,384),(1276,375),(1288,357),(1291,335)]
body=catmull(body,closed=True,samples=12)
D.polygon(P(body), fill=C('#B9683F'))
D.line(P(body+[body[0]]), fill=C('#5B3422'), width=Lw(2), joint='curve')
D.ellipse(B(1195,318,1293,347), fill=C('#C77A4C'), outline=C('#5B3422'), width=Lw(1.8))
D.ellipse(B(1204,324,1284,342), fill=C('#7B402C'))
D.arc(B(1200,329,1288,387), 15, 165, fill=C('#F0AC74'), width=Lw(2.2))
D.arc(B(1206,340,1270,390), 110, 245, fill=C('#F9C58D'), width=Lw(6))
D.line(P([(1203,351),(1203,373)]), fill=C('#FFE0B4',100), width=Lw(2))
# helper handle
D.arc(B(1182,336,1206,360), 280, 110, fill=C('#5B3422'), width=Lw(5))
D.arc(B(1184,338,1204,358), 280, 110, fill=C('#B9683F'), width=Lw(2.2))
D.ellipse(B(1270,329,1282,339), fill=C('#E4A16D'))
# skillet
pot_hook(1344,270)
D.line(P([(1372,338),(1364,315),(1352,292),(1346,276)]), fill=C('#4A3424'), width=Lw(9), joint='curve')
D.line(P([(1372,338),(1364,315),(1352,292),(1346,276)]), fill=C('#A86A42'), width=Lw(4.5), joint='curve')
D.ellipse(B(1315,334,1435,403), fill=C('#B25F3B'), outline=C('#5A3322'), width=Lw(2))
D.ellipse(B(1324,337,1427,381), fill=C('#C17549'))
D.ellipse(B(1332,344,1419,373), fill=C('#66392A'))
D.arc(B(1318,357,1432,402), 12, 168, fill=C('#EEA66E'), width=Lw(2.4))
D.arc(B(1324,342,1428,392), 190, 300, fill=C('#F8C48B',120), width=Lw(5))
D.ellipse(B(1323,331,1341,343), fill=C('#D68A58'))
D.ellipse(B(1337,269,1355,287), fill=C('#C1915D'), outline=C('#4B3422'), width=Lw(1.3))
D.ellipse(B(1342,274,1350,282), fill=C('#4A3424'))
# copper colander
pot_hook(1462,270)
D.line(P([(1462,280),(1462,294)]), fill=C('#46372A'), width=Lw(3))
D.ellipse(B(1452,289,1472,309), outline=C('#4B3422'), width=Lw(3.2))
D.ellipse(B(1458,295,1466,303), fill=C('#6E5036'))
D.ellipse(B(1418,324,1522,390), fill=C('#B8663E'), outline=C('#5A3322'), width=Lw(2))
D.ellipse(B(1413,315,1527,345), fill=C('#C97C4D'), outline=C('#5A3322'), width=Lw(1.8))
D.ellipse(B(1423,321,1517,340), fill=C('#7B402C'))
D.arc(B(1422,337,1518,392), 10, 170, fill=C('#F0AC74'), width=Lw(2.2))
D.arc(B(1424,340,1490,392), 110, 240, fill=C('#F7C088'), width=Lw(5))
for r in range(3):
    for c in range(7):
        hx=1437+c*11; hy=350+r*10
        if (hx-1470)**2/900 + (hy-358)**2/210 < 1:
            D.ellipse(B(hx-2,hy-2,hx+2,hy+2), fill=C('#5E3424'))
# colander loop handles
D.arc(B(1402,337,1424,357), 260, 100, fill=C('#5A3322'), width=Lw(4.5))
D.arc(B(1516,337,1538,357), 260, 100, fill=C('#5A3322'), width=Lw(4.5))
# ladle at far right
pot_hook(1544,282)
D.line(P([(1544,290),(1544,384)]), fill=C('#473628'), width=Lw(4))
D.line(P([(1544,290),(1544,384)]), fill=C('#A86A42'), width=Lw(2.2))
D.ellipse(B(1536,277,1552,293), outline=C('#4B3422'), width=Lw(2.8))
D.ellipse(B(1532,382,1556,406), fill=C('#B8683F'), outline=C('#5A3322'), width=Lw(1.5))
D.ellipse(B(1535,385,1553,401), fill=C('#E8A46D'))
# clock
ccx,ccy=1418,476
soft_ellipse(ccx+4,ccy+7,62,62,C('#4A2D1B'),55,8)
D.ellipse(B(ccx-60,ccy-60,ccx+60,ccy+60), fill=C('#6F4B32'), outline=C('#3D291C'), width=Lw(2.5))
D.ellipse(B(ccx-53,ccy-53,ccx+53,ccy+53), fill=C('#B18A58'), outline=C('#7C5A3B'), width=Lw(1.5))
D.ellipse(B(ccx-47,ccy-47,ccx+47,ccy+47), fill=C('#F2E6CD'), outline=C('#8A6744'), width=Lw(1.2))
for ang in range(0,360,30):
    a=math.radians(ang)
    r1=39 if ang%90 else 35
    D.line(P([(ccx+math.cos(a)*r1,ccy+math.sin(a)*r1),(ccx+math.cos(a)*43,ccy+math.sin(a)*43)]),
           fill=C('#7F6144'), width=Lw(1.4 if ang%90 else 2.2))
D.line(P([(ccx,ccy),(ccx+math.cos(math.radians(210))*24,ccy+math.sin(math.radians(210))*24)]),
       fill=C('#4A3527'), width=Lw(3))
D.line(P([(ccx,ccy),(ccx+math.cos(math.radians(300))*31,ccy+math.sin(math.radians(300))*31)]),
       fill=C('#4A3527'), width=Lw(2.2))
D.ellipse(B(ccx-4,ccy-4,ccx+4,ccy+4), fill=C('#7A5236'))
D.arc(B(ccx-40,ccy-40,ccx+40,ccy+40), 205, 305, fill=C('#FFFDF3',90), width=Lw(2))
# note: hands read about 7:10
D.arc(B(ccx-44,ccy-44,ccx+44,ccy+44), 190, 250, fill=C('#C7B18E',80), width=Lw(1.3))

# ============================================================
# COUNTER + CABINETS
# ============================================================
# under-counter body
D.rectangle(B(0,750,1600,972), fill=C('#65745C'))
# subtle vertical warmth across cabinet fronts
cab_wash=newlayer(); cwd=ImageDraw.Draw(cab_wash)
for i in range(6):
    cwd.rectangle(B(i*280,752,i*280+150,972), fill=C('#8A9A77',12))
comp(cab_wash)

# counter shadow / overhang
soft_poly([(0,748),(1600,748),(1600,770),(0,770)],C('#38291C'),95,6)
D.rectangle(B(0,744,1600,760), fill=C('#7D5133'))
D.line(P([(0,758),(1600,758)]), fill=C('#4E3120'), width=Lw(2))

# countertop butcher block
D.rounded_rectangle(B(-4,680,1604,752), radius=X(3), fill=C('#C28A59'))
# plank boards on top
plank_cols=['#C99160','#BE8453','#D09B69','#C28957','#CB9462']
for i in range(5):
    y0=684+i*13.4
    D.rectangle(B(0,y0,1600,y0+13.4), fill=C(plank_cols[i]))
    D.line(P([(0,y0+13.4),(1600,y0+13.4)]), fill=C('#8D5C39',170), width=Lw(1.1))
    D.line(P([(0,y0+1),(1600,y0+1)]), fill=C('#E2AD7C',80), width=Lw(0.8))
# wood grain
rnd2=random.Random(22)
for i in range(95):
    y=rnd2.uniform(687,748); x=rnd2.uniform(0,1520); ln=rnd2.uniform(15,120)
    D.line(P([(x,y),(x+ln,y+rnd2.uniform(-1.5,1.5))]), fill=C('#8A5838',rnd2.randint(20,55)), width=Lw(0.8))
# bright morning edge
D.line(P([(0,684),(1600,684)]), fill=C('#F6C993',190), width=Lw(2.2))
D.rectangle(B(-4,748,1604,756), fill=C('#8A5838'))
D.line(P([(0,753),(1600,753)]), fill=C('#5C3A25'), width=Lw(1.2))

# cabinet fronts helpers
def cabinet_section(x0,x1):
    # stile / frame
    soft_ellipse((x0+x1)/2, 900, (x1-x0)*.54, 108, C('#3B2C22'), 35, 8)
    D.rectangle(B(x0,766,x1,966), fill=C('#6B7B62'), outline=C('#52614D'), width=Lw(1.2))
    # drawer
    D.rounded_rectangle(B(x0+16,776,x1-16,844), radius=X(3), fill=C('#75846A'), outline=C('#4A5946'), width=Lw(1.6))
    D.rounded_rectangle(B(x0+24,784,x1-24,836), radius=X(2), outline=C('#53624E'), width=Lw(1.2))
    D.line(P([(x0+24,785),(x1-24,785)]), fill=C('#93A17F',90), width=Lw(1))
    # door
    D.rounded_rectangle(B(x0+16,854,x1-16,956), radius=X(3), fill=C('#6F8066'), outline=C('#4A5946'), width=Lw(1.8))
    D.rounded_rectangle(B(x0+26,866,x1-26,944), radius=X(2), outline=C('#4E5D49'), width=Lw(1.4))
    D.line(P([(x0+26,867),(x1-26,867)]), fill=C('#8E9D7B',80), width=Lw(1))
    D.line(P([(x0+27,943),(x1-27,943)]), fill=C('#4B5A46',80), width=Lw(1))
    # knob
    kx=(x0+x1)/2
    D.ellipse(B(kx-6,858,kx+6,870), fill=C('#C29A58'), outline=C('#6E4E2D'), width=Lw(1))
    D.ellipse(B(kx-3,860,kx+2,865), fill=C('#F1D28F'))

for x0,x1 in [(18,282),(296,558),(928,1188),(1202,1432),(1446,1580)]:
    cabinet_section(x0,x1)

# sink apron
D.rounded_rectangle(B(594,754,902,852), radius=X(7), fill=C('#EDE0C8'), outline=C('#6A4B34'), width=Lw(2))
D.rectangle(B(604,760,892,780), fill=C('#DCC8A8'))
for i in range(12):
    x=614+i*24
    D.line(P([(x,782),(x,842)]), fill=C('#C9B392',85), width=Lw(1.2))
D.line(P([(604,848),(892,848)]), fill=C('#C8B08E'), width=Lw(2))
D.line(P([(604,762),(892,762)]), fill=C('#FFF4DC',130), width=Lw(1.5))
# lower doors under sink
for x0,x1 in [(608,738),(754,884)]:
    D.rounded_rectangle(B(x0,860,x1,956), radius=X(3), fill=C('#6F8066'), outline=C('#4A5946'), width=Lw(1.8))
    D.rounded_rectangle(B(x0+10,870,x1-10,944), radius=X(2), outline=C('#4E5D49'), width=Lw(1.3))
    kx=(x0+x1)/2
    D.ellipse(B(kx-6,862,kx+6,874), fill=C('#C29A58'), outline=C('#6E4E2D'), width=Lw(1))

# depth and warmth across the cabinet fronts
soft_poly([(0,840),(1600,840),(1600,970),(0,970)], C('#2F2B22'), 24, 18)
soft_poly([(0,758),(1600,758),(1600,798),(0,798)], C('#D9C29B'), 18, 14)
for sx in (288,566,922,1196,1438):
    soft_poly([(sx-3,758),(sx+3,758),(sx+3,970),(sx-3,970)], C('#2E3025'), 34, 4)
# baseboard
D.rectangle(B(0,956,1600,976), fill=C('#5A3D2A'))
D.line(P([(0,958),(1600,958)]), fill=C('#9A704F',110), width=Lw(1.2))
D.line(P([(0,972),(1600,972)]), fill=C('#3D291C'), width=Lw(1.2))
soft_poly([(0,976),(1600,976),(1600,992),(0,992)], C('#3B271B'),70,7)

# ============================================================
# SINK + FAUCET
# ============================================================
# basin
D.rounded_rectangle(B(636,690,864,742), radius=X(8), fill=C('#5A4C40'), outline=C('#4A3627'), width=Lw(2))
D.rounded_rectangle(B(646,696,854,733), radius=X(5), fill=C('#6E5F51'))
D.ellipse(B(650,700,850,730), fill=C('#7E6D5C'))
D.arc(B(654,700,846,730), 190, 345, fill=C('#CAB28F',90), width=Lw(2))
D.arc(B(670,704,760,726), 185, 330, fill=C('#F2DFC1',65), width=Lw(2))
D.ellipse(B(736,714,764,727), fill=C('#A3957D'), outline=C('#4D3F34'), width=Lw(1.2))
D.ellipse(B(744,717,756,724), fill=C('#4B3B2E'))
D.ellipse(B(746,718,752,722), fill=C('#A28E72'))
# inner rim highlight
D.arc(B(638,691,862,743), 185, 355, fill=C('#E9D3B4',120), width=Lw(2))

# faucet
soft_ellipse(848,704,38,10,C('#3D291C'),80,5)
D.ellipse(B(824,692,872,714), fill=C('#9B7440'), outline=C('#5B432A'), width=Lw(1.4))
D.rounded_rectangle(B(840,674,856,700), radius=X(3), fill=C('#AA8148'), outline=C('#5B432A'), width=Lw(1.2))
fauc=[(848,684),(848,642),(846,620),(830,606),(800,602),(774,610),(762,626),(760,646)]
fauc=catmull(fauc,samples=16)
D.line(P(fauc), fill=C('#B0874C'), width=Lw(8), joint='curve')
D.line(P(fauc), fill=C('#D8B16A'), width=Lw(3.4), joint='curve')
D.line(P([(850,670),(850,620),(832,606),(802,601)]), fill=C('#F2D395',150), width=Lw(1.5))
# spout tip
D.ellipse(B(750,638,772,660), fill=C('#9A713E'), outline=C('#533B24'), width=Lw(1.3))
D.ellipse(B(755,646,767,655), fill=C('#4B3A2B'))
# lever handle
D.line(P([(856,682),(884,670)]), fill=C('#8C6638'), width=Lw(5))
D.ellipse(B(882,665,894,677), fill=C('#C49A58'), outline=C('#5B432A'), width=Lw(1))
D.line(P([(850,678),(850,652)]), fill=C('#EED29A',140), width=Lw(1.2))

# soap bottle
soft_ellipse(584,706,22,6,C('#3C281A'),80,4)
D.rounded_rectangle(B(568,660,604,704), radius=X(7), fill=C('#B87434'), outline=C('#5D3E27'), width=Lw(1.3))
D.rectangle(B(576,668,596,690), fill=C('#E9D8B7'))
D.line(P([(580,674),(592,674)]), fill=C('#A66F4A',180), width=Lw(1))
D.rectangle(B(582,650,590,661), fill=C('#6B523B'))
D.rounded_rectangle(B(574,646,598,654), radius=X(2), fill=C('#7C5C3F'), outline=C('#4E3827'), width=Lw(1))

# ============================================================
# COUNTER OBJECTS
# ============================================================
# --- bowl of oranges ---
soft_ellipse(258,718,105,18,C('#3D291C'),90,8)
# lower bowl
D.pieslice(B(170,652,346,736), 0, 180, fill=C('#EAD7B7'), outline=C('#674832'), width=Lw(2))
D.arc(B(178,662,338,728), 20, 160, fill=C('#C7AF8B'), width=Lw(1.4))
# bowl rim
D.ellipse(B(168,640,348,680), fill=C('#F3E4C9'), outline=C('#674832'), width=Lw(2))
D.ellipse(B(180,648,336,676), fill=C('#BFA67F'))
# oranges
oranges=[(206,654,25),(248,640,27),(292,653,24),(265,660,22)]
for ox,oy,r in oranges:
    D.ellipse(B(ox-r,oy-r,ox+r,oy+r), fill=C('#E9893E'), outline=C('#98502A'), width=Lw(1.4))
    D.arc(B(ox-r,oy-r,ox+r,oy+r), 195, 330, fill=C('#F8B26C'), width=Lw(2.4))
    D.arc(B(ox-r,oy-r,ox+r,oy+r), 20, 150, fill=C('#B96232'), width=Lw(2))
    # dimples
    for j in range(3):
        dx=ox+random.uniform(-r*.55,r*.55); dy=oy+random.uniform(-r*.45,r*.6)
        D.ellipse(B(dx-.8,dy-.8,dx+.8,dy+.8), fill=C('#B45F31',150))
# leaves
for lx,ly,ang in [(232,625,-24),(280,632,20),(310,640,45)]:
    a=math.radians(ang)
    p0=(lx,ly); p1=(lx+math.cos(a)*14-math.sin(a)*5,ly+math.sin(a)*14+math.cos(a)*5)
    p2=(lx+math.cos(a)*26,ly+math.sin(a)*26)
    p3=(lx+math.cos(a)*14+math.sin(a)*5,ly+math.sin(a)*14-math.cos(a)*5)
    D.polygon(P([p0,p1,p2,p3]), fill=C('#738A55'), outline=C('#465B36'), width=Lw(1))
# bowl stripe
D.arc(B(180,660,336,724), 15, 165, fill=C('#C77B58'), width=Lw(4))
D.arc(B(180,664,336,728), 15, 165, fill=C('#E1A081'), width=Lw(1))

# --- honey jar ---
soft_ellipse(420,708,34,6,C('#3D291C'),80,4)
D.rounded_rectangle(B(396,650,448,704), radius=X(8), fill=C('#C58A39'), outline=C('#654328'), width=Lw(1.4))
D.rectangle(B(405,672,439,696), fill=C('#F2E2C4'))
D.line(P([(409,679),(435,679)]), fill=C('#B56D48',180), width=Lw(1))
D.line(P([(409,686),(429,686)]), fill=C('#B56D48',120), width=Lw(1))
D.ellipse(B(400,655,444,669), fill=C('#D9A24F'))
D.rounded_rectangle(B(401,642,443,657), radius=X(3), fill=C('#8B623C'), outline=C('#563A25'), width=Lw(1.2))
D.line(P([(406,653),(406,694)]), fill=C('#F5CB80',120), width=Lw(3))
# honey dipper
D.line(P([(442,652),(464,628)]), fill=C('#8C623C'), width=Lw(3.4))
for i in range(4):
    D.ellipse(B(459+i*2,626-i*2,467+i*2,634-i*2), fill=C('#A97A49'), outline=C('#6B4A2E'), width=Lw(.7))

# --- vase with wildflowers ---
soft_ellipse(544,708,38,8,C('#3D291C'),70,5)
D.rounded_rectangle(B(516,638,570,704), radius=X(10), fill=C('#A4B2A1'), outline=C('#526051'), width=Lw(1.6))
D.rounded_rectangle(B(530,620,556,646), radius=X(5), fill=C('#9EAD9B'), outline=C('#526051'), width=Lw(1.4))
D.ellipse(B(530,616,556,626), fill=C('#C0CCB7'))
D.line(P([(522,650),(522,692)]), fill=C('#DCE4D3',110), width=Lw(3))
D.line(P([(524,664),(560,682)]), fill=C('#6C8371',120), width=Lw(1.2))
# stems and flowers
flowers=[(528,576,0),(512,548,-1),(548,556,1),(560,584,1),(500,588,-1),(540,592,0)]
for fx,fy,side in flowers:
    stem=[(543,624),(538,604),(fx+side*4, fy+30),(fx,fy)]
    smooth_line(stem,C('#5F7D52'),2.1,samples=10)
    # leaves
    D.ellipse(B(fx-11,fy+30,fx-2,fy+37), fill=C('#789264'))
    D.ellipse(B(fx+2,fy+42,fx+11,fy+49), fill=C('#678457'))
    # petals
    for k in range(5):
        a=math.radians(k*72+20)
        px=fx+math.cos(a)*6; py=fy+math.sin(a)*6
        D.ellipse(B(px-4,py-4,px+4,py+4), fill=C('#F3E8C8'), outline=C('#C8B57E'), width=Lw(.7))
    D.ellipse(B(fx-3,fy-3,fx+3,fy+3), fill=C('#D99B4A'))
# buds
for bx,by in [(566,548),(506,566)]:
    D.ellipse(B(bx-4,by-5,bx+4,by+5), fill=C('#E8C378'), outline=C('#957044'), width=Lw(.8))

# --- bread board ---
soft_ellipse(1025,715,118,16,C('#3D291C'),90,8)
D.rounded_rectangle(B(920,676,1122,717), radius=X(9), fill=C('#9C623D'), outline=C('#53351F'), width=Lw(2))
D.rounded_rectangle(B(928,681,1114,708), radius=X(6), fill=C('#B37B4F'))
D.ellipse(B(1088,688,1104,704), fill=C('#6C452D'))
D.ellipse(B(1090,690,1102,702), fill=C('#C99864'))
for i in range(4):
    D.line(P([(936,690+i*5),(1082,690+i*5)]), fill=C('#865332',80), width=Lw(.9))
# linen cloth under loaf
cloth_pts=[(950,664),(1000,660),(1078,668),(1100,708),(1082,716),(1048,706),(1010,717),(968,710),(944,684)]
D.polygon(P(cloth_pts), fill=C('#E8D8BD'), outline=C('#9A8264'), width=Lw(1.2))
D.line(P([(960,676),(1030,688),(1090,680)]), fill=C('#C9B18F',120), width=Lw(1.3))
# loaf
loaf=[(970,668),(976,646),(992,625),(1018,614),(1046,614),(1068,626),(1081,646),(1080,666),(1066,675),(1035,677),(997,674)]
D.polygon(P(catmull(loaf,closed=True,samples=12)), fill=C('#D69A5B'))
D.line(P(catmull(loaf,closed=True,samples=12)+[catmull(loaf,closed=True,samples=12)[0]]), fill=C('#7F4A2A'), width=Lw(2), joint='curve')
# crust top highlight
D.line(P([(984,633),(1006,621),(1038,619),(1060,627)]), fill=C('#F0BE7B',160), width=Lw(4))
D.line(P([(982,639),(1006,626),(1040,624),(1066,633)]), fill=C('#E7A968',110), width=Lw(2))
# scores
for sx,sy in [(1000,626),(1027,620),(1052,629)]:
    D.arc(B(sx-15,sy-8,sx+15,sy+12), 195, 330, fill=C('#8E5530'), width=Lw(2.2))
    D.arc(B(sx-14,sy-10,sx+14,sy+8), 195, 330, fill=C('#F1C58B',130), width=Lw(1))
# flour dust
for i in range(40):
    fx=random.uniform(975,1075); fy=random.uniform(615,670)
    if random.random()<.45:
        D.ellipse(B(fx-.9,fy-.9,fx+.9,fy+.9), fill=C('#F8E9CB',random.randint(45,110)))

# --- copper kettle ---
soft_ellipse(1220,710,86,17,C('#3D291C'),95,8)
# trivet
D.ellipse(B(1152,700,1290,716), fill=C('#4A392B'), outline=C('#2F241B'), width=Lw(1.4))
D.ellipse(B(1160,702,1282,713), fill=C('#6A5240'))
# body
body=[(1158,657),(1168,632),(1192,617),(1230,612),(1262,620),(1280,639),(1286,666),(1281,691),(1264,704),(1178,704),(1160,687)]
bpts=catmull(body,closed=True,samples=12)
D.polygon(P(bpts), fill=C('#BF7045'))
D.line(P(bpts+[bpts[0]]), fill=C('#5B3422'), width=Lw(2.2), joint='curve')
# shading
D.pieslice(B(1160,625,1290,720), 10, 160, fill=C('#9B5136'))
D.ellipse(B(1170,640,1250,695), fill=C('#C57A4C'))
D.ellipse(B(1176,648,1214,686), fill=C('#D68B59'))
# highlight crescent
D.arc(B(1172,630,1230,700), 115, 245, fill=C('#F5BD83'), width=Lw(7))
D.arc(B(1176,638,1216,690), 125, 235, fill=C('#FFE0B0'), width=Lw(2.5))
# top lid
D.ellipse(B(1190,610,1254,632), fill=C('#C77C4F'), outline=C('#5B3422'), width=Lw(2))
D.ellipse(B(1200,614,1244,628), fill=C('#A85C38'))
D.ellipse(B(1213,600,1231,617), fill=C('#BB6E44'), outline=C('#5B3422'), width=Lw(1.4))
D.ellipse(B(1217,603,1228,611), fill=C('#E9AC72'))
# handle
handle=catmull([(1193,614),(1186,585),(1200,566),(1222,562),(1244,568),(1254,586),(1249,614)],samples=14)
D.line(P(handle), fill=C('#3E3026'), width=Lw(9), joint='curve')
D.line(P(handle), fill=C('#7E6752'), width=Lw(3), joint='curve')
D.line(P([(1199,606),(1194,588),(1206,573),(1222,569)]), fill=C('#B39B7B',120), width=Lw(1.2))
# spout
D.polygon(P([(1166,648),(1144,626),(1134,616),(1132,625),(1146,640),(1160,662)]), fill=C('#B66A42'), outline=C('#5B3422'), width=Lw(1.5))
D.ellipse(B(1128,612,1142,628), fill=C('#6E402A'), outline=C('#4F3020'), width=Lw(1.2))
D.line(P([(1165,654),(1142,630)]), fill=C('#E8A46E',130), width=Lw(1.6))
# decorative seam
D.arc(B(1164,664,1282,708), 15, 165, fill=C('#7E422C',110), width=Lw(1.3))
D.arc(B(1170,682,1276,716), 15, 165, fill=C('#E9A56E',60), width=Lw(1))

# --- mugs ---
# saucer + cream mug
soft_ellipse(1349,706,38,7,C('#3D291C'),90,5)
D.ellipse(B(1312,694,1386,710), fill=C('#E6D4B7'), outline=C('#8D7355'), width=Lw(1.2))
D.rounded_rectangle(B(1324,646,1374,696), radius=X(6), fill=C('#F0E3CB'), outline=C('#6B4B34'), width=Lw(1.7))
D.ellipse(B(1322,640,1376,654), fill=C('#F7EBD6'), outline=C('#6B4B34'), width=Lw(1.4))
D.ellipse(B(1329,643,1369,651), fill=C('#6D452D'))
D.ellipse(B(1333,644,1365,650), fill=C('#8A5A38'))
D.arc(B(1370,655,1394,684), 270, 90, fill=C('#6B4B34'), width=Lw(4))
D.arc(B(1371,657,1391,681), 270, 90, fill=C('#E6D3B5'), width=Lw(2))
D.line(P([(1328,668),(1332,692)]), fill=C('#FAF0DD',150), width=Lw(3))
D.line(P([(1330,674),(1346,676)]), fill=C('#C56D4D',80), width=Lw(1))
# terracotta mug
soft_ellipse(1415,706,34,6,C('#3D291C'),80,4)
D.rounded_rectangle(B(1392,656,1440,704), radius=X(6), fill=C('#B86848'), outline=C('#5C3425'), width=Lw(1.7))
D.ellipse(B(1390,650,1442,664), fill=C('#C77B58'), outline=C('#5C3425'), width=Lw(1.4))
D.ellipse(B(1397,653,1435,661), fill=C('#6D452D'))
D.arc(B(1436,664,1460,692), 270, 90, fill=C('#5C3425'), width=Lw(4))
D.arc(B(1437,666,1457,690), 270, 90, fill=C('#C77B58'), width=Lw(2))
D.line(P([(1398,674),(1398,698)]), fill=C('#E59A73',110), width=Lw(3))
D.line(P([(1400,684),(1428,684)]), fill=C('#8F4A35',80), width=Lw(1))

# --- utensil crock ---
soft_ellipse(1518,708,47,9,C('#3D291C'),90,6)
# spoons first
for sx,topx,col in [(1496,1482,'#A87B4C'),(1514,1526,'#936638'),(1532,1552,'#B68A58')]:
    D.line(P([(sx,650),(topx,552)]), fill=C(col), width=Lw(5))
    D.ellipse(B(topx-10,546,topx+10,566), fill=C(col), outline=C('#6C4A2E'), width=Lw(1.2))
    D.ellipse(B(topx-5,550,topx+3,560), fill=C('#D3A874',100))
# whisk
D.line(P([(1546,648),(1564,570)]), fill=C('#8D8172'), width=Lw(3))
for off in (-9,0,9):
    D.arc(B(1550+off,564,1576+off,602), 70, 250, fill=C('#A49A89'), width=Lw(1.2))
D.ellipse(B(1567,560,1577,572), fill=C('#6A5E51'))
# crock
D.rounded_rectangle(B(1478,650,1560,704), radius=X(7), fill=C('#E7D6B8'), outline=C('#6B4B34'), width=Lw(1.7))
D.ellipse(B(1476,642,1562,660), fill=C('#F1E2C7'), outline=C('#6B4B34'), width=Lw(1.5))
D.ellipse(B(1484,646,1554,656), fill=C('#BEA37E'))
D.line(P([(1484,674),(1554,674)]), fill=C('#C17A58'), width=Lw(4))
D.line(P([(1484,678),(1554,678)]), fill=C('#E8B394'), width=Lw(1.2))
D.line(P([(1488,666),(1488,696)]), fill=C('#FBF1DD',110), width=Lw(3))

# --- sink towel ---
towel=[(792,848),(856,850),(866,902),(860,926),(846,918),(834,930),(820,920),(806,930),(796,916),(786,884)]
D.polygon(P(towel), fill=C('#EFE0C5'), outline=C('#8C6A4D'), width=Lw(1.5))
# stripes + waffle texture
for y in [858,868,906,916]:
    D.line(P([(794,y),(860,y+2)]), fill=C('#B86B4E',120), width=Lw(3))
for x in range(798,860,9):
    D.line(P([(x,853),(x-2,918)]), fill=C('#C9B18D',55), width=Lw(1))
D.line(P([(800,852),(800,914)]), fill=C('#FDF4E2',120), width=Lw(2))
D.line(P([(852,852),(858,918)]), fill=C('#927255',110), width=Lw(1.3))
# shadow behind towel
soft_poly([(788,854),(862,856),(864,928),(848,920),(832,932),(816,922),(800,932),(790,916)],C('#3D2B1E'),45,4)

# ============================================================
# SILL DETAILS (over window, behind counter)
# ============================================================
# little herb pot on sill
soft_ellipse(508,606,35,7,C('#3F2B1C'),80,4)
D.polygon(P([(480,570),(536,570),(529,610),(487,610)]), fill=C('#B86B4B'), outline=C('#6A3E2A'), width=Lw(1.6))
D.rectangle(B(476,562,540,576), fill=C('#C87A56'), outline=C('#6A3E2A'), width=Lw(1.4))
D.ellipse(B(482,566,534,575), fill=C('#4D3B2B'))
for i in range(12):
    ang=math.radians(-150+i*15)
    lx=508+math.cos(ang)*random.uniform(12,31)
    ly=563+math.sin(ang)*random.uniform(10,29)
    D.ellipse(B(lx-7,ly-4,lx+7,ly+4), fill=C(['#708954','#869C62','#5D7648'][i%3]))
# small jug on right sill
D.rounded_rectangle(B(1036,566,1080,612), radius=X(8), fill=C('#8D9A86'), outline=C('#4D5A4B'), width=Lw(1.4))
D.rounded_rectangle(B(1048,552,1068,572), radius=X(4), fill=C('#8D9A86'), outline=C('#4D5A4B'), width=Lw(1.2))
D.line(P([(1042,580),(1042,604)]), fill=C('#C4CEBA',110), width=Lw(3))
for i in range(4):
    D.line(P([(1052,556),(1048+i*7,528)]), fill=C('#7A8F5D'), width=Lw(1.4))
    D.ellipse(B(1044+i*7-3,523,1044+i*7+3,532), fill=C('#A9B47A'))

# ============================================================
# RUG, CAT, SLIPPERS
# ============================================================
# rug shadow
soft_ellipse(1020,1130,360,120,C('#3A271B'),80,22)
# rug mask
rug_layer=newlayer(); rl=ImageDraw.Draw(rug_layer)
rug_bbox=B(700,1006,1350,1260)
rl.ellipse(rug_bbox, fill=C('#9C5C42'))
# braided rings
ring_cols=[('#C88A62',10),('#7F4D38',3),('#DCC59B',9),('#8A8A61',3),('#B36A4D',10),('#E3CFA9',4),('#9A7B57',8),('#C07658',3)]
for i,(col,wd) in enumerate(ring_cols):
    inset=8+i*13
    rl.ellipse((rug_bbox[0]+X(inset),rug_bbox[1]+X(inset*0.9),rug_bbox[2]-X(inset),rug_bbox[3]-X(inset*0.9)),
               outline=C(col), width=Lw(wd))
# inner field
rl.ellipse((rug_bbox[0]+X(112),rug_bbox[1]+X(88),rug_bbox[2]-X(112),rug_bbox[3]-X(88)), fill=C('#CE9A6F'))
rl.ellipse((rug_bbox[0]+X(128),rug_bbox[1]+X(106),rug_bbox[2]-X(128),rug_bbox[3]-X(106)), outline=C('#996B4E',120), width=Lw(2))
# stitch marks
for i in range(180):
    ang=random.uniform(0,2*math.pi)
    rr=random.uniform(.34,.98)
    ex=1025+math.cos(ang)*318*rr; ey=1133+math.sin(ang)*126*rr
    rl.line(P([(ex,ey),(ex+math.cos(ang+1.3)*7,ey+math.sin(ang+1.3)*7)]), fill=C('#6E4934',45), width=Lw(.8))
# clip rug to floor-ish oval already; composite
comp(rug_layer)
# soft sunlight wash on rug
soft_poly([(760,1020),(1110,1016),(1240,1200),(700,1200)], C('#FFDCA3'), 35, 18)

# cat curled on rug
# soft floor cushion beneath the cat
soft_ellipse(1142,1164,168,58,C('#3B2A1D'),85,10)
D.ellipse(B(1004,1060,1272,1192), fill=C('#58727C'), outline=C('#354B53'), width=Lw(2.4))
D.ellipse(B(1014,1052,1262,1178), fill=C('#738D97'), outline=C('#4C6670'), width=Lw(1.5))
D.ellipse(B(1024,1062,1252,1172), outline=C('#93A8AC'), width=Lw(2))
# top light and plush folds
light=newlayer(); ld2=ImageDraw.Draw(light)
ld2.ellipse(B(1040,1058,1214,1130), fill=C('#A9BABD',55))
ld2.arc(B(1028,1074,1248,1168), 200, 320, fill=C('#F1E5CE',65), width=Lw(3))
for pts in [[(1040,1122),(1090,1138),(1142,1136),(1198,1150),(1242,1138)],
            [(1060,1088),(1110,1102),(1158,1096),(1212,1106)],
            [(1072,1158),(1112,1148),(1162,1160),(1206,1148)]]:
    D.line(P(catmull(pts,samples=10)), fill=C('#4E6871',100), width=Lw(1.4), joint='curve')
# plump front lip of the cushion
D.arc(B(1008,1092,1268,1200), 18, 162, fill=C('#4D6871'), width=Lw(9))
D.arc(B(1012,1094,1264,1196), 18, 162, fill=C('#8FA3A7',90), width=Lw(2))
D.arc(B(1024,1082,1252,1188), 20, 160, fill=C('#D9C6A7',45), width=Lw(3))
# tufted buttons
for bx,by in [(1082,1106),(1142,1098),(1202,1112),(1108,1148),(1176,1152)]:
    D.ellipse(B(bx-4,by-4,bx+4,by+4), fill=C('#4C636B'), outline=C('#8FA5A9'), width=Lw(1))
    D.line(P([(bx-6,by),(bx+6,by)]), fill=C('#96ABAD',110), width=Lw(1))
    D.line(P([(bx,by-6),(bx,by+6)]), fill=C('#96ABAD',110), width=Lw(1))
cat_shadow=soft_ellipse(1138,1160,112,42,C('#4A2A18'),80,8)
# body
body_pts=[(1052,1102),(1060,1070),(1088,1048),(1128,1042),(1170,1050),(1202,1070),(1216,1102),(1208,1138),(1184,1158),(1148,1165),(1108,1158),(1074,1140),(1054,1120)]
bp=catmull(body_pts,closed=True,samples=12)
D.polygon(P(bp), fill=C('#D98648'))
D.line(P(bp+[bp[0]]), fill=C('#7D4A2A'), width=Lw(2.2), joint='curve')
# shaded flank
D.pieslice(B(1080,1044,1220,1168), 305, 130, fill=C('#C4713C'))
D.pieslice(B(1070,1050,1190,1158), 300, 115, fill=C('#D9894B'))
# belly/chest cream
D.ellipse(B(1074,1078,1140,1148), fill=C('#EFD5A8'))
D.arc(B(1072,1078,1140,1150), 80, 280, fill=C('#C39B69'), width=Lw(1.2))
# head
D.ellipse(B(1040,1056,1130,1146), fill=C('#E09151'), outline=C('#7D4A2A'), width=Lw(2.2))
# ears
D.polygon(P([(1046,1074),(1044,1040),(1074,1058)]), fill=C('#D98648'), outline=C('#7D4A2A'), width=Lw(1.3))
D.polygon(P([(1094,1052),(1117,1035),(1118,1071)]), fill=C('#D98648'), outline=C('#7D4A2A'), width=Lw(1.3))
D.polygon(P([(1051,1068),(1050,1048),(1067,1060)]), fill=C('#E4A17C'))
D.polygon(P([(1101,1055),(1113,1045),(1114,1065)]), fill=C('#E4A17C'))
# muzzle / cheeks
D.ellipse(B(1046,1100,1090,1136), fill=C('#F1D9AE'))
D.ellipse(B(1080,1096,1126,1136), fill=C('#F1D9AE'))
D.arc(B(1044,1098,1090,1138), 100, 260, fill=C('#CA9E6A'), width=Lw(1))
# face stripes
for sx,sy,ex,ey in [(1060,1056,1056,1074),(1080,1052,1080,1072),(1100,1058,1104,1074)]:
    D.line(P([(sx,sy),(ex,ey)]), fill=C('#A85D31'), width=Lw(3))
D.line(P([(1052,1068),(1058,1062)]), fill=C('#A85D31'), width=Lw(2))
D.line(P([(1104,1062),(1110,1068)]), fill=C('#A85D31'), width=Lw(2))
# closed eyes
D.arc(B(1056,1088,1076,1102), 15, 165, fill=C('#5A3421'), width=Lw(2))
D.arc(B(1088,1088,1108,1102), 15, 165, fill=C('#5A3421'), width=Lw(2))
# nose + mouth
D.polygon(P([(1076,1102),(1084,1102),(1080,1108)]), fill=C('#C76E65'))
D.line(P([(1080,1108),(1080,1114),(1074,1117)]), fill=C('#7A4A31'), width=Lw(1.2))
D.line(P([(1080,1114),(1086,1117)]), fill=C('#7A4A31'), width=Lw(1.2))
# whiskers
for dy in (-5,2,8):
    D.line(P([(1060,1110+dy),(1032,1104+dy*1.4)]), fill=C('#F8E7C7',150), width=Lw(.9))
    D.line(P([(1102,1110+dy),(1130,1102+dy*1.4)]), fill=C('#F8E7C7',150), width=Lw(.9))
# front paw
D.ellipse(B(1084,1128,1130,1154), fill=C('#EFD2A2'), outline=C('#7D4A2A'), width=Lw(1.3))
for i in range(3):
    D.arc(B(1090+i*10,1134,1100+i*10,1146), 300, 80, fill=C('#B88B5E'), width=Lw(1))
# tail curled around
tail=catmull([(1198,1133),(1214,1149),(1200,1165),(1164,1171),(1128,1168),(1102,1160)],samples=14)
D.line(P(tail), fill=C('#D98648'), width=Lw(14), joint='curve')
D.line(P(tail), fill=C('#B96535'), width=Lw(3), joint='curve')
for i in range(4):
    p=tail[6+i*6]
    D.line(P([(p[0]-7,p[1]-7),(p[0]+7,p[1]+7)]), fill=C('#A85A30'), width=Lw(5))
# back stripes
for i in range(5):
    sx=1110+i*17
    D.arc(B(sx,1044,sx+30,1088), 200, 330, fill=C('#B96535'), width=Lw(3.2))
# rim light from window
rim=catmull([(1070,1050),(1100,1041),(1140,1042),(1172,1051),(1200,1068),(1210,1086)],samples=14)
D.line(P(rim), fill=C('#FFD394',170), width=Lw(2.4), joint='curve')
D.arc(B(1044,1058,1128,1144), 190, 300, fill=C('#FFD394',120), width=Lw(2))

# wooden stool with a folded morning throw
soft_poly([(110,1128),(312,1128),(360,1180),(120,1180)], C('#3B281B'),65,12)
# rear leg
D.polygon(P([(202,1028),(216,1028),(224,1114),(212,1118)]), fill=C('#5C3B27'), outline=C('#3D281A'), width=Lw(1.2))
# rungs
D.line(P([(140,1082),(286,1094)]), fill=C('#6A462E'), width=Lw(6))
D.line(P([(140,1080),(286,1092)]), fill=C('#9A6B46'), width=Lw(2))
# front legs
D.polygon(P([(150,1032),(166,1033),(142,1132),(124,1136)]), fill=C('#7E5436'), outline=C('#4A3020'), width=Lw(1.8))
D.polygon(P([(262,1032),(280,1032),(304,1140),(286,1144)]), fill=C('#6C472F'), outline=C('#4A3020'), width=Lw(1.8))
D.line(P([(156,1040),(138,1128)]), fill=C('#A4744C',120), width=Lw(2))
D.line(P([(270,1042),(290,1132)]), fill=C('#9A6C47',105), width=Lw(2))
# seat
D.ellipse(B(128,1002,304,1044), fill=C('#A67249'), outline=C('#4A3020'), width=Lw(2.2))
D.ellipse(B(138,1006,294,1036), fill=C('#C08C5C'))
D.arc(B(136,1004,296,1040), 190, 320, fill=C('#E0AC79',120), width=Lw(2.4))
D.rounded_rectangle(B(140,1028,292,1048), radius=X(8), fill=C('#8C5B39'), outline=C('#4A3020'), width=Lw(1.5))
# soft folded blanket on the stool seat
soft_ellipse(214,1036,84,13,C('#3E2A1C'),45,5)
blue=[(148,1021),(166,1008),(238,1000),(274,1012),(281,1031),(264,1045),(190,1054),(153,1042)]
D.polygon(P(catmull(blue,closed=True,samples=12)), fill=C('#536E76'), outline=C('#3B535B'), width=Lw(1.4))
D.arc(B(158,1008,268,1048), 195, 340, fill=C('#718A90',90), width=Lw(2))
cream=[(156,1015),(178,1002),(238,996),(266,1007),(269,1024),(252,1038),(179,1046),(154,1033)]
D.polygon(P(catmull(cream,closed=True,samples=12)), fill=C('#EBD9BB'), outline=C('#886848'), width=Lw(1.3))
D.polygon(P([(178,1034),(250,1027),(259,1039),(183,1047)]), fill=C('#D7BE99'))
D.line(P([(165,1018),(235,1002),(259,1012)]), fill=C('#B56B4E',130), width=Lw(3))
D.line(P([(166,1024),(238,1008),(264,1018)]), fill=C('#869A9D',130), width=Lw(2))
D.line(P([(170,1030),(245,1013),(267,1024)]), fill=C('#C28A63',90), width=Lw(1.6))
D.line(P([(158,1032),(238,1031),(266,1033)]), fill=C('#C7A882',80), width=Lw(1.2))
D.arc(B(176,1028,260,1052), 195, 345, fill=C('#F4E6CC',120), width=Lw(2.2))
# a short folded end softening over the seat edge
D.polygon(P([(252,1022),(272,1030),(277,1046),(270,1056),(259,1050),(250,1036),(246,1028)]), fill=C('#E8D5B5'), outline=C('#806143'), width=Lw(1.1))
D.line(P([(253,1032),(271,1038)]), fill=C('#B36A4D',110), width=Lw(2.2))
D.line(P([(255,1042),(272,1046)]), fill=C('#819699',85), width=Lw(1.4))
D.line(P([(255,1034),(263,1032)]), fill=C('#F8EBD4',90), width=Lw(1.2))

# worn leather slippers by the stool
soft_ellipse(392,1180,128,24,C('#3D291C'),80,10)

def draw_slipper(x,y,leather,lining,front=False):
    # y is the top of the heel; body extends right
    sole=[(x,y+16),(x+8,y+28),(x+44,y+33),(x+88,y+31),(x+108,y+22),(x+104,y+11),(x+66,y+4),(x+24,y+6)]
    D.polygon(P(catmull(sole,closed=True,samples=12)), fill=C('#4B3120'))
    D.line(P(catmull(sole,closed=True,samples=12)+[catmull(sole,closed=True,samples=12)[0]]), fill=C('#3C271A'), width=Lw(1.3))
    # sole rim
    D.arc(B(x+8,y+20,x+108,y+36), 15, 165, fill=C('#A8774E'), width=Lw(2))
    # upper
    upper=[(x+4,y+16),(x+12,y+2),(x+40,y-7),(x+74,y-4),(x+98,y+7),(x+102,y+15),(x+88,y+22),(x+48,y+24),(x+14,y+22)]
    D.polygon(P(catmull(upper,closed=True,samples=12)), fill=C(leather), outline=C('#4B3120'), width=Lw(1.9))
    # heel opening with a deep, cosy cuff
    D.ellipse(B(x+76,y+2,x+104,y+18), fill=C(lining), outline=C('#6A4A32'), width=Lw(1.2))
    D.ellipse(B(x+79,y+7,x+101,y+16), fill=C('#B68E62'))
    D.arc(B(x+72,y-2,x+108,y+19), 178, 358, fill=C('#F5E6C9'), width=Lw(4.2))
    D.arc(B(x+74,y,x+106,y+18), 185, 350, fill=C('#FFF6E4'), width=Lw(1.4))
    D.arc(B(x+77,y-1,x+104,y+13), 195, 345, fill=C('#F7E8CD'), width=Lw(2.6))
    # toe highlight and stitching
    D.arc(B(x+10,y,x+60,y+28), 185, 305, fill=C('#D6A070',110), width=Lw(2.4))
    D.line(P([(x+18,y+15),(x+42,y+8),(x+66,y+9)]), fill=C('#C08C60',110), width=Lw(1.2))
    for i in range(4):
        sx=x+26+i*10; sy=y+21
        D.arc(B(sx-4,sy-2,sx+4,sy+2), 200, 340, fill=C('#6E4A30'), width=Lw(.9))
    if front:
        # little stitched leaf on the vamp
        D.line(P([(x+38,y+13),(x+50,y+4)]), fill=C('#7C5839'), width=Lw(1))
        D.ellipse(B(x+46,y+1,x+54,y+7), fill=C('#8E6B49'))
        D.ellipse(B(x+42,y+5,x+49,y+10), fill=C('#8E6B49'))

# back slipper
draw_slipper(300,1118,'#9A6744','#E8D0A6')
# front slipper, angled slightly and overlapping
draw_slipper(352,1140,'#865435','#EBD7B4',True)
# tiny floor shadows at contacts
soft_ellipse(350,1165,74,8,C('#3B281B'),65,4)
soft_ellipse(414,1188,76,7,C('#3B281B'),55,4)

# ============================================================
# LIGHT: beams, motes, steam
# ============================================================
# broad window haze and morning shafts
soft_ellipse(772,336,592,420,C('#FFD79A'),20,70)
beam=newlayer(); bd=ImageDraw.Draw(beam)
bd.polygon(P([(500,126),(672,126),(350,1200),(60,1200)]), fill=C('#FFDFA4',27))
bd.polygon(P([(668,126),(800,126),(610,1200),(330,1200)]), fill=C('#FFE6B4',22))
bd.polygon(P([(900,126),(1014,126),(1010,1200),(700,1200)]), fill=C('#FFE9BB',16))
bd.polygon(P([(560,126),(610,126),(250,1200),(160,1200)]), fill=C('#FFF0CC',10))
comp(beam, blur=25)

# projected window panes on the counter
pane=newlayer(); pd=ImageDraw.Draw(pane)
pd.polygon(P([(742,682),(864,682),(898,756),(764,756)]), fill=C('#FFE7B3',52))
pd.polygon(P([(878,682),(1000,682),(1048,756),(914,756)]), fill=C('#FFE7B3',43))
pd.polygon(P([(1014,682),(1090,682),(1148,756),(1064,756)]), fill=C('#FFE7B3',30))
pd.polygon(P([(866,682),(880,682),(916,756),(900,756)]), fill=C('#7A5638',22))
comp(pane, blur=4.5)

# sun pooling on the floor, with pane-shaped bands
floor_light=newlayer(); fd2=ImageDraw.Draw(floor_light)
fd2.polygon(P([(250,978),(820,978),(1070,1200),(330,1200)]), fill=C('#FFD79B',36))
for x0,w in [(340,120),(480,120),(620,120),(760,120)]:
    fd2.polygon(P([(x0,978),(x0+w,978),(x0+w+190,1200),(x0+120,1200)]), fill=C('#FFE4B2',20))
comp(floor_light, blur=18)
# sunbeam falling across the rug and cat
soft_poly([(720,1040),(1010,1004),(1210,1174),(880,1200)], C('#FFD99F'), 22, 15)
soft_poly([(1040,1044),(1130,1036),(1210,1090),(1110,1104)], C('#FFE6B7'), 24, 10)

# steam from the kettle
steam=newlayer(); sd=ImageDraw.Draw(steam)
for k in range(2):
    pts=[(1137+k*7,614),(1128+k*9,590),(1137+k*8,564),(1152+k*10,540),
         (1143+k*12,516),(1125+k*13,494),(1130+k*11,470),(1144+k*9,450)]
    pts=catmull(pts,samples=16)
    sd.line(P(pts), fill=C('#FFF8E5',40), width=Lw(12-k*2), joint='curve')
    sd.line(P(pts), fill=C('#FFFDF3',82-k*12), width=Lw(5.5-k), joint='curve')
    sd.line(P(pts), fill=C('#FFFFFF',130-k*22), width=Lw(1.8), joint='curve')
    for i in (3,7,11,15):
        px,py=pts[i]
        sd.ellipse(B(px-9-k*2,py-7,px+9+k*2,py+7), fill=C('#FFF9E8',25))
# steam from the cream mug
for k in range(2):
    pts=catmull([(1344+k*7,636),(1336+k*8,618),(1347+k*7,600),(1340+k*8,580),(1349+k*7,558),(1343+k*6,540)],samples=14)
    sd.line(P(pts), fill=C('#FFF8E5',35), width=Lw(8), joint='curve')
    sd.line(P(pts), fill=C('#FFFDF3',72-k*18), width=Lw(3.8-k*.7), joint='curve')
comp(steam, blur=3.2)
comp(steam, blur=12)

# dust motes floating in the sun
motes=newlayer(); md2=ImageDraw.Draw(motes)
for i in range(78):
    x=random.uniform(380,1150); y=random.uniform(260,1080)
    r=random.uniform(.8,3.8)
    a=random.randint(35,135)
    md2.ellipse(B(x-r,y-r,x+r,y+r), fill=C('#FFEBC2',a))
for x,y,r in [(892,470,8),(764,692,6),(620,862,9),(1012,610,7),(520,930,5),(1110,760,4),(970,1110,5)]:
    md2.ellipse(B(x-r,y-r,x+r,y+r), fill=C('#FFE7B0',20))
comp(motes, blur=1.2)
for x,y,r in [(892,470,6),(764,692,4),(620,862,7)]:
    D.ellipse(B(x-r,y-r,x+r,y+r), outline=C('#FFE9BA',35), width=Lw(1.2))

# ============================================================
# FINAL GRADE
# ============================================================
# warm color wash
warm=Image.new('RGBA',(CW,CH),C('#F6B96B',12))
canvas.alpha_composite(warm)

# vignette generated small
vw,vh=400,300
vig=Image.new('L',(vw,vh),0)
vpix=vig.load()
for y in range(vh):
    for x in range(vw):
        nx=(x-vw/2)/(vw/2); ny=(y-vh/2)/(vh/2)
        d=math.sqrt(nx*nx*0.78+ny*ny*0.82)
        val=max(0,min(1,(d-0.42)/0.75))
        vpix[x,y]=int((val**1.5)*135)
vig=vig.resize((CW,CH),Image.LANCZOS)
vig_rgba=Image.new('RGBA',(CW,CH),C('#2C1E15'))
vig_rgba.putalpha(vig)
canvas.alpha_composite(vig_rgba)

# subtle paper grain
noise=Image.effect_noise((CW,CH),20).convert('L')
noise_rgb=Image.merge('RGB',(noise,noise,noise)).convert('RGBA')
noise_rgb.putalpha(11)
canvas.alpha_composite(noise_rgb)
# larger soft mottling
small=Image.effect_noise((400,300),36).filter(ImageFilter.GaussianBlur(1.4))
small=small.resize((CW,CH),Image.LANCZOS).convert('L')
tint=Image.new('RGBA',(CW,CH),C('#8F6A4B'))
tint.putalpha(small.point(lambda v:int(v*0.045)))
canvas.alpha_composite(tint)

# final downscale + slight sharpen
out=canvas.convert('RGB').resize((W,H),Image.LANCZOS)
out=out.filter(ImageFilter.UnsharpMask(radius=1.25, percent=75, threshold=3))

# gentle morning bloom from the window and bright copper
lum=out.convert('L')
bright=lum.point(lambda v: max(0,int((v-198)*2.0)))
blurred=out.filter(ImageFilter.GaussianBlur(16))
bloom=Image.composite(blurred,Image.new('RGB',(W,H),(0,0,0)),bright)
bloom=ImageEnhance.Brightness(bloom).enhance(.62)
out=ImageChops.screen(out,bloom)

# cool shadows and warm highlights (split toning)
gray=out.convert('L')
shadow_mask=gray.point(lambda v:int(max(0,(142-v))/142*52))
cool=Image.new('RGB',(W,H),(48,63,72))
coolblend=Image.blend(out,cool,.20)
out=Image.composite(coolblend,out,shadow_mask)
gray=out.convert('L')
hi_mask=gray.point(lambda v:int(max(0,(v-194))/.60*34))
warm=Image.new('RGB',(W,H),(255,221,170))
warmblend=Image.blend(out,warm,.15)
out=Image.composite(warmblend,out,hi_mask)

out=ImageEnhance.Contrast(out).enhance(1.075)
out=ImageEnhance.Color(out).enhance(1.06)
out=ImageEnhance.Brightness(out).enhance(1.002)
vv=Image.new('L',(400,300),0)
vp=vv.load()
for yy in range(300):
    for xx in range(400):
        nx=(xx-200)/200; ny=(yy-150)/150
        dd=math.sqrt(nx*nx*.82+ny*ny*.88)
        vp[xx,yy]=int(max(0,min(1,(dd-.48)/.68))**1.4*95)
vv=vv.resize((W,H),Image.LANCZOS)
veil=Image.new('RGBA',(W,H),C('#261C14'))
veil.putalpha(vv)
out=Image.alpha_composite(out.convert('RGBA'),veil).convert('RGB')
out=out.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2))
out.save('/tmp/vellery-bmuf3gwh/work/art/cozy-kitchen-morning.png')
out.save('/tmp/vellery-bmuf3gwh/work/art/cozy-kitchen-morning.jpg',quality=94)
print('saved',out.size)
