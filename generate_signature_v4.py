from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
HTML=ROOT/'signature-source/signature-v4.html'
FRAME_DIR=ROOT/'.signature-v4-frames'
FRAME_DIR.mkdir(exist_ok=True)
OUT=ROOT/'public/mrch-signature-v4.gif'
PREVIEW=ROOT/'public/mrch-signature-v4-preview.png'

# Gmail renders the image at 370 CSS px. The binary is 3x density for crisp display.
DISPLAY_W=370
TARGET_W=DISPLAY_W*3
TARGET_H=round(TARGET_W*340/1060)
FPS=15
ACTIVE_MS=3440
STEP=round(1000/FPS)
times=list(range(0,ACTIVE_MS+1,STEP))
if times[-1] != ACTIVE_MS: times.append(ACTIVE_MS)

pngs=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1060,'height':340},device_scale_factor=2)
    page.goto(HTML.as_uri())
    page.wait_for_timeout(100)
    for i,t in enumerate(times):
        page.evaluate(f'renderAt({t})')
        fp=FRAME_DIR/f'{i:03d}.png'
        page.locator('.card').screenshot(path=str(fp),omit_background=True)
        pngs.append(fp)
    browser.close()

rgb=[Image.open(fp).convert('RGB').resize((TARGET_W,TARGET_H),Image.Resampling.LANCZOS) for fp in pngs]
idx=sorted(set([0,len(rgb)-1]+[round(i*(len(rgb)-1)/15) for i in range(16)]))
montage=Image.new('RGB',(TARGET_W,TARGET_H*len(idx)))
for j,i in enumerate(idx): montage.paste(rgb[i],(0,j*TARGET_H))
palette=montage.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
frames=[im.quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG) for im in rgb]
durations=[STEP]*len(frames); durations[-1]=3000
OUT.parent.mkdir(exist_ok=True)
frames[0].save(OUT,save_all=True,append_images=frames[1:],duration=durations,disposal=1,optimize=True)
rgb[-1].save(PREVIEW,optimize=True)
print(f'Built {OUT}: {TARGET_W}x{TARGET_H}, display width {DISPLAY_W}px, {len(frames)} frames')
