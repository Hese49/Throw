# -*- coding: utf-8 -*-
"""
@author: Hese49
Created: Dec 2024

This file 'ThrowCalc.py' is the calculation module for the file 
'Throwing_motion.py' TkInter graphical user interface (QUI). It calculates 
 the values ​​of the parameters in an oblique throwing motion when the necessary
 input data is given.
 This file can also be used as an independent program (if __name__ == "__main__"
 at the end)
 There is also a test version of this file 'ThrowCalc_Test.py'.

"""
# At the very end you will find the description of the flow of the program.
# Funktion 'calculate' (the last function) is the main function. Its input 
# is the list 'vals', which is the list of the known and unknown values of the
# quantities needed in throwing motion calculations. 
# The output of the function 'calculate' is the same list, now named as 'Vals',
# which has been supplemented with calculation results.
# The user enters the values of the known quantities in the 'Throwing_motion.py' 
# QUI or at the end of this file (if this file is used as an independent program.) 


from   sympy import symbols, Eq, sqrt, solve, nsolve, sympify,\
                    sin, cos, tan, asin, atan, atan2

# SymPy symbols:
y0,a0,v0,x1,y1,a1,v1,t,hm,v0x,v0y,v1x,v1y = symbols('y0,a0,v0,x1,y1,a1,v1,t,hm,\
v0x,v0y,v1x,v1y')
# The nine first symbols are for user entries and the rest for calculations.
# a0 = initial angle,   hm = max height    (the rest are intuitive)
Qnts = [y0,a0,v0,x1,y1,a1,v1,t,hm,v0x,v0y,v1x,v1y]    # Quantities 
global g, rad
g = 9.81                                              # Gravity constant
rad = 0.0174533                                       # Factor: deg to rad 

def find_1_uk():              # Find  equations(indices) with only one unknown
# OUT: # List of tuples (ind/eqs, var),  eq with one unknown
    unks_1 = []               # List of ind/equations with only one unknown
    to_solve_1 = []                   # Tuples (index, only unknown quantity) 
    for i, e in enumerate(unks):      # List of unknown lists
        if len(e) == 1:               # Equation e (=index) has only 1 unknown
            unks_1.append(i)          # Append index of one var equation
            to_solve_1.append((i, unks[i][0])) #Tuple (ind, var), like (1, v0y)      
    return to_solve_1    # List of tuples (ind/eqs, var),  eq with one unknown
    
def siground(number:float, ndigits=3)->float:   # Rounding to 3 signif. digits
#  IN: Number
# OUT: Number rounded to 3 significant digits
    if number == 0:
        return 0.00
    if abs(number) < 0.05:
        return 0.00
    return float(f"{number:.{ndigits}g}")
                
def solve_1(to_solve_1):    # Solves set of equations of one variable    
#  IN: List of tuples (index/eqs, variable) (like [(0, v0x), (1, v0y)])
# OUT: list of 2-tuples (variable, value) from solutions of one var equations 
    global eqs
    global Vals
    solved_1 = []           # Solutions (var, value) for return
    for tup in to_solve_1:  # Solves each one var eq from the input list 'to_solve_1'  
        if (tup[0] == 5 or tup[0] == 8 or tup[0] == 11):   # eqs5, eqs8, eqs11 
        #eqs5(t), egs8(v0y) (and eqs9(v0y)) are 2.degree and have two solutions       
            s1 = solve(eqs[tup[0]], tup[1]) # Solving equation by SymPy solve
            solved_1.append((tup[1], s1[0]))
            if tup[0] == 5 and Vals[1]== 90:     # eqs5(t) in throw straight up                 
                Vals[5] = min(s1)               
                solved_1.append((tup[1], min(s1))) # Time for a rising object
            else:
                solved_1.append((tup[1], max(s1)))
        else:
            s1 = solve(eqs[tup[0]], tup[1])           
            if s1 != []:
                solved_1.append((tup[1], s1[0])) 
    return solved_1                         # List of 2-tuples (var, val)

