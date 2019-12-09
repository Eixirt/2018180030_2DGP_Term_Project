import pico2d
import GameFrameWork
import MainState


class TimingManager:
    ACCURATE_TIMING = 0.6
    TIMING_RANGE = 0.15

    def __init__(self):
        self.timer = 0
        pass

    def update(self):
        self.timer += GameFrameWork.frame_time
        pass

    def check_timing(self, check_input):

        if TimingManager.ACCURATE_TIMING + TimingManager.TIMING_RANGE < self.timer < TimingManager.ACCURATE_TIMING + TimingManager.TIMING_RANGE and check_input is True:
            self.timer = 0
            return True
        else:
            self.timer = 0
            return False
        pass

    def draw(self):
        pass

    pass
