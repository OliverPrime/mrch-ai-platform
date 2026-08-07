from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W,H=1060,340
OUT_W,OUT_H=360,116
OUT=Path('public'); OUT.mkdir(exist_ok=True)

WORD_SIZE=(1547,269)
WORD_CONTOURS=[(-1, [[1201, 2], [1201, 265], [1320, 265], [1321, 172], [1421, 172], [1422, 265], [1541, 265], [1541, 1], [1423, 1], [1421, 92], [1321, 92], [1320, 1]]), (-1, [[832, 33], [823, 62], [823, 208], [833, 236], [852, 255], [886, 266], [1127, 265], [1150, 255], [1169, 236], [1179, 207], [1178, 158], [1057, 158], [1053, 182], [942, 179], [945, 87], [1055, 87], [1057, 109], [1178, 109], [1177, 48], [1166, 26], [1148, 10], [1125, 1], [878, 1], [849, 14]]), (-1, [[449, 1], [450, 266], [568, 265], [569, 199], [632, 199], [681, 265], [812, 265], [758, 195], [774, 188], [791, 173], [803, 142], [803, 58], [793, 30], [778, 14], [748, 1]]), (2, [[568, 88], [569, 87], [679, 87], [681, 88], [684, 92], [684, 116], [680, 120], [569, 120], [568, 119]]), (-1, [[1, 2], [1, 265], [118, 266], [121, 148], [178, 265], [248, 265], [306, 147], [308, 266], [427, 265], [427, 1], [281, 1], [215, 126], [149, 1]])]
FLAME_SIZE=(835,647)
FLAME_CONTOURS=[(-1, [[9, 395], [0, 476], [10, 533], [41, 592], [81, 625], [294, 626], [219, 585], [166, 526], [143, 444], [157, 375], [169, 454], [212, 522], [279, 576], [380, 624], [455, 645], [404, 550], [388, 460], [468, 556], [571, 614], [679, 636], [834, 624], [658, 565], [522, 471], [488, 425], [471, 376], [473, 327], [493, 279], [395, 288], [313, 324], [278, 377], [283, 446], [254, 400], [243, 337], [293, 216], [299, 152], [271, 98], [226, 70], [256, 132], [239, 193], [81, 283], [35, 337]]), (-1, [[154, 0], [141, 22], [133, 48], [132, 81], [137, 99], [148, 119], [166, 138], [197, 160], [223, 172], [228, 162], [232, 145], [232, 124], [229, 115], [218, 99], [180, 66], [164, 50], [157, 40], [152, 26], [152, 9], [155, 1]])]

FONT_REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(path,size): return ImageFont.truetype(path,size)
def layer(): return Image.new('RGBA',(W,H),(0,0,0,0))

def vector_logo(size, contours, target_h):
    sw,sh=size; scale=target_h/sh; tw=round(sw*scale)
    mask=Image.new('L',(tw,target_h),0); d=ImageDraw.Draw(mask)
    for parent,pts in contours:
        poly=[(round(x*scale),round(y*scale)) for x,y in pts]
        d.polygon(poly,fill=0 if parent>=0 else 255)
    out=Image.new('RGBA',(tw,target_h),(245,245,245,0)); out.putalpha(mask)
    return out

WORD=vector_logo(WORD_SIZE,WORD_CONTOURS,44)
FLAME=vector_logo(FLAME_SIZE,FLAME_CONTOURS,48)

def paste(dst,src,x,y): dst.alpha_composite(src,(round(x),round(y)))

