# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #1: Run simple mission

import MalmoPython
import os
import sys
import time
import json
import math
import logging
import random
import numpy
import Tkinter as tk










sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

ARENA_WIDTH = 60
ARENA_BREADTH = 60

OBSERVATION_PLAYERS = "players"
PLAYER_NAME = 'Lightside'
BOT_NAME = 'Light'


def placement3(x,y,z):
    return 'x="%s" y="%s" z="%s" yaw="0"' % (str(x),str(y),str(z))
def placement1(xyz):
    return 'x="%s" y="%s" z="%s" yaw="0"' % (str(xyz[0]),str(xyz[1]),str(xyz[2]))

BOT_XYZ = (0.5,227,0.5)

def find_player(players):
    for i in range(len(players)):
        if players[i][u'name'] == PLAYER_NAME:
            return True
    return False

def find_goal(grid):
    return u'diamond_block' in grid

def get_player(players):
    for i in range(len(players)):
        if players[i][u'name'] == PLAYER_NAME:
            return players[i]
    return False

def get_bot(players):
    for i in range(len(players)):
        if players[i][u'name'] == BOT_NAME:
            return players[i]
    return False

def get_xyz(bot):
    return (bot[u'x'],bot[u'y'],bot[u'z'])

def calculate_distance(bot,player):
    if bot == {} or player == {}:
        return 0
    squaredX = (math.fabs(bot[u'x'] - player[u'x']))**2
    squaredZ = (math.fabs(bot[u'z'] - player[u'z']))**2
    distance = math.sqrt(squaredX+squaredZ)
    return distance

def follow_player(bot,player,host):
    direction = ""

    if bot[u'x'] - player[u'x'] > 1.5:
        direction = "west"
    if bot[u'x'] - player[u'x'] < -1.5:
        direction = "east"
    if bot[u'z'] - player[u'z'] > 1.5:
        direction = "north"
    if bot[u'z'] - player[u'z'] < -1.5:
        direction = "south"
    if bot[u'y'] == player[u'y']:
        move = "move"
    else:
        move = "jump"
    if direction == "":
        return
    host.sendCommand("%s%s 1" % (move, direction))

def check_for_bumps(bot,host):
    if bot[u'x'] % 1 != 0.5:
        corrected_x = int(bot[u'x']) + 0.5
        agent_host.sendCommand("tpx %s" % corrected_x)
    if bot[u'z'] % 1 != 0.5:
        corrected_z = int(bot[u'z']) + 0.5
        agent_host.sendCommand("tpz %s" % corrected_z)

def int_xyz(xyz):
    return (int(xyz[0]),int(xyz[1]),int(xyz[2]))




def process_path(path):
    optimised_path = []
    for point in path:
        if point not in optimised_path:
            optimised_path.append(point)
        else:
            optimised_path = optimised_path[0:optimised_path.index(point)]
            optimised_path.append(point)
        print optimised_path
    return optimised_path

def path_to_actions(path):
    actions = []
    for i in range(1,len(path)):
        if(tuple(numpy.subtract(path[i],path[i-1])) == (-1,0,0)):
            actions.append("movewest 1")
            continue
        if(tuple(numpy.subtract(path[i],path[i-1])) == (1,0,0)):
            actions.append("moveeast 1")
            continue
        if(tuple(numpy.subtract(path[i],path[i-1])) == (0,0,1)):
            actions.append("movesouth 1")
            continue
        if(tuple(numpy.subtract(path[i],path[i-1])) == (0,0,-1)):
            actions.append("movenorth 1")
            continue
    print actions
    return actions



def _3d_point_to_int(xyz):
    dim = 11
    return xyz[0] + dim*dim*xyz[1] + dim*xyz[2]