def upd_eqs(sbss):                          # Make substitutions to equations
      # IN : List of substitutions: 2-tuples (var, val)
      # OUT: List 'eqs' of updated equations.
    for j, eq in enumerate(eqs):            # Through equations
        eq = eq.subs(sbss)                  # Make substitution to an equation
        eqs[j] = eq                         # Replace with substituted equation 
    return eqs                              # Updated list of equations
    
def upd_unks(sbss): 
    # Update the lists of unknown quantities in equations: unks = unk0, unk1,..
    # IN : List of substitutions: 2-tuples (var, val) like [('a0', 60.0), .. )]
    # OUT: List 'unks' of  unknown variables for each equation after update
    for sb in sbss:                         # sb = ('a0', 60.0), ('v0', 10.0),..                      
          for un in unks:                   # Like un = unk0, unk1,..
              for u in un:                  # Like u = v0x, v0, a0,..
                  if sb[0] == str(u):
                      un.remove(u)               # Like 'a0', 'v0',..
    return unks  # List of unknown variables for each equation after the update
  
def upd_Vals(solved_1):  # Update the list of values ('Vals' is output list)
# List of values 'Vals' is updated with quantity values of solved equations
# IN : List of 2-tuples (variable, value)
# OUT: List 'Vals' updated 
    for i in range(len(solved_1)): 
        index = Qnts.index(solved_1[i][0])
        if Vals[index] == 'na': Vals[index] = solved_1[i][1] 
    return Vals                  

def user_subs(Vals): # Substitute all equations with user input values...
                     # and update the lists of unknown quantities in equations.
    # IN : List of values with user entries
    # OUT: With user entries updated equations and lists of equation unknows 
          
    # Create substitutions    
    sbss = []                                     # Substitutions 
    for i, va in enumerate(Vals):                 # Through the list of values
        if va != 'na':
            sbss.append((str(Qnts[i]), Vals[i]))  # Append user entry to 'sbss'

    # Updates with substitutions    
    eqs  = upd_eqs(sbss)  # With user entries updated equations
    unks = upd_unks(sbss) # With user entries updated lists of equation unknows
    return eqs, unks

def specials(vals):     # ------ SPECIAL CASES -------------------         
# 2) ALL INITIALS  y0, a0, and v0  ARE GIVEN 
    # 2a) BASIC THROW: Find flight time t and range x1 to ground level y1=0 
    if vals[0] != 'na' and vals[1] != 'na' and vals[2] != 'na' and \
        vals[3] =='na' and vals[4] == 0 and vals[7] == 'na':
        Y0=vals[0] ; A0=vals[1]*rad ;V0=vals[2] # Initials
        V0x =  vals[2]*cos(A0)                  # horizontal velocity
        V0y =  vals[2]*sin(A0)                  # vertical init velocity
        Tr = (V0*sin(A0) + sqrt((V0*sin(A0))**2 + 2*g*Y0))/g  # Flight time
        X1 = V0*cos(A0)*Tr                                    # Range
        Tr = Tr                    # Rounding to four digits
        X1 = X1     
        vals[7] = Tr                            # Update flight time
        vals[3] = X1                            # Update range
        
    # 2b) Find position (x1, y1), given all initials y0, a0, v0 plus time t
    if vals[0] != 'na' and vals[1] != 'na' and vals[2] != 'na' and \
        vals[3] =='na' and vals[4] == 'na' and vals[7] != 'na':
        Y0=vals[0]; A0=vals[1]*rad; V0=vals[2]; Tp=vals[7]  # Initials
        V0x = V0*cos(A0)                             # horizontal velocity
        V0y =  V0*sin(A0)                            # vertical init velocity
        X1 =  V0x*Tp                    # x-position
        vals[3] = X1
        Y1 =  Y0 + V0y*Tp - 4.905*Tp**2              # y-pos
        Y1 = Y1
        vals[4] = Y1
    
