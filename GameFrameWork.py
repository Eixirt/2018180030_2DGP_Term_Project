import time


class GameState:
    def __init__(self, state):
        self.enter_state = state.enter_state
        self.exit_state = state.exit_state
        self.pause_state = state.pause_state
        self.resume_state = state.resume_state
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw


class TestGameState:

    def __init__(self, name):
        self.name = name

    def enter_state(self):
        print("State [%s] Entered" % self.name)

    def exit_state(self):
        print("State [%s] Exited" % self.name)

    def pause_state(self):
        print("State [%s] Paused" % self.name)

    def resume_state(self):
        print("State [%s] Resumed" % self.name)

    def handle_events(self):
        print("State [%s] handle_events" % self.name)

    def update(self):
        print("State [%s] update" % self.name)

    def draw(self):
        print("State [%s] draw" % self.name)


running = None
stack = None
frame_time = 0.0


def change_state(state):
    global stack
    if len(stack) > 0:
        # execute the current state's exit function
        stack[-1].exit_state()
        # remove the current state
        stack.pop()
    stack.append(state)
    state.enter_state()


def push_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].pause_state()
    stack.append(state)
    state.enter_state()


def pop_state():
    global stack
    if len(stack) > 0:
        # execute the current state's exit function
        stack[-1].exit_state()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if len(stack) > 0:
        stack[-1].resume_state()


def quit_state():
    global running
    running = False


def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter_state()

    global frame_time
    current_time = time.time()

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        # frame_rate = 1.0 / frame_time
        current_time += frame_time
        pass

    # repeatedly delete the top of the stack
    while len(stack) > 0:
        stack[-1].exit_state()
        stack.pop()


def test_game_framework():
    start_state = TestGameState('StartState')
    run(start_state)


if __name__ == '__main__':
    test_game_framework()

