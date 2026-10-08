---
title: "A simple game - part 1"
summary: "Gameplay"
icon: sports_esports
publish: true
sort: 3
---
# Tutorial 3: Acorn Highway (Part 1)

It's time to put everything together to make a simple but fun game, with lots of scope for expansion. In this part and the next part we'll cover using sprites and animations, as well as structuring the game, working with properties to easily align objects, saving and loading data through states, and working with brushes to produce animation effects. You'll make the main gameplay loop, as well as an animation when you die, and animated title and game over screens.

The game you'll be making it called Acorn Highway, and it's a simple infinite runner / platformer. You control Tufty the squirrel, hopping from branch to branch to grab as many acorns as you can without falling out of the tree. Tufty can run very fast but has a lot of momentum, so part of the challenge is to know when _not_ to run or jump. Tufty earns one point for each platform passed, and another three points for each acorn collected.

> Note: Whenever it's time to run your program to test something, you'll see an icon of Tufty running like the one below.

![Run your code!](/tut4_res/tufty.gif)

## Setting up

First of all, let's set up basic classes for three very important things we'll be using. The basics of creating a MicroPython class are outside the scope of this tutorial, but we will talk a little about properties and how they work.

Create a new app with an icon, assets folder and `__init__.py`. Here's a good image to use as `icon.png` - just right click and save the image as a PNG.

![Icon image for Acorn Highway](/tut4_res/icon.png)

Inside `__init__.py` we'll make the classes. We will still need to create a loop, we'll just be creating our own custom one instead of using the built in `update()`. We'll start by creating a class right at the top of the file for all of the things that we need to keep track of and access from other parts of the program. For now, we'll just add the following at the very top of the file:

```python-raw
class game:
    pass
```

We've not put anything inside it yet, but as we go we'll add things to this. You'll notice as we do that those things will not use `self.` to make them into variables that can change per instance - we're not going to be making any instances of this class, just using it as a convenient store for things to access, so they'll go directly inside the class as static variables.

Then, directly after that, we'll make a class for the player:

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

We'll keep all the class definitions together at the top of the file, right after any bits we need to import. After `player_base`, let's create an instance of it, and we'll also need to add our main program loop to check it's working.

Instead of `update()`, we're going to make our own loop at the very bottom of the program using `while`. It uses `while True`, so it'll loop forever just like `update()`, but this way we have more control over what happens when we update. Inside, we'll put individual commands to clear the screen with `badge.clear()`, read the badge's buttons using `badge.poll()`, and to update the screen once we've drawn what we want with `display.update()`.

```python-raw
while True:
    badge.clear()
    badge.poll()
    display.update()
```

With what we're putting in the loop right now, it can go anywhere as long as it's before we update the display, but when we implement things later we'll want to check our controls before we do anything else - so let's call the `draw()` function in between the two commands. Altogether, that's:

```python-raw
player = player_base(20, 0)

while True:
    badge.clear()
    badge.poll()

    player.draw()

    display.update()
```

![Run your code!](/tut4_res/tufty.gif)

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

```python
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

while True:
    badge.clear()
    badge.poll()

    player.x = 80
    player.y = 60
    player.draw()

    player.r = 80
    player.b = 60
    player.draw()

    display.update()
```

![Run your code!](/tut4_res/tufty.gif)

As you can see, you're getting two squares. First, you're setting the top left corner of the box to be at `80, 60` - the centre of the screen, and you're drawing it. Then you're setting the bottom right corner to be at the same coordinates, and drawing it again. When you're setting `r` and `b` there, it's calculating what `x` and `y` need to be to put it in the right place.

We'll be making lots of other methods in `player_base`, but for now let's move on. This program is structured so that the things that effect each type of entity in the game are handled and processed by that entity, so the player class will be doing all of the calculations for moving the player, the platform class will do all the calculations for placing platforms, and so on. We'll make two new classes called `platform_base` and `acorn_base` and set them up with very simiilar properties to `player_base`. For the sake of completeness you could give them setters for `r` and `b` as you did for `player_base`, but it's not necessary, they won't be used.

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

You'll notice `platform_base` has an extra parameter that gets passed in when it's initialised, which is just a unique name for that particular platform that we're storing as `self.id`. It's not important now, but will be useful later. The length of the platform is also randomly generated for each one, somewhere between half the screen width and the full screen width. Remember to insert `import random` at the very beginning of the file to import the random number functions.

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

The `acorn_base` class is basically the same as `player_base` at the moment. Given that all these properties are common between them you could potentially make a parent class which all of these are subclasses of, but that's beyond the scope of this tutorial. We'll make an example of each one being created with fairly arbitrary positions, then drawn to the screen:

```python-raw
player = player_base(20, 0)
platform = platform_base("a", 0, 80)
acorn = acorn_base(10, 45)

while True:
    badge.clear()
    badge.poll()

    player.draw()
    platform.draw()
    acorn.draw()

    display.update()
```

Which all together looks like this:

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

while True:
    badge.clear()
    badge.poll()

    player.draw()
    platform.draw()
    acorn.draw()

    display.update()
```

![Run your code!](/tut4_res/tufty.gif)

## Basic physics

Now, let's apply some physics. We'll make an `update()` method in our `player_base` class, which we'll call to update the player's physics, and eventually process the controls. For now we just need two new lines in it, but we'll also move the call to `draw()` the player into here rather than in the main loop. That way we'll only need to call `player.update()` - make sure you change the call in the loop to reflect that.

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

This will return True if the player overlaps the platform horizontally, and the bottom of the player is at the top of the platform. But if you think about how the player's position is calculated using vx and vy, you'll notice it's sometimes moving several pixels in a frame. So we also need to check whether it will pass through the top of the platform between this frame and the next one. That's not too hard, and just needs the following method adding to `player_base`:

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


class game:
    pass


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

while True:
    badge.clear()
    badge.poll()

    player.update()
    platform.draw()
    acorn.draw()

    display.update()

```