# 3) ---- FIND INITIAL VELOCITY ----
    # 3a) Find the initial velocity v0, given  y0=0, angle a0 and range x1.
    #     The throw is from 0-level to 0-level (y1=0)
    if vals[0] == 0 and vals[1] != 'na' and vals[2] == 'na' \
    and vals[3] != 'na' and vals[4] == 0:
       A0 = vals[1];  X1 = vals[3]                               # Entries
       V0 = sqrt(X1*9.81/(sin(2*A0*rad)))
       V0 = V0
       vals[2] = V0
   
    # 3b) Find the initial velocity v0 given some elevation y0 > 0, angle a0 
    #  and range x1. The throw is to 0-level (y1=0) (This works also with y0=0)
    if vals[0] != 0  and vals[1] != 'na' and vals[2] == 'na' \
    and vals[3] != 'na' and vals[4] != 'na': 
       Y0 = vals[0]; A0 = vals[1]*rad ; X1 = vals[3]; Y1 = 0     # Entries
       T = (v0*sin(A0) + sqrt((v0*sin(A0))**2  + 2*g*Y0))/g
       eq = v0*cos(A0)*T-X1
       V0 = nsolve(eq, v0, 10 )
       V0 = V0
       vals[2] = V0
                          
    # 3c) Find the initial velocity v0 to hit the target at point (x1,y1).
    # Given intitial height (y0=0) and angle a0, 
    if vals[0] == 0 and vals[1] != 'na' and vals[2] == 'na' \
    and vals[3] != 'na' and vals[4] != 'na':
       X1 = vals[3];  A0 = vals[1]*rad ; Y1 = vals[4]            # Entries
       div =2*(X1*tan(A0) - Y1)*(cos(A0)**2)
       V0 = sqrt(X1**2*9.81/div)
       V0 = V0
       vals[2] = V0
 
# 4) ---- FIND INITIAL ANGLE ----      
    # 4a) Find launch angle a0, given initial velocity v0 and range x1.
    #     The throw is from 0 level (y0=0) to 0 level (y1=0)  
    if vals[0] == 0 and vals[1] == 'na' and vals[2] != 'na' \
    and vals[3] != 'na' and vals[4] == 0:
       X1 = vals[3];  V0 = vals[2]                              # Entries
       A0 = 0.5*asin(X1*9.81/V0**2)      
       A0 = A0/rad                   
       vals[1] = A0
       
    # 4b1) Find launch angle a0, given initial velocity v0 and target (x1,y1)
    #      The throw is from 0 level (y0=0).
    
    if vals[0] == 0 and vals[1] == 'na' and vals[2] != 'na' \
    and vals[3] != 'na' and vals[4] >= 0:
       X1 = vals[3];  V0 = vals[2] ; Y1 = vals[4]               # Entries   
       eq4b1 = Y1*V0**2*(cos(a0))**2 - X1*V0**2*cos(a0)*sin(a0)\
            + 0.5*9.81*X1**2                                # Equation for a0
       # Numerical solution of eq4b1:
       A0 = nsolve(eq4b1, a0, atan(Y1/X1))        # atan() is a starting value 
       A0 = A0/rad                                # To degrees     
       vals[1] = A0                               # Update list of values 'vals'
      
    # 4b2) Find launch angle a0, given initial velocity v0 and target (x1,y1)
    #    The throw is from level y0>0.   
    if  vals[0] != 0 and vals[1] == 'na' and vals[2] != 0 \
    and vals[3] != 'na'  and vals[3] != 0 and vals[4] != 'na':
       Y0 = vals[0]; V0 = vals[2]; X1 = vals[3]; Y1 = vals[4]    # Entries  
       eq4b2 =  Y0-Y1 + X1*tan(a0) - g*X1**2/(2*V0**2*cos(a0)**2)   # Eg for a0
       # Numerical solving of eq4b2:'
       A0 = nsolve(eq4b2, a0, atan(Y1/X1))        # atan() is a starting value 
       A0 = A0/rad                                # To degrees   
       vals[1] = A0                               # Update list of values 'vals'
         
    # 4c) Find the initial angle a0 given some elevation y0 > 0, velocity v0 
       #  and time t. The throw is to 0-level (y1=vals[4]=0) 
    if vals[0] != 0  and vals[1] == 'na' and vals[2] > 0 \
       and vals[4] == 0 and vals[7] > 0: 
           Y0 = vals[0]; V0 = vals[2]; T = vals[7]   # Entries
           A0 = asin(0.5*g*T/V0 - Y0/(V0*T))         # Init angle
           X1 = cos(A0)*V0*T                         # Range
           A0 = A0/rad                               # To degrees   
           vals[1] = A0                              # Update list 'vals'
           vals[3] = X1      
 
