import pygame
pygame.init()

# Screen setup
WIDTH = 1000
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font(None, 20)
bigFont = pygame.font.Font(None, 50)
pygame.display.set_caption('Two-Player Chess')
timer = pygame.time.Clock()
fps = 60
counter = 0
winner = ''
gameOver = False

# Starting pieces and loctions on the board
whitePieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn',
               'rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
whiteLocations = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                  (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
blackPieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
               'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
blackLocations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

# Captured piece points
pieceList = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
points = [1, 9, 0, 3, 5, 3]
capturedPiecesWhite = []
pointsWhite = 0
capturedPiecesBlack = []
pointsBlack = 0

# Other variables
# 0 - White's turn no selection, 1 - White's turn piece selected, 2 - Black's turn no selection, 3 - Black's turn piece selected
step = 0
statusText = ['White\'s turn: Select a piece to move.', 'White\'s turn: Select a destination square',
              'Black\'s turn: Select a piece to move.', 'Black\'s turn: Select a destination square.']
selection = 100
validMoves = []

# Load piece images
queenBlack = pygame.image.load('assets/images/queenBlack.png')
queenBlack = pygame.transform.scale(queenBlack, (80, 80))
queenBlackSmall = pygame.transform.scale(queenBlack, (40, 40))
queenWhite = pygame.image.load('assets/images/queenWhite.png')
queenWhite = pygame.transform.scale(queenWhite, (80, 80))
queenWhiteSmall = pygame.transform.scale(queenWhite, (40, 40))
kingBlack = pygame.image.load('assets/images/kingBlack.png')
kingBlack = pygame.transform.scale(kingBlack, (80, 80))
kingBlackSmall = pygame.transform.scale(kingBlack, (40, 40))
kingWhite = pygame.image.load('assets/images/kingWhite.png')
kingWhite = pygame.transform.scale(kingWhite, (80, 80))
kingWhiteSmall = pygame.transform.scale(kingWhite, (40, 40))
rookBlack = pygame.image.load('assets/images/rookBlack.png')
rookBlack = pygame.transform.scale(rookBlack, (80, 80))
rookBlackSmall = pygame.transform.scale(rookBlack, (40, 40))
rookWhite = pygame.image.load('assets/images/rookWhite.png')
rookWhite = pygame.transform.scale(rookWhite, (80, 80))
rookWhiteSmall = pygame.transform.scale(rookWhite, (40, 40))
bishopBlack = pygame.image.load('assets/images/bishopBlack.png')
bishopBlack = pygame.transform.scale(bishopBlack, (80, 80))
bishopBlackSmall = pygame.transform.scale(bishopBlack, (40, 40))
bishopWhite = pygame.image.load('assets/images/bishopWhite.png')
bishopWhite = pygame.transform.scale(bishopWhite, (80, 80))
bishopWhiteSmall = pygame.transform.scale(bishopWhite, (40, 40))
knightBlack = pygame.image.load('assets/images/knightBlack.png')
knightBlack = pygame.transform.scale(knightBlack, (80, 80))
knightBlackSmall = pygame.transform.scale(knightBlack, (40, 40))
knightWhite = pygame.image.load('assets/images/knightWhite.png')
knightWhite = pygame.transform.scale(knightWhite, (80, 80))
knightWhiteSmall = pygame.transform.scale(knightWhite, (40, 40))
pawnBlack = pygame.image.load('assets/images/pawnBlack.png')
pawnBlack = pygame.transform.scale(pawnBlack, (80, 80))
pawnBlackSmall = pygame.transform.scale(pawnBlack, (40, 40))
pawnWhite = pygame.image.load('assets/images/pawnWhite.png')
pawnWhite = pygame.transform.scale(pawnWhite, (80, 80))
pawnWhiteSmall = pygame.transform.scale(pawnWhite, (40, 40))
imagesWhite = [pawnWhite, queenWhite, kingWhite, knightWhite, rookWhite, bishopWhite]
imagesWhiteSmall = [pawnWhiteSmall, queenWhiteSmall, kingWhiteSmall, knightWhiteSmall, rookWhiteSmall, bishopWhiteSmall]
imagesBlack = [pawnBlack, queenBlack, kingBlack, knightBlack, rookBlack, bishopBlack]
imagesBlackSmall = [pawnBlackSmall, queenBlackSmall, kingBlackSmall, knightBlackSmall, rookBlackSmall, bishopBlackSmall]

# Draw game board
def drawBoard():
    for i in range(32):
        column = i % 4
        row = i // 4
        # Draw the light squares
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [column*200, row*100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [(column*200) + 100, row*100, 100, 100])
        # Draw instruction area (bottom)
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 150])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 150], 5)
        screen.blit(bigFont.render(statusText[step], True, 'black'), (20, 820))
        # Draw points
        screen.blit(font.render(str(pointsWhite), True, 'blue'), (840, 20))
        screen.blit(font.render(str(pointsBlack), True, 'red'), (940, 20))
        # Draw captured pieces area (right)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        # Draw borders
        for i in range (9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(bigFont.render('FORFEIT', True, 'black'), (825, 860))

# Draw pieces
def drawPieces():

    # Draw white pieces
    for i in range(len(whitePieces)):
        index = pieceList.index(whitePieces[i])
        screen.blit(imagesWhite[index], (whiteLocations[i][0] * 100 + 10, whiteLocations[i][1] * 100 + 10))
        # Highlight chosen piece
        if step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [whiteLocations[i][0] * 100 + 1, whiteLocations[i][1] * 100 + 1, 100, 100], 2)

    # Draw black pieces
    for i in range(len(blackPieces)):
        index = pieceList.index(blackPieces[i])
        screen.blit(imagesBlack[index], (blackLocations[i][0] * 100 + 10, blackLocations[i][1] * 100 + 10))
        # Highlight chosen piece
        if step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [blackLocations[i][0] * 100 + 1, blackLocations[i][1] * 100 + 1, 100, 100], 2)

