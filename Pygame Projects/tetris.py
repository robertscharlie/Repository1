import pygame
import random

borderName = "Tetris"

# Game Variables
resolution = (600, 600)
gameResolution = (11, 19)  # Min (3,5)
blockSize = 30
blockGap = blockSize / 15

gameticks = 750
score = 0
linesCleared = 0
level = 1
border = 10


def font(size):
    return pygame.font.SysFont("centurygothic", size)


# Game Blocks
blocks = {
    "redBlock": [
        ["n", "n", "x"],
        ["n", "m", "x"],
        ["n", "x", "n"],
    ],
    "orangeBlock": [ 
        ["n", "x", "n"],
        ["n", "m", "n"],
        ["x", "x", "n"],
    ],
    "greenBlock": [
        ["x", "n", "n"],
        ["x", "m", "n"],
        ["n", "x", "n"],
    ],
    "blueBlock": [
        ["n", "x", "n"],
        ["n", "m", "n"],
        ["n", "x", "x"],
    ],
    "cyanBlock": [
        ["n", "x", "n"],
        ["n", "m", "n"],
        ["n", "x", "n"],
    ],
    "yellowBlock": [
        ["n", "x", "x"],
        ["n", "m", "x"],
        ["n", "n", "n"],
    ],
    "purpleBlock": [
        ["n", "x", "n"],
        ["n", "m", "x"],
        ["n", "x", "n"],
    ],
}

pygame.init()
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution)

letters = [
    "r",
    "g",
    "b",
    "o",
    "p",
    "c",
    "y",
    "n",
]

map = [["n" for _ in range(gameResolution[1])] for _ in range(gameResolution[0])]


def drawBlocks():
    def tocolour(letter):
        match letter:
            case "r":
                return "red"
            case "g":
                return "green"
            case "b":
                return "blue"
            case "c":
                return "cyan"
            case "o":
                return "orange"
            case "p":
                return "purple"
            case "y":
                return "yellow"
            case "x":
                return currentColour
            case "m":
                return currentColour
            case "n":
                return "black"
        return "white"

    pygame.draw.rect(
        screen,
        "black",
        (
            border,
            (resolution[1] - gameResolution[1] * blockSize) // 2 - border,
            2 * border + blockSize * gameResolution[0],
            2 * border + blockSize * gameResolution[1],
        ),
    )
    for row in range(gameResolution[0]):
        for column in range(gameResolution[1]):
            pygame.draw.rect(
                screen,
                tocolour(map[row][column]),
                (
                    border + row * blockSize + blockGap,
                    (resolution[1] - gameResolution[1] * blockSize) // 2
                    + column * blockSize
                    + blockGap,
                    blockSize - 2 * blockGap,
                    blockSize - 2 * blockGap,
                ),
                0,
                2,
            )


