from dataclasses import dataclass

from ppb import Scene


@dataclass
class AnimationLooped:
    scene: Scene = None
