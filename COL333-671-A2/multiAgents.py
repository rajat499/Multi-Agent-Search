# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def man_dist (self,x,y):
        return (abs(x[0]-y[0]) + abs(x[1]-y[1]))

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
        score = successorGameState.getScore()
        newFood = newFood.asList()

        if len(newFood) == 0:
            return score + 10000
        
        OldPellets = currentGameState.getCapsules()
        NewPellets = successorGameState.getCapsules()

        if len(OldPellets)-len(NewPellets) == 1:
            return score + 10000

        ghost_arr = []; food_arr = []
        for elem in newGhostStates:
            ghost_pos = elem.getPosition()
            dist = self.man_dist(newPos,ghost_pos)
            if dist < 2:
                return score - 100000
            ghost_arr.append(dist)

        for food_pos in newFood:
            dist = self.man_dist(newPos,food_pos)
            food_arr.append(dist)

        for item in NewPellets:
            dist = self.man_dist(newPos, item)
            food_arr.append(dist)

        if (len(ghost_arr) != 0 and len(food_arr) != 0):
            if min(food_arr) != 0:
                # score += (min(ghost_arr)/min(food_arr))
                score += (1/min(food_arr))
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # print(gameState.getLegalActions(0))
        # return gameState.getLegalActions(0)
        def calc(gameState,depth,id):
            if ((depth == self.depth) or (gameState.getLegalActions(id) == 0) or (gameState.isWin()) or (gameState.isLose())):
                return (self.evaluationFunction(gameState),None)
            neg_inf = -10000; pos_inf = 10000; 
            best_max = neg_inf; best_min = pos_inf
            if (id == 0):
                for elem in gameState.getLegalActions(id):
                    n = (id+1) % gameState.getNumAgents()
                    (value,move) = calc(gameState.generateSuccessor(id,elem),depth,n)
                    if (value > best_max):
                        best_max = value
                        max_move = elem
            if best_max != neg_inf:
                return (best_max,max_move)

            if (id != 0):
                for elem in gameState.getLegalActions(id):
                    n = (id+1) % gameState.getNumAgents()
                    if n != 0:
                        (value,move) = calc(gameState.generateSuccessor(id,elem),depth,n)
                    else:
                        (value,move) = calc(gameState.generateSuccessor(id,elem),depth+1,n)
                    if (value<best_min):
                        best_min = value
                        min_move = move
            if best_min != pos_inf:
                return (best_min,min_move)
       
        move = calc(gameState,0,0)[1]
        return move

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def calc(gameState,depth,id,alpha,beta):
            if ((depth == self.depth) or (gameState.getLegalActions(id) == 0) or (gameState.isWin()) or (gameState.isLose())):
                return (self.evaluationFunction(gameState),None)
            neg_inf = -10000; pos_inf = 10000; 
            best_max = neg_inf; best_min = pos_inf
            if (id == 0):
                for elem in gameState.getLegalActions(id):
                    n = (id+1) % gameState.getNumAgents()
                    (value,move) = calc(gameState.generateSuccessor(id,elem),depth,n,alpha,beta)
                    if (value > best_max):
                        best_max = value
                        max_move = elem
                    if best_max > beta:
                        return (best_max,max_move)
                    alpha = max(alpha,best_max)

            if best_max != neg_inf:
                return (best_max,max_move)

            if (id != 0):
                for elem in gameState.getLegalActions(id):
                    n = (id+1) % gameState.getNumAgents()
                    if n != 0:
                        (value,move) = calc(gameState.generateSuccessor(id,elem),depth,n,alpha,beta)
                    else:
                        (value,move) = calc(gameState.generateSuccessor(id,elem),depth+1,n,alpha,beta)
                    if (value<best_min):
                        best_min = value
                        min_move = move
                    if best_min < alpha:
                        return (best_min,min_move)
                    beta = min(beta,best_min)

            if best_min != pos_inf:
                return (best_min,min_move)

        move = calc(gameState,0,0,-10000,10000)[1]
        # print("best val = ",value);print("best move = ",move)
        return move
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def calc(gameState,depth,id):
            if ((depth == self.depth) or (gameState.getLegalActions(id) == 0) or (gameState.isWin()) or (gameState.isLose())):
                return (self.evaluationFunction(gameState),None)
            neg_inf = -10000; pos_inf = 10000; 
            best_max = neg_inf
            if (id == 0):
                for elem in gameState.getLegalActions(id):
                    n = (id+1) % gameState.getNumAgents()
                    (value,move) = calc(gameState.generateSuccessor(id,elem),depth,n)
                    if (value > best_max):
                        best_max = value
                        max_move = elem
            if best_max != neg_inf:
                return (best_max,max_move)

            total = []
            if (id != 0):
                for elem in gameState.getLegalActions(id):
                    n = (id+1) % gameState.getNumAgents()
                    if n != 0:
                        (value,move) = calc(gameState.generateSuccessor(id,elem),depth,n)
                    else:
                        (value,move) = calc(gameState.generateSuccessor(id,elem),depth+1,n)
                    total.append(value)
                    min_move = elem
            if len(total) != 0:
                return (sum(total)/len(total),min_move)
       
        move = calc(gameState,0,0)[1]
        # print("best val = ",value);print("best move = ",move)
        return move

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    def man_dist (x,y):
        return (abs(x[0]-y[0]) + abs(x[1]-y[1]))
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    pellets = currentGameState.getCapsules()
    score = currentGameState.getScore()
    
    f1 = 10; f2 = 5; f3 = 250
    
    ghost_arr = [];food_arr = []
    
    for elem in newGhostStates:
        ghost_pos = elem.getPosition()
        dist = man_dist(newPos,ghost_pos)
        ghost_arr.append(dist)
        if dist > 0:
            if elem.scaredTimer > 0:
                score += f3/dist
            else:
                score -= f2/dist
    
    for food_pos in newFood.asList():
        dist = man_dist(newPos,food_pos)
        food_arr.append(dist)
    
    for item in pellets:
        dist = man_dist(newPos,item)
        food_arr.append(dist)

    if len(food_arr) != 0:
        if min(food_arr) != 0:
            score += f1/min(food_arr)
    return score




# Abbreviation
better = betterEvaluationFunction
