---
title: "A simple game - part 2"
summary: "Animation, sprites and interactivity"
icon: sports_esports
publish: true
---
# A simple game: Acorn Highway (Part 2)

So having followed Tutorial 3, you should have a working, if ugly and speedy, platformer made of coloured blocks. Let's get it looking really good. First of all, here's the code you should have in your app by the end of the last tutorial:

```simulator
import qwstpad
import random


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAMEOVER = 3


class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False

    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False

    def is_airborne(self):
        airborne = True
        for platform in platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or controls["DROP"]:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

            if controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0: self.vx -= 0.5
            elif self.vx < 0: self.vx += 0.5

        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True

    def draw(self):
        screen.pen = color.red
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))

    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1

        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        global platforms
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False

    def draw(self):
        screen.pen = color.blue
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class acorn_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


def draw_score():
    global score
    screen.text(str(score), 0, 0)


def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None


def parse_controls():
    global controls, gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()

    if gamepad:
        controls["MOVE_LEFT"] = gamepad.held("L")
        controls["MOVE_RIGHT"] = gamepad.held("R")
        controls["DROP"] = gamepad.held("D") and gamepad.pressed("A")
        controls["JUMP"] = gamepad.pressed("A")
        controls["JUMP_LEFT"] = gamepad.held("L") and gamepad.pressed("A")
        controls["JUMP_RIGHT"] = gamepad.held("R") and gamepad.pressed("A")
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["JUMP_LEFT"] = badge.held(BUTTON_A) and badge.pressed(BUTTON_C)
        controls["JUMP_RIGHT"] = badge.held(BUTTON_B) and badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


gamepad = None
controls = {}

foreground_scroll_speed = 4

player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0

init_gamepad()
init_platforms()

def title_loop():
    global current_game_state

    screen.text("Title screen", 0, 0)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY

def gameplay_loop():
    global current_game_state

    player.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM

def death_anim_loop():
    global current_game_state

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER

def game_over_loop():
    global current_game_state, score

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        current_game_state = game_state.TITLE

def update():
    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()


run(update)
```

If you've got that in `__init__.py` in your app folder, along with an `icon.png` and an `assets` folder, you're ready to go.

# The Background

The first thing we're going to add is a background, and for that we'll need artwork. We'll provide the artwork you need to make Acorn Highway, but of course if you want to replace it with your own feel free! Once you have each file either saved from this tutorial or created yourself, just drop it into your app's `assets` folder as you go along.

![Acorn Highway background](/tut4_res/background.png)

You might notice that this and the other images we'll get into look a lot like the ones already found on your Tufty in the `assets/squirrel-sprites` folder, and they are indeed very similar. But we've made some alterations to those files for use in this game, so you'll want to use the versions provided here. For example, the above background image is extended by 20 pixels and seamlessly tiles with itself horizontally. That's a really good thing for this game, as we're going to have the background scroll past at a different rate to the platforms, to give a parallax effect.

To do that, we'll first load in the image. We'll need to do this with quite a few assets, so let's load them all in in the same place, right after we've defined all the methods and before initialising the gamepad and controls:

```python-raw
background = image.load("assets/background.png")
```

Now, let's create a method to draw that background. We'll put it right before `draw_score()`, and right at the moment we're just going to draw the image to the screen:

```python-raw
def draw_background():
    screen.blit(background, vec2(0, 0))
```

Then finally we can call that in the gameplay loop method, right after the globals:

```python-raw
def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM
```

## Scrolling the background

Now you'll see that the background displays behind the action when you're playing. But we don't want it to be static like that. Let's define a scroll speed for the background - the platforms are moving past at 4 pixels every frame, so let's have the background go at a leisurely one pixel per frame. We'll define this right after the foreground scroll speed. At the same time, we'll also want to put in a variable that keeps track of how much the background has scrolled, so we can loop it:

```python-raw
background = image.load("assets/background.png")

gamepad = None
controls = {}

foreground_scroll_speed = 4
background_scroll_speed = 1
background_scroll_amount = 0

player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0
```

And we'll alter `draw_background()` to utilise those:

```python-raw
def draw_background():
    global background_scroll_amount

    background_scroll_amount -= background_scroll_speed

    screen.blit(background, vec2(background_scroll_amount, 0))
```

Now you'll see that the background scrolls, but of course it's just scrolling off the edge of the screen. You might notice as well how much the game speeds up once the background is off the screen - that's the processing cost of using full screen images, but as long as it stays smooth and consistent that's the most important thing we're looking for.

We just need a single line of code to get the scroll to repeat - if we use the modulo operator (`%`), we can get it to loop around every time `background_scroll_amount` goes below minus 180, the width of the background image.

```python-raw
def draw_background():
    global background_scroll_amount

    background_scroll_amount -= background_scroll_speed
    background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_scroll_amount, 0))
```

Now it's repeating, but obviously still scrolling off the edge of the screen. So what to do? Simple! Draw a second copy of the background exactly where the first one ends.

```python-raw
def draw_background():
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    background_scroll_amount -= background_scroll_speed
    background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))
```

Great, that's a repeating scrolling background. But you'll notice that it only appears in the gameplay loop, as soon as you die it'll disappear. So let's call the background method in the death animation loop.

```python-raw
def death_anim_loop():
    global current_game_state

    draw_background()

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER
```

That's good, but the platforms stop scrolling when you die and right now the background keeps on going. There's an easy fix for that, we'll just add a parameter to `draw_background()` to just set whether we want it to scroll or not. So we'll alter `draw_background()` as follows:

```python_raw
def draw_background(scroll=True):
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    if scroll:
        background_scroll_amount -= background_scroll_speed
        background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))
```

We've set `scroll` to default to True, so we only need to include it when called if we _don't_ want the background to scroll. The method then just checks `scroll` and only moves the background if it's True. Then all we have to do is change the line in our death animation loop:

```python-raw
    draw_background(False)
```

And we're done - the background stops scrolling when the platform does. Here's the full code up to now.

```python
import qwstpad
import random


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAMEOVER = 3


class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False

    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False

    def is_airborne(self):
        airborne = True
        for platform in platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or controls["DROP"]:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

            if controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0: self.vx -= 0.5
            elif self.vx < 0: self.vx += 0.5

        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True

    def draw(self):
        screen.pen = color.red
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))

    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1

        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        global platforms
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False

    def draw(self):
        screen.pen = color.blue
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class acorn_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


def draw_background(scroll=True):
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    if scroll:
        background_scroll_amount -= background_scroll_speed
        background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))


def draw_score():
    global score
    screen.text(str(score), 0, 0)


def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None


def parse_controls():
    global controls, gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()

    if gamepad:
        controls["MOVE_LEFT"] = gamepad.held("L")
        controls["MOVE_RIGHT"] = gamepad.held("R")
        controls["DROP"] = gamepad.held("D") and gamepad.pressed("A")
        controls["JUMP"] = gamepad.pressed("A")
        controls["JUMP_LEFT"] = gamepad.held("L") and gamepad.pressed("A")
        controls["JUMP_RIGHT"] = gamepad.held("R") and gamepad.pressed("A")
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["JUMP_LEFT"] = badge.held(BUTTON_A) and badge.pressed(BUTTON_C)
        controls["JUMP_RIGHT"] = badge.held(BUTTON_B) and badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]

background = image.load("assets/background.png")

gamepad = None
controls = {}

foreground_scroll_speed = 4
background_scroll_speed = 1
background_scroll_amount = 0

player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0

init_gamepad()
init_platforms()

def title_loop():
    global current_game_state

    screen.text("Title screen", 0, 0)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY

def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM

def death_anim_loop():
    global current_game_state

    draw_background(False)

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER

def game_over_loop():
    global current_game_state, score

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        current_game_state = game_state.TITLE

def update():
    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()


run(update)
```

