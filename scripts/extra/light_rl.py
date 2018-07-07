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
import json
import logging
import math
import os
import sys
import time
import random

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

# Create default Malmo objects:

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




class QLearner:


    def __init__(self, alpha=0.1, gamma=1., epsilon=0.05, actions=[]):
        self.alpha = alpha # learning rate
        self.gamma = gamma  # discount
        self.epsilon = epsilon # exploration

        self.actions = actions # list of actions
        self.q_table = {} # Q table

        self.logger = logging.getLogger(__name__)

    def act(self,world_state,agent_host, current_R):
        # take an action based on current state
        observations_text = world_state.observations[-1].text
        observation = json.loads(observations_text)

        current_x = int(observation[u'XPos'])
        current_z = int(observation[u'ZPos'])
        current_state = str(current_x)+":"+str(current_z)

        if not current_x in observation or not current_z in observation: # not in observation
            return 0


        if not self.q_table.has_key(current_state):
            self.q_table[current_state] = ([0] * len(self.actions)) # make a row for that state/pos with length possible actions


        # update Q table
        if self.previous_state is not None and self.previous_action is not None:
            old_q = self.q_table[self.previous_state][self.previous_action]
            self.q_table[self.previous_state][self.previous_action] = old_q+self.alpha * (current_R + self.gamma * max(self.q_table[current_state]) - old_q)

        random = random.random()
        if rnd < self.epsilon:
            action = random.randint(0, len(self.actions) - 1)
        else:
            max_value = max(self.q_table[current_state])
            max_value_list = list()
            for i in range(0, len(self.actions)):
                if self.q_table[current_state][i] == max_value:
                    max_value_list.append(i)
            #remove from max_value_list unavailable moves
            max_value_random = random.randint(0, len(max_value_list) -1)
            action = max_value_list[max_value_random]

        agent_host.sendCommand(self.actions[action])
        self.previous_state = current_state
        self.previous_action = action

        return current_R


    def run(self, agent_host):
        #run the agent on the world

        total_reward = 0
        current_R = 0
        tolerance = 0.01

        self.previous_state = None
        self.previous_action = None

        # valid observation
        world_state = agent_host.peekWorldState()
        while world_state.is_mission_running and all(e.text == '{}' for e in world_state.observations):
            world_state = agent_host.peekWorldState()

        # valid frame
        n_frames_seen = world_state.number_of_video_frames_since_last_state
        while world_state.is_mission_running and world_state.number_of_video_frames_since_last_state == n_frames_seen:
            world_state = agent_host.peekWorldState()
        world_state = agent_host.getWorldState()
        
        for e in world_state.errors:
            print e

        if not world_state.is_mission_running:
            return 0

        observation = json.loads(world_state.observations[-1].text)
        previous_x = observation[u'XPos']
        previous_z = observation[u'ZPos']

        total_reward += self.act(world_state, agent_host, current_R)

        require_move = True
        check_expected_position = True

        #main loop
        while world_state.is_mission_running:
            #wait to update position after action
            while True:
                world_state = agent_host.peekWorldState()
                if not world_state.is_mission_running:
                    break
                if len(world_state.rewards) > 0 and not all(e.text=='{}' for e in world_state.observations):
                    observation = json.loads(world_state.observations[-1].text)
                    current_x = observation[u'XPos']
                    current_z = observation[u'ZPos']
                    if require_move:
                        if math.hypot (current_x - previous_x, current_z - previous_z) > tolerance:
                            break
                    else:
                        break


            #wait for new frame
            n_frames_seen = world_state.number_of_video_frames_since_last_state
            while world_state.is_mission_running and world_state.number_of_video_frames_since_last_state == n_frames_seen:
                world_state = agent_host.peekWorldState()

            n_frames_before_get = len(world_state.video_frames)

            world_state = agent_host.getWorldState()

            for e in world_state.errors:
                print e

            if world_state.is_mission_running:
                n_frames_after_get = len(world_state.video_frames)
                frame = world_state.video_frames[-1]
                observation = json.loads(world_state.observations[-1].text)
                current_x = obs[u'XPos']
                current_z = obs[u'ZPos']
                if check_expected_position:
                    expected_x = previous_x + [0,0,-1,1][self.previous_action]
                    expected_z = previous_z + [-1,1,0,0][self.previous_action]
                    if math.hypot( current_x - expected_x, current_z - expected_z) > tolerance:
                        print 'error'
                    else:
                        print 'okay'
                    current_x_from_render = frame.xPos
                    current_z_from_render = frame.zPos
                    if math.hypot( current_x_from_render - expected_x, current_z_from_render - expected_z) > tolerance:
                        print 'error'
                    else:
                        print 'okay'
                else:
                    print
                previous_x = current_x
                previous_z = current_z
                #act
                total_reward += self.act(world_state, agent_host, current_R)
        self.logger.debug("Final reward: %d" % current_R)
        total_reward += current_R

        #update Q values
        if self.previous_state is not None and self.previous_action is not None:
            old_q = self.q_table[self.previous_state][self.previous_action]
            self.q_table[self.previous_state][self.previous_action] = old_q + self.alpha * (current_R - old_q)

        return total_reward




