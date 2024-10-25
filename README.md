# OSC Countdown
 OSC Countdown Readout, specifically for Millumin

<img width="500" alt="Screenshot 2024-10-25 at 10 17 09 AM" src="https://github.com/user-attachments/assets/dd6e1c79-2d80-4741-b914-d47fadeb2ca5">

## Window Layout
The top section of the app will display with clip name passed from Millumin, the current clip time and clip length, and will handle the math to give a "time reamining" value in seconds.

The middle section of the app will display the current settings that are loaded, including the local IP and port on which to listen for OSC messages, and the OSC message to watch for. 

The lower section contains the buttons to setup this information, and start and stop the OSC server.

At the bottom of the screen, there is a "Sclae Display Data" slider to make the values larger to be displayed in readable sizes by those who wish to see it.

## Setup
Begin by clickign the "Setup" button and navigating to the new window that opens.

<img width="400" alt="Screenshot 2024-10-25 at 10 20 48 AM" src="https://github.com/user-attachments/assets/a2a04e70-d247-4455-9dff-03cf68b57c53">

Use the dropdown under "Local IP Address" to select the NIC on your current computer on which to listen for OSC messages.
Type in the port to listen to, and seelct the "OSC Clip Address" corresponding tot he Millumin track you plan to listen to.

Millumin will output data about the clips in a track index format, so the top track would be index:1, the second would be index:2, etc.

You can click on "Load Existing Data" to prefill the fields with the previously used settings. Change whatever settigns you need and click "Save Configuration". You can now close this setup window.

Back in the main app window, click on "Load Settings" and you should see the settings populate in the fields above the buttons. Click on "Run PSC Server" and the app will now be listening for Millumin OSC messages. Whenever settigns are changed, you must re-load the settings, and reload, or stop and start, the server. The indicator box should be green when the server is running, and red when idle.

## Millumin Setup
In Millumin, navigate to "Interactions" - Click on "Manage Devices" - Click on the "OSC" tab.
Check the box for "API feedback" and "enabled" and in the "to machine" field, type in the IP and port of the computer running OSC Reader, and the value selected in the setup screen

<img width="350" alt="Screenshot 2024-10-25 at 10 24 45 AM" src="https://github.com/user-attachments/assets/e0093b0a-6d82-4961-8138-038a7edbc38e">
