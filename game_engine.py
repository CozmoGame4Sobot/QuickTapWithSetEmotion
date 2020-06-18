"""
This is the main game engine which decides and deals the hands(light combinations)
"""
import asyncio
import copy
import cozmo
import time
from cozmo.util import degrees, distance_mm
import threading

from constants import (
                        START_CUBE,
                        WIN_CUBE,
                        LOSE_CUBE,
                        GOOD_DEAL,
                        PLAYER_ID,
                        COZMO_ID,
                        RED_LIGHT,
                        GREEN_LIGHT,
                        BLUE_LIGHT,
                        YELLOW_LIGHT,
                        PINK_LIGHT,
                        PURPLE_LIGHT,
                        SEA_LIGHT
                    )
from random import randint

thread_lock = threading.Condition()

class SpeedTapEngine:
    
    
    COLOUR_CHOICES = [ (GREEN_LIGHT, PINK_LIGHT),
                     (BLUE_LIGHT, YELLOW_LIGHT),
                     (YELLOW_LIGHT, GREEN_LIGHT),
                     (PINK_LIGHT, BLUE_LIGHT),
                     (PINK_LIGHT,SEA_LIGHT),
                     (SEA_LIGHT, GREEN_LIGHT)
                    ]
    MAX_INDEX = 5
        
    def display_choice(self):
        for i in range(0,6):
            self.robot_cube.set_lights(self.COLOUR_CHOICES[i][0])
            time.sleep(4)
            self.robot_cube.set_lights_off()
            time.sleep(10)
                        
    def __init__(self, game_robot):
        self.robot = game_robot
        self.robot_cube = None
        self.player_cube = None
        self.deal_hand_no = 0
        self.deal_score = []
        self.current_deal_type = None
        
        
    def cozmo_setup_game(self):
        light_cube_list = [cozmo.objects.LightCube1Id, cozmo.objects.LightCube2Id ,cozmo.objects.LightCube3Id ]
        
        # Get the robot to find a cube to play on
        try:
            self.robot.set_head_angle(degrees(0)).wait_for_completed()
            self.robot.move_lift(-3)
            cube = self.robot.world.wait_for_observed_light_cube(timeout=60)
        except asyncio.TimeoutError:
            print("Didn't find a cube :-(")
            return
        # Robot goes and taps cube to claim it
        try:
            cube.start_light_chaser(START_CUBE)
            self.robot.move_lift(3)
            self.robot.go_to_object(cube, distance_mm(35.0)).wait_for_completed()
            ############################
            #needs refining
            self.robot.move_lift(-2)
            time.sleep(.20)
            self.robot.move_lift(2)
            time.sleep(.20)
            tapped_event = self.robot.world.wait_for(cozmo.objects.EvtObjectTapped,timeout=0.1)
            ##############################
        except asyncio.TimeoutError:
            pass
        finally:
            cube.stop_light_chaser()
            cube.set_lights_off()
            cube.set_lights(cozmo.lights.green_light)
        
        self.robot_cube = cube
        
        other_cube_list = []
        
        # Now participant has to claim a cube
        for lightcube_id in light_cube_list:
            other_cube = self.robot.world.light_cubes.get(lightcube_id)
            if other_cube.object_id == self.robot_cube.object_id:
                # the robot's cube should not be lit
                continue
            other_cube.start_light_chaser(START_CUBE)
            other_cube_list.append(other_cube)
        
        try:
            
            tapped_event = self.robot.world.wait_for(cozmo.objects.EvtObjectTapped,timeout=120)
            if tapped_event:
                self.player_cube = tapped_event.obj
            if self.player_cube.object_id == self.robot_cube.object_id:
                print("Cannot play, You took Cozmo's cube!!!")
            else:
                pass
                #print("Player selected Cube: %d" % self.player_cube.object_id)
        except asyncio.TimeoutError:
            print("No-one tapped our cube :-(")
        finally:
            self.robot_cube.set_lights_off()
            for other_cube in other_cube_list:
                other_cube.stop_light_chaser()
                other_cube.set_lights_off()
        
        
        return self.robot_cube, self.player_cube
    
    def deal_hand(self):
        deal_type_id = randint(0,2)
        if deal_type_id == 0:
            # Sly matching red deal. tap to lose score
            self.player_cube.start_hand(RED_LIGHT)
            self.robot_cube.start_hand(RED_LIGHT)
        elif deal_type_id == 2:
            # Both cubes of same colour. Tap and score
            deal_id = randint(0,4)
            colour1, colour2 = self.COLOUR_CHOICES[deal_id]
            self.player_cube.start_hand(colour1, colour2)
            self.robot_cube.start_hand(colour1, colour2)
        else:
            # Both cubes of different coloue. Tap and lose
            deal_id = randint(0,5)
            mismatch_id = randint(0,5)
            if mismatch_id == deal_id:
                # Oops force it to be different
                mismatch_id = deal_id - 1
                if mismatch_id < 0:
                    mismatch_id = self.MAX_INDEX
            colour1, colour2 = self.COLOUR_CHOICES[deal_id]
            colour3, colour4 = self.COLOUR_CHOICES[mismatch_id]
            self.player_cube.start_hand(colour1, colour2)
            self.robot_cube.start_hand(colour3, colour4)
        self.deal_score.append(0)
        self.current_deal_type = deal_type_id
        
        return deal_type_id
    
    def register_tap(self, player=False):
        # Register whether player or robot taps first and score
        tap_registered = False
        #lock scoreboard
        try:
            thread_lock.acquire()
            if self.deal_score[self.deal_hand_no] == 0:
                # Waiting for someone to score
                 
                 if self.current_deal_type == GOOD_DEAL:
                     # For a good hand the tapper scores
                     if player:
                        cozmo.logger.info("Player tapped first, score Player")
                        self.deal_score[self.deal_hand_no] = PLAYER_ID
                        self.player_cube.start_light_chaser(WIN_CUBE)
                        self.robot_cube.set_lights_off()
                     else:
                        cozmo.logger.info("Cozmo tapped  first, score Cozmo")
                        self.deal_score[self.deal_hand_no] = COZMO_ID
                        self.robot_cube.start_light_chaser(WIN_CUBE)
                        self.player_cube.set_lights_off()
                 else:
                     # For a bad hand the person not tapping scores
                     if player:
                        cozmo.logger.info("Player tapped first - no match, score Cozmo")
                        self.deal_score[self.deal_hand_no] = COZMO_ID
                        self.player_cube.start_light_chaser(LOSE_CUBE)
                        self.robot_cube.set_lights_off()
                     else:
                        cozmo.logger.info("Cozmo tapped first - no match, score Player")
                        self.deal_score[self.deal_hand_no] = PLAYER_ID
                        self.robot_cube.start_light_chaser(LOSE_CUBE)
                        self.player_cube.set_lights_off()
                 tap_registered = True
                 self.deactivate_current_deal()
        except IndexError:
            # Tap registered outside active life
            pass
        finally:
            thread_lock.notify_all()
            thread_lock.release()
        
        return tap_registered
    
    def deactivate_current_deal(self):
        try:
            check = self.deal_score[self.deal_hand_no]
            self.deal_hand_no += 1
        except IndexError:
            # current deal is already inactive
            pass
        
                
    
        