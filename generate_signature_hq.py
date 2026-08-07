from pathlib import Path

src = Path('generate_signature.py').read_text()
src = src.replace('OUT_W,OUT_H=360,116', 'OUT_W,OUT_H=1060,340')
src = src.replace('FPS=12; active=3440', 'FPS=15; active=3440')
src = src.replace('colors=192,method=Image.Quantize.MEDIANCUT', 'colors=256,method=Image.Quantize.MEDIANCUT')
exec(compile(src, 'generate_signature.py', 'exec'))
