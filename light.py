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

def generate_line(block, start_pos,end_pos):
    return '<DrawLine x1="'+str(start_pos[0])+'" y1="'+str(start_pos[1])+'" z1="'+str(start_pos[2])+'" x2="'+str(end_pos[0])+'" y2="'+str(end_pos[1])+'" z2="'+str(end_pos[2])+'" type="'+block+'"/>'

def generate_cube(block,start_pos,end_pos):
    return '<DrawCuboid x1="'+str(start_pos[0])+'" y1="'+str(start_pos[1])+'" z1="'+str(start_pos[2])+'" x2="'+str(end_pos[0])+'" y2="'+str(end_pos[1])+'" z2="'+str(end_pos[2])+'" type="'+block+'"/>'

def generate_entity(entity, start_pos):
    return '<DrawEntity x="'+str(start_pos[0])+ '" y="'+str(start_pos[1])+'" z="'+str(start_pos[2])+'" type="'+entity+'"/>'
    
def generate_borders():
    toReturn = ""
    toReturn += generate_line("gold_block", (50,149,0),(50,149,150))
    toReturn += generate_line("gold_block", (100,149,0),(100,149,150))
    
    toReturn += generate_line("gold_block", (0,149,50),(150,149,50))
    toReturn += generate_line("gold_block", (0,149,100),(150,149,100))

    return toReturn

def generate_zoo():
    toReturn = ""
    toReturn += generate_line("planks",(0,150,50),(50,150,50))
    toReturn += generate_line('oak_stairs" face="NORTH',(0,150,51),(50,150,51))
    toReturn += generate_line('oak_stairs" face="NORTH',(0,151,50),(50,151,50))

    toReturn += generate_line("planks",(50,150,0),(50,150,50))
    toReturn += generate_line('oak_stairs" face="WEST',(51,150,0),(51,150,50))
    toReturn += generate_line('oak_stairs" face="WEST',(50,151,0),(50,151,50))

    for i in range(10):
        toReturn += generate_entity("Chicken", (25,152,25))

    toReturn += generate_cube("grass", (25,149,25),(35,149,35))
    
    return toReturn

def generate_cliff():
    toReturn = "" 
    toReturn += generate_cube("planks", (120,150,0), (150,160,35))

    return toReturn

def generate_fall():
    toReturn = "" 
    toReturn += generate_cube("planks", (115,150,115),(130,160,150))
    for i in range(11):
        toReturn += generate_line('oak_stairs" face="EAST',(105+i,150+i,115),(105+i,150+i,150))

    return toReturn

def generate_bridge():
    toReturn ="" 
    toReturn += generate_cube("planks", (145,150,60),(150,155,90))
    toReturn += generate_cube("planks", (105,150,60),(115,155,90))
    toReturn += generate_cube("planks", (116,155,61),(135,155,70))
    toReturn += generate_cube("planks", (116,155,71),(125,155,80))
    for i in range(6):
        toReturn += generate_line('oak_stairs" face="EAST',(100+i,150+i,60),(100+i,150+i,90))

    return toReturn

# Create default Malmo objects:

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>6000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                    <AllowSpawning>true</AllowSpawning>
                    <AllowedMobs>Chicken</AllowedMobs>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
                    <DrawingDecorator>
                        <!-- 150x150 cube general area -->
                        <DrawCuboid x1="0" z1="0" y1="150" x2="150" z2="150" y2="250" type="air"/>
                        ''' + generate_zoo() + '''
                        ''' + generate_cliff() + '''
                        ''' + generate_fall() + '''
                        ''' + generate_bridge() + '''
                        ''' + generate_borders() + '''

                    </DrawingDecorator>
                    <ServerQuitFromTimeUp timeLimitMs="1"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>'''+BOT_NAME+'''</Name>
                <AgentStart>
                    <Placement x="75" y="152" z="75" yaw="0" />
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