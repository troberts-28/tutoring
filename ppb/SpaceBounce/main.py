import ppb
import ppb.events as events
import math
import random
from ppb.features import loadingscene

from effects import Explosion


class Player(ppb.Sprite):
    sprite_id = "player"
    direction = ppb.Vector(0, 0)
    speed = 4
    position = ppb.Vector(0, -8)
    left_a = ppb.keycodes.A
    left = ppb.keycodes.Left
    right_d = ppb.keycodes.D
    right = ppb.keycodes.Right
    shoot = ppb.keycodes.Up
    shoot_sensitivity = 1
    shoot_direction = ppb.Vector(0, 0)
    shoot_position = ppb.Vector(0, 1)
    layer = 1
    size = 1.4
    health = 100
    image = ppb.Image("assets/sprites/player.png")

    def on_update(self, update_event: events.Update, signal):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        if (self.position.x > 12 and self.direction.x > 0) or (
            self.position.x < -12 and self.direction.x < 0
        ):
            pass
        else:
            self.position += direction * self.speed * update_event.time_delta

        if (
            abs(self.rotation) < 60
            or (self.shoot_direction.x / self.shoot_position.x) < 0
        ):
            self.shoot_position += (
                self.shoot_direction * self.speed * update_event.time_delta
            )
            self.rotation = (
                math.degrees(
                    math.atan2(self.shoot_position.y, self.shoot_position.x)
                )
                - 90
            )

        for p in update_event.scene.get(kind=Projectile):
            if (
                p.is_enemy is True
                and (p.position - self.position).length <= self.size
            ) or (
                p.is_enemy is False
                and (p.position - self.position).length <= self.size / 2
                and p.existed_for > 20
            ):
                self.health -= p.damage
                update_event.scene.remove(p)
                update_event.scene.add(Explosion(position=self.position))
                if self.health <= 0:
                    update_event.scene.remove(self)

    def on_key_pressed(self, key_event: events.KeyPressed, signal):
        if key_event.key == self.left_a:
            self.direction += ppb.Vector(-1, 0)
        elif key_event.key == self.right_d:
            self.direction += ppb.Vector(1, 0)
        elif key_event.key == self.left:
            self.shoot_direction += ppb.Vector(-1, 0)
        elif key_event.key == self.right:
            self.shoot_direction += ppb.Vector(1, 0)
        elif key_event.key == self.shoot:
            self._fire_bullet(key_event.scene)

    def on_key_released(self, key_event: events.KeyReleased, signal):
        if key_event.key == self.left_a and self.direction == ppb.Vector(
            -1, 0
        ):
            self.direction += ppb.Vector(1, 0)
        elif key_event.key == self.right_d and self.direction == ppb.Vector(
            1, 0
        ):
            self.direction += ppb.Vector(-1, 0)
        elif key_event.key == self.left:
            self.shoot_direction -= ppb.Vector(-1, 0)
        elif key_event.key == self.right:
            self.shoot_direction -= ppb.Vector(1, 0)

    def on_button_pressed(self, event, signal):
        if event.button is ppb.buttons.Primary:
            self._fire_bullet(event.scene)

    def on_mouse_motion(self, event: events.MouseMotion, signal):
        self.mouse_position = event.position

    def _fire_bullet(self, scene):
        scene.add(
            Projectile(position=self.position, direction=self.shoot_position)
        )


class Projectile(ppb.Sprite):
    size = 0.5
    direction = ppb.Vector(0, 0)
    speed = 6
    layer = 2
    is_enemy = False
    existed_for = 0
    damage = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rotation = (
            math.degrees(math.atan2(self.direction.y, self.direction.x)) - 90
        )
        if kwargs.get("is_enemy", False) is True:
            self.image = ppb.Image("assets/sprites/enemyBullet.png")
            self.size = 2
        else:
            self.image = ppb.Image("assets/sprites/friendlyBullet.png")

    def on_update(self, update_event, signal):
        if self.direction:
            direction = self.direction.normalize()
        else:
            direction = self.direction

        self.position += direction * self.speed * update_event.time_delta

        if self.is_enemy is False:
            if abs(self.position.x) > 12.2:
                self.direction = ppb.Vector(
                    -self.direction.x, self.direction.y
                )
            if abs(self.position.y) > 9:
                self.direction = ppb.Vector(
                    self.direction.x, -self.direction.y
                )
        elif abs(self.position.x > 15) or abs(self.position.y > 15):
            update_event.scene.remove(self)

        self.existed_for += 1