# Drawing the platforms

The background's checked off the list. Now we need to do the platforms, which we're going to make look like branches. Here's the image for the branch:

![Acorn Highway platform](/tut4_res/branch.png)

And we can add it in right below our background.

```python-raw
branch = image.load("assets/branch.png")
```

So, to draw these we clearly need to change up the `platform_base` class's `draw()` method. We could just blit the above image onto the shape and size of the platform, but that would make it look squashed or stretched depending on the length of the platform, as `screen.blit()` would resize it to fit. Instead, since it looks pretty much the same all the way along its length, we want to just crop it to the right length.

For this we can use the `brush` object, specifically `brush.image()`. This allows us to paint a shape with an image instead of a flat colour - in fact, behind the scenes flat colours work in just the same way as brushes. Once we have our brush we can set it as the pen and draw the exact same rectangle we were drawing before. We'll change `platform_base`'s `draw()` method as follows:

```python-raw
    def draw(self):
        screen.pen = brush.image(branch, mat3())
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)
```

As you can see we've only changed one line, and the platforms now show the branch texture. But something's very wrong. The image seems to flow along the platforms as they scroll, and sometimes it's misaligned with them. That's because `brush.image()` assumes the image starts at (0, 0) and repeats forever in x and y, and the shapes you draw using the brush are kind of like a window into that endless repeating pattern.

That means we need to change the brush to be aligned to our platform each time we draw it, which will solve both visual issues together. If you've done the dashboard tutorial you might have an idea of how we're going to do this - it's all to do with that `mat3()` we casually tossed into the brush's parameters hoping nobody would notice it. This is a transformation matrix, and we're going to use it to translate the position of the brush texture to the position of the platform whenever `draw()` is called.

At the moment it's just a plain bare `mat3()`, which means it's essentially a transformation that says "don't move it, don't rotate it, don't scale it". We don't want to do the last two, just move it, so we just need to add `.translate(x, y)` to it. And what are the x and y? The position of the platform itself, `self.x` and `self.y`. So then we know that the top left of the repeating texture will always line up with the top left of the platform, wherever that platform is vertically or however much it scrolls horizontally:

```python-raw
    def draw(self):
        screen.pen = brush.image(branch, mat3().translate(self.x, self.y))
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)
```

And that's the platforms working correctly - a lot less work than the background, since we did a lot more to set up for it earlier on. Now let's tackle Tufty in all their squirrely majesty.

# Tufty

The process for our player starts out similarly to the platforms and background, but with a twist - we're going to load in a couple of images, but this time we're going to load them in as spritesheets, something we haven't dealt with yet.

![Acorn Highway running spritesheet](/tut4_res/running.png)

![Acorn Highway death spritesheet](/tut4_res/death.png)

We'll load them in right after our other images, with the following code:

```python-raw
sqirl_run_sheet = SpriteSheet("assets/running.png", 7, 1)
sqirl_die_sheet = SpriteSheet("assets/death.png", 4, 1)
```

You'll see a difference in the images - they're each a full sprite sheet, showing every frame in an animation. That's why, when we load them in using `SpriteSheet()`, we supply them with how many sprites the sheet contains as the number of columns followed by the munber of rows. So you can see above that the running and death animations have seven and four columns respectively, in just a single row each.

We can access sprites within a `SpriteSheet` by using `SpriteSheet.sprite()` and supplying it with the coordinates of the sprite you want. This will then return an `image`. Let's apply this to the `draw()` method of `player_base` as follows:

```python-raw
    def draw(self):
        screen.blit(sqirl_run_sheet.sprite(0, 0), rect(self.x, self.y + 2, self.w, self.h))
```

And voila, one squirrel bouncing around the level. Now in fairness it's not the most animated squirrel yet, but we can change that. You might also notice in the code above that we're not drawing it exactly on the player's collision box, but actually two pixels lower so that Tufty's feet appear to sit nicely on the branch.

Instead of getting our image from the spritesheet directly, we're going to make it into an animated sprite. That means we select a range of sprites from the spritesheet, and we tell the software that they form a single animated image. Let's put the following lines in right below where you load the sprite sheets in:

```python-raw
sqirl_run = AnimatedSprite(sqirl_run_sheet, 0, 0, 7)
sqirl_die = AnimatedSprite(sqirl_die_sheet, 1, 0, 2)
```

To explain what we're doing with these, we'll just run through the parameters one by one. The first is obviously the name of the sprite sheet you want to pull an animation from. The next two integers refer to the column and row of the first frame. Then, the number of frames to count from there. There is another True/False parameter which decides whether the frames should go across or down from the starting frame, but since that defaults to True (horizontal) and that's what we want, we've not included it here.

From this, you can see that for the running sprite, it's starting from the top left sprite in the sprite sheet, and counting seven frames horizontally including the starting frame, which in this case is every sprite in the sheet. It returns an `AnimatedSprite` object which we'll be using to draw Tufty.

You might also notice that the death sprite is being done a little differently. Instead of the first one, we're starting counting frames from the second sprite along, and we're only using two frames. So although the death sprite sheet has four frames, we're only going to be using the middle two for the animation.

To get a frame from an `AnimatedSprite` object, we just use its `frame()` method, which we just pass the frame number we want. If the frame number is outside the number of frames in the `AnimatedSprite`, it just wraps around, which is a really useful feature because it means that if we've got a 'frame number' variable somewhere, we can just increase it to loop the animation without worrying about resetting it.

Here's the new `draw()` method in `player_base`:

```python-raw
    def draw(self):
        screen.blit(sqirl_run.frame(0), rect(self.x, self.y + 2, self.w, self.h))
```

That shouldn't play any different, but we've set the scene for our animation. You can test it by replacing that zero with other numbers and you'll see different frames appear.

Now, we're going to set up a variable to keep track of the frame we're showing, and increase it by 1 every time we run the main `update()` loop.

Let's put the global variable `frame_counter = 0` just before creating the player instance and after setting the scrolling speeds. Then in `update()`, we'll just bring in `frame_counter` as a global variable and increment it by one at the end of the method:

```python-raw
def update():
    global frame_counter

    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()

    frame_counter += 1
```