![Run your code!](/tut4_res/tufty.gif)

You'll see that when you run it, no matter where you put the platform, as long as it's below the player they'll fall down and land on the platform.

## Multiple platforms

It would be a pretty boring platformer with only one platform, though. Let's switch it up a bit to make a list of platforms which we initialise to start with. We'll define this list as the first thing in our `game` class and in fact while we're at it, let's do the same for the acorns as we know we'll want multiple of those. Remember to delete our old lines where we set up `platform` and `acorn`, as well as the line to draw the acorn in the main loop. Your `game` class should look like this:

```python-raw
class game:
    platforms = []
    acorns = []
```

Those lists are empty right now, but we're about to make a little function that fills the platform list with three platforms in default starting positions. Although this is short, we're making it a separate function after the classes so that we can call on it later from elsewhere in the program. Dont forget to call `init_platforms()` in your main program, right before the loop.

```python-raw
def init_platforms():
    game.platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]
```

You can see that because it's in that class we made, we're able to just access the list wherever we are in the program with `game.platforms`, which means we don't need to mess around with Micropython globals.

So we're now setting up three different platforms. Let's make sure we draw them all by looping through the list in the `while` loop:

```python-raw
    for platform in game.platforms:
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
        for platform in game.platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne:
            self.vy += 1

        for platform in game.platforms:
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


class game:
    platforms = []
    acorns = []


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
        for platform in game.platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne:
            self.vy += 1

        for platform in game.platforms:
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


def init_platforms():
    game.platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


player = player_base(20, 0)
init_platforms()

while True:
    badge.clear()
    badge.poll()

    player.update()
    for platform in game.platforms:
        platform.draw()

    display.update()

```

![Run your code!](/tut4_res/tufty.gif)

The player drops down onto the top platform, and that's it. Of course, it'd be nice to actually move around, and we'll deal with that in the next part. We'll come back to the physics of it all once we've got a way of making things happen.

## Controls

There's two ways of implementing controls, and it depends on whether or not you want to include support for the Qw/ST Pad gamepad that comes as part of Badgeware's STEM kit. We'll end up at the same place either way, but if you're wanting to create something to share, it might be a good idea to learn here how to implement Qw/ST Pad for others to use.

### Control basics

Of course, the buttons on Badgeware are built in to the software API, but we're going to be creating a structure on top of that which lets you define in-game actions and refer to them by name. The benefit of this is that those in-game actions could be a combination of two or more buttons, so once they're defined it's easy to just check on them quickly elsewhere in the program - and that it'll read both the onboard buttons and any other input you care to mention.

We're going to need several things in place. First let's set up a dictionary in the `game` class for our controls. It doesn't need to have anything in it, as we'll populate it using a function we'll create. `game` should look like this:

```python-raw
class game:
    platforms = []
    acorns = []
    controls = {}
```

And right before `init_platforms()` is defined, we'll create a function called `parse_controls()` which will fill that dictionary each turn with the appropriate values:

```python-raw
def parse_controls():
    game.controls["MOVE_LEFT"] = badge.held(BUTTON_A)
    game.controls["MOVE_RIGHT"] = badge.held(BUTTON_C)
    game.controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_B)
    game.controls["JUMP"] = badge.pressed(BUTTON_B)
    game.controls["ANY_KEY"] = badge.pressed()
```

As you can see, we've now got a dictionary of controls which we can access by name. If you're using this structure in your own projects, the definitions for those can use any of `pressed()`, `released()`, `changed()` and `held()`, and as you can see we've used both `pressed()` and `held()` here as appropriate. You can also string these together with standard logic. Now, in your code you can just check, for example, `if game.controls["MOVE_LEFT"]` and it'll give you the appropriate `True` or `False`.

You can see that we've created five controls - moving left and right depend on a button being held, jumping just happens once on a press, and dropping uses a combination of holding down and pressing B. In this case B is also used as the jump button, but it doesn't have to be, it could be anything you like.

Now we've got our function for reading in the controls, we'll just call it at the start of the main `while` loop, right after `badge.poll()`, so these values update every frame.

### Bringing in the gamepad

To bring in the Qw/ST Pad, we're just going to be adding to this structure. The badge detects when a Qw/ST pad is connected, and by default it maps some of the pad buttons to do the same as the badge's face buttons - Up, Down, A, B and C go to Up, Down, Left, B and Right on the pad.

That's probably fine for a lot of apps, but we'll do something a little different here - we can separate out some of our controls if there's a pad connected, since we've got more buttons to play with. Let's say that instead of pressing down and jump to drop, on the pad you just press Down. Also, let's have Tufty jump when any of the buttons on the right side of the pad are pressed.

To do this, first we'll need to disable the existing mappings. There's a function in `badge` to set the pad mappings - we provide it with a dictionary of which pad button maps to which badge button, like so:

```python-raw
badge.pad_map({
    PAD_UP: BUTTON_UP,
    PAD_DOWN: BUTTON_DOWN,
    PAD_LEFT: BUTTON_A,
    PAD_RIGHT: BUTTON_C,
    PAD_B: BUTTON_B,
})
```

That's the default configuration. Now if we just wanted to change around what buttons do what, we could just provide it with a different dictionary. However, we're taking a different route. On the line before `init_platforms()` is called, add the following:

```python-raw
badge.pad_map({})
```

That's setting the map to an empty dictionary, breaking the link between the pad controls and the badge controls. Now we'll set up our gamepad to read the buttons. Right after the above line, add the following:

