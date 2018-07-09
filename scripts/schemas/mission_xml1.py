missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              <ModSettings>
                <MsPerTick>25</MsPerTick>
                <PrioritiseOffscreenRendering>true</PrioritiseOffscreenRendering>
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
                        <DrawBlock x="15" y="226" z="15" type="diamond_block"/>
                    </DrawingDecorator>
                    <ServerQuitFromTimeUp timeLimitMs="100000"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>'''+BOT_NAME+'''</Name>
                <AgentStart>
                    <Placement ''' + BOT_XYZ + ''' />
                </AgentStart>
                <AgentHandlers>
                    <ObservationFromNearbyEntities>
                        <Range name="''' + OBSERVATION_PLAYERS+ '''" xrange="25" yrange="10" zrange="25" /> 
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
