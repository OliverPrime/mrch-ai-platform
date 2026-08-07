from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, random, re, base64, io

W,H=1110,356
S=W/1060
OUT=Path("public/mrch-signature-v5.gif")
PRE=Path("public/mrch-signature-v5-preview.png")
OUT.parent.mkdir(exist_ok=True)

html=Path("signature-source/signature-v4.html").read_text()
word_b64=re.search(r'class="word in".*?base64,([^"]+)"', html, re.S).group(1)
flame_b64="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"

def img_from_b64(s):
    return Image.open(io.BytesIO(base64.b64decode(s))).convert("RGBA")

WORD=img_from_b64(word_b64)
FLAME=img_from_b64(flame_b64)

def sc(v): return int(round(v*S))
FONT_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(p,s): return ImageFont.truetype(p, sc(s))

rng=random.Random(42)
buildings=[]
for cx in range(-41,46,8):
    for cz in range(-41,46,8):
        if cx>28: continue
        if math.hypot(cx+26,cz-24)<11: continue
        for _ in range(1+rng.randrange(2)):
            fx=2.2+rng.random()*2.6; fz=2.2+rng.random()*2.6
            px=cx+(rng.random()-.5)*max(.5,8-fx-2.4)
            pz=cz+(rng.random()-.5)*max(.5,8-fz-2.4)
            dist=math.hypot(px,pz)
            hh=(1.6+rng.random()*2.2)*(1+9/(1+dist*.22))
            buildings.append((px,pz,fx,fz,hh,rng.random()))

def project(x,y,z,ox,oy,scale):
    theta=.85; phi=1.02; r=52
    cam=(r*math.sin(phi)*math.cos(theta),r*math.cos(phi),r*math.sin(phi)*math.sin(theta))
    tx,ty,tz=0,1.5,0
    fx,fy,fz=tx-cam[0],ty-cam[1],tz-cam[2]
    fl=math.sqrt(fx*fx+fy*fy+fz*fz); fx,fy,fz=fx/fl,fy/fl,fz/fl
    rx,ry,rz=-fz,0,fx
    rl=math.sqrt(rx*rx+rz*rz); rx,rz=rx/rl,rz/rl
    ux=ry*fz-rz*fy; uy=rz*fx-rx*fz; uz=rx*fy-ry*fx
    vx,vy,vz=x-cam[0],y-cam[1],z-cam[2]
    X=vx*rx+vy*ry+vz*rz; Y=vx*ux+vy*uy+vz*uz; Z=vx*fx+vy*fy+vz*fz
    q=1.25/max(.1,Z)
    return ox+X*q*scale, oy-Y*q*scale

