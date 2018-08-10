#!/usr/bin/env python3

try:
    import os
    import sqlite3
    import tkinter as tk
    from tkinter import ttk
    import UpdateDB
except Exception as err:
    print("Error: " + str(err))
    exit(1)

LARGE_FONT = ("Verdana", 14)

root = None

class SearchTool:
    def __init__(self, master):
        self.master = master
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.frame = tk.Frame(self.master)

        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=0)
        self.frame.grid_rowconfigure(4, weight=0)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_columnconfigure(4, weight=1)
        self.frame.grid_columnconfigure(5, weight=0)

        self.title = ttk.Label(self.frame, text="FSearch", font=LARGE_FONT)
        self.title.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

        self.SearchString = tk.StringVar()
        self.search = ttk.Entry(self.frame, textvariable=self.SearchString)
        self.search.bind("<Return>", self.SearchFiles)
        self.search.bind("<Control-c>", self.Copy)
        self.search.bind("<Control-a>", self.SelectAll)
        self.search.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        self.search_button = ttk.Button(self.frame, text="Search", command=lambda:self.SearchFiles(self))
        self.search_button.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky="ew")

        self.txt = tk.Text(self.frame, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 10), state="disabled", wrap="none")
        self.txt.bind("<ButtonRelease-3>", self.PopupMenu)
        self.txt.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=2, pady=2)

        scrollb = ttk.Scrollbar(self.frame, command=self.txt.yview)
        scrollb.grid(row=2, column=5, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

        scrollb2 = ttk.Scrollbar(self.frame, command=self.txt.xview, orient="horizontal")
        scrollb2.grid(row=3, column=0, columnspan=5, sticky='ew')
        self.txt['xscrollcommand'] = scrollb2.set

        self.updatedb = ttk.Button(self.frame, text="Update database", command=lambda: self.Update(self))
        self.updatedb.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.quit = ttk.Button(self.frame, text="Quit", command=lambda: self.master.destroy())
        self.quit.grid(row=4, column=4, columnspan=3, padx=5, pady=5, sticky="ew")

        self.frame.grid(row=0, column=0, sticky="nsew")

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def SearchFiles(self, event):
        self.txt.config(font=("consolas", 10), state="normal")
        self.txt.delete(1.0, "end")
        if len(self.SearchString.get()) == 0:
            self.txt.insert("end", "Please enter a search term")
            self.txt.config(font=("consolas", 10), state="disabled")
            return
        conn = sqlite3.connect('Files.db')
        cursor = conn.execute("SELECT count(path) FROM Files")
        for row in cursor:
            if row[0] == 0:
                self.txt.insert("end", "Please update the database before searching.")
                self.txt.config(font=("consolas", 10), state="disabled")
                return
        cursor = conn.execute("SELECT count(path) FROM Files WHERE path LIKE \"%{}%\"".format(self.SearchString.get()))
        for row in cursor:
            if row[0] == 0:
                self.txt.insert("end", "No results found")
                self.txt.config(font=("consolas", 10), state="disabled")
                return

        cursor = conn.execute("SELECT path FROM Files WHERE path LIKE \"%{}%\"".format(self.SearchString.get()))
        for row in cursor:
            self.txt.insert("end", row[0] + "\n")
        self.txt.config(font=("consolas", 10), state="disabled")

    def Update(self, event):
        UpdateDB.main()
    
    def Copy(self, event):
        text = self.txt.get("sel.first", "sel.last")
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()

    def SelectAll(self, event):
        self.txt.tag_add("sel","1.0","end")

    def PopupMenu(self, event):
        popup = tk.Menu(self.txt, tearoff=0)
        popup.add_command(label="Copy", command=lambda: self.Copy(None))
        popup.add_command(label="Select all", command=lambda: self.SelectAll(None))
        popup.add_separator()
        popup.add_command(label="Update Database", command=lambda: self.Update(None))
        popup.add_separator()
        popup.add_command(label="Quit", command=lambda: self.master.destroy())
        popup.tk_popup(event.x_root, event.y_root, 0)
        popup.grab_release()


def main():
    global root
    root = tk.Tk()
    root.title("FSearch")
    style = ttk.Style()
    style.theme_use("clam")
    app = SearchTool(root)
    root.mainloop()

if __name__ == '__main__':
    main()
