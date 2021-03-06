# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
from game import Directions
import ghostAgents
import random, util
from mypy import *
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
  def manhattanDist(self, p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])
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
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    "TODO: make sure it's not too close to the ghost"
    "make sure it keeps eating all the food... and do not stop if the food is close"
    from searchAgents import mazeDistance

    
    "not too close to the ghosts"
    "get ALL the food"
    "get to the closest food and EAT it"
    allFood = currentGameState.getFood().asList()
    foodDistance = []
    ans = successorGameState.getScore()
    for dot in allFood:
        # distance = mazeDistance(newPos, dot, currentGameState)
        distance = self.manhattanDist(newPos, dot)
        item = (dot, distance)
        foodDistance.append(item)

    #check ALL ghosts
    numAgents = successorGameState.getNumAgents()
    allGhostPositions = []
    if numAgents==2:
      #ghostDistance = mazeDistance(newPos, successorGameState.getGhostPosition(1), successorGameState)
      ghostDistance = self.manhattanDist(newPos, successorGameState.getGhostPosition(1))
      if ghostDistance<3:
        ans = ans - (3-ghostDistance)*100000
    #for more than one ghost  
    if numAgents>2:
      for x in range(1, numAgents):
        ghostNewPos = successorGameState.getGhostPosition(x)
        allGhostPositions.append(ghostNewPos)
      for eachGhost in allGhostPositions:
        ghostDistance = self.manhattanDist(newPos, eachGhost)
        if ghostDistance<3:
          ans = ans - (3-ghostDistance)*100000
    
    if len(foodDistance)>0:
      #ans = max(result, key = lambda x: x[0])
      closestFood = min(foodDistance, key = lambda x: x[1])
      ans = ans - closestFood[1]
    if newPos in allFood:
      ans = ans + 10000
    return ans

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
  def manhattanDist(point1, point2):
    "The Manhattan distance for two positions"
    x1 = float(point1[0])
    x2 = float(point2[0])
    y1 = float(point1[1])
    y2 = float(point2[0])
    return abs(x1 - x2) + abs(y1 - y2)
  def nextAgent(self, gameState, agentIndex, depth):
    numAgents = gameState.getNumAgents()
    if agentIndex + 1 == numAgents:
      agentIndex = 0
      depth = self.nextDepth(depth)
    else:
      agentIndex = agentIndex + 1
    return agentIndex, depth

  def nextDepth(self, depth):
    if depth < self.depth:
      depth = depth+1
    return depth
  def maxValue(self, gameState, agentIndex, depth):
    v = -93372036854775807
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    for action in legalActions:
      succState = gameState.generateSuccessor(agentIndex, action)
      #agentIndex = nextAgent(agentIndex)
      v = max(v, self.value(succState, agentIndex, depth))
    return v

  def minValue(self, gameState, agentIndex, depth):
    v = 93372036854775807
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    for action in legalActions:
      succState = gameState.generateSuccessor(agentIndex, action)
      v = min(v, self.value(succState, agentIndex, depth))
    return v

  def value(self, gameState, agentIndex, depth):
    # if gameState.isWin() or gameState.isLose():
    if depth == self.depth:
      return self.evaluationFunction(gameState)
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    agentIndex, depth = self.nextAgent(gameState, agentIndex, depth)
    if agentIndex == 0:
      return self.maxValue(gameState, agentIndex, depth)
    else:
      return self.minValue(gameState, agentIndex, depth)
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    agentIndex = 0
    result = []
    depth = 0
    allActions = gameState.getLegalActions(agentIndex)
    if 'Stop' in allActions:
      allActions.remove('Stop')
    #we need to add actions here, so do the first iteration here.
    for action in allActions:
      successorState = gameState.generateSuccessor(agentIndex, action)
      eachResult = (self.value(successorState, agentIndex, depth), action)
      result.append(eachResult)
    ans = max(result, key = lambda x: x[0])
    return ans[1]
    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  def nextAgent(self, gameState, agentIndex, depth):
    numAgents = gameState.getNumAgents()
    if agentIndex + 1 == numAgents:
      agentIndex = 0
      depth = self.nextDepth(depth)
    else:
      agentIndex = agentIndex + 1
    return agentIndex, depth

  def nextDepth(self, depth):
    if depth < self.depth:
      depth = depth+1
    return depth
  def maxValue(self, gameState, alpha, beta, agentIndex, depth):
    v = -93372036854775807
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    for action in legalActions:
      succState = gameState.generateSuccessor(agentIndex, action)
      v = max(v, self.value(succState, alpha, beta, agentIndex, depth))
      if v>= beta:
        return v
      alpha = max(alpha, v)
    return v

  def minValue(self, gameState, alpha, beta, agentIndex, depth):
    v = 93372036854775807
    legalActions = gameState.getLegalActions(agentIndex)
    #terminal state
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    
    for action in legalActions:
      succState = gameState.generateSuccessor(agentIndex, action)
      v = min(v, self.value(succState, alpha, beta, agentIndex, depth))
      if v <= alpha:
        return v
      beta = min(beta, v)
    return v

  def value(self, gameState, alpha, beta, agentIndex, depth):
    if depth == self.depth:
      return self.evaluationFunction(gameState)
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    agentIndex, depth = self.nextAgent(gameState, agentIndex, depth)
    if agentIndex == 0:
      return self.maxValue(gameState, alpha, beta, agentIndex, depth)
    else:
      return self.minValue(gameState, alpha, beta, agentIndex, depth)
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    agentIndex = 0
    result = []
    depth = 0
    allActions = gameState.getLegalActions(agentIndex)
    #define alpha and beta first
    alpha = gameState #MAX best option on path to root
    beta = gameState #MIN best option: need to calculate here, since we only need the first one (the first ghost), we only get the first best beta
    findBeta = []
    if 'Stop' in allActions:
      allActions.remove('Stop')
    for action in allActions:
      successorState = gameState.generateSuccessor(agentIndex, action)
      evalResult = self.evaluationFunction(successorState)
      item = (evalResult, successorState)
      findBeta.append(item)
    beta = min(findBeta, key = lambda x: x[0])
    #now call the minimax algorithm

    for action in allActions:
      successorState = gameState.generateSuccessor(agentIndex, action)
      eachResult = (self.value(successorState, alpha, beta, agentIndex, depth), action)
      result.append(eachResult)
    ans = max(result, key = lambda x: x[0])
    return ans[1]
    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  #import ghostAgents does not seem to work so I copied the code here
  def getRandomGhostDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist
  def nextAgent(self, gameState, agentIndex, depth):
    numAgents = gameState.getNumAgents()
    if agentIndex + 1 == numAgents:
      agentIndex = 0
      depth = self.nextDepth(depth)
    else:
      agentIndex = agentIndex + 1
    return agentIndex, depth

  def nextDepth(self, depth):
    if depth < self.depth:
      depth = depth+1
    return depth
  def maxValue(self, gameState, agentIndex, depth):
    v = -93372036854775807
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    for action in legalActions:
      succState = gameState.generateSuccessor(agentIndex, action)
      v = max(v, self.value(succState, agentIndex, depth))
    return v

  def expValue(self, gameState, agentIndex, depth):
    
    v = 0
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    for action in legalActions:
      succState = gameState.generateSuccessor(agentIndex, action)
      v = v + self.value(succState, agentIndex, depth)
      distribution = self.getRandomGhostDistribution(succState)
    return v

  def value(self, gameState, agentIndex, depth):
    # if gameState.isWin() or gameState.isLose():
    if depth == self.depth:
      return self.evaluationFunction(gameState)
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions)==0:
      return self.evaluationFunction(gameState)
    agentIndex, depth = self.nextAgent(gameState, agentIndex, depth)
    if agentIndex == 0:
      return self.maxValue(gameState, agentIndex, depth)
    else:
      return self.expValue(gameState, agentIndex, depth)
  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    agentIndex = 0
    result = []
    depth = 0
    allActions = gameState.getLegalActions(agentIndex)
    if 'Stop' in allActions:
      allActions.remove('Stop')
    #we need to add actions here, so do the first iteration here.
    for action in allActions:
      successorState = gameState.generateSuccessor(agentIndex, action)
      eachResult = (self.value(successorState, agentIndex, depth), action)
      result.append(eachResult)
    ans = max(result, key = lambda x: x[0])
    return ans[1]
    util.raiseNotDefined()