Of course this won't do anything unless we apply it, so there's another change to `draw()` in `player_base`, to replace the hard coded frame number with `frame_counter`:

```python-raw
    def draw(self):
        screen.blit(sqirl_run.frame(frame_counter), rect(self.x, self.y + 2, self.w, self.h))
```

Run the program now, and Tufty is animated! But hoo boy, that's one squirrely squirrel - that frame rate is clearly way too fast. We can fix it though - how about, instead of updating the frame every `update()`, we actually time it?

We're going to set up another global variable called `last_frame` and set it to the badge's `ticks` value - that is, the number of milliseconds that have passed from the badge starting up to the beginning of the current `update()` loop. Then in `update()`, we can check the current `badge.ticks` and see if a specified amount of time has passed since `last_frame`. If it has, we'll update the frame counter and set `last_frame` to be the current `badge.ticks`, ready for the next frame.

```python-raw
frame_counter = 0
player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0
last_frame = badge.ticks
```

The last line there sets up the last frame time - now we just need to check it in `update()`.

```python-raw
def update():
    global frame_counter, last_frame

    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()

    if badge.ticks - last_frame > 83:
        frame_counter += 1
        last_frame = badge.ticks
```

Note that because we need to write to `last_frame`, we've brought it in as a global. We've chosen a time of 83ms for each frame, because that's approximately one twelfth of a second, so the animation will run around 12fps - a good speed for this animation.

If everything's gone right so far, your code should look like this, and Tufty should be animating like a champ!

```python
import qwstpad
import random


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAMEOVER = 3


class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False

    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False

    def is_airborne(self):
        airborne = True
        for platform in platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or controls["DROP"]:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

            if controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0: self.vx -= 0.5
            elif self.vx < 0: self.vx += 0.5

        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True

    def draw(self):
        screen.blit(sqirl_run.frame(frame_counter), rect(self.x, self.y + 2, self.w, self.h))


class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))

    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1

        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        global platforms
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False

    def draw(self):
        screen.pen = brush.image(branch, mat3().translate(self.x, self.y))
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class acorn_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


def draw_background(scroll=True):
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    if scroll:
        background_scroll_amount -= background_scroll_speed
        background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))


def draw_score():
    global score
    screen.text(str(score), 0, 0)


def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None


def parse_controls():
    global controls, gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()

    if gamepad:
        controls["MOVE_LEFT"] = gamepad.held("L")
        controls["MOVE_RIGHT"] = gamepad.held("R")
        controls["DROP"] = gamepad.held("D") and gamepad.pressed("A")
        controls["JUMP"] = gamepad.pressed("A")
        controls["JUMP_LEFT"] = gamepad.held("L") and gamepad.pressed("A")
        controls["JUMP_RIGHT"] = gamepad.held("R") and gamepad.pressed("A")
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["JUMP_LEFT"] = badge.held(BUTTON_A) and badge.pressed(BUTTON_C)
        controls["JUMP_RIGHT"] = badge.held(BUTTON_B) and badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]

background = image.load("assets/background.png")
branch = image.load("assets/branch.png")
sqirl_run_sheet = SpriteSheet("assets/running.png", 7, 1)
sqirl_die_sheet = SpriteSheet("assets/death.png", 4, 1)
sqirl_run = AnimatedSprite(sqirl_run_sheet, 0, 0, 7)
sqirl_die = AnimatedSprite(sqirl_die_sheet, 1, 0, 2)

gamepad = None
controls = {}

foreground_scroll_speed = 4
background_scroll_speed = 1
background_scroll_amount = 0

frame_counter = 0
player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0
last_frame = badge.ticks

init_gamepad()
init_platforms()

def title_loop():
    global current_game_state

    screen.text("Title screen", 0, 0)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY

def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM

def death_anim_loop():
    global current_game_state

    draw_background(False)

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER

def game_over_loop():
    global current_game_state, score

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        current_game_state = game_state.TITLE

def update():
    global frame_counter, last_frame

    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()

    if badge.ticks - last_frame > 83:
        frame_counter += 1
        last_frame = badge.ticks


run(update)
```

# Other animation states

Tufty is running great, but let's improve on those animations. Right now, when you jump you're running through the air, frantically pedalling your little squirrel limbs. We can take a page from the book of classic platformers of the past and just freeze on a single frame when you jump. It looks like the third frame along on the sprite sheet (numbered 2) would be good, so let's just put in a little check in the player's `draw()` method that checks if you're in gameplay and airborne, and if so just displays frame 2, otherwise displaying whichever frame the frame counter tells us to.

```python-raw
    def draw(self):
        if self.airborne and current_game_state == game_state.GAMEPLAY:
            frame = 2
        else:
            frame = frame_counter
        screen.blit(sqirl_run.frame(frame), rect(self.x, self.y + 2, self.w, self.h))
```

And now Tufty strikes a Dynamic Action Pose whener you jump! But it's still not quite right when we die, and as you may have suspected when we imported sprites for it, we've got another animation for that.

The setup we need to do for this involves making the player's current animation a variable in the class - that way, by changing that variable between different sprites we can change Tufty's animation. So we'll just add `self.animation = sqirl_run` in at the end of the player's `__init__()` method, after we set `self.dead`. Then we can alter `draw()` to use that variable:

```python-raw
    def draw(self):
        if self.airborne and current_game_state == game_state.GAMEPLAY:
            frame = 2
        else:
            frame = frame_counter
        screen.blit(self.animation.frame(frame), rect(self.x, self.y + 2, self.w, self.h))
```

Now we just need add a line to the end of the player's `reset()` and `death()` methods to switch Tufty's current animation to the right one at the right time.

```python-raw
    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False
        self.animation = sqirl_run

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True
        self.animation = sqirl_die
```

And we're done with the animations! If you've been following along, your code should look like this:

