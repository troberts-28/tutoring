import ppb
import random
from ppb import keycodes
from mzutil import smooth_step, collide

DIRECTIONS = {
    keycodes.Left: ppb.Vector(-1, 0),
    keycodes.Right: ppb.Vector(1, 0),
    keycodes.Up: ppb.Vector(0, 1),
    keycodes.Down: ppb.Vector(0, -1),
}


class Penguin(ppb.Sprite):
    direction = ppb.Vector(0, 0)

    def on_update(self, update_event, signal):
        self.position += update_event.time_delta * self.direction

    def on_key_pressed(self, key_event, signal):
        self.direction = DIRECTIONS.get(key_event.key, ppb.Vector(0, 0))

    def on_key_released(self, key_event, signal):
        if key_event.key in DIRECTIONS:
            self.direction = ppb.Vector(0, 0)


class OrangeBall(ppb.Sprite):
    is_moving = False
    x_offset = 0.25
    y_offset = 0.25

    def kick(self, direction):
        self.target_position = self.position + direction
        self.original_position = self.position
        self.time_passed = 0
        self.is_moving = True

    def maybe_move(self, update_event, signal):
        if not self.is_moving:
            return False
        self.time_passed += update_event.time_delta
        if self.time_passed >= 1:
            self.position = self.target_position
            self.is_moving = False
            return False
        t = smooth_step(self.time_passed)
        self.position = (1 - t) * self.original_position + t * self.target_position
        return True

    def on_update(self, update_event, signal):
        if self.maybe_move(update_event, signal):
            return
        (penguin,) = update_event.scene.get(kind=Penguin)
        if not collide(penguin, self):
            return
        try:
            direction = (self.position - penguin.position).normalize()
        except ZeroDivisionError:
            direction = ppb.Vector(
                random.uniform(-1, 1), random.uniform(-1, 1)
            ).normalize()
        self.kick(direction)


class Target(ppb.Sprite):
    def on_update(self, update_event, signal):
        for ball in update_event.scene.get(kind=OrangeBall):
            if not collide(ball, self):
                continue
            update_event.scene.remove(ball)
            update_event.scene.add(OrangeBall(pos=(-4, random.uniform(-3, 3))))
            update_event.scene.add(
                Fish(pos=(random.uniform(-4, -3), random.uniform(-3, 3)))
            )


class Fish(ppb.Sprite):
    x_offset = 0.05
    y_offset = 0.2

    def on_update(self, update_event, signal):
        (penguin,) = update_event.scene.get(kind=Penguin)
        if collide(penguin, self):
            update_event.scene.remove(self)


def setup(scene):
    scene.add(Penguin(pos=(0, 0)))
    scene.add(OrangeBall(pos=(-4, 0)))
    scene.add(Target(pos=(4, 0)))

ppb.run(setup)
