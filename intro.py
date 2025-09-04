from manim import *

# Render tips:
# Preview (fast): manim -pqh --renderer=opengl "/home/nasemul1/Documents/Python/Day 3 assignment/intro.py" LogoIntro
# High quality:   manim -pqh --renderer=opengl "/home/nasemul1/Documents/Python/Day 3 assignment/intro.py" LogoIntro

class LogoIntro(Scene):
    def construct(self):
        # Background
        try:
            self.set_background_color(BLACK)
        except Exception:
            self.camera.background_color = BLACK

        svg_path = "/home/nasemul1/Documents/Python/Day 3 assignment/logo.svg"

        # Load SVG; start with transparent fill and visible white stroke
        logo = SVGMobject(svg_path)
        logo.set_fill(WHITE, opacity=0.0)
        logo.set_stroke(WHITE, width=3)
        logo.center().scale(1.25)

        # Collect drawable parts
        parts = [m for m in logo.family_members_with_points()]

        # 1) Tracing pass: a thicker white line sweeps along each path
        tracer = VGroup(*[p.copy().set_stroke(WHITE, width=6) for p in parts])
        self.play(
            LaggedStart(*[ShowPassingFlash(t, time_width=0.25) for t in tracer],
                        lag_ratio=0.06),
            run_time=2.2,
        )

        # 2) Solidify the outline so it stays after tracing
        for p in parts:
            p.set_fill(opacity=0.0).set_stroke(WHITE, width=3)
        self.play(LaggedStart(*[Create(p) for p in parts], lag_ratio=0.02), run_time=1.0)

        # 3) Fill in white
        self.play(logo.animate.set_fill(WHITE, opacity=1.0), run_time=0.7, rate_func=smooth)

        # Optional: reduce stroke for a clean filled look
        self.play(logo.animate.set_stroke(width=0), run_time=0.4)

        self.wait(0.5)

        # Add "Imranslab" text under the logo
        imranslab_text = Text("Imranslab", color=WHITE, font_size=48)
        imranslab_text.next_to(logo, DOWN, buff=0.5)
        self.play(FadeIn(imranslab_text), run_time=0.8)

        self.wait(1)