# 5)---- FIND TIME ----
    # 5) How long does it take to reach maximum altitude? 
    if vals[0] == 0 and vals[1] != 'na' and vals[2] != 'na' \
    and vals[3] == 'na' and vals[4] == 'na'  and vals[7] == 'na':
       A0 = vals[1]*rad;  V0 = vals[2]           # Entries 
       T1 = V0*sin(A0)/9.81
       T1 = T1
       vals[7] = T1   
    return vals


# ================  CALCULATE()  the main function ===========================

def calculate(vals): # 'vals' is the list of quantities coming from TkInter GUI
    global Vals                             # List of quantity values 
    Vals = vals                             # User input
    global g; g = 9.81
    
            
    # Equations and lists of their unknown quantities
    eq0 = Eq(v0x - v0*cos(a0*rad), 0)                # x-component of v0
    unk0 = [a0, v0, v0x]
    eq1 = Eq(v0y - v0*sin(a0*rad), 0)                # y-component of v0
    unk1 = [a0, v0, v0y]                             
    eq2 = Eq(v1x - v0x,0)                            # Horizontal speed 
    unk2 = [v0x, v1x]         
    eq3 = Eq((v1y - v0y + 9.81*t), 0)                # Vertical speed       
    unk3 = [t, v0y, v1y]  
    eq4 = Eq(x1 - v0x*t, 0)                          # x-coordinate          
    unk4 = [t, v0x, x1]
    eq5 = Eq(y1 - y0 - v0y*t + 4.905*t**2, 0)        # y-coordinate          
    unk5 = [y1, y0, v0y, t]
    eq6 = Eq(a1 - 57.3*atan2(v1y, v1x), 0)           # angle         
    unk6 = [a1, v1y, v1x]
    eq7 = sympify(Eq(v1 - sqrt(v1x**2 + v1y**2), 0)) # Speed
    unk7 = [v1, v1x, v1y]
    eq8 = sympify(Eq(v0y**2 - v1y**2 - 19.62*y1 + 19.62*y0, 0)) # Energy principle
    unk8 = [v0y, v1y, y1]
    eq9 = sympify(Eq(v0y**2  - 19.62*hm + 19.62*y0, 0)) # Energy principle for max high
    unk9 = [y0, v0y, hm]
    eq10 =Eq(a0 - 57.3*atan(v0y/v0x), 0)             # initial angle
    unk10 = [a0, v0x, v0y]
    # Launch velocity from range and launch angle whwén y0 = 0:
    eq11 = Eq(  v0 - 3.1321*sqrt(x1)/abs(sqrt(sin(2*a0*rad))), 0)  
    unk11 = [a0, v0, x1]
        
    global eqs                              # List of equations
    eqs = [eq0, eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, eq11]
    global unks         # List of lists for unknown variables in each equation
    unks = [unk0, unk1, unk2, unk3, unk4, unk5, unk6, unk7, unk8, unk9,
            unk10, unk11]         # 'unk1' is list of unknown variables in eq1
       
