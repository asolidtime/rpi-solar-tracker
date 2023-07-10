import AccelStepper
import solarglobals, utils
import RPi.GPIO as gp



steps_per_rev = 3200
min_pulse_width_us = 1000
stepper_conversion_factor = steps_per_rev/360

gp.setmode(gp.BCM)
gp.setup(22, gp.OUT)
gp.setup(27, gp.OUT)
gp.setup(17, gp.OUT)
gp.setup(18, gp.OUT) #azimuth stepper STEP pin


#TODO: this is a common-cathode 8-segment, so we may have to reverse these once connected to an actual stepper driver
def alt_step_forward():
    gp.output(22, True)
    utils.sleep_us(min_pulse_width_us)
    gp.output(22, False)
    gp.output(27, True)
    solarglobals.gpstate = not solarglobals.gpstate
    #print("alt f")

def alt_step_backward():
    gp.output(22, True)
    utils.sleep_us(min_pulse_width_us)
    gp.output(22, False)
    gp.output(27, False)
    solarglobals.gpstate = not solarglobals.gpstate
    #print("alt b")


def azi_step_forward():
    gp.output(18, True)
    utils.sleep_us(min_pulse_width_us)
    gp.output(18, False)
    gp.output(17, True)
    solarglobals.gpstate = not solarglobals.gpstate
    #print("azi f")

def azi_step_backward():
    gp.output(18, True)
    utils.sleep_us(min_pulse_width_us)
    gp.output(18, False)
    gp.output(17, False)
    solarglobals.gpstate = not solarglobals.gpstate
    #print("azi b")





altstepper = AccelStepper.AccelStepper(alt_step_forward, alt_step_backward)
azistepper = AccelStepper.AccelStepper(azi_step_forward, azi_step_backward)
altstepper.set_acceleration(800)
altstepper.set_max_speed(1500)
azistepper.set_acceleration(800)
altstepper.set_max_speed(1500)

def move_alt_to(loc): # todo: conversion from degrees to steps
    altstepper.move_to(int(loc * stepper_conversion_factor))

def move_azi_to(loc):
    azistepper.move_to(int(loc * stepper_conversion_factor))



def evalboth(): # if this were a normal or statement, altstepper.run() wouldn't be evaluated until azistepper.run() returned false
    one = azistepper.run()
    two = altstepper.run()
    return one or two

def run_steppers_to_position():
    while evalboth():
        pass

def cleanup():
    gp.cleanup()