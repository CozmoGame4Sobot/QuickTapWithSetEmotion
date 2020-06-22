# QuickTap Game With Set Emotion
## Introduction
QuickTap is a game that is provided with the Cozmo app. We needed to use it for some HRI behaviour studies but wanted to control the emotions Cozmo displayed when it lost the final game.

In this code Cozmo will play one round of quick tap. The round here is defined as the quickest 5 points scorer. Whether Cozmo will act sad or angry can be manipulated from commandline.The game difficulty can also be specified from commandline.

Note that this program is written for Cozmo app 1.5. It may or maynot run with later apps and the animations and the animation names change between different versions of Cozmo app. So you will need to check if the animations used in this code are still available for you version of Cozmo and if they show the right emotion. We did not use the animation_group for evoking the animation which would have possibly made it version independent because that does not give us control over the emotion.

##Requirements

We used Python version 3.5.3 with the following packages 
numpy==1.16.4
Pillow==6.1.0
cozmoclad==1.5.0
cozmo==0.14.0

The cozmo sdk(s) are a match for version Cozmo app version 1.5 . They need to be installed in order provided so that a newer version of the packages don't get pulled in.

To setup your device and computer to run custom python code, see instruction from Anki here: http://cozmosdk.anki.com/docs/initial.html


## To run the game
Connect to Cozmo and run it in SDK mode

Then from commandline cd to the file where you have downloaded the files from this repository.

The commandline helps looks like this : 
tap_game.py -h (--help) [-s (--sad), -a (--angry)] [-e (--easy), -d (--difficult) -t= (--timed=)] [-l (--logPath) -i(--ignoreLogging)]  < Note the log options, if provided, must be the last option>



 -h -- help : will bring up the help line above
 ###  One of the following two options needed 
 -s -- sad: Cozmo will be sad when they lose the game
 
 -a --angry: Cozmo will be angry when they lose the game
 
 ### One of the following three options needed 
 -e --easy: It will be easy to win against Cozmo as Cozmo waits for longer making it slow
 
 -d -- difficult: It will be hard to win against Cozmo as Cozmo waits for shorter time making it very fast
 
 -t --time= Specifies how long to wait for in seconds explicitly
 
 ### The next two a related to logging
 -l --logPath: Expets full path to log directory
 
 -i --ignoreLogging: There will be no logs
 
 ## Animations used
 Listing all animation if someone needs to check that they exist and are valid for their groups
 ### sad animations : 
 * 'anim_speedtap_losegame_intensity02_01',
 * 'anim_fistbump_fail_01',
 * 'anim_keepaway_losegame_02',
 * 'anim_memorymatch_failgame_cozmo_03' 
 
 ### angry animations :
 * 'anim_speedtap_losegame_intensity03_01',
 * 'anim_memorymatch_failgame_cozmo_01',
 * 'anim_reacttocliff_stuckrightside_02',
 * 'anim_pyramid_reacttocube_frustrated_mid_01'
 
 ### happy animations :
 * 'anim_speedtap_winround_intensity01_01',
 * 'anim_speedtap_winround_intensity02_02',
 * 'anim_speedtap_winround_intensity02_01',
 * 'anim_speedtap_wingame_intensity02_01',
 * 'anim_speedtap_wingame_intensity02_02',
 * 'anim_speedtap_wingame_intensity03_01'
 
 ### wait animations:
 * 'anim_speedtap_wait_short',
 * 'anim_speedtap_wait_medium',
 * 'anim_speedtap_wait_medium_02',
 * 'anim_speedtap_wait_medium_03',
 * 'anim_speedtap_wait_long'
 
 ### other animations:
 - anim_speedtap_losehand_01
 - anim_speedtap_losehand_02
 - anim_speedtap_losehand_03
 - anim_speedtap_winhand_01
 - anim_speedtap_winhand_02
 - anim_speedtap_winhand_03
 - anim_speedtap_fakeout_01
