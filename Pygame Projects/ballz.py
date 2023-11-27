import pygame
import random
import math

resolution = (320, 600)
borderName = "Ballz"

pygame.init()
pygame.display.set_caption(borderName)
screen = pygame.display.set_mode(resolution)


class ball(pygame.sprite.Sprite):
    def __init__(self, colour, x, y, mousepos):
        super().__init__()

        self.width = 10
        self.height = 10

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.actualx = self.rect.centerx * 100
        self.actualy = self.rect.centery * 100

        v = [mousepos[0] * 100 - self.actualx, mousepos[1] * 100 - self.actualy]
        magnitude = int(math.sqrt((v[0] ** 2 + v[1] ** 2)))
        direction = [v[0] / magnitude, v[1] / magnitude]
        self.direction = direction

    def update(self):
        self.actualx += (score // 20 + 1) * 3 * int(self.direction[0] * 100)
        self.actualy += (score // 20 + 1) * 3 * int(self.direction[1] * 100)

        self.rect.centerx = self.actualx / 100
        self.rect.centery = self.actualy / 100

        if self.rect.centerx > resolution[0] - 5 or self.rect.centerx < 5:
            self.direction[0] *= -1
        if self.rect.y < 50:
            self.direction[1] *= -1
        if self.rect.y > resolution[1] - 35:
            finalballpos.append(self.rect.centerx)
            self.kill()

        for block in pygame.sprite.spritecollide(self, blocks, 0):
            if abs(self.rect.centerx - block.rect.centerx) <= abs(
                self.rect.centery - block.rect.centery
            ):
                self.direction[1] *= -1
            else:
                self.direction[0] *= -1
            block.health -= 1


class block(pygame.sprite.Sprite):
    def __init__(self, colour, x, y, health):
        super().__init__()
        self.width = 42
        self.height = 42
        self.image = pygame.Surface((self.width, self.height))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.health = health
        self.text = pygame.font.SysFont("centurygothic", 25).render(
            ascii(self.health), True, "Black"
        )

    def update(self):
        if self.rect.bottom > 565:
            exit()
        if self.health < 1:
            self.kill()
        self.image.fill(self.colour)
        self.text = pygame.font.SysFont("centurygothic", 25).render(
            ascii(self.health), True, "Black"
        )
        self.image.blit(
            self.text,
            (
                (self.width - self.text.get_width()) / 2,
                (self.height - self.text.get_height()) / 2,
            ),
        )


class coin(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        super().__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.health = 1

    def update(self):
        global ballNumber
        for ball in pygame.sprite.spritecollide(self, balls, 0):
            self.health -= 1
        if self.health < 1:
            ballNumber += 1
            self.kill()
        if self.rect.bottom > 560:
            self.kill()


balls = pygame.sprite.Group()
blocks = pygame.sprite.Group()
coins = pygame.sprite.Group()


def generateBall(mousepos):
    balls.add(ball("white", startpos[0], startpos[1], mousepos))


def moveBlocks():
    for i in blocks:
        i.rect.y += 45
        screen.fill("black")
        blocks.draw(screen)
    for i in coins:
        i.rect.y += 45
        screen.fill("black")
        coins.draw(screen)
    for i in range(7):
        n = random.randint(1, 10)
        if n >= 7:
            blocks.add(
                block(
                    "white",
                    25 + i * 45,
                    120,
                    random.randint(score + 1, score + 2),
                )
            )
        elif n == 1:
            coins.add(
                coin(
                    "white",
                    25 + i * 45,
                    120,
                )
            )


# Game Setup
for i in range(7):
    for j in range(2):
        n = random.randint(1, 15)
        if n >= 10:
            blocks.add(
                block(
                    "white",
                    25 + i * 45,
                    120 + j * 45,
                    random.randint(1, 2),
                )
            )
        elif n == 1:
            coins.add(
                coin(
                    "white",
                    25 + i * 45,
                    120 + j * 45,
                )
            )

# Game Variables
simulating = False
score = 1
ballNumber = 3
startpos = [resolution[0] // 2, resolution[1] - 30]
queue = []
finalballpos = []

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not simulating:
                mousepos = pygame.mouse.get_pos()
                for i in range(ballNumber):
                    queue.append(
                        ("ball", int(pygame.time.get_ticks() + i * 200), mousepos)
                    )
                simulating = True

    if len(queue) != 0:
        for i in queue:
            if i[1] < int(pygame.time.get_ticks()):
                if i[0] == "ball":
                    generateBall(i[2])
                    queue.pop(0)

    while simulating and len(queue) == 0 and len(balls) == 0:
        moveBlocks()
        score += 1

        if 5 < finalballpos[0] < resolution[0] - 5:
            startpos[0] = finalballpos[0]
        else:
            if abs(5 - finalballpos[0]) < abs((resolution[0] - 5) - finalballpos[0]):
                startpos[0] = 5
            else:
                startpos[0] = resolution[0] - 5

        finalballpos = []
        simulating = False

    # Update all sprites
    balls.update()
    blocks.update()
    coins.update()

    # Draw all items to the screen
    screen.fill("#313131")
    pygame.draw.rect(
        screen,
        "black",
        pygame.Rect(0, 50, resolution[0], resolution[1] - 75),
    )
    balls.draw(screen)
    blocks.draw(screen)
    coins.draw(screen)

    scoretext = pygame.font.SysFont("centurygothic", 30).render(
        f"{score}", True, "white"
    )
    screen.blit(scoretext, ((resolution[0] - scoretext.get_width()) / 2, 7))

    if simulating:
        if len(finalballpos) != 0:
            pygame.draw.rect(
                screen,
                "white",
                pygame.Rect(finalballpos[0], startpos[1] - 5, 10, 10),
            )

    if not simulating:
        ballText = pygame.font.SysFont("centurygothic", 17).render(
            f"x{ballNumber}", True, "white"
        )
        screen.blit(ballText, (startpos[0] + 10, startpos[1] - 20))

        pygame.draw.line(
            screen,
            "white",
            (startpos[0] + 5, startpos[1]),
            (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),
            2,
        )
        pygame.draw.rect(
            screen,
            "white",
            pygame.Rect(startpos[0], startpos[1] - 5, 10, 10),
        )

    pygame.display.flip()
    clock.tick(120)
