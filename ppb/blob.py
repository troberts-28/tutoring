import math
import ppb
import random
from ppb import keycodes
from ppb.features.animation import Animation
import ppb.events as events


def lerp(a, b, t):
    return a * (1 - t) + b * t


def lerp_vector(a, b, t):
    c = ppb.Vector(lerp(a.x, b.x, t), lerp(a.y, b.y, t))
    return c


class Blob(ppb.Sprite):
    image = Animation("resources/blobs/blob_{0..6}.png", 10)
    target = ppb.Vector(0, 0)
    speed = 0
    forward_w = keycodes.W
    forward = keycodes.Up
    cam_origin = None
    cam_target = None
    cam_progress = 0

    def on_mouse_motion(self, event: events.MouseMotion, signal):
        self.target = event.position

    def on_update(self, event: events.Update, signal):
        intent_vector = self.target - self.position
        if intent_vector:
            self.position += intent_vector.scale(self.speed * event.time_delta)
            self.rotation = (
                math.degrees(math.atan2(intent_vector.y, intent_vector.x)) - 90
            )

        cam = event.scene.main_camera
        cam.position = self.position

    def on_key_pressed(self, key_event: events.KeyPressed, signal):
        if key_event.key == self.forward or key_event.key == self.forward_w:
            self.speed += 5

    def on_key_released(self, key_event: events.KeyReleased, signal):
        if key_event.key == self.forward or key_event.key == self.forward_w:
            self.speed -= 5


class Target(ppb.Sprite):
    layer = 1
    direction = ppb.Vector(0, 0)
    speed = 5
    shoot_frequency = 1
    fire_bullets = True
    random_move_frequency = 1
    random_movement = True
    dodge_projectile = True
    image = ppb.Image("SpaceBounce/assets/sprites/target.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shoot_time_counter = kwargs.get(
            "shoot_time_counter", random.uniform(-5, 1)
        )
        self.random_move_time_counter = kwargs.get(
            "random_move_time_counter", random.uniform(-5, 1)
        )

    def on_update(self, update_event, signal):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        self.position += direction * self.speed * update_event.time_delta

        next_direction = self.direction

        if (
            self.random_move_time_counter > 1
            and self.random_movement
            and self.direction != next_direction
        ):
            next_direction = random.choice(
                [ppb.Vector(1, 0), ppb.Vector(-1, 0)]
            )
            self.random_move_time_counter -= 1

        self.direction = next_direction

        self.random_move_time_counter += update_event.time_delta


def setup(scene):
    scene.add(Blob(position=ppb.Vector(0, -4)))
    scene.add(Target())


ppb.run(setup)