```python-raw
game.gamepad = badge.pad[0]
```

This sets up a variable inside `game` for the first gamepad that's connected. Now that we've got access to the gamepad's buttons, we can integrate them into the controls. This is very simple, we're just asking the badge to check for either the badge button or the gamepad button being pressed. The options for the badge buttons are:

- PAD_UP
- PAD_DOWN
- PAD_LEFT
- PAD_RIGHT
- PAD_A
- PAD_B
- PAD_X
- PAD_Y
- PAD_PLUS
- PAD_MINUS

Let's see the `parse_controls()` function with that added in.

```python-raw
def parse_controls():
    game.controls["MOVE_LEFT"] = badge.held(BUTTON_A) or game.gamepad.held(PAD_LEFT)
    game.controls["MOVE_RIGHT"] = badge.held(BUTTON_C) or game.gamepad.held(PAD_RIGHT)
    game.controls["DROP"] = (badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_B)) or game.gamepad.pressed(PAD_DOWN)
    game.controls["JUMP"] = badge.pressed(BUTTON_B) or game.gamepad.pressed(PAD_A) or game.gamepad.pressed(PAD_B) or game.gamepad.pressed(PAD_X) or game.gamepad.pressed(PAD_Y)
    game.controls["ANY_KEY"] = badge.pressed() or game.gamepad.pressed()
```

So, we've got a set of controls we can query for our game mechanics. But currently you can't even tell if they're working or not, since they're not hooked up to anything. Next up, let's learn to move.

## Player movement

### Jumping

We'll start with a simple jump. For this we're going back up to the `player_base` class - remember, all movement _of_ the player is handled _by_ the player, so we're going to put this in `player_base`'s `update()` method.

You don't want to be able to jump while you're in the air, but fortunately we already created `airborne` to check whether that's the case. There's even an `if` statement already there for checking whether we should fall. Let's just modify that with an `else`, and check our controls to see if we need to jump:

```python-raw
        if self.airborne:
            self.vy += 1
        else:
            if game.controls["JUMP"]:
                self.vy = -10
```

So if we're standing on a platform, we'll check to see if the button we've assigned to jump has been pressed that frame, and if so we're setting `vy` to -10. Remember, y increases going downwards in screen coordinates, so a negative value will give us an instant upward speed. That will slowly be decreased over the next few frames by the code we've already written though, so that we're falling again.

Here's the full code so far:

```python
import random


class game:
    platforms = []
    acorns = []
    controls = {}


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
        for platform in game.platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne:
            self.vy += 1
        else:
            if game.controls["JUMP"]:
                self.vy = -10

        for platform in game.platforms:
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


def parse_controls():
    game.controls["MOVE_LEFT"] = badge.held(BUTTON_A) or game.gamepad.held(PAD_LEFT)
    game.controls["MOVE_RIGHT"] = badge.held(BUTTON_C) or game.gamepad.held(PAD_RIGHT)
    game.controls["DROP"] = (badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_B)) or game.gamepad.pressed(PAD_DOWN)
    game.controls["JUMP"] = badge.pressed(BUTTON_B) or game.gamepad.pressed(PAD_A) or game.gamepad.pressed(PAD_B) or game.gamepad.pressed(PAD_X) or game.gamepad.pressed(PAD_Y)
    game.controls["JUMP_LEFT"] = game.controls["MOVE_LEFT"] and game.controls["JUMP"]
    game.controls["JUMP_RIGHT"] = game.controls["MOVE_RIGHT"] and game.controls["JUMP"]
    game.controls["ANY_KEY"] = badge.pressed() or game.gamepad.pressed()


def init_platforms():
    game.platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


player = player_base(20, 0)
badge.pad_map({})
game.gamepad = badge.pad[0]
init_platforms()

while True:
    badge.clear()
    badge.poll()
    parse_controls()

    player.update()
    for platform in game.platforms:
        platform.draw()

    display.update()

```

![Run your code!](/tut4_res/tufty.gif)

### Running

Running is easy, we just add a bit of acceleration to the player in the appropriate direction. Again, just like jumping, we only want to be able to run if we're standing on a platform, so we can add this in right after our jump, within that same `else` statement:

```python-raw
            if game.controls["MOVE_RIGHT"]:
                self.vx += 1.5

            if game.controls["MOVE_LEFT"]:
                self.vx -= 1.5
```

![Run your code!](/tut4_res/tufty.gif)

Test that now and you'll find two things - first, you just accelerate and don't stop, and second, you disappear off the edge of the screen. We can remedy the second one easy enough. Right after changing the player's position and before drawing them, we can clamp your position using the following line:

```python-raw
        self.x = clamp(self.x, 0, screen.width - self.w)
```

![Run your code!](/tut4_res/tufty.gif)

Now you'll see you'll at least not fly off the screen, but that speed is still wild. You're a squirrel, not a rocket. We want it to be pretty nippy, part of the gameplay is that you're controlling something very fast moving, but we clearly need some kind of damping. That's easy enough to implement - right after our movement controls, within that same `else` statement, let's say:

```python-raw
            if self.vx > 0:
                self.vx -= 0.5
            elif self.vx < 0:
                self.vx += 0.5
```

![Run your code!](/tut4_res/tufty.gif)

So now your speed is reduced by 0.5 every frame you're touching the ground. Tufty still clearly has the zoomies and we'll address the speed issue soon, but you can see that there is now a deceleration after a light tap on the buttons.

### Dropping

Let's also look at dropping through the platforms. This is easy, as we've already established a control for drop, and all we want to happen when it's activated is for the player to start falling under gravity. We have that condition anyway - it applies whenever the player is airborne - so we just need to add to that check to tell it to also fall if we've hit 'Drop':

```python-raw
        if self.airborne or game.controls["DROP"]:
```

