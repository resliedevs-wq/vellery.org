from PIL import Image, ImageDraw
import math
import re

S = 3
W, H = 900, 800
paper = '#F8F2E5'
ink = '#253D42'
im = Image.new('RGB', (W*S, H*S), paper)
d = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', '<title>A pelican riding a turquoise bicycle</title>', f'<rect width="900" height="800" fill="{paper}"/>']

def path(data, fill=None, stroke=ink, width=4):
    svg.append(f'<path d="{data}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
    tokens = re.findall(r'[MLCQZ]|-?\d+(?:\.\d+)?', data)
    i, points, last, start = 0, [], (0, 0), (0, 0)
    while i < len(tokens):
        c = tokens[i]; i += 1
        n = {'M':2, 'L':2, 'C':6, 'Q':4, 'Z':0}[c]
        a = list(map(float, tokens[i:i+n])); i += n
        if c in ('M', 'L'):
            last = tuple(a); points.append(last)
            if c == 'M': start = last
        elif c == 'Z':
            points.append(start); last = start
        else:
            p0 = last
            for k in range(1, 51):
                t = k/50; u = 1-t
                if c == 'C':
                    p = (u**3*p0[0]+3*u*u*t*a[0]+3*u*t*t*a[2]+t**3*a[4], u**3*p0[1]+3*u*u*t*a[1]+3*u*t*t*a[3]+t**3*a[5])
                else:
                    p = (u*u*p0[0]+2*u*t*a[0]+t*t*a[2], u*u*p0[1]+2*u*t*a[1]+t*t*a[3])
                points.append(p)
            last = p
    pts = [(round(x*S), round(y*S)) for x,y in points]
    if fill: d.polygon(pts, fill=fill)
    if stroke and width:
        d.line(pts, fill=stroke, width=round(width*S), joint='curve')
        r = width*S/2
        for x,y in (pts[0], pts[-1]): d.ellipse((x-r,y-r,x+r,y+r), fill=stroke)

def ellipse(x,y,rx,ry,fill,stroke=None,width=3):
    svg.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{width}"/>')
    box = ((x-rx)*S,(y-ry)*S,(x+rx)*S,(y+ry)*S)
    d.ellipse(box, fill=fill, outline=stroke, width=round(width*S))

def line(x1,y1,x2,y2,color=ink,width=4):
    path(f'M {x1} {y1} L {x2} {y2}', stroke=color, width=width)

# A warm, quiet day by the seaside.
ellipse(660,180,61,61,'#F2CD74')
path('M 147 218 C 158 192 184 194 195 212 C 213 203 233 211 239 227 L 132 227', '#FFFDF5', None)
path('M 659 325 C 668 303 689 303 699 319 C 712 309 734 316 735 329 L 646 329', '#FFFDF5', None)
path('M 158 342 Q 174 331 189 341 M 125 367 Q 140 356 153 366', stroke='#BBC9C0', width=3)
ellipse(438,689,271,15,'#E6E4D5')
line(125,686,756,686,'#D0D7C5',3)
line(174,701,205,701,'#D0D7C5',3)
line(690,701,733,701,'#D0D7C5',3)

# The far pedal and leg.
path('M 350 413 L 324 464 L 372 530', stroke='#DDA155', width=16)
path('M 367 521 Q 384 517 398 534 L 358 537 Z', '#F3BC65', ink,3)
line(369,533,402,533,ink,7)

# Bicycle wheels, cream sidewalls, and fine spokes.
for x in (257,582):
    ellipse(x,574,108,108,'#F8F2E5',ink,9)
    ellipse(x,574,96,96,None,'#D2BFA1',3)
    for j in range(12):
        a=2*math.pi*j/12
        line(x,574,x+93*math.cos(a),574+93*math.sin(a),'#B9C6BF',1.5)
    ellipse(x,574,10,10,'#D5D9CB',ink,3)

# A classic turquoise diamond frame.
teal='#3C9A96'
path('M 257 574 L 341 457 L 429 574 Z', stroke=ink,width=12)
path('M 341 457 L 506 457 L 429 574', stroke=ink,width=12)
path('M 257 574 L 341 457 L 429 574 Z', stroke=teal,width=7)
path('M 341 457 L 506 457 L 429 574', stroke=teal,width=7)
path('M 582 574 L 501 439 L 492 404 L 525 394',stroke=ink,width=12)
path('M 582 574 L 501 439 L 492 404',stroke=teal,width=7)
path('M 488 405 L 519 395 Q 535 392 539 406',stroke=ink,width=7)
path('M 524 395 Q 535 393 539 406',stroke='#B37351',width=9)
line(341,457,333,432,ink,8)
path('M 304 428 Q 328 420 362 428 Q 368 436 353 438 L 313 438 Q 302 438 304 428 Z','#AA6D4C',ink,4)
path('M 268 565 L 425 558 Q 450 558 449 577 Q 449 592 429 591 L 268 583 Q 255 580 268 565 Z',None,'#748C82',3)
ellipse(429,574,19,19,'#DFDDC7',ink,4)
line(429,574,456,537,ink,5)
line(443,537,472,537,ink,7)

# The near leg ends in a very determined webbed foot.
path('M 389 419 Q 407 439 393 463 L 374 482 L 438 529',stroke=ink,width=19)
path('M 389 419 Q 407 439 393 463 L 374 482 L 438 529',stroke='#F3BC65',width=12)
path('M 434 519 Q 444 516 450 523 L 474 534 Q 457 540 431 533 Z','#F3BC65',ink,3)
line(445,528,456,532,'#C89148',2)

# Tail, round body, and the long curling pelican neck.
path('M 299 371 Q 257 378 227 342 Q 256 345 271 336 Q 236 319 238 299 Q 267 320 305 319 Z','#FFFDF6',ink,4)
path('M 286 326 C 328 306 367 321 393 337 C 424 354 440 352 443 321 C 446 292 430 268 444 237 C 454 209 486 201 510 215 C 536 231 537 255 518 273 C 502 287 498 305 500 337 C 502 385 480 415 440 433 C 409 448 365 448 326 428 C 285 408 269 360 286 326 Z','#FFFDF6',ink,4.5)
# Cool shadows on the belly and folded wing.
path('M 295 379 C 332 420 392 439 440 420 C 466 409 486 390 495 368 C 486 401 467 420 439 433 C 397 453 334 440 309 410 Z','#E4E9DF',None)
path('M 300 339 C 335 322 389 348 414 397 C 392 411 349 404 320 384 C 306 373 300 356 300 339 Z','#E9EDE3',ink,3.5)
path('M 318 350 Q 352 356 380 384 M 315 364 Q 342 385 367 389',stroke='#ABBEB4',width=2.5)

# Wing tip reaches the handlebars.
path('M 423 350 C 447 360 455 383 477 390 L 510 391 Q 520 395 510 403 C 468 415 442 396 426 385', '#FFFDF6',ink,4)
path('M 481 394 Q 497 399 510 397',stroke='#ABBEB4',width=2)

# A bright little scarf flutters behind the bird.
path('M 443 286 Q 469 299 499 288 L 499 306 Q 465 314 443 301 Z','#D96850',ink,3)
path('M 445 298 C 411 292 402 271 374 277 L 384 292 L 373 300 C 401 296 412 321 448 306 Z','#E98466',ink,3)
line(387,284,404,291,'#F5B39A',2)

# The unmistakable enormous bill and curved orange throat pouch.
path('M 510 244 L 710 264 C 700 298 658 327 612 319 C 570 312 540 285 510 269 Z','#EBA063',ink,4)
path('M 510 240 C 560 239 646 248 715 260 Q 727 263 712 270 L 512 262 Z','#F5C66B',ink,4)
path('M 542 275 Q 615 322 674 292',stroke='#CA7C51',width=2.5)
line(527,251,695,263,'#FFE0A0',2)
ellipse(493,239,6.5,7.5,ink)
ellipse(495,236.5,1.8,2,'#FFFDF6')
path('M 480 223 Q 491 217 503 222',stroke=ink,width=3)
ellipse(491,260,9,5,'#E9B5A0')
# A small jaunty crest.
path('M 457 219 Q 447 203 453 194 M 467 215 Q 466 196 475 190 M 478 213 Q 485 198 492 198',stroke=ink,width=3.5)

# Roadside details and a few movement marks.
path('M 734 684 Q 730 666 720 660 M 735 684 Q 741 662 751 656 M 735 684 L 735 655',stroke='#819A7E',width=3)
ellipse(735,650,4,4,'#DFA66B')
path('M 174 474 L 211 474 M 153 491 L 195 491 M 173 508 L 191 508',stroke='#A9BBB0',width=3)

svg.append('</svg>')
open('pelican-on-a-bike.svg','w').write('\n'.join(svg))
im.resize((W,H), Image.Resampling.LANCZOS).save('pelican-on-a-bike.png')
