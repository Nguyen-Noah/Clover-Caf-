import pickle

import imgui

from engine.utils.elements import ElementSingleton

class SceneHierarchyWindow(ElementSingleton):
    def __init__(self):
        super().__init__()

    def imgui(self):
        imgui.begin('Scene Hierarchy')

        entities = self.e['Game'].current_scene.entities
        index = 0
        for entity in entities:
            if not entity.do_serialization:
                continue

            tree_node_open = self.do_tree_node(entity, index)
            if tree_node_open:
                imgui.tree_pop()

            index += 1

        imgui.end()

    def do_tree_node(self, entity, index):
        imgui.push_id(str(index))
        tree_node_open = imgui.tree_node(entity.name,
                                         imgui.TREE_NODE_DEFAULT_OPEN | imgui.TREE_NODE_FRAME_PADDING | imgui.TREE_NODE_OPEN_ON_ARROW | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH,
                                         )

        imgui.pop_id()

        """ if imgui.begin_drag_drop_source():
            entity_bytes = pickle.dumps(entity.serialize())
            imgui.set_drag_drop_payload('SceneHierarchy', entity_bytes)
            imgui.text(entity.name)

            imgui.end_drag_drop_source()

        if imgui.begin_drag_drop_target():
            payload_obj = imgui.accept_drag_drop_payload('SceneHierarchy')
            print(payload_obj)
            if payload_obj is not None:
                print(payload_obj.__class__)

            imgui.end_drag_drop_target() """

        return tree_node_open