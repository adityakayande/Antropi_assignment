#!/bin/bash
# Spawns a 0.5 m red box that the saved map does not contain.
# Usage: ./spawn_obstacle.sh [x] [y] [name]
X=${1:-0.5}; Y=${2:-0.5}; NAME=${3:-box1}
WORLD=$(gz service -l | grep -o '/world/[^/]*/create' | head -1 | cut -d/ -f3)
gz service -s /world/$WORLD/create --reqtype gz.msgs.EntityFactory --reptype gz.msgs.Boolean --timeout 2000 --req "sdf: \"<sdf version=\\\"1.9\\\"><model name=\\\"$NAME\\\"><pose>$X $Y 0.25 0 0 0</pose><static>true</static><link name=\\\"l\\\"><collision name=\\\"c\\\"><geometry><box><size>0.5 0.5 0.5</size></box></geometry></collision><visual name=\\\"v\\\"><geometry><box><size>0.5 0.5 0.5</size></box></geometry><material><ambient>1 0 0 1</ambient></material></visual></link></model></sdf>\""
