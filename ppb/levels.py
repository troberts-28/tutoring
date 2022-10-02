import ppb
from ppb import keycodes
from ppb.events import KeyPressed
from ppb.features import loadingscene

class LoadingSprite(ppb.Sprite):
    ready_image = ppb.Image("resources/load_bar/center_filled.png")
    waiting_image = ppb.Image("resources/load_bar/center_empty.png")
    layer = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = self.waiting_image


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


ppb.run(starting_scene=LoadScreen, title="Alien Shooter")
