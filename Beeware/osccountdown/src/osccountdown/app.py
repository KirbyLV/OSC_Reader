"""
OSC Countdown clock to work with Millumin
"""
#region Setup

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import threading
import sys
import os
import json
from pythonosc import dispatcher
from pythonosc import osc_server

#endregion

class OSCCountdown(toga.App):
    def startup(self):
        #Create the main window
        main_box = toga.Box(style=Pack(direction=COLUMN))

        #Variables List
        self.ipAddr = ""
        self.port = ""
        self.msgAddr = ""
        self.clipNameAddr = ""
        self.oscMsg = ""
        self.oscNameMsg = ""
        self.oscArgs = ""
        self.osc_arg1 = ""
        self.osc_arg2 = ""
        self.countdown = ""
        self.arg1_display = ""
        self.arg2_display = ""
        self.clipName = ""
        self.zoomScale = 1.0
        self.isServer = False

        #Frame / Box Elements
        bgFrame = toga.Box(style=Pack(direction=COLUMN, padding=10))
        headerFrame = toga.Box(style=Pack(direction=COLUMN, padding=10))
        displayFrame = toga.Box(style=Pack(direction=COLUMN, padding=10))
        currentSettingsFrame = toga.Box(style=Pack(direction=ROW, padding=10))
        ipFrame = toga.Box(style=Pack(direction=ROW, padding=10))
        portFrame = toga.Box(style=Pack(direction=ROW, padding=10))
        msgFrame = toga.Box(style=Pack(direction=ROW, padding=10))
        footerFrame = toga.Box(style=Pack(direction=COLUMN, padding=10))
        scalerFrame = toga.Box(style=Pack(direction=COLUMN, padding=10))

        #Pack frames into main layout
        main_box.add(bgFrame)
        bgFrame.add(headerFrame)
        bgFrame.add(displayFrame)
        bgFrame.add(currentSettingsFrame)
        currentSettingsFrame.add(ipFrame)
        currentSettingsFrame.add(portFrame)
        currentSettingsFrame.add(msgFrame)
        bgFrame.add(footerFrame)
        main_box.add(scalerFrame)

        #Set content of the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        headerLabel = toga.Label("OSC Countdown", style=Pack(padding=(0, 5)))
        headerFrame.add(headerLabel)

        clipNameLabel = toga.Label(self.clipName, style=Pack(padding=(0,0)))
        displayFrame.add(clipNameLabel)

        label_arg1 = toga.Label(self.arg1_display, style=Pack)

    def handle_osc_message(self, addr, arg1, arg2):
        self.oscMsg = addr
        self.osc_arg1 = str(arg1)
        self.osc_arg2 = str(arg2)
        try:
            arg1_rounded = round(float(self.osc_arg1.strip()), 1)
            arg2_rounded = round(float(self.osc_arg2.strip()), 1)
        except ValueError:
            arg1_rounded = "NaN"
            arg2_rounded = "NaN"
        self.arg1_display = f"Current Clip Time: {arg1_rounded}"
        self.arg2_display = f"Clip Length: {arg2_rounded}"

        try:
            clipTime = float(self.osc_arg2.strip())
            currentTime = float(self.osc_arg1.strip())
            countdownTime = round(clipTime - currentTime, 1)
            self.countdown = countdownTime
        except ValueError:
            self.countdown = "Args could not be converted to floats"
    
    def handle_osc_name(self,addr, *args):
        self.oscNameMsg = addr
        self.clipName = str(args[1])

    def run_osc_server(self, ip, port, msg_addr1, msg_addr2):
        disp = dispatcher.Dispatcher()
        disp.map(msg_addr1, self.handle_osc_message)
        disp.map(msg_addr2, self.handle_osc_name)
        server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
        print(f"Serving on {server.server_address}")
        server.serve_forever()

    def start_server(self):
        if not self.isServer:
            self.isServer = True
            self.server_thread = threading.Thread(target=self.run_osc_server, daemon=True)
            self.server_thread.start()

    def stop_osc_server(self):
        if server:
            print("Stopping the server...")
            server.shutdown()
            server.server_close()
            server = None
            self.isServer = False

    def reload_server(self):
        self.stop_osc_server()
        self.isServer = False
        self.oscServerThread()
        self.isServer = True
    
    def retrieve_settings(self):
        data = open('localSettings.json')
        settings = json.load(data)
        data.close()
        try:
            self.ipAddr = settings['LOCAL_IPADDRESS']
            self.port = settings['LOCAL_PORT']
            self.msgAddr = settings['CLOCKINDEXADDRESS']
            self.clipNameAddr = settings['CLIPINDEXADDRESS']
        except Exception as e:
            print("Cannot Load Existing Settins.", e)
            self.main_window.error_dialog("Cannot Load Existing Settings", e)
        if (
            len(self.ipAddr) != 0 and
            len(self.port) != 0
        ):
            print("All good")
        else:
            self.main_window.error_dialog("Incomplete Values", "Not all required settings are present")

    def update_status_indicator(self):
        if self.isServer:
            #Configure Indicator State to Green
        else:
            #configure indicator status to red


def main():
    return OSCCountdown()
