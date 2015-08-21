Chess problem
==============

The problem is to find all unique configurations of a set of normal chess pieces 
on a chess board with dimensions M×N where none of the pieces is in a position 
to take any of the others. Assume the colour of the piece does not matter, and 
that there are no pawns among the pieces.

Input
-----
*  The dimensions of the board: M, N
*  The number of pieces of each type (King, Queen, Bishop, Rook and Knight) to try and place on the board.

Output
------
List all the unique configurations to the console for which all of the pieces can be placed on the board without threatening each other.


Usage
-----
pythom -m chess.main -w \<number of parallel processes \> -r \<number of rows\> -c \<number of  columns\> -p \<string of pieces (like 'kkrrnn')\>


Testing
-------
python runtests.py


Results
-------
In a Intel(R) Core(TM) i5-4460  CPU @ 3.20GHz the process took 2010 seconds using 4 cores to find 3,063,828 possibilities for a 7x7 board with 2 kings, 2 queens, 2 bishops and one knight.

