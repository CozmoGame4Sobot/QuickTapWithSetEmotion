"""
Main file for Cozmo's actions
"""
import asyncio
import copy
import cozmo
import time
from cozmo.util import degrees, distance_mm, Pose

from asyncio.locks import Lock
from constants import (
                        START_CUBE,
                        WIN_CUBE,
                        LOSE_CUBE,
                        GOOD_DEAL,
                        PLAYER_ID,
                        COZMO_ID
                    )

from game_engine import SpeedTapEngine
from human_player import Human_Listener
from game_cubes import BlinkyCube
from random import randint

cozmo.world.World.light_cube_factory = BlinkyCube

class CozmoPlayerActions(object):
    """
    A singleton class defining how cozmo will act
    """
    
    __instance = None
    
    def __new__(cls):
      if not CozmoPlayerActions.__instance:
          CozmoPlayerActions.__instance = object.__new__(cls)
          CozmoPlayerActions.__instance.sad_not_angry = True
          CozmoPlayerActions.__instance.reaction_time = 1
      return  CozmoPlayerActions.__instance
    
        
    def set_reaction_time(self, set_time):
        self.reaction_time = set_time
        
    def set_game_lose_reaction(self, is_sad):
        self.sad_not_angry = is_sad
                
    
    def cozmo_tap_decision(self, game_robot, deal_type, speed_tap_game):
        """
        Cozmo deciding to tap
        """
        cozmo_tapped = False
        if deal_type == GOOD_DEAL:
                # The lights match, tap fast to score. Cozmo will tap after the set reaction time
                time.sleep(self.reaction_time)
                game_robot.move_lift(-3)
                time.sleep(.1)
                game_robot.move_lift(4)
                time.sleep(.1)
                #game_robot.play_anim('anim_speedtap_tap_01').wait_for_completed()
                cozmo_tapped = speed_tap_game.register_tap(player=False)
        else:
            # Light is mis-matched or red. If you tap first you lose score.
            wrong_decision = randint(0, 10)
            time.sleep(0.75)
            if wrong_decision in [0, 5, 10]:
                # Cozmo decision to fake a tap
                game_robot.play_anim('anim_speedtap_fakeout_01').wait_for_completed()
            elif wrong_decision == 4 and self.reaction_time > 0.75:
                # Cozmo to take a wrong decision after set time
                game_robot.move_lift(-3)
                time.sleep(.1)
                game_robot.move_lift(4)
                time.sleep(.1)
                game_robot.play_anim('anim_speedtap_tap_02').wait_for_completed()
                cozmo_tapped = speed_tap_game.register_tap(player=False)
        return cozmo_tapped
    
    def select_wait(self):
        """
        Play a wait animation
        """
        wait_anims = ['anim_speedtap_wait_short',
          'anim_speedtap_wait_medium',
          'anim_speedtap_wait_medium_02',
          'anim_speedtap_wait_medium_03',
          'anim_speedtap_wait_long'
          ]
        selected = randint(0,4)
        return wait_anims[selected]
    
    def select_win_game(self):
        """
        PLay a win emotion animation
        """
        win_game_anims =['anim_speedtap_winround_intensity01_01',
                            'anim_speedtap_winround_intensity02_02',
                            'anim_speedtap_winround_intensity02_01',
                            'anim_speedtap_wingame_intensity02_01',
                            'anim_speedtap_wingame_intensity02_02',
                            'anim_speedtap_wingame_intensity03_01']
        cozmo.logger.info("Cozmo win game reacion")
        return win_game_anims[randint(0,5)]
        
    def select_lose_game(self):
        """
        PLay a lose emotion animation. Happy or sad as per manipulation
        """
        if self.sad_not_angry:
            # Play sad animation
            lose_game_anim = ['anim_speedtap_losegame_intensity02_01',
                              'anim_fistbump_fail_01',
                              'anim_keepaway_losegame_02',
                              'anim_memorymatch_failgame_cozmo_03'                                  
                             ]
            cozmo.logger.info("Cozmo sad lose game reacion")            
        else:
            # Play angry  animation
            lose_game_anim = ['anim_speedtap_losegame_intensity03_01',
                             'anim_memorymatch_failgame_cozmo_01',
                             'anim_reacttocliff_stuckrightside_02',
                             'anim_pyramid_reacttocube_frustrated_mid_01']
            cozmo.logger.info("Cozmo angry lose game reacion") 
        return lose_game_anim[randint(0,3)] 
        
    
    def act_out(self, game_robot, act_type):
        """
        Acting out the various emotion displays
        """
        selected_anim = None
        if act_type == "lose_hand":
            # Minor emotion when losing hand
            selected_anim = "anim_speedtap_losehand_0%s" % randint(1, 3)
        elif act_type == "win_hand":
            # Minor emotion when winning a hand
            selected_anim = "anim_speedtap_winhand_0%s" % randint(1, 3)
        elif act_type == "stand_back":
            #Roll back to have space to act, away from cube.
            game_robot.go_to_pose(Pose(-20, 0, 0, angle_z=degrees(0)),
                    relative_to_robot=True).wait_for_completed()
            game_robot.move_lift(-3)
            time.sleep(0.2)
        elif act_type == "win_game":
            # Major win game emotion
            selected_anim = self.select_win_game()
        elif act_type == "lose_game":
            #Major lose game emotion
            selected_anim = self.select_lose_game()
        else:
            # animation to show waiting for light to change
            selected_anim = self.select_wait()
           
        # Play animation
        if selected_anim:
            game_robot.play_anim(selected_anim).wait_for_completed()
            
        