### Jumping sideways

And finally, we can already jump sideways if we've got a running start, but given how much we're bouncing between platforms it might be good to actually have a sideways jump. For this, let's create new controls in `parse_controls()`:

```python-raw
    game.controls["MOVE_LEFT"] = badge.held(BUTTON_A) or game.gamepad.held(PAD_LEFT)
    game.controls["MOVE_RIGHT"] = badge.held(BUTTON_C) or game.gamepad.held(PAD_RIGHT)
    game.controls["DROP"] = (badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_B)) or game.gamepad.pressed(PAD_DOWN)
    game.controls["JUMP"] = badge.pressed(BUTTON_B) or game.gamepad.pressed(PAD_A) or game.gamepad.pressed(PAD_B) or game.gamepad.pressed(PAD_X) or game.gamepad.pressed(PAD_Y)
    game.controls["JUMP_LEFT"] = game.controls["MOVE_LEFT"] and game.controls["JUMP"]
    game.controls["JUMP_RIGHT"] = game.controls["MOVE_RIGHT"] and game.controls["JUMP"]
    game.controls["ANY_KEY"] = badge.pressed() or game.gamepad.pressed()
```

We're treating this a bit differently, looking for other commands further up the list instead of specific button inputs. We can just add lines in to refer to these too, after the jump command and before the movement:

```python-raw
            if game.controls["JUMP"]:
                self.vy = -10

            if game.controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif game.controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif game.controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif game.controls["MOVE_LEFT"]:
                self.vx -= 1.5
```

You'll see we've altered the existing commands to include a couple of `elif`s there. If Jump has been pressed, we always want to get that upward acceleration whether we're pressing left, right or nothing, so it just uses `if`. But the rest of the controls we want to each do a specific thing, so they're in their order of priority and made exclusive using `elif` statements.

For the `JUMP_LEFT` and `JUMP_RIGHT` commands, we've already got the vertical movement from `JUMP`, so we can just concentrate on giving Tufty a horizontal boost. If you're jumping sideways, your speed will be set to 3 unless it's already more than 3. That way, if you are taking a running jump, you won't suddenly slow down when you jump.

### Final player movement bits

And that's it! That's pretty much everything for player movement. There's one more thing, and while it won't come up until a bit later we can set the groundwork for it now. When you die, we want you to pass through all of the platforms and not land on them. So, we can just add `self.dead = False` to our `__init__()` method, and then check for it in `update()` when checking for whether we fall:

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
        if self.airborne or self.dead or game.controls["DROP"]:
```

For the moment, `dead` will just stay permanently on `False`, but watch out for it, it'll show up again. You'll notice that because all of the controls are in the `else` after the `if`, that being dead will also automatically disable all of your control inputs. Here's the code you should have if you've been following along:

```python
import random


class game:
    platforms = []
    acorns = []
    controls = {}
    gamepad = None


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
        for platform in game.platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or game.controls["DROP"]:
            self.vy += 1
        else:
            if game.controls["JUMP"]:
                self.vy = -10

            if game.controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif game.controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif game.controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif game.controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0:
                self.vx -= 0.5
            elif self.vx < 0:
                self.vx += 0.5

        for platform in game.platforms:
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


def parse_controls():
    game.controls["MOVE_LEFT"] = badge.held(BUTTON_A) or game.gamepad.held(PAD_LEFT)
    game.controls["MOVE_RIGHT"] = badge.held(BUTTON_C) or game.gamepad.held(PAD_RIGHT)
    game.controls["DROP"] = (badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_B)) or game.gamepad.pressed(PAD_DOWN)
    game.controls["JUMP"] = badge.pressed(BUTTON_B) or game.gamepad.pressed(PAD_A) or game.gamepad.pressed(PAD_B) or game.gamepad.pressed(PAD_X) or game.gamepad.pressed(PAD_Y)
    game.controls["JUMP_LEFT"] = game.controls["MOVE_LEFT"] and game.controls["JUMP"]
    game.controls["JUMP_RIGHT"] = game.controls["MOVE_RIGHT"] and game.controls["JUMP"]
    game.controls["ANY_KEY"] = badge.pressed() or game.gamepad.pressed()


def init_platforms():
    game.platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


player = player_base(20, 0)
badge.pad_map({})
game.gamepad = badge.pad[0]
init_platforms()

while True:
    badge.clear()
    badge.poll()
    parse_controls()

    player.update()
    for platform in game.platforms:
        platform.draw()

    display.update()

```

![Run your code!](/tut4_res/tufty.gif)

We're not quite done with the `player_base` class overall, but we're at least done for now. Now, we'll work on getting some scrolling platforms.

## Making the platforms move

So you can move, but what about your environment? This infinite runner doesn't feel very infinite right now. We presumably need an infinite number of platforms to scroll past for Tufty to jump on, right? Well, not quite, because we're going to cheat. We could keep spawning new platforms off the right hand side of the screen, but we'd need to destroy them again once they had passed, otherwise they'd just take up more and more memory and processing power the longer you played.

Creating and destroying objects is comparatively computationally expensive, so we're going to take an eco-friendly approach and just recycle the platforms we have. So we'll just stick to the three platforms we've already made, and as soon as each one disappears off the left side of the screen, we'll move it back to the right side. We'll also reset its length to a new random length.

Because the platforms are random lengths, it means that they'll respawn at different times and be in different positions relative to each other every time. We can chaos it up a little further by making them respawn at a random height on the screen.

First though, we need to make them scroll in the first place. Just like `player_base` for the player's behaviour, all of the platforms' behaviour is going to be taken care of within `platform_base`. First, let's make an `update()` method inside `platform_base` and use that to call `draw()`:

```python-raw
    def update(self):
        self.draw()
