from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide. You are welcome to change
      it in any way you see fit, so long as you don't touch the method
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        score = 0


        if newScaredTimes > 0:
            for ghosts in newGhostStates:
                if manhattanDistance(newPos, ghosts.getPosition()) <= 1:
                    score -= 470000

        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 100

        x, y = newPos
        if(newFood[x][y] == False):
            score -= 100


        if action == Directions.STOP:
            score -= 50
        """for ghost.getGhostPosition in newGhostStates:
            if newPos == ghost:
                score -= 100"""
        "*** YOUR CODE HERE ***"
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
      add functionality to all your adversarial search agents. Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended. Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        bestPlay = self.value(gameState, self.index, self.depth)

        return bestPlay[1]
        

    def value(self, state, index, depth):
        if depth == 0 or state.isWin() or state.isLose():
            return (self.evaluationFunction(state))
        elif index == 0:
            return(self.max(state, index, depth))
        else:
            return(self.mini(state, index, depth))

    def mini(self, state, index, depth):
        v = (float("inf"), None)
        numberOfGhost = state.getNumAgents()-1
        legalActions = state.getLegalActions(index)
        if index == numberOfGhost:
            for action in legalActions:
                comparedAction = state.generateSuccessor(index, action)
                temp = self.value(comparedAction,0, depth-1)
                if temp < v[0]:
                    v = (temp, action)
                    print v[0]
        else:
            for action in legalActions:
                comparedAction = state.generateSuccessor(index, action)
                temp = self.value(comparedAction,index+1, depth)
                if temp < v[0]:
                    v = (temp, action)
                    print v[0]
        return v

    def max(self, state, index, depth):
        v = float("-inf"), None
        legalActions = state.getLegalActions(self.index)
        for action in legalActions:
            comparedAction = state.generateSuccessor(index, action)
            temp = self.value(comparedAction,index+1, depth)
            if temp > v[0]:
                v = (temp, action)
                print v[0]

        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestPlay = self.value(gameState, self.index, self.depth, float("-inf"), float("inf"))

        return bestPlay[1]


    def value(self, state, index, depth, alpha, beta):
        if depth == 0 or state.isWin() or state.isLose():
            return (self.evaluationFunction(state))
        elif index == 0:
            return(self.max(state, index, depth,alpha, beta))
        else:
            return(self.mini(state, index, depth, alpha, beta))

    def mini(self, state, index, depth, alpha, beta):
        v = (float("inf"), None)
        numberOfGhost = state.getNumAgents()-1
        legalActions = state.getLegalActions(index)
        if index == numberOfGhost:
            for action in legalActions:
                comparedAction = state.generateSuccessor(index, action)
                temp = self.value(comparedAction,0, depth-1, alpha, beta)
                if temp < v[0]:
                    v = (temp, action)
                    print v[0]
                if v[0] < alpha:
                    return v
                beta = min(beta, v[0])
        else:
            for action in legalActions:
                comparedAction = state.generateSuccessor(index, action)
                temp = self.value(comparedAction,index+1, depth, alpha, beta)
                if temp < v[0]:
                    v = (temp, action)
                    print v[0]
                if v[0] < alpha:
                    return v
                beta = min(beta, v[0])
        return v

    def max(self, state, index, depth, alpha, beta):
        v = float("-inf"), None
        legalActions = state.getLegalActions(self.index)
        for action in legalActions:
            comparedAction = state.generateSuccessor(index, action)
            temp = self.value(comparedAction,index+1, depth, alpha, beta)
            if temp > v[0]:
                v = (temp, action)
                print v[0]
            if v[0] > beta:
                return v
            alpha = max(alpha, v[0])

        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestPlay = self.value(gameState,self.index,self.depth)
        return bestPlay[1]

    def value(self, state, index, depth):
        if depth == 0 or state.isWin() or state.isLose():
            notAFloatValue = self.evaluationFunction(state)
            makeAFloatValue = float(notAFloatValue)
            return(makeAFloatValue,None)
        elif index == 0:
            return(self.max(state, index, depth))
        else:
            return(self.exp(state, index, depth))

    def exp(self, state, index, depth):
        v = 0.0, None
        numberOfGhost = state.getNumAgents()-1
        legalActions = state.getLegalActions(index)
        length = len(legalActions)
        p = 1.0/float(length)

        if index == numberOfGhost:
            for action in legalActions:
                comparedAction = state.generateSuccessor(index, action)
                temp = self.value(comparedAction,0, depth-1)

                score = temp[0]
                probabillity = (score * p)
                v = (probabillity, action)
        else:
            for action in legalActions:
                comparedAction = state.generateSuccessor(index, action)
                temp = self.value(comparedAction,0, depth-1)

                score = temp[0]
                probabillity = (score * p)
                v = (probabillity, action)
        print v
        return v

    def max(self, state, index, depth):
        v = float("-inf"), None
        legalActions = state.getLegalActions(self.index)
        for action in legalActions:
            comparedAction = state.generateSuccessor(index, action)
            temp = self.value(comparedAction,index+1, depth)
            if temp[0] > v[0]:
                v = (temp[0], action)
                #print v[0]

        return v



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function.

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = currentGameState.getScore()
    nearestFood = float("inf")
    for food in newFood.asList():
        temp = manhattanDistance(food, newPos)
        if temp < nearestFood:
            nearestFood = temp
    score += 4.0/(nearestFood+1)

    for ghosts in newGhostStates:
        distance = float(manhattanDistance(newPos, ghosts.getPosition()))
        if distance <= 6:
            score -= 10.0/(distance+1)









        """for ghost.getGhostPosition in newGhostStates:
            if newPos == ghost:
                score -= 100"""
        "*** YOUR CODE HERE ***"
    return score



# Abbreviation
better = betterEvaluationFunction

