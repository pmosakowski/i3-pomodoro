#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To use it, ensure your ~/.i3status.conf contains this line:
#     output_format = "i3bar"
# in the 'general' section.
# Then, in your ~/.i3/config, use:
#     status_command i3status | ~/i3status/contrib/wrapper.py
# In the 'bar' section.
#
# © 2012 Valentin Haenel <valentin.haenel@gmx.de>
# © 2018 Pawel Mosakowski <pawel@mosakowski.net>
#
# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You can redistribute it and/or modify it under
# the terms of the Do What The Fuck You Want To Public License (WTFPL), Version
# 2, as published by Sam Hocevar. See http://sam.zoy.org/wtfpl/COPYING for more
# details.

import sys
import json

import os
from datetime import timedelta, datetime

path = os.environ['XDG_RUNTIME_DIR'] + '/' + 'i3-pomodoro'

pomodoro_duration = timedelta(seconds = 25*60)
break_duration = timedelta(seconds = 5*60)

red = '#FF0000'
green = '#00FF00'
blue = '#0000FF'

def marker_exists(path):
    return os.path.isfile(path)

def get_marker_age(path):
    return os.path.getmtime(path)

def get_remaining_time(path):
    
    if marker_exists(path):

        age = datetime.fromtimestamp(get_marker_age(path))
        now = datetime.now()

        elapsed = now - age

        if elapsed < pomodoro_duration:
            
            remaining = pomodoro_duration - elapsed
            colour = red
            output = '[' + to_timer(remaining) + ']'

        elif elapsed < pomodoro_duration + break_duration:

            remaining = pomodoro_duration + break_duration - elapsed
            colour = green
            output = '[' + to_timer(remaining) + ']'

        else:

            colour = blue
            output = '[' + 'START' + ']'

    else:

            colour = blue
            output = '[' + 'START' + ']'

    return colour, output

def to_timer(delta):
    delta_seconds = int(delta.total_seconds())
    minutes = delta_seconds // 60
    seconds = delta_seconds % 60
    output = "{:02d}:{:02d}".format(minutes,seconds)
    return output

def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()

def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        if line.startswith(','):
            line, prefix = line[1:], ','

        j = json.loads(line)
        # insert information into the start of the json, but could be anywhere
        # CHANGE THIS LINE TO INSERT SOMETHING ELSE
        colour, output = get_remaining_time(path)
        j.insert(0, {'full_text' : output, 'color': colour, 'name' : 'pomodoro'})
        # and echo back new encoded json
        print_line(prefix+json.dumps(j))
