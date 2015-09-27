from multiAgents import *

def manhattanDist(point1, point2):
  "The Manhattan distance for two positions"
  x1 = point1[0]
  x2 = point2[0]
  y1 = point1[1]
  y2 = point2[0]
  return abs(x1 - x2) + abs(y1 - y2)
def nextAgent(agentIndex):
  numAgents = gameState.getNumAgents()
  if agentIndex + 1 == numAgents:
  	agentIndex = 0
  else:
  	agentIndex = agentIndex + 1
  return agentIndex

def maxValue(gameState, agentIndex):
  v = -93372036854775807
  legalActions = gameState.getLegalActions(agentIndex)
  for action in legalActions:
  	succState = gameState.generateSuccessor(agentIndex, action)
  	#agentIndex = nextAgent(agentIndex)
  	v = max(v, value(succState, agentIndex))
  return v

def maxValue(gameState, agentIndex):
  v = 93372036854775807
  legalActions = gameState.getLegalActions(agentIndex)
  for action in legalActions:
  	succState = gameState.generateSuccessor(agentIndex, action)
  	
  	v = min(v, value(succState, agentIndex))
  return v

def value(gameState, agentIndex):
  if gameState.isWin() or gameState.isLose():
  	return MinimaxAgent.evaluationFunction(gameState)
  legalActions = gameState.getLegalActions(agentIndex)
  agentIndex = nextAgent(agentIndex)
  if agentIndex == 0:
    return maxValue(gameState, agentIndex)
  else:
    return minValue(gameState, agentIndex)
  	
