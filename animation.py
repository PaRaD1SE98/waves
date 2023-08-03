# manim .\animation.py -pql
from manim import *


class Ani(Scene):
    def construct(self):
        square = Square(color=WHITE,
                        fill_opacity=0,
                        side_length=5).shift(LEFT*3)
        text_square = Text("Any Plate", color=WHITE,
                           font_size=25).next_to(square, UP)
        square_group = VGroup(square, text_square)
        # add a circle and a dot in the square
        circle = Circle(color=BLUE,
                        fill_opacity=0,
                        radius=.2).shift(LEFT*1.5)

        dot = Dot(color=GREEN,
                  fill_opacity=1,
                  radius=0.1).shift(RIGHT*1.5)
        # add animation

        # # add text
        sensor_laser_group = VGroup(circle, dot)
        text_sensor = Text("Sensor", color=BLUE,
                           font_size=25).next_to(circle, UP)
        text_laser = Text("Laser", color=GREEN, font_size=25).next_to(dot, UP)
        item_group = VGroup(sensor_laser_group,
                            text_sensor, text_laser).shift(LEFT*3)
        # plot a wave
        # add a xy axis
        axes = Axes(
            x_range=[0, 1, .1],
            y_range=[-1, 1, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": WHITE},
            tips=False
        ).shift(RIGHT*3)
        # add a wave
        wave = axes.plot(lambda x: np.sin(100*x)*np.exp(-5*x),
                         color=WHITE,
                         x_range=[0, 1, .1])

        self.add(square_group,
                 item_group,
                 axes,
                 wave)
        # connect the circle and the dot
        line = Line(dot.get_center(), circle.get_center()+RIGHT*.2)

        # add animation
        self.play(Create(line), Create(wave))
        self.play(FadeOut(line), FadeOut(wave))
        self.play(Rotate(item_group,
                         PI,
                         about_point=sensor_laser_group.get_center()))
        self.play(Rotate(text_sensor, PI),
                  Rotate(text_laser, PI))

        line = Line(dot.get_center(),
                    circle.get_center()+LEFT*.2)
        self.play(Create(line), Create(wave))


class Gra(Scene):
    def construct(self):
        square = Square(color=WHITE,
                        fill_opacity=0,
                        side_length=5).shift(LEFT*3)
        square_group = VGroup(square)
        # add a circle and a dot in the square
        circle = Circle(color=BLUE,
                        fill_opacity=0,
                        radius=.2).shift(LEFT*1.5)
        circle_group = VGroup(circle,
                              circle.copy().shift(UP),
                              circle.copy().shift(DOWN))

        dot = Dot(color=GREEN,
                  fill_opacity=1,
                  radius=0.1).shift(RIGHT*1.5)
        # add animation

        # # add text
        sensor_laser_group = VGroup(circle_group,
                                    circle_group.copy().shift(RIGHT),
                                    dot)
        item_group = VGroup(sensor_laser_group).shift(LEFT*3)
        text_sensor = Text("Sensor", color=BLUE,
                           font_size=25).next_to(circle_group, UP)
        text_laser = Text("Laser", color=GREEN,
                          font_size=25).next_to(dot, UP)
        self.add(square_group, item_group, text_sensor, text_laser)

        square2 = square_group.copy().shift(RIGHT*6)
        # add a circle and a dot in the square
        dot = Dot(color=GREEN,
                  fill_opacity=1,
                  radius=.1).shift(LEFT*1.5)
        dot_group = VGroup(dot,
                           dot.copy().shift(UP),
                           dot.copy().shift(DOWN))

        circle = Circle(color=BLUE,
                        fill_opacity=0,
                        radius=0.2).shift(RIGHT*1.5)
        # add animation

        # # add text
        sensor_laser_group2 = VGroup(dot_group,
                                     dot_group.copy().shift(RIGHT),
                                     circle)
        item_group2 = VGroup(sensor_laser_group2).shift(RIGHT*3)
        text_sensor2 = Text("Sensor", color=BLUE,
                            font_size=25).next_to(circle, UP)
        text_laser2 = Text("Laser", color=GREEN,
                           font_size=25).next_to(dot_group, UP)
        self.add(square2, item_group2, text_sensor2, text_laser2)
