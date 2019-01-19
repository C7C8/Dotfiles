#!/bin/zsh
if ! pkill -x "streamer" -SIGTERM > /dev/null
then
	padsp streamer -q -c /dev/video0 -f jpeg -F mono16 -r 30 -t 01:00:00 -o ~/"Videos/Recorded/Webcam/$(date).avi" &
fi