```python
import qwstpad
import random


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAMEOVER = 3


class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False

        self.animation = sqirl_run

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False

    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False

    def is_airborne(self):
        airborne = True
        for platform in platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or controls["DROP"]:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

            if controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0: self.vx -= 0.5
            elif self.vx < 0: self.vx += 0.5

        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False
        self.animation = sqirl_run

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True
        self.animation = sqirl_die

    def draw(self):
        if self.airborne and current_game_state == game_state.GAMEPLAY:
            frame = 2
        else:
            frame = frame_counter
        screen.blit(self.animation.frame(frame), rect(self.x, self.y + 2, self.w, self.h))


class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))

    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1

        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        global platforms
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False

    def draw(self):
        screen.pen = brush.image(branch, mat3().translate(self.x, self.y))
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class acorn_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


def draw_background(scroll=True):
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    if scroll:
        background_scroll_amount -= background_scroll_speed
        background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))


def draw_score():
    global score
    screen.text(str(score), 0, 0)


def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None


def parse_controls():
    global controls, gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()

    if gamepad:
        controls["MOVE_LEFT"] = gamepad.held("L")
        controls["MOVE_RIGHT"] = gamepad.held("R")
        controls["DROP"] = gamepad.held("D") and gamepad.pressed("A")
        controls["JUMP"] = gamepad.pressed("A")
        controls["JUMP_LEFT"] = gamepad.held("L") and gamepad.pressed("A")
        controls["JUMP_RIGHT"] = gamepad.held("R") and gamepad.pressed("A")
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["JUMP_LEFT"] = badge.held(BUTTON_A) and badge.pressed(BUTTON_C)
        controls["JUMP_RIGHT"] = badge.held(BUTTON_B) and badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]

background = image.load("assets/background.png")
branch = image.load("assets/branch.png")
sqirl_run_sheet = SpriteSheet("assets/running.png", 7, 1)
sqirl_die_sheet = SpriteSheet("assets/death.png", 4, 1)
sqirl_run = AnimatedSprite(sqirl_run_sheet, 0, 0, 7)
sqirl_die = AnimatedSprite(sqirl_die_sheet, 1, 0, 2)

gamepad = None
controls = {}

foreground_scroll_speed = 4
background_scroll_speed = 1
background_scroll_amount = 0

frame_counter = 0
player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0
last_frame = badge.ticks

init_gamepad()
init_platforms()

def title_loop():
    global current_game_state

    screen.text("Title screen", 0, 0)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY

def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM

def death_anim_loop():
    global current_game_state

    draw_background(False)

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER

def game_over_loop():
    global current_game_state, score

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        current_game_state = game_state.TITLE

def update():
    global frame_counter, last_frame

    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()

    if badge.ticks - last_frame > 83:
        frame_counter += 1
        last_frame = badge.ticks


run(update)
```

# Something to collect

Way back in the mists of time in the first part of this tutorial, you were promised collectables - acorns that Tufty could pick up to score extra points. They're the final gameplay element, and now we're finally going to implement them.

Back then we already made an `acorn_base` class, as well as a global list to hold all our acorns. So really we just need a way of drawing them, a way of spawning them and a way of collecting them. Just like the player and platforms, all of the stuff to do with the acorns being picked up and suchlike will be handled by the acorns themselves. Here's our image:

![Acorn Highway acorn small](/tut4_res/acorn_sml.png)

First of all let's draw them as that's nice and easy. After we import the other images, let's import the acorn with `acorn_sml = image.load("assets/acorn_sml.png")`.

Then we can just alter the `acorn_base`'s `draw()` method to draw that image.

```python-raw
    def draw(self):
        screen.blit(acorn_sml, vec2(self.x, self.y))
```

That's done. Now, we want to spawn the acorns on top of the platforms. Which means we need to know where each platform is, and what part of the program knows that? The platforms themselves! So the basic idea is that each time a platform resets, it has a two in three chance of spawning an acorn on top of it.

To do that, we'll need to create a method in `platform_base`, right before its `draw()` method. It looks like this:

```python-raw
    def spawn_acorn(self):
        global acorns
        acorn = acorn_base(random.randint(self.x, self.r - 10), self.y - 10)
        acorns.append(acorn)
```

This is very simple. First we bring in the `acorns` list as a global, the second line creates a new acorn and the third line adds it to the list.

If you recall when we created the `acorn_base` class, it takes in x and y coordinates for the position of the acorn. We're providing that - the x coordinate is a random number between the left side of the platform, and the right side minus the width of the acorn. So in other words, somewhere along the length of the platform. The y coordinate is just ten pixels above the top of the platform - again, the height of the acorn.

Now, we can just call that method right after we reset the platform to a new position on the right side of the screen - by picking a random number between 0 and 2, and spawning an acorn if the number is greater than 0, we get our two in three chance. We could use `if random.randint(0, 2) > 0:`, but the `> 0` is unnecessary, as Python considers zeroes to be False and any number other then zero to be True, so we can just check for that.

```python-raw
    def update(self):
        global score

        self.x -= foreground_scroll_speed
        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1
            if random.randint(0, 2):
                self.spawn_acorn()
        self.draw()
```

That spawns the acorns, but you won't see them as we're not drawing them yet - and even if we were, they would be off the right hand side of the screen when they appeared, and they aren't moving anywhere yet. Let's fix these things.

In `acorn_base`, let's create a `move()` method and an `update()` method right before `draw()`.

```python-raw
    def move(self):
        self.x -= foreground_scroll_speed
        self.draw()

    def update(self):
        global acorns

        if self.r < 0:
            acorns.remove(self)
```

Hopefully both of these are pretty self explanatory. `move()` shifts the acorn's position to the left by `foreground_scroll_speed` number of pixels and then draws it, and `update()` deletes the acorn if it's completely off the left side of the screen - in other words, if it's not been picked up.

You'll notice that while `move()` calls `draw()`, `update()` is kept in a separate method. That's because to do the move/draw and the update, we have to loop through the `acorns` list, and there's a chance that the acorn's `update()` method might cause it to be removed from that list. MicroPython allows that to happen, but because of the way it iterates through the list it will skip an item, meaning one acorn won't be moved, drawn or updated. In the game this means that the acorns would appear to flicker or not move for a single frame every time one disappeared off the left side of the screen.

Instead, what we'll do is loop through all of the acorns, moving them (which also draws them), and then we'll loop through them again updating them, which removes any from the list that need removing in time for the next frame. We'll do this in our `gameplay_loop()`, in between updating the player and drawing the score, so that the method now looks like this:

```python-raw
def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for acorn in acorns:
        acorn.move()

    for acorn in acorns:
        acorn.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM
```

Before we get on to the next bit, picking up the acorns, we just want to quickly add in `acorns.clear()` into `game_over_loop()`, right after we reset the score - that way the list of acorns get cleared when everything else resets for a new game.

Once that's done, let's get Tufty grabbing those acorns. Like we mentioned above, that's going to be taken care of in the `acorn_base` class. And as a bonus, we've already done all the legwork for it! In `acorn_base`'s `update()` method, we just need to check if the acorn's bounding box overlaps the player's, and if it does, add three to the score and delete the acorn from the list! Easy!

```python-raw
    def update(self):
        global acorns, score

        if self.bounding_box.intersects(player.bounding_box):
            acorns.remove(self)
            score += 3

        elif self.r < 0:
            acorns.remove(self)
```

The more we get through this, the more we find that the mechanisms we need are already there. If you try playing now you can pick up the acorns and add to the score! There's just one last thing to do. You might notice that it's a bit easy to pick up the acorns - you don't really have to touch them to pick them up, and it's pretty easy to see why. Remember the red square we had for our player before adding the Tufty sprite? It's a lot bigger than the sprite itself, 32x32px, and as soon as any part of it hits an acorn that acorn's picked up.

Fixing this isn't too complicated. The player's `bounding_box` property is used in just one place in the program - checking for collision with the acorns. That means that we can fine tune the size and location of that bounding box to better fit Tufty's actual dimensions. The property as it stands is calculated with

```python-raw
    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)
```

We could fine tune it to fit Tufty's exact bounding box for every frame of the animation, but that's really more effort than is needed for this application, so we'll just try a one-size-fits-all size. After a little tweaking, we've found this works well:

