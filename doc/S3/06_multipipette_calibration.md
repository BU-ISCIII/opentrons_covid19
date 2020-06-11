# OT-2 Multipipette V2 calibration

Multipipettes can not be calibrated as single pipettes, as they also need to calibrate levelling of the 8 channels.

## Steps

1) Mount the multipipette following the instructions of the app, as you would do with a single pipette.

*Note:* You need your app and robot in version >3.16 to be able to attach multipipettes gen 2. If they do not appear as options in the attach pipette menu, make sure you have enabled the developer options in the app.

2) Once the pipette is successfully installed, turn off the robot.

3) With the robot turne off, now it is safe to manually move the arm of the robot without damaging the internal motors.

4) Place the calibration piece in one slot of the robot and move the arm above it.

![multipipette_calibration_block.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/multipipette_calibration_block.jpg?raw=true)

5) Slowly, pull down the pipette until it touches the calibration piece at the corresponding surface.

*Note:* There are two surfaces, each for one of the multipipette models. Make sure you are using the right one.

![multipipette_calibration_block_surfaces.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/multipipette_calibration_block_surfaces.jpg?raw=true)

6) Unscrew the lower screw of the pipette and loose the two top ones. Now you can adjust the pipette so all channels touch the calibration surface.

7) Carefully screw back the two top screws of the pipette and move the arm up and down to check if the calibration is correct. You can use a flashlight to check that all channels touch the surface again.

![multipipette_calibration_levelling.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/multipipette_calibration_levelling.jpg?raw=true)

*Note:* You do not need to screw the third screw. It usually causes the pipette to discalibrate again, and it works fine with only the two top screws.

8) Remove the calibration block from the deck and turn on the robot. The multipipette should be now successfully installed.