def draw_map(t):
    mw,mh=sc(291),H
    im=Image.new("RGB",(mw,mh),(10,11,13)); d=ImageDraw.Draw(im)
    ox,oy=mw*.50,mh*.64; ps=2400*S
    d.polygon([(mw*.72,0),(mw,0),(mw,mh),(mw*.64,mh)],fill=(15,22,29))
    for i in range(18):
        yy=(i*23 + int(t*5))%mh
        d.line((mw*.69,yy,mw,yy-sc(7)),fill=(19,29,39),width=max(1,sc(.6)))
    for a in range(-37,46,8):
        d.line([project(-45,0,a,ox,oy,ps),project(45,0,a,ox,oy,ps)],fill=(28,28,33),width=max(1,sc(1)))
        d.line([project(a,0,-45,ox,oy,ps),project(a,0,45,ox,oy,ps)],fill=(28,28,33),width=max(1,sc(1)))
    d.line([project(-45,.02,0,ox,oy,ps),project(53,.02,0,ox,oy,ps)],fill=(42,42,49),width=sc(3))
    d.line([project(0,.02,-45,ox,oy,ps),project(0,.02,45,ox,oy,ps)],fill=(42,42,49),width=sc(3))
    pc=project(-26,.02,24,ox,oy,ps)
    d.ellipse((pc[0]-sc(16),pc[1]-sc(8),pc[0]+sc(16),pc[1]+sc(8)),fill=(19,30,21))
    for i in range(14):
        aa=i*2.399; rr=3+(i%5)*1.1
        p=project(-26+math.cos(aa)*rr,.8,24+math.sin(aa)*rr,ox,oy,ps)
        d.ellipse((p[0]-sc(1.5),p[1]-sc(2),p[0]+sc(1.5),p[1]+sc(1)),fill=(28,46,32))
    for px,pz,fx,fz,hh,typ in sorted(buildings,key=lambda b:b[0]+b[1]):
        base=[project(px-fx/2,0,pz-fz/2,ox,oy,ps),project(px+fx/2,0,pz-fz/2,ox,oy,ps),project(px+fx/2,0,pz+fz/2,ox,oy,ps),project(px-fx/2,0,pz+fz/2,ox,oy,ps)]
        top=[project(px-fx/2,hh,pz-fz/2,ox,oy,ps),project(px+fx/2,hh,pz-fz/2,ox,oy,ps),project(px+fx/2,hh,pz+fz/2,ox,oy,ps),project(px-fx/2,hh,pz+fz/2,ox,oy,ps)]
        face=(23,23,28) if typ>.7 else ((24,23,27) if typ<.45 else (20,22,29))
        d.polygon([base[0],base[1],top[1],top[0]],fill=face)
        d.polygon([base[1],base[2],top[2],top[1]],fill=tuple(max(0,c-3) for c in face))
        d.polygon(top,fill=tuple(min(255,c+4) for c in face))
        if typ<.7 and hh>4:
            c=(201,160,90) if typ<.45 else (124,147,184)
            for q in (.28,.52,.76):
                x=top[0][0]*(1-q)+top[1][0]*q; y=top[0][1]*(1-q)+top[1][1]*q
                d.rectangle((x-sc(.6),y+sc(2),x+sc(.6),y+sc(3.2)),fill=c)
    d.line([project(31,1.15,0,ox,oy,ps),project(53,1.15,0,ox,oy,ps)],fill=(44,44,53),width=sc(4))
    for side in (-1,1):
        d.line([project(31,1.55,side*1.84,ox,oy,ps),project(53,1.55,side*1.84,ox,oy,ps)],fill=(58,58,68),width=sc(1))
        for px in (36,44):
            d.line([project(px,1.35,side*1.84,ox,oy,ps),project(px,6.4,side*1.84,ox,oy,ps)],fill=(67,68,80),width=sc(1))
            pts=[]
            for i in range(13):
                q=i/12; xx=px-7+q*14; yy=1.7+4.4*(abs(q-.5)*2)**1.6
                pts.append(project(xx,yy,side*1.84,ox,oy,ps))
            d.line(pts,fill=(86,87,100),width=1)
            for i in range(1,12,2):
                q=i/12; xx=px-7+q*14; yy=1.7+4.4*(abs(q-.5)*2)**1.6
                d.line([project(xx,yy,side*1.84,ox,oy,ps),project(xx,1.35,side*1.84,ox,oy,ps)],fill=(75,76,89),width=1)
    for a in range(-41,45,7):
        for side in (-1,1):
            for x,y,z in ((a,1.5,side*2.1),(side*2.1,1.5,a)):
                if z>31 and abs(x)<4: continue
                p=project(x,y,z,ox,oy,ps)
                d.ellipse((p[0]-sc(.8),p[1]-sc(.8),p[0]+sc(.8),p[1]+sc(.8)),fill=(217,177,106))
    span=90
    for i in range(9):
        for dirn,col,lane in ((1,(245,242,232),.85),(-1,(216,69,46),-.85)):
            off=(i*9.7+7)%span; speed=7.2
            p=((off+t*speed)%span)-45
            if dirn<0:p=-p
            yy=1.35 if p>31 else .18
            x,y=project(p,yy,lane,ox,oy,ps)
            d.ellipse((x-sc(1.3),y-sc(.8),x+sc(1.3),y+sc(.8)),fill=col)
    for i in range(6):
        for dirn,col,lane in ((1,(245,242,232),.85),(-1,(216,69,46),-.85)):
            off=(i*14.2+3)%span; speed=6.1
            p=((off+t*speed)%span)-45
            if dirn<0:p=-p
            x,y=project(lane,.18,p,ox,oy,ps)
            d.ellipse((x-sc(.8),y-sc(1.2),x+sc(.8),y+sc(1.2)),fill=col)
    b0=project(0,0,0,ox,oy,ps); bh=project(0,2.9,0,ox,oy,ps)
    d.line([b0,bh],fill=(255,255,255),width=sc(1))
    d.ellipse((bh[0]-sc(2.6),bh[1]-sc(2.6),bh[0]+sc(2.6),bh[1]+sc(2.6)),fill="white")
    for phase in (0,.5):
        ph=((t*.45)+phase)%1
        rr=(.6+ph*5.5)*S*1.8
        shade=int(150*(1-ph))
        d.ellipse((b0[0]-rr,b0[1]-rr*.4,b0[0]+rr,b0[1]+rr*.4),outline=(shade,shade,shade),width=max(1,sc(1)))
    return im

