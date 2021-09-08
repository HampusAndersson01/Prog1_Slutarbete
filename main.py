import pygame
from pygame.locals import *
import random
from tkinter import *

#standard status för spelen
PongRun = False
TTTrun = False
FlappyDotRun = False

#Startar de olika spelen
def startPong():
    global PongRun
    PongRun = True
    root.destroy()
def startTTT():
    global TTTrun
    TTTrun = True
    root.destroy()
def startFlappyDot():
    global FlappyDotRun
    FlappyDotRun = True
    root.destroy()

root = Tk()
root.geometry("600x400")

l1 = Label(root, text="Gamehub av Hampus Andersson",anchor=CENTER,font=("Times","24","bold"))
l1.pack(side=TOP,pady=30)

#Spelknapparna
b1 = Button(root,text="Pong",command=startPong,width=600)
b2 = Button(root,text="Tic Tac Toe",command=startTTT,width=600)
b3 = Button(root,text="Flappy Dot",command=startFlappyDot,width=600)
b1.pack(side=TOP)
b2.pack(side=TOP)
b3.pack(side=TOP)
root.mainloop()

#Pong
while PongRun == True:
    active = True

    while active is True:
        #Variabler
        screenW = 800
        screenH = 500
        grey = [50, 50, 50]
        white = [255, 255, 255]
        red = [255,0,0]
        startDir = [8]
        AispeedY = 0
        AispeedX = 0

        pygame.init()
        pygame.display.set_caption ('Pong')
        screen = pygame.display.set_mode ((screenW, screenH))
        myfont = pygame.font.SysFont('Arial', 30)
        pygame.font.init()
        clock = pygame.time.Clock()
        aiPoints = 0
        playerPoints = 0
        gameon = True

        while gameon is True:
            #Variabler
            speedX = random.choice(startDir)
            speedY = random.randint(-1,1)
            start = 0
            debug = False
            started = False
            running = True
            speed = 5
            playerY = 250
            aiY = 250
            playerTop = playerY - 40
            playerBottom = playerY + 40
            aiTop = aiY - 40
            aiBottom = aiY + 40

            #Ger Ai bollen 3x bollens hastighet
            if speedX > 0:
                AispeedY = speedY*3
                AispeedX = speedX*3

            #Ritar Backgrund och väggar
            def drawBoard():
                screen.fill (grey)
                #Ritar väggar
                pygame.draw.rect(screen,white,(5,1,screenW-10,10))
                pygame.draw.rect(screen,white,(5,screenH-11,screenW-10,10))

            newBallX = 0
            newBallY = 0
            count = 0
            calcY = -1


            #Räknar ut hur bollen kommer att studsa genom att skapa en osynlig boll med 3x hastigheten
            #och sedan flyttar Ai:n till den beräknade positionen
            def calcMove():
                global newBallX,newBallY, AispeedX, AispeedY, count, calcY

                newBallX += AispeedX
                newBallY += AispeedY

                #Flyttar Ai:n
                if calcY >= 0:
                    if calcY+5 < aiY:
                        moveBars(-speed,"ai")
                    elif calcY-5 > aiY:
                        moveBars(speed,"ai")
                    if aiY == calcY and speedX > 0:
                        calcY = -1
                elif calcY == -1:
                    midY = screenH/2
                    if midY+5 < aiY:
                        moveBars(-speed,"ai")
                    elif midY-5 > aiY:
                        moveBars(speed,"ai")

                #Sätter startposition och hastighet när den skjuts av spelaren
                if ballX >= screenW-30 and speedX < 0:
                    newBallX = ballX
                    newBallY = ballY
                    AispeedY = speedY*3
                    AispeedX = speedX*3
                    count = 0

                elif newBallX <= 20 and count == 0:
                    calcY = newBallY
                    AispeedX = 0
                    AispeedY = 0
                    newBallY = calcY
                    newBallX = 20
                    count = 1

                elif newBallX < 0:
                    newBallX = 0
                    newBallY = 0

                if newBallY <= 15 and AispeedY < 0:
                    AispeedY *= -1

                elif  newBallY >= screenH-15:
                    AispeedY *= -1

                if count == 1 and speedX > 0:
                    calcY = -1

            #Flyttar spelarna
            def moveBars(direction,player):
                global playerY, playerTop, playerBottom, aiY, aiTop, aiBottom
                if player == "player":
                    playerTop = playerY - 35
                    playerBottom = playerY + 35
                    if direction < 0 and playerY > 50:
                        playerY += direction
                    elif direction > 0 and playerY < screenH - 50:
                        playerY += direction
                if player == "ai":
                    aiTop = aiY - 35
                    aiBottom = aiY + 35
                    if direction < 0 and aiY > 50:
                        aiY += direction
                    elif direction > 0 and aiY < screenH - 50:
                        aiY += direction
            #Ritar spelaren
            def drawPlayer(y):
                pygame.draw.rect(screen,white,(screenW-20,y-35,10,70))
            #Ritar AI:n
            def drawAi(y):
                pygame.draw.rect(screen,white,(10,y-35,10,70))

            ballX = 400
            ballY = 250
            #Flyttar bollen korrekt
            def moveBall(X,Y):
                global speedY, speedX, start, ballX, ballY
                if Y <= 15 or Y >= screenH-15:
                    speedY *= -1
                if Y <= playerBottom and Y >= playerTop and X >= screenW-20 and X <= screenW-10:
                    playerCenter = playerY
                    if Y < playerCenter-7:
                        if Y <= playerCenter-10:
                            speedY -= 3
                        elif Y <= playerCenter-30:
                            speedY -= 4
                        else:
                            speedY -= 1
                    elif Y > playerCenter+7:
                        if Y >= playerCenter+10:
                            speedY += 3
                        elif Y >= playerCenter+30:
                            speedY += 4
                        else:
                            speedY += 2

                    speedX *= -1
                elif Y <= aiBottom and Y >= aiTop and X <= 20 and X >= 10:
                    aiCenter = aiY
                    if Y < aiCenter-10:
                        if Y <= aiCenter-20:
                            speedY -= 3
                        elif Y <= aiCenter-30:
                            speedY -= 4
                        else:
                            speedY -= 1
                    elif Y > aiCenter+10:
                        if Y >= aiCenter+20:
                            speedY += 3
                        elif Y >= aiCenter+30:
                            speedY += 4
                        else:
                            speedY += 2

                    speedX *= -1

                X += speedX
                Y += speedY
                ballX = X
                ballY = Y

            #Kollar om bollen hamnar utanför skärmen
            def ballOut():
                global aiPoints, playerPoints, running
                if ballX < 0:
                    playerPoints += 1
                    running = False
                elif ballX > screenW:
                    aiPoints += 1
                    running = False
                textsurface = myfont.render((str(aiPoints)), False,white)
                textsurface2 = myfont.render((str(playerPoints)), False,white)
                screen.blit(textsurface,(335,10))
                screen.blit(textsurface2,(445,10))

            #Ritar bollen
            def drawBall():
                pygame.draw.circle(screen,white,(ballX,ballY),4)
                if debug == True:
                    pygame.draw.circle(screen,red,(newBallX,newBallY),2)


            #Huvudloop
            while running is True:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type is QUIT:
                        running = False
                        active = False
                        gameon = False
                        PongRun = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    moveBars(-speed,"player")
                elif keys[pygame.K_DOWN]:
                    moveBars(speed,"player")
                if keys[pygame.K_r]:
                    running = False
                    gameon = False
                if keys[pygame.K_SPACE]:
                    started = True
                if keys[pygame.K_f]:
                    if debug == True:
                        debug = False
                    else:
                        debug = True
                drawBoard()
                if started is True:
                    moveBall(ballX,ballY)
                    calcMove()
                else:
                    screen.blit(myfont.render(("Press Space to start"), False, white),(screenW/2-120,50))
                ballOut()
                drawPlayer(playerY)
                drawAi(aiY)
                drawBall()
                pygame.display.flip()

