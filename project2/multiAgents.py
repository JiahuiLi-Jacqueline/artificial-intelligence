# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)#getscore(): 4
    newPos = successorGameState.getPacmanPosition() #eg:(1,1)
    newFood = successorGameState.getFood()#bollen
    newGhostStates = successorGameState.getGhostStates()#[0]getPosition: (1,1)
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]#eg:[0]
    

    "*** YOUR CODE HERE ***"
    #print ("successorGameState", successorGameState.getScore())
   #print ("newPos", newPos)
    #print ("newfood", newFood.asList())
    #print ("newGhostStates", newGhostStates[0].getPosition())
    #print ("newScaredTimes", newScaredTimes)
    
    distanceToGhost = 0
    score = 0
    distance = 10000

    for food in currentGameState.getFood().asList():
      distanceToFood = manhattanDistance(newPos,food)
      if distanceToFood<distance:
        distanceToFood = manhattanDistance(newPos,food)

    for ghost in newGhostStates:
      if manhattanDistance(newPos,ghost.getPosition())==0:
        return -5000 ##worst case
      if manhattanDistance(newPos,ghost.getPosition())==1:
        return -distanceToFood-30
      else:
        distanceToGhost += manhattanDistance(newPos,ghost.getPosition())
    
    if distanceToFood == 0:
      distanceToFood = -50
    if distanceToFood ==1 :
      distanceToFood = -40

    if distanceToGhost>4 :
      distanceToGhost = 0 #when the ghost is far away, do not consider the ghost


    score =-distanceToFood+0.1*distanceToGhost
 
    return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    if gameState.isWin() or gameState.isLose() or self.depth == 0:
      return self.evaluationFunction(gamestate)

    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions(0)
    legalMoves.remove(Directions.STOP)

    # Choose one of the best actions
    scores = [self.minValue(gameState.generateSuccessor(0,action),1,self.depth) for action in legalMoves]
    #scores,action = self.max_value(gameState,self.depth) #sinnce paceman is agent 0 (max)
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
 
    return legalMoves[chosenIndex]

  def maxValue(self,gameState, agentIndex, depth):

    if(depth == 0) or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    v = -10000000
    legalActions = gameState.getLegalActions(0)
    for suc in (gameState.generateSuccessor(0, action) for action in legalActions):
      v = max(v, self.minValue(suc,1,depth))
    return v

  def minValue(self,gameState, agentIndex, depth):

    if(depth == 0) or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    v = 10000000
    numAgents = gameState.getNumAgents()
    legalActions = gameState.getLegalActions(agentIndex)
    for suc in (gameState.generateSuccessor(agentIndex, action) for action in legalActions):
      nextAgentIndex = (agentIndex+1)%numAgents
      if nextAgentIndex == 0:
        v = min(v, self.maxValue(suc,nextAgentIndex,depth-1))
      else:
        v = min(v, self.minValue(suc,nextAgentIndex,depth))
    return v


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  
  def getAction(self, gameState):
    a = -10000000
    b =  10000000
    if gameState.isWin() or gameState.isLose() or self.depth == 0:
      return self.evaluationFunction(gamestate)

    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions(0)
    legalMoves.remove(Directions.STOP)

    # Choose one of the best actions
    scores = [self.minValue(gameState.generateSuccessor(0,action),1,self.depth,a,b) for action in legalMoves]
    #scores,action = self.max_value(gameState,self.depth) #sinnce paceman is agent 0 (max)
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
 
    return legalMoves[chosenIndex]

  def maxValue(self,gameState, agentIndex,depth,a,b):

    if(depth == 0) or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    v = -10000000
    legalActions = gameState.getLegalActions(0)
    for suc in (gameState.generateSuccessor(0, action) for action in legalActions):
      v = max(v, self.minValue(suc,1,depth,a,b))
      a = max(a,v)
      if a>=b:
        return v
    return v

  def minValue(self,gameState, agentIndex, depth,a,b):

    if(depth == 0) or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    v = 10000000
    numAgents = gameState.getNumAgents()
    legalActions = gameState.getLegalActions(agentIndex)
    for suc in (gameState.generateSuccessor(agentIndex, action) for action in legalActions):
      nextAgentIndex = (agentIndex+1)%numAgents
      if nextAgentIndex == 0:
        v = min(v, self.maxValue(suc,nextAgentIndex,depth-1,a,b))
        b = min(b,v)
        if a>=b:
          return v
      else:
        v = min(v, self.minValue(suc,nextAgentIndex,depth,a,b))
        
    return v


  

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    if gameState.isWin() or gameState.isLose() or self.depth == 0:
      return self.evaluationFunction(gamestate)

    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions(0)
    legalMoves.remove(Directions.STOP)

    # Choose one of the best actions
    scores = [self.expValue(gameState.generateSuccessor(0,action),1,self.depth) for action in legalMoves]
    #scores,action = self.max_value(gameState,self.depth) #sinnce paceman is agent 0 (max)
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
 
    return legalMoves[chosenIndex]

  def maxValue(self,gameState, agentIndex, depth):

    if(depth == 0) or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    v = -10000000
    legalActions = gameState.getLegalActions(0)
    for suc in (gameState.generateSuccessor(0, action) for action in legalActions):
      v = max(v, self.expValue(suc,1,depth))
    return v

  def expValue(self,gameState, agentIndex, depth):
    

    if(depth == 0) or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)

    expectV = 0
    allV = []
    i = 0
    
    numAgents = gameState.getNumAgents()
    legalActions = gameState.getLegalActions(agentIndex)
    for suc in (gameState.generateSuccessor(agentIndex, action) for action in legalActions):
      nextAgentIndex = (agentIndex+1)%numAgents
      if nextAgentIndex == 0:
        v = self.maxValue(suc,nextAgentIndex,depth-1)

        allV.append(v)
        i = i+1
        expectV = sum(allV)/i
        
      else:
        v = self.expValue(suc,nextAgentIndex,depth)
        allV.append(v)
        i = i+1
        expectV = sum(allV)/i
        
    
    return expectV
    
  

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  
  pacmanPosition = currentGameState.getPacmanPosition() #eg:(1,1)
  foodPosition = currentGameState.getFood().asList() #list
  ghostStates = currentGameState.getGhostStates()#[0]getPosition: (1,1)
  ghostNumber = currentGameState.getNumAgents()-1  #worth -150
  foodNumber = currentGameState.getNumFood()   #worth -300
  capsulePosition = currentGameState.getCapsules()

  
  scores = 0
  distance = 1000000
  capsuleDistance = 1000000
  distanceToGhost = 0
  distanceToFood = 0
  distanceToCapsule = 0

  if currentGameState.isWin():
    scores =  10000000
  if currentGameState.isLose():
    scores = -10000000

  scores = ghostNumber*(-10)+foodNumber*(-300)+len(capsulePosition)*(-400)

  for food in foodPosition:
    distanceToFood = manhattanDistance(pacmanPosition,food)
    if distanceToFood < distance:
      #print(distanceToFood)
      distanceToFood = manhattanDistance(pacmanPosition,food)   # find the nearest distance to food
      distance = distanceToFood

  for ghost in ghostStates: 
    if ghost.scaredTimer == 0:
      if manhattanDistance(pacmanPosition,ghost.getPosition())== 0:
        return -10000000
      if manhattanDistance(pacmanPosition,ghost.getPosition()) == 1:
        return scores-distanceToFood-30
      else:
        distanceToGhost = distanceToGhost+manhattanDistance(pacmanPosition,ghost.getPosition())

    ###no use
    #if scaredTimes == 1:
      #if manhattanDistance(pacmanPosition,ghost.getPosition())== 1:
        #scores = scores-20
  for capsule in capsulePosition:
    distanceToCapsule = manhattanDistance(pacmanPosition,capsule)
    #print(distanceToCapsule)
    if distanceToCapsule < capsuleDistance:
      distanceToCapsule = manhattanDistance(pacmanPosition,capsule)   # find the nearest distance to food
      capsuleDistance = distanceToCapsule
      
  if distanceToFood == 0:
    distanceToFood = -50

  if distanceToFood == 1:
    distanceToFood = -40

  #when the ghost is far away, do not consider the ghost
  if distanceToGhost > 4 :
    distanceToGhost = 0 

  if distanceToCapsule == 0: # comapre to food, prefer capsule
    distanceToCapsule = -50

  if distanceToCapsule == 1 :
    distanceToCapsule = -40

  scores = scores - distanceToFood + 0.1*distanceToGhost-2*distanceToCapsule

  return scores


# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

