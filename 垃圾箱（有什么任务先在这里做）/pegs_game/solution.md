# Pegs in a row — complete solution

Board: holes 1..n, k pegs (1<=k<n). Start: pegs on 1..k. Move: move exactly one peg to a vacant
hole strictly to its right. End: pegs on the k rightmost holes; player to move then loses.

## Answer
Alice (first player) wins  <=>  NOT (n even AND k even).
Equivalently: Bob wins  <=>  n and k are both even.

## 1. Word encoding and termination
Write a position as a word of length n over {P = peg, E = empty}. A move = choose x<y with w_x=P,
w_y=E and swap them. Let I(w) = #{(x,y): x<y, w_x=P, w_y=E} (sum over pegs of the number of empty
holes to its right). A legal move strictly decreases I (the pair (x,y) stops being an inversion and
no inversion is created). Hence:
 * the game is finite;
 * I=0 exactly for the word E^{n-k} P^k, i.e. pegs on n-k+1..n, which is the only position with no
   legal move. So normal play, terminal = packed-right.

## 2. Lemma (packed-left with even board and even number of pegs is P)
Let m=2t be even, k even, k<m, board 1..m, pegs on 1..k ("packed-left"). Then the player to move loses.
Proof. Pair holes (1,2),(3,4),...,(2t-1,2t); call a position *paired* if the two entries of every
pair are equal.
 * Packed-left is paired (k even, m-k even); the terminal word is paired too.
 * If a paired position is not terminal and a move peg x -> vacant y (x<y) is made, then x,y are in
   different pairs (a single pair has equal entries). Pair of x is PP, pair of y is EE before the
   move. Let x', y' be the partners. Reply: move the peg x' to the vacant hole y'. Legal since
   x'<y' (pair of x is left of pair of y) and y' is empty. Afterwards both pairs are equal again.
 * Induction: every position at the first player's turns is paired. The terminal position is paired,
   hence it can never arise right after a first-player move (which produces exactly two non-equal
   pairs), and can never be faced by the second player. The second player's reply always exists and
   is legal. By finiteness the play ends with the first player unable to move. QED

## 3. Alice's first move in the three remaining parity cases
All moves below are legal (target hole is strictly right and vacant), and each lands on a position
isomorphic to a packed-left position with EVEN board size and EVEN number of pegs, hence P by Lemma 2.

(a) n even, k odd: move the peg at hole 1 to hole n.  Result: pegs on {2,...,k} u {n}.
    Hole 1 stays empty forever, hole n is occupied forever (nothing to its right); so the game is
    exactly the packed-left game on the (n-2)-hole board {2,...,n-1} with the k-1 pegs on 2..k.
    n-2, k-1 are both even. Terminal matches: {n-k+1,...,n-1} u {n}.

(b) n odd, k even: move the peg at hole 1 to hole k+1.  Result: pegs on {2,...,k+1}.
    Hole 1 is inert; the game is the packed-left game on the (n-1)-hole board {2,...,n} with the k
    pegs on 2..k+1. n-1, k are both even. Terminal matches: {n-k+1,...,n}.

(c) n odd, k odd: move the peg at hole k to hole n.  Result: pegs on {1,...,k-1} u {n}.
    Hole n is occupied forever; the game is the packed-left game on the (n-1)-hole board {1,...,n-1}
    with the k-1 pegs on 1..k-1. n-1, k-1 are both even. Terminal matches: {n-k+1,...,n-1} u {n}.

In each case the player to move next (Bob) faces a P-position, so he loses.

## 4. Remaining case
n even, k even: the initial position is itself packed-left on an even board with an even number of
pegs, so by Lemma 2 Bob (as second player) wins.

Boundary cases: k=1 with n even -> case (a) moves peg 1 to n, terminal. k=1 with n odd -> case (c)
gives the sub-board with 0 pegs, already terminal. k=n-1 -> the prescribed move reaches the terminal
position. n=2,k=1 -> case (a) reaches the terminal position immediately.

## 5. Machine verification
Brute force (Grundy values, plus an independent backward induction) for 2<=n<=14 confirms
"packed(n,k) is P iff n,k both even". It also confirms for every non-(even,even) case that the
prescribed first move is legal and lands on a P-position, and that the Grundy value of that position
equals the Grundy value of the corresponding packed subgame (i.e. the isomorphism claims above).
Scripts: small.py, verify.py, pstates.py, moves.py, final_check.py (this folder).
