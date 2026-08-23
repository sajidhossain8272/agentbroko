"""node_stack — nested rounded cards in columns (a system/architecture diagram).
Reference: the "Your agent" + "Integrations" beat.

scene fields:
  columns: [ { "title": str, "rows": [ row, ... ] }, ... ]
    where a row is either a string (full-width sub-card) or a list of strings
    (split into equal sub-cards on one line).
  Falls back to a single column built from `items` if `columns` is absent.

Column width is derived from the canvas rather than fixed, and in portrait the
columns stack vertically: a fixed side-by-side width overflowed 1080-wide frames
and clipped both the titles and the outer cells.
"""

from ..theme import accent_family
from ._common import (bg_wash, content_w, enter, is_portrait, new_canvas,
                      rise_dy, side_margin)

HDR_H = 70.0
ROW_H = 66.0
RGAP = 14.0
COL_GAP = 64.0
STACK_GAP = 46.0
MAX_COL_W = 600.0


def _columns(scene):
    cols = scene.get("columns")
    if cols:
        return cols
    return [{"title": scene.get("title", ""), "rows": scene.get("items", [])}]


def _col_height(col):
    h = (HDR_H + RGAP) if col.get("title") else 0.0
    rows = col.get("rows", [])
    h += len(rows) * (ROW_H + RGAP)
    return h - RGAP if h else 0.0


def render(ctx):
    cv = new_canvas(ctx)
    W, H = cv.W, cv.H
    p = ctx.p
    bg_wash(cv, p, 0.9)

    cols = _columns(ctx.scene)
    ncol = len(cols)
    margin = side_margin(cv)
    avail = content_w(cv)
    stacked = is_portrait(cv) and ncol > 1

    if stacked:
        col_w = avail
        total_h = sum(_col_height(c) for c in cols) + STACK_GAP * (ncol - 1)
        top0 = (H - total_h) / 2
    else:
        col_w = min(MAX_COL_W, (avail - COL_GAP * (ncol - 1)) / ncol)
        total_w = col_w * ncol + COL_GAP * (ncol - 1)
        x0 = (W - total_w) / 2
        top0 = (H - max(_col_height(c) for c in cols)) / 2

    fam = accent_family(cv.accent, ncol, spread=0.03)
    ink_dark = (24, 24, 24)
    y_cursor = top0

    for i, col in enumerate(cols):
        acc = fam[i]
        kcol = enter(p, 0.04 + i * 0.12, 0.4)
        cx0 = margin if stacked else x0 + i * (col_w + COL_GAP)
        y = (y_cursor if stacked else top0) + rise_dy(kcol, 22)

        title = col.get("title")
        if title:
            cv.card(cx0, y, col_w, HDR_H, r=16, alpha=kcol, elevate=22)
            cv.grad_rrect(cx0, y, col_w, HDR_H, 16,
                          cv.tint(acc, 0.30), cv.tint(acc, 0.10), alpha=kcol)
            cv.ellipse(cx0 + 40, y + HDR_H / 2, 11, fill=acc, alpha=kcol)
            tsize = cv.fit_size(title, "medium", 30, col_w - 100, min_size=18)
            cv.text(cx0 + 68, y + HDR_H / 2, title, "medium", tsize, ink_dark,
                    anchor="lm", alpha=kcol)
            y += HDR_H + RGAP

        for j, row in enumerate(col.get("rows", [])):
            kr = enter(p, 0.12 + i * 0.1 + j * 0.06, 0.4)
            cells = row if isinstance(row, list) else [row]
            m = len(cells)
            sw = (col_w - RGAP * (m - 1)) / m
            for c, cell in enumerate(cells):
                sx = cx0 + c * (sw + RGAP)
                cv.grad_rrect(sx, y, sw, ROW_H, 14,
                              cv.tint(acc, 0.15), cv.tint(acc, 0.05), alpha=kr)
                size = cv.fit_size(str(cell), "regular", 26, sw - 40, min_size=16)
                cv.text_center(sx + sw / 2, y + ROW_H / 2, str(cell), "regular",
                               size, ink_dark, alpha=kr)
            y += ROW_H + RGAP

        if stacked:
            y_cursor += _col_height(col) + STACK_GAP
    return cv.finish()
