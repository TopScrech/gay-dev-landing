#!/usr/bin/env python3
"""Renders the 20 s village-horror teaser to public/videos/teaser.mp4

Everything is procedural except the devblog concept art. Title and tagline are
read from src/lib/site.ts, so re-run this after the real title lands.

  python3 tools/teaser/make_teaser.py            # full render
  python3 tools/teaser/make_teaser.py --still 14  # one frame to scratch PNG
"""
import argparse
import re
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'public/images/blog/devblog-1'
OUT = ROOT / 'public/videos/teaser.mp4'
FONT = '/System/Library/Fonts/Supplemental/Luminari.ttf'

W, H, FPS, DUR = 1920, 1080, 24, 20.0
N = int(FPS * DUR)
BAR = 138  # 2.39:1 letterbox
SR = 44100

site = (ROOT / 'src/lib/site.ts').read_text()
TITLE = re.search(r"GAME_TITLE = '([^']*)'", site).group(1)
TAGLINE = re.search(r"TAGLINE = '([^']*)'", site).group(1)
STUDIO = re.search(r"STUDIO_NAME = '([^']*)'", site).group(1)

BONE = np.array([0.93, 0.88, 0.78], np.float32)
WARM = np.array([1.0, 0.62, 0.26], np.float32)
PURPLE = np.array([0.62, 0.32, 1.0], np.float32)
BOG = np.array([0.62, 0.86, 0.70], np.float32)

rng = np.random.default_rng(13)
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)


# ---------- small helpers ----------

def smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def ramp(t, a, b):
    return float(smooth((t - a) / (b - a)))


def window(t, a, b, fin=0.3, fout=0.3):
    return ramp(t, a, a + fin) * (1 - ramp(t, b - fout, b))


