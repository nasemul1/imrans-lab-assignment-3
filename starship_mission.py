from manim import *

class RocketLaunchScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.0)
        # Set background color safely for both renderers
        try:
            self.renderer.camera.background_color = BLACK
        except Exception:
            try:
                self.camera.background_color = BLACK
            except Exception:
                pass

        # Improved starbase pad: large, flat, placed horizontally (no rotation)
        pad = Square(side_length=6, fill_color=GRAY, fill_opacity=0.8)
        pad.move_to(ORIGIN + 0.01 * DOWN)
        self.add(pad)

        # Improved rocket: taller, upright, placed on pad
        body = Cylinder(radius=0.22, height=2.2, direction=OUT, fill_color=GREY_B, fill_opacity=1)
        nose = Cone(base_radius=0.22, height=0.5, direction=OUT, fill_color=GREY_B, fill_opacity=1)
        nose.move_to(body.get_top())
        # Add simple fins
        fin_left = Triangle(fill_color=GREY_D, fill_opacity=1).scale(0.18).rotate(PI/2, RIGHT).move_to(body.get_bottom() + 0.25*LEFT + 0.12*DOWN)
        fin_right = fin_left.copy().move_to(body.get_bottom() + 0.25*RIGHT + 0.12*DOWN)
        rocket = VGroup(body, nose, fin_left, fin_right)
        rocket.move_to(pad.get_center() + body.height/2 * UP + 0.01 * UP)
        self.add(rocket)

        # Countdown
        countdown = Text("3", font_size=64, color=YELLOW)
        countdown.to_corner(UR)
        self.add_fixed_in_frame_mobjects(countdown)
        for i in range(3, 0, -1):
            self.play(countdown.animate.become(Text(str(i), font_size=64, color=YELLOW)), run_time=0.5)
        self.play(FadeOut(countdown), run_time=0.5)

        # Simple flame effect at launch
        flame = Cone(base_radius=0.18, height=0.7, direction=IN, fill_color=ORANGE, fill_opacity=0.8)
        flame.move_to(body.get_bottom() + 0.35*IN)
        self.add(flame)
        self.play(flame.animate.scale(1.2), run_time=0.3)

        # Launch animation
        self.play(
            rocket.animate.move_to(rocket.get_center() + 6 * UP + 4 * OUT),
            flame.animate.move_to(flame.get_center() + 6 * UP + 4 * OUT).set_opacity(0),
            run_time=3,
            rate_func=rate_functions.ease_in_sine
        )

        self.play(FadeOut(pad), run_time=1)
        self.wait(0.5)
        self.wait(0.5)
