import random, pygame, sys
from pygame.locals import *
#initialization
FPS = 100
##WINDOWWIDTH = 640
#WINDOWHEIGHT = 480
WINDOWWIDTH = 600
WINDOWHEIGHT = 480
CELLSIZE = 30
assert WINDOWHEIGHT % CELLSIZE == 0, "Window width must be a multiple of cell size!"
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size!"

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
BLUE     = (   0,  0,   255)
DARKBLUE = (   0,  0,   155)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = WHITE


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

direction = UP
DIRECTION = [UP,DOWN,LEFT,RIGHT]

HEAD = 0 # syntactic sugar: index of the snake's head

inf = 10000
dis = []

for y in range(CELLHEIGHT + 2):
    dis.append([])
    for x in range(CELLWIDTH + 2):
        dis[y].append(inf)
#check for bfs
def check(gd, queue, visited, snake, food):
    x = gd[0]
    y = gd[1]
    if (x, y) == (food['x'],food['y']):
        return False
    elif x < 0 or x >= CELLWIDTH or y < 0 or y >= CELLHEIGHT:
        return False
    elif (x, y) in queue or (x, y) in visited:
        return False
    else:
        return True

#canmove further
def canmove(x, y, snake):
    if x < 0 or x >= CELLWIDTH:
        return False
    elif y < 0 or y >= CELLHEIGHT:
        return False
    elif isSnake(x, y,snake):
        return False
    elif (x, y) == (snake[HEAD]['x'], snake[HEAD]['y']):
        return False
    else:
        return True

#isSnakebody
def isSnake(x, y, snake):
    for body in snake:
        if body['x'] == x and body['y'] == y:
            return True
    return False

#bfs
def caldis(snake,food):
    queue = [(food['x'], food['y'])]
    visited = []
    found = False
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            dis[y][x] = inf

    dis[food['y']][food['x']] = 0

    while len(queue) != 0:
        head = queue[0]
        visited.append(head)
        up_grid = head[0], head[1] - 1
        down_grid = head[0], head[1] + 1
        left_grid = head[0] - 1, head[1]
        right_grid = head[0] + 1, head[1]

        for grid in [up_grid, down_grid, left_grid, right_grid]:
            if check(grid, queue, visited, snake, food):
                if grid[0] == snake[HEAD]['x'] and grid[1] == snake[HEAD]['y']:
                    found = True
                if not isSnake(grid[0], grid[1], snake):
                    queue.append(grid)
                    dis[grid[1]][grid[0]] = dis[head[1]][head[0]] + 1
        queue.pop(0)
    return found

#return the next direction
def dirCheck(now, direc):
    loc = {'x':0,'y':0}
    if direc == UP:
        loc = {'x':now['x'],'y':now['y'] - 1}
    elif direc == DOWN:
        loc = {'x':now['x'],'y':now['y'] + 1}
    elif direc == RIGHT:
        loc = {'x':now['x'] + 1,'y':now['y']}
    elif direc == LEFT:
        loc = {'x':now['x'] - 1,'y':now['y']}
    return loc

#calculate distance between two points
def fdis(x,y):
    return abs(x['x']-y['x']) + abs(x['y'] - x['y'])

