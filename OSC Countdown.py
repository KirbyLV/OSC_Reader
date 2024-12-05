#region setup

import threading
import subprocess
import sys
import os
import json
import tkinter.messagebox

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", '-r', package])
package = 'requirements.txt'
install(package)

import tkinter
import customtkinter

from pythonosc import dispatcher
from pythonosc import osc_server

from osc_setup import open_setup_window

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#endregion
#region Window Setup

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme(resource_path("Oceanix.json"))

root = customtkinter.CTk()
root.minsize(width=720, height=540)
root.title("OSC Reader")

bgFrame = customtkinter.CTkFrame(master=root)
bgFrame.pack(expand=True)

headerFrame = customtkinter.CTkFrame(master=bgFrame)
headerFrame.pack(padx = 20, pady = 20, anchor = "n")

displayFrame = customtkinter.CTkFrame(master=bgFrame)
displayFrame.pack(padx = 0, pady = 20, anchor = "n")

currentSettingsFrame = customtkinter.CTkFrame(master=bgFrame)
currentSettingsFrame.pack(padx=0, pady=20, anchor = "n", fill="both", expand=True)

ipFrame = customtkinter.CTkFrame(master=currentSettingsFrame)
ipFrame.grid(row=0, column=0)

portFrame = customtkinter.CTkFrame(master=currentSettingsFrame)
portFrame.grid(row=0, column=1)

msgFrame = customtkinter.CTkFrame(master=currentSettingsFrame)
msgFrame.grid(row=0, column=2)

footerFrame = customtkinter.CTkFrame(master=bgFrame)
footerFrame.pack(padx = 20, pady = 20, anchor = "n")

scalerFrame = customtkinter.CTkFrame(master=root)
scalerFrame.pack(anchor="s")

#endregion
#region Variables and Fucntions

ipAddr = tkinter.StringVar()
port = tkinter.StringVar()
msgAddr = tkinter.StringVar()
clipNameAddr = tkinter.StringVar()
oscMsg = tkinter.StringVar()
oscNameMsg = tkinter.StringVar()
oscArgs = tkinter.StringVar()
osc_arg1 = tkinter.StringVar()
osc_arg2 = tkinter.StringVar()
countdown = tkinter.StringVar()
arg1_display = tkinter.StringVar()
arg2_display = tkinter.StringVar()
clipName = tkinter.StringVar()
zoomScale = tkinter.DoubleVar()
isServer = tkinter.BooleanVar()

isServer.set(False)
server = None
server_thread = None

def handle_osc_message(addr, arg1, arg2):
    oscMsg.set(addr)
    osc_arg1.set(arg1)
    osc_arg2.set(arg2)
    try:
        arg1_rounded = round(float(osc_arg1.get().strip()), 1)
        arg2_rounded = round(float(osc_arg2.get().strip()), 1)
    except ValueError:
        arg1_rounded = "NaN"
        arg2_rounded = "NaN"
    arg1_display.set(f"Current Clip Time: {arg1_rounded}")
    arg2_display.set(f"Clip Length: {arg2_rounded}")

    try:
        clipTime = float(osc_arg2.get().strip())
        currentTime = float(osc_arg1.get().strip())
        countdownTime = round(clipTime - currentTime, 1)
        countdown.set(str(seconds_to_minutes(countdownTime)))
    except ValueError:
        countdown.set("Args could not be converted to floats")

def handle_osc_name(addr, *args):
    oscNameMsg.set(addr)
    clipName.set(args[1])

def run_osc_server(ip, port, msg_addr1, msg_addr2):
    global server, server_thread
    disp = dispatcher.Dispatcher()
    disp.map(msg_addr1, handle_osc_message)
    disp.map(msg_addr2, handle_osc_name)
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Serving on {server.server_address}")
    server.serve_forever()
    reloadServer.configure(state ='normal')
    stopServer.configure(state='normal')

def stop_osc_server():
    global server
    if server:
        print("Stopping the server...")
        server.shutdown()
        server.server_close()
        server = None
        isServer.set(False)

def reload_server():
    stop_osc_server()
    isServer.set(False)
    oscServerThread()
    isServer.set(True)


def retrieve_settings():
    data = open(resource_path('localSettings.json'))
    settings = json.load(data)
    data.close()
    try:
        ipAddr.set(settings['LOCAL_IPADDRESS'])
        port.set(settings['LOCAL_PORT'])
        msgAddr.set(settings['CLOCKINDEXADDRESS'])
        clipNameAddr.set(settings['CLIPINDEXADDRESS'])
    except Exception as e:
        print("Cannot Load Existing Settings.", e)
        tkinter.messagebox.showwarning(title="No Existing Settings", message="No Existing Settings", default="Ok")
    if (
        len(ipAddr.get()) != 0 and
        len(port.get()) != 0
        ):
        runApp.configure(state='normal')
    else:
        tkinter.messagebox.showwarning(title="Incomplete Values", message="Not all required settings are present", default="ok")
        print("Missing some variables")

