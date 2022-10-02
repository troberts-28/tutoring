import ppb
from ppb.features.animation import Animation
from events import AnimationLooped

class Explosion(ppb.Sprite):
    image = Animation("assets/effects/explosion{1..3}.png", 3)
    layer = 10
    size = 1
    timer = 0
    run_once = True

    def __init__(self, **props):
        super().__init__(**props)
        self.duration = 0.5

    def on_update(self, event, signal):
        if self.timer >= self.duration:
            signal(AnimationLooped())
        self.timer += event.time_delta

    def on_animation_looped(self, event, signal):
        if self.run_once:
            event.scene.remove(self)