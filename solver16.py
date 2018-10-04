#!/usr/bin/env python3
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#Updated by Justin, Satya, Abhinav 2018

#INITIAL STATE:
#The input file is the initial state

#GOAL STATE:
#All the 16 numbers must be aranged in four rows in ascending order

#STATE SPACE:
#Fringe consists of states which are produced by moving a particular row or column of the parent board to either left or right
#For any board, total 16 states will be generated

#======================================================HEURISTIC FUNCTIONS:========================================================
#We have tried the below heuristic functions

#1) Since we are considering the 16 puzzle as a tuple,We found the distance of the misplaced element from its original position and adding
# all distances in a particular successor. If this sum is less than that of the sum obtained for the parent board, we have returnedthis board.
# Otherwise, we have ignored this. Though this heuristic is not admissible, it worked really well till board 16
# <Number of Ordered Rows and Columns>
# In order for the puzzle to reach a goal, both rows and columns needed to be ordered. We compared each row and column if they are ordered
# and returned the number of mismatched rows and columns for the heuristic.
#
#
# 2)<Misplaced Tiles for First Row and Column>
# By examining row shifts and column shifts, we felt that first row and first column plays a major role to the goal state. We calculated number of 
# misplaced tiles in the first row and first column.
#
# 
# 3)<34 Rule> 
# http://mathworld.wolfram.com/DuerersMagicSquare.html
# http://jwilson.coe.uga.edu/EMT668/EMAT6680.2002/Nooney/EMAT6600-ProblemSolving/AssignmentPages-EMAT6600/MagicSquare(4x4).html
# We were able to meet this 34 property, which the sums of diagonal entries are 34 and sum of inner entries (2,2), (2,3), (3,2), (3,3) are 34. 
# We regarded something far from 34 is away from the goal state, so we calculated the absolute difference of the 3 sums of the current board and
# calculated 1) mean, 2) maximum difference etc.
#
# 
# 4)<Different loops of manhatten distance>
#
# We kept getting memory error, so we decided to utilize the most out of PriorityQueue. We made 2 to 3 loops of successor function and stored in 
# the the open fridge and popped the board with the least Manhatten distance, which implies closer to the goal board.
#
# 
# 5)<Triangle Rotation>
# https://pdfs.semanticscholar.org/66c1/46fd2ed05cfaba26b4c28c25c3c2bfba2bfe.pdf
# After reading this journal, we tried to apply three element rotation for the solution. However, we found out that this is mathematical approach 
# rather than computer science apporach and felt that it would be difficult to implement this as heuristic.
# 
# 
# 6)<The number of matching rows and columns with sums compared to the goal state>
# Calculated the sum of each row and column and returned the counts of rows and columns of that matches the sum of the goal state.
#
#WE HAVE IMPLEMENTED MODIFIED MANHATTEN WHICH IS EXPLAINED BELOW

from queue import PriorityQueue
import sys
# shift a specified row left (-1) or right (1)
def shift_row(state, row, dir):
    change_row = state[(row * 4):(row * 4 + 4)]
    return (state[:(row * 4)] + change_row[-dir:] + change_row[:-dir] + state[(row * 4 + 4):],
            ("L" if dir == -1 else "R") + str(row + 1))


# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col + 1))


# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print
        '%3d %3d %3d %3d' % (row[j:(j + 4)])