```python-raw
    @property
    def bounding_box(self):
        return rect(self.x + 8, self.y + 20, self.w - 16, self.h - 20)
```

This takes the top of the sprite down by 20px and the sides in by 8px, like so:

![Acorn Highway sprite bounding box](/tut4_res/sprite_clip_demo.png)

(You don't need to download this image, it's just to show the new bounding box.)

And now gameplay is almost entirely complete. Let's move on to prettying up the rest of the game - here's the code you should have so far:

```python
import qwstpad
import random


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAMEOVER = 3


class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False

        self.animation = sqirl_run

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h

    @property
    def bounding_box(self):
        return rect(self.x + 8, self.y + 20, self.w - 16, self.h - 20)

    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False

    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False

    def is_airborne(self):
        airborne = True
        for platform in platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or controls["DROP"]:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

            if controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0: self.vx -= 0.5
            elif self.vx < 0: self.vx += 0.5

        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False
        self.animation = sqirl_run

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True
        self.animation = sqirl_die

    def draw(self):
        if self.airborne and current_game_state == game_state.GAMEPLAY:
            frame = 2
        else:
            frame = frame_counter
        screen.blit(self.animation.frame(frame), rect(self.x, self.y + 2, self.w, self.h))


class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))

    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1
            if random.randint(0, 2):
                self.spawn_acorn()
        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        global platforms
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False

    def spawn_acorn(self):
        global acorns
        acorn = acorn_base(random.randint(self.x, self.r - 10), self.y - 10)
        acorns.append(acorn)

    def draw(self):
        screen.pen = brush.image(branch, mat3().translate(self.x, self.y))
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class acorn_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def move(self):
        self.x -= foreground_scroll_speed
        self.draw()

    def update(self):
        global acorns, score

        if self.bounding_box.intersects(player.bounding_box):
            acorns.remove(self)
            score += 3

        elif self.r < 0:
            acorns.remove(self)

    def draw(self):
        screen.blit(acorn_sml, vec2(self.x, self.y))


def draw_background(scroll=True):
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    if scroll:
        background_scroll_amount -= background_scroll_speed
        background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))


def draw_score():
    global score
    screen.text(str(score), 0, 0)


def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None


def parse_controls():
    global controls, gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()

    if gamepad:
        controls["MOVE_LEFT"] = gamepad.held("L")
        controls["MOVE_RIGHT"] = gamepad.held("R")
        controls["DROP"] = gamepad.held("D") and gamepad.pressed("A")
        controls["JUMP"] = gamepad.pressed("A")
        controls["JUMP_LEFT"] = gamepad.held("L") and gamepad.pressed("A")
        controls["JUMP_RIGHT"] = gamepad.held("R") and gamepad.pressed("A")
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["JUMP_LEFT"] = badge.held(BUTTON_A) and badge.pressed(BUTTON_C)
        controls["JUMP_RIGHT"] = badge.held(BUTTON_B) and badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]

background = image.load("assets/background.png")
branch = image.load("assets/branch.png")
sqirl_run_sheet = SpriteSheet("assets/running.png", 7, 1)
sqirl_die_sheet = SpriteSheet("assets/death.png", 4, 1)
sqirl_run = AnimatedSprite(sqirl_run_sheet, 0, 0, 7)
sqirl_die = AnimatedSprite(sqirl_die_sheet, 1, 0, 2)
acorn_sml = image.load("assets/acorn_sml.png")

gamepad = None
controls = {}

foreground_scroll_speed = 4
background_scroll_speed = 1
background_scroll_amount = 0

frame_counter = 0
player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0
last_frame = badge.ticks

init_gamepad()
init_platforms()

def title_loop():
    global current_game_state

    screen.text("Title screen", 0, 0)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY

def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for acorn in acorns:
        acorn.move()

    for acorn in acorns:
        acorn.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM

def death_anim_loop():
    global current_game_state

    draw_background(False)

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER

def game_over_loop():
    global current_game_state, score, acorns

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        acorns.clear()
        current_game_state = game_state.TITLE

def update():
    global frame_counter, last_frame

    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()

    if badge.ticks - last_frame > 83:
        frame_counter += 1
        last_frame = badge.ticks


run(update)
```

# The title and game over screens

We could just display static images for these, but we could pretty them up some, make them look a little flashier. What if the title screen was animated and showed Tufty running along an endless branch? That would look cool and we can do it using all the existing assets we've already got.

We'll need a couple more images:

![Acorn Highway title logo](/tut4_res/title.png)

![Acorn Highway game over screen](/tut4_res/gameover.png)

Let's import these in right after the others.

```python-raw
title = image.load("assets/title.png")
gameover = image.load("assets/gameover.png")
```

The game over loop then becomes very easy to do, as we're just replacing the line that draws the text with one that blits the image:

```python-raw
def game_over_loop():
    global current_game_state, score, acorns

    screen.blit(gameover, vec2(0, 0))

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        acorns.clear()
        current_game_state = game_state.TITLE
```

For the title screen, the first thing we can do is lay down the background using `draw_background()` just like in the gameplay loop, and then we can blit the title on top of it. The title image is the width of the screen, so we can just position it at (0, 0) and it'll be in the right place.

```python-raw
def title_loop():
    global current_game_state

    draw_background()

    screen.blit(title, vec2(0, 0))

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY
```

Alright, that's a good backdrop. Now, remember how we used an image brush to draw the platforms? We're going to do the same here for our infinite branch, but instead of moving the platform we're going to keep it in one place and let the texture scroll across it. Here's what we're going to do.

```python-raw
def title_loop():
    global current_game_state

    draw_background()

    screen.blit(title, vec2(0, 0))

    branch_y = 73
    branch_tex_matrix = mat3().translate(0, branch_y)

    branch_bar = shape.rectangle(0, branch_y, screen.width, 10)
    screen.pen = brush.image(branch, branch_tex_matrix)
    screen.shape(branch_bar)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY
```

Let's go through those new lines one by one. First we're going to set a variable for the branch's y position on the screen. Then we'll create a transformation matrix, just like we did for the platforms which moves the tiling branch texture down to that same height. We'll be using the x coordinate of this matrix to scroll the branch, but for now we'll leave it at zero.

Then we create a rectangle of the right size in the right position - in this case full screen width, 10px high, and our previously decided y position. Finally we just set the pen to be a new image brush using our already-loaded branch texture as the image, the matrix we just created as the transformation, and we draw it to the screen.

If you run the program now you should see a static branch along the horizon line. To animate it, we just need to reduce that x coordinate of the texture by a certain amount every frame, and we're good. The texture does wrap around many times, but not forever - if we didn't reset it at some point we'd eventually see the scrolling texture start to break and the branch would just display the first column of pixels in the image over and over again. So we'll also use the modulo operator (`%`) to reset it.

> Note: In theory you could use this technique to do the background scrolling as well, but in practice we found that because of some internal workings of the back end code, the way it's been accomplished in this tutorial gave a much smoother and more consistent framerate.

