# OT-2 Wireless Controller calibration

Calibrating the robots may be a painful process using the controls in the app, specially if the computer controlling the robot is not located next to it or if you need to put your head inside the robot to check the location of the tip.

We have been using a video game wireless controller to make our lives easier when calibrating. In particular, we use the Nintendo Switch JoyCon controller because it can be operated with one hand, it is really small, has a wristband to avoid falling from the hand, and connects via common bluetooth with any device.

![miguel_joycon_calibrating.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/miguel_joycon_calibrating.jpg?raw=true)

This guide may be use to map any other controller to the keyboard to use it in the calibration of the robots, but the connection process may be different.

## Steps

1) Connect the controller to the computer. In our case, we just needed to open the bluetooth menu of the computer, activate bluetooth and bluetooth devices auto discovery and press the reset button on the controller. Then, it appears on the menu and you can connect ti clicking on it with the mouse.

2) Use a key mapper software to map controller buttons to single keyboard keystrokes. We use controllermate in macOS and joytokey in Windows, but any one should do the trick.

3) Create a profile to map the following keystrokes to the controller button you like the most:
- arrow UP
- arrow DOWN
- arrow LEFT
- arrow RIGHT
- SHIFT
- -
- +

![miguel_joycon_profile.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/miguel_joycon_profile.jpg?raw=true)

4) Test the controller to verify the input is correct

5) Connect the controller and turn on the keybinding software with the right profile whenever you want to calibrate your robot.