class Target(ppb.Sprite):
    layer = 1
    direction = ppb.Vector(0, 0)
    speed = 5
    shoot_frequency = 1
    fire_bullets = True
    random_move_frequency = 1
    random_movement = True
    dodge_projectile = True
    image = ppb.Image("assets/sprites/target.png")

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

        if (self.position.x > 11.5 and self.direction.x > 0) or (
            self.position.x < -11.5 and self.direction.x < 0
        ):
            next_direction = ppb.Vector(
                self.direction.x * -1, self.direction.y
            )
        else:
            for p in update_event.scene.get(kind=Projectile):
                if (
                    p.is_enemy is False
                    and self.dodge_projectile
                    and (p.position - self.position).length <= self.size
                    and p.position.x - self.position.x != 0
                ):
                    next_direction = ppb.Vector(
                        (p.position.x - self.position.x)
                        / (p.position.x - self.position.x),
                        0,
                    )
                    break

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

        for p in update_event.scene.get(kind=Projectile):
            if p.is_enemy is False:
                if (p.position - self.position).length <= self.size:
                    update_event.scene.add(Explosion(position=self.position))
                    update_event.scene.remove(p)
                    update_event.scene.remove(self)

        if self.shoot_time_counter > 1 and self.fire_bullets:
            self._fire_bullet(update_event.scene)
            self.shoot_time_counter -= 1

        self.random_move_time_counter += update_event.time_delta
        self.shoot_time_counter += update_event.time_delta

    def _fire_bullet(self, scene):
        scene.add(
            Projectile(
                position=self.position,
                direction=ppb.Vector(random.uniform(-1, 1), -1),
                is_enemy=True,
            )
        )


class HealthBar(ppb.Sprite):
    image = ppb.Image("assets/health/Health bar15.png")
    layer = 2
    size = 0.8
    health = 150
    linked_sprite_id = "player"

    def __init__(self, **props):
        super().__init__(**props)

    def on_update(self, update_event, signal):
        try:
            sprite = next(filter(
                lambda x: x.sprite_id == self.linked_sprite_id,
                update_event.scene.get(kind=Player),
            ))
            if sprite:
                print(sprite)
                self.position = sprite.position + ppb.Vector(0, 1.5)
                self.image = ppb.Image(
                    f"assets/health/Health bar{int(sprite.health / 10)}.png"
                )
        except:
            pass


class LoadingSprite(ppb.Sprite):
    ready_image = ppb.Image("assets/load/center_filled.png")
    waiting_image = ppb.Image("assets/load/center_empty.png")
    layer = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = self.waiting_image


class GameBackground(ppb.Sprite):
    background_image = ppb.Image("assets/backgrounds/background1.png")
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
    move_with_player = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = ppb.Text(
            self.text,
            font=ppb.Font(
                "assets/fonts/ubuntu_font/UbuntuMono-B.ttf", size=40
            ),
            color=self.color,
        )

    def on_update(self, update_event, signal):
        if self.move_with_player:
            try:
                player = next(update_event.scene.get(kind=Player))
                if player:
                    self.position = player.position + ppb.Vector(0, 2)
            except:
                pass


class FinishTitle(ppb.Scene):
    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(
            GameBackground(
                background_image=ppb.Image(
                    "assets/backgrounds/finishBackground.jpg"
                )
            )
        )
        self.add(
            Label(
                text="You won! You beat the aliens!", size=1, color=(0, 0, 0)
            )
        )


class GameOver(ppb.Scene):
    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(GameBackground())
        self.add(Label(text="Game Over :("))

    def on_key_pressed(self, key_event: events.KeyPressed, signal):
        if key_event.key == ppb.keycodes.Space:
            signal(ppb.events.ReplaceScene(new_scene=Level1Title))
            signal(ppb.events.StopScene(self))


class Level3Game(ppb.Scene):
    next_scene = FinishTitle
    player = Player()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        # self.add(
        #     Label(
        #         text=(str(self.player.noOflives) + " Lives"),
        #         position=ppb.Vector(-9, 8),
        #         size=1,
        #     )
        # )
        self.add(self.player)
        self.add(GameBackground())

        for x in range(-8, 9, 2):
            for y in range(3, 9, 2):
                self.add(
                    Target(
                        position=ppb.Vector(x, y),
                        direction=random.choice(
                            [ppb.Vector(1, 0), ppb.Vector(-1, 0)]
                        ),
                        speed=random.choice(list(range(1, 5))),
                        shoot_frequency=5,
                        random_move_frequency=0.1,
                    )
                )

    def on_update(self, update_event, signal):
        # for label in update_event.scene.get(kind=Label):
        #     label.text = str(self.player.noOflives) + " Lives"
        if not any(True for _ in self.get(kind=Target)):
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(scene=self))
        if not any(True for _ in self.get(kind=Player)):
            signal(ppb.events.ReplaceScene(new_scene=GameOver))
            signal(ppb.events.StopScene(scene=self))


