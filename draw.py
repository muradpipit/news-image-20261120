#!/usr/bin/env python3
"""Draw the front page for news-image-20261120. Deterministic, PIL only."""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 90, 86)
LINE = (40, 40, 40)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_flag(d, x, y, w, h, kind):
    """Simple geometric flag."""
    if kind == "us":
        d.rectangle([x, y, x + w, y + h], fill=(60, 59, 110), outline=INK)
        for i in range(7):
            yy = y + i * h // 7
            if i % 2 == 0:
                d.rectangle([x, yy, x + w, yy + h // 7], fill=(255, 255, 255))
        cw, chh = int(w * 0.4), h * 4 // 7
        d.rectangle([x, y, x + cw, y + chh], fill=(60, 59, 110))
        for r in range(3):
            for c in range(4):
                sx = x + 3 + c * (cw // 4)
                sy = y + 3 + r * (chh // 3)
                d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 255, 255))
    elif kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK)
        d.ellipse([x + 6, y + 6, x + 22, y + 22], fill=(255, 222, 0))
    elif kind == "ru":
        d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255), outline=INK)
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))
        d.rectangle([x, y, x + w, y + h], outline=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin

    # --- Masthead ---
    f_mast = font(FS, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 18), title, font=f_mast, fill=INK)
    d.rectangle([m, 92, W - m, 96], fill=RED)
    f_date = font(FB, 30)
    date = "Friday, 20 November 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 104), date, font=f_date, fill=RED)
    d.rectangle([m, 146, W - m, 149], fill=LINE)

    # --- Main story ---
    f_head = font(FB, 40)
    f_sub = font(FR, 21)
    head = "TRUMP, XI & PUTIN SIGN JOINT PEACE DECLARATION AT SHENZHEN SUMMIT"
    lines = wrap(d, head, f_head, W - 2 * m)
    y = 162
    for ln in lines:
        d.text((m, y), ln, font=f_head, fill=INK)
        y += 48
    sub = ("Trilateral summit ends with a shared pledge on peace; "
           "a Ukraine resolution is named the top priority.")
    for ln in wrap(d, sub, f_sub, W - 2 * m - 300):
        d.text((m, y), ln, font=f_sub, fill=INK)
        y += 27
    # three flags illustration, right side, BELOW the sub-headline.
    # Headline line 2 spans x 28-869 at y 210-250 and the sub-headline
    # occupies the left side until y~312, so the right column (x>=726)
    # is free from y=256 down to the divider at y=330. Flags are smaller
    # (62x36) and each label is centred under its own flag.
    fx, fy, fw, fh = W - m - 270, 256, 62, 36
    f_lab = font(FB, 14)
    for i, (kind, lab) in enumerate(zip(["us", "cn", "ru"],
                                        ["US", "CHINA", "RUSSIA"])):
        flag_x = fx + i * 92
        draw_flag(d, flag_x, fy, fw, fh, kind)
        lw = d.textlength(lab, font=f_lab)
        d.text((flag_x + (fw - lw) / 2, fy + fh + 5), lab,
               font=f_lab, fill=GREY)
    # handshake-ish: two clasped bars, moved below the flag labels
    hy = 316
    d.rectangle([fx, hy, fx + 130, hy + 8], fill=RED)
    d.rectangle([fx + 140, hy, fx + 270, hy + 8], fill=(30, 90, 160))
    d.ellipse([fx + 122, hy - 4, fx + 138, hy + 8], fill=(240, 200, 120), outline=INK)
    y = 330
    d.rectangle([m, y, W - m, y + 3], fill=LINE)

    # --- Secondary stories: 3 columns x 3 rows ---
    stories = [
        ("ICJ: MYANMAR GUILTY OF GENOCIDE",
         "Court rules 9-6 against Myanmar over the Rohingya - the first such verdict against a state.",
         "scales"),
        ("ANTHROPIC IPO SOARS ON NASDAQ",
         "Shares +17% to ~$97 (ticker ANT) - the first frontier AI company to go public.",
         "chart"),
        ("MARKETS FALL FOR 5TH DAY",
         "US stocks slide again; Nikkei -4.8%; Taiwan shares plunge 2,200+ points intraday.",
         "down"),
        ("HOUTHI MISSILE HITS PIF TOWER",
         "Missile damages Riyadh's PIF Tower; Houthis claim four targets struck.",
         "tower"),
        ("UKRAINE HITS KERCH BRIDGE AGAIN",
         "Third strike on the bridge this week; fresh missile attack on Kyiv on Friday.",
         "bridge"),
        ("US SENATE REJECTS IRAN WAR POWERS",
         "Resolution fails 51-48 in the Senate.",
         "vote"),
        ("KENYA SENDS HOME LAST EBOLA PATIENT",
         "Final Ebola patient discharged as the outbreak ends.",
         "cross"),
        ("UK PLEDGES 1,000+ DRONES FOR UKRAINE",
         "Part of a 260 million-pound support package.",
         "drone"),
        ("TRUMP PARDONS PETE ROSE",
         "Posthumous pardon announced for the baseball great.",
         "star"),
    ]
    f_h = font(FB, 21)
    f_b = font(FR, 17)
    gx, gy = m, 348
    cw = (W - 2 * m - 2 * 16) // 3
    ch = 208
    for i, (h, b, icon) in enumerate(stories):
        cx = gx + (i % 3) * (cw + 16)
        cy = gy + (i // 3) * (ch + 14)
        d.rectangle([cx, cy, cx + cw, cy + ch], outline=LINE, width=1)
        d.rectangle([cx, cy, cx + cw, cy + 5], fill=RED)
        # icon strip
        ix, iy = cx + 10, cy + 14
        if icon == "scales":
            d.line([ix + 20, iy, ix + 20, iy + 22], fill=INK, width=3)
            d.line([ix, iy + 4, ix + 40, iy + 4], fill=INK, width=3)
            d.ellipse([ix + 2, iy + 20, ix + 12, iy + 28], outline=INK, width=2)
            d.ellipse([ix + 28, iy + 20, ix + 38, iy + 28], outline=INK, width=2)
        elif icon == "chart":
            pts = [(ix, iy + 26), (ix + 12, iy + 18), (ix + 24, iy + 22), (ix + 40, iy + 4)]
            d.line(pts, fill=(30, 120, 60), width=3)
        elif icon == "down":
            pts = [(ix, iy + 4), (ix + 12, iy + 12), (ix + 24, iy + 10), (ix + 40, iy + 26)]
            d.line(pts, fill=RED, width=3)
        elif icon == "tower":
            d.polygon([(ix + 20, iy), (ix + 32, iy + 28), (ix + 8, iy + 28)], fill=(120, 120, 120))
            d.rectangle([ix + 16, iy + 6, ix + 24, iy + 28], fill=(60, 60, 60))
        elif icon == "bridge":
            d.arc([ix, iy + 6, ix + 40, iy + 30], 180, 360, fill=INK, width=3)
            d.line([ix, iy + 16, ix + 40, iy + 16], fill=INK, width=3)
        elif icon == "vote":
            d.rectangle([ix + 2, iy + 4, ix + 18, iy + 26], outline=INK, width=2)
            d.rectangle([ix + 22, iy + 4, ix + 38, iy + 26], outline=INK, width=2)
            d.text((ix + 6, iy + 7), "X", font=font(FB, 14), fill=RED)
        elif icon == "cross":
            d.rectangle([ix + 16, iy + 2, ix + 24, iy + 28], fill=RED)
            d.rectangle([ix + 4, iy + 10, ix + 36, iy + 18], fill=RED)
        elif icon == "drone":
            d.ellipse([ix + 4, iy + 4, ix + 12, iy + 12], outline=INK, width=2)
            d.ellipse([ix + 28, iy + 4, ix + 36, iy + 12], outline=INK, width=2)
            d.rectangle([ix + 10, iy + 14, ix + 30, iy + 20], fill=INK)
        elif icon == "star":
            d.polygon([(ix + 20, iy), (ix + 25, iy + 12), (ix + 38, iy + 12),
                       (ix + 28, iy + 20), (ix + 32, iy + 32), (ix + 20, iy + 25),
                       (ix + 8, iy + 32), (ix + 12, iy + 20), (ix + 2, iy + 12),
                       (ix + 15, iy + 12)], fill=(220, 170, 0), outline=INK)
        ty = cy + 48
        for ln in wrap(d, h, f_h, cw - 20):
            d.text((cx + 10, ty), ln, font=f_h, fill=INK)
            ty += 26
        for ln in wrap(d, b, f_b, cw - 20):
            d.text((cx + 10, ty), ln, font=f_b, fill=(50, 50, 50))
            ty += 22

    # footer
    d.rectangle([m, H - 26, W - m, H - 24], fill=LINE)
    f_f = font(FR, 15)
    foot = "THE WORLD IN ONE DAY  •  Friday, 20 November 2026  •  All the day's news in one image"
    fw = d.textlength(foot, font=f_f)
    d.text(((W - fw) / 2, H - 20), foot, font=f_f, fill=GREY)

    img.save("entry.png", optimize=True)
    data = open("entry.png", "rb").read()
    print("saved entry.png", img.size, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
