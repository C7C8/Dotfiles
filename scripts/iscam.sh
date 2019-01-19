#!/bin/zsh
if pgrep -x "streamer" > /dev/null; then
	echo "  "
else
	echo " "
fi