# Check all pieces valid moves
def  checkOptions(pieces, locations, turn):
    movesList = []
    allMovesList = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            movesList = checkPawn(location, turn)
        elif piece == 'rook':
            movesList = checkRook(location, turn)
        elif piece == 'knight':
            movesList = checkKnight(location, turn)
        elif piece == 'bishop':
            movesList = checkBishop(location, turn)
        elif piece == 'queen':
            movesList = checkQueen(location, turn)
        elif piece == 'king':
            movesList = checkKing(location, turn)
        allMovesList.append(movesList)
    return allMovesList

# Check valid king moves
def checkKing(position, color):
    movesList = []
    if color == 'white':
        enemiesList = blackLocations
        friendsList = whiteLocations
    else:
        friendsList = blackLocations
        enemiesList = whiteLocations
    # Check 8 squares
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friendsList and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            movesList.append(target)
    return movesList

# Check valid queen moves
def checkQueen(position, color):
    movesList = []
    bishopList = checkBishop(position, color)
    rookList = checkRook(position, color)
    for i in range(len(bishopList)):
        movesList.append(bishopList[i])
    for i in range(len(rookList)):
        movesList.append(rookList[i])
    return movesList


# Check valid bishop moves
def checkBishop(position, color):
    movesList = []
    if color == 'white':
        enemiesList = blackLocations
        friendsList = whiteLocations
    else:
        friendsList = blackLocations
        enemiesList = whiteLocations
    # Check all 4 directions: Up-Right, Up-Left, Down-Right, Down-Left
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friendsList and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                movesList.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain *y)) in enemiesList:
                    path = False
                chain +=1
            else:
                path = False
    return movesList

# Check valid knight moves
def checkKnight(position, color):
    movesList = []
    if color == 'white':
        friendsList = whiteLocations
    else:
        friendsList = blackLocations
    # Check 8 squares
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friendsList and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            movesList.append(target)
    return movesList

# Check valid rook moves
def checkRook(position, color):
    movesList = []
    if color == 'white':
        enemiesList = blackLocations
        friendsList = whiteLocations
    else:
        friendsList = blackLocations
        enemiesList = whiteLocations
    # Check all 4 directions: Down, Up, Right, Left
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain *  x), position[1] + (chain * y)) not in friendsList and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                movesList.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position [1] + (chain * y)) in enemiesList:
                    path = False
                chain += 1
            else:
                path = False
    return movesList

# Check valid pawn moves
def checkPawn(position, color):
    movesList = []
    if color == 'black':
        if (position[0], position[1] + 1) not in whiteLocations and (position[0], position[1] + 1) not in blackLocations and position[1] < 7:
            movesList.append((position[0], position[1] + 1))
        if (position[0], position[1] + 1) not in whiteLocations and (position[0], position[1] + 1) not in blackLocations and position[1] == 1:
            movesList.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in whiteLocations:
            movesList.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in whiteLocations:
            movesList.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in whiteLocations and (position[0], position[1] - 1) not in blackLocations and position[1] > 0:
            movesList.append((position[0], position[1] - 1))
        if (position[0], position[1] - 1) not in whiteLocations and (position[0], position[1] - 1) not in blackLocations and position[1] == 6:
            movesList.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in blackLocations:
            movesList.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in blackLocations:
            movesList.append((position[0] - 1, position[1] - 1))
    return movesList

# Check valid moves for selection
def checkValidMoves():
    if step < 2:
        optionsList = whiteOptions
    else:
        optionsList = blackOptions
    validOptions = optionsList[selection]
    return validOptions

