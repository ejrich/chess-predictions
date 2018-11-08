import os
from flask import Flask, g, request, jsonify
from flask_cors import CORS
from sklearn.externals import joblib

app = Flask(__name__)
CORS(app)

linearRegression = joblib.load(os.path.join(os.path.dirname(__file__), '../models/201801_linear_regression.joblib'))
logisticRegression = joblib.load(os.path.join(os.path.dirname(__file__), '../models/201801_logistic_regression.joblib'))
randomForestRegression = joblib.load(os.path.join(os.path.dirname(__file__), '../models/201801_random_forest_regression.joblib'))

pieces = ['P', 'B', 'R', 'N', 'Q', 'K']

def makeLinearPrediction(gameState):
    prediction = linearRegression.predict([gameState])
    return prediction[0]

def makeLogisticPrediction(gameState):
    prediction = logisticRegression.predict([gameState])
    return prediction[0]

def makeRandomForestPrediction(gameState):
    prediction = randomForestRegression.predict([gameState])
    return prediction[0]

def translateGameState(gameState):
    translation = []

    translation.append(int(gameState['WhitePawns']))
    translation.append(int(gameState['BlackPawns']))
    translation.append(int(gameState['WhiteRooks']))
    translation.append(int(gameState['BlackRooks']))
    translation.append(int(gameState['WhiteBishops']))
    translation.append(int(gameState['BlackBishops']))
    translation.append(int(gameState['WhiteKnights']))
    translation.append(int(gameState['BlackKnights']))
    translation.append(int(gameState['WhiteQueen']))
    translation.append(int(gameState['BlackQueen']))
    translation.append(int(gameState['WhiteKing']))
    translation.append(int(gameState['BlackKing']))
    translation.append(int(gameState['WhiteTotal']))
    translation.append(int(gameState['BlackTotal']))

    for rank in range(1, 9):
        for file in range(ord('a'), ord('h') + 1):
            id = chr(file) + str(rank)

            colors = [1, 0] if gameState[id + '_color'] == 1 else [0, 1] if gameState[id + '_color'] == 2 else [0, 0]
            translation += colors

            pieceCategories = [0, 0, 0, 0, 0, 0]
            piece = pieces.index(gameState[id + '_piece']) if gameState[id + '_piece'] else None
            if piece != None:
                pieceCategories[piece] = 1

            translation += pieceCategories

    return translation

@app.route('/prediction/linear', methods=['POST'])
def linearPrediction():
    gameState = request.json

    translation = translateGameState(gameState)

    predictionValue = makeLinearPrediction(translation)

    return jsonify({ 'prediction': predictionValue })

@app.route('/prediction/logistic', methods=['POST'])
def logisticPrediction():
    gameState = request.json

    translation = translateGameState(gameState)

    predictionValue = makeLogisticPrediction(translation)

    return jsonify({ 'prediction': int(predictionValue) })

@app.route('/prediction/random_forest', methods=['POST'])
def randomForestPrediction():
    gameState = request.json

    translation = translateGameState(gameState)

    predictionValue = makeRandomForestPrediction(translation)

    return jsonify({ 'prediction': predictionValue })

if __name__ == '__main__':
    app.run()
