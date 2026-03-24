---
title: A simple game
summary: "Animation, sprites and interactivity"
icon: sports_esports
publish: true
---
# Tutorial 3: A simple game: Acorn Highway (Part 1)

It's time to put everything together to make a simple but fun game, with lots of scope for expansion. In this part and the next part we'll cover using sprites and animations, as well as structuring the game, working with properties to easily align objects, saving and loading data through states, and working with brushes to produce animation effects. You'll make the main gameplay loop, as well as an animation when you die, and animated title and game over screens.

The game you'll be making it called Acorn Highway, and it's a simple infinite runner / platformer. You control Tufty the squirrel, hopping from branch to branch to grab as many acorns as you can without falling out of the tree. Tufty can run very fast but has a lot of momentum, so part of the challenge is to know when _not_ to run or jump. Tufty earns one point for each platform passed, and another three points for each acorn collected.

# Setting up

First of all, let's set up basic classes for two very important things we'll be using. The basics of creating a MicroPython class are outside the scope of this tutorial, but we will talk a little about properties and how they work.

Create a new app with an icon, assets folder and `__init__.py`. Here's a good image to use as `icon.png` - just right click and save the image as a PNG.

![Icon image for Acorn Highway](/tut4_res/icon.png)

Inside `__init__.py` we'll make the classes. We will still need to do the usual `update()` loop, we'll just be putting it in later. We'll start by creating a class for the player:

```python-raw
class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0

    def draw(self):
        screen.pen = color.red
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)
```

`x` and `y` are the position of the top left of the player, with `w` and `h` being its width and height, which we're hard coding to 32 pixels, the dimensions of the sprite we'll be using later. `vy` and `vx` are the player's horizontal and vertical velocity, which we'll set at 0 for now, but they'll get changed by processing the physics and controls.

Then we've put in a `draw()` method too, that we can call whenever we want to draw the player. We'll be using a fancy animated sprite later, but for now we're just drawing a simple red box.

We'll keep all the class definitions together at the top of the file, right after any bits we need to import. After `player_base`, let's create an instance of it, and then add our `update()` loop just to check it's working:

```python-raw
player = player_base(20, 0)

def update():
    player.draw()

run(update)
```

This should give you a red square at the top of the screen, 20 pixels from the left. Of course, positioning things is nice and easy if you only ever want to check on the top left corner, but what about other positions on the player? We could store the position of the right and bottom as variables, and update them every time the x and y change, but there's a way that makes life simpler throughout the rest of the program. In the `player_base` class, add the following, after `__init__` and before `draw()`:

```python-raw
    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h
```

The `@property` on these makes them very useful. They're defined like methods, but they act like variables. They're like variables that aren't stored as a fixed value in the instance of the class, but calculated fresh every time the program asks for them, and it's that calculation that is in the methods you just added. So another part of the program could use, say, `player.r` in a calculation, and it would be whatever value is equal to the player's x position plus their width - or in other words, the player's right hand side. We can go further with this. Add the following after the above:

```python-raw
    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h
```

This essentially works the same, but in reverse. It allows people to assign values to `player.r` or `player.b`, and this will be taken in as the parameter `a` and used to calculate how to change the x and y coordinates. Let's try this out - alter `update()` so that the whole program looks like this:

```simulator
class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0

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

    def draw(self):
        screen.pen = color.red
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)

player = player_base(20, 0)

def update():
    player.x = 80
    player.y = 60
    player.draw()

    player.r = 80
    player.b = 60
    player.draw()

run(update)
```

As you can see, you're getting two squares. First, you're setting the top left corner of the box to be at `80, 60` - the centre of the screen, and you're drawing it. Then you're setting the bottom right corner to be at the same coordinates, and drawing it again. When you're setting `r` and `b` there, it's calculating what `x` and `y` need to be to put it in the right place.

We'll be making lots of other methods in `player_base`, but for now let's move on. This program is structured so that the things that effect each type of entity in the game are handled and processed by that entity, so the player class will be doing all of the calculations for moving the player, the platform class will do all the calculations for placing platforms, and so on. We'll make two new classes called `platform_base` and `acorn_base` and set them up with very simiilar properties to `player_base`. You could give them setters for `r` and `b` as you did for `player_base`, but it's not necessary, it doesn't get used.

```python-raw
class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    def draw(self):
        screen.pen = color.blue
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)
```

