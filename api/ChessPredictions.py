import os
from flask import Flask, g, request, jsonify
from flask_cors import CORS
from sklearn.externals import joblib
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)
CORS(app)

linearRegression = joblib.load(os.path.join(os.path.dirname(__file__), '../models/201801_linear_regression.joblib'))
logisticRegression = joblib.load(os.path.join(os.path.dirname(__file__), '../models/201801_logistic_regression.joblib'))
randomForestRegression = joblib.load(os.path.join(os.path.dirname(__file__), '../models/201801_random_forest_regression.joblib'))

pieces = ['P', 'B', 'R', 'N', 'Q', 'K']
dl_pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
models = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']

def makeLinearPrediction(gameState):
    prediction = linearRegression.predict([gameState])
    return prediction[0]

def makeLogisticPrediction(gameState):
    prediction = logisticRegression.predict([gameState])
    return prediction[0]

def makeRandomForestPrediction(gameState):
    prediction = randomForestRegression.predict([gameState])
    return prediction[0]

def makeDeepLearningPrediction(gameState):
    linearDense = load_model(os.path.join(os.path.dirname(__file__), '../models/20190209_linear.h5'))
    inputs = np.array([gameState])
    prediction = linearDense.predict(inputs)
    return prediction[0][0]

def makeConvolutionPrediction(gameState):
    convolution = load_model(os.path.join(os.path.dirname(__file__), '../models/20190210_convolution.h5'))
    inputs = np.array([gameState])
    prediction = convolution.predict(inputs)[0]
    return prediction[1] - prediction[2]

def loadMoveModel(piece):
    return load_model(os.path.join(os.path.dirname(__file__), '../models/20190213_' + models[piece] + '_convolution.h5'))

def makeMovePrediction(gameState):
    pieceModel = load_model(os.path.join(os.path.dirname(__file__), '../models/20190213_piece_convolution.h5'))

    inputs = np.array([gameState])
    piecePred = pieceModel.predict(inputs)[0]

    square = np.argmax(piecePred)

    rank = int(square / 8)
    file = int(square % 8)

    piece = np.argmax(inputs[0][rank][file])

    moveModel = loadMoveModel(piece)
    movePred = moveModel.predict(inputs)[0]

    square = np.argmax(movePred)

    moveRank = int(square / 8)
    moveFile = int(square % 8)

    return (rank, file, moveRank, moveFile)

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

def translateGameState_dl(gameState):
    translation = []

    for rank in range(1, 9):
        for file in range(ord('a'), ord('h') + 1):
            id = chr(file) + str(rank)

            color = 0 if gameState[id + '_color'] == 1 else 6 if gameState[id + '_color'] == 2 else 0

            pieceCategories = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            piece = dl_pieces.index(gameState[id + '_piece']) if gameState[id + '_piece'] else None
            if piece != None:
                pieceCategories[piece + color] = 1

            translation += pieceCategories

    return translation

def translateGameState_conv(gameState):
    translation = np.zeros((8, 8, 6))

    for rank in range(1, 9):
        for file in range(ord('a'), ord('h') + 1):
            id = chr(file) + str(rank)

            value = 1 if gameState[id + '_color'] == 1 else -1 if gameState[id + '_color'] == 2 else 0

            piece = dl_pieces.index(gameState[id + '_piece']) if gameState[id + '_piece'] else None
            if piece != None:
                translation[rank - 1][file - 97][piece] = value

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

@app.route('/prediction/dl_linear', methods=['POST'])
def deepLearningPrediction():
    gameState = request.json

    translation = translateGameState_dl(gameState)

    predictionValue = makeDeepLearningPrediction(translation)

    return jsonify({ 'prediction': float(predictionValue) })

@app.route('/prediction/convolution', methods=['POST'])
def convolutionPrediction():
    gameState = request.json

    translation = translateGameState_conv(gameState)

    predictionValue = makeConvolutionPrediction(translation)

    return jsonify({ 'prediction': float(predictionValue) })

@app.route('/prediction/move', methods=['POST'])
def movePrediction():
    gameState = request.json

    translation = translateGameState_conv(gameState)

    move = makeMovePrediction(translation)

    return jsonify({ 'rank': move[0], 'file': move[1], 'moveRank': move[2], 'moveFile': move[3] })

if __name__ == '__main__':
    app.run()