Let's have the infinite branch move at the same speed as the ingame platforms. That gives us visual consistency, and also lets us reuse our `foreground_scroll_speed` variable. We just need another global to keep track of the scroll position of the texture, and we'll create that right below the other scrolling-related globals as `title_scroll_amount = 0`. Then in our title screen loop, we'll bring in the global, set the x coordinate of the texture transformation to `title_scroll_amount` and remember to decrease `title_scroll_amount` by `foreground_scroll_speed`.

```python-raw
def title_loop():
    global current_game_state, title_scroll_amount

    draw_background()

    screen.blit(title, vec2(0, 0))

    branch_y = 73
    branch_tex_matrix = mat3().translate(title_scroll_amount, branch_y)
    title_scroll_amount -= foreground_scroll_speed
    title_scroll_amount %= branch.width

    branch_bar = shape.rectangle(0, branch_y, screen.width, 10)
    screen.pen = brush.image(branch, branch_tex_matrix)
    screen.shape(branch_bar)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY
```

Now we just need to add Tufty running along there. This is a lot easier than the interactive Tufty, as this one doesn't need to move or take in input from buttons, it's just an animated image.

```python-raw
    sqirl_x = (screen.width - 32) / 2
    sqirl_y = 43
    screen.blit(sqirl_run.frame(frame_counter), rect(sqirl_x, sqirl_y, 32, 32))
```

So we're just using the existing frame counter we've always got running in the background for this. First we're setting x and y coordinates so that Tufty will be at the right height and centred on screen, then blitting the appropriate frame from the animation.

# Captions

For another touch, let's add a flashing "Press any button!" message to the title and game over screens. There are some pixel fonts just the right fit for this purpose - we'll add the following line right at the end of our image imports:

```python-raw
title_font = rom_font.yesterday
```

We're actually going to be centering text on the screen a fair bit for the rest of this tutorial, so let's make a quick method for doing this more easily. Here it is in full, and it can go at the very beginning of our methods, right after the definition for the `acorn_base` class:

```python-raw
def centre_text(message, y):
    text_w, text_h = screen.measure_text(message)

    x = (screen.width - text_w) / 2

    screen.text(message, vec2(x, y))
```

This is probably pretty familiar if you've done the previous tutorials. You can see here that we're specifying the text and the y coordinate as parameters, then we're simply measuring the text, using that to work out an x position on the screen and finally drawing the text at the calculated position.

Now we've got that, we can easily use it ingame. You just need the following lines in `title_loop()` and `game_over_loop()`, each right after drawing everything else and before checking for button presses.

```python-raw
    screen.font = title_font
    screen.pen = color.white

    if int(badge.ticks / 500) % 2:
        restarttext = "Press any button!"
        centre_text(restarttext, 100)
```

Setting the font and the pen is self-explanatory, as is drawing the text. That `if` statement bears some explaining though - it's looking at the badge's `ticks` property again, dividing it by 500, rounding it to a whole number and seeing if that whole number is even. The way the maths works out, the result of that calculation would switch between odd and even every half a second, so we can use it in an if statement to make the text flash on and off. Dividing by 500 gives us that half second rate - as `ticks` is in milliseconds, 500 ticks is half a second - but you can experiment and see how different values in there will alter the rate of flashing.

At this point, your program should look like this:

```python
import qwstpad
import random


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAMEOVER = 3


class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False

        self.animation = sqirl_run

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h

    @property
    def bounding_box(self):
        return rect(self.x + 8, self.y + 20, self.w - 16, self.h - 20)

    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False

    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False

    def is_airborne(self):
        airborne = True
        for platform in platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or controls["DROP"]:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

            if controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0: self.vx -= 0.5
            elif self.vx < 0: self.vx += 0.5

        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False
        self.animation = sqirl_run

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True
        self.animation = sqirl_die

    def draw(self):
        if self.airborne and current_game_state == game_state.GAMEPLAY:
            frame = 2
        else:
            frame = frame_counter
        screen.blit(self.animation.frame(frame), rect(self.x, self.y + 2, self.w, self.h))


class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))

    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1
            if random.randint(0, 2):
                self.spawn_acorn()
        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        global platforms
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False

    def spawn_acorn(self):
        global acorns
        acorn = acorn_base(random.randint(self.x, self.r - 10), self.y - 10)
        acorns.append(acorn)

    def draw(self):
        screen.pen = brush.image(branch, mat3().translate(self.x, self.y))
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class acorn_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def move(self):
        self.x -= foreground_scroll_speed
        self.draw()

    def update(self):
        global acorns, score

        if self.bounding_box.intersects(player.bounding_box):
            acorns.remove(self)
            score += 3

        elif self.r < 0:
            acorns.remove(self)

    def draw(self):
        screen.blit(acorn_sml, vec2(self.x, self.y))


def centre_text(message, y):
    text_w, text_h = screen.measure_text(message)

    x = (screen.width - text_w) / 2

    screen.text(message, vec2(x, y))


def draw_background(scroll=True):
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    if scroll:
        background_scroll_amount -= background_scroll_speed
        background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))


def draw_score():
    global score
    screen.text(str(score), 0, 0)


def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None


def parse_controls():
    global controls, gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()

    if gamepad:
        controls["MOVE_LEFT"] = gamepad.held("L")
        controls["MOVE_RIGHT"] = gamepad.held("R")
        controls["DROP"] = gamepad.held("D") and gamepad.pressed("A")
        controls["JUMP"] = gamepad.pressed("A")
        controls["JUMP_LEFT"] = gamepad.held("L") and gamepad.pressed("A")
        controls["JUMP_RIGHT"] = gamepad.held("R") and gamepad.pressed("A")
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["JUMP_LEFT"] = badge.held(BUTTON_A) and badge.pressed(BUTTON_C)
        controls["JUMP_RIGHT"] = badge.held(BUTTON_B) and badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]

background = image.load("assets/background.png")
branch = image.load("assets/branch.png")
sqirl_run_sheet = SpriteSheet("assets/running.png", 7, 1)
sqirl_die_sheet = SpriteSheet("assets/death.png", 4, 1)
sqirl_run = AnimatedSprite(sqirl_run_sheet, 0, 0, 7)
sqirl_die = AnimatedSprite(sqirl_die_sheet, 1, 0, 2)
acorn_sml = image.load("assets/acorn_sml.png")
title = image.load("assets/title.png")
gameover = image.load("assets/gameover.png")
title_font = rom_font.yesterday

gamepad = None
controls = {}

foreground_scroll_speed = 4
background_scroll_speed = 1
background_scroll_amount = 0
title_scroll_amount = 0

frame_counter = 0
player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0
last_frame = badge.ticks

init_gamepad()
init_platforms()

def title_loop():
    global current_game_state, title_scroll_amount

    draw_background()

    screen.blit(title, vec2(0, 0))

    branch_y = 73
    branch_tex_matrix = mat3().translate(title_scroll_amount, branch_y)
    title_scroll_amount -= foreground_scroll_speed

    branch_bar = shape.rectangle(0, branch_y, screen.width, 10)
    screen.pen = brush.image(branch, branch_tex_matrix)
    screen.shape(branch_bar)

    sqirl_x = (screen.width - 32) / 2
    sqirl_y = 43
    screen.blit(sqirl_run.frame(frame_counter), rect(sqirl_x, sqirl_y, 32, 32))

    screen.font = title_font
    screen.pen = color.white

    if int(badge.ticks / 500) % 2:
        restarttext = "Press any button!"
        centre_text(restarttext, 100)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY

def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for acorn in acorns:
        acorn.move()

    for acorn in acorns:
        acorn.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM

def death_anim_loop():
    global current_game_state

    draw_background(False)

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER

def game_over_loop():
    global current_game_state, score, acorns

    screen.blit(gameover, vec2(0, 0))

    screen.font = title_font
    screen.pen = color.white

    if int(badge.ticks / 500) % 2:
        restarttext = "Press any button!"
        centre_text(restarttext, 100)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        acorns.clear()
        current_game_state = game_state.TITLE

def update():
    global frame_counter, last_frame

    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()

    if badge.ticks - last_frame > 83:
        frame_counter += 1
        last_frame = badge.ticks


run(update)
```

