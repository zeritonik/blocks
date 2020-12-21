import pygame
from random import randint

pygame.font.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

BLOCK = 30


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.left = 5
        self.right = 5
        self.top = 50
        self.bottom = 5

        self.rect = pygame.Rect(self.left, self.top, self.width * BLOCK, self.height * BLOCK)

        self.rects = [[], []]

    def get_cell(self, pos):
        if pos[0] not in range(self.left, self.left + self.rect.width) or pos[1] not in range(self.top, self.top + self.rect.height):
            return None
        else:
            return (pos[0] - self.left) // BLOCK, (pos[1] - self.top) // BLOCK

    def add_rect(self, pos, sides, n):
        if not self.rects[n]:
            if n == 0:
                rect = pygame.Rect(self.left, self.top, sides[0] * BLOCK, sides[1] * BLOCK)
            elif n == 1:
                rect = pygame.Rect(self.left + self.rect.width - sides[0] * BLOCK, self.top + self.rect.height - sides[1] * BLOCK, sides[0] * BLOCK, sides[1] * BLOCK)
            self.rects[n].append(rect)
            return True
        pos = self.get_cell(pos)
        if pos:
            rect = pygame.Rect(self.left + pos[0] * BLOCK, self.top + pos[1] * BLOCK, sides[0] * BLOCK, sides[1] * BLOCK)
            if not self.rect.contains(rect):
                return False
            for i in self.rects:
                if rect.collidelist(i) != -1:
                    return False
            else:
                for i in self.rects[n]:
                    if rect.left in range(i.left, i.right + 1) or rect.right in range(i.left, i.right + 1):
                        if rect.top == i.bottom or rect.bottom == i.top:
                            self.rects[n].append(rect)
                            return True
                    if rect.top in range(i.top, i.bottom + 1) or rect.bottom in range(i.top, i.bottom + 1):
                        if rect.left == i.right or rect.right == i.left:
                            self.rects[n].append(rect)
                            return True
        return False

    def draw_field(self, window):
        pygame.draw.rect(window, BLACK, self.rect, 1)

        for i in range(self.top + BLOCK, self.top + self.rect.height, BLOCK):
            pygame.draw.line(window, BLACK, (self.left, i), (self.left + self.rect.width - 1, i))
        for i in range(self.left + BLOCK, self.left + self.rect.width, BLOCK):
            pygame.draw.line(window, BLACK, (i, self.top), (i, self.top + self.rect.height - 1))

    def show_rect(self, window, color, pos, sides):
        pos = self.get_cell(pos)
        if pos:
            pygame.draw.rect(window, color, (self.left + pos[0] * BLOCK, self.top + pos[1] * BLOCK, sides[0] * BLOCK, sides[1] * BLOCK), 4)

    def draw_rects(self, window):
        for i in self.rects[0]:
            pygame.draw.rect(window, RED, i)
        for i in self.rects[1]:
            pygame.draw.rect(window, BLUE, i)

    def get_size(self):
        return self.left + self.right + self.rect.width, self.top + self.bottom + self.rect.height

    def get_max_s(self):
        return self.width * self.height

    def blit_sides(self, window, sides, color):
        text = FONT.render(f'{sides[0]}, {sides[1]}', 0, color)
        window.blit(text, (self.rect.width // 2 - FONT.get_height(), self.top // 2))

    def blit_s(self, window, s):
        s0 = FONT.render(str(s[0]), 0, RED)
        s1 = FONT.render(str(s[1]), 0, BLUE)
        window.blit(s0, (self.left, 10))
        window.blit(s1, (self.left + self.rect.width - s1.get_width(), 10))


class Game:
    def __init__(self, field, colors=(RED, BLUE)):
        self.player = randint(0, 1)
        self.colors = colors
        self.field = field

    def game_cycle(self, window, clock):
        s = [0, 0]

        game = True
        sides = None
        while game:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if sides and self.field.add_rect(event.pos, sides, self.player):
                        s[self.player] += sides[0] * sides[1]
                        sides = None
                        self.player ^= 1
                        game = self.check_win(s)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not sides:
                        sides = [randint(1, 6), randint(1, 6)]
                    elif event.key == pygame.K_SPACE:
                        sides = [randint(1, 6), randint(1, 6)]
                        self.player ^= 1

            window.fill(WHITE)
            
            self.field.draw_field(window)
            self.field.draw_rects(window)
            self.field.blit_s(window, s)

            if sides:
                self.field.blit_sides(window, sides, self.colors[self.player])
                self.field.show_rect(window, GREEN, pygame.mouse.get_pos(), sides)

            pygame.display.flip()

    def check_win(self, s):
        if sum(s) == self.field.get_max_s():
            if s[0] > s[1]:
                print('Winner: player 1!')
            elif s[1] > s[0]:
                print('Winner: player 2!')
            else:
                print('Draw!')
            return False
        return True


field = Field(20, 20)
game = Game(field)

FONT = pygame.font.Font(None, 30)
window = pygame.display.set_mode(field.get_size())
pygame.display.set_caption('Blocks')
clock = pygame.time.Clock()

game.game_cycle(window, clock)
pygame.quit()
input()