#################################### MODIFIED MANHATTEN ##################################
#We have seggregated the rows and columns of a particular state. then we calculated the manhattan 
#distance and took the minimum of (that diatance and absolute value of (4-that distance)). Since we 
#can move the rows and columns in both left and right direction, the element which is present in the 
#same row and has a manhatten distance of 3 can be moved to its right position in just one move according
#to our successor function. So our heuristic function takes care of this. To make it admissible, we divided
# the final heuristic value with 4. So, our heuristic function is now admissible
def heuristic(board):
    dict_row = dict()
    dict_col = dict()
    count = 0
    for i in range(1,17):
        ith = i//4
        if i%4:
            dict_row[i]=ith
        else:
            dict_row[i]=ith-1

        dict_col[i]=count
        count+=1
        if count>3:
            count=0


    row1=board[0:4]
    row2=board[4:8]
    row3=board[8:12]
    row4=board[12:16]
    col1=board[0::4]
    col2=board[1::4]
    col3=board[2::4]
    col4=board[3::4]

    row_distances = {}
    col_distances = {}
    rows=[row1,row2,row3,row4]
    cols=[col1,col2,col3,col4]

    for row in rows:
        for i in range(0,len(row)):
            rowi = rows.index(row)
            elem = row[i]
            temp_dist = abs(dict_row[elem]-rowi)
            row_distances[elem]= min(temp_dist, abs(4-temp_dist))

    for row in rows:
        for i in range(0,len(row)):
            elem = row[i]
            temp_dist = abs(dict_col[elem]-i)
            col_distances[elem]=min(temp_dist, abs(4-temp_dist))

    modified_manhattan = {}

    for i in range(1,17):
        modified_manhattan[i]= row_distances[i]+col_distances[i]

    heuristic_value = sum(list(modified_manhattan.values()))/4
    return heuristic_value



# return a list of possible successor states
def successors(state,route_so_far):
    initial_count=0
    a=[]
    for d in (1,-1):
        for i in range(0,4):
            a.append(shift_row(state,i,d))
            
    heuristic_a=[]        
    for board in a:
        heuristic_a.append(heuristic(board[0]))
        
    list1=[]
    for i in range(len(a)):
        list1.append(list(a[i]))
    
    for item in list1:
        item[1]=route_so_far+item[1]
    
    
    
    for i in range(len(a)):
        
        intital_count = len(list(list1[i][1]))/2
        list1[i].insert(0,heuristic_a[i]+initial_count)
    
    b=[]
    for d in (1,-1):
        for i in range(0,4):
            b.append(shift_col(state,i,d))
            
    heuristic_b=[]        
    for board in b:
        heuristic_b.append(heuristic(board[0]))
        
    list2=[]
    for i in range(len(b)):
        list2.append(list(b[i]))

    for item in list2:
        item[1]=route_so_far+item[1]
        
    for i in range(len(b)):
        intital_count = len(list(list2[i][1]))/2
        list2[i].insert(0,heuristic_b[i]+initial_count)
    
            
    final_list = list1+list2
    
    for i in final_list:
        if i[1] in CLOSED:
            final_list.remove(i)
    return final_list


# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)


def solve(initial_board):

    fringe1 = [(1, initial_board, "")]
    fringe_q = PriorityQueue()
    for i in fringe1:
        fringe_q.put(i)
        
    global CLOSED    
    CLOSED=[]
    MOVE=[]
    Final_route=[]
    ROUTE=[]
    while fringe_q.empty()==False:

        (cost, state, route_so_far) = fringe_q.get()
        CLOSED.append(state)
        
        for (cost, succ, move) in successors(state, route_so_far):
            MOVE.append(move)
            if is_goal(succ):
                Final_route.append(MOVE[-1].split())
                return(Final_route[0][-1])
            ROUTE.append(MOVE[-1].split())
            
            if len(ROUTE[0][-1])//2 >= 12:
                continue
            elif succ not in CLOSED:
                fringe_q.put((cost,succ, route_so_far + " " + move))
            else:
                continue
    return False


# test cases
start_state = []
input_file=sys.argv[1]
with open(input_file) as file:
    for line in file:
        start_state += [int(i) for i in line.split()]

if len(start_state) != 16:
    print("Error: couldn't parse start state file")

#print("Start state: ")
#print_board(tuple(start_state))

#print("Solving...")
route = solve(tuple(start_state))

#print("Solution found in " + str(len(route)//2) + " moves:" + "\n")
for i in range(len(route)):
    print(route[i],end="")
    if i%2!=0:print(end=" ")