```

Don't forget to change the call in the main `while` loop to `platform.update()` instead of `platform.draw()`.

Scrolling is pretty easy. Let's create a `foreground_scroll_speed` variable within `game` with a value of 4, so that if we need to change it we only have to change it in one place. Then, we just need to subtract this value from the platform's x co-ordinate every frame, and voila! Scrolling platforms. It should look like this:

```python-raw
    def update(self):
        self.x -= game.foreground_scroll_speed
        self.draw()
```

And now you should see that all the platforms scroll off the screen and the player drops down into the endless void. Probably a good metaphor for something, but not great for gameplay - still, it's something. Now we just need to get them to reappear on the other side.

To do this, we can easily just check to see if the right hand side of the platform is at less than zero in x, and if it is, let's set the platform's x coordinate to the screen width:

```python-raw
    def update(self):
        self.x -= game.foreground_scroll_speed

        if self.r <= 0:
            self.x = screen.width

        self.draw()
```

![Run your code!](/tut4_res/tufty.gif)

And all of a sudden, there's gameplay! It's very fast-paced and pretty difficult, but it is technically playable.

## Getting a consistent framerate

Not playable enough, though. At the moment the Tufty is putting out frames as fast as it can draw them, and since everything moves the same amount every frame that means it's going too fast. Not only that, but loops where the processor needs to do more work will take longer than ones where it has to do less, so that frame rate isn't necessarily consistent. We need a framerate limiter.

> Note: Acorn Highway is pretty light on the processor, which is why it goes so fast. That means the variation in frame time likely won't be visible to the naked eye in this case, but it's there. It becomes a lot more apparent when you're taxing the hardware a bit more or when there's a bigger variation on how much work needs doing in different frames.

The first step in limiting the frame rate is finding out how long the frame took to process. We can do this using MicroPython's built in `time` module. Badgeware has a very similar thing in its own API, but it's tied into `update()`, which we're not using.

First, let's add `import time` to our imports at the top of the file. We'll also add another variable into `game`, which we'll call `last_frame`. We'll set it at zero right now. Your `game` class should look like this by now:

```python-raw
class game:
    platforms = []
    acorns = []
    controls = {}
    gamepad = None
    foreground_scroll_speed = 4
    last_frame = 0
```

Every time we go round the loop, we're going to check `time.ticks_ms()`, which will tell us how many milliseconds it's been since the badge was powered on. We can easily calculate how many milliseconds we want each frame to take, dividing 1000 by our desired framerate. We want Acorn Highway running at 30fps, so that's about 33ms per frame.

Basically each time round the loop we'll check if it's been 33ms or more since the last frame we calculated. If it has, great, we can calculate the next one. If not, we just keep running round the loop until enough time has passed.

It's just a few lines of code to do the above, and it's all in the main `while` loop:

```python-raw
while True:
    ticks = time.ticks_ms()
    frametime = ticks - game.last_frame

    if frametime >= 33:
        badge.clear()
        badge.poll()
        parse_controls()

        player.update()
        for platform in game.platforms:
            platform.update()

        display.update()

        game.last_frame = ticks
```

![Run your code!](/tut4_res/tufty.gif)

The first two lines work out how many milliseconds it's been since `game.last_frame`. Then everything that was in the loop before is now behind the new `if` statement, checking if it's been more than 33ms. Finally, we've added a very important line at the end, to set `game.last_frame` to the new ticks value for the next frame. Note that it's inside the `if` statement, as we only want that to happen on those times through the loop where we calculate a new frame.

## Renewing platforms

Right now, the platforms are staying at their original size and their original height - that's not getting changed when they respawn. Let's cleanly make that happen by making a `reset()` method in `platform_base` which takes care of all of those things, and then just calling that.

```python-raw
    def update(self):
        self.x -= game.foreground_scroll_speed

        if self.r <= 0:
            self.reset()

        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)
```

![Run your code!](/tut4_res/tufty.gif)

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
        for platform in game.platforms:
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
        self.x -= game.foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()

        self.draw()
```

![Run your code!](/tut4_res/tufty.gif)

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

![Run your code!](/tut4_res/tufty.gif)

And now we've got nicely spawning, nicely spaced platforms.

> Note: It's possible to get the game to lock up completely here. If you decide you want more than three platforms at once, or if the keepout value is too high, then it's possible to get a situation where there isn't a big enough gap for a new platform to spawn into. If this happens, then the game will completely freeze while it goes round in an endless loop trying to find a gap and never finding one. Which makes Tufty sad.

Here's your code so far:

```python
import random
import time


class game:
    platforms = []
    acorns = []
    controls = {}
    foreground_scroll_speed = 4
    last_frame = 0


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
        for platform in game.platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or game.controls["DROP"]:
            self.vy += 1
        else:
            if game.controls["JUMP"]:
                self.vy = -10

            if game.controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif game.controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif game.controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif game.controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0:
                self.vx -= 0.5
            elif self.vx < 0:
                self.vx += 0.5

        for platform in game.platforms:
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
        self.x -= game.foreground_scroll_speed

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
        for platform in game.platforms:
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


def parse_controls():
    game.controls["MOVE_LEFT"] = badge.held(BUTTON_A) or game.gamepad.held(PAD_LEFT)
    game.controls["MOVE_RIGHT"] = badge.held(BUTTON_C) or game.gamepad.held(PAD_RIGHT)
    game.controls["DROP"] = (badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_B)) or game.gamepad.pressed(PAD_DOWN)
    game.controls["JUMP"] = badge.pressed(BUTTON_B) or game.gamepad.pressed(PAD_A) or game.gamepad.pressed(PAD_B) or game.gamepad.pressed(PAD_X) or game.gamepad.pressed(PAD_Y)
    game.controls["JUMP_LEFT"] = game.controls["MOVE_LEFT"] and game.controls["JUMP"]
    game.controls["JUMP_RIGHT"] = game.controls["MOVE_RIGHT"] and game.controls["JUMP"]
    game.controls["ANY_KEY"] = badge.pressed() or game.gamepad.pressed()


def init_platforms():
    game.platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


player = player_base(20, 0)
badge.pad_map({})
game.gamepad = badge.pad[0]
init_platforms()

while True:
    ticks = time.ticks_ms()
    frametime = ticks - game.last_frame

    if frametime >= 33:
        badge.clear()
        badge.poll()
        parse_controls()

        player.update()
        for platform in game.platforms:
            platform.update()

        display.update()

        game.last_frame = ticks

```

