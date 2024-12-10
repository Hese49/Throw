# Calculator for oblique throwing motion

THE FILES 

The file  '**Throwing_motion.py**'  is a  TkInter  graphical user interface (QUI).
It calculates the values ​​of the parameters in an oblique throwing motion when
the necessary input data is given. 

The file  '**ThrowCalc.py**'  is used as a calculation module of the QUI file. This file can also be used as an independent program (if __name__ == "__main__"  at the end of the file). There is also available a file '**ThrowCalc_Test.py**' , where there are many opportunities for printing intermediate results in a problem cases.

The file '**TestRuns.txt**' shows many possibilities for using the program to solve problems related to oblique throwing.  In '**Calculator.gif**' you can see the layout of the calculator. 

PROGRAM FLOW    
    The user  enters the known quantities into QUI and those quantities are then sent as a  
    list 'vals' to the calculation module. 
    The output (return) of the calculation module is the list 'Vals', which includes the values 
    given by the user and calculated in this module.
               
    Phase I
    Some special cases will be calculated first separately (Special 1..5).
    The updates are made in the list 'vals', (but after PHASE I they are in
    the list 'Vals').
    
    Phase II
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
    
    Output
    Print the list 'Vals' in the console.
    Return the list 'Vals' to the TkInter GUI to be printed  in its
    entry fields.       

    H.M.  Dec 2024               
