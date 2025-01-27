import imgui
from engine.ecs.system import System
from engine.components.sprite_renderer import SpriteRenderer
from engine.components.state_machine import StateMachine

class StateMachineSystem(System):
    def __init__(self):
        super().__init__()

    def _update(self, dt):
        for entity, state_machine, sprite in self.world.get_components(StateMachine, SpriteRenderer):
            if state_machine.current_state is not None:
                state_machine.current_state.update(dt)
                if sprite is not None:
                    sprite.set_sprite(state_machine.current_state.get_current_sprite())

    def process(self, dt):
        self._update(dt)

    def update(self, dt):
        self._update(dt)

    @staticmethod
    def trigger(entity, trigger):
        state_machine = entity.get_component(StateMachine)
        if not state_machine or not state_machine.current_state_title:
            return

        key = (state_machine.current_state_title, trigger)
        next_state_title = state_machine.state_transfers[key]
        if not next_state_title:
            print(f'Unable to find trigger {trigger} from state {state_machine.current_state_title}')

        if next_state_title in state_machine.states:
            state_machine.current_state_title = next_state_title
            print(f'Entity {entity.uid} transitioned to state {next_state_title}.')
        else:
            print(f'State {next_state_title} does not exist in the state machine.')

    def imgui(self):
        # Optional: Provide imgui interface for debugging or editing state machines
        for entity, state_machine, sprite_renderer in self.world.get_components(StateMachine, SpriteRenderer):
            if imgui.begin(f"Entity {entity.uid} - State Machine"):
                imgui.text(f'Current State: {state_machine.current_state.title}')
                trigger_input = ""
                changed, trigger_input = imgui.text(f'Trigger Entity {entity.uid}')
                if changed and trigger_input:
                    print('sdfklj')
                    self.trigger(entity, trigger_input)
            imgui.end()