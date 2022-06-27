from manim import *

import random
import os

# Stuff to demo
# - Writing latex
class Latex(Scene):
    def construct(self):
        equation = MathTex(
            r'e^x = \sum_{n=0}^\infty \frac{1}{n!} x^n'
        )
        self.play(Write(equation), run_time=3)

# - Graphing area of integral
class Integral(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-0.1, 3.1],
            y_range = [-0.1, 2.1],
            x_axis_config = {
                'numbers_to_include': [0,1,2,3]
            }
        )
        curve = axes.plot(
            lambda x: 0.25 + 1.5/((5*(x-1.5))**2+1),
            x_range = [0, 3],
            color=BLUE_E
        )
        b = ValueTracker(0)
        line = axes.get_vertical_line(axes.i2gp(b.get_value(), curve))
        area = axes.get_area(
            curve, 
            x_range=[0,b.get_value()], 
            color=GREY, 
            opacity=0.5
        )
        line.add_updater(lambda l: 
            l.become(axes.get_vertical_line(axes.i2gp(b.get_value(), curve)))
        )
        area.add_updater(lambda a:
            a.become(axes.get_area(
                curve,
                x_range=[0,b.get_value()],
                color=GREY,
                opacity=0.5
            ))
        )
        self.add(axes, curve, line, area)
        self.wait()
        self.play(b.animate.set_value(3), run_time=3)
        self.wait(2)

# - Zooming moving camera
class MovingCamera(MovingCameraScene):
    def construct(self):
        for i in range(1,9):
            self.add(Circle(radius=i))
        d1 = Dot(3*LEFT+2*UP, radius=0.1)
        d2 = Dot(3*LEFT+2*DOWN, radius=0.1)
        self.add(d1, d2)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.3).move_to(d1))
        self.play(self.camera.frame.animate.move_to(d2))
        self.play(self.camera.frame.animate.move_to(2*RIGHT))
        self.play(Restore(self.camera.frame))
        

# - Moving object around based on equation
class MovingObject(Scene):
    def construct(self):
        random.seed('boo')
        for _ in range(40):
            x = 6*(2*random.random()-1)
            y = 4*(2*random.random()-1)
            self.add(Dot(x*RIGHT+y*UP, radius=0.05))
        sq = Square(side_length=1, color=GREEN_E).set_fill(GREEN_B, opacity=0.3)
        self.play(Create(sq))
        self.wait()
        t = ValueTracker(0)
        def parabola(t):
            x = 10/3*t-5
            y = -6*(x-5)*(x+5)/25-3
            return x,y
        def trace_para(mob):
            x, y = parabola(t.get_value())
            mob.set_x(x)
            mob.set_y(y)
        self.play(sq.animate.move_to([-5,-3,0]))
        self.wait()
        sq.add_updater(trace_para)
        self.play(t.animate.set_value(3), run_time=3)
        self.wait()

# - Custom colors (including bg color)
class ColorPallet:
    def __init__(self, bg, fg, purple, blue, green, yellow, orange, red):
        self.bg = bg
        self.fg = fg
        self.purple = purple
        self.blue = blue
        self.green = green
        self.yellow = yellow
        self.orange = orange
        self.red = red
        self.spectrum = [self.purple, self.blue, self.green, self.yellow, self.orange, self.red]

    def show_pallet(self, label):
        bg = Rectangle(width=12, height=2, color=self.bg)
        bg.set_fill(self.bg, opacity=1)
        pallet = Group(bg)
        pallet.add(Line(start=[-5.85, 0, 0], end=[5.85, 0, 0], color=self.fg))
        for i, c in enumerate(self.spectrum):
            sq = Square(side_length=1.5, color=c).set_fill(c, opacity=0.5)
            sq.move_to([-5+2*i, 0, 0])
            pallet.add(sq)
        pallet.add(Text(label).next_to([-6,1,0],DR))
        return pallet