# ----- PHASE I --- SPECIAL CASES --------------------- 
   
 # 1a) Modify equations for horizontal throw calculations (launch angle a0=0)
    if vals[1] == 0:                 # Horizontal throw: launch angle = 0
        vals[1] = 0.00                      # a0: 0 --> 0.00
        vals[8] = vals[0]                   # hm = y0
        vals[9] = vals[2]                   # v0x = v0
        vals[11] = vals[2]                  # v1x = v0
        eq0 = Eq(v0x - v0, 0)               # v0x = v0 
        unk0 = [v0x, v0]
        eq1 = Eq(v0y, 0)                    # v0y = 0.0
        unk1 = [v0y] 
        eq3 = Eq((v1y + 9.81*t), 0)         # Vertical speed 
        unk3 = [v1y, t]
        eq5 = Eq(y1 - y0  + 4.905*t**2, 0)  # y-coordinate          
        unk5 = [y1, y0, t]
        eq8 = sympify(Eq(v1y**2 - 19.62*y0 + 19.62*y1, 0)) # Energy principle
        unk8 = [v1y, y0, y1]
        eq9 = sympify(Eq(-hm +y0, 0))     # Energy principle for max high
        unk9 = [hm, y0]
        
        if vals[3] != 'na' and vals[2] != 'na':   # Horiz.velocity and range
            Y0 = g*vals[3]**2/(2*vals[2]**2)
            Y0 = Y0
            vals[0] = Y0 
            
 # 1b) The initial angle a0 = 90 deg: Throw straight up  or free fall
    if vals[1] == 90 or vals[1] == -90:
       vals[3] = 0;  vals[5] = 90                  # x1 = 0, v1 = 90
       Y0 = vals[0]; V0y = vals[2]; Y1 = vals[4]; V1y = vals[6]
       T = vals[7]; Ym = vals[8]
       vals[3] = 0;                           # No horizontal movement x1 = 0
       
       # Position after time T
       if V0y != 'na' and T != 'na':        
           V1y = V0y - g*T;  vals[6] = V1y   
           if Y0 != 'na':
              Y1 = Y0 + V0y*T - 0.5*g*T**2; vals[4] = Y1
       
       # Max hight
       if V1y == 0: #   and float(V1y) == 0.0:
          T = V0y/g;  vals[7] = T
          Y1 = Y0 + V0y*T - 0.5*g*T**2; vals[4] = Y1
          vals[8]=vals[4]                             # Max height Ym
          
       # How long does it take to reach some altitude Y1?
       if Y0 != 'na' and V0y != 'na' and Y1 != 'na' and T == 'na':
           T1 = (-V0y - sqrt(V0y**2 + 2*g*(Y0 -Y1)))/(2*(-0.5*g))
           T2 = (-V0y + sqrt(V0y**2 + 2*g*(Y0 -Y1)))/(2*(-0.5*g))
           vals[7] = T2
           V1y = V0y - g*T2;  vals[6] = V1y  
    
       # Given max height Ym, what is the initial velocity V0y?
       if Y0 != 'na' and V0y == 'na' and Ym != 'na' and T == 'na':
           Y1 = Ym; vals[4]  = Y1
           V0y = sqrt(2*g*(Y1-Y0))
           vals[2] = V0y
                     
    # Rounding all output values to 3 signif.digits 
       for i, va in enumerate(vals):
           if va != 'na':
               va = siground (va, 3)
               vals[i] = va
               
       if vals[7] != 'na' and vals[7] < 0: vals[7] = -vals[7]        
       return vals                                   # Goes to TkInter GUI        
                                               
    if vals[1] != 'na' and float(vals[1]) < 0:
        vals[8] = vals[0]    # In downward sloping throw hm = y0
        
    
    Vals = vals              # Input 'vals' is copied into 'Vals'
    # Other special cases are calculated in the function 'specials()':    
    Vals = specials(vals)  # List 'Vals' comes from QUI and after special cases          
    # Substitute the known values in equations and update the lists of unknown 
    # quantities in each equation after user input and possible  special
    # case calculations:
    eqs, unks = user_subs(Vals)                            
   
