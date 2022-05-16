import ppb
from ppb import keycodes
from ppb.events import KeyPressed, KeyReleased
from ppb.features import loadingscene
import ppb.events as events
import math
import random


class Player(ppb.Sprite):
    direction = ppb.Vector(0, 0)
    speed = 4
    position = ppb.Vector(0, -3)
    left = keycodes.Left
    right = keycodes.Right
    shoot = keycodes.Space
    mouse_direction = ppb.Vector(0, 0)
    shoot_vector = ppb.Vector(0, 0)
    layer = 1

    def on_update(self, update_event, signal):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        self.position += direction * self.speed * update_event.time_delta

        intent_vector = self.mouse_direction - self.position
        if intent_vector:
            self.shoot_vector = intent_vector
            self.rotation = (
                math.degrees(math.atan2(intent_vector.y, intent_vector.x)) - 90
            )

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

    def on_mouse_motion(self, event: events.MouseMotion, signal):
        self.mouse_direction = event.position

    def _fire_bullet(self, scene):
        scene.add(
            Projectile(position=self.position, direction=self.shoot_vector)
        )


class Projectile(ppb.Sprite):
    size = 0.25
    direction = ppb.Vector(0, 0)
    speed = 6
    layer = 1

    def on_update(self, update_event, signal):
        if self.direction:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        self.position += direction * self.speed * update_event.time_delta


class Target(ppb.Sprite):
    layer = 1
    direction = ppb.Vector(0, 0)
    speed = 2
    time_counter = 0
    random_movement = True

    def on_update(self, update_event, signal):
        
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        self.position += direction * self.speed * update_event.time_delta
        
        for p in update_event.scene.get(kind=Projectile):
            if (p.position - self.position).length <= self.size:
                update_event.scene.remove(self)
                update_event.scene.remove(p)
                break
        
        if self.position.x > 11 or self.position.x < -11:
            self.direction *= -1
        elif self.time_counter > 1 and self.random_movement:
            self.direction = random.choice([ppb.Vector(1, 0), ppb.Vector(-1, 0)])
            self.time_counter -= 1

        self.time_counter += update_event.time_delta


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

    def __init__(self, text=None, **kwargs):
        super().__init__(**kwargs)
        self.image = ppb.Text(
            text,
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
            Label("You won! You beat the aliens!", size=1, color=(0, 0, 0))
        )


class Level3Game(ppb.Scene):
    next_scene = FinishTitle

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Player())
        self.add(GameBackground())

        for x in range(-8, 9, 2):
            for y in range(3, 9, 2):
                self.add(Target(position=ppb.Vector(x, y), direction=random.choice([ppb.Vector(1, 0), ppb.Vector(-1, 0)]), speed=random.choice(list(range(5)))))

    def on_update(self, update_event, signal):
        if not any(True for _ in self.get(kind=Target)):
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(scene=self))


class Level3Title(ppb.Scene):
    next_scene = Level3Game

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Label("Level 3"))
        self.add(GameBackground())

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == keycodes.Space:
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(self))


class Level2Game(ppb.Scene):
    next_scene = Level3Title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Player())
        self.add(GameBackground())

        for x in range(-4, 5, 2):
            for y in range(3, 9, 2):
                self.add(Target(position=ppb.Vector(x, y), direction=random.choice([ppb.Vector(1, 0), ppb.Vector(-1, 0)])))

    def on_update(self, update_event, signal):
        if not any(True for _ in self.get(kind=Target)):
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(scene=self))


class Level2Title(ppb.Scene):
    next_scene = Level2Game

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Label("Level 2"))
        self.add(GameBackground())

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == keycodes.Space:
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(self))


class Level1Game(ppb.Scene):
    next_scene = Level2Title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Player())
        self.add(GameBackground())

        for x in range(-4, 5, 2):
            self.add(Target(position=ppb.Vector(x, 3), direction=random.choice([ppb.Vector(1, 0), ppb.Vector(-1, 0)]), random_movement=False))

    def on_update(self, update_event, signal):
        if not any(True for _ in self.get(kind=Target)):
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(scene=self))


class Level1Title(ppb.Scene):
    next_scene = Level1Game

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Label("Level 1"))
        self.add(GameBackground())

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == keycodes.Space:
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(scene=self))


class LoadScreen(loadingscene.BaseLoadingScene):
    next_scene = Level1Title

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


ppb.run(starting_scene=LoadScreen, title="Alien Shooter")