Looking good. But what we've got right now is a gameplay snippet, nothing more. Let's turn it into something with a start and a finish.

## Game states

To start off with, we're going to introduce three basic states - the title screen, gameplay, and the game over screen. The loop will be that the game starts at the title screen, switches to the gameplay screen when any button is pressed, switches to the game over screen when you die, then switches back to the title screen when you press any button on the game over screen.

First, let's do some setup. We'll make a little mini class to define our game states. At the very top of the file, right below the imports and and before `game`, we're going to add the following class:

```python-raw
class game_state:
    TITLE = 0
    GAMEPLAY = 1
    GAME_OVER = 3
```

That's it, that's the whole class. Don't worry about the numbers going "0, 1, 3" - that certainly isn't foreshadowing about a secret extra state we're going to add later or anything, nooo, not at all.

You can see that these are static variables, just like the ones in `game` - we're not making an instance of this class anywhere and in fact we'll never change these, it's just going to sit there as a shorthand to make the code readable. We could just have a variable in `game` called `game_state` and set it to different numbers to indicate different states, but this way stops us having to remember "Was it 1 that was gameplay, or was that 2?". Plus, having a name in the code means that anyone else looking at it will immediately understand what's going on in a way that they wouldn't with just a number.

Now, we are going to make that variable in `game` that keeps track of which state we're in, but we can now use a name instead of a number. We'll put it just after setting up our other variables:

```python-raw
class game:
    platforms = []
    acorns = []
    controls = {}
    gamepad = None
    foreground_scroll_speed = 4
    last_frame = 0
    current_game_state = game_state.TITLE
```

Now, we're going to put a series of checks into the main `while` loop which lets it choose what it wants to do based on what `current_game_state` is set to. We'll leave `parse_controls()` where it is, since you're going to need to read button inputs whatever state you're in. Let's rewrite the loop so it looks like this:

```python-raw
while True:
    ticks = time.ticks_ms()
    frametime = ticks - game.last_frame

    if frametime >= 33:
        badge.clear()
        badge.poll()
        parse_controls()

        if game.current_game_state == game_state.TITLE:
            title_loop()
        elif game.current_game_state == game_state.GAMEPLAY:
            gameplay_loop()
        elif game.current_game_state == game_state.GAME_OVER:
            game_over_loop()

        display.update()

        game.last_frame = ticks
```

It's a very simple loop, since all the fancy stuff is happening in those functions with `_loop` in the names. Of course, right now this would just throw up an error as we haven't written any of those functions yet, so let's write them. We'll put them directly after `init_platforms()` and keep them simple to start with - you can see that `gameplay_loop()` just contains the lines we removed from the main loop, and the other two just draw a line of text:

```python-raw
def title_loop():
    screen.text("Title screen", 0, 0)


def gameplay_loop():
    player.update()

    for platform in game.platforms:
        platform.update()


def game_over_loop():
    screen.text("Game Over screen", 0, 0)
```

![Run your code!](/tut4_res/tufty.gif)

Well, this seems like a step backwards. Try running it now, and you'll just get a black screen with "Title screen" written on it that you can't get out of. And of course that's because we started with the state set to `TITLE` and we've got nothing in place to change it. You can see the stuff that used to be in the `while` loop right there in `gameplay_loop()`, we just can't get to it yet. That's easily fixed, we just check for a button press each frame and when it's pressed, we move it onto the next one:

```python-raw
def title_loop():
    screen.text("Title screen", 0, 0)

    if game.controls["ANY_KEY"]:
        game.current_game_state = game_state.GAMEPLAY


def gameplay_loop():
    player.update()

    for platform in game.platforms:
        platform.update()


def game_over_loop():
    screen.text("Game Over screen", 0, 0)

    if game.controls["ANY_KEY"]:
        game.current_game_state = game_state.TITLE
```

![Run your code!](/tut4_res/tufty.gif)

## Losing the game

That gets us into gameplay, but now we can't get out of it - there's no lose condition yet. Well, we know when we want game over to happen - when the player falls off the screen. So we could simply do a check for the player hitting the bottom edge of the screen instead of a button press. Simple!

```python-raw
def title_loop():
    screen.text("Title screen", 0, 0)

    if game.controls["ANY_KEY"]:
        game.current_game_state = game_state.GAMEPLAY


def gameplay_loop():
    player.update()

    for platform in game.platforms:
        platform.update()

    if player.b >= screen.height:
        game.current_game_state = game_state.GAME_OVER


def game_over_loop():
    screen.text("Game Over screen", 0, 0)

    if game.controls["ANY_KEY"]:
        game.current_game_state = game_state.TITLE
```

![Run your code!](/tut4_res/tufty.gif)

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

Then we call that so that the player is reset when we start a new game. You might think this happens in the title screen function, but if it did then it would be carried out every frame - not a problem for resetting the player's position, but for other things later on it would cause issues. So, anything we want to happen just once when you first enter a game state goes in the same block of code that switches to that game state.

