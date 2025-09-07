from manim import *
import random

# Constants for clarity
BG_COLOR = "#02030A"
PAD_WIDTH = 8
PAD_HEIGHT = 0.5
TOWER_WIDTH = 0.25
TOWER_HEIGHT = 2.4
ROCKET_ALTITUDE = 0.9
TOWER_ROCKET_GAP = 0.06

def make_ship(scale=1.0, color=GREY_B):
    body = RoundedRectangle(width=0.46, height=1.6, corner_radius=0.12).set_fill(color, 1).set_stroke(DARK_GREY, 2)
    nose = Triangle().scale(0.22).set_fill(color, 1).set_stroke(DARK_GREY, 2)
    nose.next_to(body, UP, buff=-0.02)
    cap = Ellipse(width=0.36, height=0.12).set_fill(color, 1).set_stroke(DARK_GREY, 1)
    cap.move_to(body.get_top() + 0.02 * DOWN)
    stripe1 = Rectangle(width=0.34, height=0.06).set_fill(WHITE, 0.12).set_stroke(width=0).move_to(body.get_center()+0.18*UP)
    stripe2 = Rectangle(width=0.34, height=0.06).set_fill(WHITE, 0.08).set_stroke(width=0).move_to(body.get_center()-0.05*UP)
    w1 = Circle(radius=0.06, fill_color=BLACK, fill_opacity=0.85).move_to(body.get_center()+0.35*UP)
    w2 = Circle(radius=0.06, fill_color=BLACK, fill_opacity=0.85).move_to(body.get_center()+0.05*UP)
    w3 = Circle(radius=0.06, fill_color=BLACK, fill_opacity=0.85).move_to(body.get_center()+0.25*DOWN)
    rim = VGroup(*(c.copy().set_fill(opacity=0).set_stroke(WHITE, 1, opacity=0.35) for c in (w1,w2,w3)))
    fin_l = Triangle().scale(0.2).set_fill(GREY_D,1).set_stroke(DARK_GREY,1)
    fin_l.rotate(PI/6).move_to(body.get_bottom()+0.15*LEFT+0.06*DOWN)
    fin_r = fin_l.copy().rotate(-PI/3).move_to(body.get_bottom()+0.15*RIGHT+0.06*DOWN)
    bell_l = Ellipse(width=0.12, height=0.08).set_fill(DARK_GREY,1).set_stroke(DARK_GREY,1).move_to(body.get_bottom()+0.12*LEFT+0.08*DOWN)
    bell_m = Ellipse(width=0.12, height=0.08).set_fill(DARK_GREY,1).set_stroke(DARK_GREY,1).move_to(body.get_bottom()+0.0*DOWN+0.08*DOWN)
    bell_r = Ellipse(width=0.12, height=0.08).set_fill(DARK_GREY,1).set_stroke(DARK_GREY,1).move_to(body.get_bottom()+0.12*RIGHT+0.08*DOWN)
    nozzle = Circle(radius=0.04, fill_color=ORANGE, fill_opacity=0.0).move_to(body.get_bottom()+0.08*DOWN)
    ship = VGroup(body, cap, nose, stripe1, stripe2, w1, w2, w3, rim, fin_l, fin_r, bell_l, bell_m, bell_r, nozzle)
    ship.scale(scale)
    return ship

def make_stars(n=120, w=14, h=8, seed=0, opacity=0.5):
    random.seed(seed)
    g = VGroup()
    for _ in range(n):
        x = random.uniform(-w/2, w/2)
        y = random.uniform(-h/2, h/2)
        r = random.uniform(0.005, 0.02)
        g.add(Dot(point=[x,y,0], radius=r, color=WHITE).set_opacity(opacity))
    return g

# New small helpers for clarity
def make_pad():
    """Create the landing pad."""
    return Rectangle(width=PAD_WIDTH, height=PAD_HEIGHT).set_fill(GRAY_D, 1).set_stroke(GRAY_B, 2)

