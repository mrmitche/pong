import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
     ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window


class PongBall(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speedup  = 1.1
            offset = 0.02 * Vector(0, ball.center_y-self.center_y)
            ball.velocity =  speedup * (offset - ball.velocity)

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None
	
    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel #Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4,0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(4,0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    #TODO: add additional condition to prevent paddles from moving off screen
    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.player2.center_y += 20
        elif keycode[1] == 'down':
            self.player2.center_y -= 20
        elif keycode[1] == 'w':
            self.player1.center_y += 20
        elif keycode[1] == 's':
            self.player1.center_y -= 20

        return True
		

class PongApp(App):

    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