def cozmo_tap_game(robot: cozmo.robot.Robot):
    """
    The main game
    """
    #Setup
    speed_tap_game = SpeedTapEngine(robot)
    robot_game_action = CozmoPlayerActions()
    
    #emotion manipulation
    if robot_game_action.sad_not_angry:
       reaction_bias = "sad"
    else:
       reaction_bias = "angry"
    cozmo.logger.info("Starting tap game with reaction time %s and game reaction bias %s" % (robot_game_action.reaction_time, 
                                                                                             reaction_bias))
    cozmo.logger.info("Player %s : Cozmo " % COZMO_ID)
    cozmo.logger.info("Player %s : Human" % PLAYER_ID)
    # Robot selects cube
    robot_cube, player_cube = speed_tap_game.cozmo_setup_game()
    time.sleep(0.25)
    # Participant select cube
    monitor_player_tap = Human_Listener(robot, player_cube, speed_tap_game)
    game_complete = False
    winner = 0
    score_to = 5 
    
    monitor_player_tap.game_on = True
    monitor_player_tap.start()
    deal_count = 1
    try:
        while not winner:
            # robot wait for the light to change on cube i.e. light to be dealt
            robot_game_action.act_out(robot, "wait")
            deal_type = speed_tap_game.deal_hand()
            cozmo.logger.info("Hand %s delt" % deal_count)
            deal_count += 1
            
            # Cozmo's tap decision 
            tapped = robot_game_action.cozmo_tap_decision(robot, deal_type, speed_tap_game)
            # Give player time to take decision
            time.sleep(1)         
            # Current deal is now deactivated
            speed_tap_game.deactivate_current_deal()  
            #Check who scored and do the right emotion display for winning/losing hand          
            if speed_tap_game.deal_score[-1] == PLAYER_ID:
                if speed_tap_game.deal_score.count(PLAYER_ID) >= score_to:
                    winner = PLAYER_ID
                robot_game_action.act_out(robot, "lose_hand")
            elif speed_tap_game.deal_score[-1] == COZMO_ID:
                if speed_tap_game.deal_score.count(COZMO_ID) >= score_to:
                    winner = COZMO_ID
                robot_game_action.act_out(robot, "win_hand")
            
            # stop light chaser and prep for next round  
            robot_cube.stop_light_chaser()
            player_cube.stop_light_chaser()
            robot_cube.set_lights_off()
            player_cube.set_lights_off()
            
            cozmo.logger.info("Score Board : %s" % speed_tap_game.deal_score)
            cozmo.logger.info("Cozmo : %s" % speed_tap_game.deal_score.count(COZMO_ID))
            cozmo.logger.info("Player : %s" % speed_tap_game.deal_score.count(PLAYER_ID))
             
        # clear up games to show final gameresult    
        robot_cube.stop_light_chaser()
        player_cube.stop_light_chaser()
        robot_cube.set_lights_off()
        player_cube.set_lights_off()
        monitor_player_tap.game_on = False
        robot_game_action.act_out(robot, "stand_back")
       
        
        # Indicate win/loss to player
        if winner == COZMO_ID:
            robot_cube.set_lights(cozmo.lights.green_light.flash())
            player_cube.set_lights(cozmo.lights.red_light.flash())
        elif winner == PLAYER_ID:
            player_cube.set_lights(cozmo.lights.green_light.flash())
            robot_cube.set_lights(cozmo.lights.red_light.flash())
        
        robot.go_to_object(robot_cube, distance_mm(60.0)).wait_for_completed()
        cozmo.logger.info("Final Score Cozmo : %s" % speed_tap_game.deal_score.count(COZMO_ID))
        cozmo.logger.info("Final Score Player : %s" % speed_tap_game.deal_score.count(PLAYER_ID))
             
        # Game end emotion act display     
        if winner == COZMO_ID:
            robot_game_action.act_out(robot, "win_game")
        else:
            robot_game_action.act_out(robot, "lose_game")
            
        
    finally:
         monitor_player_tap.game_on = False
         robot_cube.stop_light_chaser()
         player_cube.stop_light_chaser()
         robot_cube.set_lights_off()
         player_cube.set_lights_off()
         monitor_player_tap.join()
         del speed_tap_game
         del player_cube
         del robot_cube
         