# Visual finishing touches

One thing we've neglected so far is that poor little score indicator in the gameplay screen. It's been sitting there, sometimes flickering with the branch brush, other times whatever colour was last used - let's give it a little love. We're going to put in a slightly larger acorn icon and some fancy looking text for it. This isn't tricky, we've just got to do the necessary importing of images and fonts and such. Here's the image.

![Acorn Highway acorn large](/tut4_res/acorn_lg.png)

And we'll import it in just the same way as we have the others, adding in right after them

```python-raw
acorn_lg = image.load("assets/acorn_lg.png")
score_font = rom_font.futile
```

You can see we also loaded another pixel font from memory. That's all the assets we need to add for the game! Now let's just implement them. Let's scroll back up to the `draw_score()` method that we created all that time ago.

We're going to put the icon in the top right of the screen, with the score next to it, aligned to the right. The score will just be plain text, but we're going to do two copies of it, offset just slightly to give a drop shadow effect. This is the only place we're going to use this, so there's no point in making a matrix transformation or anything like we did in the dashboard tutorial. Here we can just position it by hand.

First, let's do the image:

```python-raw
def draw_score():
    global score

    x = screen.width - 16
    y = 3

    acorn_coords = vec2(x, y)
    screen.blit(acorn_lg, acorn_coords)
```

After that we'll measure the text - remember, it's an integer, so will need converting to a string before we draw or measure it:

```python-raw
    score_w, score_h = screen.measure_text(str(score))
```

To draw the text and the drop shadow we need to do the shadow first, so that the text displays over the top of it. We'll modify and reuse the x and y coordinates we already made for the acorn icon to get first the position of the drop shadow and then of the score text.

```python-raw
    screen.font = score_font
    screen.pen = color.black

    x -= score_w
    y -= 5
    screen.text(str(score), vec2(x, y))
```

As you can see, we've just shifted our x coordinate left by the width of the score text, and our y coordinate up a little. We've also set the font and the colour for our drop shadow, and then drawn it to the screen.

```python-raw
    x -=2
    y -=2
    screen.pen = color.brown
    screen.text(str(score), vec2(x, y))
```

Finally we'll just move the position up and to the left by two pixels, change the pen colour and draw the same text again. Your method should now look like the following, and should display a neat looking bold score up in the top right of the screen.

```python-raw
def draw_score():
    global score

    x = screen.width - 16
    y = 3

    acorn_coords = vec2(x, y)
    screen.blit(acorn_lg, acorn_coords)

    score_w, score_h = screen.measure_text(str(score))

    screen.font = score_font
    screen.pen = color.black

    x -= score_w
    y -= 5
    screen.text(str(score), vec2(x, y))

    x -=2
    y -=2
    screen.pen = color.brown
    screen.text(str(score), vec2(x, y))
```

Not bad, right?

# Final score tricks

Now we just want to put on two finishing touches - displaying your final score when you get a game over, and keeping track of the high score so you can compete against yourself or others.

Displaying the score is trivial - you just need the following lines in `game_over_loop()`, right after you display the flashing 'Press any button!' message:

```python-raw
    scoretext = f"Your score: {str(score)}"
    centre_text(scoretext, 87)
```

> Note: If you've not seen this type of string formatting before, it's simple - if you put an f before opening the string, you can include variables in the string by enclosing them in curly braces. It just saves on faffing about concatenating strings together.

That's all you need. High scores are trickier though, and they require the use of the last part of the API to be covered in this tutorial, states.

In essence, a state is just a little JSON file that contains simple data - in this case, one single number - that of the current high score. There's methods in the Badgeware API that let you easily and quickly load and save states, and this is ideal for what we want to do.

States are saved in the form of a dictionary, and we need to set up that dictionary with default values, so that if there is no save state file (like when the program is first run), there's still data to work with. We're working just after we've set our player, acorns, game state and so on, right before we run `init_gamepad()` and/or `init_platforms()`.

```python-raw
save_state = {"highscore": 0}
```

This single line sets up a little dictionary with a single entry - the key is the string "highscore", and the value starts at 0. It's this dictionary we read the high score from and write it to, so before we've even done any saving or loading we can add in the code for displaying it.

Let's go to our `title_loop()` method and add in the following, right after the flashing text:

```python-raw
    highscoretext = f"High score: {str(save_state["highscore"])}"
    centre_text(highscoretext, 85)
```

I'm sure you're getting the hang of this by now - we're drawing another centred line of text, a bit higher, and we're including in the string `save_state[highscore]` - that is, the value from the dictionary we just created. Note that again, the value is an integer, so we need to convert it into a string.

We can put the same high score into our `game_over_loop()` method, although this time, we've got a little more to do.

We could just say `highscoretext = f"High score: {str(save_state["highscore"])}"` just like in the title screen. But if you get a new high score, we need to update the dictionary to reflect that - and while we could just show "Your score - 99, High score - 99" it might be cool to use that space to actually congratulate the player. Let's go with the following:

```python-raw
    if score >= save_state["highscore"]:
        highscoretext = "High score!"
        save_state["highscore"] = score
    else:
        highscoretext = f"High score: {str(save_state["highscore"])}"

    centre_text(highscoretext, 74)
```

So, probably pretty easy to see what's going on here - if the current score is greater than or equal to the high score, make that the high score and display one message, otherwise display the same message we did on the title screen. This code should go in the same place as on the title screen, after the last text you wrote and before the button check.

> Note: It's `>=` rather than just `>` because otherwise, the game would consider it a new high score for the first frame of displaying it, and then after that it would have updated the dictionary, so it wouldn't flag up as a high score any more and would just display the normal message.

Nice! Your high scores are being recorded. Only problem is, the game is forgetting the high score every time it restarts. That's there the states come in, and it's just two more lines of code before you're done with the whole thing!