You'll notice `platform_base` has an extra parameter when you create it, which is just a unique name for that particular platform. It's not important now, but useful later. The length of the platform is also randomly generated for each one, somewhere between half the screen width and the full screen width. Remember to insert `import random` at the very beginning of the file to import the random number functions.

```python-raw
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

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)
```

The `acorn_base` class is basically the same as `player_base` at the moment. Given that all these properties are common between them you could potentially make a parent class which all of these are subclasses of, but that's beyond the scope of this tutorial. Here's an example of each one being created with fairly abitrary positions, then drawn to the screen:

```python
import random

class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0

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

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

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

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


player = player_base(20, 0)
platform = platform_base("a", 0, 80)
acorn = acorn_base(10, 45)

def update():
    player.draw()
    platform.draw()
    acorn.draw()

run(update)
```

# Basic physics

Now, let's apply some physics. We'll make an `update()` method in our `player_base` class, which we'll call to update the player's physics, and eventually process the controls. For now we just need two new lines in it, but we'll also move the call to `draw()` the player in here rather than in the main `update()` loop. That way we'll only need to call `player.update()`.

```python-raw
class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0

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

    def update(self):
        self.vy += 1

        self.x += self.vx
        self.y += self.vy

        self.draw()

    def draw(self):
        screen.pen = color.red
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)
```

So with those new lines, we're adding 1 to `vy`, the player's y speed, every update. And then we're adding the speed to the player's Y position. The end result - the player accelerates downward and falls off the bottom of the screen. Some say... it's still falling to this day. This is a very basic physics engine, though - if we're constantly adding to the speed, then that's an acceleration. That speed is a positive number on the y axis, so it's downward. A constant downward acceleration means that we've just given our game basic gravity.

However, a game where the player disappears off the edge of the screen within the first second isn't going to be winning any Game Of The Year awards, except maybe really artsy ones. Let's see if we can get it to land on the platform. For that, we need it to stop when it hits the platform, and to do that we'll add the following method into the `player_base` class:

```python-raw
    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False
```

This will return True if the player overlaps the platform horizontally, and the bottom of the player is at the top of the platform. But if you think about how the player's position is calculated using vx and vy, you'll notice it's sometimes moving several pixels in a frame. So we also need to check whether it passes through the top of the platform _between_ frames, as it were. That's not too hard, and just needs the following method adding to `player_base`:

```python-raw
    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False
```

You can see that this is very similar to `is_standing()` - it's just that there's an extra condition. That third line of the method checks if the bottom of the player is currently above the top of the platform, and also checks whether this will still be true if you add `vy` to the player's position, which is where it will be next frame. In other words, will it change from being above the platform to below it between this frame and the next? If so, we know we're landing this frame and we return `True`.

What we're going to do is first check if we're in the air to see whether we want to accelerate downward this frame. For this we'll use `is_standing()`. But then, before we move, we want to check if we're going to land next frame. If we are, we'll set our position to the top of the platform and our y speed to 0 so that next frame, `is_standing()` will catch it and not accelerate the player downward. Let's change the player's `update()` to look like this:

```python-raw
    def update(self):

        if not self.is_standing(platform):
            self.vy += 1

        if self.is_landing(platform):
            self.b = platform.y
            self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.draw()
```

The whole program should look like this:

```python
import random

class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0

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

    def update(self):

        if not self.is_standing(platform):
            self.vy += 1

        if self.is_landing(platform):
            self.b = platform.y
            self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.draw()

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

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

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

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


player = player_base(20, 0)
platform = platform_base("a", 0, 80)
acorn = acorn_base(10, 45)


def update():
    player.update()
    platform.draw()
    acorn.draw()


run(update)
```

You'll see that when you run it, no matter where you put the platform, as long as it's below the player they'll fall down and land on the platform.

# Multiple platforms

It would be a pretty boring platformer with only one platform, though. Let's switch it up a bit to make a list of platforms which we initialise to start with. We'll define this list where we created the platform before, and in fact while we're at it, let's do the same for the acorns as we know we'll want multiple of those, remembering to delete the line to draw the acorn:

```python-raw
player = player_base(20, 0)
platforms = []
acorns = []
```

That list is empty right now, but we're about to make a little method that fills it with three platforms in default starting positions. Although this is so short, we're making it a separate method so we can call on it later from elsewhere in the program. Dont forget to call `init_platforms()` in your main program, right before the `update()` loop.

```python-raw
def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]
```