def manhattanDist(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])
def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  "need to get the successor game state...?"
  from searchAgents import mazeDistance
  ans = currentGameState.getScore()
  currentPos = currentGameState.getPacmanPosition()
  allFood = currentGameState.getFood().asList()
  foodDistance = []
  for dot in allFood:
    distance = manhattanDist(currentPos, dot)
    item = (dot, distance)
    foodDistance.append(item)

  numAgents = currentGameState.getNumAgents()
  allGhostPositions = []
  if numAgents==2:
    #ghostDistance = mazeDistance(newPos, successorGameState.getGhostPosition(1), successorGameState)
    ghostDistance = manhattanDist(newPos, currentGameState.getGhostPosition(1))
    if ghostDistance<3:
      ans = ans - (3-ghostDistance)*100000
  #for more than one ghost  
  if numAgents>2:
    for x in range(1, numAgents):
      ghostPos = currentGameState.getGhostPosition(x)
      allGhostPositions.append(ghostPos)
    for eachGhost in allGhostPositions:
      ghostDistance = manhattanDist(currentPos, eachGhost)
      if ghostDistance<3:
        ans = ans - (3-ghostDistance)*100000
  
  if len(foodDistance)>0:
    #ans = max(result, key = lambda x: x[0])
    closestFood = min(foodDistance, key = lambda x: x[1])
    ans = ans - closestFood[1]
  if currentPos in allFood:
    ans = ans + 10000
  return ans




  util.raiseNotDefined()
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

