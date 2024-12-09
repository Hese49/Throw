 # -*- coding: utf-8 -*-
"""
Throwing_motion.py
Created  Dec 2024
@author: Hese49

This file 'Throwing_motion.py' is a TkInter graphical user interface (QUI).
It calculates the values ​​of the parameters in an oblique throwing motion when
the necessary input data is given.
It uses the file 'ThrowCalc.py' as a calculation module.

"""

import tkinter as tk
import sympy as sym 
import ThrowCalc as ThClc

# Sympy symbols
y0,a0,v0,x1,y1,a1,v1,t,mh, v0x,v0y,v1x,v1y = sym.symbols('y0,a0,v0,x1,y1,a1,v1,t,mh,\
v0x,v0y,v1x,v1y')
# The nine first symbols are for entries and the rest four for calculations.
# a0 = initial angle, mh = max hight,  tr = rise time, (the rest are intuitive)
#Qnts = [y0,a0,v0,x1,y1,a1,v1,t,mh, v0x,v0y,v1x,v1y]    # Quantities
global vals
vals = []                         # List of quantity values after user input

# ===================  FUNCTIONS  ======================================

# Submit the user entries to the list 'vals'.
def solve():
    global vals
    for en in ents:                    # Runs the entries
        val = en.get()                 # Get the entry values from the user
        if val != '':
            val = float(val)      
            vals.append(val)           # Non empty entry is added
        else:
            vals.append('na')          # The user did not provide this value
    extras = ['na', 'na', 'na', 'na']  # For non user quantities at he end..
    vals.extend(extras)                #   i.e for v0x,v0y,v1x,v1y
           
    for entry in ents:                 # Empty the entry fields before output                     
        entry.delete(0, tk.END)
    
    # Calculate with errror handling
    try:                               # Send the user entries to the module..
        result = ThClc.calculate(vals) # .. 'ThrowCalc' for calculations.                    
    except Exception as e:               
        tk.messagebox.showerror("Error",
            "Check Your input, please. Maybe more data is needed.\
             Maybe Your input can't be calculated in this program. ")
        reset() 
                                                                    
    output(result)      # Fill the entry fields with calculated quantities
    button2.focus()     # Focus to button 'Reset'                                  
    
# Fill the entry fields with the known quantities after calculations..
# in the module ThrowCalc.py 
def output(result):  
    i=0
    for ent in ents:                   # Runs the entry fields E0,...,E8
        ent.insert(0, result[i])       # Inserts the value from the list 'vals'
        i += 1
    
# Reset ready for the next problem, from button 'Reset'.
def reset(): 
    global vals   
    vals = []                          # Empty the quantity list of user input
    for entry in ents:                 # Empty entries E0...E8                              
        entry.delete(0, tk.END)
        entry.config(bg='white')
    E0.insert(0, 0)                    # Set default final   hight to 0
    E0.config(bg='lightyellow')
    E4.insert(0, 0)                    # Set default initial hight to 0
    E4.config(bg='lightyellow')
    #E0.focus_set()
    root.focus()                       # No visible focus

def white_entry(event):
    if event.widget.get() == '':
        event.widget.config(bg='white')

def error_message():
    tk.messagebox.showinfo("Warning", 'Not calculated, check your input')
    

# ===================  QUI WIDGETS  =====================================
# --- BASICS -----
root = tk.Tk()
root.title("Throwing Motion Calculator")
root.geometry("330x840")

# Title
txt0 = tk.StringVar() 
txt0.set("Throwing Motion")
lbl0 = tk.Label(root, 
                 textvariable=txt0, 
                 anchor=tk.CENTER,       
                 bg="lightblue",      
                 height=2,              
                 width=20,              
                 bd=3,                  
                 font=("Arial", 16, "bold"), 
                 #cursor="hand2",   
                 fg="black",             
                 #padx=15,               
                 #pady=15,                
                 justify=tk.LEFT,    
                 relief=tk.GROOVE  # RIDGE SUNKEN RAISED #  
                 #underline=0,           
                 #wraplength=250         
                )
lbl0.place(x=25,y=20)

# Instruction
txt1 = tk.StringVar()
txt1.set(" Enter the quantities you know\n (four is needed) and press the \
          \n the button 'Solve'.")
lbl1 = tk.Label(root, 
                  textvariable=txt1,
                  anchor=tk.W,  
                  height=3,              
                  width=32,              
                  bd=3,                  
                  font=("Arial", 14),
                  justify=tk.LEFT)                  
lbl1.place(x=25,y=90)

# --- INITIAL SITUATION -----
txt2 = tk.StringVar()
txt2.set("Initial situation" )
lbl2 = tk.Label(root, 
                  textvariable=txt2,            
                  height=1,              
                  width=14,              
                  bd=3,                  
                  font=("Arial", 14,),
                  fg="blue")
lbl2.place(x=0,y=180)
           
L0a = tk.Label(root, text="Height (default)", font=("Arial",14))
L0a.place(x=20,y=220)
E0 = tk.Entry(root, bg='lightyellow', width=6, justify='center', font=("Arial",14))
E0.insert(0, 0)                    # Insert the default value 0 for final hight
E0.bind('<FocusIn>', lambda n:E0.config(bg='lightyellow'))
E0.bind('<FocusOut>', white_entry) 
E0.place(x=170,y=220)
L0b = tk.Label(root, text="m", font=("Arial",14))
L0b.place(x=250,y=220)

