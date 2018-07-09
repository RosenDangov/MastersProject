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
    return false

def get_bot_xyz(bot):
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



# Create default Malmo objects:

def generateXML(placement_xyz):
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              <ModSettings>
                <MsPerTick>25</MsPerTick>
                <PrioritiseOffscreenRendering>false</PrioritiseOffscreenRendering>
              </ModSettings>
              <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>12000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                    <AllowSpawning>false</AllowSpawning>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_2" />
                    
                    <DrawingDecorator>
                        <DrawBlock x="1" y="226" z="15" type="diamond_block"/>
                    </DrawingDecorator>
                    <ServerQuitFromTimeUp timeLimitMs="100000"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>''' + BOT_NAME + '''</Name>
                <AgentStart>
                    <Placement ''' + placement1(placement_xyz) + ''' />
                </AgentStart>
                <AgentHandlers>
                    <ObservationFromNearbyEntities>
                        <Range name="''' + OBSERVATION_PLAYERS + '''" xrange="25" yrange="10" zrange="25" /> 
                    </ObservationFromNearbyEntities>
                    <ObservationFromGrid>
                        <Grid name="goal_vision">
                            <min x="-5" y="-5" z="-5"/>
                            <max x="5" y="5" z="5"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ObservationFromFullStats/>
                    <DiscreteMovementCommands/>
                    <ChatCommands/>
                    <MissionQuitCommands/>
                    <AbsoluteMovementCommands/>
                    <ContinuousMovementCommands turnSpeedDegs="180"/>
                    <AgentQuitFromCollectingItem>
                        <Item type="stick"/>
                    </AgentQuitFromCollectingItem>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''
    return xml

missionXML = generateXML(BOT_XYZ)





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

my_mission = MalmoPython.MissionSpec(missionXML,True)
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


# Loop until mission ends:
while world_state.is_mission_running:


    world_state = agent_host.getWorldState()
    time.sleep(0.1)
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)

        players = []
        if "players" in ob:
            players = ob["players"]
        agent_bot = get_bot(players)
        player_found = find_player(players)



        goal_vision = []
        if "goal_vision" in ob:
            goal_vision = ob["goal_vision"]
        goal_found = find_goal(goal_vision)

        if goal_found and not following_player and not busy:
            following_player = False
            agent_host.sendCommand("quit")
            time.sleep(0.2)
            my_mission = MalmoPython.MissionSpec(generateXML(get_bot_xyz(agent_bot)),True)
            my_mission_record = MalmoPython.MissionRecordSpec()
            agent_host.startMission(my_mission,my_mission_record)
            time.sleep(1)
            busy = True

    
    if following_player:
        agent_player = get_player(players)
        if following_player:
            follow_player(agent_bot,agent_player,agent_host)
        check_for_bumps(agent_bot,agent_host)
        time.sleep(0.1)

    if not following_player and not busy:
        agent_host.sendCommand("movesouth 1")

    if busy:
        agent_host.sendCommand("jump 1")


    for error in world_state.errors:
	    print "Error:",error.text

print
print "Mission ended"
# Mission has ended.