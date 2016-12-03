#!/bin/bash
prev=`amixer get Master | grep -P 'Front Left' | grep -Po '\d+\%'`
amixer -D pulse sset Master 75%
play "$1"
amixer -D pulse sset Master $prev
