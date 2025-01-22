from typing import Dict, Tuple

import imgui

from engine.animations.animation_state import AnimationState
from engine.components.component import Component
from engine.components.component_deserializer import register_component
from engine.components.sprite_renderer import SpriteRenderer

@register_component
class StateMachine(Component):
    def __init__(self):
        super().__init__()
        self.state_transfers: Dict[Tuple[str, str], str] = {}
        self.states: Dict[str, AnimationState] = {}
        self.current_state: AnimationState = None
        self.default_state_title = ''

    def add_state_trigger(self, from_str: str, to_str: str, on_trigger: str):
        self.state_transfers[(from_str, on_trigger)] = to_str

    def add_state(self, state: AnimationState):
        self.states[state.title] = state

    def add_directional_state(self, base_title, direction, state: AnimationState):
        full_title = f'{base_title}_{direction}'
        state.title = full_title
        self.states[full_title] = state

    def set_default_state(self, animation_title: str):
        found = self.states.get(animation_title)
        if found is None:
            print(f'Unable to find state {animation_title} in set default state')
        else:
            self.default_state_title = animation_title
            if self.current_state is None:
                self.current_state = found
                return

    def set_direction(self, base_title, direction):
        key = f'{base_title}_{direction}'
        found = self.states[key]
        if found:
            self.current_state = found
        else:
            print(f'Unable to find state {key}')

    def trigger(self, trigger: str):
        key = (self.current_state.title, trigger)
        next_state_title = self.state_transfers.get(key)
        if not next_state_title:
            print(f'Unable to find trigger {trigger}')
            return

        found = self.states.get(next_state_title)
        if found:
            self.current_state = found
        else:
            print(f'Unable to find trigger {trigger}')

    def start(self):
        for state in self.states:
            if state.title == self.default_state_title:
                self.current_state = state
                break

    def imgui(self):
        for state in self.states:
            changed, new_title = imgui.input_text('State: ', state.title, 256)
            if changed:
                state.title = new_title

            for i, frame in enumerate(state.animation_frames):
                changed, new_time = imgui.drag_float(
                    f'Frame({i}) Time: ',
                    frame.frame_time,
                    0.01,
                    0.0,
                    10.0
                )
                if changed:
                    frame.frame_time = new_time

    def _update(self, dt):
        if self.current_state is not None:
            self.current_state.update(dt)
            sprite = self.entity.get_component(SpriteRenderer)
            if sprite is not None:
                sprite.set_sprite(self.current_state.get_current_sprite())

    def editor_update(self, dt):
        self._update(dt)

    def update(self, dt):
        self._update(dt)

    def serialize(self):
        data = super().serialize()
        data.update({
            "default_state_title": self.default_state_title,
            "current_state": self.current_state.serialize(),
        })

        transfers = []
        for state_trigger, to_state_title in self.state_transfers.items():
            transfers.append({
                'from': state_trigger.state,
                'trigger': state_trigger.trigger,
                'to': to_state_title
            })
        data['state_transfers'] = transfers

        states_data = {}
        for anim_state in self.states:
            states_data[anim_state] = self.states.get(anim_state).serialize()

        data['states'] = states_data

        return data

    @classmethod
    def deserialize(cls, data):
        sm = cls()

        sm.default_state_title = data.get('default_state_title', '')

        states_data = data.get('states', {})
        for st_data in states_data:
            sm.states[st_data] = AnimationState.deserialize(states_data[st_data])

        transfers = data.get('state_transfers', [])
        for t in transfers:
            from_state = t.get('from')
            to_state = t.get('to')
            trigger = t.get('trigger')
            if from_state and to_state and trigger:
                sm.add_state_trigger(from_state, to_state, trigger)

        current_state_title = data.get('current_state_title', None)

        if current_state_title:
            for st in sm.states:
                if st.title == current_state_title:
                    sm.current_state = st
                    break

        sm.set_default_state(sm.default_state_title)

        return sm