First off, right after creating that dictionary, we'll just load in any saved states into it:

```python-raw
save_state = {"highscore": 0}
State.load("acorn_highway", save_state)
```

Let's unpack that `State.load()`. The first parameter is the name of the save state - it could be any string, just as long as you've got the same name in there when you load as when you save. The second parameter is the dictionary to load into, in this case the one created in the line above. If it doesn't find any saved states, this method will just leave the dictionary as it is, so you don't need to worry about missing files.

Similarly, where we just were on the game over screen, right after putting the new high score in the dictionary we're going to add a line:

```python-raw
    if score >= save_state["highscore"]:
        highscoretext = "High score!"
        save_state["highscore"] = score
        State.save("acorn_highway", save_state)
```

# The end

And that's it! By'eck, it's been a litle while, but we got there. You should have a fully fledged platform game for Tufty. Here's the final code for the game. Well done for getting this far and happy coding in the future!

```python
import qwstpad
import random


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAMEOVER = 3


class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False

        self.animation = sqirl_run

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h

    @property
    def bounding_box(self):
        return rect(self.x + 8, self.y + 20, self.w - 16, self.h - 20)

    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False

    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False

    def is_airborne(self):
        airborne = True
        for platform in platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or controls["DROP"]:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

            if controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0: self.vx -= 0.5
            elif self.vx < 0: self.vx += 0.5

        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False
        self.animation = sqirl_run

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True
        self.animation = sqirl_die

    def draw(self):
        if self.airborne and current_game_state == game_state.GAMEPLAY:
            frame = 2
        else:
            frame = frame_counter
        screen.blit(self.animation.frame(frame), rect(self.x, self.y + 2, self.w, self.h))


class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))

    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1
            if random.randint(0, 2):
                self.spawn_acorn()
        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        global platforms
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False

    def spawn_acorn(self):
        global acorns
        acorn = acorn_base(random.randint(self.x, self.r - 10), self.y - 10)
        acorns.append(acorn)

    def draw(self):
        screen.pen = brush.image(branch, mat3().translate(self.x, self.y))
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class acorn_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def move(self):
        self.x -= foreground_scroll_speed
        self.draw()

    def update(self):
        global acorns, score

        if self.bounding_box.intersects(player.bounding_box):
            acorns.remove(self)
            score += 3

        elif self.r < 0:
            acorns.remove(self)

    def draw(self):
        screen.blit(acorn_sml, vec2(self.x, self.y))


def centre_text(message, y):
    text_w, text_h = screen.measure_text(message)

    x = (screen.width - text_w) / 2

    screen.text(message, vec2(x, y))


def draw_background(scroll=True):
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    if scroll:
        background_scroll_amount -= background_scroll_speed
        background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))


def draw_score():
    global score

    x = screen.width - 16
    y = 3

    acorn_coords = vec2(x, y)
    screen.blit(acorn_lg, acorn_coords)

    score_w, score_h = screen.measure_text(str(score))

    screen.font = score_font
    screen.pen = color.black

    x -= score_w
    y -= 5
    screen.text(str(score), vec2(x, y))

    x -=2
    y -=2
    screen.pen = color.brown
    screen.text(str(score), vec2(x, y))


def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None


def parse_controls():
    global controls, gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()

    if gamepad:
        controls["MOVE_LEFT"] = gamepad.held("L")
        controls["MOVE_RIGHT"] = gamepad.held("R")
        controls["DROP"] = gamepad.held("D") and gamepad.pressed("A")
        controls["JUMP"] = gamepad.pressed("A")
        controls["JUMP_LEFT"] = gamepad.held("L") and gamepad.pressed("A")
        controls["JUMP_RIGHT"] = gamepad.held("R") and gamepad.pressed("A")
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["JUMP_LEFT"] = badge.held(BUTTON_A) and badge.pressed(BUTTON_C)
        controls["JUMP_RIGHT"] = badge.held(BUTTON_B) and badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]

background = image.load("assets/background.png")
branch = image.load("assets/branch.png")
sqirl_run_sheet = SpriteSheet("assets/running.png", 7, 1)
sqirl_die_sheet = SpriteSheet("assets/death.png", 4, 1)
sqirl_run = AnimatedSprite(sqirl_run_sheet, 0, 0, 7)
sqirl_die = AnimatedSprite(sqirl_die_sheet, 1, 0, 2)
acorn_sml = image.load("assets/acorn_sml.png")
title = image.load("assets/title.png")
gameover = image.load("assets/gameover.png")
title_font = rom_font.yesterday
acorn_lg = image.load("assets/acorn_lg.png")
score_font = rom_font.futile

gamepad = None
controls = {}

foreground_scroll_speed = 4
background_scroll_speed = 1
background_scroll_amount = 0
title_scroll_amount = 0

frame_counter = 0
player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0
last_frame = badge.ticks

save_state = {"highscore": 0}
State.load("acorn_highway", save_state)

init_gamepad()
init_platforms()

def title_loop():
    global current_game_state, title_scroll_amount

    draw_background()

    screen.blit(title, vec2(0, 0))

    branch_y = 73
    branch_tex_matrix = mat3().translate(title_scroll_amount, branch_y)
    title_scroll_amount -= foreground_scroll_speed
    title_scroll_amount %= branch.width

    branch_bar = shape.rectangle(0, branch_y, screen.width, 10)
    screen.pen = brush.image(branch, branch_tex_matrix)
    screen.shape(branch_bar)

    sqirl_x = (screen.width - 32) / 2
    sqirl_y = 43
    screen.blit(sqirl_run.frame(frame_counter), rect(sqirl_x, sqirl_y, 32, 32))

    screen.font = title_font
    screen.pen = color.white

    if int(badge.ticks / 500) % 2:
        restarttext = "Press any button!"
        centre_text(restarttext, 100)

    highscoretext = f"High score: {str(save_state["highscore"])}"
    centre_text(highscoretext, 85)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY

def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for acorn in acorns:
        acorn.move()

    for acorn in acorns:
        acorn.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM

def death_anim_loop():
    global current_game_state

    draw_background(False)

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER

def game_over_loop():
    global current_game_state, score, acorns

    screen.blit(gameover, vec2(0, 0))

    screen.font = title_font
    screen.pen = color.white

    if int(badge.ticks / 500) % 2:
        restarttext = "Press any button!"
        centre_text(restarttext, 100)

    scoretext = f"Your score: {str(score)}"
    centre_text(scoretext, 87)

    if score >= save_state["highscore"]:
        highscoretext = "High score!"
        save_state["highscore"] = score
        State.save("acorn_highway", save_state)
    else:
        highscoretext = f"High score: {str(save_state["highscore"])}"

    centre_text(highscoretext, 74)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        acorns.clear()
        current_game_state = game_state.TITLE

def update():
    global frame_counter, last_frame

    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.DEATH_ANIM:
        death_anim_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()

    if badge.ticks - last_frame > 83:
        frame_counter += 1
        last_frame = badge.ticks


run(update)
```