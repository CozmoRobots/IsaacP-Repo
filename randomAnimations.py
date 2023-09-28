import cozmo
import random

def cozmo_program(robot: cozmo.robot.Robot):
 all_animations = robot.anim_triggers
 random.shuffle(all_animations)

 triggers = 8
 chosen_triggers = all_animations[:triggers]
 print('Playing {} random animations'.format(triggers))

 for trigger in chosen_triggers:
  print('Playing {}'.format(trigger.name))
  robot.play_anim_trigger(trigger).wait_for_completed()
cozmo.run_program(cozmo_program)