class Level3Title(ppb.Scene):
    next_scene = Level3Game
    player = Player()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        # self.add(
        #     Label(
        #         text=(str(self.player.noOflives) + " Lives"),
        #         position=ppb.Vector(-9, 8),
        #         size=1,
        #     )
        # )
        self.add(Label(text="Level 3"))
        self.add(GameBackground())

    def on_key_pressed(self, key_event: events.KeyPressed, signal):
        if key_event.key == ppb.keycodes.Space:
            signal(
                ppb.events.ReplaceScene(self.next_scene(player=self.player))
            )
            signal(ppb.events.StopScene(self))


class Level2Game(ppb.Scene):
    next_scene = Level3Title
    player = Player()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        # self.add(
        #     Label(
        #         text=(str(self.player.noOflives) + " Lives"),
        #         position=ppb.Vector(-9, 8),
        #         size=1,
        #     )
        # )
        self.add(self.player)
        self.add(GameBackground())

        for x in range(-4, 5, 2):
            for y in range(3, 9, 4):
                self.add(
                    Target(
                        position=ppb.Vector(x, y),
                        direction=random.choice(
                            [ppb.Vector(1, 0), ppb.Vector(-1, 0)]
                        ),
                        shoot_frequency=8,
                    )
                )

    def on_update(self, update_event, signal):
        # for label in update_event.scene.get(kind=Label):
        #     label.text = str(self.player.noOflives) + " Lives"
        if not any(True for _ in self.get(kind=Target)):
            signal(
                ppb.events.ReplaceScene(self.next_scene(player=self.player))
            )
            signal(ppb.events.StopScene(scene=self))
        if not any(True for _ in self.get(kind=Player)):
            signal(ppb.events.ReplaceScene(new_scene=GameOver))
            signal(ppb.events.StopScene(scene=self))


class Level2Title(ppb.Scene):
    next_scene = Level2Game
    player = Player()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        # self.add(
        #     Label(
        #         text=(str(self.player.noOflives) + " Lives"),
        #         position=ppb.Vector(-9, 8),
        #         size=1,
        #     )
        # )
        self.add(Label(text="Level 2"))
        self.add(GameBackground())

    def on_key_pressed(self, key_event: events.KeyPressed, signal):
        if key_event.key == ppb.keycodes.Space:
            signal(
                ppb.events.ReplaceScene(self.next_scene(player=self.player))
            )
            signal(ppb.events.StopScene(self))


class Level1Game(ppb.Scene):
    next_scene = Level2Title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(
            Player(
                direction=ppb.Vector(0, 0),
                position=ppb.Vector(0, -8),
                health=150,
            )
        )
        self.add(HealthBar(position=ppb.Vector(0, -8), health=150))
        self.add(GameBackground())

        for x in range(-4, 5, 2):
            self.add(
                Target(
                    position=ppb.Vector(x, 3),
                    direction=random.choice(
                        [ppb.Vector(1, 0), ppb.Vector(-1, 0)]
                    ),
                    random_movement=True,
                    shoot_frequency=9,
                )
            )

    def on_update(self, update_event, signal):
        player = Player()
        for player_object in update_event.scene.get(kind=Player):
            player = player_object
        # for label in update_event.scene.get(kind=Label):
        #     label.text = str(player.noOflives) + " Lives"
        if not any(True for _ in self.get(kind=Target)):
            signal(ppb.events.ReplaceScene(self.next_scene(player=player)))
            signal(ppb.events.StopScene(scene=self))
        if not any(True for _ in self.get(kind=Player)):
            signal(ppb.events.ReplaceScene(new_scene=GameOver))
            signal(ppb.events.StopScene(scene=self))


class Level1Title(ppb.Scene):
    next_scene = Level1Game

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(Label(text="Level 1"))
        self.add(GameBackground())

    def on_key_pressed(self, key_event: events.KeyPressed, signal):
        if key_event.key == ppb.keycodes.Space:
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))
            signal(ppb.events.StopScene(scene=self))


class LoadScreen(loadingscene.BaseLoadingScene):
    next_scene = Level1Title

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        self.add(GameBackground())

    def get_progress_sprites(self):
        left = LoadingSprite(
            position=ppb.Vector(-4, 0),
            ready_image=ppb.Image("assets/load/left_filled.png"),
            waiting_image=ppb.Image("assets/load/left_empty.png"),
        )
        center = [
            LoadingSprite(position=ppb.Vector(x, 0)) for x in range(-3, 4)
        ]
        right = LoadingSprite(
            position=ppb.Vector(4, 0),
            ready_image=ppb.Image("assets/load/right_filled.png"),
            waiting_image=ppb.Image("assets/load/right_empty.png"),
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


ppb.run(starting_scene=LoadScreen, title="Space Bounce")
