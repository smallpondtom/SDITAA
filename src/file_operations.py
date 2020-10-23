"""
 ___________   _________     _____________   ______________    ______            ______
|     ______| |   ___   >\  |_____   _____| |_____    _____|  /< __ >\          /> __ <\
|    |______  |  |   \   >\      |   |           |    |      /> |__| <\        /< |__| >\
|_______    | |  |    |  >|      |   |           |    |     /< ______ >\      /> ______ <\
 ______|    | |  |___/   >/  ____|   |____       |    |    /> |      | <\    /< |      | >\
|___________| |_________>/  |_____________|      |____|   /<__|      |__>\  />__|      |__<\

"""

from tkinter import *
from tkinter import ttk, filedialog
#import io

class ReadFileApp:

    def __init__(self, master):

        self.label = ttk.Label(master, text = "How Read a File Content!")
        self.label.grid(row = 0, column = 0, columnspan = 2)

        ttk.Button(master, text = "Open File",
                   command = self.select_file).grid(row = 2, column = 0)

        ttk.Button(master, text = "Print the Content",
                   command = self.count_occurrences).grid(row = 2, column = 1)

    def select_file(self):
            filename = filedialog.askopenfilename(initialdir="C:\\")
            self.infile = open(filename, "r")
            #self.infile = io.TextIOWrapper(self.infile, encoding='utf8', newline='')
            print(self.infile.name)

    def count_occurrences(self):
        with open(self.infile.name, 'r') as myfile:
            txt_file=myfile.read().replace('\n', '')
        print(txt_file)

def main():
    main = Tk()
    app = ReadFileApp(main)
    main.mainloop()

if __name__ == "__main__": main()