def ease(p): return 1-(1-p)**4
delays={"word":40,"vrule":220,"flame":360,"col":500,"bar":660,"tag":760,"name":900,"role":980,"phone":1120,"email":1260,"web":1400,"map":1560,"loc":1760}
def prog(ms,d,dur=760):
    if ms<=d:return 0
    if ms>=d+dur:return 1
    return ease((ms-d)/dur)

def compose(ms):
    im=Image.new("RGBA",(W,H),(16,16,18,255)); d=ImageDraw.Draw(im)
    def add_asset(a,x,y,h,key):
        p=prog(ms,delays[key])
        if p<=0:return
        hh=sc(h); ww=round(a.width*hh/a.height)
        aa=a.resize((ww,hh),Image.Resampling.LANCZOS)
        aa.putalpha(aa.getchannel("A").point(lambda v:int(v*p)))
        im.alpha_composite(aa,(sc(x),sc(y+9*(1-p))))
    add_asset(WORD,48,111,44,"word")
    p=prog(ms,220)
    if p:d.rectangle((sc(354),sc(101),sc(355),sc(165)),fill=(255,255,255,int(70*p)))
    add_asset(FLAME,376,109,48,"flame")
    p=prog(ms,500)
    if p:d.rectangle((sc(448),sc(44),sc(449),sc(296)),fill=(255,255,255,int(40*p)))
    p=prog(ms,660)
    if p:d.rounded_rectangle((sc(48),sc(195),sc(418),sc(200)),radius=sc(2),fill=(255,255,255,int(25*p)))
    rev=max(0,min(1,(ms-1040)/2400))
    if rev:
        x0,x1=sc(48),sc(418); y0,y1=sc(195),sc(200)
        stops=[(0,(196,57,42)),(.24,(218,111,57)),(.40,(226,160,70)),(.52,(212,173,78)),(.64,(163,180,84)),(.78,(113,189,91)),(1,(79,190,92))]
        for x in range(x0,int(x0+(x1-x0)*rev)):
            u=(x-x0)/(x1-x0); c=stops[-1][1]
            for j in range(len(stops)-1):
                a,c0=stops[j]; b,c1=stops[j+1]
                if a<=u<=b:
                    q=(u-a)/(b-a); c=tuple(round(c0[k]*(1-q)+c1[k]*q) for k in range(3)); break
            d.line((x,y0,x,y1),fill=c)
    def txt(x,y,text,size,key,bold=False,alpha=235):
        p=prog(ms,delays[key]);
        if p<=0:return
        f=font(FONT_BOLD if bold else FONT_REG,size)
        d.text((sc(x),sc(y+9*(1-p))),text,font=f,fill=(245,245,245,int(alpha*p)))
    txt(48,228,"MANUFACTURING, RESOURCES & CLOTHING HUB",9,"tag",False,225)
    txt(485,48,"Oliver Prime",32,"name",True,255)
    txt(485,91,"Founder/Owner",14,"role",False,158)
    def contact(y,label,key,kind):
        p=prog(ms,delays[key]);
        if p<=0:return
        cy=sc(y+27); col=(255,255,255,int(255*p))
        d.ellipse((sc(485),sc(y+9),sc(521),sc(y+45)),fill=(26,26,30,int(255*p)),outline=(255,255,255,int(35*p)))
        if kind=="phone":
            pts=[(496,y+19),(499,y+17),(502,y+19),(503,y+22),(501,y+24),(503,y+27),(506,y+30),(508,y+28),(511,y+29),(513,y+32),(511,y+36),(507,y+36),(502,y+33),(498,y+29),(496,y+25)]
            d.line([(sc(x),sc(yy)) for x,yy in pts],fill=col,width=sc(2),joint="curve")
        elif kind=="mail":
            d.rectangle((sc(496),cy-sc(6),sc(510),cy+sc(5)),outline=col,width=sc(1)); d.line((sc(496),cy-sc(6),sc(503),cy,sc(510),cy-sc(6)),fill=col,width=sc(1))
        else:
            d.ellipse((sc(496),cy-sc(7),sc(510),cy+sc(7)),outline=col,width=sc(1)); d.line((sc(503),cy-sc(7),sc(503),cy+sc(7)),fill=col,width=sc(1)); d.line((sc(496),cy,sc(510),cy),fill=col,width=sc(1))
        txt(535,y+17,label,15,key,False,235)
    contact(127,"414-364-2639","phone","phone")
    if prog(ms,1180): d.rectangle((sc(485),sc(181),sc(741),sc(182)),fill=(255,255,255,int(26*prog(ms,1180))))
    contact(182,"oliver@mrchcorp.com","email","mail")
    if prog(ms,1320): d.rectangle((sc(485),sc(236),sc(741),sc(237)),fill=(255,255,255,int(26*prog(ms,1320))))
    contact(237,"www.mrchcorp.com","web","web")
    p=prog(ms,1560)
    if p:
        m=draw_map(ms/1000).convert("RGBA"); m.putalpha(m.getchannel("A").point(lambda v:int(v*p))); im.alpha_composite(m,(sc(769),0))
    p=prog(ms,1760)
    if p:
        d.rounded_rectangle((sc(917),sc(264),sc(1046),sc(322)),radius=sc(15),fill=(24,24,28,int(242*p)),outline=(255,255,255,int(32*p)))
        d.ellipse((sc(930),sc(281),sc(942),sc(293)),outline=(255,255,255,int(255*p)),width=sc(2))
        txt(957,274,"Brooklyn,",13,"loc",False,255); txt(957,292,"New York",13,"loc",False,255)
    return im.convert("RGB")

times=list(range(0,3441,67)); rgb=[compose(t) for t in times]
sample=Image.new("RGB",(W,H*12))
for j,i in enumerate([round(k*(len(rgb)-1)/11) for k in range(12)]): sample.paste(rgb[i],(0,j*H))
pal=sample.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
frames=[im.quantize(palette=pal,dither=Image.Dither.FLOYDSTEINBERG) for im in rgb]
dur=[67]*len(frames); dur[-1]=3000
frames[0].save(OUT,save_all=True,append_images=frames[1:],duration=dur,disposal=1,optimize=True)
rgb[-1].save(PRE,optimize=True)
print(OUT, OUT.stat().st_size)
