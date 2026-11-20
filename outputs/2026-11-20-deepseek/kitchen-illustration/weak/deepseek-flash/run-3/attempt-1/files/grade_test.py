from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import math

src = Image.open('cozy-kitchen.png').convert('RGB')
W,H = src.size

def make_lut(gamma, lift=0, gain=1.0):
    return [max(0,min(255,round((((i/255.0)**gamma)*gain + lift/255.0)*255))) for i in range(256)]

def grade(src, bloom_amt=0.3, vignette_amt=0.95, texture_amt=0.14, warm_amt=0.7):
    img = ImageEnhance.Color(src).enhance(1.10)
    img = ImageEnhance.Contrast(img).enhance(1.055)
    r,g,b=img.split()
    img=Image.merge('RGB',(r.point(make_lut(0.955,2,1.035)),g.point(make_lut(0.98,1,1.0)),b.point(make_lut(1.04,0,0.97))))

    lum=img.convert('L')
    mask=lum.point(lambda p: max(0,min(255,int((p-192)*3.2))))
    black=Image.new('RGB',(W,H),(0,0,0))
    bloom=Image.composite(img.filter(ImageFilter.GaussianBlur(34)),black,mask)
    img=ImageChops.screen(img, Image.eval(bloom, lambda x:int(x*bloom_amt)))

    # warm glow from the window corner
    small=(400,275); glow=Image.new('L',small,0); p=glow.load()
    for y in range(275):
        for x in range(400):
            dx=(x-100)/270; dy=(y-75)/220
            d=math.sqrt(dx*dx+dy*dy)
            p[x,y]=int(70*max(0,1-d)**2)
    glow=glow.resize((W,H),Image.LANCZOS)
    warm=Image.new('RGB',(W,H),(255,190,112))
    img=ImageChops.screen(img,Image.composite(warm,black,glow))

    # paper grain / canvas
    noise=Image.effect_noise((W,H),24).convert('L').filter(ImageFilter.GaussianBlur(1.0))
    noise_rgb=Image.merge('RGB',(noise,noise,noise))
    soft=ImageChops.soft_light(img,noise_rgb)
    img=Image.blend(img,soft,texture_amt)

    # vignette
    small=(320,220); grad=Image.new('L',small,0); p=grad.load()
    for y in range(220):
        for x in range(320):
            dx=(x-160)/160; dy=(y-110)/110
            rr=math.sqrt(dx*dx+dy*dy)
            v=max(0,min(1,(rr-0.6)/0.5))
            p[x,y]=int(120*v*v)
    grad=grad.resize((W,H),Image.LANCZOS)
    shade=Image.new('RGB',(W,H),(47,29,23))
    vig=Image.composite(shade,Image.new('RGB',(W,H),(255,255,255)),grad)
    if vignette_amt != 1.0:
        # lighten the shade toward white to reduce strength
        vig=Image.blend(Image.new('RGB',(W,H),(255,255,255)), vig, vignette_amt)
    img=ImageChops.multiply(img,vig)

    grain=Image.effect_noise((W,H),11).convert('L')
    grain_rgb=Image.merge('RGB',(grain,grain,grain))
    img=Image.blend(img,ImageChops.overlay(img,grain_rgb),0.04)
    img=img.filter(ImageFilter.UnsharpMask(radius=2.0,percent=55,threshold=2))
    return img

im=grade(src,0.3,0.9,0.14)
im.resize((2000,1375),Image.LANCZOS).save('graded2-preview.png')
im.save('graded2.png')
print('done')