In this case that means we reset the player at the end of the game over screen, when we're switching the game state back to the title screen:

```python-raw
def game_over_loop():
    screen.text("Game Over screen", 0, 0)

    if controls["ANY_KEY"]:
        player.reset()
        game.current_game_state = game_state.TITLE
```

That'll just reset the player back to the starting position and zero out their speed. You might notice we've still not used that `dead` property of the player, but that'll come in later still. The suspense must be killing you. And now we've got a full gameplay loop.

![Run your code!](/tut4_res/tufty.gif)

It's still not quite right though. Do you notice that after you finish your first playthrough, after that you sometimes just fall and die instantly because there's no platform beneath you? That's as a result of the same thing - the platforms aren't resetting, they're exactly where you left them. Easily fixed though - we'll call `init_platforms()` that we made ages ago to reset their positions, and we'll do it right after we reset the player:

```python-raw
    if game.controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        game.current_game_state = game_state.TITLE
```

## Scoring

What's next, then? How about a score? Say, one point for every platform you pass? Sounds good. Let's add in a variable, once again in `game`, named `score`. It can go right after we initially set the game state, and of course it wants to start off set to zero. We can easily increase the score by adding `game.score += 1` to `platform_base`'s `update()` method just after the `while` loop to find a new position for the platform:

```python-raw
def update(self):
    self.x -= game.foreground_scroll_speed

    if self.r <= 0:
        self.reset()
        while self.check_collisions():
            self.reset()
        game.score += 1

    self.draw()
```

That way, the score goes up by one every time a platform passes off the left side of the screen. We should probably display the score, too. Now, we'll just do a line of text for now, but we're going to be displaying the score in a fancier way later on so it makes sense to set up a separate function for it ahead of time. We'll make a function just before `init_gamepad()` (or `parse_controls()` if you didn't set up the gamepad), as follows:

```python-raw
def draw_score():
    screen.text(str(game.score), 0, 0)
```

Then we can call it after we've drawn everything else:

```python-raw
def gameplay_loop():
    player.update()

    for platform in game.platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        game.current_game_state = game_state.GAME_OVER
```

The final thing is to reset the score when you go back to the title screen. That'll happen at the end of the game over screen, at the same time as we're resetting the player and platforms:

```python-raw
def game_over_loop():
    screen.text("Game Over screen", 0, 0)

    if game.controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        game.score = 0
        game.current_game_state = game_state.TITLE
```

By this point you should be working with something a lot like this:

```python
import random
import time


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    GAME_OVER = 3


class game:
    platforms = []
    acorns = []
    controls = {}
    gamepad = None
    foreground_scroll_speed = 4
    last_frame = 0
    current_game_state = game_state.TITLE
    score = 0


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
        for platform in game.platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or game.controls["DROP"]:
            self.vy += 1
        else:
            if game.controls["JUMP"]:
                self.vy = -10

            if game.controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif game.controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif game.controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif game.controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0:
                self.vx -= 0.5
            elif self.vx < 0:
                self.vx += 0.5

        for platform in game.platforms:
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
        self.x -= game.foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            game.score += 1

        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        for platform in game.platforms:
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
    screen.text(str(game.score), 0, 0)


def parse_controls():
    game.controls["MOVE_LEFT"] = badge.held(BUTTON_A) or game.gamepad.held(PAD_LEFT)
    game.controls["MOVE_RIGHT"] = badge.held(BUTTON_C) or game.gamepad.held(PAD_RIGHT)
    game.controls["DROP"] = (badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_B)) or game.gamepad.pressed(PAD_DOWN)
    game.controls["JUMP"] = badge.pressed(BUTTON_B) or game.gamepad.pressed(PAD_A) or game.gamepad.pressed(PAD_B) or game.gamepad.pressed(PAD_X) or game.gamepad.pressed(PAD_Y)
    game.controls["JUMP_LEFT"] = game.controls["MOVE_LEFT"] and game.controls["JUMP"]
    game.controls["JUMP_RIGHT"] = game.controls["MOVE_RIGHT"] and game.controls["JUMP"]
    game.controls["ANY_KEY"] = badge.pressed() or game.gamepad.pressed()


def init_platforms():
    game.platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


def title_loop():
    screen.text("Title screen", 0, 0)

    if game.controls["ANY_KEY"]:
        game.current_game_state = game_state.GAMEPLAY


def gameplay_loop():
    player.update()

    for platform in game.platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        game.current_game_state = game_state.GAME_OVER


def game_over_loop():
    screen.text("Game Over screen", 0, 0)

    if game.controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        game.score = 0
        game.current_game_state = game_state.TITLE


player = player_base(20, 0)
badge.pad_map({})
game.gamepad = badge.pad[0]
init_platforms()

while True:
    ticks = time.ticks_ms()
    frametime = ticks - game.last_frame

    if frametime >= 33:
        badge.clear()
        badge.poll()
        parse_controls()

        if game.current_game_state == game_state.TITLE:
            title_loop()
        elif game.current_game_state == game_state.GAMEPLAY:
            gameplay_loop()
        elif game.current_game_state == game_state.GAME_OVER:
            game_over_loop()

        display.update()

        game.last_frame = ticks

```

![Run your code!](/tut4_res/tufty.gif)

## Losing, but properly

We'll get into the fancy graphics soon. But first, does that dying seem abrupt to you? Hit the bottom of the screen and then boom, straight to game over? In fact, if you're mashing the buttons it's easy to accidentally hit it an extra time and skip the game over and even the title screen.

Well, we can remedy that with a.... secret fourth game state nobody knew about! Who could have seen that coming?

