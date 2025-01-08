from enum import Enum

class EventType(Enum):
    GAME_ENGINE_START_PLAY = "GameEngineStartPlay"
    GAME_ENGINE_STOP_PLAY = "GameEngineStopPlay"
    TOGGLE_PHYSICS_DEBUG_DRAW = "TogglePhysicsDebugDraw"
    SAVE_LEVEL = "SaveLevel"
    LOAD_LEVEL = "LoadLevel"
    USER_EVENT = "UserEvent"
