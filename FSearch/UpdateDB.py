#!/usr/bin/env python3

'''
        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, August 10

 Copyright (C) 2018 Tovi Jaeschke (jaeschke@tuta.io)

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.
'''

try:
    import sys
    import os
    import threading
    import tkinter as tk
    import sqlite3
    from tkinter import ttk
except Exception as err:
    print("Error: " + str(err))

LARGE_FONT = ("Verdana", 14)
PATH_SPLIT = "/"
app = None

if sys.platform == "win32":
    PATH_SPLIT = "\\"

def UpdateDB():
    global app
    try:
        conn = sqlite3.connect(os.path.join(PATH_SPLIT.join(os.path.realpath(__file__).split(PATH_SPLIT)[:-1]), 'Files.db'))

        conn.execute("DROP TABLE IF EXISTS Files")
        conn.execute("CREATE TABLE Files (path TEXT)")
        for directory, dirnames, filenames in os.walk(os.path.abspath(os.sep)):
            for fil in filenames:
                conn.execute("INSERT INTO Files (path) VALUES (\"{0}\")".format(os.path.join(directory, fil)))
        conn.commit()
        conn.close()
        app.title.configure(text="Finished updating database")
        app.quitButton.configure(text="Done")
        return
    except Exception as err:
        conn.close()
        app.title.configure(text="Error: " + str(err))
        app.quitButton.configure(text="Done")
        return


class UpdatingDatabase:
    def __init__(self, master):
        self.master = master
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        style = ttk.Style()
        style.theme_use("clam")

        self.frame = tk.Frame(self.master)

        self.title = ttk.Label(self.frame, text="Updating database, please wait...", font=LARGE_FONT)
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.quitButton = ttk.Button(self.frame, text = 'Cancel', width = 25, command = self.close_windows)
        self.quitButton.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.frame.grid(row=0, column=0, sticky="nsew")

    def close_windows(self):
        self.master.destroy()


def main():
    global app
    root = tk.Tk()
    root.title("FSearch")
    app = UpdatingDatabase(root)
    update_thread = threading.Thread(target=UpdateDB)
    update_thread.daemon = True
    update_thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()
