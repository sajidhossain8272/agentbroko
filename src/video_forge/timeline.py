"""Timeline: turn a normalized spec into a time-addressable sequence of frames.

Scenes are laid end-to-end with a short overlap; during the overlap the outgoing
and incoming scenes cross-dissolve. A global fade eases from/to the background at
the head and tail. `frame_at(t)` renders the composited RGB frame at time `t`.

Durations are VO-driven when a per-scene duration list is supplied (Phase 2);
otherwise each scene falls back to spec.default_duration (silent proof renders).
`scene_start(i)` exposes each scene's start time so the audio stage can place VO
on the exact same clock.
"""

from PIL import Image

from .context import FrameCtx
from .easing import clamp, smoothstep
from .spec import default_duration
from .scenes import REGISTRY
from .theme import Theme


class _Seg:
    __slots__ = ("scene", "act", "index", "start", "dur")

    def __init__(self, scene, act, index, start, dur):
        self.scene = scene
        self.act = act
        self.index = index
        self.start = start
        self.dur = dur

    @property
    def end(self):
        return self.start + self.dur


class Timeline:
    def __init__(self, spec, durations=None):
        self.spec = spec
        self.theme = Theme(spec)
        self.scenes = spec["scenes"]
        v = spec["video"]
        self.fps = int(v["fps"])
        self.xfade = float(v.get("crossfade", 0.45))
        self.fade_in = float(v.get("fade_in", 0.6))
        self.fade_out = float(v.get("fade_out", 0.9))

        durs = self._resolve_durations(durations)
        self.segs = []
        start = 0.0
        for i, (sc, d) in enumerate(zip(self.scenes, durs)):
            self.segs.append(_Seg(sc, sc["act"], i, start, d))
            # next scene overlaps by a clamped crossfade
            if i + 1 < len(durs):
                xf = min(self.xfade, 0.5 * d, 0.5 * durs[i + 1])
                start = start + d - xf
        self.total = self.segs[-1].end if self.segs else 0.0
        self._bg_cache = {}

    # -- durations ---------------------------------------------------------
    def _resolve_durations(self, durations):
        out = []
        for i, sc in enumerate(self.scenes):
            if sc.get("duration"):
                out.append(float(sc["duration"]))
            elif durations and i < len(durations) and durations[i]:
                out.append(float(durations[i]))
            else:
                out.append(default_duration(sc))
        return out

    def total_seconds(self):
        return self.total

    def frame_count(self):
        return max(1, int(round(self.total * self.fps)))

    def scene_start(self, i):
        return self.segs[i].start

    def scene_duration(self, i):
        return self.segs[i].dur

    # -- rendering ---------------------------------------------------------
    def _bg(self, act):
        img = self._bg_cache.get(act)
        if img is None:
            img = Image.new("RGB", (self.theme.W, self.theme.H),
                            self.theme.palette(act)["bg"])
            self._bg_cache[act] = img
        return img

    def _render_seg(self, seg, t):
        local = t - seg.start
        p = clamp(local / seg.dur) if seg.dur > 0 else 1.0
        ctx = FrameCtx(theme=self.theme, scene=seg.scene, act=seg.act,
                       p=p, t=local, dur=seg.dur, index=seg.index,
                       total=len(self.segs))
        return REGISTRY[seg.scene["type"]](ctx)

    def _active(self, t):
        return [s for s in self.segs if s.start - 1e-6 <= t < s.end - 1e-6] \
            or [self.segs[-1] if t >= self.total else self.segs[0]]

    def frame_at(self, t):
        active = self._active(t)
        if len(active) == 1:
            frame = self._render_seg(active[0], t)
            dom_act = active[0].act
        else:
            a, b = active[0], active[1]
            overlap = a.end - b.start
            w = clamp((t - b.start) / overlap) if overlap > 1e-6 else 1.0
            fa = self._render_seg(a, t)
            fb = self._render_seg(b, t)
            frame = Image.blend(fa, fb, smoothstep(w))
            dom_act = b.act if w >= 0.5 else a.act

        f = self._fade_factor(t)
        if f < 0.999:
            frame = Image.blend(self._bg(dom_act), frame, f)
        return frame

    def _fade_factor(self, t):
        f = 1.0
        if self.fade_in > 0 and t < self.fade_in:
            f = min(f, t / self.fade_in)
        tail = self.total - t
        if self.fade_out > 0 and tail < self.fade_out:
            f = min(f, tail / self.fade_out)
        return clamp(f)

    def frames(self):
        """Yield every RGB frame in order (generator)."""
        n = self.frame_count()
        for i in range(n):
            yield self.frame_at(i / self.fps)