def make_tower():
    """Create the tower/stand."""
    column = Rectangle(width=TOWER_WIDTH, height=TOWER_HEIGHT).set_fill(GRAY_E, 1).set_stroke(GRAY_C, 2)
    arm = Line(LEFT*0.15 + UP*(TOWER_HEIGHT/2 - 0.0), RIGHT*0.15 + UP*(TOWER_HEIGHT/2 - 0.0), stroke_width=3, color=GRAY_C)
    return VGroup(column, arm).arrange(DOWN, buff=0)

def make_flame_for(rocket: VMobject) -> VGroup:
    """Create an exhaust flame positioned under the rocket."""
    flame = VGroup(
        Polygon([0, -0.05, 0], [0.08, -0.5, 0], [-0.08, -0.5, 0], color=ORANGE, fill_opacity=0.6).scale(0.9)
    )
    return flame.move_to(rocket.get_bottom() + 0.18*DOWN).set_opacity(0.2)

def layout_dock(pad: VMobject, tower: VMobject, rocket: VMobject, gap=TOWER_ROCKET_GAP, lift=ROCKET_ALTITUDE) -> VGroup:
    """Place tower and rocket side-by-side above the pad."""
    pair = VGroup(tower, rocket).arrange(RIGHT, buff=gap)
    pair.move_to(pad.get_top() + lift*UP)
    pad.next_to(pair, DOWN, buff=0)
    return pair

class StarbaseDock(MovingCameraScene):
    def construct(self):
        # Simplified background setup
        try:
            self.camera.background_color = BG_COLOR
        except Exception:
            pass

        frame = self.camera.frame

        stars = make_stars(n=160, w=30, h=18, seed=3, opacity=0.35)
        self.add(stars)

        # Build cleanly with helpers
        pad = make_pad().move_to(DOWN*2.8)
        tower = make_tower()
        rocket = make_ship(scale=1.0, color=TEAL)
        pad_tower_rocket = layout_dock(pad, tower, rocket)

        sign = Text("STARBASE", font_size=28, color=WHITE).next_to(pad, UP, buff=0.15)
        flood_l = Circle(radius=0.08, fill_color=YELLOW, fill_opacity=0.6).move_to(pad.get_left()+RIGHT*0.8+UP*0.2)
        flood_r = flood_l.copy().move_to(pad.get_right()+LEFT*0.8+UP*0.2)

        flame = make_flame_for(rocket)

        base_group = VGroup(pad, pad_tower_rocket, sign, flood_l, flood_r, flame)
        self.play(FadeIn(base_group, shift=0.4*UP), run_time=1.0)

        self.play(
            frame.animate.move_to(rocket.get_center()).scale(0.9),
            stars.animate.shift(LEFT*1.6),
            run_time=2.2,
            rate_func=rate_functions.ease_in_out_quart
        )

        self.play(rocket.animate.shift(0.06*UP), flame.animate.set_opacity(0.45), run_time=0.6, rate_func=there_and_back)
        self.play(rocket.animate.shift(-0.06*UP), flame.animate.set_opacity(0.2), run_time=0.6, rate_func=there_and_back)

        self.play(frame.animate.move_to(pad.get_center()).scale(1.1), stars.animate.shift(RIGHT*0.8), run_time=2)
        self.wait(0.8)

        # --- Launch Animation ---
        launch_distance = 8
        self.play(
            rocket.animate.shift(UP*launch_distance),
            flame.animate.shift(UP*launch_distance).set_opacity(0.7),
            FadeOut(VGroup(pad, tower, sign, flood_l, flood_r), shift=0.5*DOWN),
            run_time=2.5,
            rate_func=rate_functions.ease_in_cubic
        )

        # --- Earth Orbit Animation ---
        earth = Circle(radius=1.2, color=BLUE, fill_opacity=0.7).set_fill(BLUE_E, 1)
        earth.move_to(UP*6)
        orbit = Arc(radius=2.2, angle=PI, color=WHITE, stroke_width=3).move_to(earth.get_center())
        self.play(FadeIn(earth), FadeIn(orbit), run_time=1)

        # Move rocket past the orbit
        self.play(
            rocket.animate.move_to(earth.get_center() + UP*2.5),
            flame.animate.move_to(earth.get_center() + UP*2.32).set_opacity(0.3),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )

        # Fade out rocket and flame as it leaves scene
        self.play(FadeOut(rocket), FadeOut(flame), run_time=1)
        self.wait(0.5)