So we're now setting up three different platforms. Let's make sure we draw them all by looping through the list in the `update()` method:

```python-raw
    for platform in platforms:
        platform.draw()
```

And before we can run this again, we'll also need to change up the player's `update()` method to check through every platform. To do this we'll make one more method in `player_base`, `is_airborne()`, which we'll use to check if we're in the air and just set a variable on the player, as it's something we need to check several times in a frame and we might as well just calculate it once. Here's our new `player_base`.

```python-raw
class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False

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

        if self.airborne:
            self.vy += 1

        for platform in platforms:
            if self.is_landing(platform):
                self.b = platform.y
                self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.draw()

    def draw(self):
        screen.pen = color.red
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)
```

Okay, by the end of this part your code should look like this:

```python
import random

class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False

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

        if self.airborne:
            self.vy += 1

        for platform in platforms:
            if self.is_landing(platform):
                self.b = platform.y
                self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.draw()

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

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

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

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


player = player_base(20, 0)
platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]
acorns = []

def update():
    player.update()

    for platform in platforms:
        platform.draw()


run(update)
```

The player drops down onto the top platform, and that's it. Of course, it'd be nice to actually move around, and we'll deal with that in the next part. We'll come back to the physics of it all once we've got a way of making things happen.

# Controls

There's two ways of implementing controls, and it depends on whether or not you want to include support for the Qw/ST Pad gamepad that comes as part of Badgeware's STEM kit. We'll end up at the same place either way, but if you're wanting to create something to share, it might be a good idea to learn here how to implement Qw/ST Pad for others to use.

## Control basics

Of course, the buttons on Badgeware are built in to the software API, but we're going to be creating a structure on top of that which lets you define in-game actions and refer to them by name. The benefit of this is that those in-game actions could be a combination of two or more buttons, so once they're defined it's easy to just check on them quickly elsewhere in the program - and that it'll read both the onboard buttons and any other input you care to mention.

We're going to need several things in place. First let's set up a dictionary for our controls. It doesn't need to have anything in it, as we'll populate it using a method we'll create, but it wants to go after our classes and before creating our player, platforms, and acorns:

```python-raw
controls = {}

player = player_base(20, 0)
platforms = []
acorns = []
```

And right before `init_platforms()` is defined, we'll create a method called `parse_controls()` which will fill that dictionary each turn with the appropriate values:

```python-raw
def parse_controls():
    global controls

    controls["MOVE_LEFT"] = badge.held(BUTTON_A)
    controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
    controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
    controls["JUMP"] = badge.pressed(BUTTON_C)
    controls["ANY_KEY"] = badge.pressed()
```

As you can see, we've now got a dictionary of controls which we can access by name. If you're using this structure in your own projects, the definitions for those can use any of `pressed()`, `released()`, `changed()` and `held()`, and as you can see we've used both `pressed()` and `held()` here as appropriate. You can also string these together with standard logic. Now, in your code you can just check, for example, `if controls["MOVE_LEFT"]` and it'll give you the appropriate `True` or `False`.

You can see that we've created five controls - moving left and right depend on a button being held, jumping just happens once on a press, and dropping uses a combination of holding down and pressing C. In this case C is also used as the jump button, but it doesn't have to be, it could be anything you like.

Now we've got our method for reading in the controls, we'll just call it at the very start of the main `update()` loop, so these values update every frame.

## Bringing in the gamepad

To bring in the Qw/ST Pad, we're just going to be adding to this structure. First of all we need to import that library, so at the very top of the file add `import qwstpad`.

Now, we need to connect to the pad and create an object we can read its buttons from. We'll make a method to initialise the gamepad, which we'll call `init_gamepad()` - this can go right before `parse_controls()` and after the classes. We'll also add in `gamepad = None` right before `controls = {}`.

```python-raw
def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None
```

This code uses the `qwstpad` library to check for the presence of Qw/ST Pads, and adds any it finds to a temporary list called `gamepads`. Then it just runs through the list and returns the first one that's connected. If there aren't any, it just returns None. Let's make sure we call this at the start of everything, inserting `init_gamepad()` right before `init_platforms()`

Now it's easy to use this to check for connected pads and assign the first one to the `gamepad` variable we made. Then when we're parsing controls we can just check if `gamepad` has a value that's not None to see if we need to check its controls. If we check regularly, each update, the system can even handle plugging and unplugging pads mid-game. Let's do that - first of all, we'll change the beginning of `parse_controls()` to read:

