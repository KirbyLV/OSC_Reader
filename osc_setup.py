import tkinter
import customtkinter
import json
import socket
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def open_setup_window():
    #region window setup
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme(resource_path("TrojanBlue.json"))

    setupWindow = customtkinter.CTkToplevel()
    setupWindow.minsize(width=540, height=300)
    setupWindow.title("OSC Setup")

    setupHeaderFrame = customtkinter.CTkFrame(master=setupWindow)
    setupHeaderFrame.pack(padx = 20, pady = 20, anchor = "n")

    settingsFrame = customtkinter.CTkFrame(master=setupWindow)
    settingsFrame.pack(padx = 0, pady = 20, anchor = "n")

    footerFrame = customtkinter.CTkFrame(master=setupWindow)
    footerFrame.pack(padx = 20, pady = 20, anchor = "n")

    #endregion
    #region Vars + Functions

    localIpAddr = tkinter.StringVar(setupWindow)
    localPort = tkinter.StringVar()
    msgAddr = tkinter.StringVar()
    clipAddr = tkinter.StringVar()
    clipIndex = tkinter.StringVar(setupWindow)

    def getLocalIPs():
        hostName = socket.gethostname()
        localIPs = socket.gethostbyname_ex(hostName)[2]
        return localIPs

    ipList = getLocalIPs()

    #JSON Data structure
    defaultSettings = data = '''{
        "LOCAL_IPADDRESS": null,
        "LOCAL_PORT": null,
        "MSGADDRESS": null,
        "CLIPADDRESS": null,
        "CLIPINDEX": null,
        "CLIPINDEXADDRESS": null,
        "CLOCKINDEXADDRESS": null
        }
        '''

    settings = json.loads(defaultSettings)
    settingsPath = resource_path('localSettings.json')

    def saveVariables():
        settings['LOCAL_IPADDRESS'] = localIpAddr.get().strip()
        settings['LOCAL_PORT'] = localPort.get().strip()
        settings['MSGADDRESS'] = msgAddr.get().strip()
        settings['CLIPADDRESS'] = clipAddr.get().strip()
        settings['CLIPINDEX'] = clipIndex.get().strip()
        clipIndexAddress = f"/millumin/index:{clipIndex.get()}/mediaStarted"
        settings['CLIPINDEXADDRESS'] = clipIndexAddress
        clockIndexAddress = f"/millumin/index:{clipIndex.get()}/media/time"
        settings['CLOCKINDEXADDRESS'] = clockIndexAddress
        final = open(settingsPath, 'w')
        final.write(json.dumps(settings))
        final.close()
        
        return settings
    
    def loadExstingData():
        f = open(settingsPath)
        existingData = json.load(f)
        f.close()
        try:
            localIpAddr.set(existingData['LOCAL_IPADDRESS'])
            localPort.set(existingData['LOCAL_PORT'])
            msgAddr.set(existingData['CLOCKINDEXADDRESS'])
            clipAddr.set(existingData['CLIPADDRESS'])
            clipIndex.set(existingData['CLIPINDEX'])
        except Exception as e:
            print("Cannot load existing settings.", e)

    #endregion
    #region on screen elements

    setupHeaderLabel = customtkinter.CTkLabel(setupHeaderFrame, text="OSC Setup", font=('Arial', 25))
    setupHeaderLabel.pack()

    localIpLabel = customtkinter.CTkLabel(settingsFrame, text="Local IP Address:", padx = 10, pady = 10)
    localPortLabel = customtkinter.CTkLabel(settingsFrame, text="Local Port:", padx = 10, pady = 10)
    #msgAddrLabel = customtkinter.CTkLabel(settingsFrame, text="OSC Clock Address:", padx = 10, pady = 10)
    clipAddrLabel = customtkinter.CTkLabel(settingsFrame, text="OSC Clip Name Address: ", padx = 10, pady = 10)

    localIpLabel.grid(row = 0, column = 0, sticky = "E")
    localPortLabel.grid(row = 1, column = 0, sticky = "E")
    #msgAddrLabel.grid(row = 2, column = 0, sticky = "E")
    clipAddrLabel.grid(row=3, column=0, sticky="E")

    localIpAddr.set(ipList[0])
    ipDropdown = customtkinter.CTkOptionMenu(settingsFrame, variable=localIpAddr, values=ipList)
    ipDropdown.grid(row = 0, column = 1, sticky = "W")

    localPortEntry = customtkinter.CTkEntry(settingsFrame, width=200, textvariable=localPort)
    localPortEntry.grid(row = 1, column = 1, sticky = "W")

    #msgAddrEntry = customtkinter.CTkEntry(settingsFrame, placeholder_text="/message/address/", width=300, textvariable=msgAddr)
    #msgAddrEntry.grid(row = 2, column = 1, sticky = "W")

    clipIndexDropdown = customtkinter.CTkOptionMenu(settingsFrame, variable=clipIndex, values=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    clipIndexDropdown.grid(row=3, column=1, sticky="W")

    #clipAddrEntry = customtkinter.CTkEntry(settingsFrame, placeholder_text="/message/address/", width=300, textvariable=clipAddr)
    #clipAddrEntry.grid( row = 3, column = 1, sticky= "W")

    saveButton = customtkinter.CTkButton(footerFrame, width=200, height=50, corner_radius=20, text="Save Configuration", command=saveVariables)
    saveButton.pack()

    loadExistingButton = customtkinter.CTkButton(footerFrame, width=150, height=20, corner_radius=10, text="Load Existing Data", command=loadExstingData)
    loadExistingButton.pack()

    ##setupWindow.mainloop()

if __name__ == "__main__":
    open_setup_window()