from starrail.unlock.fps import set_fps

default_fps = 60


def unlock_fps(fps: int, reset: bool):
    if reset:
        fps = default_fps
    if fps:
        set_fps(fps)
