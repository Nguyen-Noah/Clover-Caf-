from engine.animations.animation_state import AnimationState
from engine.components.sprite_renderer import SpriteRenderer
from engine.components.state_machine import StateMachine


class Prefabs:
    @staticmethod
    def generate_sprite_object(e, sprite, size_x, size_y):
        block = e['Game'].current_scene.create_entity(name='Sprite_Object_Gen')
        block.transform.scale.x = size_x
        block.transform.scale.y = size_y
        renderer = SpriteRenderer(sprite=sprite)
        block.add_component(renderer)
        return block

    @staticmethod
    def generate_player(e, size_x, size_y):
        player_state = 'idle_down'
        player_sprites = e['Assets'].get_spritesheets('animations/player/idle')
        player = Prefabs.generate_sprite_object(e, player_sprites.get_state_sprite(player_state, 0), size_x, size_y)

        idle = AnimationState(player_state)
        default_frame_time = 0.23
        idle.add_frame(player_sprites.get_state_sprite(idle.title, 0), default_frame_time)
        idle.add_frame(player_sprites.get_state_sprite(idle.title, 1), default_frame_time)
        idle.add_frame(player_sprites.get_state_sprite(idle.title, 2), default_frame_time)
        idle.add_frame(player_sprites.get_state_sprite(idle.title, 3), default_frame_time)

        state_machine = StateMachine()
        state_machine.add_state(idle)
        state_machine.set_default_state(idle.title)

        player.add_component(state_machine)

        return player