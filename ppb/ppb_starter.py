import ppb
from ppb import keycodes
from ppb.events import KeyPressed, KeyReleased


class Player(ppb.Sprite):
    direction = ppb.Vector(0, 0)
    speed = 0
    position = ppb.Vector(0, -3)
    left = keycodes.Left
    right = keycodes.Right
    shoot = keycodes.Space

    def on_update(self, update_event, signal):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        self.position += direction * self.speed * update_event.time_delta

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == self.left:
            self.direction
        elif key_event.key == self.right:
            self.direction
        elif key_event.key == self.shoot:
            key_event.scene.add(Projectile(position=self.position))

    def on_key_released(self, key_event: KeyReleased, signal):
        if key_event.key == self.left:
            self.direction
        elif key_event.key == self.right:
            self.direction


class Projectile(ppb.Sprite):
    size = None
    direction = ppb.Vector(0, 1)
    speed = None

    def on_update(self, update_event, signal):
        return


class Target(ppb.Sprite):

    def on_update(self, update_event, signal):
        return


def setup(scene):
    scene.add(Player())

    for x in [0]:
        scene.add(Target(position=ppb.Vector(x, 3)))


ppb.run(setup)