# ------- PHASE II --- SOLVE EQUATIONS WITH ONE UNKNOWN ------------------------
# Solve those equations with only one variable left, make updates and 
# and try if new equations with only one unknown have appeared, and solve them.
# Continue that process in loop so long as possible.

    is_1 = True                        # Control flag for while loop if ..                                       
    while is_1 == True:                #..there are any one_variable equations.
          to_solve_1 = find_1_uk()     # Find tuples (indice/eq, unknown).. 
          if to_solve_1 == []:         # When there are no more one ..
              is_1 = False             # variable equations
              break             
          else:                        # SOLVE all equations with one unknown
              solved_1 = solve_1(to_solve_1)  # Solve like [(v0x, 5.0), ..] 
          # UPDATE 'Vals', 'eqs' and 'unks':
          Vals = upd_Vals(solved_1)           # Updated list of quantity values
          eqs = upd_eqs(solved_1)             # Updated  equations 
        
          # Transform 'solved_1' to 'sbss' for 'unks' update because quantit..
          # symbols are needed in string form for 'upd_unks(sbss)' function.
          sbss = []
          for su in solved_1:
            sbss.append((str(su[0]), su[1]))                   
          unks = upd_unks(sbss)             # Updated list of equation unknowns
   # END while
   
    # Rounding all output values to 3 signif.digits 
    for i, va in enumerate(Vals):
        if va != 'na':
            va = siground (va, 3)
            Vals[i] = va

    # Ad_hoc   
    if Vals[7] < 0: Vals[7] = -Vals[7] # negative time  -> make it positive 
    if Vals[5] == -180: Vals[5] = 90   # -180 deg = 90 deg
    print(Vals)   # For console printing
    return(Vals)  # Return all quantity values to the TkInter QUI for printing. 
    #      ----------------   END OF CALCULATIONS  -------------------


# ============   WHEN FILE IS USED AS AN INDEPENDENT PROGRAM   ================

if __name__ == "__main__":               # When used as an independent program

# Give your initial values of the quantities below:
    vals = [0,  30, 14.1, 'na',  0, 'na',  'na', 'na', 'na', 'na','na', 'na', 'na']                                              
#          [y0, a0,  v0,   x1,   y1,   a1,    v1,   t,    hm,] [v0x,  v0y, v1x, v1y]
#   indices 0    1    2    3     4     5      6     7     8      9    10   11   12
#           a0 = initial angle,  hm = max height  (the rest are intuitive) 
            
    calculate(vals)   # Runs the calculations as an independent program.
 
    
"""       
    PROGRAM FLOW
    
    The main function 'calculate' get its Input list 'vals' from TkInter GUI.
    List 'vals' includes  values of quantities  needed in throwing motion.
    The user has entered the known quantities into that list.
    The Output of this module is the list 'Vals', which includes the values 
    given by the user and calculated in this module.
               
    PHASE I
    Some special cases will be calculated first separately (Special 1..5).
    The updates are made in the list 'vals', but after PHASE I they are in
    the list 'Vals'.
    
    PHASE II
    The idea is to find all those equations having only one unknown variable 
    and solve them. Then make updates and check if new equations,
    with only one unknown have appeared, and solve them. Continue this process
    in loop so long as possible and then give out the list 'Vals'. 
    
    1) Substitute all equations 'eqs' with user input values and with values 
       calculated in special cases. These values can be found in the list 'Vals'.
       Also update the unknown quantities in the lists of list 'unks'.
       (List 'unks' contain a list for every equation for its unknowns.)
         
    2) Find those equations with only one variable ('function find_1_uk()').
    
    3) Solve equations with only one variable      ('function solve_1_uk()').
    
    4) Do three updates with the newly found variable values:
          -Update values 'Vals'        (function 'upd_Vals()'
          -Update equations 'eqs'      (function 'upd_egs()'
          -Update list of unknow variables 'unks' for every equation
          (function'upd_unks())'
     
    Repeat repeat steps 1)...4) until there are no more equations with
    only one unknown variable (while loop).
    
    OUTPUT
    Print the list 'Vals' in the console.
    Return the list 'Vals' to the TkInter GUI to be printed  in its
    entry fields.                                                                    
"""