```python-raw
    global controls, gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()
```

We're defining `gamepad` as a global, so that it's looking at the right variable, and then if it's connected we're telling it to read the status of all of its buttons. We're also enclosing that in a `try` statement so that if it throws an error (as it would if the pad was disconnected unexpectedly) it ignores reading the gamepad for this update and instead just tries to initialise it again for the next update. If there isn't a pad connected it'll try and connect to one, because you never know, someone might have just plugged one in.

Now that we've got access to the gamepad's buttons, we can integrate them into the controls. This is very simple, just an `if` statement checking on the gamepad's status, and then a set of new definitions for if it's connected. The `qwstpad` library for Badgeware provides the same methods you can call on the Badgeware buttons, just using strings to identify the buttons - your options are `U, D, L, R, A, B, X, Y, +, -`.

Let's see the `parse_controls()` method with that added in.

```python-raw
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
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()
```

You can see that currently, the badge buttons would essentially be disabled when the gamepad was plugged in, but it doesn't have to be like that - you could use `or` statements to allow either button to activate the control.

So, we've got a set of controls we can query for our game mechanics. But currently you can't even tell if they're working or not, since they're not hooked up to anything. Next up, let's learn to move.

# Player movement

## Jumping

We'll start with a simple jump. For this we're going back up to the `player_base` class - remember, all movement _of_ the player is handled _by_ the player, so we're going to put this in `player_base`'s `update()` method.

You don't want to be able to jump while you're in the air, but fortunately we already created `airborne` to check whether that's the case. There's even an `if` statement already there for checking whether we should fall. Let's just modify that with an `else`, and check our controls to see if we need to jump:

```python-raw
        if self.airborne:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10
```

So if we're standing on a platform, we'll check to see if the button we've assigned to jump has been pressed that frame, and if so we're setting `vy` to -10. Remember, y increases going downwards in screen coordinates, so a negative value will give us an instant upward speed. That will slowly be decreased over the next few frames by the code we've already written though, so that we're falling again.

Here's the full code so far:

```python
import qwstpad
import random

class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False

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

        if self.airborne:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

        for platform in platforms:
            if self.is_landing(platform):
                self.b = platform.y
                self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.draw()

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

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

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

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


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
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


gamepad = None
controls = {}

player = player_base(20, 0)
platforms = []
acorns = []

init_gamepad()
init_platforms()

def update():
    parse_controls()

    player.update()

    for platform in platforms:
        platform.draw()


run(update)
```

## Running

Running is easy, we just add a bit of acceleration to the player in the appropriate direction. Again, just like jumping, we only want to be able to run if we're standing on a platform, so we can add this in right after our jump, within that same `else` statement:

```python-raw
    if controls["MOVE_RIGHT"]:
        self.vx += 1.5

    if controls["MOVE_LEFT"]:
        self.vx -= 1.5
```

Test that now and you'll find two things - first, you just accelerate and don't stop, and second, you disappear off the edge of the screen. We can remedy the second one easy enough. Right after changing the player's position and before drawing them, we can clamp your position using the following line:

```python-raw
    self.x = clamp(self.x, 0, screen.width - self.w)
```

Now you'll see you'll at least not fly off the screen, but that speed is still wild. You're a squirrel, not a rocket. We want it to be pretty nippy, part of the gameplay is that you're controlling something very fast moving, but we clearly need some kind of damping. That's easy enough to implement - right after our movement controls, within that same `else` statement, let's say:

```python-raw
    if self.vx > 0: self.vx -= 0.5
    elif self.vx < 0: self.vx += 0.5
```

So now your speed is reduced by 0.5 every frame you're touching the ground. Tufty still clearly has the zoomies, but you can see that there is now a deceleration after a light tap on the buttons.

## Dropping

Let's also look at dropping through the platforms. This is easy, as we've already established a control for drop, and all we want to happen when it's activated is for the player to start falling under gravity. We have that condition anyway - it applies whenever the player is airborne - so we just need to add to that check to tell it to also fall if we've hit 'Drop':

```python-raw
        if self.airborne or controls["DROP"]:
```

## Jumping sideways

And finally, we can already jump sideways if we've got a running start, but given how much we're bouncing between platforms it might be good to actually have a sideways jump. For this, let's create new controls in `parse_controls()`:

```python-raw
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
```

We're treating this just like the Drop command and checking for jump being pressed while a direction is held. We can just add these lines in too, after the jump command and before the movement:

