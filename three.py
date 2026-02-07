import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from manim import *

# the TracedPath mobjects don't like caching for some reason :(
config.disable_caching = True


# the data
SQRT3 = np.sqrt(3)

def pos_r1(t):
    return np.array([
        3/4*np.cos(t/SQRT3) + 3/4*np.sin(t/SQRT3) + 1/4*np.cos(t) - SQRT3/4*np.sin(t),
        -SQRT3/4*np.cos(t/SQRT3) + 3*SQRT3/4*np.sin(t/SQRT3) + SQRT3/4*np.cos(t) + 1/4*np.sin(t),
        0
    ])

def pos_r2(t):
    return np.array([
        -3/4*np.cos(t/SQRT3) - 3/4*np.sin(t/SQRT3) + 1/4*np.cos(t) - SQRT3/4*np.sin(t),
        SQRT3/4*np.cos(t/SQRT3) - 3*SQRT3/4*np.sin(t/SQRT3) + SQRT3/4*np.cos(t) + 1/4*np.sin(t),
        0
    ])

def pos_r3(t):
    return np.array([
        -1/2*np.cos(t) + SQRT3/2*np.sin(t),
        -SQRT3/2*np.cos(t) - 1/2*np.sin(t),
        0
    ])

# data for steady state motion

def rot(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

class DemoIntro(MovingCameraScene):
    def construct(self):
        # make the mobjects
        dot_1 = Dot(np.array([1, 0, 0]), color=BLUE_E, radius=0.1, z_index=2, sheen_factor=0.8)
        dot_2 = Dot(np.array([1, 0, 0])@rot(TAU/3), color=BLUE_E, radius=0.1, z_index=2, sheen_factor=0.8)
        dot_3 = Dot(np.array([1, 0, 0])@rot(2*TAU/3), color=BLUE_E, radius=0.1, z_index=2, sheen_factor=0.8)

        spring_1 = Spring(dot_2.get_center(), dot_3.get_center(), color=WHITE, z_index=0)
        spring_2 = Spring(dot_1.get_center(), dot_3.get_center(), color=WHITE, z_index=0)
        spring_3 = Spring(dot_1.get_center(), dot_2.get_center(), color=WHITE, z_index=0)

        trace_1 = TracedPath(dot_1.get_center, stroke_color=BLUE, dissipating_time=1.5, stroke_opacity=[0, 1], stroke_width=4, z_index=0)
        trace_2 = TracedPath(dot_2.get_center, stroke_color=BLUE, dissipating_time=1.5, stroke_opacity=[0, 1], stroke_width=4, z_index=0)
        trace_3 = TracedPath(dot_3.get_center, stroke_color=BLUE, dissipating_time=1.5, stroke_opacity=[0, 1], stroke_width=4, z_index=0)

        self.camera.frame.set_width(Group(dot_1, dot_2, dot_3).width * 3.5)

        system = VGroup(dot_1, dot_2, dot_3, spring_1, spring_2, spring_3)

        system.add_updater(lambda s, dt: s.rotate_about_origin(dt))

        self.play(FadeIn(system, trace_1, trace_2, trace_3))
        self.wait(5)

        self.play(self.camera.frame.animate.shift(RIGHT))
        self.wait(0.5)

        text_1 = Paragraph('Three identical balls,', 'attached by identical springs,', 'are rotating in a circle.').scale(1/3.5).next_to(Circle(1), RIGHT)

        self.play(FadeIn(text_1, shift=RIGHT), run_time=1.5)
        self.wait(5)

        text_2 = Paragraph('The springs are in tension,', 'holding the system', 'in steady state.').scale(1/3.5).next_to(Circle(1), RIGHT)

        self.play(FadeOut(text_1, shift=RIGHT), run_time=1.5)
        self.play(FadeIn(text_2, shift=RIGHT), run_time=1.5)
        self.wait(5)

        text_3 = Paragraph('What if we instantly', 'removed a spring?').scale(1/3.5).next_to(Circle(1), RIGHT)

        self.play(FadeOut(text_2, shift=RIGHT), run_time=1.5)
        self.play(FadeIn(text_3, shift=RIGHT), run_time=1.5)
        self.wait(5)

        self.play(FadeOut(text_3, shift=RIGHT), run_time=1.5)
        self.wait()
        self.play(self.camera.frame.animate.shift(LEFT).set_width(Circle(1).width * 6))

        # wait till the system is in initial conditions
        def temp():
            return np.isclose(dot_1.get_center()[0], 1, rtol=1e-3)
        self.wait(15, stop_condition=temp)

        t = ValueTracker(0)
        system.clear_updaters()
        self.remove(spring_3)
        dot_1.add_updater(lambda d: d.move_to(pos_r1(t.get_value())))
        dot_2.add_updater(lambda d: d.move_to(pos_r3(t.get_value())))
        dot_3.add_updater(lambda d: d.move_to(pos_r2(t.get_value())))
        spring_1.add_updater(lambda sp: sp.become(Spring(dot_2.get_center(), dot_3.get_center(), color=WHITE, z_index=1)))
        spring_2.add_updater(lambda sp: sp.become(Spring(dot_1.get_center(), dot_3.get_center(), color=WHITE, z_index=1)))

        text_speed_up = Text('Speed X2', color=RED).next_to(Circle(1), UP)

        self.play(t.animate.increment_value(4), run_time=4, rate_func=linear)
        # speed up
        self.add(text_speed_up)
        self.play(t.animate.increment_value(4), run_time=2, rate_func=linear)
        self.remove(text_speed_up)
        self.play(t.animate.increment_value(32), run_time=16, rate_func=linear)

        # fade out with video editor

class DemoTransient(MovingCameraScene):
    def construct(self):
        # make the mobjects
        t = ValueTracker(0)
        dot_1 = Dot(pos_r1(0), color=BLUE, radius=0.1, z_index=2)
        dot_1.add_updater(lambda d: d.move_to(pos_r1(t.get_value())))
        dot_2 = Dot(pos_r2(0), color=GREEN, radius=0.1, z_index=2)
        dot_2.add_updater(lambda d: d.move_to(pos_r2(t.get_value())))
        dot_3 = Dot(pos_r3(0), color=ORANGE, radius=0.1, z_index=2)
        dot_3.add_updater(lambda d: d.move_to(pos_r3(t.get_value())))

        spring_1 = Spring(dot_1.get_center(), dot_3.get_center(), color=WHITE, z_index=0)
        spring_1.add_updater(lambda sp: sp.become(Spring(dot_1.get_center(), dot_3.get_center(), color=WHITE, z_index=1)))
        spring_2 = Spring(dot_2.get_center(), dot_3.get_center(), color=WHITE, z_index=0)
        spring_2.add_updater(lambda sp: sp.become(Spring(dot_2.get_center(), dot_3.get_center(), color=WHITE, z_index=1)))

        trace_1 = TracedPath(dot_1.get_center, stroke_color=BLUE, dissipating_time=1, stroke_opacity=[0, 1], stroke_width=4, z_index=0)
        trace_2 = TracedPath(dot_2.get_center, stroke_color=GREEN, dissipating_time=1, stroke_opacity=[0, 1], stroke_width=4, z_index=0)
        trace_3 = TracedPath(dot_3.get_center, stroke_color=ORANGE, dissipating_time=1, stroke_opacity=[0, 1], stroke_width=4, z_index=0)

        self.camera.frame.set_width(Group(dot_1, dot_2, dot_3).width * 6)

        self.add(trace_1, trace_2, trace_3, dot_1, dot_2, dot_3, spring_1, spring_2)

        self.play(t.animate.set_value(40), rate_func=rate_functions.linear, run_time=15)

        self.wait()

class DemoWithDotOne(MovingCameraScene):
    def construct(self):
        # make the mobjects
        t = ValueTracker(0)
        dot_1 = Dot(pos_r1(0), color=BLUE, z_index=2, sheen_factor=0.8, radius=0.1)
        dot_1.add_updater(lambda d: d.move_to(pos_r1(t.get_value())))
        dot_2 = Dot(pos_r2(0), color=BLUE, z_index=2, sheen_factor=0.8, stroke_opacity=0.25, radius=0.1)
        dot_2.add_updater(lambda d: d.move_to(pos_r2(t.get_value())))
        dot_3 = Dot(pos_r3(0), color=RED, z_index=2, sheen_factor=0.8, stroke_opacity=0.25, radius=0.1)
        dot_3.add_updater(lambda d: d.move_to(pos_r3(t.get_value())))

        spring_1 = Spring(dot_1.get_center(), dot_3.get_center(), color=WHITE, z_index=0, stroke_opacity=0.25)
        spring_1.add_updater(lambda sp: sp.become(Spring(dot_1.get_center(), dot_3.get_center(), color=WHITE, z_index=1, stroke_opacity=0.25)))
        spring_2 = Spring(dot_2.get_center(), dot_3.get_center(), color=WHITE, z_index=0, stroke_opacity=0.25)
        spring_2.add_updater(lambda sp: sp.become(Spring(dot_2.get_center(), dot_3.get_center(), color=WHITE, z_index=1, stroke_opacity=0.25)))

        trace_1 = TracedPath(dot_1.get_center, stroke_color=BLUE_C, dissipating_time=1.5, stroke_opacity=[0.25, 1], stroke_width=4, z_index=0)
        trace_2 = TracedPath(dot_2.get_center, stroke_color=BLUE_C, dissipating_time=1.5, stroke_opacity=[0.25, 1], stroke_width=4, z_index=0)

        self.camera.frame.set_width(Group(dot_1, dot_2, dot_3).width * 6).shift(RIGHT*1.5)

        # get path for dot 1
        path_1 = VMobject(color=BLUE_E, stroke_opacity=0.4, z_index=0, stroke_width=2).set_points_smoothly([pos_r1(dt) for dt in np.linspace(0, 400, 1000)])

        self.add(path_1, trace_1, trace_2, dot_1, dot_2, dot_3, spring_1, spring_2)

        self.play(t.animate.set_value(12), rate_func=linear, run_time=3)

        text = Paragraph('The locus for', 'two of these balls.').scale(0.85).next_to(path_1, RIGHT)

        self.play(t.animate(rate_func=linear, run_time=7).set_value(28), FadeIn(text, shift=RIGHT, rate_func=smooth, run_time=1))

        # fade out in editor

class DemoWithDotThree(MovingCameraScene):
    def construct(self):
        # make the mobjects
        t = ValueTracker(0)
        dot_1 = Dot(pos_r1(0), color=BLUE, z_index=2, sheen_factor=0.8, stroke_opacity=0.25, radius=0.1)
        dot_1.add_updater(lambda d: d.move_to(pos_r1(t.get_value())))
        dot_2 = Dot(pos_r2(0), color=BLUE, z_index=2, sheen_factor=0.8, stroke_opacity=0.25, radius=0.1)
        dot_2.add_updater(lambda d: d.move_to(pos_r2(t.get_value())))
        dot_3 = Dot(pos_r3(0), color=RED, z_index=2, sheen_factor=0.8, radius=0.1)
        dot_3.add_updater(lambda d: d.move_to(pos_r3(t.get_value())))

        spring_1 = Spring(dot_1.get_center(), dot_3.get_center(), color=WHITE, z_index=0, stroke_opacity=0.25)
        spring_1.add_updater(lambda sp: sp.become(Spring(dot_1.get_center(), dot_3.get_center(), color=WHITE, z_index=1, stroke_opacity=0.25)))
        spring_2 = Spring(dot_2.get_center(), dot_3.get_center(), color=WHITE, z_index=0, stroke_opacity=0.25)
        spring_2.add_updater(lambda sp: sp.become(Spring(dot_2.get_center(), dot_3.get_center(), color=WHITE, z_index=1, stroke_opacity=0.25)))

        trace_3 = TracedPath(dot_3.get_center, stroke_color=RED_C, dissipating_time=1, stroke_opacity=[0.25, 1], stroke_width=4, z_index=0)

        self.camera.frame.set_width(Group(dot_1, dot_2, dot_3).width * 6).shift(RIGHT*1.5)

        # get path for dot 3
        path_3 = VMobject(color=RED_E, stroke_opacity=0.4, z_index=0, stroke_width=2).set_points_smoothly([pos_r3(dt) for dt in np.linspace(0, 400, 1000)])

        self.add(path_3, trace_3, dot_1, dot_2, dot_3, spring_1, spring_2)

        self.play(t.animate.set_value(12), rate_func=rate_functions.linear, run_time=3)

        text = Paragraph('The locus for', 'the other ball.').scale(0.85).next_to(path_3, RIGHT).shift(0.5*RIGHT)

        self.play(t.animate(rate_func=linear, run_time=7).increment_value(28), FadeIn(text, shift=RIGHT, rate_func=smooth, run_time=1))

class Spring(VMobject):
    def __init__(
        self,
        start: np.ndarray = LEFT,
        end: np.ndarray = RIGHT,
        num_coils: int = 10,
        coil_width: float = 0.25,
        end_length: float = 0.125,
        **kwargs: Any
    ) -> None:
        self.start = start
        self.end = end
        self.num_coils = num_coils
        self.coil_width = coil_width
        self.end_length = end_length
        super().__init__(stroke_width=2, **kwargs)

    def generate_points(self) -> None:
        # start spring end
        spring_dir = (self.end - self.start)/np.linalg.norm(self.end - self.start)
        end_one = self.start + self.end_length*spring_dir

        # end spring end
        end_two = self.end - self.end_length*spring_dir

        # coil points
        coil_d = np.linalg.norm(end_one - end_two)
        num_points = self.num_coils*2
        dx = coil_d/num_points
        perp_dir = spring_dir@np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        points = [self.start, end_one]
        for i in range(num_points):
            points.append(end_one + dx*(i+1)*spring_dir + self.coil_width/2*perp_dir*(-1)**i)
        points.append(end_two)
        points.append(self.end)

        self.set_points_smoothly(points)

# fig = plt.figure()
# axis = plt.axes(xlim=(-3, 3), ylim=(-3, 3))
#
# t = np.linspace(0, 700, 10000)
# r1 = [pos_r1(tee) for tee in t]
# r2 = [pos_r2(tee) for tee in t]
# r3 = [pos_r3(tee) for tee in t]
#
# plt.gca().set_aspect('equal')
# plt.plot([r[0] for r in r1], [r[1] for r in r1], c='tab:blue')
# plt.show()
# plt.gca().set_aspect('equal')
# plt.plot([r[0] for r in r2], [r[1] for r in r2], c='tab:orange')
# plt.show()
# plt.gca().set_aspect('equal')
# plt.plot([r[0] for r in r3], [r[1] for r in r3], c='tab:green')
# plt.show()
