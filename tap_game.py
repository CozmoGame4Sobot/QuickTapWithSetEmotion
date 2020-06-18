
import asyncio
import copy
import cozmo
from datetime import datetime
import getopt
import logging
import os
import sys 
import time
from cozmo_player import CozmoPlayerActions, cozmo_tap_game


def add_file_logger(log_path, cozmo_action):
    ''' setup file logger'''
    if cozmo_action.sad_not_angry:
        filename="sad_tap_%s.log" % datetime.now().strftime("%H%M%S_%d%m%Y")
    else:
        filename="angry_tap_%s.log" % datetime.now().strftime("%H%M%S_%d%m%Y")
    filePath = os.path.join(log_path, filename)
    
    # create error file handler and set level to info
    handler = logging.FileHandler(os.path.join(log_path, filename),"w", encoding=None, delay="true")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    
    # add file handler to cozmo
    cozmo.logger.addHandler(handler)
    
def handle_selection(argv, cozmo_action):    
    help_string = 'tap_game.py -h (--help) [-s (--sad), -a (--angry)] [-e (--easy), -d (--difficult) -t= (--timed=)] [-l (--logPath) -i(--ignoreLogging)]   < Note the log options must be the last option>'
    log_path = None
    
    try:
       opts, args = getopt.getopt(argv,"hsaedt:l:i",["help","sad", "angry", "easy", "difficult", "timed", "logPath", "ignoreLogging"])
    except getopt.GetoptError:
       print(help_string)
       sys.exit(2)
       
    if not opts[-1][0] in ["--ignoreLogging", "-i"]:
        print("%s" % opts[-1][1])
        if opts[-1][0] in ["--logPath", "-l"]:
            log_path = opts[-1][1].strip('=')
        else:
            log_path = None
            log_path = os.path.join('./logs')
        
        if log_path and not os.path.isdir(log_path):
            print("Please create the log directory '%s' on your system." % log_path)
            print("If you do not want to log, run with the -i as the last option")
            print("If you want to log at an alternative location use -l=<log_path> as the last option")
            exit(0)       
            
    for opt, arg in opts:
        if opt in ("-h", "--help"):
           print("python tap_game.py -h (--help) [-s (--sad), -a (--angry)] [-e (--easy), -d (--difficult) -t= (--timed=)] [-l (--logPath) -i(--ignoreLogging)]\n"\
                 "Note the log options, if provided, must be the last option.By default it tries to log to \"CozmoTest/log\" in the root directory\n\n"\
                 "-h (--help)           Show the help string\n\n"\
                 "Emotion arguments:\n"\
                 "-s (--sad)         Cozmo reacts sadly to losing game\n"\
                 "                    e.g. python tap_game.py -s\n\n"\
                 "-a (--angry)       Cozmo reacts angrily to losing game\n"\
                 "                    e.g. python tap_game.py -z\n\n"\
                 "Game-ease arguments:\n"\
                 "-e (--easy)         Cozmo is easy to defeat\n"\
                 "                    e.g. python tap_game.py -e\n\n"\
                 "-d (--difficult)    Cozmo is hard to defeat\n"\
                 "                    e.g. python tap_game.py -d\n\n"\
                 "-t= (--timed=)      Cozmo's reaction time control in seconds\n"\
                 "                    For the following 2.5sec reaction time"
                 "                    e.g. python tap_game.py -t=2.5 \n\n"\
                 "Logging arguments:\n"\
                 "-l (--logPath)         Optional last argument to specify directory to log to.\n" \
                 "                    e.g. python tap_game.py -z -l \"E:/log\" \n\n"\
                 "-i(--ignoreLogging)     Optional last argument to ignore logging to file\n"\
                 "                    e.g. python tap_game.py -v -i")
           sys.exit()
        elif opt in ("-s", "--sad"):
           cozmo_action.set_game_lose_reaction(is_sad=True)
           
        elif opt in ("-a", "--angry"):
           cozmo_action.set_game_lose_reaction(is_sad=False)
           
        elif opt in ("-e", "--easy"):
           cozmo_action.set_reaction_time(set_time = 2.5)
           
        elif opt in ("-d", "--difficult"):
           cozmo_action.set_reaction_time(set_time = 0.75)
        elif opt in ("-t", "--timed"):
          
           if arg:
               try:                   
                   entered_time = float(arg.strip('='))
                   cozmo_action.set_reaction_time(set_time=entered_time)
               except ValueError:
                      print("Please enter a decimal number to indicate seconds delay in cozmo's reaction time")
                      exit(0)
           else:
               print("Please enter a decimal number to indicate seconds delay in cozmo's reaction time")
               exit(0)         
        elif opt in ("-i", "-l", "--ignoreLogging", "--logPath"):
           pass
        else:
           log_path = None
           print(help_string)
           return False
        
    #end for
    if log_path:
      add_file_logger(log_path, cozmo_action)
    return True
         
if __name__ == "__main__":
   if len(sys.argv) < 2:
       print('tap_game.py -h (--help) [-s (--sad), -a (--angry)] [-e (--easy), -d (--difficult) -t= (--timed=)] [-l (--logPath) -i(--ignoreLogging)]  < Note the log options, if provided, must be the last option>')
   else: 
       # Command is syntactically correct. Setup the Cozmo robot
       cozmo_action = CozmoPlayerActions()
       # Handle command line entried
       if handle_selection(sys.argv[1:], cozmo_action):
           # start the game
           cozmo.run_program(cozmo_tap_game)
       del cozmo_action
   exit(0)
    
   
    
