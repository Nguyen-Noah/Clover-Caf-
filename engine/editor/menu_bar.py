import imgui
from engine.observers.event_system import EventSystem
from engine.editor.game_view_window import GameViewWindow
from engine.observers.events.event import Event, EventType

class MenuBar:
    def __init__(self):
        pass

    def imgui(self):
        with imgui.begin_main_menu_bar():
            if imgui.begin_menu('File').opened:
                clicked, _ = imgui.menu_item('Save', 'Ctrl+S')
                if clicked:
                    EventSystem.notify(Event(EventType.SAVE_LEVEL))
                
                clicked, _ = imgui.menu_item('Load', 'Ctrl+O')
                if clicked:
                    EventSystem.notify(Event(EventType.LOAD_LEVEL))

                imgui.end_menu()

            is_playing = GameViewWindow.is_playing
            clicked, _ = imgui.menu_item('Play', '', is_playing, not is_playing)
            if clicked:
                is_playing = True
                EventSystem.notify(Event(EventType.GAME_ENGINE_START_PLAY))

            clicked, _ = imgui.menu_item('Stop', '', not is_playing, is_playing)
            if clicked:
                is_playing = False
                EventSystem.notify(Event(EventType.GAME_ENGINE_STOP_PLAY))
            GameViewWindow.is_playing = is_playing
