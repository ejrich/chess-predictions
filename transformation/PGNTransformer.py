import csv, os, re, sys
from Game import Game

propertyRegex = r'\[(.+) "(.+)"\]'

# Removed for the new deep learning approach
# def createColumns():
#     headers = ['Result']

#     pieces = ['Pawns', 'Rooks', 'Bishops', 'Knights', 'Queen', 'King', 'Total']

#     for piece in pieces:
#         headers.append('White' + piece)
#         headers.append('Black' + piece)

#     for rank in range(8):
#         for file in range(8):
#             actualFile = chr(file + 97)
#             headers.append(actualFile + str(rank + 1) + '_color')
#             headers.append(actualFile + str(rank + 1) + '_piece')
    
#     return headers

def createColumns():
    headers = ['Result', 'Move', 'Turn']

    for rank in range(8):
        for file in range(8):
            actualFile = chr(file + 97)
            headers.append(actualFile + str(rank + 1))
    
    return headers

def writeHeader(writer, headers):
    writer.writerow(headers)

def writeGameState(writer, headers, gameStates):
    for gameState in gameStates:
        row = []
        for column in headers:
            row.append(gameState[column])
        writer.writerow(row)

def readInputFile(inputFile, outputFile):
    writer = csv.writer(outputFile)
    header = createColumns()
    writeHeader(writer, header)

    game = Game()
    gameCount = 1
    errorGames = []
    for _, line in enumerate(inputFile):
        prop = re.match(propertyRegex, line)

        if prop:
            game.setProperty(prop.group(1), prop.group(2))

        elif line.startswith('1.'):
            # print('Simulating Game ' + str(gameCount))
            try:
                game.simulateGame(line)
                writeGameState(writer, header, game.gameStates)
            except:
                errorGames.append(gameCount)
            gameCount += 1
            game = Game()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide input and output files')
        exit(1)

    inputFileName = os.path.join(os.path.dirname(__file__), sys.argv[1])
    outputFileName = os.path.join(os.path.dirname(__file__), sys.argv[2])

    with open(inputFileName, 'r') as inputFile:
        with open(outputFileName, 'w', newline='') as outputFile:
            readInputFile(inputFile, outputFile)
