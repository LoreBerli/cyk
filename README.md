# CYK Algorithm
## TOC assigment 2016 ##
***
##### Lorenzo Berlincioni ######
***
##Usage##
	
	 >python cyk.py gram1 "001d#" -t
	 


The program takes as input:

* a *path* to a file representing a grammar
* a *string* that will be checked for belonging in the grammar
* *-t* as an optional argument to print on console the derivation tree

It returns a boolean according to the belonging of the string in the grammar.
## Grammar ##
The grammar must be in ChomskyNormalForm and in the following format:

    Variable->VariableVariable|Terminal
 ie.
 
    S->AB
    A->AA|a
    B->AB|b

Where *S,A,B* are Variables and *a,b* are Terminals.
It mush have a starting symbol 'S'.
Supports only single char terminals
## Extra ##
* tester.sh reads every newline in the file *strings* and feeds it to the algorithm
with the *-t* flag.
Then it redirects the output appending it to a file named *output*.