agent_host = MalmoPython.AgentHost()

# add some args
agent_host.addOptionalStringArgument('mission_file',
    'Path/to/file from which to load the mission.', '../Sample_missions/cliff_walking_1.xml')
agent_host.addOptionalFloatArgument('alpha',
    'Learning rate of the Q-learning agent.', 1)
agent_host.addOptionalFloatArgument('epsilon',
    'Exploration rate of the Q-learning agent.', 0.01)
agent_host.addOptionalFloatArgument('gamma', 'Discount factor.', 0.9)
agent_host.addOptionalFlag('load_model', 'Load initial model from model_file.')
agent_host.addOptionalStringArgument('model_file', 'Path to the initial model file', '')
agent_host.addOptionalFlag('debug', 'Turn on debugging.')




for imap in xrange(1):

    # -- set up the agent -- #
    actionSet = ["jumpnorth 1", "jumpsouth 1", "jumpwest 1", "jumpeast 1"]

    agent = QLearner(
        actions=actionSet,
        epsilon=0.01,
        alpha=1,
        gamma=0.9)

    # -- set up the mission -- #
    mission_file = 'cliff_walking_1.xml'
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        mission_xml = f.read()
        my_mission = MalmoPython.MissionSpec(mission_xml, True)
    my_mission.removeAllCommandHandlers()
    my_mission.allowAllDiscreteMovementCommands()
    my_mission.requestVideo( 320, 240 )
    my_mission.setViewpoint( 1 )
    # add holes for interest
    for z in range(2,12,2):
        x = random.randint(1,3)
        my_mission.drawBlock( x,45,z,"lava")

    my_clients = MalmoPython.ClientPool()
    my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

    max_retries = 3
    agentID = 0
    expID = 'tabular_q_learning'

    num_repeats = 150
    cumulative_rewards = []
    for i in range(num_repeats):
        
        print "\nMap %d - Mission %d of %d:" % ( imap, i+1, num_repeats )

        my_mission_record = MalmoPython.MissionRecordSpec( "./save_%s-map%d-rep%d.tgz" % (expID, imap, i) )
        my_mission_record.recordCommands()
        my_mission_record.recordMP4(20, 400000)
        my_mission_record.recordRewards()
        my_mission_record.recordObservations()

        for retry in range(max_retries):
            try:
                agent_host.startMission( my_mission, my_clients, my_mission_record, agentID, "%s-%d" % (expID, i) )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print "Error starting mission:",e
                    exit(1)
                else:
                    time.sleep(2.5)

        print "Waiting for the mission to start",
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            sys.stdout.write(".")
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print "Error:",error.text
        print

        # -- run the agent in the world -- #
        cumulative_reward = agent.run(agent_host)
        print 'Cumulative reward: %d' % cumulative_reward
        cumulative_rewards += [ cumulative_reward ]

        # -- clean up -- #
        time.sleep(0.5) # (let the Mod reset)

    print "Done."

    print
    print "Cumulative rewards for all %d runs:" % num_repeats
    print cumulative_rewards