def make_base_layers():
    L={}
    im=layer(); d=ImageDraw.Draw(im); d.rounded_rectangle((0,0,W-1,H-1),radius=26,fill=(16,16,18,255)); L['base']=im
    im=layer(); paste(im,WORD,48,111); L['word']=im
    vx=48+WORD.width+20
    im=layer(); ImageDraw.Draw(im).rectangle((vx,101,vx+1,165),fill=(255,255,255,72)); L['vrule']=im
    im=layer(); paste(im,FLAME,vx+21,109); L['flame']=im
    im=layer(); ImageDraw.Draw(im).rectangle((448,44,449,296),fill=(255,255,255,42)); L['colrule']=im
    im=layer(); ImageDraw.Draw(im).rounded_rectangle((48,195,418,200),radius=2,fill=(255,255,255,25)); L['bartrack']=im
    stops=[(0,(196,57,42)),(.24,(218,111,57)),(.40,(226,160,70)),(.52,(212,173,78)),(.64,(163,180,84)),(.78,(113,189,91)),(1,(79,190,92))]
    ramp=Image.new('RGBA',(370,5),(0,0,0,0)); p=ramp.load()
    def color(u):
        for i in range(len(stops)-1):
            a,c0=stops[i]; b,c1=stops[i+1]
            if a<=u<=b:
                q=(u-a)/(b-a); return tuple(round(c0[j]*(1-q)+c1[j]*q) for j in range(3))+(255,)
        return stops[-1][1]+(255,)
    for x in range(370):
        c=color(x/369)
        for y in range(5): p[x,y]=c
    im=layer(); im.alpha_composite(ramp,(48,195)); L['ramp']=im
    im=layer(); d=ImageDraw.Draw(im); d.text((48,228),'MANUFACTURING, RESOURCES & CLOTHING HUB',font=font(FONT_REG,9),fill=(224,224,224,225)); L['tag']=im
    im=layer(); d=ImageDraw.Draw(im); d.text((485,48),'Oliver Prime',font=font(FONT_BOLD,32),fill='white'); L['name']=im
    im=layer(); d=ImageDraw.Draw(im); d.text((485,91),'Founder/Owner',font=font(FONT_REG,14),fill=(255,255,255,158)); L['role']=im
    def contact(label,y,kind):
        im=layer(); d=ImageDraw.Draw(im); d.ellipse((485,y+9,521,y+45),fill=(26,26,30),outline=(255,255,255,35)); cy=y+27
        if kind=='phone': d.arc((496,cy-8,510,cy+8),30,145,fill='white',width=2); d.line((498,cy-7,495,cy-4),fill='white',width=2); d.line((508,cy+6,511,cy+3),fill='white',width=2)
        elif kind=='mail': d.rectangle((496,cy-6,510,cy+5),outline='white',width=1); d.line((496,cy-6,503,cy),fill='white',width=1); d.line((510,cy-6,503,cy),fill='white',width=1)
        else: d.ellipse((496,cy-7,510,cy+7),outline='white',width=1); d.line((503,cy-7,503,cy+7),fill='white',width=1); d.line((496,cy,510,cy),fill='white',width=1)
        d.text((535,y+17),label,font=font(FONT_REG,15),fill=(245,245,245,235)); return im
    L['phone']=contact('414-364-2639',127,'phone'); L['email']=contact('oliver@mrchcorp.com',182,'mail'); L['website']=contact('www.mrchcorp.com',237,'web')
    for k,y in [('hr1',181),('hr2',236)]: im=layer(); ImageDraw.Draw(im).rectangle((485,y,741,y+1),fill=(255,255,255,26)); L[k]=im
    im=layer(); d=ImageDraw.Draw(im); d.rectangle((769,0,1060,340),fill=(11,12,14))
    for y in range(-20,380,55): d.line((745,y,1080,y-45),fill=(35,35,39),width=1)
    for x in range(760,1080,56): d.line((x,-20,x-55,380),fill=(35,35,39),width=1)
    d.line((760,168,1060,140),fill=(67,68,75),width=4); d.line((805,-20,975,360),fill=(61,62,69),width=3); L['map']=im
    im=layer(); d=ImageDraw.Draw(im); d.rounded_rectangle((917,264,1046,322),radius=15,fill=(24,24,28,242),outline=(255,255,255,32)); d.ellipse((930,281,942,293),outline='white',width=2); d.ellipse((934,285,938,289),fill='white'); d.text((957,274),'Brooklyn,',font=font(FONT_REG,13),fill='white'); d.text((957,292),'New York',font=font(FONT_REG,13),fill='white'); L['loc']=im
    return L

L=make_base_layers()

def bez_y(x,x1,y1,x2,y2):
    def bez(t,a,b): return 3*(1-t)*(1-t)*t*a+3*(1-t)*t*t*b+t*t*t
    def deriv(t,a,b): return 3*(1-t)*(1-t)*a+6*(1-t)*t*(b-a)+3*t*t*(1-b)
    t=x
    for _ in range(8):
        d=deriv(t,x1,x2)
        if abs(d)<1e-8: break
        nt=t-(bez(t,x1,x2)-x)/d
        if nt<0 or nt>1: break
        t=nt
    lo,hi=0,1
    for _ in range(20):
        v=bez(t,x1,x2)
        if abs(v-x)<1e-7: break
        if v<x: lo=t
        else: hi=t
        t=(lo+hi)/2
    return bez(t,y1,y2)

def prog(ms,delay,dur,curve):
    if ms<=delay:return 0
    if ms>=delay+dur:return 1
    return bez_y((ms-delay)/dur,*curve)

def motion(src,p):
    if p<=0:return None
    if p>=.999:return src
    blur=5*(1-p); tmp=src.filter(ImageFilter.GaussianBlur(blur)) if blur>.05 else src
    a=tmp.getchannel('A').point(lambda z:int(z*p)); tmp=tmp.copy(); tmp.putalpha(a)
    out=layer(); out.alpha_composite(tmp,(0,round(9*(1-p)))); return out

rise=(.22,1,.36,1); fillcurve=(.36,0,.18,1)
delays={'word':40,'vrule':220,'flame':360,'colrule':500,'bartrack':660,'tag':760,'name':900,'role':980,'phone':1120,'hr1':1180,'email':1260,'hr2':1320,'website':1400,'map':1560,'loc':1760}
FPS=12; active=3440; step=round(1000/FPS); times=list(range(0,active+1,step))
if times[-1]!=active: times.append(active)
frames=[]
for t in times:
    c=L['base'].copy()
    for k in ['word','vrule','flame','colrule','bartrack','tag','name','role','phone','hr1','email','hr2','website','map']:
        e=motion(L[k],prog(t,delays[k],760,rise))
        if e:c=Image.alpha_composite(c,e)
    rev=prog(t,1040,2400,fillcurve); par=prog(t,660,760,rise)
    if rev>0 and par>0:
        r=L['ramp'].copy(); m=Image.new('L',(W,H),0); ImageDraw.Draw(m).rectangle((48,195,48+round(370*rev),200),fill=255); r.putalpha(Image.composite(r.getchannel('A'),Image.new('L',(W,H),0),m)); e=motion(r,par); c=Image.alpha_composite(c,e)
    pl,pm=prog(t,1760,760,rise),prog(t,1560,760,rise)
    if pl>0 and pm>0:
        e=motion(L['loc'],pl); e=motion(e,pm) if e else None
        if e:c=Image.alpha_composite(c,e)
    c=c.convert('RGB').resize((OUT_W,OUT_H),Image.Resampling.LANCZOS)
    frames.append(c.quantize(colors=192,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.FLOYDSTEINBERG))

durations=[step]*len(frames); durations[-1]=3000
path=OUT/'mrch-signature.gif'
frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,disposal=1,optimize=True)
frames[-1].convert('RGB').save(OUT/'mrch-signature-preview.png')
print(path, path.stat().st_size)
