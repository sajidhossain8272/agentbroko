"""Easing + interpolation helpers.

clamp/smoothstep/ease_out/ramp are lifted verbatim from the original render.py so
the motion language matches; the rest extend it for the new scene library.
"""


def clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else hi if v > hi else v


def smoothstep(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def smootherstep(x):
    x = clamp(x)
    return x * x * x * (x * (x * 6 - 15) + 10)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x)
    return x ** 3


def ease_out_back(x, s=1.70158):
    x = clamp(x)
    x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def ramp(t, a, b):
    """0 before a, 1 after b, smooth in between."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return smoothstep((t - a) / (b - a))


def stagger(i, n, t, span=0.5, hold=0.28):
    """Progress (0..1) for the i-th of n items given scene progress t.

    Items enter one after another over `span` of the scene, each taking `hold`.
    """
    if n <= 1:
        start = 0.0
    else:
        start = (i / max(1, n - 1)) * max(0.0, span - hold)
    return ramp(t, start, start + hold)


def lerp(a, b, k):
    return a + (b - a) * k


def mix(c0, c1, k):
    """Blend two RGB(A) tuples."""
    k = clamp(k)
    return tuple(int(round(lerp(c0[i], c1[i], k))) for i in range(len(c0)))
