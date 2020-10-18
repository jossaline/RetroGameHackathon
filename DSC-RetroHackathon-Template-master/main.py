from random import random

import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1

BLOCK_SPEED = 1.0
bulletDirection = 0

bullets = []
blocks = []


class Game:
    # how big it is
    WIDTH = 160
    HEIGHT = 120

    def __init__(self):
        pyxel.init(self.WIDTH, self.HEIGHT, caption="Retro Game")  # The game screen will be 160x120 pixels
        self.scene = SCENE_TITLE
        self.player = None
        self.ended = False
        self.did_win = False
        self.new_game()
        pyxel.run(self.update, self.draw)  # Run the game

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        # elif self.scene == SCENE_GAMEOVER:
        #     self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY

    def new_game(self):  # Creates a new game
        self.player = Player()
        self.ended = False

        bullets.clear()  # Remove any bullets that have been left behind
        blocks.clear()  # Remove any blocks that have been left behind
        for x in range(0, self.WIDTH, Block.WIDTH * 2):  # The blocks are placed 1 block width apart
            blocks.append(Block(x, 1))

    def update_play_scene(self):
        if self.ended:  # If the game is over, nothing should be able to move
            if pyxel.btn(pyxel.KEY_ENTER):
                self.new_game()
            return

        self.player.update()
        for b in bullets:
            b.update()
        for b in blocks:
            b.update(self)

    def draw(self):
        pyxel.cls(0)

        # self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        # elif self.scene == SCENE_GAMEOVER:
        #     self.draw_gameover_scene()

    def draw_title_scene(self):
        pyxel.text(10, 10, "KAREN Simulator: 2020 Edition", pyxel.frame_count % 16)
        pyxel.text(10, 20, "A Pyxel Shooter", pyxel.frame_count % 16)
        pyxel.text(10, 30, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_BLACK)  # Make the background black
        self.player.draw()  # Draw the player
        for b in blocks:  # Draw the blocks
            b.draw()
        for b in bullets:  # Draw the bullets
            b.draw()
        if self.ended:
            pyxel.text(10, 10, "You Won!" if self.did_win else "Game Over!",
                       pyxel.COLOR_GREEN if self.did_win else pyxel.COLOR_RED)
            pyxel.text(10, 20, "Press ENTER to play again...", pyxel.COLOR_WHITE)

    def won(self):
        self.did_win = True
        self.ended = True

    def lost(self):
        self.did_win = False
        self.ended = True


class Player:
    RECHARGE_TIME = 5

    def __init__(self):
        self.x = 100  # Player starts at (100, 100)
        self.y = 100
        self.recharge = 0
        self.direction = 0

    def update(self):
        # Move depending on which keys the player moves
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        elif pyxel.btn(pyxel.KEY_UP):
            # rotates right (clockwise)
            if 0 <= self.direction < 3:
                self.direction += 1
            else:
                self.direction = 0
        elif pyxel.btn(pyxel.KEY_DOWN):
            # rotates left (anti-clockwise)
            if 0 < self.direction <= 3:
                self.direction -= 1
            else:
                self.direction = 3
        global bulletDirection
        bulletDirection = self.direction

        if pyxel.btn(pyxel.KEY_SPACE) and self.recharge == 0:  # Player can only shoot when the recharge time is at 0
            bullets.append(Bullet(self.x, self.y, 0, -1))
            self.recharge = self.RECHARGE_TIME
        self.recharge = max(0, self.recharge - 1)  # Recharge timer goes down until it hits 0

    def draw(self):
        # Draw a triangle shape around the player's position
        # pyxel.tri(self.x, self.y, self.x - 2, self.y + 2, self.x + 2, self.y + 2, pyxel.COLOR_DARKBLUE)
        if self.direction == 0:
            pyxel.tri(self.x, self.y, self.x - 2, self.y + 2, self.x + 2, self.y + 2, pyxel.COLOR_DARKBLUE)
        elif self.direction == 1:
            pyxel.tri(self.x, self.y, self.x - 2, self.y - 2, self.x - 2, self.y + 2, pyxel.COLOR_DARKBLUE)
        elif self.direction == 2:
            pyxel.tri(self.x, self.y, self.x + 2, self.y - 2, self.x - 2, self.y - 2, pyxel.COLOR_DARKBLUE)
        elif self.direction == 3:
            pyxel.tri(self.x, self.y, self.x + 2, self.y - 2, self.x + 2, self.y + 2, pyxel.COLOR_DARKBLUE)


class Bullet:

    def __init__(self, x, y, width_x, height_y):
        self.x = x
        self.y = y
        self.width_x = width_x
        self.height_y = height_y
        self.direction = bulletDirection

    def update(self):
        if self.direction == 0:
            # self.x += self.width_x
            self.y += self.height_y
        elif self.direction == 1:
            self.x += self.width_x
            # self.y += self.height_y
        elif self.direction == 2:
            # self.x += self.width_x
            self.y -= self.height_y
        elif self.direction == 3:
            self.x -= self.width_x
            # self.y += self.height_y

        if self.y < 0:
            bullets.remove(self)


    def draw(self):
        if self.direction == 0:
            pyxel.rect(self.x, self.y, 1, 1, pyxel.COLOR_WHITE)
        if self.direction == 1:
            pyxel.rect(self.x + 2, self.y, 1, 1, pyxel.COLOR_WHITE)
        if self.direction == 2:
            pyxel.rect(self.x, self.y + 2, 1, 1, pyxel.COLOR_WHITE)
        if self.direction == 3:
            pyxel.rect(self.x - 2, self.y, 1, 1, pyxel.COLOR_WHITE)


class Block:
    WIDTH = 5
    HEIGHT = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.offset = int(random() * 60)
        self.alive = True

    def update(self, game):
        self.y += 0.1  # Blocks fall down
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += BLOCK_SPEED
            # self.dir = 1
        else:
            self.x -= BLOCK_SPEED
            # self.dir = -1

        if self.y > pyxel.height - 1:
            self.alive = False

        if self.y + self.WIDTH >= Game.HEIGHT:
            game.lost()  # If a game hits the bottom, then you've lost!

        for b in bullets:
            if (self.x <= b.x <= self.x + self.WIDTH) and (self.y <= b.y <= self.y + self.HEIGHT):
                bullets.remove(b)
                blocks.remove(self)
                if len(blocks) == 0:
                    game.won()  # If all the blocks are destroyed, then you win the game!

    def draw(self):
        pyxel.rect(self.x, self.y, self.WIDTH, self.HEIGHT, pyxel.COLOR_WHITE)


Game()
