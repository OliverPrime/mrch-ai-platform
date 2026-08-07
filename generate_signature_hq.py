from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# EXACT EXISTING SIGNATURE DESIGN.
# Only the previously approved HQ logo/tagline treatment plus a repaired phone glyph.

src = Path('generate_signature.py').read_text()

# Preserve all existing geometry/animation; only increase final output density/palette.
src = src.replace('OUT_W,OUT_H=360,116', 'OUT_W,OUT_H=1060,340')
src = src.replace('FPS=12; active=3440', 'FPS=15; active=3440')
src = src.replace('colors=192,method=Image.Quantize.MEDIANCUT', 'colors=256,method=Image.Quantize.MEDIANCUT')

# Supersample ONLY the existing logo contour geometry. No new design/artwork/layout.
old = '''def vector_logo(size, contours, target_h):
    sw,sh=size; scale=target_h/sh; tw=round(sw*scale)
    mask=Image.new('L',(tw,target_h),0); d=ImageDraw.Draw(mask)
    for parent,pts in contours:
        poly=[(round(x*scale),round(y*scale)) for x,y in pts]
        d.polygon(poly,fill=0 if parent>=0 else 255)
    out=Image.new('RGBA',(tw,target_h),(245,245,245,0)); out.putalpha(mask)
    return out
'''
new = '''def vector_logo(size, contours, target_h):
    sw,sh=size; aa=12; scale=(target_h*aa)/sh; tw_hi=round(sw*scale)
    mask_hi=Image.new('L',(tw_hi,target_h*aa),0); d=ImageDraw.Draw(mask_hi)
    for parent,pts in contours:
        poly=[(round(x*scale),round(y*scale)) for x,y in pts]
        d.polygon(poly,fill=0 if parent>=0 else 255)
    tw=round(sw*target_h/sh)
    mask=mask_hi.resize((tw,target_h),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(tw,target_h),(245,245,245,0)); out.putalpha(mask)
    return out
'''
assert old in src
src = src.replace(old,new)

# Tagline visible bounds exactly equal the existing 370px loading bar bounds.
old_tag = "    im=layer(); d=ImageDraw.Draw(im); d.text((48,228),'MANUFACTURING, RESOURCES & CLOTHING HUB',font=font(FONT_REG,9),fill=(224,224,224,225)); L['tag']=im\n"
new_tag = '''    im=layer()
    tag='MANUFACTURING, RESOURCES & CLOTHING HUB'
    f=font(FONT_REG,36)
    scratch=Image.new('RGBA',(2400,120),(0,0,0,0)); sd=ImageDraw.Draw(scratch)
    sd.text((20,20),tag,font=f,fill=(224,224,224,225),stroke_width=0)
    bbox=scratch.getchannel('A').getbbox(); glyph=scratch.crop(bbox)
    glyph=glyph.resize((370,max(1,round(glyph.height*370/glyph.width))),Image.Resampling.LANCZOS)
    ga=glyph.getchannel('A')
    if ga.getbbox():
        px=ga.load()
        left_src=next((x for x in range(ga.width) if any(px[x,y] for y in range(ga.height))),0)
        right_src=next((x for x in range(ga.width-1,-1,-1) if any(px[x,y] for y in range(ga.height))),ga.width-1)
        for y in range(ga.height):
            px[0,y]=px[left_src,y]; px[ga.width-1,y]=px[right_src,y]
    glyph.putalpha(ga)
    im.alpha_composite(glyph,(48,228)); L['tag']=im
'''
assert old_tag in src
src = src.replace(old_tag,new_tag)

# Repair ONLY the phone handset glyph. The old thin arc/line construction could vanish
# during GIF quantization. This is a solid filled handset occupying the same icon circle.
old_phone = "        if kind=='phone': d.arc((496,cy-8,510,cy+8),30,145,fill='white',width=2); d.line((498,cy-7,495,cy-4),fill='white',width=2); d.line((508,cy+6,511,cy+3),fill='white',width=2)\n"
new_phone = '''        if kind=='phone':
            # Filled handset: same center/footprint, but robust under GIF palette conversion.
            pts=[(496,cy-8),(500,cy-10),(504,cy-6),(503,cy-3),(501,cy-2),
                 (503,cy+1),(506,cy+4),(508,cy+2),(511,cy+2),(514,cy+6),
                 (511,cy+10),(507,cy+9),(502,cy+6),(498,cy+2),(496,cy-2),(495,cy-5)]
            d.polygon(pts,fill='white')
'''
assert old_phone in src
src = src.replace(old_phone,new_phone)

exec(compile(src, 'generate_signature.py', 'exec'))
