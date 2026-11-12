"""
Fractions and Decimals: multiplication and division (Class 7 maths),
narrated by an Indian-English voice.

Step 1 - make the voice-over (offline, one time):

    pip install kokoro-onnx soundfile
    python fractions_decimals/generate_voiceover.py

Step 2 - render the video with the voice-over:

    manimgl fractions_decimals/fractions_decimals.py FractionsAndDecimals -w --hd

Each chapter is also its own scene (e.g. ``MultiplyingFractions``,
``DividingDecimals``) for quick previews.  If the voice-over files are
missing, the scenes still render silently with estimated timings.
"""
from __future__ import annotations

import os
import sys
import textwrap
from contextlib import contextmanager

from manimlib import *
from pydub import AudioSegment

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from narration import NARRATION  # noqa: E402

VOICE_DIR = os.path.join(HERE, "voiceover")

BG_COLOR = "#14302A"      # chalkboard green
NUM_COLOR = YELLOW        # numerators
DEN_COLOR = BLUE_B        # denominators
ACCENT = ORANGE
GOOD = GREEN_B
FONT = "Sans"

# manimgl's default LaTeX template loads the `physics` package, which turns
# \div into the divergence operator (a nabla).  Restore the plain ÷ sign.
DIV_FIX = R'\renewcommand{\div}{\mathchar"2204\relax}'
_Tex = Tex


def Tex(*tex_strings, **kwargs):
    kwargs["additional_preamble"] = kwargs.get("additional_preamble", "") + DIV_FIX
    return _Tex(*tex_strings, **kwargs)


# --------------------------------------------------------------------------
# Building blocks
# --------------------------------------------------------------------------
def T(text, font_size=36, color=WHITE, **kwargs):
    return Text(text, font=FONT, font_size=font_size, color=color, **kwargs)


class Frac(VGroup):
    """A fraction built from separate pieces so they can be animated."""

    def __init__(self, num, den, font_size=72, num_color=NUM_COLOR, den_color=DEN_COLOR, **kwargs):
        num = Tex(str(num), font_size=font_size).set_color(num_color)
        den = Tex(str(den), font_size=font_size).set_color(den_color)
        width = max(num.get_width(), den.get_width()) + 0.2 * font_size / 72
        bar = Line(LEFT, RIGHT).set_width(width).set_stroke(WHITE, 4 * font_size / 72)
        num.next_to(bar, UP, buff=0.12 * font_size / 72)
        den.next_to(bar, DOWN, buff=0.12 * font_size / 72)
        super().__init__(num, bar, den, **kwargs)
        self.num, self.bar, self.den = num, bar, den


def expr(*items, font_size=72, buff=0.28):
    """Lay out fractions / numbers / symbols in a row, centred on the bars."""
    mobs = [
        Tex(item, font_size=font_size) if isinstance(item, str) else item
        for item in items
    ]
    row = VGroup(*mobs).arrange(RIGHT, buff=buff)
    for mob in mobs:
        if isinstance(mob, Frac):
            mob.shift((row.get_y() - mob.bar.get_y()) * UP)
    return row


def flip_into(src: Frac, dst: Frac):
    """Animations that turn a copy of ``src`` upside down into ``dst``."""
    return [
        TransformFromCopy(src.num, dst.den, path_arc=-PI),
        TransformFromCopy(src.den, dst.num, path_arc=-PI),
        TransformFromCopy(src.bar, dst.bar),
    ]


