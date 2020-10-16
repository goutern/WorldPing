import platform  # For getting the operating system name
from subprocess import Popen, PIPE  # For executing a shell command
import re
import operator
import tkinter as tk
from tkinter.ttk import Progressbar


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    time = re.compile('time=(.+?)ms')
    match = time.search(output.decode("utf-8"))
    seconds = 999
    if match is not None:
        seconds = int(match.group(1))
    return (seconds)


def getPing():
    worlds = []
    Lb.delete(0, tk.END)
    for x in range(1, 140):
        worlds.append([ping("world%s.runescape.com" % x), x])
        progress['value'] = (x * 0.72)
        r.update_idletasks()

    worlds.sort(key=operator.itemgetter(0))

    for x in range(1, 6):
        Lb.insert(x, ("World: " + str(worlds[x][1]) + " Ping: " + str(worlds[x][0])))
    Lb.pack(pady=8)


r = tk.Tk()
r.title('Get Ping')
r.geometry("300x200")

button = tk.Button(r, text='Get Pings', width=25, command=getPing)
button.pack(pady=8)
Lb = tk.Listbox(r)
progress = Progressbar(r, orient=tk.HORIZONTAL,
                       length=100, mode='determinate')
progress.pack()
r.mainloop()
