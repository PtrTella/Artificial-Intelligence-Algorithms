
---------------------------

Some Prolog Examples
---------------------------


1. Here are some clauses (facts).

likes(mary,food).
likes(mary,wine).
likes(john,wine).
likes(john,mary).

The following queries yield the specified answers.

 | ?- likes(mary,food). 
		yes.
		
 | ?- likes(john,wine). 
		yes.
		
 | ?- likes(john,food). 
		no.

How do you add the following facts?

1. John likes anything that Mary likes 
2. John likes anyone who likes wine 

==========================================================================

2. Slightly more complicated family tree.


                              James I
                                 |
                                 |
                +----------------+-----------------+
                |                                  |
             Charles I                          Elizabeth
                |                                  |
                |                                  |
     +----------+------------+                     |
     |          |            |                     |
 Catherine   Charles II   James II               Sophia
                                                   |
                                                   |
                                                   |
                                                George I

Here are the resultant clauses:
-------------------------------
  male(james1).
  male(charles1).
  male(charles2).
  male(james2).
  male(george1).

  female(catherine).
  female(elizabeth).
  female(sophia).

  parent(charles1, james1).
  parent(elizabeth, james1).
  parent(charles2, charles1).
  parent(catherine, charles1).
  parent(james2, charles1).
  parent(sophia, elizabeth).
  parent(george1, sophia).


Here is how you would formulate the following queries:
			  
     Who was Charles I's parent?
              Query: parent(charles1,X). 
			  
     Who were the children of Charles I?
              Query: parent(X,charles1). 

Now try expressing the following rules:

     M is the mother of X if she is a parent of X and is female 



==========================================================================

3. Constraints modeling

To be able to use constraints you need to import the library clpfd 

:- use_module(library(clpfd)).


Example
t(X) :- X  in 10..19.
s(Y) :- Y  in 19..30.

    ?-t(A),s(A).


Example
>= is a Prolog predicate. X >= Y requires that X and Y are ground.
maxValue(X,Y,X) :- X >= Y.
maxValue(X,Y,Y) :- X < Y.

  ?-maxValue(7,5,W).
  ?-maxValue(A,5,W).


#>= is a constraint. 
maxValueCon(X,Y,X) :- X #>= Y.
maxValueCon(X,Y,Y) :- X #< Y.

  ?-maxValueCon(7,5,W).
  ?-maxValueCon(A,5,W).



Example
sum(X,Y,Z) :- X+Y #= Z.
  ?-  X in 1..4, Y in 2..5, Z in 1..4\/ 19, sum(X,Y,Z).


Example
Generate values and then test for solutions

generate(1).
generate(X) :- generate(Y), X is Y+1.

test(10000).
goal :- generate(X), writeln(X), test(X), write('success').

  ?-goal.


Example
Using constraints results in a more efficient solution

generateCon(X) :- X in 1 .. 40000 .
goalCon :- generateCon(X), test(X), write(X).
  ?-goalCon.


Example
Optimization problem

q(A,B,C,S,P) :-
   A in 0..10,
   B in 0..10,
   C in 0..10,
   S #>= 2*A+3*B+7*C,
   P #= 3*A+4*B+10*C,
   labeling([max(P)],[P,S,A,B,C]).

   ?- q(A,B,C,13,P).


==========================================================================

4. Scheduling problem

Train schedule represented as a list of quadruples,
denoting departure and arrival places and times for each train.
In the following program, Ps is a feasible journey of length 3 from A to D
via trains that are part of the given schedule.


:- use_module(library(clpfd)).

trains([[1,2,0,1],    % from station, to station, departs at, arrives at
        [2,3,4,5],
        [2,3,0,1],
        [3,4,5,6],
        [3,4,2,3],
        [3,4,8,9]]).

threepath(A, D, Ps) :-
        Ps = [[A,B,_T0,T1],[B,C,T2,T3],[C,D,T4,_T5]],
        T2 #> T1,
        T4 #> T3,
        trains(Ts),
        tuples_in(Ps, Ts).

   example queries
     ?-threepath(1, 4, Ps).
       Ps = [[1, 2, 0, 1], [2, 3, 4, 5], [3, 4, 8, 9]].

