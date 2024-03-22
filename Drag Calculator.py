##--------------------------------Libraries--------------------------------##
import tkinter as tk
import tkinter.ttk as ttk
import math
import matplotlib.pyplot as plt
import json
import glob
from pathlib import Path
import os
##--------------------------------Main GUI--------------------------------##
class objtosave():
    def __init__(self,givenname,givencoefficient,givenarea):
        self.name = givenname
        self.coefficient = givencoefficient
        self.area = givenarea
class App():
    def __init__(self,master):
        
        self.startupwin = master
        self.titlelabel_start = ttk.Label(
            self.startupwin,
            style="title.TLabel",
            text="Drag Coefficient Calculator"
        )
        self.loaded = False
        style = ttk.Style()
        style.configure("title.TLabel",font=("Arial",30))
        style.configure("button.TButton",font=("Arial",15))
        style.configure("sub.TLabel",font=("Arial",20))    
        style.configure("text.TLabel",font=("Arial",15)) 
        self.newbutt = ttk.Button(
            self.startupwin,
            style="button.TButton",
            text="Create New Object",
            command=self.newobject
        )
        self.oldbutt = ttk.Button(
            self.startupwin,
            style="button.TButton",
            text="Use Old Object",
            command=self.oldobject  
        )
        self.titlelabel_start.pack()
        self.newbutt.pack()
        self.oldbutt.pack()
        self.startupwin.mainloop()
    def oldobject(self):
        self.oldwin = tk.Toplevel(self.startupwin)
        style = ttk.Style()
        style.configure("title.TLabel",font=("Arial",30))
        style.configure("button.TButton",font=("Arial",15))
        style.configure("sub.TLabel",font=("Arial",20))    
        style.configure("text.TLabel",font=("Arial",15)) 
        self.titlelabel_oldwin = ttk.Label(
            self.oldwin,
            style="title.TLabel",
            text="Select Object:"
        )
        self.objectfiles_var= tk.StringVar()
        self.objectfiles= ttk.Combobox(
            self.oldwin, 
            textvariable=self.objectfiles_var
        )
        self.files = []
        self.objectfiles["values"] = (self.files)
        self.objectfiles['state'] = 'readonly'
        self.objectfiles.bind("<<ComboboxSelected>>", self.objectboxvalue)
        self.importbutt= ttk.Button(
            self.oldwin,
            text="Import Objects",
            style="button.TButton",
            command=self.importfiles
        )
        self.contbutt = ttk.Button(
            self.oldwin,
            style="button.TButton",
            text="Continue With Selected Object",
            command=self.load
        )
        self.titlelabel_oldwin.pack()
        self.objectfiles.pack()
        self.importbutt.pack()
        self.contbutt.pack()
    def objectboxvalue(self,event):
        self.chosenfile =  self.objectfiles.get()
    def newobject(self):
        self.dragcoefficient = 0.0
        self.shapename = ""
        self.homewin = tk.Toplevel(self.startupwin)
        style = ttk.Style()
        style.configure("title.TLabel",font=("Arial",30))
        style.configure("button.TButton",font=("Arial",15))
        style.configure("sub.TLabel",font=("Arial",20))    
        style.configure("text.TLabel",font=("Arial",15)) 
        #objects
        self.titlelabel = ttk.Label(
            self.homewin,
            style="title.TLabel",
            text="Create Object"
        )
        self.shapenameentrylabel = ttk.Label(
            self.homewin,
            style="sub.TLabel",
            text="Enter Name of Object:"
        )
        self.shapenameentry = ttk.Entry(
            self.homewin
        )
        self.frontalareaentrylabel = ttk.Label(
            self.homewin,
            style="sub.TLabel",
            text="Enter Frontal Area:"
        )
        self.frontalareaentry = ttk.Entry(
            self.homewin,
        )
        self.dragcoefficientlabel = ttk.Label(
            self.homewin,
            style="sub.TLabel",
            text="Enter Drag coefficient:"
        )
        self.dragcoefficiententry = ttk.Entry(
            self.homewin,
        )
        self.calculatebutt = ttk.Button(
            self.homewin,
            style="button.TButton",
            text="Calculate!",
            command=self.dragcalc  
        )   
        self.dragearealabel = ttk.Label(
            self.homewin,
            style="sub.TLabel",
            text="Drag Area:"
        )
        self.savebutt = ttk.Button(
            self.homewin,
            style="button.TButton",
            text="Save",
            command=self.save  
        ) 
        try:
            self.frontalareaentry.insert(0,self.loadedobject.area)
            self.dragcoefficiententry.insert(0,self.loadedobject.coefficient)
        except:
            self.frontalareaentry.insert(0,"")
            self.dragcoefficiententry.insert(0,"")
            
        self.titlelabel.pack()
        self.shapenameentrylabel.pack()
        self.shapenameentry.pack()
        self.frontalareaentrylabel.pack()
        self.frontalareaentry.pack()
        self.dragcoefficientlabel.pack()
        self.dragcoefficiententry.pack()
        self.dragearealabel.pack()
        self.calculatebutt.pack()
        self.savebutt.pack()
        self.homewin.mainloop()
        
    def shapeselectorvaluefinder(self,event):
        self.chosenshape =  self.shapeselector.get()
    def dragcalc(self):
        if self.loaded == False:
            self.dragcoefficient = float(self.dragcoefficiententry.get())
            self.dragarea = self.dragcoefficient*float(self.frontalareaentry.get())
        else:
            self.dragcoefficient = float(self.loadedobject.coefficient)
            self.dragarea = self.dragcoefficient*float(self.loadedobject.area)
            self.loaded = False
            self.dragcalcwin()
            
        self.dragearealabel.config(text="Drag Area: " +str(round(self.dragarea,1))+"m^2")
        self.speeds = []
        self.forces = []
        for i in range (0,41,1):
            self.speeds.append(i)
            self.forces.append(self.forcecalc(i))
        plt.plot(self.speeds,self.forces)
        plt.xlabel("Speed (m/s)")
        plt.ylabel("Force (kN)")
        plt.title("Force vs Speed")
        plt.show()
    def forcecalc(self,speed):
        return((math.floor(0.5*1.2*self.dragarea*(speed**2)))/1000)
    def save(self):
        self.shapename = str(self.shapenameentry.get())
        #pulls data from input and makes a player using object
        obj = objtosave(self.shapename,self.dragcoefficiententry.get,self.frontalareaentry.get())
        #converts object to json to be saved 
        try:
            base = Path("L:/DragCalc")
            jsonpath = base / (self.shapename+".json")
            jsonStr = json.dumps(obj.__dict__)
            base.mkdir(exist_ok=True)
            with open(jsonpath,"w") as outfile:
                outfile.write(jsonStr)  
        except:
            base = Path("C:/DragCalc")
            jsonpath = base / (self.shapename+".json")
            jsonStr = json.dumps(obj.__dict__)
            base.mkdir(exist_ok=True)
            with open(jsonpath,"w") as outfile:
                outfile.write(jsonStr) 
    def importfiles(self):
        self.foundfiles = []
        try:
            p = Path("L:/DragCalc")
            os.chdir(p)
            for file in glob.glob("*.json"):
                if file not in self.foundfiles:
                    self.foundfiles.append(file.replace(".json",""))
            self.objectfiles["values"] = self.foundfiles
        except:
            p = Path("C:/DragCalc")
            os.chdir(p)
            for file in glob.glob("*.json"):
                if file not in self.foundfiles:
                    self.foundfiles.append(file.replace(".json",""))
            self.objectfiles["values"] = self.foundfiles
    def load(self):
        try:
            base = Path("L:/DragCalc")
            jsonpath = base / (self.chosenfile+".json")
            pfile = open(jsonpath)
            objectsave = json.load(pfile)
            self.loadedobject = objtosave(objectsave["name"],objectsave["coefficient"],objectsave["area"])
            self.loaded = True
            self.dragcalc()
        except:
            base = Path("C:/DragCalc")
            jsonpath = base / (self.chosenfile+".json")
            pfile = open(jsonpath)
            objectsave = json.load(pfile)
            self.loadedobject = objtosave(objectsave["name"],objectsave["coefficient"],objectsave["area"])
            self.loaded = True
            self.dragcalc()

master = tk.Tk(
    className=" Drag Calculator"
)
def startup():
    #create player folder
    try:
        path = "L:/DragCalc"
        if not os.path.exists(path):
            os.makedirs(path)        
    except:
        path = "C:/DragCalc"
        if not os.path.exists(path):
            os.makedirs(path)
startup()
runapp = App(master)