#virtual run
def vRun(snakeCoords, food,direction):
    snakeCoords = list(snakeCoords)
    food_eated = False
    #make virtual moves
    while not food_eated:
        caldis(snakeCoords,food)
        disDir = [inf] * 4
        # distance of 4 directions
        if canmove(snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'] - 1, snakeCoords):
            disDir[0] = dis[snakeCoords[HEAD]['y'] - 1][snakeCoords[HEAD]['x']]
        if canmove(snakeCoords[HEAD]['x'] + 1, snakeCoords[HEAD]['y'], snakeCoords):
            disDir[1] = dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] + 1]
        if canmove(snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'] + 1, snakeCoords):
            disDir[2] = dis[snakeCoords[HEAD]['y'] + 1][snakeCoords[HEAD]['x']]
        if canmove(snakeCoords[HEAD]['x'] - 1, snakeCoords[HEAD]['y'], snakeCoords):
            disDir[3] = dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] - 1]

        minNum = min(disDir)
        #choose direction for each move
        if disDir[0] < inf and dis[snakeCoords[HEAD]['y'] - 1][snakeCoords[HEAD]['x']] == minNum and direction != DOWN:
            direction = UP
        elif disDir[1] < inf and dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] + 1] == minNum and direction != LEFT:
            direction = RIGHT
        elif disDir[2] < inf and dis[snakeCoords[HEAD]['y'] + 1][snakeCoords[HEAD]['x']] == minNum and direction != UP:
            direction = DOWN
        elif disDir[3] < inf and dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] - 1] == minNum and direction != RIGHT:
            direction = LEFT
        #over
        if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
            return
        for snakeBody in snakeCoords[1:]:
            if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
                return
        # make move
        if direction == UP:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
        #eaten
        if snakeCoords[HEAD]['x'] != food['x'] or snakeCoords[HEAD]['y'] != food['y']:
            food_eated = True
            snakeCoords.insert(0, newHead)
        else:
            del snakeCoords[-1] # remove snake's tail segment
            snakeCoords.insert(0, newHead)
    #compare and select direction
    result = caldis(snakeCoords, snakeCoords[-1])
    for i in range(4):
        temp = dirCheck(snakeCoords[HEAD],DIRECTION[i])
        if temp['x'] == snakeCoords[-1]['x'] and temp['y'] == snakeCoords[-1]['y']:
            result = False
    return result

#random move
def randomMove(snake,food,direction):
    tempdir = direction
    mindis = inf
    used = [0] * 4
    cnt = 0
    loop = 0
    while True:
        loop += 1
        print(loop)
        cnt  = 0
        for i in range(4):
            cnt += used[i]
        if cnt == 4:
            return None
        while True:
            i = random.randint(0, 3)
            if used[i] == 0:
                break
        used[i] = 1
        temp = dirCheck(snake[0], DIRECTION[i])
        if canmove(temp['x'],temp['y'],snake) and (checkDir(DIRECTION[i], direction)):
                tempdir = DIRECTION[i]
                break
    return tempdir

#check direction conflict
def checkDir(temp , direction):
    if direction == UP:
        if temp == DOWN:
            return False
    elif direction == RIGHT:
        if temp == LEFT:
            return False
    elif direction == LEFT:
        if temp == RIGHT:
            return False
    elif direction == DOWN:
        if temp == UP:
            return False
    return True

#check if head movement is possible
def checkHead(snake,direction):
    for i in range(4):
        temp = dirCheck(snake[HEAD], DIRECTION[i])
        if canmove(temp['x'],temp['y'],snake) and checkDir(DIRECTION[i],direction):
            if dis[temp['y']][temp['x']] < inf:
                return True
    return False

