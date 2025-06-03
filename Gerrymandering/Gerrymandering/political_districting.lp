% Political Districting ASP Program
% Maximizes representatives for a specified party (party_to_optimize)

% --- Inputs ---
% cell(X,Y) - cell at position (X,Y) exists
% vote(X,Y,P) - cell (X,Y) votes for party P (0 or 1)
% grid_size(MaxRows, MaxCols) - grid dimensions
% num_districts(K) - number of districts to create

% --- Parameter (to be set via command line, e.g., clingo -c party_to_optimize=0 ...) ---
#const party_to_optimize = 0. % Default, will be overridden by -c

% --- Helper for district and party domains ---
district_id(D) :- num_districts(K), D = 1..K.
party_id(0).
party_id(1).

% --- Generate district assignments ---
% Each cell must belong to exactly one district.
{ district(X,Y,D) : district_id(D) } = 1 :- cell(X,Y). % Changed: D = 1..K to district_id(D)

% --- Adjacency definition ---
% Cells are adjacent if they share an edge (Manhattan distance 1).
adjacent(X1,Y1,X2,Y2) :- cell(X1,Y1), cell(X2,Y2),
                         |X1-X2| + |Y1-Y2| = 1.

% --- Connectivity Constraint: Each district must be connected ---

% 1. Choose a unique "root" cell for each district.
%    For example, the cell with the smallest X, then smallest Y, within that district.
%    Exactly one root per district.
1 { root(X,Y,D) : cell(X,Y) } 1 :- district_id(D).
% Ensure the root cell is actually part of the district it's a root for.
:- root(X,Y,D), not district(X,Y,D).

% 2. Define reachability within a district from its root.
reachable(X,Y,D) :- root(X,Y,D). % The root is reachable.

reachable(X2,Y2,D) :- reachable(X1,Y1,D),      % If (X1,Y1) is reachable in D
                      district(X2,Y2,D),       % and (X2,Y2) is in D
                      adjacent(X1,Y1,X2,Y2).  % and they are adjacent, then (X2,Y2) is reachable.

% Symmetric reachability, can sometimes help the solver or make logic clearer
reachable(X1,Y1,D) :- reachable(X2,Y2,D),
                      district(X1,Y1,D),
                      adjacent(X1,Y1,X2,Y2).


% 3. All cells in a district D must be reachable from the root of D.
:- district(X,Y,D), not reachable(X,Y,D).

% --- Vote Counting ---
% Count votes for each party P in each district D.
district_votes(D,P,N) :- district_id(D), party_id(P), % Changed: domaining D and P
                         N = #count{ X,Y : district(X,Y,D), vote(X,Y,P) }.

% --- Determine District Winner (Majority Rule) ---
% Party P wins district D if it has strictly more votes than party 1-P.
district_winner(D,P) :- district_id(D), party_id(P), % Changed: domaining D and P
                        district_votes(D,P,N1),
                        district_votes(D,1-P,N2), % 1-P is safe as P is 0 or 1
                        N1 > N2.

% Handle ties: If votes are equal, assign winner to party 0 for consistency.
district_winner(D,0) :- district_id(D), % Changed: domaining D
                        party_id(0), % Explicitly stating P=0
                        district_votes(D,0,N_Party0), % Use distinct var names for clarity
                        district_votes(D,1,N_Party1),
                        N_Party0 == N_Party1. % Ensure it's a tie

% --- Count Representatives for the Target Party ---
% Count how many districts are won by the party_to_optimize.
representatives_for_optimized_party(N) :-
    N = #count{ D : district_id(D), district_winner(D,party_to_optimize) }.

% --- Optimization Goal ---
#maximize { N : representatives_for_optimized_party(N) }.

% --- Display Results ---
#show district/3.
#show district_winner/2.
#show representatives_for_optimized_party/1.