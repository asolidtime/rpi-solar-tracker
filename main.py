from soltrack import SolTrack
import datetime as dt
import AccelStepper
import RPi.GPIO as gp
import utils
import solarglobals
import signal, sys
import steppermovementsystem as step
solarglobals.init()

geo_lon = 41.6578
geo_lat = 91.5346

st = SolTrack(geo_lon, geo_lat, use_degrees=True)
st.set_date_time(dt.datetime.now())
st.compute_position()

step.move_alt_to(st.altitude)
step.move_azi_to(st.azimuth)
step.run_steppers_to_position()
print("Done moving steppers to position")
print("Corrected azimuth, altitude:         %10.6lf° %10.6lf°"     % (st.azimuth, st.altitude))
print()

def signal_handler(sig, frame):
    print('Ctrl-C pressed, returning steppers to default positions')
    step.move_alt_to(0)
    step.move_azi_to(0)
    step.run_steppers_to_position()
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)
while True:
    st.set_date_time(dt.datetime.now())
    st.compute_position()
    step.move_alt_to(st.altitude)
    step.move_azi_to(st.azimuth)
    step.run_steppers_to_position()