#run the game
def runGame():

    global running_,DIRECTION
    # Set a random start point.
    startx = random.randint(0, CELLWIDTH -1)
    starty = random.randint(0, CELLHEIGHT -1)
    snakeCoords = [{'x': startx,     'y': starty}, {'x': startx - 1, 'y': starty}, {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    running_ = True

    food = getRandomLocation(snakeCoords)
    count = 0

    while True:
        if full(snakeCoords, food) == True:
            return

        #print("run")
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        newDir = None
        if caldis(snakeCoords,food):
            if vRun(snakeCoords, food, direction):
                # there is a possible way => make a move
                caldis(snakeCoords,food)
                disdir = [inf] * 4
                if canmove(snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'] - 1, snakeCoords):
                    disdir[0] = dis[snakeCoords[HEAD]['y'] - 1][snakeCoords[HEAD]['x']]
                if canmove(snakeCoords[HEAD]['x'] + 1, snakeCoords[HEAD]['y'], snakeCoords):
                    disdir[1] = dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] + 1]
                if canmove(snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'] + 1, snakeCoords):
                    disdir[2] = dis[snakeCoords[HEAD]['y'] + 1][snakeCoords[HEAD]['x']]
                if canmove(snakeCoords[HEAD]['x'] - 1, snakeCoords[HEAD]['y'], snakeCoords):
                    disdir[3] = dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] - 1]

                maxNum = min(disdir)

                if disdir[0] < inf and dis[snakeCoords[HEAD]['y'] - 1][snakeCoords[HEAD]['x']] == maxNum and direction != DOWN:
                    newDir = UP
                elif disdir[1] < inf and dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] + 1] == maxNum and direction != LEFT:
                    newDir = RIGHT
                elif disdir[2] < inf and dis[snakeCoords[HEAD]['y'] + 1][snakeCoords[HEAD]['x']] == maxNum and direction != UP:
                    newDir = DOWN
                elif disdir[3] < inf and dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] - 1] == maxNum and direction != RIGHT:
                    newDir = LEFT

                print("a possible road", newDir)
            else:
                count += 1
                disdir = [-1] * 4
                caldis(snakeCoords, snakeCoords[-1])
                if canmove(snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'] - 1, snakeCoords):
                    disdir[0] = dis[snakeCoords[HEAD]['y'] - 1][snakeCoords[HEAD]['x']]
                if canmove(snakeCoords[HEAD]['x'] + 1, snakeCoords[HEAD]['y'], snakeCoords):
                    disdir[1] = dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] + 1]
                if canmove(snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'] + 1, snakeCoords):
                    disdir[2] = dis[snakeCoords[HEAD]['y'] + 1][snakeCoords[HEAD]['x']]
                if canmove(snakeCoords[HEAD]['x'] - 1, snakeCoords[HEAD]['y'], snakeCoords):
                    disdir[3] = dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] - 1]
                maxNum = 0
                for i in disdir:
                    if i != inf:
                        if i > maxNum:
                            maxNum = i

                if disdir[0] > -1 and dis[snakeCoords[HEAD]['y'] - 1][snakeCoords[HEAD]['x']] == maxNum and direction != DOWN:
                    newDir = UP
                elif disdir[1] > -1 and dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] + 1] == maxNum and direction != LEFT:
                    newDir = RIGHT
                elif disdir[2] > -1 and dis[snakeCoords[HEAD]['y'] + 1][snakeCoords[HEAD]['x']] == maxNum and direction != UP:
                    newDir = DOWN
                elif disdir[3] > -1 and dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] - 1] == maxNum and direction != RIGHT:
                    newDir = LEFT
                if(count != 5):
                    print("longest way",newDir)
                if count == 5:
                    print("rand1")
                    newDir = randomMove(snakeCoords, food, direction)
                    print("randomway", newDir)
                    count = 0


        else:
            disdir = [-1] * 4
            caldis(snakeCoords, snakeCoords[-1])
            if canmove(snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'] - 1, snakeCoords):
                disdir[0] = dis[snakeCoords[HEAD]['y'] - 1][snakeCoords[HEAD]['x']]
            if canmove(snakeCoords[HEAD]['x'] + 1, snakeCoords[HEAD]['y'], snakeCoords):
                disdir[1] = dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] + 1]
            if canmove(snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'] + 1, snakeCoords):
                disdir[2] = dis[snakeCoords[HEAD]['y'] + 1][snakeCoords[HEAD]['x']]
            if canmove(snakeCoords[HEAD]['x'] - 1, snakeCoords[HEAD]['y'], snakeCoords):
                disdir[3] = dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] - 1]

            maxNum = 0
            for i in disdir:
                if i != inf:
                    if i > maxNum:
                        maxNum = i

            if disdir[0] > -1 and dis[snakeCoords[HEAD]['y'] - 1][snakeCoords[HEAD]['x']] == maxNum and direction != DOWN:
                newDir = UP
            elif disdir[1] > -1 and dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] + 1] == maxNum and direction != LEFT:
                newDir = RIGHT
            elif disdir[2] > -1 and dis[snakeCoords[HEAD]['y'] + 1][snakeCoords[HEAD]['x']] == maxNum and direction != UP:
                newDir = DOWN
            elif disdir[3] > -1 and dis[snakeCoords[HEAD]['y']][snakeCoords[HEAD]['x'] - 1] == maxNum and direction != RIGHT:
                newDir = LEFT
        if newDir == None:
            print("rand2")
            direction = randomMove(snakeCoords, food, direction)
            print("fianl rand",direction)
            if direction == None:
                return
        else:
            direction = newDir
            print(("final",direction))

        if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
            print("died for touching the border", direction)
            return
        for snakeBody in snakeCoords[1:]:
            print(snakeBody['x'],snakeBody['y'])
            if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
                print("died for touching the snake itself", direction)
                return
        #make move
        if direction == UP:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
        snakeCoords.insert(0, newHead) # set a new food somewhere
        # eaten
        if snakeCoords[HEAD]['x'] == food['x'] and snakeCoords[HEAD]['y'] == food['y']:
            food = getRandomLocation(snakeCoords)
        else:
            del snakeCoords[-1]
        #over
        DISPLAYSURF.fill(BGCOLOR)
        #draw
        drawSnaky(snakeCoords)
        drawFood(food)
        drawScore(len(snakeCoords) - 3)
        pygame.display.update()
        #pygame.time.wait(10 + len(snakeCoords))


