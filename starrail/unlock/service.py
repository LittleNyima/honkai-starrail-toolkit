from starrail.unlock.fps import safe_set_fps

default_fps = 60


def unlock_fps(fps: int, reset: bool):
    if reset:
        fps = default_fps
    if fps:
        safe_set_fps(fps)
