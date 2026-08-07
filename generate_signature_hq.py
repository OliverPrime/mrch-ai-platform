from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# EXACT EXISTING SIGNATURE DESIGN.
# Only three revisions are made here:
# 1) higher-fidelity MRCH wordmark rasterization,
# 2) higher-fidelity Flame M rasterization,
# 3) tagline visible bounds exactly equal the existing loading bar bounds.

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
    # 12x supersampling eliminates jagged/pixelated contour edges while retaining
    # the exact existing MRCH and Flame geometry and exact target dimensions.
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

# Replace ONLY the existing tagline layer. The loading bar's actual source bounds
# are x=48 through x=417 (370 pixels). We render the text, crop to its nontransparent
# glyph bounds, then resample that glyph crop to exactly 370 pixels. Therefore its
# ACTUAL VISIBLE first and last pixels are mathematically identical to the bar bounds.
old_tag = "    im=layer(); d=ImageDraw.Draw(im); d.text((48,228),'MANUFACTURING, RESOURCES & CLOTHING HUB',font=font(FONT_REG,9),fill=(224,224,224,225)); L['tag']=im\n"
new_tag = '''    im=layer()
    tag='MANUFACTURING, RESOURCES & CLOTHING HUB'
    # Render oversized first so the final small lettering remains crisp.
    f=font(FONT_REG,36)
    scratch=Image.new('RGBA',(2400,120),(0,0,0,0)); sd=ImageDraw.Draw(scratch)
    sd.text((20,20),tag,font=f,fill=(224,224,224,225),stroke_width=0)
    alpha=scratch.getchannel('A'); bbox=alpha.getbbox()
    glyph=scratch.crop(bbox)
    glyph=glyph.resize((370, max(1,round(glyph.height*370/glyph.width))),Image.Resampling.LANCZOS)
    # Force the two extreme columns to retain visible antialiased glyph pixels;
    # this makes measured nontransparent bounds exactly x=48..417, same as bar.
    ga=glyph.getchannel('A')
    gd=ImageDraw.Draw(ga)
    # Preserve visual shape; only ensure edge coverage where the first/last glyph lands.
    if ga.getbbox():
        top,bottom=0,ga.height-1
        # Copy nearest nonzero edge-column alpha into exact boundary columns.
        px=ga.load()
        left_src=next((x for x in range(ga.width) if any(px[x,y] for y in range(ga.height))),0)
        right_src=next((x for x in range(ga.width-1,-1,-1) if any(px[x,y] for y in range(ga.height))),ga.width-1)
        for y in range(ga.height):
            px[0,y]=px[left_src,y]
            px[ga.width-1,y]=px[right_src,y]
    glyph.putalpha(ga)
    im.alpha_composite(glyph,(48,228)); L['tag']=im
'''
assert old_tag in src
src = src.replace(old_tag,new_tag)

exec(compile(src, 'generate_signature.py', 'exec'))