L1a = tk.Label(root, text="Angle", font=("Arial",14))
L1a.place(x=20,y=260)
E1 = tk.Entry(root, width=6, justify='center', font=("Arial",14))
E1.place(x=170,y=260)
E1.bind('<FocusIn>', lambda n:E1.config(bg='lightyellow'))
E1.bind('<FocusOut>', white_entry)   
L1b = tk.Label(root, text="deg", font=("Arial",14))
L1b.place(x=250,y=260)

L2a = tk.Label(root, text="Speed", font=("Arial",14))
L2a.place(x=20,y=300)
E2 = tk.Entry(root, width=6, justify='center', font=("Arial",14))
E2.place(x=170,y=300)
E2.bind('<FocusIn>', lambda n:E2.config(bg='lightyellow'))
E2.bind('<FocusOut>', white_entry)  
L2b = tk.Label(root, text="m/s", font=("Arial",14))
L2b.place(x=250,y=300)


# --- END SITUATION -----
txt3 = tk.StringVar()
txt3.set("End situation" )
lbl3 = tk.Label(root, 
                  textvariable=txt3,             
                  height=1,              
                  width=14,              
                  bd=3,                  
                  font=("Arial", 14,),
                  fg="blue")
lbl3.place(x=0,y=360)
             
L3a = tk.Label(root, text="X-coord. (range)", font=("Arial",14))
L3a.place(x=20,y=400)
E3 = tk.Entry(root, width=6, justify='center', font=("Arial",14))
E3.place(x=170,y=400)
E3.bind('<FocusIn>', lambda n:E3.config(bg='lightyellow'))
E3.bind('<FocusOut>', white_entry)  
L3b = tk.Label(root, text="m", font=("Arial",14))
L3b.place(x=250,y=400)

L4a = tk.Label(root, text="Y-coord. (height):", font=("Arial",14))
L4a.place(x=20,y=440)
E4 = tk.Entry(root, bg='lightyellow', width=6, justify='center', font=("Arial",14),)
E4.insert(0, 0)                    # Insert the default value 0 for final hight
E4.bind('<FocusIn>', lambda n:E4.config(bg='lightyellow'))
E4.bind('<FocusOut>', white_entry)
E4.place(x=170,y=440)
L4b = tk.Label(root, text="m", font=("Arial",14))
L4b.place(x=250,y=440)

L5a = tk.Label(root, text="Angle", font=("Arial",14))
L5a.place(x=20,y=480)
E5 = tk.Entry(root, width=6, justify='center', font=("Arial",14))
E5.place(x=170,y=480)
E5.bind('<FocusIn>', lambda n:E5.config(bg='lightyellow'))
E5.bind('<FocusOut>', white_entry)  
L5b = tk.Label(root, text="deg", font=("Arial",14))
L5b.place(x=250,y=480)

L6a = tk.Label(root, text="Speed", font=("Arial",14))
L6a.place(x=20,y=520)
E6 = tk.Entry(root, width=6, justify='center', font=("Arial",14))
E6.place(x=170,y=520)
E6.bind('<FocusIn>', lambda n:E6.config(bg='lightyellow'))
E6.bind('<FocusOut>', white_entry)  
L6b = tk.Label(root, text="m/s", font=("Arial",14))
L6b.place(x=250,y=520)

L7a = tk.Label(root, text="Time", font=("Arial",14))
L7a.place(x=20,y=560)
E7 = tk.Entry(root, width=6, justify='center', font=("Arial",14))
E7.place(x=170,y=560)
E7.bind('<FocusIn>', lambda n:E7.config(bg='lightyellow'))
E7.bind('<FocusOut>', white_entry)  
L7b = tk.Label(root, text="s", justify='center', font=("Arial",14))
L7b.place(x=250,y=560)

# --- OTHER -----
txt4 = tk.StringVar()
txt4.set("Other")
lbl4 = tk.Label(root, 
                  textvariable=txt4,             
                  height=1,              
                  width=8,                  
                  bd=3,                  
                  font=("Arial", 14,),
                  fg="blue")
lbl4.place(x=0,y=620)
              
L8a = tk.Label(root, text="Max height", font=("Arial",14))
L8a.place(x=20,y=660)
E8 = tk.Entry(root, width=6, justify='center', font=("Arial",14))
E8.place(x=170,y=660)
E8.bind('<FocusIn>', lambda n:E8.config(bg='lightyellow'))
E8.bind('<FocusOut>', white_entry)  
L8b = tk.Label(root, text="m", font=("Arial",14))
L8b.place(x=250,y=660)

ents = [E0,E1,E2,E3,E4,E5,E6,E7,E8]                  # List of Entry fields
root.focus()

# --- BUTTONS -----
button1 = tk.Button(root, 
                   text="Solve", 
                   command=solve,
                   width=6,
                   activebackground="lightblue", 
                   bd=5,
                   cursor="hand2",
                   font=("Arial", 14), 
                   justify="center",
                   overrelief="raised",                  
                   )
button1.place(x=80,y=730)

button2 = tk.Button(root, 
                   text="Reset", 
                   command=reset,
                   width=6,
                   activebackground="lightblue", 
                   bd=5,
                   cursor="hand2",
                   font=("Arial", 14), 
                   justify="center",
                   overrelief="raised",                  
                   )
button2.place(x=190,y=730)

# --- RUN THE PROGRAM ---

root.mainloop()                                      
