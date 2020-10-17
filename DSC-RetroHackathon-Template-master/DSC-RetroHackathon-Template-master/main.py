import pyxel

bullets = []
blocks = []


class Game:
    WIDTH = 160
    HEIGHT = 120

    def __init__(self):
        pyxel.init(self.WIDTH, self.HEIGHT, caption="Retro Game")  # The game screen will be 160x120 pixels
        self.player = None
        self.ended = False
        self.did_win = False
        self.new_game()
        pyxel.run(self.update, self.draw)  # Run the game

    def new_game(self):  # Creates a new game
        self.player = Player()
        self.ended = False

        bullets.clear()  # Remove any bullets that have been left behind
        blocks.clear()  # Remove any blocks that have been left behind
        for x in range(0, self.WIDTH, Block.WIDTH * 2):  # The blocks are placed 1 block width apart
            blocks.append(Block(x, 1))

    def update(self):
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

    def update(self):
        # Move depending on which keys the player moves
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        elif pyxel.btn(pyxel.KEY_UP):
            self.y -= 1
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += 1

        if pyxel.btn(pyxel.KEY_SPACE) and self.recharge == 0:  # Player can only shoot when the recharge time is at 0
            bullets.append(Bullet(self.x, self.y, 0, -1))
            self.recharge = self.RECHARGE_TIME
        self.recharge = max(0, self.recharge - 1)  # Recharge timer goes down until it hits 0

    def draw(self):
        # Draw a triangle shape around the player's position
        pyxel.tri(self.x, self.y, self.x - 2, self.y + 2, self.x + 2, self.y + 2, pyxel.COLOR_DARKBLUE)


class Bullet:
    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.y < 0:
            bullets.remove(self)

    def draw(self):
        pyxel.rect(self.x, self.y, 1, 1, pyxel.COLOR_WHITE)


class Block:
    WIDTH = 5
    HEIGHT = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, game):
        self.y += 0.2  # Blocks fall down

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
