"""pill_list — vertically stacked outlined chips, staggered in. Reference: the
"Speech to Text / Turn Taking / ..." column on the dark act.

scene fields: items: ["label", ...], optional align_jitter (bool)."""

from ._common import color_for, drift, enter, new_canvas, rise_dy


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    items = ctx.scene.get("items") or []
    n = max(1, len(items))

    ph = 78.0          # pill height
    gap = 26.0
    pad_x = 44.0
    block_h = n * ph + (n - 1) * gap
    top = (H - block_h) / 2 + drift(p)

    stroke = cv.pal["stroke"]
    text_col = cv.pal["ink"] if ctx.act == "dark" else cv.pal["ink"]

    # gentle horizontal zig so the column feels hand-placed, like the reference
    jitter = ctx.scene.get("align_jitter", True)
    offsets = [(-34 if i % 2 else 30) if jitter else 0 for i in range(n)]

    for i, label in enumerate(items):
        label = str(label)
        k = enter(p, 0.05 + i * (0.5 / n), 0.4)
        if k <= 0.003:
            continue
        size = 36
        tw = cv.measure(label, "regular", size)
        pw = tw + pad_x * 2
        cx = W / 2 + offsets[i]
        y = top + i * (ph + gap) + rise_dy(k, 26)
        cv.pill(cx - pw / 2, y, pw, ph, outline=stroke, width=1.4, alpha=k)
        cv.text_center(cx, y + ph / 2, label, "regular", size, text_col, alpha=k)
    return cv.finish()
