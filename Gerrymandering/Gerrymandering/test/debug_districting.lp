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
% connected_in_district(X,Y,D) :- district(X,Y,D),
%                                 #count{ X2,Y2 : district(X2,Y2,D) } = 1.
% connected_in_district(X,Y,D) :- district(X,Y,D),
%                                 connected_in_district(X2,Y2,D),
%                                 adjacent(X,Y,X2,Y2).
% :- district(X,Y,D), not connected_in_district(X,Y,D).

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