def state_actions_fd(bot,player,path,actions,start,goal,observation):
    # start and goal are absolute positions
    # bot and player are absolute positions
    # path contains relative position
    # observation contains 11x11x11 around bot
    if bot == {} or player == {}:
        return
    player_table = {}
    for i in range(0,len(path)-1):
        # state: [Xdist,Ydist,Zdist,NSblock,WEblock]
        x_dist = abs(path[i][0]+start[0] - goal[0])
        y_dist = abs(path[i][1]+start[1] - goal[1])
        z_dist = abs(path[i][2]+start[2] - goal[2])


        #tuple distance between chars + 5
        observation_tuple = (5+path[i][0]+start[0]-int(bot[u'x']),5+path[i][1]+start[1]-int(bot[u'y']),5+path[i][2]+start[2]-int(bot[u'z']))


        if path[i][2]+start[2] - goal[2] > 0:
            block_tuple = tuple(numpy.add(observation_tuple,(0,0,-1)))
            print _3d_point_to_int(block_tuple), block_tuple, "north"
            ns_block = observation[_3d_point_to_int(block_tuple)]
        elif path[i][2]+start[2] - goal[2] == 0:
            ns_block = "none"
        else:
            block_tuple = tuple(numpy.add(observation_tuple,(0,0,1)))
            print _3d_point_to_int(block_tuple), block_tuple, "south"
            ns_block = observation[_3d_point_to_int(block_tuple)]
        if path[i][0]+start[0] - goal[0] > 0:
            block_tuple = tuple(numpy.add(observation_tuple,(-1,0,0)))
            print _3d_point_to_int(block_tuple), block_tuple, "west"
            we_block = observation[_3d_point_to_int(block_tuple)]
        elif path[i][0]+start[0] - goal[0] == 0:
            we_block = "none"
        else:
            block_tuple = tuple(numpy.add(observation_tuple,(1,0,0)))
            print _3d_point_to_int(block_tuple), block_tuple, "east"
            we_block = observation[_3d_point_to_int(block_tuple)]

        print x_dist,y_dist,z_dist,ns_block,we_block











agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)



mission_file = "cliff_climbing_lfd.xml"
with open(mission_file, 'r') as f:
    print "Loading mission from %s" % mission_file
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
my_mission_record = MalmoPython.MissionRecordSpec()


# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:",e
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()

while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()


    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission running ",

player_found = False
following_player = False
learning = False
playing = False
busy = False
agent_player = {}
agent_bot = {}


start = (4,46,1)
goal = (1,46,2)
player_history = [(0,0,0)]
player_table = {}
learning = True


# Loop until mission ends:
while world_state.is_mission_running:

    world_state = agent_host.getWorldState()
    time.sleep(0.1)
    if world_state.number_of_observations_since_last_state > 0:


        msg = world_state.observations[-1].text
        ob = json.loads(msg)

        players = []
        obs_learning_area = []
        if "players" in ob:
            players = ob["players"]
        if "learning_area" in ob:
            obs_learning_area = ob["learning_area"]
            # for i in range(1331):
            #     if obs_learning_area[i] == "gold_ore":
            #         print i
        agent_bot = get_bot(players)
        player_found = find_player(players)
        if player_found:
            agent_player = get_player(players)

    if learning and player_found:
        moved = True
        step = tuple(numpy.subtract(int_xyz(get_xyz(agent_player)), start))
        if step == player_history[-1]:
            moved = False
            if step == tuple(numpy.subtract(goal, start)):
                learning = False
                print "Path learned"
                player_history = process_path(player_history)
                actions = path_to_actions(player_history)
                player_table = (state_actions_fd(agent_bot,agent_player,player_history,actions,start,goal,obs_learning_area))
        if moved:
            player_history.append(step)
            print player_history




    #     goal_vision = []
    #     if "goal_vision" in ob:
    #         goal_vision = ob["goal_vision"]
    #     goal_found = find_goal(goal_vision)

    #     if goal_found and not following_player and not busy:
    #         following_player = False
    #         agent_host.sendCommand("quit")
    #         time.sleep(0.2)
    #         my_mission = MalmoPython.MissionSpec(generateXML(get_xyz(agent_bot)),True)
    #         my_mission_record = MalmoPython.MissionRecordSpec()
    #         agent_host.startMission(my_mission,my_mission_record)
    #         time.sleep(1)
    #         busy = True

    
    # if following_player:
    #     agent_player = get_player(players)
    #     if following_player:
    #         follow_player(agent_bot,agent_player,agent_host)
    #     check_for_bumps(agent_bot,agent_host)
    #     time.sleep(0.1)

    # if not following_player and not busy:
    #     agent_host.sendCommand("movesouth 1")

    # if busy:
    #     agent_host.sendCommand("jump 1")


    for error in world_state.errors:
	    print "Error:",error.text

print
print "Mission ended"
# Mission has ended.