```python-raw
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
```

You'll see we've altered the existing commands to include a couple of `elif`s there. If Jump has been pressed, we always want to get that upward acceleration whether we're pressing left, right or nothing, so it just uses `if`. But the rest of the controls we want to each do a specific thing, so they're in their order of priority and made exclusive using `elif` statements.

For the `JUMP_LEFT` and `JUMP_RIGHT` commands, we've already got the vertical movement from `JUMP`, so we can just concentrate on giving Tufty a horizontal boost. If you're jumping sideways, your speed will be set to 3 unless it's already more than 3. That way, if you are taking a running jump, you won't suddenly slow down when you jump.

## Final player movement bits

And that's it! That's pretty much everything for player movement. There's one more thing, and while it won't come up until a bit later we can set the groundwork for it now. When you die, we want you to pass through all of the platforms and not land on them. So, we can just add `self.dead = False` to our `__init__()` method, and then check for it when checking for whether we fall:

```python-raw
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False
```

```python-raw
        if self.airborne or self.dead or controls["DROP"]:
```

For the moment, `dead` will just stay permanently on `False`, but watch out for it, it'll show up again. You'll notice that because all of the controls are in the `else` after the `if`, that being dead will also automatically disable all of your control inputs. Here's the code you should have if you've been following along:

```python
import qwstpad
import random

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

        for platform in platforms:
            if self.is_landing(platform):
                self.b = platform.y
                self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

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

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

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

    def draw(self):
        screen.pen = color.lime
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


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

player = player_base(20, 0)
platforms = []
acorns = []

init_gamepad()
init_platforms()

def update():
    parse_controls()

    player.update()

    for platform in platforms:
        platform.draw()


run(update)
```

We're not quite done with the `player_base` class overall, but we're at least done for now. Now, we'll work on getting some scrolling platforms.

# Making the platforms move

So you can move, but what about your environment? This infinite runner doesn't feel very infinite right now. We presumably need an infinite number of platforms to scroll past for Tufty to jump on, right? Well, not quite, because we're going to cheat. We could keep spawning new platforms off the right hand side of the screen, but we'd need to destroy them again once they had passed, otherwise they'd just take up more and more memory and processing power the longer you played.

Creating and destroying objects is comparatively computationally expensive, so we're going to take an eco-friendly approach and just recycle the platforms we have. So we'll just stick to the three platforms we've already made, and as soon as each one disappears off the left side of the screen, we'll move it back to the right side. We'll also reset its length to a new random length.

Because the platforms are random lengths, it means that they'll respawn at different times and be in different positions relative to each other every time. We can chaos it up a little further by making them respawn at a random height on the screen.

First though, we need to make them scroll in the first place. Just like `player_base` for the player's behaviour, all of the platforms' behaviour is going to be taken care of within `platform_base`. First, let's make an `update()` method inside `platform_base` and use that to call `draw()`:

```python-raw
    def update(self):
        self.draw()
```

Don't forget to change the call in the main `update()` loop to `platform.update()` instead of `platform.draw()`.

Scrolling is pretty easy. Let's set a global `foreground_scroll_speed` variable with a value of 4, so that if we need to change it we only have to change it in one place. Let's put it right after `controls = {}`. Then, we just need to subtract this value from the platform's x co-ordinate every frame, and voila! Scrolling platforms. It should look like this:

```python-raw
    def update(self):
        self.x -= foreground_scroll_speed
        self.draw()
```

And now you should see that all the platforms scroll off the screen and the player drops down into the endless void. Probably a good metaphor for something, but not great for gameplay - still, it's something. Now we just need to get them to reappear on the other side.

To do this, we can easily just check to see if the right hand side of the platform is at less than zero in x, and if it is, let's set the platform's x coordinate to the screen width:

```python-raw
    def update(self):
        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.x = screen.width

        self.draw()
```

And all of a sudden, there's gameplay! It's very fast-paced and pretty difficult, but playable. It'll slow down a little once we've got it crunching numbers on all the graphics, but it's intended to still be pretty speedy even then.

## Renewing platforms

Right now, the platforms are staying at their original size and their original height - that's not getting changed when they respawn. Let's cleanly make that happen by making a `reset()` method in `platform_base` which takes care of all of those things, and then just calling that.

```python-raw
    def update(self):
        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()

        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)
```

