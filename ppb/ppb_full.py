import ppb
from ppb import keycodes
from ppb.events import KeyPressed, KeyReleased
from ppb.features import animation, loadingscene
from itertools import product
import ppb.events as events


class Player(ppb.Sprite):
    direction = ppb.Vector(0, 0)
    speed = 4
    position = ppb.Vector(0, -3)
    left = keycodes.Left
    right = keycodes.Right
    shoot = keycodes.Space
    projectile_direction = ppb.Vector(0, 0)

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
    
    def on_mouse_motion(self, event: events.MouseMotion, signal):
        self.projectile_direction = event.position
    
    def _fire_bullet(self, scene):
        scene.add(
                Projectile(position=self.position + ppb.Vector(0, 0.5), direction=self.projectile_direction)
            )


class Projectile(ppb.Sprite):
    size = 0.25
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


class LoadingSprite(ppb.Sprite):
    ready_image = ppb.Image("resources/load_bar/center_filled.png")
    waiting_image = ppb.Image("resources/load_bar/center_empty.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = self.waiting_image


class Label(ppb.Sprite):
    image = ppb.Text("Level 1", font=ppb.Font("resources/ubuntu_font/UbuntuMono-B.ttf", size=12))


class Game(ppb.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Player())
        self.add(Label())

        for x in range(-4, 5, 2):
            self.add(Target(position=ppb.Vector(x, 3)))


class Level1Screen(ppb.Scene):
    next_scene = Game
    
    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Label())
    
    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == keycodes.Space:
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(self))


class LoadScreen(loadingscene.BaseLoadingScene):
    next_scene = Level1Screen

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

