# Calibration

Check here the [official guide](https://support.opentrons.com/en/articles/3499692-how-does-calibration-work-on-the-ot-2)

Remember that not all tips are perfectly made, and some, specially the longest ones, can be quite curved. It is always better to calibrate with the shortest tip available, but in any case you should keep these thins in mind:

- As longer tips may not be completely straight, it really does not matter if the tip is perfectly centered on the well. What you have to make sure of is that the tip is just inside the well, at the height where if you level your eye with the labware top you do not see the edge of the tip.

- You may need to calibrate several times the same labware or tiprack in different slots for the same protocol. Do not skip this calibration after the firs one si done, as you may find not all of them keep the same calibration by default.

- When calibrating a waste container, or a reservoir, or anything with big wells, it may be interesting calibrating the tip not in the center of the well but over a different region. This allows you to aspirate and dispense in certain locations depending on the calibration, not the coding of the protocol, so they can be adjusted by people who does not code.

- You can calibrate aiming for he bottom of the well instead of the top. This is useful if you really need to reach the bottom of the labware, but be aware that some wells may again not be perfect and have little different heights or shapes, which could cause the tip to hit bottom during the execution and not aspirate properly. Check the robot main menu inside the app.

# Check calibration

Once you have finished calibrating, or before starting using a protocol in a robot for the first time of the day and you are not sure if it is already correctly calibrated, or if you see some issues with the protocol execution and you want to make sure it is not a problem of the calibration, we provide a range of scripts for calibration check.

You can find them in the folder [calibration_check](ttps://github.com/BU-ISCIII/opentrons_covid19/blob/develop/calibration_check) and there is one for each protocol.

To use them, just load the script corresponding the protocol you want to use as if it was the protocol, set the labware, and run. The script will move the pipettes to all the positions in required in the protocol, attach the needed tips and aspirate and dispense water in the first and last well of each labware. Between each action, the robot will stop and ask the operator if the action was executed right, and if there is any problem with the calibration the user will be able to easily locate it.

# Useful tips for calibration

When calibrating, it is sometimes difficult to see where exactly the edge of the tip is, specially under bad light circumstances or when calibrating the deck.

We propose the following tips to make it an easier experience:

- Always make sure you have good lighting. If the internal led strips of your robot work, turn them on and that should be enough.

- Turn on the lights of the robot before starting the calibration process.

- Use a wireless connected laptop for calibration, as you can be closer to the robot and calibrate it without having to walk to the desktop computer between observations.

- Or, even better, [use a wireless controller for calibration](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/doc/S3/07_wireless_controller_calibration.md)

- If possible, calibrate always using a single channel p20. The shorter the tip is, the better the calibration. Avoid at all costs calibrating with a single channel p1000.

- If you have to calibrate with a p1000, use a 3D printed solution attached to the pipette instead of a tip to get better results.

- Be careful if you have to use a multichannel pipette to calibrate, as it will crash against the walls of the robot in certain positions. Avoid if possible.

# OT-2 Modifications recommended for tips used in calibration

From our experience, we propose some modifications you can use to improve your calibrating accuracy:

- Paint your tips edges with a red permanent marker, so it is easier to see them when calibrating.

![calibrating_painted_tip.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/calibrating_painted_tip.jpg?raw=true)

- Use a rigid 3D printed tip for calibrating with longer tips as the 1000ul ones.

(We will provide link to the printable file as soon as it is tested) 