Now they're randomised alright, but we've got a problem - they keep overlapping one another. We need to check whether a platform is going to respawn in the same space as another, and make it choose somewhere else if it does so. For this we can take advantage of a property that Badgeware's `rect` object has, which is a very quick check to see if it intersects with another `rect`. Useful!

But where are we going to get that `rect` from? Well, just like `r` and `b`, we can make it a property. We'll just add the following in below the definitions for those two:

```python-raw
    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)
```

Now we can just access `platform.bounding_box` and get the `rect` we want. Let's add the same property into `player_base` and `acorn_base` too - it's not needed right now, but we'll want it down the line.

Now we've got everything we need to, when we reset a platform, check against the other platforms and see if its bounding box intersects their bounding box. If it does, we'll just keep resetting until it finds a position that's good. Let's create a new method in `platform_base`, right after `reset()`:

```python-raw
    def check_collisions(self):
        global platforms
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False
```

This is where that `id` property comes in. The program is running through the global platforms list, and checking against the other platform using `rect.intersects()` to see if they overlap. But of course, it doesn't want to check against its own bounding box. After all, wherever you go to, there you are.

So we're just checking the `id` of each platform and if it's our own `id`, we're just skipping it. If at any point we find an overlap, we can just finish early and return `True`, or if we don't find an overlap then we're all good and can return `False`.

We call this method right after resetting the platform, and loop it using `while` until it comes back `False`. If we're lucky, that's first time, but generally it needs a few go rounds:

```python-raw
    def update(self):
        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()

        self.draw()
```

Run this now, and you'll see that you've got rid of the overlapping platforms. But they're still spawning _really_ close to each other. Well, we can sort this easily by just changing the size of the bounding box. Let's put a value called `keepout` into the platform's `__init__()`, and set it to 5 - this will be the number of pixels beyond the platform's borders the bounding box wants to extend.

```python_raw
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5
```

Then we can alter the method we use to generate the bounding box, using `keepout` to give it its new size and position. Note that it's only the bounding box in `platform_base` you're changing, the others can stay as you originally created them:

```python-raw
    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))
```

And now we've got nicely spawning, nicely spaced platforms.

> Note: It's possible to get the game to lock up completely here. If you decide you want more than three platforms at once, or if the keepout value is too high, then it's possible to get a situation where there isn't a big enough gap for a new platform to spawn into. If this happens, then the game will completely freeze while it goes round in an endless loop trying to find a gap and never finding one. Which makes Tufty sad.

Here's your code so far:

```python
import qwstpad
import random

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

        for platform in platforms:
            if self.is_landing(platform):
                self.b = platform.y
                self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

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
        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()

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

init_gamepad()
init_platforms()

def update():
    parse_controls()

    player.update()

    for platform in platforms:
        platform.update()


run(update)
```

Looking good. But what we've got right now is a gameplay snippet, nothing more. Let's turn it into something with a start and a finish.

# Game states

To start off with, we're going to introduce three basic states - the title screen, gameplay, and the game over screen. The loop will be that the game starts at the title screen, switches to the gameplay screen when any button is pressed, switches to the game over screen when you die, then switches back to the title screen when you press any button on the game over screen.

First, let's do some setup. We'll make a little mini class to define our game states. At the very top of the file, right below the imports and and before `player_base`, we're going to add the following class:

```python-raw
class game_state:
    TITLE = 0
    GAMEPLAY = 1
    GAMEOVER = 3
```

That's it, that's the whole class. Don't worry about the numbers going "0, 1, 3" - that certainly isn't foreshadowing about a secret fourth state we're going to add later or anything, nooo, not at all.

You can see that these are static variables - we're not making an instance of this class anywhere, it's just going to sit there as a shorthand to make the code readable. We could just have an global variable called `game_state` and set it to different numbers to indicate different states, but this way stops us having to remember "Was it 1 that was gameplay, or was that 2?". Plus, having a name in the code means that anyone else looking at it will immediately understand what's going on in a way that they wouldn't with just a number.

Now let's make a global variable that keeps track of which state we're in. We'll put it just after setting up our player, platforms, and acorns:

```python-raw
player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
```

Now, we're going to put a series of checks into the main `update()` which lets it choose what it wants to do based on what `current_game_state` is set to. We'll leave `parse_controls()` where it is, since you're going to need to read button inputs whatever state you're in. Let's rewrite `update()` so it looks like this:

