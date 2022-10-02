import ppb
from ppb import keycodes
from ppb.features.animation import Animation
from ppb.events import KeyPressed, KeyReleased
from ppb.features import loadingscene
from ppb.features.twophase import TwoPhaseMixin, TwoPhaseSystem
import ppb.events as events
import math
import random

class Player(ppb.Sprite):
    layer = 1
    image = Animation("resources/blobs/blob_{0..6}.png", 10)
    target = ppb.Vector(0, 0)
    speed = 2

    def on_mouse_motion(self, event: events.MouseMotion, signal):
        self.target = event.position

    def on_update(self, event: events.Update, signal):
        intent_vector = self.target - self.position
        if intent_vector:
            self.position += intent_vector.scale(self.speed * event.time_delta)
            self.rotation = math.degrees(math.atan2(intent_vector.y, intent_vector.x)) - 90


class Blob(ppb.Sprite, TwoPhaseMixin):
    layer = 1
    gravitational_constant = 1
    size = 1
    velocity = ppb.Vector(0, 0)
    image = ppb.Image("resources/friendlyBullet.png")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = ppb.Vector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.gravitational_constant = random.uniform(0.5, 2)
        self.size = random.uniform(0.5, 3)

    def get_bodies(self, scene):
        for blob in scene.get(kind=Blob):
            yield blob, (blob.position - self.position) * 3, blob.size

    def on_update(self, update_event, signal):
        force = sum(
            (
                mass * delta / (len(delta) ** 2)
                for _, delta, mass in self.get_bodies(update_event.scene)
            ),
            ppb.Vector(0, 0)
        )

        self.velocity += force * self.gravitational_constant * update_event.time_delta

        if self.position.x > 12 or self.position.x < -12:
            self.velocity = ppb.Vector(self.velocity.x * -1, self.velocity.y)
        if self.position.y > 8.8 or self.position.y < -8.8:
            self.velocity = ppb.Vector(self.velocity.x, self.velocity.y * -1)

        self.stage_changes(
            position=self.position + self.velocity * update_event.time_delta
        )
        

class LoadingSprite(ppb.Sprite):
    ready_image = ppb.Image("resources/load_bar/center_filled.png")
    waiting_image = ppb.Image("resources/load_bar/center_empty.png")
    layer = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = self.waiting_image


class GameBackground(ppb.Sprite):
    background_image = ppb.Image("resources/backgrounds/background1.png")
    size = 20
    layer = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = self.background_image


class Label(ppb.Sprite):
    size = 2
    layer = 1
    color = (255, 255, 255)
    text = None
    image = None

    def on_update(self, update_event, signal):
        self.image = ppb.Text(
            self.text,
            font=ppb.Font("resources/ubuntu_font/UbuntuMono-B.ttf", size=40),
            color=self.color,
        )

class FinishTitle(ppb.Scene):
    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(
            GameBackground(
                background_image=ppb.Image(
                    "resources/backgrounds/finishBackground.jpg"
                )
            )
        )
        self.add(
            Label(text="You won! You beat the aliens!", size=1, color=(0, 0, 0))
        )


class GameOver(ppb.Scene):
    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(GameBackground())
        self.add(
            Label(text="Game Over :(")
        )
    
    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == keycodes.Space:
            signal(ppb.events.ReplaceScene(new_scene=Level1Title))
            signal(ppb.events.StopScene(self))


class Level1Game(ppb.Scene):
    player = Player()
    add_blob_timer = 0
    add_blob_frequency = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(self.player)
        self.add(Label(text="5 Lives", position=ppb.Vector(-9, 8), size=1))
        self.add(GameBackground())

        for x in range(-4, 5, 1):
            self.add(
                Blob(
                    position=ppb.Vector(x, random.uniform(3, 9)),
                )
            )
    
    def on_update(self, update_event, signal):
        if self.shoot_time_counter > 1 and self.fire_bullets:
            self._fire_bullet(update_event.scene)
            self.shoot_time_counter -= 1

        self.random_move_time_counter += update_event.time_delta
        self.shoot_time_counter += update_event.time_delta


class Level1Title(ppb.Scene):
    next_scene = Level1Game

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Label(text="Level 1"))
        self.add(GameBackground())

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == keycodes.Space:
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(scene=self))


class LoadScreen(loadingscene.BaseLoadingScene):
    next_scene = Level1Title

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(GameBackground())

    def get_progress_sprites(self):
        left = LoadingSprite(
            position=ppb.Vector(-4, 0),
            ready_image=ppb.Image("resources/load_bar/left_filled.png"),
            waiting_image=ppb.Image("resources/load_bar/left_empty.png"),
        )
        center = [
            LoadingSprite(position=ppb.Vector(x, 0)) for x in range(-3, 4)
        ]
        right = LoadingSprite(
            position=ppb.Vector(4, 0),
            ready_image=ppb.Image("resources/load_bar/right_filled.png"),
            waiting_image=ppb.Image("resources/load_bar/right_empty.png"),
        )
        return [left, *center, right]

    def update_progress(self, progress):
        bar = sorted(self.get(tag="progress"), key=lambda s: s.position.x)

        progress_index = progress * len(bar)

        for i, sprite in enumerate(bar):
            if i <= progress_index:
                sprite.image = sprite.ready_image
            else:
                sprite.image = sprite.waiting_image


ppb.run(starting_scene=LoadScreen, title="Gravity Dodgems", systems=[TwoPhaseSystem])