#main
def main():
    global  DISPLAYSURF, BASICFONT

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snaky')

    showStartScreen()
    while True:
        runGame()
        showOver()

def drawPressKeyMsg():
    #ok
    pressKeySurf = BASICFONT.render('Press a key to start.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (120, 300)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    #ok
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    #mark = pygame.image.load("mole.png")
    titleSurf1 = titleFont.render('Snaky!', True, WHITE, DARKBLUE)
    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rect = [120, 200, 200, 200]
        DISPLAYSURF.blit(titleSurf1, rect)
        '''
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
        '''
        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation(snake):
    temp = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    while testStuck(temp, snake):
        temp = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    return temp


def testStuck(temp, snake):
    for body in snake:
        if temp['x'] == body['x'] and temp['y'] == body['y']:
            return True
    return False


def full(snake, food):
    length = len(snake)
    x = food['x']
    y = food['y']
    if ([x - 1, y] in snake and [x + 1, y] in snake and[x, y + 1] in snake and [x, y - 1] in snake) or (length == CELLWIDTH * CELLHEIGHT - 1):
        print("full screen!")
        gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
        gameSurf = gameOverFont.render('FULL SCREEN!', True, RED)
        gameRect = gameSurf.get_rect()
        gameRect.midtop = (WINDOWWIDTH / 2, 200)

        DISPLAYSURF.blit(gameSurf, gameRect)
        pygame.display.update()
        pygame.time.wait(500)
        return True
    return False


def showOver():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 75)
    gameSurf = gameOverFont.render('Opps!', True, BLACK)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)

    DISPLAYSURF.blit(gameSurf, gameRect)
    pygame.display.update()
    pygame.time.wait(500)
    #checkForKeyPress() # clear out any key presses in the event queue


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawSnaky(snakeCoords):
    cnt = 0
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        r = BLUE[0]
        g = BLUE[1]
        b = BLUE[2]
        rr = int(r + 100/len(snakeCoords) * cnt) % 256
        gg = int(g + 100/len(snakeCoords) * cnt) % 256
        bb = int(b - 100/len(snakeCoords) * cnt + 256) % 256
        pygame.draw.rect(DISPLAYSURF, (rr, gg, bb), snakeRect)
        cnt += 1

def drawFood(coord):
    #ok
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    foodRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, foodRect)

'''
def drawGrid():
    #ok
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, WHITE, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, WHITE, (0, y), (WINDOWWIDTH, y))

running_ = True
'''

if __name__ == '__main__':
    main()