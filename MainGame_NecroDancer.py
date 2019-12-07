import pico2d
import GameFrameWork

import StartState

CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 720

pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
GameFrameWork.run(StartState)
pico2d.close_canvas()

