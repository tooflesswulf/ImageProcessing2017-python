"""
For now this serves as a test program to perfect the vision pipeline and
display results. Later we will have a server that communicates this
information.
"""

import os
import cv2
import gstreamer as gs
Gst = gs.Gst

try:
    os.remove(gs.SOCKET_PATH)
except FileNotFoundError:
    pass

process = gs.raspicam_streaming_process(gs.STREAM_HOST, gs.STREAM_PORT)
cap_string = gs.get_caps_from_process_and_wait(process)

print(cap_string)

# Code for using webcam is below
# pipeline = gs.webcam_streaming_pipeline(gs.STREAM_HOST, gs.STREAM_PORT)
# pipeline.set_state(Gst.State.PLAYING)

# # TODO: Find a better method to wait for playback to start
# print(pipeline.get_state(Gst.CLOCK_TIME_NONE)) # Wait for pipeline to play

# caps = gs.get_sink_caps(pipeline.get_by_name(gs.SINK_NAME))
# cap_string = gs.make_command_line_parsable(caps)

cap = cv2.VideoCapture(gs.webcam_loopback_command(cap_string))

while True:
    _, img = cap.read()
    cv2.imshow('frame', img)
    if cv2.waitKey(1) == ord('q'):
        break

# TODO I cannot think of any way to kill GStreamer through the process given by
# raspicam_streaming_process. Ideally it would be nice to use something nicer.
os.system('killall gst-launch-1.0')