#Tic Tac Toe
while TTTrun == True:
    active = True
    AiPoints = 0
    playerPoints = 0
    matches = 0
    while active == True:
        playerWin = 0
        AiWin = 0
        # Globala variabler
        XO   = "X"   # Vems tur det är X = Spelaren O = AI
        grid = [ [ None, None, None ], \
                 [ None, None, None ], \
                 [ None, None, None ] ]
        gridCoord = [[0,0],[0,1],[0,2],\
                     [1,0],[1,1],[1,2],\
                     [2,0],[2,1],[2,2],]

        winner = None
        tied = False
        move = 0
        Gboard = [" " for x in range(10)]
        # Skapar Spelplanen
        def createBoard(ttt):
            # Skapar bakgrunden
            background = pygame.Surface (ttt.get_size())
            background = background.convert()
            background.fill ((250, 250, 250))

            # vertikala linjer
            pygame.draw.line (background, (0,0,0), (100, 0), (100, 300), 2)
            pygame.draw.line (background, (0,0,0), (200, 0), (200, 300), 2)

            # horizontella linjer
            pygame.draw.line (background, (0,0,0), (0, 100), (300, 100), 2)
            pygame.draw.line (background, (0,0,0), (0, 200), (300, 200), 2)

            return background

        def drawStatus (board):
            # Skriver ut all nödvändig text
            global XO, winner, playerWin, AiWin

            # Kollar om någon har vunnit
            if (tied is True and winner is None):
                message = "Game tied! Press R to restart"
            elif (winner is None):
                message = XO + "'s turn"+"          "+"Matches: "+ str(matches)+" You: "+str(playerPoints)+" AI: "+str(AiPoints)
            else:
                if (winner == "X"):
                    playerWin = 1
                elif (winner == "O"):
                    AiWin = 1
                message = winner + " won! Press R to restart"

            # renderar status text
            font = pygame.font.Font(None, 24)
            text = font.render(message, 1, (10, 10, 10))

            # kopierar statusen till skärmen
            board.fill ((250, 250, 250), (0, 300, 300, 25))
            board.blit(text, (10, 300))

        def showBoard (ttt, board):
            drawStatus (board)
            ttt.blit (board, (0, 0))
            pygame.display.flip()

        def boardPos (mouseX, mouseY):
            # Kollar vilken ruta spelaren tryckt i
            # ---------------------------------------------------------------
            # mouseX : X kordinaterna som spelaren klickade
            # mouseY : Y kordinaterna som spelaren klickade

            # Kollar vilken rad spelaren tryckt i
            if (mouseY < 100):
                row = 0
            elif (mouseY < 200):
                row = 1
            else:
                row = 2

            # Kollar vilken kolumn spelaren tryckt i
            if (mouseX < 100):
                col = 0
            elif (mouseX < 200):
                col = 1
            else:
                col = 2

            return (row, col)

        def drawMove (board, boardRow, boardCol, Piece):
            # ritar spelar markörer på spelplanen

            # räknar ut mitten på rutan
            centerX = ((boardCol) * 100) + 50
            centerY = ((boardRow) * 100) + 50

            # ritar den rätta spelarmarkören

            if (Piece == "O"):
                pygame.draw.circle (board, (0,0,0), (centerX, centerY), 44, 2)
            else:
                pygame.draw.line (board, (0,0,0), (centerX - 22, centerY - 22), \
                                 (centerX + 22, centerY + 22), 2)
                pygame.draw.line (board, (0,0,0), (centerX + 22, centerY - 22), \
                                 (centerX - 22, centerY + 22), 2)

            # markerar rutan som använd
            grid [boardRow][boardCol] = Piece

        def clickBoard(board):
            # Kollar var spelaren klickade och sätter ut X där
            global grid, XO
            if (XO == "X"):
                (mouseX, mouseY) = pygame.mouse.get_pos()
                (row, col) = boardPos (mouseX, mouseY)

                # Kollar om rutan är upptagen
                if ((grid[row][col] == "X") or (grid[row][col] == "O")):
                    return

                # ritar X
                drawMove (board, row, col, "X")

                # bytar spelartur
                if (XO == "X"):
                    XO = "O"

        def iswinner(bo,le):
            return ((bo[6] == le and bo[7] == le and bo[8] == le) or # Övre raden
                    (bo[3] == le and bo[4] == le and bo[5] == le) or # Mitten raden
                    (bo[0] == le and bo[1] == le and bo[2] == le) or # Nedre raden
                    (bo[6] == le and bo[3] == le and bo[0] == le) or # Ner på vänster sida
                    (bo[7] == le and bo[4] == le and bo[1] == le) or # Ner genom mitten
                    (bo[8] == le and bo[5] == le and bo[2] == le) or # Ner på höger sida
                    (bo[6] == le and bo[4] == le and bo[2] == le) or # diagonal
                    (bo[8] == le and bo[4] == le and bo[0] == le))   # diagonal

        def gameWon(board):
            # kollar om någon vunnit

            global grid, winner, tied

            # kollar efter vinnande rader
            for row in range (0, 3):
                if ((grid [row][0] == grid[row][1] == grid[row][2]) and \
                   (grid [row][0] is not None)):
                    winner = grid[row][0]
                    pygame.draw.line (board, (250,0,0), (0, (row + 1)*100 - 50), \
                                      (300, (row + 1)*100 - 50), 2)
                    break

            # kollar efter vinnande kolumner
            for col in range (0, 3):
                if (grid[0][col] == grid[1][col] == grid[2][col]) and \
                   (grid[0][col] is not None):
                    winner = grid[0][col]
                    pygame.draw.line (board, (250,0,0), ((col + 1)* 100 - 50, 0), \
                                      ((col + 1)* 100 - 50, 300), 2)
                    break

            # kollar efter vinnande diagonaler
            if (grid[0][0] == grid[1][1] == grid[2][2]) and \
               (grid[0][0] is not None):
                winner = grid[0][0]
                pygame.draw.line (board, (250,0,0), (50, 50), (250, 250), 2)

            if (grid[0][2] == grid[1][1] == grid[2][0]) and \
               (grid[0][2] is not None):
                winner = grid[0][2]
                pygame.draw.line (board, (250,0,0), (250, 50), (50, 250), 2)

            # kollar om det blir lika
            summa = 0
            for i in range(3):
                for k in range(3):
                    if (grid[i][k] != None):
                        summa += 1
            if (summa == 9):
                tied = True

        def compMove():
            Gboard = []
            count = 0
            if count < 9:
                for i in grid:
                    for k in i:
                        Gboard.insert(count,k)
                        count += 1

            possibleMoves = [x for x, letter in enumerate(Gboard) if letter == None and x != "O"]
            move = -1

            for let in ["O", "X"]:
                for i in possibleMoves:
                    GboardCopy = Gboard[:]
                    GboardCopy[i] = let
                    if iswinner(GboardCopy, let) is True:
                        move = i
                        return move

            #Försöker sätta i mitten
            if 4 in possibleMoves:
                move = 4
                return move

            #Försöker sätta i hörnen
            cornersOpen = []
            for i in possibleMoves:
                if i in [0,2,6,8]:
                    cornersOpen.append(i)
            if len(cornersOpen) > 0:
                move = selectRandom(cornersOpen)
                return move

            #Försöker ta kanterna
            edgesOpen = []
            for i in possibleMoves:
                if i in [1,3,5,7]:
                    edgesOpen.append(i)

            if len(edgesOpen) > 0:
                move = selectRandom(edgesOpen)

            return move

        def selectRandom(li):
            ln = len(li)
            r = random.randrange(0, ln)
            return li[r]
        #---------------------------------------------------------------------
        pygame.init()
        ttt = pygame.display.set_mode ((300, 350))
        pygame.display.set_caption ("Tic-Tac-Toe")

        # skapar spelplan
        board = createBoard (ttt)

        # huvudloop
        running = 1

        while (running == 1):
            for event in pygame.event.get():
                if event.type is QUIT:
                    running = 0
                    active = False
                    TTTrun = False
                elif event.type is MOUSEBUTTONDOWN and winner is None:
                    clickBoard(board)

                elif event.type == KEYDOWN:
                    if event.key == pygame.K_r:
                        running = 0
            gameWon (board)
            if (XO == "O" and winner is None and tied is False):
                    moveint = compMove()
                    drawMove(board,gridCoord[moveint][0],gridCoord[moveint][1],"O")
                    XO = "X"

            showBoard (ttt, board)
        playerPoints += playerWin
        AiPoints += AiWin
        matches += 1

