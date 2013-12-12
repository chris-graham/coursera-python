import simplegui

attempts = 0
running = False
successes = 0
time = 0

def format(t):
    """
    converts time in tenths of seconds into formatted string A:BC.D
    """
    milliseconds = t % 10
    seconds = (t // 10) % 60
    minutes = (t // 10) // 60

    if seconds < 10:
        return str(minutes) + ":" + "0" + str(seconds) + "." + str(milliseconds)
    else:
        return str(minutes) + ":" + str(seconds) + "." + str(milliseconds)

# event handlers
def start_stopwatch():
    global running

    running = True
    timer.start()

def stop_stopwatch():
    """
    stops timer first to avoid any extra executions of stopwatch(), 
    then updates the state of the game if the stopwatch was running
    """
    timer.stop()

    global attempts, running, successes

# verify stopwatch was running before updating game state
    if running:
        running = False
        attempts += 1

        if time % 10 == 0:
            successes += 1

def reset_stopwatch():
    """
    stops timer and resets the state of the game
    """
    timer.stop()

    global attempts, running, successes, time

    time = 0
    attempts = 0
    successes = 0
    running = False

def stopwatch():
    """
    timer handeler - increments the time global variable every millisecond 
    """
    global time

    time += 1

def draw(canvas):
    """
    draws the stopwatch and attempts / successes text; additionally shifts text as
    number of digits increase in attempts / successes (I thought this was prettier!)
    """
    # determine pixel width of stats in order to align stats in the top right corner
    stats_width = 250 - f.get_canvas_textwidth(str(successes) + "/" + str(attempts), 24)

    canvas.draw_text(format(time), (63.5, 116), 50, "White")
    canvas.draw_text(str(successes) + "/" + str(attempts), (stats_width, 19), 24, "Green")

# create frame
f = simplegui.create_frame("Stopwatch: The Game", 250, 200)

# register event handlers
f.set_draw_handler(draw)
f.add_button("Start", start_stopwatch, 100)
f.add_button("Stop", stop_stopwatch, 100)
f.add_button("Reset", reset_stopwatch, 100)
timer = simplegui.create_timer(100, stopwatch)

# start frame
f.start()