import math
import ppb
from ppb import keycodes
from ppb.features.animation import Animation
import ppb.events as events


class Blob(ppb.Sprite):
    image = Animation("resources/blobs/blob_{0..6}.png", 10)
    target = ppb.Vector(0, 0)
    speed = 0
    forward_w = keycodes.W
    forward = keycodes.Up

    def on_mouse_motion(self, event: events.MouseMotion, signal):
        self.target = event.position

    def on_update(self, event: events.Update, signal):
        intent_vector = self.target - self.position
        if intent_vector:
            self.position += intent_vector.scale(self.speed * event.time_delta)
            self.rotation = math.degrees(math.atan2(intent_vector.y, intent_vector.x)) - 90
    
    def on_key_pressed(self, key_event: events.KeyPressed, signal):
        if key_event.key == self.forward or key_event.key == self.forward_w:
            self.speed += 5

    def on_key_released(self, key_event: events.KeyReleased, signal):
        if key_event.key == self.forward or key_event.key == self.forward_w:
            self.speed -= 5


def setup(scene):
    scene.add(Blob())


ppb.run(setup)
