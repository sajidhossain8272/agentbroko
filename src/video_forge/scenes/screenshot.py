"""screenshot — a supplied image presented in a rounded device frame with a slow
Ken Burns push. Optional caption line beneath. Falls back to a placeholder card
if the image is missing or unreadable, so a spec never hard-fails on a bad path.

scene fields: image (path), caption (optional), fit ("contain"|"cover", default
"cover"), zoom (float end-scale, default 1.06)."""

import os

from PIL import Image

from ..easing import ease_out, lerp, ramp, smoothstep
from ._common import enter, new_canvas


def _load(path):
    if not path or not os.path.exists(path):
        return None
    try:
        im = Image.open(path)
        im.load()
        return im.convert("RGB")
    except (OSError, ValueError):
        return None


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    caption = ctx.scene.get("caption", "")

    # frame geometry (design units)
    margin_x = 260.0
    top = 150.0
    fw = W - margin_x * 2
    fh = (H - top * 2) - (90 if caption else 0)
    fx, fy = (W - fw) / 2, top
    r = 26.0

    ke = enter(p, 0.0, 0.5)
    dy = (1.0 - ke) * 26.0
    fy += dy

    im = _load(ctx.scene.get("image"))
    if im is None:
        # graceful placeholder
        cv.card(fx, fy, fw, fh, r=r, fill=cv.pal["card2"], alpha=ke, elevate=30)
        cv.text_center(W / 2, fy + fh / 2, ctx.scene.get("image", "screenshot"),
                       "medium", 34, cv.pal["faint"], alpha=ke)
        if caption:
            cv.text_center(W / 2, fy + fh + 52, caption, "regular", 30,
                           cv.pal["muted"], alpha=ke)
        return cv.finish()

    # Ken Burns: slow push-in over the hold.
    zoom_end = float(ctx.scene.get("zoom", 1.06))
    z = lerp(1.0, zoom_end, smoothstep(p))
    fit = ctx.scene.get("fit", "cover")

    # target pixel box inside the frame
    pfw, pfh = cv.s(fw), cv.s(fh)
    iw, ih = im.size
    scale_contain = min(pfw / iw, pfh / ih)
    scale_cover = max(pfw / iw, pfh / ih)
    base = scale_cover if fit == "cover" else scale_contain
    scale = base * z
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    im2 = im.resize((nw, nh), Image.Resampling.LANCZOS)

    # center-crop / center the scaled image to the frame box, with a gentle pan
    pan = int((z - 1.0) * pfw * 0.10)
    left = (nw - pfw) // 2 + pan
    upper = (nh - pfh) // 2
    left = max(0, min(left, max(0, nw - pfw)))
    upper = max(0, min(upper, max(0, nh - pfh)))
    if nw >= pfw and nh >= pfh:
        crop = im2.crop((left, upper, left + pfw, upper + pfh))
    else:
        crop = Image.new("RGB", (pfw, pfh), tuple(cv.pal["card2"][:3]))
        crop.paste(im2, ((pfw - nw) // 2, (pfh - nh) // 2))

    # rounded-corner mask
    mask = Image.new("L", (pfw, pfh), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pfw - 1, pfh - 1],
                                           radius=cv.s(r), fill=255)

    cv.drop_shadow(fx, fy, fw, fh, r, spread=34,
                   alpha=(0.14 if cv.act == "light" else 0.5) * ke, dy=14)
    if ke < 0.999:
        mask = mask.point(lambda v: int(v * ease_out(ke)))
    cv.img.paste(crop, (cv.s(fx), cv.s(fy)), mask)
    # thin containing stroke
    cv.rrect(fx, fy, fw, fh, r, outline=cv.pal["stroke"], width=1.2, alpha=ke)

    if caption:
        kc = ease_out(ramp(p, 0.25, 0.7))
        cv.text_center(W / 2, fy + fh + 52, caption, "regular", 30,
                       cv.pal["muted"], alpha=kc)
    return cv.finish()