class CustomColors(MovingCameraScene):
    def construct(self):
        default_pallet = ColorPallet(BLACK, WHITE, PURPLE, BLUE, GREEN, YELLOW, ORANGE, RED)
        solarized_pallet = ColorPallet('#073642','#EEE8D5', '#6C71C4', '#268BD2', '#859900', '#B58900', '#CB4B16', '#DC322F')
        tomorrow_pallet = ColorPallet('#1D1F21', '#C5C8C6', '#B294BB', '#81A2BE', '#B5BD68', '#F0C674', '#DE935F', '#CC6666')
        eighties_pallet = ColorPallet('#2D2D2D', '#CCCCCC', '#CC99CC', '#6699CC', '#99CC99', '#FFCC66', '#F99157', '#F2777A')
        bright_pallet = ColorPallet('#000000', '#EAEAEA', '#C397D8', '#7AA6DA', '#B9CA4A', '#E7C547', '#E78C45', '#D54E53')
        pallets = [default_pallet, solarized_pallet, tomorrow_pallet, eighties_pallet, bright_pallet]
        labels = ['Default', 'Solarized', 'Tomorrow', 'Tomorrow Eighties', 'Tomorrow Bright']
        cur_pallet = pallets[0].show_pallet(labels[0])
        self.add(cur_pallet)
        self.wait(2)
        for p, l in zip(pallets[1:], labels[1:]):
            self.play(FadeOut(cur_pallet))
            # self.play(self.camera.frame.animate.set_background(p.bg))
            cur_pallet = p.show_pallet(l)
            self.play(FadeIn(cur_pallet))
            self.wait(2)

# - Create and load SVG
class StillSvgs(Scene):
    def construct(self):
        #   - lines only
        rocket = SVGMobject(os.path.join('assets','rocket_lines.svg'))
        rocket.set(height=6, color=BLUE)
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for smo, c in zip(rocket.submobjects, colors):
            self.play(Create(smo.set(color=c)))
            self.wait(1)
        self.play(FadeOut(rocket))
        #   - filled/stacked polygons
        rocket = SVGMobject(os.path.join('assets','rocket_polygons.svg'))
        rocket.set(height=6, color=BLUE)
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for smo, c in zip(rocket.submobjects, colors):
            self.play(Create(smo.set(color=c)))
            self.wait(1)
        self.play(FadeOut(rocket))
        #   - filled/stacked polygons with groupe
        rocket = SVGMobject(os.path.join('assets','rocket_fin_group.svg'), unpack_groups=False)
        rocket.set(height=6, color=BLUE)
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for smo, c in zip(rocket.submobjects, colors):
            self.play(Create(smo.set(color=c)))
            self.wait(1)
        self.play(FadeOut(rocket))
        #   - lines + filled/stacked polygons with holes
        rocket = SVGMobject(os.path.join('assets','rocket_with_hole.svg'), unpack_groups=False)
        rocket.set(height=6, color=BLUE)
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for smo, c in zip(rocket.submobjects, colors):
            self.play(Create(smo.set(color=c)))
            self.wait(1)

# - Animating SVGs
#   - Swapping in place
#   - Animating between frames
class KittySvg(Scene):
    def construct(self):
        kitty = SVGMobject(os.path.join('assets','face_forward.svg'))
        look_forward = SVGMobject(os.path.join('assets','face_forward.svg'))
        look_right = SVGMobject(os.path.join('assets','face_right.svg'))
        look_left = SVGMobject(os.path.join('assets','face_left.svg'))
        for obj in [kitty, look_forward, look_right, look_left]:
            obj.set(
                # height=4,
                color=BLUE_E,
                # stroke=WHITE,
            )
        self.play(FadeIn(look_forward))
        self.wait(1)
        self.remove(look_forward)
        self.add(look_right)
        self.wait(1)
        self.remove(look_right)
        self.add(look_left)
        self.wait(1)
        self.remove(look_left)
        self.add(look_forward)
        self.play(FadeOut(look_forward))
        self.wait(1)
        self.play(Create(kitty), run_time=2)
        self.wait()
        self.play(Transform(kitty, look_forward))
        self.play(Transform(kitty, look_right))
        self.play(Transform(kitty, look_left))
        self.play(Transform(kitty, look_right))
        self.play(Transform(kitty, look_forward))
        self.wait()
