import csv, re, sys
from Game import Game

propertyRegex = r'\[(.+) "(.+)"\]'

def readInputFile(inputFile):
    games = []
    game = Game()
    for line in enumerate(inputFile):
        prop = re.match(propertyRegex, line)

        if prop:
            game.setProperty(prop.group(0), prop.group(1))

        elif line.startswith('1.'):
            game.simulateGame(line)
            games += game.getGameStates()
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

    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    with open(inputFileName, 'r') as inputFile:
        games = readInputFile(inputFile)
    
    with open(outputFileName, 'w') as outputFile:
        writeOutputFile(outputFile, games)
