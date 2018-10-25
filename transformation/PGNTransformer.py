import csv, os, re, sys
from Game import Game

propertyRegex = r'\[(.+) "(.+)"\]'

def readInputFile(inputFile):
    games = []
    game = Game()
    gameCount = 1
    for _, line in enumerate(inputFile):
        prop = re.match(propertyRegex, line)

        if prop:
            game.setProperty(prop.group(0), prop.group(1))

        elif line.startswith('1.'):
            print('Simulating Game ' + str(gameCount))
            game.simulateGame(line)
            games += game.getGameStates()
            gameCount += 1
            game = Game()

    return games

def writeOutputFile(outputFile, games):
    writer = csv.writer(outputFile)
    for game in games:
        # TODO
        print(game)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide input and output files')
        exit(1)

    inputFileName = os.path.join(os.path.dirname(__file__), sys.argv[1])
    outputFileName = os.path.join(os.path.dirname(__file__), sys.argv[2])

    with open(inputFileName, 'r') as inputFile:
        games = readInputFile(inputFile)

    with open(outputFileName, 'w') as outputFile:
        writeOutputFile(outputFile, games)
