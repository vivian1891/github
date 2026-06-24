from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)
random.seed(20260624)


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def gradient(size, top=(7, 18, 42), bottom=(31, 38, 92)):
    w, h = size
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        for x in range(w):
            wave = 0.06 * math.sin((x / w) * math.pi * 2 + t * 3)
            k = min(1, max(0, t + wave))
            px[x, y] = tuple(int(top[i] * (1 - k) + bottom[i] * k) for i in range(3))
    return img.convert("RGBA")


def overlay_grid(draw, w, h, color=(113, 202, 255, 38), step=80):
    for x in range(-step, w + step, step):
        draw.line([(x, 0), (x + 180, h)], fill=color, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y + 60)], fill=color, width=1)


def node(draw, x, y, r, fill=(68, 220, 255, 230), outline=(255, 255, 255, 120)):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=max(1, r // 4))


def line(draw, a, b, fill=(73, 203, 255, 120), width=4):
    draw.line([a, b], fill=fill, width=width)


def save_webp(img, name, size):
    img = img.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    path = OUT / name
    img.save(path, format="WEBP", quality=88, method=6)
    with path.open("rb") as fh:
        header = fh.read(12)
    if not (header[:4] == b"RIFF" and header[8:12] == b"WEBP"):
        raise RuntimeError(f"{name} is not a RIFF/WEBP file")
    with Image.open(path) as check:
        if check.format != "WEBP" or check.size[0] <= 0 or check.size[1] <= 0:
            raise RuntimeError(f"{name} failed WebP verification")


def base_scene(size, seed_shift=0):
    random.seed(20260624 + seed_shift)
    img = gradient(size)
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = size
    overlay_grid(draw, w, h)
    for i in range(26):
        x = random.randint(40, w - 40)
        y = random.randint(40, h - 40)
        r = random.randint(3, 8)
        node(draw, x, y, r, (255, 255, 255, random.randint(50, 130)), (255, 255, 255, 40))
    return img, draw


def hero():
    img, draw = base_scene((1600, 900), 1)
    points = [(160, 620), (390, 470), (620, 540), (850, 330), (1120, 400), (1410, 250)]
    for i in range(len(points) - 1):
        line(draw, points[i], points[i + 1], (67, 224, 255, 155), 7)
        line(draw, (points[i][0], points[i][1] + 80), (points[i + 1][0], points[i + 1][1] + 30), (133, 103, 255, 105), 4)
    for idx, p in enumerate(points):
        node(draw, p[0], p[1], 18 + idx % 3 * 4, (74, 219, 255, 220), (255, 255, 255, 160))
    for x in range(260, 1350, 180):
        draw.arc((x, 170, x + 220, 390), 205, 340, fill=(255, 188, 82, 90), width=3)
    return img


def route_atlas():
    img, draw = base_scene((1400, 875), 2)
    hubs = [(170, 440), (430, 250), (640, 520), (880, 300), (1130, 520), (1230, 210)]
    for a in hubs:
        for b in random.sample(hubs, 3):
            if a != b:
                line(draw, a, b, (97, 221, 255, 78), 3)
    for i, p in enumerate(hubs):
        node(draw, *p, 22 if i in (0, 4) else 14, (44, 198, 220, 220), (255, 255, 255, 120))
    draw.rounded_rectangle((90, 655, 1260, 740), radius=18, outline=(246, 183, 60, 150), width=3, fill=(255, 255, 255, 24))
    return img


def device_matrix():
    img, draw = base_scene((1400, 875), 3)
    panels = [(120, 140, 390, 640), (470, 210, 710, 570), (790, 110, 1240, 610), (280, 650, 1110, 760)]
    colors = [(255, 255, 255, 42), (36, 198, 220, 54), (112, 87, 255, 56), (35, 179, 122, 48)]
    for box, color in zip(panels, colors):
        draw.rounded_rectangle(box, radius=22, fill=color, outline=(255, 255, 255, 96), width=2)
    for x in [210, 560, 930, 1120]:
        for y in [230, 360, 490, 690]:
            node(draw, x, y, 9, (246, 183, 60, 210), (255, 255, 255, 110))
    return img


def performance_console():
    img, draw = base_scene((1400, 875), 4)
    draw.rounded_rectangle((105, 105, 1295, 770), radius=26, fill=(255, 255, 255, 34), outline=(255, 255, 255, 92), width=2)
    for i in range(5):
        y = 170 + i * 92
        draw.rounded_rectangle((155, y, 520, y + 54), radius=12, fill=(255, 255, 255, 40))
        draw.rounded_rectangle((570, y, 1220, y + 54), radius=12, fill=(36, 107, 254, 35))
    pts = []
    for i in range(16):
        x = 610 + i * 38
        y = 620 - int(90 * math.sin(i / 2.1) + random.randint(-28, 28))
        pts.append((x, y))
    draw.line(pts, fill=(36, 198, 220, 230), width=6)
    for p in pts[::3]:
        node(draw, *p, 8, (255, 255, 255, 220), (36, 198, 220, 180))
    return img


def how_it_works():
    img, draw = base_scene((1400, 875), 5)
    centers = [(170, 430), (380, 300), (600, 440), (820, 300), (1030, 440), (1220, 310)]
    for i in range(len(centers) - 1):
        line(draw, centers[i], centers[i + 1], (246, 183, 60, 150), 6)
    for idx, c in enumerate(centers):
        draw.rounded_rectangle((c[0] - 58, c[1] - 58, c[0] + 58, c[1] + 58), radius=20, fill=(255, 255, 255, 38), outline=(255, 255, 255, 100), width=2)
        node(draw, c[0], c[1], 15 + (idx % 2) * 5, (75, 220, 255, 220), (255, 255, 255, 120))
    return img


def remote_office():
    img, draw = base_scene((1400, 875), 6)
    draw.rounded_rectangle((120, 150, 760, 610), radius=24, fill=(255, 255, 255, 46), outline=(255, 255, 255, 100), width=2)
    draw.rounded_rectangle((820, 220, 1220, 520), radius=22, fill=(112, 87, 255, 58), outline=(255, 255, 255, 100), width=2)
    for p in [(260, 300), (460, 420), (640, 270), (930, 350), (1120, 420)]:
        node(draw, *p, 15, (36, 198, 220, 225), (255, 255, 255, 130))
    line(draw, (640, 270), (930, 350), (246, 183, 60, 150), 5)
    line(draw, (460, 420), (1120, 420), (74, 220, 255, 100), 4)
    return img


def privacy_layer():
    img, draw = base_scene((1400, 875), 7)
    for i in range(5):
        inset = 110 + i * 54
        draw.rounded_rectangle((inset, inset, 1400 - inset, 875 - inset), radius=34, outline=(255, 255, 255, 60 + i * 20), width=3)
    draw.polygon([(700, 190), (930, 300), (900, 570), (700, 690), (500, 570), (470, 300)], fill=(36, 198, 220, 58), outline=(255, 255, 255, 130))
    for p in [(700, 190), (930, 300), (900, 570), (700, 690), (500, 570), (470, 300)]:
        node(draw, *p, 12, (246, 183, 60, 210), (255, 255, 255, 140))
    return img


def light_update():
    img, draw = base_scene((1400, 875), 8)
    for i in range(7):
        x = 150 + i * 165
        h = 210 + (i % 3) * 64
        draw.rounded_rectangle((x, 520 - h, x + 86, 520), radius=18, fill=(255, 255, 255, 48), outline=(255, 255, 255, 95), width=2)
        node(draw, x + 43, 570, 12, (35, 179, 122, 220), (255, 255, 255, 130))
    draw.arc((420, 180, 980, 740), 210, 510, fill=(36, 198, 220, 185), width=8)
    draw.arc((482, 242, 918, 678), 30, 320, fill=(112, 87, 255, 160), width=5)
    return img


def journal_cover(kind):
    img, draw = base_scene((1200, 675), 20 + kind)
    if kind == 0:
        draw.rounded_rectangle((90, 130, 520, 500), radius=20, fill=(255, 255, 255, 40))
        draw.rounded_rectangle((670, 155, 1080, 460), radius=20, fill=(36, 198, 220, 46))
        line(draw, (520, 310), (670, 310), (246, 183, 60, 180), 6)
    elif kind == 1:
        pts = [(140 + i * 62, 430 - int(math.sin(i / 1.7) * 80 + random.randint(-35, 35))) for i in range(15)]
        draw.line(pts, fill=(36, 198, 220, 235), width=6)
        for p in pts[::2]:
            node(draw, *p, 9, (255, 255, 255, 220))
    elif kind == 2:
        draw.rounded_rectangle((130, 110, 980, 520), radius=20, fill=(255,255,255,45), outline=(255,255,255,100), width=2)
        for i in range(6):
            draw.rounded_rectangle((210, 180 + i * 48, 880, 208 + i * 48), radius=8, fill=(36,107,254,45))
    elif kind == 3:
        draw.rounded_rectangle((150, 150, 430, 520), radius=28, fill=(255,255,255,44), outline=(255,255,255,110), width=2)
        draw.rounded_rectangle((700, 185, 1020, 470), radius=24, fill=(112,87,255,58), outline=(255,255,255,110), width=2)
        line(draw, (430, 330), (700, 330), (246,183,60,170), 5)
    elif kind == 4:
        for box in [(120,150,430,470),(470,210,760,520),(800,120,1080,430)]:
            draw.rounded_rectangle(box, radius=18, fill=(255,255,255,42), outline=(255,255,255,90), width=2)
        line(draw, (430, 310), (470, 360), (36,198,220,150), 5)
        line(draw, (760, 360), (800, 270), (36,198,220,150), 5)
    else:
        for i in range(5):
            draw.rounded_rectangle((160+i*160, 430-i*36, 265+i*160, 520), radius=16, fill=(35,179,122,58), outline=(255,255,255,100), width=2)
        draw.arc((340, 120, 850, 600), 210, 500, fill=(246,183,60,170), width=7)
    for i in range(9):
        node(draw, 130 + i * 115, 100 + (i % 3) * 145, 7, (255,255,255,160), (255,255,255,70))
    return img


def logo():
    img = Image.new("RGBA", (600, 160), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((18, 20, 142, 140), radius=28, fill=(8, 19, 44, 255))
    for p in [(48, 98), (80, 58), (112, 92)]:
        node(draw, *p, 10, (43, 210, 232, 235), (255, 255, 255, 150))
    line(draw, (48, 98), (80, 58), (112, 87, 255, 210), 5)
    line(draw, (80, 58), (112, 92), (36, 198, 220, 210), 5)
    draw.arc((36, 38, 124, 126), 205, 25, fill=(246, 183, 60, 190), width=5)
    draw.text((170, 34), "加速器", font=font(52, True), fill=(8, 19, 44, 255))
    draw.text((174, 96), "ZQCG GLOBAL LINK", font=font(22, False), fill=(88, 104, 134, 255))
    img.save(OUT / "logo.png", format="PNG")


def favicon():
    img = Image.new("RGBA", (256, 256), (8, 19, 44, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    for p in [(74, 152), (128, 78), (184, 146)]:
        node(draw, *p, 20, (36, 198, 220, 240), (255,255,255,170))
    line(draw, (74, 152), (128, 78), (112, 87, 255, 235), 12)
    line(draw, (128, 78), (184, 146), (36, 198, 220, 235), 12)
    draw.arc((48, 48, 208, 208), 205, 25, fill=(246, 183, 60, 220), width=10)
    img.save(OUT / "favicon-source.png", format="PNG")
    sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img.save(ROOT / "favicon.ico", format="ICO", sizes=sizes)


def main():
    logo()
    favicon()
    assets = [
        ("hero-network.webp", hero(), (1600, 900)),
        ("route-atlas.webp", route_atlas(), (1400, 875)),
        ("device-matrix.webp", device_matrix(), (1400, 875)),
        ("performance-console.webp", performance_console(), (1400, 875)),
        ("how-it-works.webp", how_it_works(), (1400, 875)),
        ("remote-office.webp", remote_office(), (1400, 875)),
        ("privacy-layer.webp", privacy_layer(), (1400, 875)),
        ("light-update.webp", light_update(), (1400, 875)),
        ("journal-network-difference.webp", journal_cover(0), (1200, 675)),
        ("journal-node-latency.webp", journal_cover(1), (1200, 675)),
        ("journal-desktop-status.webp", journal_cover(2), (1200, 675)),
        ("journal-mobile-switch.webp", journal_cover(3), (1200, 675)),
        ("journal-remote-work.webp", journal_cover(4), (1200, 675)),
        ("journal-version-update.webp", journal_cover(5), (1200, 675)),
    ]
    for name, img, size in assets:
        save_webp(img, name, size)
    with Image.open(OUT / "logo.png") as logo_check:
        if logo_check.format != "PNG" or logo_check.size != (600, 160):
            raise RuntimeError("logo.png verification failed")
    with Image.open(ROOT / "favicon.ico") as ico_check:
        if ico_check.format != "ICO":
            raise RuntimeError("favicon.ico verification failed")
    print("PASS generated image assets")


if __name__ == "__main__":
    main()
