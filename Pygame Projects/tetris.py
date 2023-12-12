import pygame
import random

borderName = "Tetris"

# Game Variables
resolution = (500, 600)
gameResolution = (11, 19)  # Min (3,5)
blockSize = 30
blockGap = blockSize / 15

gameticks = 750

# Game Blocks
blocks = {
    "redBlock": [
        ["n", "n", "x"],
        ["n", "x", "x"],
        ["n", "x", "n"],
    ],
    "orangeBlock": [
        ["n", "x", "n"],
        ["n", "x", "n"],
        ["x", "x", "n"],
    ],
    "greenBlock": [
        ["x", "n", "n"],
        ["x", "x", "n"],
        ["n", "x", "n"],
    ],
    "blueBlock": [
        ["n", "x", "n"],
        ["n", "x", "n"],
        ["n", "x", "x"],
    ],
    "cyanBlock": [
        ["n", "x", "n"],
        ["n", "x", "n"],
        ["n", "x", "n"],
    ],
    "yellowBlock": [
        ["n", "x", "x"],
        ["n", "x", "x"],
        ["n", "n", "n"],
    ],
    "purpleBlock": [
        ["n", "x", "n"],
        ["n", "x", "x"],
        ["n", "x", "n"],
    ],
}

pygame.init()
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution)

letters = ["r", "g", "b", "o", "p", "c", "y", "n"]

map = [["n" for _ in range(gameResolution[1])] for _ in range(gameResolution[0])]


# for j in range(7):
#     for i in range(gameResolution[0]):
#         map[i][gameResolution[1] - 1 - j] = random.choice(
#             ["r", "g", "b", "o", "p", "c", "y"]
#         )

# map[0][gameResolution[1] - 1 - 6] = "n"

# map[4][gameResolution[1] - 1 - 3] = "n"

# map[4][gameResolution[1] - 1] = "n"


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
            case "n":
                return "black"
        return "white"

    border = 10
    pygame.draw.rect(
        screen,
        "black",
        (
            (resolution[0] - gameResolution[0] * blockSize) // 2 - border,
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
                    (resolution[0] - gameResolution[0] * blockSize) // 2
                    + row * blockSize
                    + blockGap,
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
                if block[i][j] == "x":
                    map[j - 1 + gameResolution[0] // 2][i] = "x"
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
                ):  # if block is being played
                    map[gameResolution[0] - i - 1][gameResolution[1] - j - 2] = "n"
                    map[gameResolution[0] - i - 1][gameResolution[1] - j - 1] = "x"

    def convertBlocks():
        for j in range(gameResolution[1]):
            for i in range(gameResolution[0]):
                if map[gameResolution[0] - i - 1][gameResolution[1] - j - 2] == "x":
                    map[gameResolution[0] - i - 1][
                        gameResolution[1] - j - 2
                    ] = currentColour[0]

    # Checks last layer
    for i in range(gameResolution[0]):
        if map[i][gameResolution[1] - 1] == "x":
            convertBlocks()
            return True  # Blocks cannot move

    # Check if every Block **CAN** move
    moveBlock = True
    for j in range(gameResolution[1] - 1):
        for i in range(gameResolution[0]):
            block = map[gameResolution[0] - i - 1][gameResolution[1] - j - 2]
            underBlock = map[gameResolution[0] - i - 1][gameResolution[1] - j - 1]
            if block == "x":
                if not (underBlock == "n" or underBlock == "x"):
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
            if map[i][j] == "x":
                if i + direction < 0 or i + direction > gameResolution[0] - 1:
                    moveBlock = False
                else:
                    sideBlock = map[i + direction][j]
                    if not (sideBlock == "n" or sideBlock == "x"):
                        moveBlock = False

    if moveBlock:
        for j in range(gameResolution[1]):
            for i in range(gameResolution[0]):
                if direction > 0:
                    if map[gameResolution[0] - 1 - i][j] == "x":
                        map[gameResolution[0] - 1 - i][j] = "n"
                        map[gameResolution[0] - 1 - i + direction][j] = "x"
                else:
                    if map[i][j] == "x":
                        map[i][j] = "n"
                        map[i + direction][j] = "x"


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
        count = strrow.count("x") + strrow.count("n")

        if count == 0:
            for i in range(gameResolution[0]):
                map[i][gameResolution[1] - 1 - row] = "n"
            moveAllDown(gameResolution[1] - row)
            moved = True
            break

    if moved:
        checkfull()


def rotateBlocks():
    pass


placeBlock()
drawBlocks()

clock = pygame.time.Clock()
last = 0
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
                if updateBlocks():
                    checkfull()
                    if not placeBlock():
                        print("GAME OVER")

    # Game Functions

    current = pygame.time.get_ticks() // gameticks
    if current > last:
        last = current
        if updateBlocks():
            checkfull()
            if not placeBlock():
                print("GAME OVER")

    screen.fill("#313190")

    drawBlocks()
    pygame.display.flip()
    clock.tick(60)