# Draw valid moves for selection
def drawValidMoves(moves):
    if step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

# Draw captured pieces and calculate points
def drawCapturedPieces():
    for i in range(len(capturedPiecesWhite)):
        capturedPiece = capturedPiecesWhite[i]
        index = pieceList.index(capturedPiece)
        screen.blit(imagesWhiteSmall[index], (925, 50 + 50*i))
    for i in range(len(capturedPiecesBlack)):
        capturedPiece = capturedPiecesBlack[i]
        index = pieceList.index(capturedPiece)
        screen.blit(imagesBlackSmall[index], (825, 50 + 50*i))

# Check indicator
def drawCheck():
    if step < 2:
        if 'king' in whitePieces:
            kingIndex = whitePieces.index('king')
            kingLocation = whiteLocations[kingIndex]
            for i in range(len(blackOptions)):
                if kingLocation in blackOptions[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [whiteLocations[kingIndex][0] * 100 + 1, whiteLocations[kingIndex][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in blackPieces:
            kingIndex = blackPieces.index('king')
            kingLocation = blackLocations[kingIndex]
            for i in range(len(whiteOptions)):
                if kingLocation in whiteOptions[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [blackLocations[kingIndex][0] * 100 + 1, blackLocations[kingIndex][1] * 100 + 1, 100, 100], 5)

# Game over screen
def drawGameOver():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to play again.', True, 'white'), (210, 240))

# Initial valid moves calculation
blackOptions = checkOptions(blackPieces, blackLocations, 'black')
whiteOptions = checkOptions(whitePieces, whiteLocations, 'white')

# Main game loop
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark grey')
    drawBoard()
    drawPieces()
    drawCapturedPieces()
    drawCheck()
    if selection != 100:
        validMoves = checkValidMoves()
        drawValidMoves(validMoves)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and not gameOver:
            xCoord = event.pos[0] // 100
            yCoord = event.pos[1] // 100
            clickCoords = (xCoord, yCoord)
            # White's turn
            if step < 2:
                if clickCoords == (8, 8) or clickCoords == (8, 9):
                    winner = 'black'
                if clickCoords in whiteLocations:
                    selection = whiteLocations.index(clickCoords)
                    if step == 0:
                        step = 1
                if clickCoords in validMoves and selection != 1000:
                    whiteLocations[selection] = clickCoords
                    if clickCoords in blackLocations:
                        target = blackLocations.index(clickCoords)
                        capturedPiecesBlack.append(blackPieces[target])
                        index = pieceList.index(blackPieces[target])
                        # Winner check
                        if points[index] == 0:
                            winner = 'white'
                        # Points increase
                        pointsWhite = pointsWhite + points[index]
                        blackPieces.pop(target)
                        blackLocations.pop(target)
                    blackOptions = checkOptions(blackPieces, blackLocations, 'black')
                    whiteOptions = checkOptions(whitePieces, whiteLocations, 'white')
                    step = 2
                    selection = 100
                    validMoves = []
            # Black's turn
            if step >= 2:
                if clickCoords == (8, 8) or clickCoords == (8, 9):
                    winner = 'white'
                if clickCoords in blackLocations:
                    selection = blackLocations.index(clickCoords)
                    if step == 2:
                        step = 3
                if clickCoords in validMoves and selection != 1000:
                    blackLocations[selection] = clickCoords
                    if clickCoords in whiteLocations:
                        target = whiteLocations.index(clickCoords)
                        capturedPiecesWhite.append(whitePieces[target])
                        index = pieceList.index(whitePieces[target])
                        # Winner check
                        if points[index] == 0:
                            winner = 'black'
                        # Points increase
                        pointsBlack = pointsBlack + points[index]
                        whitePieces.pop(target)
                        whiteLocations.pop(target)
                    blackOptions = checkOptions(blackPieces, blackLocations, 'black')
                    whiteOptions = checkOptions(whitePieces, whiteLocations, 'white')
                    step = 0
                    selection = 100
                    validMoves = []
        
        # Restart the game
        if event.type == pygame.KEYDOWN and gameOver:
            if event.key == pygame.K_RETURN:
                gameOver = False
                winner = ''
                whitePieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn',
                'rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
                whiteLocations = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                                  (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
                blackPieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                               'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                blackLocations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                capturedPiecesWhite = []
                pointsWhite = 0
                capturedPiecesBlack = []
                pointsBlack = 0
                step = 0
                selection = 100
                validMoves = []
                blackOptions = checkOptions(blackPieces, blackLocations, 'black')
                whiteOptions = checkOptions(whitePieces, whiteLocations, 'white')
 
    # Game over
    if winner != '':
        gameOver = True
        drawGameOver()
        
    pygame.display.flip()
pygame.quit()