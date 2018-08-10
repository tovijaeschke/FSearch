#!/usr/bin/env python3

try:
    import os
    import threading
    import tkinter as tk
    import sqlite3
    from tkinter import ttk
except Exception as err:
    print("Error: " + str(err))

LARGE_FONT = ("Verdana", 14)

app = None

def UpdateDB():
    global app
    try:
        conn = sqlite3.connect('Files.db')
        conn.execute("DROP TABLE IF EXISTS Files")
        conn.execute("CREATE TABLE Files (path TEXT)")
        for directory, dirnames, filenames in os.walk(os.path.abspath(os.sep)):
            for fil in filenames:
                conn.execute("INSERT INTO Files (path) VALUES (\"{0}\")".format(os.path.join(directory, fil)))
        conn.commit()
        conn.close()
        app.title.configure(text="Finished updating database")
        app.quitButton.configure(text="Done")
    except Exception as err:
        conn.close()
        app.title.configure(text="Error: " + str(err))
        app.quitButton.configure(text="Done")


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