class DecimalRow:
    """
    Digits sitting in fixed place-value slots with a decimal point that
    hops between them.  Slot ``i`` is at ``x0 + i * spacing``; the point at
    position ``k`` sits between slot ``k - 1`` and slot ``k``.
    """

    def __init__(self, digits: str, k: int, x0=0.0, y=0.0, font_size=110, spacing=0.8, color=WHITE):
        self.font_size = font_size
        self.spacing = spacing
        self.x0 = x0
        self.y = y
        self.color = color
        self.slots: dict[int, Tex] = {}
        for i, char in enumerate(digits):
            self.slots[i] = self._digit(char, i)
        ref = self.slots[0]
        self.baseline = ref.get_bottom()[1]
        self.point = Dot(radius=0.09 * font_size / 110, fill_color=ACCENT)
        self.point.move_to(self._point_loc(k))
        self.k = k
        self.group = VGroup(*self.slots.values(), self.point)

    def _digit(self, char, i):
        d = Tex(char, font_size=self.font_size).set_color(self.color)
        d.move_to([self.x0 + i * self.spacing, self.y, 0])
        return d

    def _point_loc(self, k):
        return np.array([
            self.x0 + (k - 0.5) * self.spacing,
            self.baseline + self.point.get_height() / 2,
            0,
        ])

    def digits_mob(self):
        return VGroup(*(self.slots[i] for i in sorted(self.slots)))

    def _opacity_updates(self):
        """Dim zeros that do not count (leading zeros, a point at the end)."""
        lo, hi = min(self.slots), max(self.slots)
        anims = []
        for i in range(lo, hi + 1):
            significant = True
            if i < self.k - 1:   # integer part, check leading zeros
                if all(self.slots[j].get_tex() == "0" for j in range(lo, i + 1)):
                    significant = False
            if i >= self.k:      # fractional part, check trailing zeros
                if all(self.slots[j].get_tex() == "0" for j in range(i, hi + 1)):
                    significant = False
            anims.append(self.slots[i].animate.set_opacity(1 if significant else 0.25))
        point_visible = self.k <= hi
        anims.append(self.point.animate.set_opacity(1 if point_visible else 0.2))
        return anims

    def move_point(self, scene: Scene, steps: int, hop_time=0.6, arc_color=ACCENT):
        """Hop the decimal point ``steps`` places (positive = right)."""
        target = self.k + steps
        lo = min(min(self.slots), target - 1)
        hi = max(max(self.slots), target - 1)
        new_zeros = []
        for i in range(lo, hi + 1):
            if i not in self.slots:
                self.slots[i] = self._digit("0", i).set_color(arc_color)
                new_zeros.append(self.slots[i])
                self.group.add(self.slots[i])
        if new_zeros:
            scene.play(LaggedStart(*(FadeIn(z, scale=1.5) for z in new_zeros), lag_ratio=0.3), run_time=0.6)

        arcs = VGroup()
        direction = 1 if steps > 0 else -1
        for n in range(abs(steps)):
            start = self._point_loc(self.k)
            self.k += direction
            end = self._point_loc(self.k)
            arc = Arrow(
                start + 0.15 * DOWN, end + 0.15 * DOWN,
                path_arc=direction * PI * 0.8, buff=0.05,
                thickness=3, fill_color=arc_color,
            )
            count = Integer(n + 1, font_size=30, color=arc_color).next_to(arc, DOWN, buff=0.08)
            arcs.add(VGroup(arc, count))
            scene.play(
                self.point.animate.move_to(end).set_opacity(1),
                GrowArrow(arc), FadeIn(count),
                run_time=hop_time,
            )
        scene.play(*self._opacity_updates(), run_time=0.4)
        return arcs


# --------------------------------------------------------------------------
# A scene that speaks
# --------------------------------------------------------------------------
class VoiceScene(Scene):
    default_camera_config = dict(background_color=BG_COLOR)
    subtitles = True

    def setup(self):
        super().setup()
        self.header = None
        self.caption = None

    @contextmanager
    def voice(self, key, pad=0.35):
        """
        Play the narration clip ``key`` while the animations inside the
        ``with`` block run; then wait until the clip has finished.
        """
        path = next(
            (p for p in (os.path.join(VOICE_DIR, f"{key}.{ext}") for ext in ("mp3", "wav")) if os.path.exists(p)),
            None,
        )
        if path:
            duration = AudioSegment.from_file(path).duration_seconds
            self.add_sound(path)
        else:
            duration = len(NARRATION[key].split()) / 2.5
        if self.subtitles:
            self.show_caption(NARRATION[key])
        start = self.time
        yield duration
        remaining = duration + pad - (self.time - start)
        if remaining > 0.02:
            self.wait(remaining)

    def show_caption(self, text):
        lines = textwrap.wrap(text, 72)
        caption = VGroup(*(T(line, font_size=26, color=GREY_A) for line in lines))
        caption.arrange(DOWN, buff=0.1)
        caption.to_edge(DOWN, buff=0.22)
        back = BackgroundRectangle(caption, fill_opacity=0.55, buff=0.12)
        new = VGroup(back, caption)
        new.fix_in_frame()
        if self.caption is not None:
            self.remove(self.caption)
        self.add(new)
        self.caption = new

    def set_header(self, text, color=YELLOW):
        title = T(text, font_size=44, color=color, weight=BOLD)
        title.to_corner(UL, buff=0.45)
        line = Underline(title, stretch_factor=1.05).set_stroke(color, 3)
        new = VGroup(title, line)
        if self.header is None:
            self.play(Write(title), ShowCreation(line), run_time=1)
        else:
            self.play(FadeTransform(self.header, new), run_time=0.8)
        self.header = new
        return new

    def clear_board(self, keep_header=False, run_time=0.7):
        keep = {self.caption}
        if keep_header:
            keep.add(self.header)
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*(FadeOut(m) for m in mobs), run_time=run_time)
        if not keep_header:
            self.header = None


