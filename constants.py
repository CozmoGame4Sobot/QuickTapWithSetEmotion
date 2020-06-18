import cozmo
START_CUBE = 0
WIN_CUBE = 1
LOSE_CUBE = 2

DEAL_CHOICE = ["all_red", "no_match", "Match"]
GOOD_DEAL = 2 # The third hand in the deal_choice is the good hand

PLAYER_ID = 1
COZMO_ID = 2

RED_LIGHT = cozmo.lights.red_light
BLUE_LIGHT = cozmo.lights.blue_light
GREEN_LIGHT = cozmo.lights.green_light
YELLOW_LIGHT = cozmo.lights.Light(cozmo.lights.Color(rgb=(255, 255, 0)),
                                                        cozmo.lights.off)
PINK_LIGHT = cozmo.lights.Light(cozmo.lights.Color(rgb=(255, 0, 255)),
                                                        cozmo.lights.off)
SEA_LIGHT = cozmo.lights.Light(cozmo.lights.Color(rgb=(0, 255, 255)),
                                                        cozmo.lights.off)
PURPLE_LIGHT = cozmo.lights.Light(cozmo.lights.Color(rgb=(65,0,130)),
                                                        cozmo.lights.off)
                                  