def placeBlock():
    colour = random.choice(
        ["red", "orange", "green", "blue", "cyan", "yellow", "purple"]
    )
    block = blocks[colour + "Block"]

    global currentColour
    currentColour = colour

    place = True

    for i in range(3):
        for j in range(3):
            if map[j - 1 + gameResolution[0] // 2][i] != "n":
                place = False

    if place:
        for i in range(3):
            for j in range(3):
                if block[i][j] == "x" or block[i][j] == "m":
                    map[j - 1 + gameResolution[0] // 2][i] = block[i][j]
        return True
    else:
        return False


def updateBlocks():
    def moveBlocks():
        for j in range(gameResolution[1] - 1):
            for i in range(gameResolution[0]):
                # Checks every block
                if (
                    map[gameResolution[0] - i - 1][gameResolution[1] - j - 2] == "x"
                    or map[gameResolution[0] - i - 1][gameResolution[1] - j - 2] == "m"
                ):  # if block is being played
                    map[gameResolution[0] - i - 1][gameResolution[1] - j - 1] = map[
                        gameResolution[0] - i - 1
                    ][gameResolution[1] - j - 2]
                    map[gameResolution[0] - i - 1][gameResolution[1] - j - 2] = "n"

    def convertBlocks():
        for j in range(gameResolution[1]):
            for i in range(gameResolution[0]):
                if (
                    map[gameResolution[0] - i - 1][gameResolution[1] - j - 2] == "x"
                    or map[gameResolution[0] - i - 1][gameResolution[1] - j - 2] == "m"
                ):
                    map[gameResolution[0] - i - 1][
                        gameResolution[1] - j - 2
                    ] = currentColour[0]

    # Checks last layer
    for i in range(gameResolution[0]):
        if map[i][gameResolution[1] - 1] == "x" or map[i][gameResolution[1] - 1] == "m":
            convertBlocks()
            return True  # Blocks cannot move

    # Check if every Block **CAN** move
    moveBlock = True
    for j in range(gameResolution[1] - 1):
        for i in range(gameResolution[0]):
            block = map[gameResolution[0] - i - 1][gameResolution[1] - j - 2]
            underBlock = map[gameResolution[0] - i - 1][gameResolution[1] - j - 1]
            if block == "x" or block == "m":
                if not (underBlock == "n" or underBlock == "x" or underBlock == "m"):
                    moveBlock = False

    if moveBlock:
        moveBlocks()
    else:
        convertBlocks()
        return True


def shiftBlocks(direction):
    if direction == 0:
        return False

    moveBlock = True
    for j in range(gameResolution[1]):
        for i in range(gameResolution[0]):
            if map[i][j] == "x" or map[i][j] == "m":
                if i + direction < 0 or i + direction > gameResolution[0] - 1:
                    moveBlock = False
                else:
                    sideBlock = map[i + direction][j]
                    if not (sideBlock == "n" or sideBlock == "x" or sideBlock == "m"):
                        moveBlock = False

    if moveBlock:
        for j in range(gameResolution[1]):
            for i in range(gameResolution[0]):
                if direction > 0:
                    if (
                        map[gameResolution[0] - 1 - i][j] == "x"
                        or map[gameResolution[0] - 1 - i][j] == "m"
                    ):
                        map[gameResolution[0] - 1 - i + direction][j] = map[
                            gameResolution[0] - 1 - i
                        ][j]
                        map[gameResolution[0] - 1 - i][j] = "n"
                else:
                    if map[i][j] == "x" or map[i][j] == "m":
                        map[i + direction][j] = map[i][j]
                        map[i][j] = "n"


def checkfull():
    moved = False

    def moveAllDown(rowstart):
        for j in range(rowstart - 1):
            for i in range(gameResolution[0]):
                map[i][rowstart - j - 1] = map[i][rowstart - j - 2]
                map[i][rowstart - j - 2] = "n"

    for row in range(gameResolution[1]):
        strrow = ""
        for i in range(gameResolution[0]):
            strrow += map[i][gameResolution[1] - row - 1]
        count = strrow.count("x") + strrow.count("m") + strrow.count("n")

        if count == 0:
            for i in range(gameResolution[0]):
                map[i][gameResolution[1] - 1 - row] = "n"
            moveAllDown(gameResolution[1] - row)
            moved = True
            break

    if moved:
        global score
        score += 100
        checkfull()


def rotateBlocks():
    rotate = True

    # Get indexes of 3x3 of blocks
    listIndexes = []
    listElements = []
    for j in range(gameResolution[1]):
        for i in range(gameResolution[0]):
            if map[i][j] == "m":
                if i == 0 or i == gameResolution[0] + 1:
                    rotate = False
                try:
                    for k in range(3):
                        listIndexesTemp = []
                        listElementsTemp = []
                        for l in range(3):
                            listIndexesTemp.append([i - 1 + k, j - 1 + l])
                            listElementsTemp.append(map[i - 1 + k][j - 1 + l])
                        listIndexes.append(listIndexesTemp)
                        listElements.append(listElementsTemp)
                except IndexError:
                    rotate = False

    for each in listElements:
        for element in each:
            if element != "x" and element != "m" and element != "n":
                rotate = False

    if rotate:
        transposed = list(zip(*listElements))[::-1]
        rotated_matrix = [list(row) for row in transposed]
        for e in range(len(listIndexes)):
            for r in range(3):
                map[listIndexes[e][r][0]][listIndexes[e][r][1]] = rotated_matrix[e][r]


def gameUpdate():
    if updateBlocks():
        checkfull()
    if not placeBlock():
        print("GAME OVER")


placeBlock()
drawBlocks()


clock = pygame.time.Clock()
last = 0
downHeld = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shiftBlocks(-1)
            elif event.key == pygame.K_RIGHT:
                shiftBlocks(1)
            if event.key == pygame.K_DOWN:
                last -= 1
                downHeld = True
                # print("down")
            if event.key == pygame.K_UP:
                rotateBlocks()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                downHeld = False

    # Game Functions

    current = pygame.time.get_ticks() // gameticks
    if current > last or downHeld:
        last = current
        if updateBlocks():
            checkfull()
            pygame.time.delay(150)
            if not placeBlock():
                print("GAME OVER")

    # Draw all elements to Screen

    screen.fill("#313190")
    drawBlocks()

    scoretext = font(30).render(f"Score: {score}", True, "white")
    screen.blit(scoretext, ((3 * border + blockSize * gameResolution[0] + 10, 7)))

    pygame.display.flip()
    clock.tick(30)