# --------------------------------------------------------------------------
# Chapters
# --------------------------------------------------------------------------
class Lesson(VoiceScene):
    """Mixin holding every chapter of the lesson as a method."""

    # ---------------------------------------------------------------- intro
    def intro(self):
        title = T("Fractions and Decimals", font_size=84, weight=BOLD)
        title.set_color_by_gradient(YELLOW, ORANGE)
        sub = T("Multiplication and Division", font_size=42, color=BLUE_B)
        sub.next_to(title, DOWN, buff=0.4)
        cls = T("Class 7  •  Mathematics", font_size=28, color=GREY_B)
        cls.next_to(sub, DOWN, buff=0.5)

        with self.voice("intro_1"):
            self.play(Write(title), run_time=2)
            self.play(FadeIn(sub, shift=UP), FadeIn(cls), run_time=1)

        with self.voice("intro_2"):
            self.play(VGroup(title, sub, cls).animate.scale(0.6).to_edge(UP, buff=0.4), run_time=1)
            learnt = T("Already learnt:", font_size=34, color=GREY_A)
            ex1 = expr(Frac(1, 4, 60), "+", Frac(2, 4, 60), "=", Frac(3, 4, 60), font_size=60)
            ex2 = Tex(R"0.5 + 0.2 = 0.7", font_size=60)
            ex3 = Tex(R"0.9 - 0.4 = 0.5", font_size=60)
            recap = VGroup(ex1, ex2, ex3).arrange(RIGHT, buff=1.0)
            group = VGroup(learnt, recap).arrange(DOWN, buff=0.5).shift(0.2 * DOWN)
            self.play(FadeIn(learnt))
            self.play(LaggedStart(*(FadeIn(m, shift=UP) for m in recap), lag_ratio=0.4), run_time=2)
            ticks = VGroup(*(
                Checkmark().set_color(GOOD).scale(1.2).next_to(m, DOWN, buff=0.3) for m in recap
            ))
            self.play(LaggedStartMap(Write, ticks, lag_ratio=0.3))

        with self.voice("intro_3"):
            self.play(FadeOut(group), FadeOut(ticks))
            boxes = VGroup()
            labels = [
                (R"\times", "Fractions", NUM_COLOR),
                (R"\div", "Fractions", NUM_COLOR),
                (R"\times", "Decimals", BLUE_B),
                (R"\div", "Decimals", BLUE_B),
            ]
            for sym, word, col in labels:
                rect = RoundedRectangle(width=2.8, height=2.0, corner_radius=0.2)
                rect.set_stroke(col, 3).set_fill(col, 0.08)
                s = Tex(sym, font_size=90).set_color(col)
                w = T(word, font_size=28)
                inner = VGroup(s, w).arrange(DOWN, buff=0.25).move_to(rect)
                boxes.add(VGroup(rect, inner))
            boxes.arrange(RIGHT, buff=0.4).shift(0.3 * DOWN)
            self.play(LaggedStartMap(FadeIn, boxes, shift=UP, lag_ratio=0.35), run_time=3)
            self.play(LaggedStart(*(Indicate(b[1][0]) for b in boxes), lag_ratio=0.3), run_time=2)
        self.clear_board()

    # ---------------------------------------------------- multiply fractions
    def multiplying_fractions(self):
        with self.voice("mul_1"):
            self.set_header("Multiplication of Fractions")
            rule = Tex(
                R"\text{Product} = "
                R"{\text{Product of numerators} \over \text{Product of denominators}}",
                font_size=46,
                t2c={"numerators": NUM_COLOR, "denominators": DEN_COLOR},
            )
            rule.shift(1.6 * UP)
            self.play(Write(rule), run_time=3)

        f1, f2 = Frac(2, 3), Frac(5, 7)
        prod = Frac(R"2 \times 5", R"3 \times 7")
        ans = Frac(10, 21)
        full = expr(f1, R"\times", f2, "=", prod, "=", ans)
        full.shift(0.6 * DOWN)
        lhs = full[:3]
        eq1, eq2 = full[3], full[5]

        with self.voice("mul_2"):
            self.play(LaggedStart(*(FadeIn(m, shift=UP) for m in lhs), lag_ratio=0.3), run_time=1.5)

        with self.voice("mul_3"):
            num_box = SurroundingRectangle(VGroup(f1.num, f2.num), buff=0.15).set_stroke(NUM_COLOR, 3)
            self.play(ShowCreation(num_box), FadeIn(eq1))
            self.play(
                TransformFromCopy(f1.num, prod.num["2"][0]),
                TransformFromCopy(f2.num, prod.num["5"][0]),
                Write(prod.num[R"\times"][0]),
                ShowCreation(prod.bar),
                run_time=1.2,
            )
            den_box = SurroundingRectangle(VGroup(f1.den, f2.den), buff=0.15).set_stroke(DEN_COLOR, 3)
            self.play(ReplacementTransform(num_box, den_box))
            self.play(
                TransformFromCopy(f1.den, prod.den["3"][0]),
                TransformFromCopy(f2.den, prod.den["7"][0]),
                Write(prod.den[R"\times"][0]),
                run_time=1.2,
            )
            self.play(FadeOut(den_box))

        with self.voice("mul_4"):
            self.play(FadeIn(eq2))
            self.play(TransformFromCopy(prod.num, ans.num), run_time=1)
            self.play(TransformFromCopy(prod.bar, ans.bar), TransformFromCopy(prod.den, ans.den), run_time=1)
            box = SurroundingRectangle(ans, buff=0.2).set_stroke(GOOD, 4)
            self.play(ShowCreation(box), FlashAround(ans, color=GOOD))
        self.clear_board()

    # ------------------------------------------------------ fraction as "of"
    def fraction_of(self):
        with self.voice("of_1"):
            self.set_header("A Fraction as the Operator 'of'")
            question = Tex(R"\frac{1}{2} \text{ of } 2 = \; ?", font_size=80)
            question.shift(2.1 * UP)
            self.play(Write(question))

        def roti():
            r = Circle(radius=0.9).set_fill("#D9A441", 1).set_stroke("#8B5A2B", 4)
            spots = VGroup(*(
                Dot(radius=0.06, fill_color="#8B5A2B").move_to(
                    r.get_center() + 0.55 * np.array([np.cos(a), np.sin(a), 0]) * (0.5 + 0.5 * ((i * 37) % 7) / 7)
                )
                for i, a in enumerate(np.linspace(0, TAU, 9)[:-1])
            ))
            return VGroup(r, spots)

        rotis = VGroup(roti(), roti()).arrange(RIGHT, buff=1.2).shift(1.1 * DOWN)
        with self.voice("of_2"):
            self.play(LaggedStartMap(GrowFromCenter, rotis, lag_ratio=0.4), run_time=1.5)
            brace = Brace(rotis, UP)
            two = brace.get_tex("2").set_color(NUM_COLOR)
            self.play(GrowFromCenter(brace), FadeIn(two))
            divider = DashedLine(UP, DOWN).set_height(2.4).move_to(rotis)
            divider.set_stroke(WHITE, 3)
            self.play(ShowCreation(divider))
            halves = VGroup(
                SurroundingRectangle(rotis[0], buff=0.15),
                SurroundingRectangle(rotis[1], buff=0.15),
            ).set_stroke(GREY_B, 2)
            self.play(ShowCreation(halves))

        with self.voice("of_3"):
            self.play(
                halves[0].animate.set_stroke(GOOD, 5),
                rotis[1].animate.set_opacity(0.25),
                halves[1].animate.set_stroke(opacity=0.3),
            )
            one = Tex("1", font_size=72).set_color(GOOD).next_to(halves[0], DOWN, buff=0.2)
            self.play(Write(one))
            answer = Tex(R"\frac{1}{2} \text{ of } 2 = \frac{1}{2} \times 2 = 1", font_size=72)
            answer.move_to(question)
            answer["1"][-1].set_color(GOOD)
            self.play(FadeTransform(question, answer), run_time=1.5)
        self.clear_board()

    # --------------------------------------------- size of the product
    def product_size(self):
        with self.voice("cmp_1"):
            self.set_header("How Big is the Product?")
            line = NumberLine((0, 3, 1), unit_size=3.4, include_numbers=True, tick_size=0.12)
            line.numbers.set_color(GREY_B)
            line.shift(0.35 * DOWN)
            # sixths
            small_ticks = VGroup(*(
                Line(UP, DOWN).set_height(0.12).set_stroke(GREY_C, 1.5).move_to(line.n2p(x / 6))
                for x in range(1, 18) if x % 6
            ))
            self.play(ShowCreation(line), FadeIn(small_ticks), run_time=1.5)

        cases = [
            ("cmp_2", "Proper × Proper", (1, 2), (1, 3), (1, 6),
             R"\frac{1}{6} < \frac{1}{3} \quad\text{and}\quad \frac{1}{6} < \frac{1}{2}",
             "Product is LESS than both"),
            ("cmp_3", "Proper × Improper", (1, 2), (5, 3), (5, 6),
             R"\frac{1}{2} < \frac{5}{6} < \frac{5}{3}",
             "Product is BETWEEN the two"),
            ("cmp_4", "Improper × Improper", (3, 2), (5, 3), (5, 2),
             R"\frac{5}{2} > \frac{3}{2} \quad\text{and}\quad \frac{5}{2} > \frac{5}{3}",
             "Product is GREATER than both"),
        ]
        shown = VGroup()
        for key, name, a, b, p, compare, verdict in cases:
            with self.voice(key):
                if len(shown):
                    self.play(FadeOut(shown), run_time=0.5)
                title = T(name, font_size=34, color=ACCENT).to_edge(UP, buff=1.25)
                fa, fb, fp = Frac(*a, 54), Frac(*b, 54), Frac(*p, 54, GOOD, GOOD)
                equation = expr(fa, R"\times", fb, "=", fp, font_size=54)
                equation.next_to(title, DOWN, buff=0.25)
                self.play(FadeIn(title), Write(equation), run_time=1.2)

                dots, labels = VGroup(), VGroup()
                for (n, d), col in [(a, BLUE_B), (b, BLUE_B), (p, GOOD)]:
                    dot = Dot(line.n2p(n / d), radius=0.1, fill_color=col)
                    lab = Frac(n, d, 40, col, col)
                    lab.next_to(dot, UP, buff=0.25)
                    dots.add(dot)
                    labels.add(lab)
                self.play(
                    LaggedStart(*(GrowFromCenter(d) for d in dots[:2]), lag_ratio=0.3),
                    LaggedStart(*(FadeIn(l, shift=DOWN) for l in labels[:2]), lag_ratio=0.3),
                )
                arrow = Arrow(
                    dots[0].get_center() + 0.2 * DOWN, dots[2].get_center() + 0.2 * DOWN,
                    path_arc=PI / 2 if p[0] / p[1] > a[0] / a[1] else -PI / 2,
                    buff=0.1, fill_color=GOOD, thickness=3,
                )
                self.play(
                    TransformFromCopy(dots[0], dots[2], path_arc=-PI / 2),
                    GrowArrow(arrow),
                    TransformFromCopy(fp, labels[2]),
                    run_time=1.2,
                )
                result = VGroup(
                    Tex(compare, font_size=44),
                    T(verdict, font_size=30, color=GOOD),
                ).arrange(DOWN, buff=0.2).next_to(line, DOWN, buff=0.6)
                self.play(Write(result[0]), run_time=1.2)
                self.play(FadeIn(result[1], shift=UP))
                shown = VGroup(title, equation, dots, labels, arrow, result)
        self.clear_board()

    # ------------------------------------------------------------ reciprocal
    def reciprocal(self):
        f = Frac(3, 5, 130)
        f.shift(3 * LEFT + 0.2 * DOWN)
        r = Frac(5, 3, 130)
        r.shift(3 * RIGHT + 0.2 * DOWN)
        with self.voice("rec_1"):
            self.set_header("Reciprocal of a Fraction")
            self.play(FadeIn(f, scale=0.8))
            turn = Arrow(f.get_right() + 0.3 * RIGHT + 0.6 * UP, r.get_left() + 0.3 * LEFT + 0.6 * UP,
                         path_arc=-PI / 3, fill_color=ACCENT, thickness=5)
            word = T("Turn it upside down!", font_size=32, color=ACCENT).next_to(turn, UP, buff=0.2)
            self.play(GrowArrow(turn), FadeIn(word))
            self.play(*flip_into(f, r), run_time=2)

        with self.voice("rec_2"):
            lab1 = T("fraction", font_size=30, color=GREY_B).next_to(f, DOWN, buff=0.4)
            lab2 = T("reciprocal", font_size=30, color=GOOD).next_to(r, DOWN, buff=0.4)
            self.play(FadeIn(lab1), FadeIn(lab2))
            self.play(Indicate(f.num), Indicate(r.den), run_time=1.2)
            self.play(Indicate(f.den), Indicate(r.num), run_time=1.2)
            check = Tex(R"\frac{3}{5} \times \frac{5}{3} = 1", font_size=56).to_edge(DOWN, buff=1.6)
            self.play(Write(check))
        self.clear_board()

    # -------------------------------------------------------------- division
    def dividing_fractions(self):
        rows_y = [1.55, -0.1, -1.75]
        tags = ["(a) Whole ÷ Fraction", "(b) Fraction ÷ Whole", "(c) Fraction ÷ Fraction"]
        font = 56

        def tag(i):
            return T(tags[i], font_size=26, color=ACCENT).move_to([-4.7, rows_y[i], 0])

        def place(row, i):
            row.move_to([1.4, rows_y[i], 0])
            return row

        # (a) 2 ÷ 3/5 = 2 × 5/3 = 10/3
        with self.voice("div_1"):
            self.set_header("Division of Fractions")
            t = tag(0)
            self.play(FadeIn(t, shift=RIGHT))
            rule = T("multiply by the reciprocal", font_size=30, color=GOOD).to_edge(UP, buff=0.55).to_edge(RIGHT)
            self.play(Write(rule))
        a_src, a_rec, a_ans = Frac(3, 5, font), Frac(5, 3, font), Frac(10, 3, font, GOOD, GOOD)
        row = place(expr("2", R"\div", a_src, "=", "2", R"\times", a_rec, "=", a_ans, font_size=font), 0)
        with self.voice("div_2"):
            self.play(Write(row[:3]))
            self.play(
                FadeIn(row[3]), TransformFromCopy(row[0], row[4]),
                TransformFromCopy(row[1], row[5]), *flip_into(a_src, a_rec), run_time=1.5,
            )
            self.play(FadeIn(row[7]), FadeIn(a_ans, shift=LEFT))

        # (b) 2/3 ÷ 7 = 2/3 × 1/7 = 2/21
        with self.voice("div_3"):
            self.play(FadeIn(tag(1), shift=RIGHT))
        b1, b2, b_rec, b_ans = Frac(2, 3, font), Frac(2, 3, font), Frac(1, 7, font), Frac(2, 21, font, GOOD, GOOD)
        row = place(expr(b1, R"\div", "7", "=", b2, R"\times", b_rec, "=", b_ans, font_size=font), 1)
        with self.voice("div_4"):
            self.play(Write(row[:3]))
            self.play(
                FadeIn(row[3]), TransformFromCopy(b1, b2), TransformFromCopy(row[1], row[5]),
                TransformFromCopy(row[2], b_rec.den, path_arc=-PI / 2),
                FadeIn(b_rec.num), ShowCreation(b_rec.bar), run_time=1.5,
            )
            self.play(FadeIn(row[7]), FadeIn(b_ans, shift=LEFT))

        # (c) 2/3 ÷ 5/7 = 2/3 × 7/5 = 14/15
        with self.voice("div_5"):
            self.play(FadeIn(tag(2), shift=RIGHT))
        c1, c2, c3, c_rec, c_ans = (
            Frac(2, 3, font), Frac(5, 7, font), Frac(2, 3, font), Frac(7, 5, font), Frac(14, 15, font, GOOD, GOOD)
        )
        row = place(expr(c1, R"\div", c2, "=", c3, R"\times", c_rec, "=", c_ans, font_size=font), 2)
        with self.voice("div_6"):
            self.play(Write(row[:3]))
            self.play(
                FadeIn(row[3]), TransformFromCopy(c1, c3), TransformFromCopy(row[1], row[5]),
                *flip_into(c2, c_rec), run_time=1.5,
            )
            self.play(FadeIn(row[7]), FadeIn(c_ans, shift=LEFT))
            self.play(FlashAround(c_ans, color=GOOD))
        self.clear_board()

    # ------------------------------------------------- multiplying decimals
    def multiplying_decimals(self):
        problem = Tex(R"0.5 \times 0.7", font_size=96).shift(1.6 * UP)
        with self.voice("dmul_1"):
            self.set_header("Multiplication of Decimals", color=BLUE_B)
            self.play(Write(problem), run_time=1.5)

        step1 = Tex(R"5 \times 7 = 35", font_size=72).shift(2.5 * LEFT + 0.3 * DOWN)
        s1_label = T("Step 1: multiply as whole numbers", font_size=26, color=ACCENT)
        s1_label.next_to(step1, UP, buff=0.3)
        with self.voice("dmul_2"):
            self.play(FadeIn(s1_label))
            self.play(
                TransformFromCopy(problem["5"][0], step1["5"][0]),
                TransformFromCopy(problem["7"][0], step1["7"][0]),
                TransformFromCopy(problem[R"\times"][0], step1[R"\times"][0]),
            )
            self.play(Write(step1["= 35"]))

        with self.voice("dmul_3"):
            s2_label = T("Step 2: count decimal places", font_size=26, color=ACCENT)
            s2_label.move_to(3.3 * RIGHT + 0.2 * UP)
            self.play(FadeIn(s2_label))
            marks = VGroup()
            for part in (problem["5"][0], problem["7"][0]):
                ul = Underline(part, buff=0.08).set_stroke(ACCENT, 5)
                one = Tex("1", font_size=40).set_color(ACCENT).next_to(ul, DOWN, buff=0.1)
                marks.add(VGroup(ul, one))
                self.play(ShowCreation(ul), FadeIn(one, shift=DOWN), run_time=0.8)
            count = Tex(R"1 + 1 = 2 \text{ places}", font_size=48).set_color(ACCENT)
            count.next_to(s2_label, DOWN, buff=0.35)
            self.play(Write(count))

        with self.voice("dmul_4"):
            s3_label = T("Step 3: place the point, 2 places from the right", font_size=26, color=ACCENT)
            s3_label.move_to(2.0 * DOWN + 1.5 * LEFT)
            row = DecimalRow("35", 2, x0=-2.6, y=-2.0 - 0.0, font_size=90, spacing=0.6)
            row.group.next_to(s3_label, RIGHT, buff=0.8)
            # rebuild at that location so slot positions are consistent
            x0 = row.slots[0].get_x()
            row = DecimalRow("35", 2, x0=x0, y=s3_label.get_y(), font_size=90, spacing=0.6)
            row.point.set_opacity(0)
            self.play(FadeIn(s3_label), TransformFromCopy(step1["35"][0], row.digits_mob()))
            self.add(row.point)
            arcs = row.move_point(self, -2, hop_time=0.8)
            answer = Tex(R"0.5 \times 0.7 = 0.35", font_size=72).set_color(GOOD)
            answer.move_to(problem)
            self.play(FadeOut(arcs), TransformMatchingTex(problem, answer), FadeOut(marks))
            self.play(FlashAround(answer, color=GOOD))
        self.clear_board()

    def decimal_times_powers_of_ten(self):
        with self.voice("p10_1"):
            self.set_header("Multiplying by 10, 100, 1000", color=BLUE_B)
            rule = T("Point moves RIGHT  →  one place for each zero", font_size=32, color=ACCENT)
            rule.next_to(self.header, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
            self.play(Write(rule))
        results = VGroup()
        for key, factor, steps, answer in [
            ("p10_2", "10", 1, "5.3"),
            ("p10_3", "100", 2, "53"),
            ("p10_4", "1000", 3, "530"),
        ]:
            with self.voice(key):
                row = DecimalRow("053", 1, x0=-5.2, y=-0.3)
                label = Tex(R"\times " + factor, font_size=60).next_to(row.digits_mob(), UP, buff=0.6)
                label.set_x(row.slots[1].get_x() + 0.3)
                label[factor[1:]].set_color(ACCENT)
                self.play(FadeIn(row.group), FadeIn(label))
                arcs = row.move_point(self, steps, hop_time=0.55)
                res = Tex(R"0.53 \times " + factor + " = " + answer, font_size=52)
                res[-len(answer):].set_color(GOOD)
                res.move_to([3.3, 0.8 - 1.0 * len(results), 0])
                self.play(FadeIn(res, shift=LEFT))
                results.add(res)
                self.play(FadeOut(VGroup(row.group, arcs, label)), run_time=0.5)
        self.clear_board()

    # ------------------------------------------------- dividing decimals
    def decimal_by_whole(self):
        with self.voice("ddiv_1"):
            self.set_header("Division of Decimals", color=BLUE_B)
            tag = T("(a) Decimal ÷ Whole number", font_size=30, color=ACCENT)
            tag.next_to(self.header, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
            self.play(FadeIn(tag, shift=RIGHT))
        problem = Tex(R"8.4 \div 4", font_size=90).shift(1.0 * UP)
        whole = Tex(R"84 \div 4 = 21", font_size=72).shift(0.6 * DOWN)
        with self.voice("ddiv_2"):
            self.play(Write(problem))
            self.play(
                TransformFromCopy(problem["8"][0], whole["8"][0]),
                TransformFromCopy(problem["4"][0], whole["4"][0]),
                TransformFromCopy(problem[R"\div 4"][0], whole[R"\div 4"][0]),
            )
            self.play(Write(whole["= 21"]))
        with self.voice("ddiv_3"):
            # glyphs: 8 . 4 ÷ 4 = 2 . 1
            final = Tex(R"8.4 \div 4 = 2.1", font_size=90).move_to(problem)
            final[-3:].set_color(GOOD)
            point_box = SurroundingRectangle(problem[1], buff=0.08).set_stroke(ACCENT, 3)
            self.play(ShowCreation(point_box))
            self.play(
                ReplacementTransform(problem, final[:5]),
                FadeOut(point_box),
                FadeIn(final[5]),
                TransformFromCopy(whole[-2], final[-3]),   # 2
                TransformFromCopy(whole[-1], final[-1]),   # 1
                run_time=1.2,
            )
            self.play(GrowFromCenter(final[-2]), Flash(final[-2], color=ACCENT))
            note = T("Note: only divisions with remainder zero", font_size=26, color=GREY_B)
            note.next_to(whole, DOWN, buff=0.8)
            self.play(FadeIn(note))
        self.clear_board()

    def decimal_by_powers_of_ten(self):
        with self.voice("d10_1"):
            self.set_header("Dividing by 10, 100, 1000", color=BLUE_B)
            rule = T("Point moves LEFT  ←  one place for each zero", font_size=32, color=ACCENT)
            rule.next_to(self.header, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
            self.play(Write(rule))
        results = VGroup()
        for key, factor, steps, answer in [
            ("d10_2", "10", 1, "2.39"),
            ("d10_3", "100", 2, "0.239"),
            ("d10_4", "1000", 3, "0.0239"),
        ]:
            with self.voice(key):
                row = DecimalRow("239", 2, x0=-3.0, y=-0.3, font_size=100, spacing=0.72)
                label = Tex(R"\div " + factor, font_size=60).move_to([-2.6, 1.1, 0])
                label[factor[1:]].set_color(ACCENT)
                self.play(FadeIn(row.group), FadeIn(label))
                arcs = row.move_point(self, -steps, hop_time=0.55)
                res = Tex(R"23.9 \div " + factor + " = " + answer, font_size=50)
                res[-len(answer):].set_color(GOOD)
                res.move_to([3.6, 0.8 - 1.0 * len(results), 0])
                self.play(FadeIn(res, shift=LEFT))
                results.add(res)
                self.play(FadeOut(VGroup(row.group, arcs, label)), run_time=0.5)
        self.clear_board()

    def decimal_by_decimal(self):
        with self.voice("dd_1"):
            self.set_header("Decimal ÷ Decimal", color=BLUE_B)
            rule = T("Shift the point equally in both, until the divisor is a whole number",
                     font_size=28, color=ACCENT)
            rule.next_to(self.header, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
            self.play(Write(rule), run_time=2)

        top = DecimalRow("24", 1, x0=-3.2, y=0.2, font_size=100, spacing=0.72)
        bottom = DecimalRow("02", 1, x0=1.6, y=0.2, font_size=100, spacing=0.72)
        div = Tex(R"\div", font_size=100).move_to([(-3.2 + 0.72 + 1.6) / 2, 0.2, 0])
        div.set_x((top.slots[1].get_right()[0] + bottom.slots[0].get_left()[0]) / 2)
        lab_a = T("dividend", font_size=24, color=GREY_B).next_to(top.digits_mob(), UP, buff=0.4)
        lab_b = T("divisor", font_size=24, color=GREY_B).next_to(bottom.digits_mob(), UP, buff=0.4)
        with self.voice("dd_2"):
            self.play(FadeIn(top.group), FadeIn(div), FadeIn(bottom.group), FadeIn(lab_a), FadeIn(lab_b))
            arcs_a = top.move_point(self, 1, hop_time=0.7)
            arcs_b = bottom.move_point(self, 1, hop_time=0.7)
            times = Tex(R"\text{(both} \times 10)", font_size=36).set_color(ACCENT)
            times.next_to(div, DOWN, buff=1.1)
            self.play(FadeIn(times))

        with self.voice("dd_3"):
            answer = Tex(R"2.4 \div 0.2 = 24 \div 2 = 12", font_size=72).shift(2.0 * DOWN)
            answer["12"].set_color(GOOD)
            self.play(FadeOut(VGroup(arcs_a, arcs_b, times)), Write(answer), run_time=1.5)
            self.play(FlashAround(answer["12"], color=GOOD))
        self.clear_board()

    # --------------------------------------------------------------- summary
    def summary(self):
        with self.voice("sum_1"):
            self.set_header("Quick Revision", color=GOOD)
        items = VGroup(
            Tex(R"\frac{a}{b} \times \frac{c}{d} = \frac{a \times c}{b \times d}", font_size=44),
            Tex(R"\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \times \frac{d}{c}", font_size=44),
            Tex(R"0.5 \times 0.7 = 0.35 \quad (1 + 1 = 2 \text{ places})", font_size=40),
            Tex(R"0.53 \times 100 = 53 \quad (\text{point} \rightarrow)", font_size=40),
            Tex(R"23.9 \div 100 = 0.239 \quad (\text{point} \leftarrow)", font_size=40),
            Tex(R"2.4 \div 0.2 = 24 \div 2 = 12", font_size=40),
        )
        cards = VGroup()
        for item in items:
            rect = RoundedRectangle(width=6.2, height=1.25, corner_radius=0.15)
            rect.set_stroke(GREY_B, 2).set_fill(BLACK, 0.25)
            item.set_max_width(5.8).move_to(rect)
            cards.add(VGroup(rect, item))
        cards.arrange_in_grid(3, 2, h_buff=0.4, v_buff=0.3).shift(0.15 * DOWN)
        with self.voice("sum_2"):
            self.play(LaggedStartMap(FadeIn, cards, shift=UP, lag_ratio=0.5), run_time=6)
        with self.voice("sum_3"):
            self.play(FadeOut(cards), FadeOut(self.header))
            self.header = None
            bye = T("Thank you, students!", font_size=72, weight=BOLD)
            bye.set_color_by_gradient(YELLOW, ORANGE)
            hw = T("Practise at home  •  See you in the next class", font_size=32, color=BLUE_B)
            VGroup(bye, hw).arrange(DOWN, buff=0.5)
            self.play(Write(bye), run_time=1.5)
            self.play(FadeIn(hw, shift=UP))
        self.wait(0.5)


# --------------------------------------------------------------------------
# Renderable scenes
# --------------------------------------------------------------------------
class FractionsAndDecimals(Lesson):
    """The complete lesson (about 6 minutes)."""

    def construct(self):
        self.intro()
        self.multiplying_fractions()
        self.fraction_of()
        self.product_size()
        self.reciprocal()
        self.dividing_fractions()
        self.multiplying_decimals()
        self.decimal_times_powers_of_ten()
        self.decimal_by_whole()
        self.decimal_by_powers_of_ten()
        self.decimal_by_decimal()
        self.summary()


class Intro(Lesson):
    def construct(self):
        self.intro()


class MultiplyingFractions(Lesson):
    def construct(self):
        self.multiplying_fractions()
        self.fraction_of()
        self.product_size()


class DividingFractions(Lesson):
    def construct(self):
        self.reciprocal()
        self.dividing_fractions()


class MultiplyingDecimals(Lesson):
    def construct(self):
        self.multiplying_decimals()
        self.decimal_times_powers_of_ten()


class DividingDecimals(Lesson):
    def construct(self):
        self.decimal_by_whole()
        self.decimal_by_powers_of_ten()
        self.decimal_by_decimal()


class Summary(Lesson):
    def construct(self):
        self.summary()
