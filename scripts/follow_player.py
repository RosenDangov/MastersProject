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

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

ARENA_WIDTH = 60
ARENA_BREADTH = 60

OBSERVATION_PLAYERS = "players"
PLAYER_NAME = 'Lightside'
BOT_NAME = 'Light'



def find_player(players):
    for i in range(len(players)):
        if players[i][u'name'] == PLAYER_NAME:
            return True
    return False

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

def calculate_distance(bot,player):
    if bot == {} or player == {}:
        return 0
    squaredX = (math.fabs(bot[u'x'] - player[u'x']))**2
    squaredZ = (math.fabs(bot[u'z'] - player[u'z']))**2
    distance = math.sqrt(squaredX+squaredZ)
    return distance





def calculate_angle(bot, player):
    if bot == {} or player == {}:
        return 0
    yaw = bot[u'yaw']%360
    distance = calculate_distance(bot,player)
    b = math.fabs(bot[u'z'] - player[u'z'])
    a = math.fabs(bot[u'x'] - player[u'x'])

    sinNewYaw = a/distance
    cosNewYaw = b/distance

    sinTheta = math.sin(math.radians(180-yaw))
    cosTheta = math.cos(math.radians(180-yaw))
    phi = math.acos((-a*sinTheta-b*cosTheta)/distance)
    print math.degrees(phi)


    # tanBetta = a/b
    # cosBetta = b/distance
    # bettaR = math.atan(tanBetta)
    # bettaD = math.degrees(bettaR)
    # alpha = bot[u'yaw']%360 - bettaD
    # return alpha

# Create default Malmo objects:

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>12000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>rain</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_2" />
                    <DrawingDecorator>
                        <DrawCuboid x1="-50" z1="-50" y1="150" x2="50" z2="50" y2="250" type="air"/>
                    </DrawingDecorator>
                    <ServerQuitFromTimeUp timeLimitMs="10000"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>'''+BOT_NAME+'''</Name>
                <AgentStart>
                    <Placement x="0" y="152" z="0" yaw="0" />
                </AgentStart>
                <AgentHandlers>
                    <ObservationFromNearbyEntities>
                        <Range name="''' + OBSERVATION_PLAYERS+ '''" xrange="10" yrange="10" zrange="10" /> 
                    </ObservationFromNearbyEntities>
                    <ObservationFromFullStats/>
                    <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''




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
    
    if player_found:
        agent_player = get_player(players)



    for error in world_state.errors:
	    print "Error:",error.text

print
print "Mission ended"
# Mission has ended.