# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"


    fringeNode = util.Stack()
    nodeExpanded = []
    
    #print('path',path.list)
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
   

    #######start
    startState = problem.getStartState()# coordinate
    currentState = startState #
    path = [] #direction
    fringeNode.push((startState,path,[]))

    while not fringeNode.isEmpty():
          
        if not problem.isGoalState(currentState):
            
            if currentState not in nodeExpanded:

                #if len(problem.getSuccessors(currentState)) :

                    currentChildren = problem.getSuccessors(currentState) #expanding
                    nodeExpanded.append(currentState) 
        
                    for i in currentChildren[::-1]: #reverse order                     
                        if i[0] not in nodeExpanded:
                            tempPath = i[1]
                            fringeNode.push((i[0], path+[tempPath],i[2]) )

            currentState,path,cost= fringeNode.pop() 
            #print("currentState",currentState)
        else:
            
            return path             

    util.raiseNotDefined()       


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"

    #######start
    fringeNode = util.Queue()
    nodeExpanded = []

    startState = problem.getStartState()# coordinate
    currentState = startState #
    path = [] #direction
    fringeNode.push((startState,path,[]))

    while not fringeNode.isEmpty():
          
        if not problem.isGoalState(currentState):
            currentState,path,cost= fringeNode.pop() 
            if currentState not in nodeExpanded:

                #if len(problem.getSuccessors(currentState)) :

                    currentChildren = problem.getSuccessors(currentState) #expanding
                    nodeExpanded.append(currentState) 
        
                    for i in currentChildren[::-1]: #reverse order                     
                        if i[0] not in nodeExpanded:
                            tempPath = i[1]
                            fringeNode.push((i[0], path+[tempPath],i[2]) )

            
            #print("currentState",currentState)
        else:
            
            return path             

    util.raiseNotDefined()       



def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    #######start
    fringeNode = util.PriorityQueue()
    nodeExpanded = []

    startState = problem.getStartState()# coordinate
    currentState = startState #
    path = [] #direction
    cost = 0
    fringeNode.push((startState,path,cost),cost)

    while not fringeNode.isEmpty():
          
        if not problem.isGoalState(currentState):
            
            currentState,path,cost= fringeNode.pop() 
            if currentState not in nodeExpanded:

                #if len(problem.getSuccessors(currentState)) :

                    currentChildren = problem.getSuccessors(currentState) #expanding
                    nodeExpanded.append(currentState) 
        
                    for i in currentChildren[::-1]: #reverse order                     
                        if i[0] not in nodeExpanded:
                            tempPath = i[1]
                            tempCost = i[2]
                            #cost = cost + i[2]
                            #print cost
                            fringeNode.push((i[0], path+[tempPath],cost+tempCost),cost+tempCost)

            
            #print("currentState",currentState)
        else:
            
            return path             

    util.raiseNotDefined()       



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    #######start

    fringeNode = util.PriorityQueue()
    nodeExpanded = []

    startState = problem.getStartState()# coordinate
    currentState = startState #
    path = [] #direction
    cost_g = 0
    cost_h  = heuristic(currentState, problem)
    #print 'co
    cost = cost_h+cost_g
    fringeNode.push((startState,path,cost_g),cost)

    while not fringeNode.isEmpty():
        
        if not problem.isGoalState(currentState):

            currentState,path,cost_g = fringeNode.pop() 

            if currentState not in nodeExpanded:
                    
                #if len(problem.getSuccessors(currentState)) :

                    currentChildren = problem.getSuccessors(currentState) #expanding
                    nodeExpanded.append(currentState) 
        
                    for i in currentChildren[::-1]: #reverse order                     
                        if i[0] not in nodeExpanded:
                            tempPath = i[1]
                            tempCost = i[2]
                            #cost_g = cost_g + i[2]
                            cost_h  = heuristic(i[0], problem)

                            fringeNode.push((i[0], path+[tempPath],cost_g+tempCost),cost_g+tempCost+cost_h)
    
        else:
            #print 'currentstate', currentState
            return path             


    util.raiseNotDefined()






# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
