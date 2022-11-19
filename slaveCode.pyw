import socket
import time
import threading
import subprocess
import os
import win32api, win32con
try:
    import ctypes
except:
    subprocess.call("pip install ctypes", shell=False)
    import ctypes

PI = [49, 48, 46, 48, 46, 48, 46, 49, 50, 54]
IP = ''.join(map(chr, PI))
PORT = 5050
ADDR = (IP, PORT)

CONNECTED = False

client = None

def processCommand(cmd, args):
    if cmd == "lock":
        subprocess.call("Rundll32.exe user32.dll,LockWorkStation", shell=False)
        return "!READY"
    elif cmd == "restart":
        subprocess.call("shutdown -r -t 00", shell=False)
        return "!STOP"
    elif cmd == "shutdown":
        subprocess.call("shutdown -s -t 00", shell=False)
        return "!STOP"
    elif cmd == "!PING":
        sendTime = args[0]
        sendTime = float(sendTime)*100
        ping = int(time.time()*100 - sendTime)
        toSend = str(ping) + " " + str(time.time())
        return toSend
    elif cmd == "search":
        if args:
            searchTerm = "+".join(args)
            searchTerm = "https://www.google.com/search?q=" + searchTerm
            command = "start " + searchTerm
            os.system(command)
            return "!READY"
        else:
            return "!ARGS"
    elif cmd == "web":
        if args:
            website = args[0]
            command = "start " + website
            os.system(command)
            return "!READY"
        else:
            return "!ARGS"
    elif cmd == "say":
        if args and args[1]:
            dwldFolder = os.path.expanduser("~/Downloads")
            textFileName = args[0]
            textToSay = " ".join(args[1:])
            x = open(dwldFolder + "\\" + textFileName + ".txt", "w+")
            x.write(textToSay)
            x.close()
            os.system(dwldFolder + "\\" + textFileName + ".txt")
            return "!READY"
        else:
            return "!ARGS"
    elif cmd == "screen-off":
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)
        return "!READY"
    elif cmd == "screen-on":
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)
        x, y = (0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)
        return "!READY"
    elif cmd == "clear-dns":
        subprocess.call("ipconfig /flushdns", shell=False)
        return "!READY"
    else:
        print('[ERROR] Unknown command: ' + '"' + cmd + '"')
        return "!UNKNOWN"

def Receive():
    global CONNECTED
    global client
    while True:
        if CONNECTED == True:
            try:
                msgLength = client.recv(2048).decode("utf-8")
                msg = client.recv(int(msgLength)).decode("utf-8")
                if msg != "":
                    msgList = msg.split(" ")
                    cmd = msgList[0]
                    args = None
                    if msgList:
                        msgList.pop(0)
                        args = msgList
                    toSend = processCommand(cmd, args)
                    client.send(toSend.encode("utf-8"))
            except:
                print("[ERROR] Master disconnected / failed to listen for command.")
                CONNECTED = False
                checkConnection()
                break
        else:
            time.sleep(0.5)
            continue

def checkConnection():
    global CONNECTED
    global client
    while True:
        if CONNECTED == False:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(ADDR)
                CONNECTED = True
                print("[CLIENT] Successfully connected to master computer!")
                Receive()
                break
            except:
                CONNECTED = False
                print("[ERROR] Failed to connect. Retrying in 1 second...")
                time.sleep(1)
                continue

checkConnectionThread = threading.Thread(target=checkConnection)
checkConnectionThread.run()