def to_pil(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def to_arr(img):
    return np.asarray(img.convert('RGB'), np.float32) / 255


def cam(img, cx, cy, vw):
    """Crop a 16:9 view of width vw centred on (cx, cy) and scale it to the frame"""
    vh = vw * H / W
    box = (cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2)
    return to_arr(img.transform((W, H), Image.EXTENT, box, Image.BICUBIC))


def glow(cx, cy, s):
    return np.exp(-((XX - cx) ** 2 + (YY - cy) ** 2) / (2 * s * s))[..., None]


def jitter(t, seed, rate=9.0):
    """Cheap smooth noise in [-1, 1]"""
    return float(np.sin(t * rate + seed) * 0.6 + np.sin(t * rate * 2.37 + seed * 3.1) * 0.4)


def make_fog(h, w, seed):
    r = np.random.default_rng(seed)
    f = np.zeros((h, w), np.float32)
    for cell, amp in [(300, 1.0), (130, 0.5), (55, 0.25)]:
        gh, gw = h // cell + 3, w // cell + 3
        small = Image.fromarray((r.random((gh, gw)) * 255).astype(np.uint8))
        big = small.resize((gw * cell, gh * cell), Image.BICUBIC)
        f += np.asarray(big, np.float32)[:h, :w] / 255 * amp
    f = (f - f.min()) / (f.max() - f.min())
    return smooth((f - 0.3) / 0.55).astype(np.float32)


def text_mask(text, size, y, x=W / 2, blur=0):
    img = Image.new('L', (W, H), 0)
    ImageDraw.Draw(img).text((x, y), text, font=ImageFont.truetype(FONT, size), fill=255, anchor='mm')
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(img, np.float32)[..., None] / 255


# ---------- assets ----------

def ink_on_black(path, tint, crop=None, outline=False):
    """White-paper sketches flipped to pale lines on black"""
    im = Image.open(path).convert('RGB')
    if crop:
        im = im.crop(crop)
    a = to_arr(im)
    lum = a @ np.array([0.3, 0.59, 0.11], np.float32)
    ink = np.clip((0.93 - lum) / 0.55, 0, 1) ** 0.75
    if outline:  # solid fills would invert into blobs, so keep only their edges
        edges = np.asarray(im.convert('L').filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3)), np.float32) / 255
        edges[:4], edges[-4:], edges[:, :4], edges[:, -4:] = 0, 0, 0, 0
        ink = np.maximum(np.clip(edges * 2.5, 0, 1), ink * 0.18)
        ink = np.asarray(Image.fromarray((ink * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    col = ink[..., None] * tint
    return to_pil(col)


def load_creature():
    src = Image.open(ART / 'creature-concept.webp')
    w, h = src.size
    gy, gx = np.mgrid[0:h, 0:w].astype(np.float32)
    falloff = smooth(1.15 - np.sqrt(((gx - 500) / 470) ** 2 + ((gy - 520) / 520) ** 2))
    frames = []
    for i in range(src.n_frames):
        src.seek(i)
        g = np.asarray(src.convert('L'), np.float32) / 255
        border = np.median(np.concatenate([g[:, :40].ravel(), g[:, -40:].ravel(), g[:40].ravel()]))
        p = np.clip((g - border - 0.02) / (1 - border), 0, 1)
        p = np.clip(p * 1.9, 0, 1) ** 1.25 * falloff
        rgb = p[..., None] * BOG + (p ** 3)[..., None] * (np.array([1.0, 0.92, 0.6]) - BOG)
        frames.append(to_pil(rgb))
    return frames


def load_villager():
    a = to_arr(Image.open(ART / 'villager-concept.jpg'))
    lum = a @ np.array([0.3, 0.59, 0.11], np.float32)
    alpha = np.clip((0.78 - lum) / 0.32, 0, 1) ** 1.2
    grey = lum[..., None]
    col = (a * 0.55 + grey * 0.45) * 0.8
    return col, alpha


def load_lantern():
    im = Image.open(ART / 'lantern.png').convert('RGB')
    im = im.crop((im.width // 2, 0, im.width, im.height))
    bbox = im.point(lambda v: 255 if v > 18 else 0).getbbox()
    im = im.crop(bbox)
    scale = 700 / im.height
    im = im.resize((int(im.width * scale), 700), Image.LANCZOS)
    pad = Image.new('RGB', (im.width + 400, im.height * 2 + 40), 'black')
    pad.paste(im, (200, im.height + 40))  # ring sits at pad centre so rotate() pivots on it
    return pad


def build_village():
    VW, VH = 2400, 1350
    r = np.random.default_rng(4)
    gy, gx = np.mgrid[0:VH, 0:VW].astype(np.float32)
    top, hor = np.array([0.012, 0.018, 0.035]), np.array([0.085, 0.10, 0.135])
    sky = top + (hor - top) * (np.clip(gy / 930, 0, 1) ** 1.7)[..., None]
    mx, my = 1760, 320
    d2 = (gx - mx) ** 2 + (gy - my) ** 2
    sky += np.exp(-d2 / (2 * 240 ** 2))[..., None] * np.array([0.09, 0.11, 0.12])
    sky += np.exp(-d2 / (2 * 700 ** 2))[..., None] * np.array([0.02, 0.03, 0.035])
    moon = smooth((68 - np.sqrt(d2)) / 2.5)[..., None]
    craters = 1 - 0.12 * (np.exp(-((gx - 1745) ** 2 + (gy - 305) ** 2) / 400)
                          + np.exp(-((gx - 1785) ** 2 + (gy - 345) ** 2) / 250))[..., None]
    sky = sky * (1 - moon) + moon * np.array([0.80, 0.82, 0.74]) * craters
    img = to_pil(sky)

    clouds = Image.new('L', (VW, VH), 0)
    cd = ImageDraw.Draw(clouds)
    for cx, cy, w, h in [(1700, 350, 520, 34), (1900, 395, 380, 22), (600, 260, 700, 30), (1150, 180, 500, 18)]:
        cd.ellipse((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=210)
    clouds = clouds.filter(ImageFilter.GaussianBlur(14))
    img = Image.composite(Image.new('RGB', (VW, VH), (14, 17, 24)), img, clouds)

    d = ImageDraw.Draw(img)
    hill = [(x, 935 + 38 * np.sin(x / 310) + 22 * np.sin(x / 97 + 1) + r.normal(0, 4)) for x in range(-20, VW + 60, 30)]
    d.polygon(hill + [(VW + 60, VH), (-20, VH)], fill=(11, 13, 18))
    x = -30
    while x < VW + 30:
        base = 950 + 30 * np.sin(x / 310)
        h = r.uniform(90, 270)
        w = h * r.uniform(0.28, 0.4)
        for k in range(4):  # ragged tiers
            yy = base - h + h * k * 0.22
            ww = w * (0.35 + k * 0.22)
            d.polygon([(x + r.normal(0, 3), base - h + k * h * 0.12), (x - ww / 2, yy + h * 0.32), (x + ww / 2, yy + h * 0.32)], fill=(7, 9, 13))
        d.rectangle((x - 3, base - 20, x + 3, base + 20), fill=(7, 9, 13))
        x += r.uniform(14, 46)

    house_col, yg = (4, 5, 8), 1185
    windows = []

    def house(x, w, wh, rh, skew, wins, chimney=True):
        lean = skew * wh
        d.polygon([(x - w / 2, yg), (x + w / 2, yg), (x + w / 2 + lean, yg - wh), (x - w / 2 + lean, yg - wh)], fill=house_col)
        apex = x + lean * 1.5 + r.uniform(-18, 18)
        d.polygon([(x - w / 2 + lean - 18, yg - wh + 4), (x + w / 2 + lean + 18, yg - wh + 4), (apex, yg - wh - rh)], fill=house_col)
        if chimney:
            cx = x + w * 0.22 + lean
            d.polygon([(cx, yg - wh - rh * 0.3), (cx + 24, yg - wh - rh * 0.38), (cx + 28, yg - wh - rh * 0.85), (cx + 2, yg - wh - rh * 0.8)], fill=house_col)
        for fx, fy in wins:
            wx = x + fx * w + lean * fy
            wy = yg - fy * wh
            windows.append((wx, wy, 13 + r.uniform(-2, 3), 17 + r.uniform(-2, 4)))

    house(240, 230, 170, 150, 0.05, [(-0.2, 0.55), (0.2, 0.6)])
    house(470, 180, 140, 170, -0.07, [(0.05, 0.5)])
    house(690, 250, 190, 130, 0.03, [(-0.25, 0.5), (0.22, 0.5), (0.0, 0.85)])
    house(915, 170, 150, 190, -0.04, [(-0.1, 0.55)])
    # church
    d.polygon([(1180, yg), (1480, yg), (1478, yg - 230), (1182, yg - 232)], fill=house_col)
    d.polygon([(1165, yg - 228), (1495, yg - 228), (1330, yg - 350)], fill=house_col)
    d.polygon([(1105, yg), (1195, yg), (1192, yg - 420), (1110, yg - 425)], fill=house_col)
    d.polygon([(1100, yg - 420), (1200, yg - 418), (1168, yg - 700)], fill=house_col)
    d.line([(1168, yg - 700), (1172, yg - 760)], fill=house_col, width=5)
    d.polygon([(1150, yg - 742), (1192, yg - 748), (1172, yg - 738)], fill=house_col)  # bent weather vane
    church_window = (1151, yg - 360, 20, 20)
    windows.append((1290, yg - 150, 16, 34))
    windows.append((1380, yg - 150, 16, 34))
    house(1640, 210, 160, 150, 0.06, [(-0.2, 0.55), (0.2, 0.55)])
    house(1860, 190, 185, 140, -0.05, [(0.0, 0.6)])
    house(2090, 260, 150, 175, 0.04, [(-0.22, 0.5), (0.25, 0.5)], chimney=False)

    ground = [(x, yg - 6 + 14 * np.sin(x / 130) + r.normal(0, 3)) for x in range(-20, VW + 60, 25)]
    d.polygon(ground + [(VW + 60, VH), (-20, VH)], fill=(3, 4, 6))
    for i, px in enumerate(range(80, 760, 62)):  # crooked fence
        a = r.normal(0, 0.12)
        h = r.uniform(80, 120)
        d.line([(px, 1300), (px + np.sin(a) * h, 1300 - np.cos(a) * h)], fill=(2, 2, 4), width=11)
    d.line([(60, 1240), (780, 1225)], fill=(2, 2, 4), width=7)

    def branch(x, y, ang, ln, wd, depth):
        x2, y2 = x + np.cos(ang) * ln, y - np.sin(ang) * ln
        d.line([(x, y), (x2, y2)], fill=(2, 2, 4), width=max(1, int(wd)))
        if depth:
            for da in (r.uniform(0.25, 0.6), -r.uniform(0.25, 0.6)):
                branch(x2, y2, ang + da, ln * r.uniform(0.6, 0.78), wd * 0.62, depth - 1)

    branch(2250, VH, np.pi / 2 + 0.12, 420, 46, 7)

    base = to_arr(img)
    lights = []
    t_offs = np.sort(r.uniform(1.3, 4.1, len(windows)))
    r.shuffle(t_offs)
    for (wx, wy, ww, wh), toff in zip(windows, t_offs):
        lights.append(((wx, wy, ww, wh), toff, WARM))
    lights.append((church_window, 4.5, PURPLE))  # the church keeps its light longest
    return Image.fromarray((base * 255).astype(np.uint8)), base, lights


GLOW_PATCH = np.exp(-(np.mgrid[-90:90, -90:90] ** 2).sum(0) / (2 * 30 ** 2)).astype(np.float32)[..., None]


def light_level(t, toff, seed):
    if t > toff:
        return 0.0
    if t > toff - 0.25:
        return 0.35 + 0.65 * (np.sin(t * 90 + seed) > 0)
    return 0.92 + 0.08 * jitter(t, seed, 14)


# ---------- scenes ----------

class Teaser:
    def __init__(self):
        self.village_img, self.village, self.lights = build_village()
        self.fog = make_fog(H, W * 2 + 400, 3)
        self.creature = load_creature()
        self.vill_col, self.vill_a = load_villager()
        self.lantern = load_lantern()
        self.spider = ink_on_black(ART / 'spider-sketches.png', BONE, (20, 250, 300, 540))
        self.web = ink_on_black(ART / 'spider-sketches.png', BONE * 0.9, (480, 0, 816, 300))
        self.veteran = ink_on_black(ART / 'veteran-concept.png', np.array([1.0, 0.42, 0.3], np.float32), (110, 0, 560, 430), outline=True)
        self.grain = [rng.standard_normal((H, W)).astype(np.float32) for _ in range(6)]
        r = np.sqrt(((XX - W / 2) / (W * 0.62)) ** 2 + ((YY - H / 2) / (H * 0.72)) ** 2)
        self.vignette = (1 - 0.75 * smooth(r - 0.35))[..., None]
        cy = H - BAR / 2
        self.captions = [
            (0.7, 3.9, text_mask('The village goes to bed at dusk.', 50, cy)),
            (5.5, 7.9, text_mask('Bring a lantern.', 50, cy)),
            (8.3, 10.4, text_mask('Granny says it only eats the curious.', 50, cy)),
            (11.65, 13.0, text_mask('You are very curious.', 50, cy)),
        ]
        self.title = text_mask(TITLE, 150, 470)
        self.title_glow = text_mask(TITLE, 150, 470, blur=28)
        self.tag = text_mask(TAGLINE, 36, 600)
        self.studio = text_mask(f'{STUDIO}   ·   Wishlist now', 30, 760)

    def fog_layer(self, t, speed, offset=0):
        x = int(offset + t * speed) % (self.fog.shape[1] - W)
        return self.fog[:, x:x + W, None]

    # 0-5 s: the village switches off, something watches from the trees
    def village_scene(self, t):
        world = self.village.copy()
        for i, ((wx, wy, ww, wh), toff, col) in enumerate(self.lights):
            k = light_level(t, toff, i * 1.7)
            if k <= 0:
                continue
            x0, y0 = int(wx - ww / 2), int(wy - wh / 2)
            world[y0:y0 + int(wh), x0:x0 + int(ww)] = col * (0.9 * k)
            gy, gx = int(wy) - 90, int(wx) - 90
            world[gy:gy + 180, gx:gx + 180] += GLOW_PATCH * col * (0.32 * k)
        if 3.4 < t < 5.0:  # eyes in the treeline
            blink = 0.0 if 4.15 < t < 4.27 else 1.0
            k = ramp(t, 3.4, 3.9) * blink
            for ex in (512, 540):
                world[921:925, ex - 5:ex + 5] += BOG * 1.2 * k
                world[903:943, ex - 20:ex + 20] += GLOW_PATCH[70:110, 70:110] * BOG * 0.18 * k
        vw = 2400 - 260 * ramp(t, 0, 5.2)
        img = cam(to_pil(world), 1200 - 40 * ramp(t, 0, 5), 675 + 60 * ramp(t, 0, 5), vw)
        band = np.exp(-((YY - 760) / 190) ** 2)[..., None] * 0.6 + smooth((YY - 820) / 260)[..., None] * 0.5
        f = self.fog_layer(t, 38) * band
        img += (np.array([0.11, 0.13, 0.15]) - img) * f * 0.55
        return img * (1 - ramp(t, 4.55, 5.0))

    # 5-8 s: a lantern sparks and swings
    def lantern_scene(self, t):
        lt = t - 5.0
        ignite = ramp(lt, 0.0, 0.35) * (0.6 + 0.4 * (np.sin(lt * 70) > -0.3)) if lt < 0.5 else 1.0
        flick = (0.88 + 0.12 * jitter(t, 2, 17)) * ignite
        ang = 9 * np.sin(lt * 2 * np.pi / 1.7 + 0.4) * np.exp(-lt * 0.18)
        scale = 1.0 + 0.06 * ramp(lt, 0, 3)
        rot = self.lantern.rotate(ang, resample=Image.BICUBIC)
        lw, lh = rot.size
        rot = rot.resize((int(lw * scale), int(lh * scale)), Image.BICUBIC)
        a = to_arr(rot) * flick
        img = np.zeros((H, W, 3), np.float32)
        px, py = W // 2 - a.shape[1] // 2, BAR + 40 - a.shape[0] // 2
        ys, xs = max(0, -py), max(0, -px)
        sub = a[ys:ys + H - max(py, 0), xs:xs + W - max(px, 0)]
        img[max(py, 0):max(py, 0) + sub.shape[0], max(px, 0):max(px, 0) + sub.shape[1]] = sub
        img[:BAR + 40, W // 2 - 2:W // 2 + 2] = 0.08 * flick  # chain
        rad = np.radians(ang)
        cx = W / 2 + np.sin(rad) * 430 * scale
        cy = BAR + 40 + np.cos(rad) * 430 * scale
        g = glow(cx, cy, 420)
        img += g * WARM * 0.32 * flick
        img += self.fog_layer(t, -55, 900) * g * WARM * 0.35 * flick
        return img

    # 8-10.5 s: granny, half in lantern light
    def granny_scene(self, t):
        lt = t - 8.0
        img = np.zeros((H, W, 3), np.float32) + np.array([0.02, 0.025, 0.035])
        s = 0.86 + 0.08 * ramp(lt, 0, 2.5)
        cw, ch = int(1080 * s), int(1440 * s)
        col = np.asarray(to_pil(self.vill_col).resize((cw, ch), Image.BICUBIC), np.float32) / 255
        al = np.asarray(Image.fromarray((self.vill_a * 255).astype(np.uint8)).resize((cw, ch), Image.BICUBIC), np.float32)[..., None] / 255
        x0, y0 = W // 2 - cw // 2 + 60 + int(30 * lt), BAR - 40
        hh = min(ch, H - y0)
        reg = img[y0:y0 + hh, x0:x0 + cw]
        img[y0:y0 + hh, x0:x0 + cw] = reg * (1 - al[:hh]) + col[:hh] * al[:hh]
        flick = 0.85 + 0.15 * jitter(t, 5, 15)
        out = ramp(lt, 2.15, 2.5)
        light = 0.12 + glow(520, 520, 680) * WARM * 1.9 * flick
        img = img * light * (1 - out * (np.sin(t * 80) > 0)) * (1 - out)
        img += self.fog_layer(t, 30, 1600) * glow(330, 700, 500) * WARM * 0.1 * flick
        return img

    # 10.5-13 s: things in the margins of the sketchbook
    def sketch_scene(self, t):
        if 10.5 <= t < 10.95:
            k = ramp(t, 10.5, 10.95)
            return cam(self.spider, 150 - 20 * k, 140, 560 - 160 * k)
        if 11.05 <= t < 11.5:
            k = ramp(t, 11.05, 11.5)
            return cam(self.web.rotate(-12 * k, resample=Image.BICUBIC), 170, 150, 470 - 90 * k)
        if 11.62 <= t < 12.6:
            k = ramp(t, 11.62, 12.6)
            img = cam(self.veteran, 225 + 10 * jitter(t, 1, 30), 190 - 15 * k, 760 - 260 * k)
            return img * (0.75 + 0.25 * (np.sin(t * 50) > -0.6))
        return np.zeros((H, W, 3), np.float32)

    # 13-17 s: lightning, then the thing itself
    def creature_scene(self, t):
        lt = t - 13.0
        frame = self.creature[int(t * 10) % len(self.creature)]
        flash = max(np.exp(-max(0, lt - 0.35) * 9) * (lt > 0.35), np.exp(-max(0, lt - 0.9) * 7) * (lt > 0.9) * 0.9)
        steady = ramp(lt, 1.4, 3.0) * (1.25 + 0.25 * jitter(t, 9, 11))
        light = max(flash * 1.6, steady)
        if lt < 3.2:
            vw = 2250 - 900 * ramp(lt, 1.2, 3.2)
            cx, cy = 480 - 30 * ramp(lt, 1.2, 3.2), 520 - 40 * ramp(lt, 1.2, 3.2)
            shake = 6 * ramp(lt, 1.5, 3.2)
        else:
            k = ramp(lt, 3.2, 3.75) ** 2
            vw = 1350 - 1150 * k
            cx, cy = 450 - 4 * k, 480 - 15 * k
            shake = 6 + 14 * k
        cx += shake * jitter(t, 3, 47)
        cy += shake * jitter(t, 8, 53)
        img = cam(frame, cx, cy, vw) * light
        if flash > 0.05:
            img += flash * 0.25 * np.array([0.7, 0.8, 1.0], np.float32)
        return img

    # 17-20 s: title card, then something blinks
    def title_scene(self, t):
        img = np.zeros((H, W, 3), np.float32)
        on = ramp(t, 17.35, 17.6)
        if 17.35 < t < 17.85:
            on *= 0.4 + 0.6 * (np.sin(t * 95) > -0.4)
        flick = 0.92 + 0.08 * jitter(t, 4, 13)
        img += self.title_glow * WARM * 0.9 * on * flick
        img += self.title * BONE * on * flick
        img += self.tag * BONE * 0.75 * ramp(t, 17.9, 18.4)
        img += self.studio * BONE * 0.55 * ramp(t, 18.5, 19.0)
        img += glow(W / 2, 470, 500) * WARM * 0.05 * on
        if 19.05 < t < 19.85:  # it was watching the title card too
            k = ramp(t, 19.05, 19.4)
            lid = 1 - 0.95 * window(t, 19.55, 19.72, 0.07, 0.07)
            eye = self.creature[0].crop((375, 405, 530, 520))
            ew, eh = 200, max(2, int(150 * lid))
            e = np.asarray(eye.resize((ew, eh), Image.BICUBIC), np.float32) / 255
            ex, ey = 1580, 240 + (150 - eh) // 2
            img[ey:ey + eh, ex:ex + ew] += e * 1.1 * k
        return img * (1 - ramp(t, 19.85, 19.95))

    def frame(self, i):
        t = i / FPS
        if t < 5.0:
            img = self.village_scene(t)
        elif t < 8.0:
            img = self.lantern_scene(t)
        elif t < 10.5:
            img = self.granny_scene(t)
        elif t < 13.0:
            img = self.sketch_scene(t)
        elif t < 17.0:
            img = self.creature_scene(t)
        else:
            img = self.title_scene(t)
        grain = 0.05 if 10.5 <= t < 17 else 0.035
        img = img * self.vignette * (1 + 0.025 * jitter(t, 1, 23))
        img += self.grain[i % len(self.grain)][..., None] * grain * (0.35 + img.mean(2, keepdims=True))
        img[:BAR] = 0
        img[H - BAR:] = 0
        for a, b, mask in self.captions:
            k = window(t, a, b, 0.35, 0.3)
            if k > 0:
                img += mask * BONE * k * (0.9 + 0.1 * jitter(t, a, 19))
        return (np.clip(img, 0, 1) * 255).astype(np.uint8)


# ---------- sound ----------

def lowpass(x, fc, order=2):
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(np.fft.rfft(x) / np.sqrt(1 + (f / fc) ** (2 * order)), len(x))


def highpass(x, fc, order=2):
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(np.fft.rfft(x) / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order)), len(x))


def make_audio(path):
    ns = int(SR * DUR)
    L, R = np.zeros(ns), np.zeros(ns)
    t = np.arange(ns) / SR
    ar = np.random.default_rng(21)

    def add(sig, start, gain=1.0, pan=0.0):
        i = int(start * SR)
        n = min(len(sig), ns - i)
        if n > 0:
            L[i:i + n] += sig[:n] * gain * np.cos((pan + 1) * np.pi / 4) * 1.414
            R[i:i + n] += sig[:n] * gain * np.sin((pan + 1) * np.pi / 4) * 1.414

    def tt(dur):
        return np.arange(int(dur * SR)) / SR

    def env(x, a, b):
        return np.clip((x - a) / max(b - a, 1e-6), 0, 1)

    def hit(dur, decay, fc, gain=1.0):
        x = tt(dur)
        return lowpass(ar.standard_normal(len(x)), fc) * np.exp(-x / decay) * gain

    def boom(dur, f0, f1, decay):
        x = tt(dur)
        ph = 2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-x / 0.12)) / SR
        return np.sin(ph) * np.exp(-x / decay) * np.minimum(1, x / 0.004)

    def bell(freq, dur=1.6, detune=0.0):
        x = tt(dur)
        f = freq * (1 + detune)
        s = np.sin(2 * np.pi * f * x) + 0.35 * np.sin(2 * np.pi * f * 2.76 * x) * np.exp(-x / 0.25) + 0.2 * np.sin(2 * np.pi * f * 5.4 * x) * np.exp(-x / 0.08)
        return s * np.exp(-x / 0.55) * np.minimum(1, x / 0.003)

    # wind and drone under everything until the hard cut at 17 s
    wind = lowpass(ar.standard_normal(ns), 420) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 6.5))
    wind2 = lowpass(ar.standard_normal(ns), 300) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 5.1 + 2))
    drone = (np.sin(2 * np.pi * 55 * t) + 0.7 * np.sin(2 * np.pi * 58.3 * t) + 0.35 * np.sin(2 * np.pi * 82.4 * t + np.sin(t * 0.7)))
    lvl = 0.25 + 0.75 * env(t, 0, 16.5)
    cut = (t < 17.0)
    L += (wind * 2.2 + drone * 0.08) * lvl * cut
    R += (wind2 * 2.2 + drone * 0.08) * lvl * cut

    # crickets that stop all at once
    for pan, f, rate, ofs in ((-0.6, 4700, 0.47, 0.0), (0.55, 5200, 0.53, 0.2)):
        x = t[:int(4.62 * SR)]
        pulses = (np.sin(2 * np.pi * 32 * x) > 0.3) * (((x + ofs) % rate) < 0.1)
        add(np.sin(2 * np.pi * f * x) * pulses * 0.035, 0, pan=pan)

    # windows going out: tiny wooden latches
    for k, s in enumerate(np.linspace(1.4, 4.4, 7)):
        add(hit(0.08, 0.012, 2500, 0.25), s + ar.uniform(-0.1, 0.1), pan=ar.uniform(-0.7, 0.7))

    # lantern: whump, creaks at each end of the swing, flame crackle
    add(hit(0.9, 0.25, 600, 1.1) + boom(0.9, 90, 50, 0.3) * 0.5, 5.0)
    for k in range(4):
        x = tt(0.35)
        creak = np.sin(2 * np.pi * (330 + 70 * np.sin(x * 9)) * x) * (np.sin(2 * np.pi * 38 * x) > 0.6) * np.sin(np.pi * x / 0.35)
        add(lowpass(creak, 1800) * 0.09, 5.2 + k * 0.85, pan=0.3 if k % 2 else -0.3)
    crackle = (ar.random(int(3 * SR)) > 0.9993) * ar.standard_normal(int(3 * SR))
    add(highpass(lowpass(crackle, 5000), 800) * 0.35, 5.1)

    # granny: a wonky music-box lullaby
    for k, (note, when) in enumerate([(659, 0.0), (784, 0.3), (740, 0.6), (587, 0.9), (659, 1.35), (523, 1.65)]):
        add(bell(note, detune=-0.004 * k) * 0.13, 8.1 + when, pan=-0.2)
    add(hit(1.2, 0.5, 300, 0.6) * np.sin(np.pi * tt(1.2) / 1.2), 10.05)  # lantern gutters

    # sketches: heartbeat speeding up, slams on every cut, skittering legs
    beat = 10.5
    while beat < 13.0:
        bpm = 75 + 85 * (beat - 10.5) / 2.5
        add(boom(0.25, 70, 45, 0.07) * 0.9, beat)
        add(boom(0.25, 65, 42, 0.06) * 0.6, beat + 0.2 * 75 / bpm)
        beat += 60 / bpm
    for s in (10.5, 11.05, 11.62):
        add(hit(0.8, 0.12, 3000, 0.9) + boom(0.8, 120, 38, 0.35) * 0.9, s)
    for span in ((10.5, 10.95), (11.05, 11.5)):
        n = int((span[1] - span[0]) * SR)
        clicks = (ar.random(n) > 0.9975) * ar.standard_normal(n)
        add(highpass(clicks, 2500) * 0.6, span[0], pan=0.4)

    # creature: two thunderclaps, a riser and a growl, then silence
    for s, g in ((13.35, 1.0), (13.9, 0.85)):
        x = tt(2.5)
        add((hit(2.5, 0.08, 6000, 1.3) + lowpass(ar.standard_normal(len(x)), 140) * np.exp(-x / 0.9) * 3) * g, s)
    x = tt(3.0)
    gl = np.exp(np.log(90) + (np.log(420) - np.log(90)) * (x / 3.0) ** 1.6)
    riser = sum(np.sin(2 * np.pi * np.cumsum(gl * m) / SR) for m in (1.0, 1.5, 2.02))
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * (4 + 14 * x / 3) * x)
    add(riser * trem * (x / 3.0) ** 2 * 0.12, 14.0)
    add(highpass(ar.standard_normal(len(x)), 1800) * (x / 3.0) ** 3 * 0.25, 14.0)
    x = tt(2.6)
    saw = 2 * ((np.cumsum(62 + 9 * np.sin(2 * np.pi * 5.5 * x)) / SR) % 1) - 1
    add(lowpass(saw * (1 + 0.6 * ar.standard_normal(len(x))), 500) * env(x, 0, 1.5) * 0.4, 14.4)

    # title: a deep thud, the lullaby again but winding down, and a wet little blink
    add(boom(3.0, 70, 30, 0.9) * 1.1 + hit(3.0, 0.6, 250, 1.0), 17.35)
    for k, (note, when) in enumerate([(659, 0.0), (784, 0.42), (740, 0.84), (587, 1.3), (659, 1.85)]):
        add(bell(note, dur=1.4, detune=-0.012 * k) * 0.12, 17.7 + when)
    x = tt(0.14)
    add(np.sin(2 * np.pi * np.cumsum(320 - 1400 * x) / SR) * np.exp(-x / 0.04) * 0.35, 19.6)

    mix = np.stack([L, R], 1)
    mix = np.tanh(mix / np.abs(mix).max() * 1.6) / np.tanh(1.6) * 0.89
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--still', type=float, nargs='*')
    ap.add_argument('--still-dir', default=str(ROOT / 'tools/teaser/stills'))
    args = ap.parse_args()
    teaser = Teaser()
    if args.still:
        out = Path(args.still_dir)
        out.mkdir(parents=True, exist_ok=True)
        for s in args.still:
            Image.fromarray(teaser.frame(int(s * FPS))).save(out / f'{s:05.2f}.png')
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wav = OUT.with_suffix('.wav')
    make_audio(wav)
    ff = subprocess.Popen([
        'ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-i', str(wav),
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '26', '-tune', 'grain', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(OUT),
    ], stdin=subprocess.PIPE)
    for i in range(N):
        ff.stdin.write(teaser.frame(i).tobytes())
        if i % 48 == 0:
            print(f'{i / FPS:5.1f}s', flush=True)
    ff.stdin.close()
    ff.wait()
    wav.unlink()
    print(OUT)


if __name__ == '__main__':
    main()