This is going to be a little death animation similar to those you see in classic Sonic or Mario games, where the player bounces up from the bottom of the screen, then falls back down and disappears. Once we've got our full graphics, we can use a different sprite animation to show the owies.

First of all, let's create that missing game state, by adding in `DEATH_ANIM = 2` in the appropriate place in our `game_state` class. Then, we'll  create a `death_anim_loop()` function in between `gameplay_loop()` and `game_over_loop()`. What's going in this function, though? Well, for now, it's just going to almost be a copy of `gameplay_loop()`:

```python-raw
def death_anim_loop():
    player.update()

    for platform in game.platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        game.current_game_state = game_state.GAME_OVER
```

Can you spot the difference? In this state, we're calling `platform.draw()` instead of `platform.update()`. That means the platforms will still get drawn, but they won't move, reset or anything else. The scrolling stops when you die.

Now, let's hook this into everything else. Since it's now `death_anim_loop()` that changes the game state to `GAME_OVER`, we want to alter `gameplay_loop()` to point to the `DEATH_ANIM` state instead. And finally, we need to add an extra `elif` statement into the main loop, so that it's at the right point in the sequence:

```python-raw
        elif game.current_game_state == game_state.DEATH_ANIM:
            death_anim_loop()
```

But surely none of that will matter, because this screen will only be up for a single frame, right? Nothing has reset the player's position, so it'll display, detect that the player is at the bottom of the screen and then move on to the game over screen, surely?

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

This will mean that when the player updates, they'll fall with gravity and all of the controls will be locked out.  We need to do one more thing with that here, though. In the player's `update()` method, we need to put that check for landing on a platform behind a test of `dead` so that they'll just fall through platforms and not land on them:

```python-raw
        if not self.dead:
            for platform in game.platforms:
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

We also need to call `player.death()` when we switch from `GAMEPLAY` to `DEATH_ANIM`, just like we reset the player when going from `GAMEOVER` to `TITLE`:

```python-raw
def gameplay_loop():
    player.update()

    for platform in game.platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        game.current_game_state = game_state.DEATH_ANIM
```

Now you might be able to see what's going to happen. When you hit the bottom of the screen the first time, it goes into the `DEATH_ANIM` mode. This stops the platforms from scrolling, moves the player up a tiny bit so they won't immediately trigger the game over screen, and gives them a boost upward while disabling controls and collisions with platforms. Since they're still being affected by gravity, they're going to bounce up, fall down and then trigger the game over screen when they hit the bottom of the screen again.

![Run your code!](/tut4_res/tufty.gif)

And by jingo, it works. Here's the full code so far:

```python
import random
import time


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAME_OVER = 3


class game:
    platforms = []
    acorns = []
    controls = {}
    foreground_scroll_speed = 4
    last_frame = 0
    current_game_state = game_state.TITLE
    score = 0


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
        for platform in game.platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or game.controls["DROP"]:
            self.vy += 1
        else:
            if game.controls["JUMP"]:
                self.vy = -10

            if game.controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif game.controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif game.controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif game.controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0:
                self.vx -= 0.5
            elif self.vx < 0:
                self.vx += 0.5

        if not self.dead:
            for platform in game.platforms:
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
        self.x -= game.foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            game.score += 1

        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        for platform in game.platforms:
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
    screen.text(str(game.score), 0, 0)


def parse_controls():
    game.controls["MOVE_LEFT"] = badge.held(BUTTON_A) or game.gamepad.held(PAD_LEFT)
    game.controls["MOVE_RIGHT"] = badge.held(BUTTON_C) or game.gamepad.held(PAD_RIGHT)
    game.controls["DROP"] = (badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_B)) or game.gamepad.pressed(PAD_DOWN)
    game.controls["JUMP"] = badge.pressed(BUTTON_B) or game.gamepad.pressed(PAD_A) or game.gamepad.pressed(PAD_B) or game.gamepad.pressed(PAD_X) or game.gamepad.pressed(PAD_Y)
    game.controls["JUMP_LEFT"] = game.controls["MOVE_LEFT"] and game.controls["JUMP"]
    game.controls["JUMP_RIGHT"] = game.controls["MOVE_RIGHT"] and game.controls["JUMP"]
    game.controls["ANY_KEY"] = badge.pressed() or game.gamepad.pressed()


def init_platforms():
    game.platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


def title_loop():
    screen.text("Title screen", 0, 0)

    if game.controls["ANY_KEY"]:
        game.current_game_state = game_state.GAMEPLAY


def gameplay_loop():
    player.update()

    for platform in game.platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        game.current_game_state = game_state.DEATH_ANIM


def death_anim_loop():
    player.update()

    for platform in game.platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        game.current_game_state = game_state.GAME_OVER


def game_over_loop():
    screen.text("Game Over screen", 0, 0)

    if game.controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        game.score = 0
        game.current_game_state = game_state.TITLE


player = player_base(20, 0)
badge.pad_map({})
game.gamepad = badge.pad[0]
init_platforms()

while True:
    ticks = time.ticks_ms()
    frametime = ticks - game.last_frame

    if frametime >= 33:
        badge.clear()
        badge.poll()
        parse_controls()

        if game.current_game_state == game_state.TITLE:
            title_loop()
        elif game.current_game_state == game_state.GAMEPLAY:
            gameplay_loop()
        elif game.current_game_state == game_state.DEATH_ANIM:
            death_anim_loop()
        elif game.current_game_state == game_state.GAME_OVER:
            game_over_loop()

        display.update()

        game.last_frame = ticks

```

Now, it's not especially attractive. But that's what the other part of the tutorial is for. We're going to take this functional starting point and give it that beautiful Triple-A Badgeware sheen, as well as adding acorns for Tufty to collect, and a couple of other bells and whistles too.