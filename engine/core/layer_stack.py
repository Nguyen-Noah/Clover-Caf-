from typing import List

from engine.core.layer import Layer


class LayerStack:
    def __init__(self):
        self.layers: List[Layer] = []
        self.layer_insert_index = 0

    def push_layer(self, layer: Layer):
        self.layers.insert(self.layer_insert_index, layer)
        self.layer_insert_index += 1

    def push_overlay(self, overlay: Layer):
        self.layers.append(overlay)

    def pop_layer(self, layer: Layer):
        if layer in self.layers:
            self.layers.remove(layer)
            self.layer_insert_index -= 1

    def pop_overlay(self, overlay: Layer):
        if overlay in self.layers:
            self.layers.remove(overlay)

    def __iter__(self):
        return iter(self.layers)