from time import process_time_ns, sleep

def ticks_us():
    return process_time_ns() / 1000

def sleep_ms(ms):
    sleep(float(ms) / 1000.0)

def sleep_us(us):
    sleep_ms(float(us) / 1000.0)

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))