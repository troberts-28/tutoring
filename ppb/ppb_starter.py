import ppb
from ppb import keycodes
from ppb.events import KeyPressed, KeyReleased


class Player(ppb.Sprite):
    direction = ppb.Vector(0, 0)
    speed = 4
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
            self.direction += ppb.Vector(-1, 0)
        elif key_event.key == self.right:
            self.direction += ppb.Vector(1, 0)
        elif key_event.key == self.shoot:
            self._fire_bullet(key_event.scene)

    def on_key_released(self, key_event: KeyReleased, signal):
        if key_event.key == self.left:
            self.direction += ppb.Vector(1, 0)
        elif key_event.key == self.right:
            self.direction += ppb.Vector(-1, 0)

    def on_button_pressed(self, event, signal):
        if event.button is ppb.buttons.Primary:
            self._fire_bullet(event.scene)
    
    def _fire_bullet(self, scene):
        scene.add(
            Projectile(position=self.position, direction=ppb.Vector(0, 1))
        )


class Projectile(ppb.Sprite):
    size = 1
    direction = ppb.Vector(0, 0)
    speed = 6

    def on_update(self, update_event, signal):
        if self.direction:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        self.position += direction * self.speed * update_event.time_delta


class Target(ppb.Sprite):
    def on_update(self, update_event, signal):
        for p in update_event.scene.get(kind=Projectile):
            if (p.position - self.position).length <= self.size:
                update_event.scene.remove(self)
                update_event.scene.remove(p)
                break


def setup(scene):
    scene.add(Player())

    for x in [0, 1, 2,  8, 10, 3, 4, -5, 100, 5, -6, -9, -10, -0, -3, 7, -7, -8, -1, -2,  9, 10, ]:
        scene.add(Target(position=ppb.Vector(x, x)))


ppb.run(setup)