#Flappy Dot
while FlappyDotRun == True:
    #Variabler
    screenW = 400
    screenH = 600
    grey = [50, 50, 50]
    white = [255, 255, 255]
    red = [255,0,0]
    green = [0,255,0]
    blue = [66, 134, 244]
    startedfd = False

    pygame.init()
    pygame.display.set_caption ('Flappy Dot')
    screen = pygame.display.set_mode ((screenW, screenH))
    myfont = pygame.font.SysFont('Arial', 30)
    pygame.font.init()
    clock = pygame.time.Clock()

    points = 0
    running = True
    playerX = screenW * 0.2
    playerY = screenH/2

    pipeVelX = -4
    baseY = screenH * 0.85
    pipeGap = 100
    playerVelY    =  -9
    playerMaxVelY =  10
    playerMinVelY =  -8
    playerAccY    =   1
    playerFlapAcc =  -8
    playerFlapped = False

    lowerPipe = []
    upperPipe = []

    #Laddar spelarbild
    image = pygame.image.load("flappyDot.png")
    img_rect = image.get_rect()
    angle = 0

    #Ritar Bakgrunden
    def drawBoard():
        screen.fill (blue)
        pygame.draw.rect(screen,green,((0,baseY),(screenW,screenH)))
        screen.blit(myfont.render(str(points), False,white),(10,10))

    #Ritar spelaren
    def drawPlayer():
        #Räknar ut centrum på bilden
        rot_image = pygame.transform.rotate(image, angle)
        rot_im_rect = rot_image.get_rect()
        rot_im_rect.center = img_rect.center

        rot_im_rect[0] += playerX-20
        rot_im_rect[1] += playerY-20
        screen.blit(rot_image, rot_im_rect)

    #Flyger upp
    def jump():
        global playerVelY,playerFlapped
        if playerY > 0:
            playerVelY = playerFlapAcc
            playerFlapped = True

    #Skapar Ett rör med randomiserad höjd
    def getRandomPipe():
        gapY = random.randrange(0, int(baseY * 0.6 - pipeGap))
        pipeHeight = random.randrange(50,baseY-50)
        pipeX = screenW + 60

        upperPipe.append({'x': pipeX, 'y': pipeHeight - 100})  # upper pipe
        lowerPipe.append({'x': pipeX, 'y': gapY + pipeGap}) # lower pipe

    #skapare det första röret
    getRandomPipe()


    #Ritar rören
    def drawPipes():
        global upperx1, upperx2, uppery1, uppery2, lowerx1, lowerx2, lowery1, lowery2
        #Fyra hörnen för övre rörer
        upperx1 = upperPipe[0]["x"]
        uppery1 = -100
        upperx2 = upperPipe[0]["x"] - 60
        uppery2 = upperPipe[0]["y"]
        #Fyra hörnen för övre rörer
        lowerx1 = lowerPipe[0]["x"]
        lowery1 = upperPipe[0]["y"]+150
        lowerx2 = lowerPipe[0]["x"] - 60
        lowery2 = upperPipe[0]["y"]+150 + screenH-upperPipe[0]["y"]+100

        pygame.draw.rect(screen,grey,((upperPipe[0]["x"],0),(-60,upperPipe[0]["y"])))
        pygame.draw.rect(screen,grey,((lowerPipe[0]["x"],upperPipe[0]["y"]+150),(-60,screenH-upperPipe[0]["y"]+100)))

    dead = False
    #Kollar efter kollision
    def checkColl():
        global upperx1, upperx2, uppery1, uppery2, lowerx1, lowerx2, lowery1, lowery2, pipeVelX, playerVelY,playerMaxVelY,playerMinVelY, playerAccY,playerFlapAcc, dead
        #Stoppar all rörelse vid kollision
        if playerY - 20 <= uppery2 and playerY - 20 >= uppery1 and playerX >= upperx2 and playerX <= upperx1:
            pipeVelX = 0
            playerVelY = 0
            playerMaxVelY = 0
            playerMinVelY = 0
            playerAccY = 0
            playerFlapAcc = 0
        if playerY + 20 <= lowery2 and playerY + 20 >= lowery1 and playerX >= lowerx2 and playerX <= lowerx1:
            pipeVelX = 0
            playerVelY = 0
            playerMaxVelY = 0
            playerMinVelY = 0
            playerAccY = 0
            playerFlapAcc = 0
            dead = True
    #Roterar spelaren om den är påväg upp eller ner
    def rotatePlayer():
        global angle
        if playerVelY < 0:
            angle = 25
        elif playerVelY > 0:
            #Vid fall ändras vinkeln exponentiell
            angle = int(playerVelY*4)*-1
        else:
            angle = 0
    #Huvud loop
    while running is True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type is QUIT:
                running = False
                FlappyDotRun = False
        #Kollar efter inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if startedfd == False:
                startedfd = True
            jump()
        if keys[pygame.K_r]:
            running = False
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False


        playerY += min(playerVelY, baseY - playerY)
        drawBoard()
        drawPipes()
        rotatePlayer()
        drawPlayer()
        if startedfd == True:
            checkColl()
            #Skapar nytt rör när det andra går ur bild
            if upperPipe[0]['x'] < 5:
                getRandomPipe()
            #Flyttar rören
            for uPipe, lPipe in zip(upperPipe, lowerPipe):
                uPipe['x'] += pipeVelX
                lPipe['x'] += pipeVelX

            #Tar bort det röret som är passerat
            if upperPipe[0]['x'] <= 0:
                upperPipe.pop(0)
                lowerPipe.pop(0)
                points += 1
            #Stoppar all rörelse om spelaren nuddar marken
            if playerY == baseY:
                pipeVelX = 0
                playerVelY = 0
                playerMaxVelY = 0
                playerMinVelY = 0
                playerAccY = 0
                playerFlapAcc = 0
                dead = True
        else:
            screen.blit(myfont.render(("Press Space to start"), False, white),(screenW/2-120,50))
        if dead == True:
            screen.blit(myfont.render(("Press R to restart"), False, white),(screenW/2-120,50))
        pygame.display.flip()