```python-raw
def update():
    parse_controls()

    if current_game_state == game_state.TITLE:
        title_loop()
    elif current_game_state == game_state.GAMEPLAY:
        gameplay_loop()
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()
```

It's a very simple `update()`, since all the fancy stuff is happening in those methods with `_loop` in the names. Of course, right now this would just throw up an error as we haven't written any of those methods yet, so let's write them. We'll put them directly before `update()` and keep them simple to start with - you can see that `gameplay_loop()` just contains the lines we removed from `update()`, and the other two just draw a line of text:

```python-raw
def title_loop():
    screen.text("Title screen", 0, 0)

def gameplay_loop():
    player.update()

    for platform in platforms:
        platform.update()

def game_over_loop():
    screen.text("Game Over screen", 0, 0)
```

Well, this seems like a step backwards. Try running it now, and you'll just get a black screen with "Title screen" written on it that you can't get out of. And of course that's because we started with the state set to `TITLE` and we've got nothing in place to change it. You can see the stuff that used to be in `update()` right there in `gameplay_loop()`, we just can't get to it yet. That's easily fixed, we just check for a button press each frame and when it's pressed, we move it onto the next one:

```python-raw
def title_loop():
    global current_game_state

    screen.text("Title screen", 0, 0)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY

def gameplay_loop():
    player.update()

    for platform in platforms:
        platform.update()

def game_over_loop():
    global current_game_state

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        current_game_state = game_state.TITLE
```

> Note: When you're using globals in a method like we are here, you need to declare them at the top of the method. We've mentioned this before, but it's worth a reminder here as it's one of the easier things to forget to do, especially if the code that uses them isn't anywhere near the top of the method. If your code isn't working and you're not sure why, this is a good first thing to double check.

## Losing the game

That gets us into gameplay, but now we can't get out of it - there's no lose condition yet. Well, we know when we want game over to happen - when the player falls off the screen. So we could simply do a check for the player hitting the bottom edge of the screen instead of a button press. Simple!

```python-raw
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

    if player.b >= screen.height:
        current_game_state = game_state.GAME_OVER

def game_over_loop():
    global current_game_state

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        current_game_state = game_state.TITLE
```

Hmmm, well now there's another problem. That loop seems to work okay once - title screen, gameplay till you die, game over screen, title screen - but then the second time round it flashes up gameplay for a single frame and goes straight to game over. What's happening?

## Resetting everything

Well, the gameplay loop is checking for the player being at the bottom of the screen, and after playing for the first time and losing, that's where the player is. We haven't moved them or anything, so as soon you start over, you're already in a game over situation and on the next frame it'll kick you back to the game over screen.

Not too big of a problem though - let's just put a `reset()` method into `player_base`, right before `draw()`:

```python-raw
    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
```

Then we call that so that the player is reset when we start a new game. You might think this happens in the title screen method, but if it did then it would be carried out every frame - not a problem for resetting the player's position, but for other things later on it would cause issues. So, anything we want to happen just once when you first enter a game state goes in the same block of code that switches to that game state.

In this case that means we reset the score at the end of the game over screen, when we're switching the game state back to the title screen:

```python-raw
def game_over_loop():
    global current_game_state, score

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        player.reset()
        current_game_state = game_state.TITLE
```

That'll just reset the player back to the starting position and zero out their speed. You might notice we've still not used that `dead` property of the player, but that'll come in later still. The suspense must be killing you. And now we've got a full gameplay loop.

It's still not quite right though. Do you notice that after you finish your first playthrough, after that you sometimes just fall and die instantly because there's no platform beneath you? That's as a result of the same thing - the platforms aren't resetting, they're exactly where you left them. Easily fixed though - we'll call `init_platforms()` that we made ages ago to reset their positions, and we'll do it right after we reset the player:

```python-raw
    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        current_game_state = game_state.TITLE
```

# Scoring

What's next, then? How about a score? Say, one point for every platform you pass? Sounds good. Let's add in a global variable named `score`. It can go right after we initially set the game state, and of course it wants to start off set to zero. We can easily increase the score by adding it as a global into the `update()` method of `platform_base`, and then adding in `score += 1` just after the `while` loop to find a new position for the platform:

```python-raw
    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1

        self.draw()
```

That way, the score goes up by one every time a platform passes off the left side of the screen. We should probably display the score, too. Now, we'll just do a line of text for now, but we're going to be displaying the score in a fancier way later on so it makes sense to set up a separate method for it ahead of time. We'll make a method just before `init_gamepad()` (or `parse_controls()` if you didn't set up the gamepad), as follows:

```python-raw
def draw_score():
    global score
    screen.text(str(score), 0, 0)
```

Then we can call it after we've drawn everything else:

```python-raw
def gameplay_loop():
    global current_game_state

    player.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.reset()
        current_game_state = game_state.GAMEOVER
```

The final thing is to reset the score when you go back to the title screen. That'll happen at the end of the game over screen, at the same time as we're resetting the player and platforms:

```python-raw
def game_over_loop():
    global current_game_state, score

    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        current_game_state = game_state.TITLE
```

By this point you should be working with something a lot like this:

```python
import qwstpad
import random


class game_state:
    TITLE = 0
    GAMEPLAY = 1
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
    elif current_game_state == game_state.GAMEOVER:
        game_over_loop()


run(update)
```

# Losing, but properly

We'll get into the fancy graphics soon. But first, does that dying seem abrupt to you? Hit the bottom of the screen and then boom, straight to game over? In fact, if you're mashing the buttons it's easy to accidentally hit it an extra time and skip the game over and even the title screen.

Well, we can remedy that with a.... secret fourth state nobody knew about! Who could have seen that coming?

This is going to be a little death animation similar to those you see in classic Sonic or Mario games, where the player bounces up from the bottom of the screen, then falls back down and disappears. Once we've got our full graphics, we can use a different sprite animation to show the owies.

First of all, let's create that missing game state, by adding in `DEATH_ANIM = 2` in the appropriate place in our `game_state` class. Then, we'll do the same to set it up in `update()` and create a `death_anim_loop()` method, such that it sits in between `GAMEPLAY` and `GAMEOVER`. You'll also need to change `gameplay_loop()` so that it points to `DEATH_ANIM` instead of `GAMEOVER`.

What's going in this method, though? Well, for now, it's just going to almost be a copy of `gameplay_loop()`:

```python-raw
def death_anim_loop():
    global current_game_state

    for platform in platforms:
        platform.draw()

    player.update()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER
```

Can you spot the difference? In this state, we're calling `platform.draw()` instead of `platform.update()`. That means they'll still get drawn, but they won't move, reset or anything else. The scrolling stops when you die.

But surely that won't matter, because this screen will only be up for a single frame, right? Nothing has reset the player's position, so it'll display, detect that the player is at the bottom of the screen and then move on to the game over screen, surely?

Absolutely, that's what would happen with things as they are right now. But that same hitting-the-screen-bottom logic is still going to be what takes us to the game over screen in the end. We've just got to stop it firing off too early.

We're going to create one more method within `player_base`, with the delightful name of `death()`, which should be placed right after the player's `reset()` method:

```python-raw
    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True
```

You might be able to see where this is going. It's just like the `reset()` method, only it's leaving the player where they are in x, moving them to just one pixel above the screen bottom in y so that they won't trigger the game over screen, and giving them an upward speed just a little bigger than a normal jump. It's also, finally, doing something with that `dead` property, setting it to True.

This will mean that when the player updates, they'll be subject to gravity and all of the controls will be locked out.  We need to do one more thing with that here, though. In the player's `update()` method, we need to put that check for landing on a platform behind a test of `dead` so that they'll just fall through platforms and not land on them:

```python-raw
        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0
```

Finally we just need to add a line to the player's `reset()` method to set `dead` back to False when the player resets, otherwise they'd start off the gameplay dead. Which is a terrible way to begin any adventure.

```python-raw
    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False
```

We also need to call `player.death()` when we switch from `GAMEPLAY` to `DEATH_ANIM`, just like we reset the player when going from `GAMEOVER` to `TITLE`

Now you might be able to see what's going to happen. When you hit the bottom of the screen the first time, it goes into the `DEATH_ANIM` mode. This stops the platforms from scrolling, moves the player up a tiny bit so they won't immediately trigger the game over screen, and gives them a boost upward while disabling controls and collisions with platforms. Since they're still being affected by gravity, they're going to bounce up, fall down and then trigger the game over screen when they hit the bottom of the screen again.

And by jingo, it works. Here's the full code so far:

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

Now, it runs very fast, so it's pretty difficult. And it's not especially attractive. But that's what the other part of the tutorial is for. We're going to take this functional starting point and give it that beautiful Triple-A Badgeware sheen, as well as adding acorns for Tufty to collect, and a couple of other bells and whistles too.