def oscServerThread():
    ip = ipAddr.get()
    portNo = int(port.get())
    msgClock = msgAddr.get()
    msgName = clipNameAddr.get()
    isServer.set(True)
    osc_thread = threading.Thread(target=run_osc_server, args=(ip, portNo, msgClock, msgName), daemon=True)
    osc_thread.start()

def update_status_indicator():
    if isServer.get():
        isRunningStatus.configure(bg_color="green")
    else:
        isRunningStatus.configure(bg_color="red")
    root.after(100, update_status_indicator)

def windowZoom(zoomValue):
    zoomScale.set(zoomValue)
    customtkinter.set_widget_scaling(zoomValue)

def seconds_to_minutes(time_str):
    try:
        total_seconds = float(time_str)
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:.2f}"
    except ValueError:
            return "Invalid Input"

#endregion
#region on screen elements

headerLabel = customtkinter.CTkLabel(headerFrame, text="OSC Reader")
headerLabel.pack()

clipNameLabel = customtkinter.CTkLabel(displayFrame, textvariable=clipName, font=('Arial', 24))
clipNameLabel.grid(row=1, column=0, columnspan=2)

label_arg1 = customtkinter.CTkLabel(displayFrame, textvariable=arg1_display)
label_arg1.grid(row=2, column=0, padx = 10)

label_arg2 = customtkinter.CTkLabel(displayFrame, textvariable=arg2_display)
label_arg2.grid(row=2, column=1, padx = 10)

label_countdown = customtkinter.CTkLabel(displayFrame, text="Time Remaining: ")
label_countdown.grid(row=3, column=0, sticky="e")

value_countdown = customtkinter.CTkLabel(displayFrame, textvariable=countdown, font=('Arial', 50))
value_countdown.grid(row=3, column=1, sticky = "w")

#current settings display
currentIpLabel = customtkinter.CTkLabel(ipFrame, text="Local IP:")
currentIpLabel.grid(row=0, column=0)

currentIPValue = customtkinter.CTkLabel(ipFrame, textvariable=ipAddr, padx=10)
currentIPValue.grid(row=0, column=1)

currentPortLabel = customtkinter.CTkLabel(portFrame, text="Port:")
currentPortLabel.grid(row=0, column=0)

currentPortValue = customtkinter.CTkLabel(portFrame, textvariable=port, padx=10)
currentPortValue.grid(row=0, column=1)

currentMsgLabel = customtkinter.CTkLabel(msgFrame, text="Current OSC Msg:")
currentMsgLabel.grid(row=0, column=0)

currentMsgValue = customtkinter.CTkLabel(msgFrame, textvariable=msgAddr, padx=10)
currentMsgValue.grid(row=0, column=1)

#execute buttons
openSettings = customtkinter.CTkButton(footerFrame, width=200, height=50, corner_radius=20, text="Setup", command=open_setup_window)
openSettings.grid(row=0, column=0)

loadSettings = customtkinter.CTkButton(footerFrame, width=200, height=50, corner_radius=20, text="Load Settings", command=retrieve_settings)
loadSettings.grid(row=0, column=1)

runApp = customtkinter.CTkButton(footerFrame, width=200, height=50, corner_radius=20, text="Run OSC Server", command=oscServerThread, state='disabled')
runApp.grid(row=0, column=2)

reloadServer = customtkinter.CTkButton(footerFrame, width=200, height=50, corner_radius=20, text="Reload Server", command=reload_server)
reloadServer.grid(row=1, column=1)

stopServer = customtkinter.CTkButton(footerFrame, width=200, height=50, corner_radius=20, text="Stop Server", command=stop_osc_server)
stopServer.grid(row=1, column=2)

isRunningLabel = customtkinter.CTkLabel(footerFrame, text="Server Runnimg:")
isRunningLabel.grid(row=2, column=1, sticky="e")

isRunningStatus = customtkinter.CTkLabel(footerFrame, text="", width=50, height=50, corner_radius=25)
isRunningStatus.grid(row=2, column=2, sticky="w")

#zoom slider
zoomLabel = customtkinter.CTkLabel(scalerFrame, text="Scale Display Data:")
zoomLabel.grid(row=0, column=0)

zoomSlider = customtkinter.CTkSlider(master=scalerFrame, from_=1, to=3, command=windowZoom)
zoomSlider.grid(row=0, column=1)

#endregion

update_status_indicator()

root.mainloop()