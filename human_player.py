import asyncio
import cozmo
import time
import threading

class Human_Listener(threading.Thread):

    def __init__(self,
                 game_robot,
                 human_cube,
                 tap_game):
        threading.Thread.__init__(self)
        self.player_cube  = human_cube
        self.robot = game_robot
        self.game=tap_game
        self.game_on = False

    def run(self):
        # Parallel thread for listening to human tapping on their cube
        player_cube_id = self.player_cube.object_id
        while self.game_on:
            try:
                # If the game is on then lister for player tap 
                tapped_event = self.robot.world.wait_for(cozmo.objects.EvtObjectTapped,timeout=4)
                if tapped_event and tapped_event.obj.object_id == player_cube_id:
                    # Register player tap with the game
                    if self.game.register_tap(player=True):
                       pass
            except asyncio.TimeoutError:
                pass