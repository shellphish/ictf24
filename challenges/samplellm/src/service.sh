#!/bin/bash

timeout 180 /home/challenge/src/rate_limiter.py &&
source /tmp/ictf.env &&
timeout 180 /home/challenge/src/challenge.py
