#region setup

import threading
import subprocess
import sys
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

#endregion
#region Window Setup

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("Oceanix.json")

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
currentSettingsFrame.pack(padx=0, pady=20, anchor = "n")

ipFrame = customtkinter.CTkFrame(master=currentSettingsFrame)
ipFrame.grid(row=0, column=0)

portFrame = customtkinter.CTkFrame(master=currentSettingsFrame)
portFrame.grid(row=0, column=1)

msgFrame = customtkinter.CTkFrame(master=currentSettingsFrame)
msgFrame.grid(row=0, column=2)

footerFrame = customtkinter.CTkFrame(master=bgFrame)
footerFrame.pack(padx = 20, pady = 20, anchor = "n")

#endregion
#region Variables and Fucntions

ipAddr = tkinter.StringVar()
port = tkinter.StringVar()
msgAddr = tkinter.StringVar()
oscMsg = tkinter.StringVar()
oscArgs = tkinter.StringVar()
osc_arg1 = tkinter.StringVar()
osc_arg2 = tkinter.StringVar()
countdown = tkinter.StringVar()
arg1_display = tkinter.StringVar()
arg2_display = tkinter.StringVar()
clipName = tkinter.StringVar()

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
        countdown.set(str(countdownTime))
    except ValueError:
        countdown.set("Args could not be converted to floats")

def run_osc_server(ip, port, msg_addr):
    disp = dispatcher.Dispatcher()
    disp.map(msg_addr, handle_osc_message)
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Serving on {server.server_address}")
    server.serve_forever()

def retrieve_settings():
    data = open('localSettings.json')
    settings = json.load(data)
    data.close()
    try:
        ipAddr.set(settings['LOCAL_IPADDRESS'])
        port.set(settings['LOCAL_PORT'])
        msgAddr.set(settings['MSGADDRESS'])
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
    msg = msgAddr.get()
    osc_thread = threading.Thread(target=run_osc_server, args=(ip, portNo, msg), daemon=True)
    osc_thread.start()

#endregion
#region on screen elements

headerLabel = customtkinter.CTkLabel(headerFrame, text="OSC Reader")
headerLabel.pack()

messageLabel = customtkinter.CTkLabel(displayFrame, textvariable=oscMsg)
messageLabel.grid(row=0, column=0, sticky = "w")

label_arg1 = customtkinter.CTkLabel(displayFrame, textvariable=arg1_display)
label_arg1.grid(row=2, column=0, sticky = "w")

label_arg2 = customtkinter.CTkLabel(displayFrame, textvariable=arg2_display)
label_arg2.grid(row=2, column=1, sticky = "w")

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
#endregion

root.mainloop()