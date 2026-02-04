---
title: Tutorial 1: A Simple Badge
summary: An absolute beginner's guide to coding an app for Badgeware.
icon: build
publish: true
---
# Tutorial 1: A Simple Badge

In this tutorial, we're going to demonstrate how to do the basic setup of graphics on the screen by making a badge similar to the one preloaded onto the badges already. It'll show a name and picture, and a current mood which you can change using the buttons. It doesn't require any familiarity with Badgeware or with MicroPython, but does assume you know how to navigate around your computer, copy and rename files and so forth.

> Note: Although this tutorial shows examples for Tufty, you can make it work very easily for Badger and even for Blinky, although we have to drop the image to get enough space to work with on Blinky. Any differences between the platforms will be called out in notes like this.

# Setting Up

First, let's set up your virtual coding space. You can code straight onto the badge, or you can do your work in a folder on your own computer and then copy it across onto the badge. This tutorial will asume you're coding straight onto the badge, but it goes just the same if you're working locally - you'll just need to copy the files across to the badge to see it working.

Plug your badge in, and go into Disk Mode by either going to the menu option on the home screen or by double-tapping the `RESET` button. Now, find it in your file manager. It should come up as BADGER, TUFTY or BLINKY. Open it and navigate into the `/apps/` folder.

You should see the folders for each app. Create a new one and call it `my_badge`. Once it's created, open it up. You'll need three things in here - an `assets` folder, a menu icon and `__init__.py`, which is the file that will contain your code.

Let's create that `assets` folder inside your app folder, and then check out the icon. This has to be named `icon.png`, and should be a 24 x 24 pixel PNG file. It can have transparency if you want. You can either find or create a suitable icon yourself, or alternatively you could make a copy of `icon.png` from one of the other apps on the badge.

Finally it's time to get coding and create `__init__.py`. First, make a text file in your app folder and rename it to `__init__.py`. Then you can open it in whatever software you want to use to edit. Any text editor will do, although dedicated code editors like Thonny or Visual Studio Code as well as advanced text editors like Sublime Text or Notepad++ have the benefit of highlighting different parts of your code in different colours to make it easier to see what everything is. The main thing that's not recommended is a full fledged word processor like Microsoft Word or OpenOffice. These are geared toward layout on a page rather than pure text, so as well as being harder to read they'll often put extra features and characters into your code that might have adverse effects.

Anyway, open `__init__.py` in your editor of choice (this tutorial was written in VS Code), and you can begin...

# Writing your first lines of code

In the most basic fashion, MicroPython just reads your code from the start of the file down to the end, and executes it as it goes. But there's lots of exceptions to this, and we'll go through each concept as it's introduced.

## Imports

You're not on your own in this blank MicroPython file. Often in Python and related languages, you'll need to import modules from elsewhere. This might be something that's installed as part of MicroPython, it might be part of the platform you're working on or it might be code you wrote that you've separated out into another file for convenience. These are generally imported at the very start of the file, using `import`.

On Badgeware, if you're creating an app to be run from the menu as we are doing here, all of Badgeware's features, like drawing functions and so on, are already imported, so there's no need to do anything here. But bear it in mind, because it'll come up in later tutorials.

## Variables

A variable is, put very simply, a thing. A piece of information that you've given a name to. This can be text, a number, or other much more complicated structures outside the scope of this tutorial. One you've set up a variable, you can refer to it by name and the code will use whatever value is currently assigned to it. So, for example:

```python-raw
x = 3
print(x)     # prints "3" in the console

x = 5        # x has been changed to 5
print(x)     # prints "5" in the console

x = x + 3    # x has had 3 added to it
print(x)     # prints "8" in the console

print(x / 2) # prints "4" in the console
# at this point, x is still 8 - for the last command we didn't ask it to change the value of x itself, just print what x divided by two was.

```

Variables come in different types, such as integers, text, floating point numbers and so on. MicroPython mostly keeps track of this behind the scenes, but it does become something you need to be aware of once you get past beginner programming. For now though, it's out of the scope of this tutorial.

## Methods

A key part of MicroPython is the method. This is a block of code that you define - when MicroPython reads it, it won't execute it right away but it'll keep it in memory and execute it when you call on it somewhere in the program. Depending on how you've defined it, you can give the method some material to work on (known as parameters), and it may or may not return a result when it's finished.

### Defining a method

First, we can define a method by typing `def`, followed by the name of the method and then a pair of parentheses. These parentheses can either be empty, or they can contain any parameters you might want to pass to the method. So the following would just print "Hello World!" to the console when called:

```python-raw
def say_hello():
  print("Hello World!")

```

You'll notice that the line ends with a colon, and the next line is indented. That's how we tell MicroPython that the "print" line is inside the method definition - other languages use brackets of different kinds, but in Python and its derivatives, it's different levels of indentation.

### Calling a method

Now we've defined a method, we can call it very simply by typing its name with the parentheses, passing in any parameters the method takes. We saw this in both the examples above, with print(). Print doesn't send any values back when it's done, but it does take one parameter, and it writes that parameter to the console. Most of the time when working on Badgeware you can't see the console, but we're just telling you what it says in these examples until we get to writing things to the screen. So let's define a method that takes any number and doubles it, passing that result back to the place in the code it was called from.

```python-raw
# First we define our method, including the parameter
def double_any_number(original_number):
  # We take the number given to us as a parameter and multiply by two...
  new_number = original_number * 2
  # Then we throw that result back to where the method was called from.
  return new_number

# Now let's set a variable for our starting number. Note that it doesn't have to have the same name as the parameter you set up in the method.
starting_number = 10

# And now we'll call the method, passing it our starting number as its parameter. When it throws the result back here, we can catch it by saying that some variable or other equals the result of the method, like so:
doubled_number = double_any_number(starting_number)

# Now starting_number equals 10 and doubled_number equals 20.
```

Note that you could put starting_number before the equals sign when calling the method, and still used starting_number as the parameter. That way you'd be updating the existing variable with the result rather than creating a new one.

# The update() method

Now you're familiar with methods, let's look at one that's built in in Badgeware - the `update()` method. This is actually required in apps that run through the menu, and it forms what's called the main program loop.

When Badgeware starts an app, it looks for a method called `update()` in that app's `__init__.py`, and then runs it over and over again in a loop until you return to the menu or power off the device. Anything you put in `update()` runs once every frame - Tufty and Blinky aim for 60 frames per second, and Badger updates with a new frame every time a button is pressed or on a timer from the internal clock.

`update()` always finishes by updating the screen, so anything you want to put on the screen this frame should be included inside this method. Let's finally start coding and get something into your app.

```python
def update():
    pass
```

You can save and run this from the menu! And, how, er... exciting! A blank screen, yay!

Of course, we've not told it to actually do anything yet. the `pass` line there just meas "don't do anything" in MicroPython, because we can't leave the method with nothing inside it. Let's start drawing to the screen.

# Drawing to the screen

The full set of controls for drawing are explained in depth elsewhere on this site, but the real basic version is that they are methods which you call, passing variables in for things like position and size. Let's start simple though, by setting the pen colour, and then clearing the screen. We're using the named colours in the built-in palette here, but we'll demonstrate defining colours further down.

```python
def update():
    screen.pen = color.navy
    screen.clear()
```

And we should see that the screen is now navy blue. The screen here is actually an [image](/api/image.md) - it starts off clearing to black every frame, then during `update()` it gets altered in different ways, then finally after it gets sent to actually be displayed. With your first line of code in `update()` you're setting the screen's pen (i.e. the colour you're drawing with) to navy blue, then in the second you're calling the screen image's `clear()` method, which fills the entire image with the current pen.

> Note: If you're a Badger user, this will probably come out all dark grey or black. This might be fine now, but when we get pictures involved we'll show you a way to dither them to give more of a range of greys on Badger's screen. If you're a Blinky user, your colours will be turned into brightnesses of the LEDs.

So far so good, but let's create a border. Keeping the code we already had, let's change our pen colour and draw a rectangle in the centre of the screen. To do that we need to work out the x and y position of its top left corner, as well as its width and height. Now we could just calculate those values ourselves and enter them in as numbers, but there's a smarter way of doing it, which will allow it to work on any shape and size of screen.

> Note: Badger and Blinky users might want to tweak the border thickness and colours here to suit their unit. 

```python
# We're setting our screen border thickness as a variable right up at the top, since it's not going to change between different loops of update().
screen_border = 5

def update():
    screen.pen = color.navy
    screen.clear()

    # First we get the width and height of our rectangle by taking the screen width and height, and subtracting double our screen border.
    rect_width = screen.width - (screen_border * 2)
    rect_height = screen.height - (screen_border * 2)

    # x and y will just be our border thickness. Remember, co-ordinates 0, 0 are at the top left of the screen, with X increasing as you go left to right and Y increasing as you go top to bottom.
    rect_x = screen_border
    rect_y = screen_border

    # We'll create a rect, a type of data structure, to hold the x and y as well as its width and height. Notice how we're passing more than one variable to the rect() method separated with commas, and it's returning to us the object with the data in.
    inside_rectangle = rect(rect_x, rect_y, rect_width, rect_height)

    # Now we'll change our colour and draw the rectangle.
    screen.pen = color.smoke
    screen.rectangle(inside_rectangle)
```

> Note: We could have passed the x, y, width and height straight into screen.rectangle() there, but putting them together into a rect object makes it nice and convenient if we want to use those same dimensions and position somewhere else in the code.

# Adding a picture

Now let's add a picture to our badge. For this example we're going to decide on the size of the image in pixels, and position it centred, butting up against our top border. The image file should be called `avatar.png` stored in the assets folder inside your app folder, so make sure to copy it over there. You can use any PNG for this, but for this example it should ideally be square. It doesn't have to be the exact size that you'll be using it at in your program, but it's a little nicer quality if you do, and also a little bit faster if you're dealing with lots of images.

> Note: Badger users may want to make the picture a fair bit bigger, as their screens are are higher resolution than Tufty in its default Lores mode. Similarly Blinky users might want to skip the image entirely for reasons of space.

```python
screen_border = 5

# Here we're loading in our file from the assets folder. It won't be changing and it does take a little time and memory to load an image so we can do it here, outside the update loop.
picture = image.load("assets/avatar.png")

def update():
    screen.pen = color.navy
    screen.clear()

    rect_width = screen.width - (screen_border * 2)
    rect_height = screen.height - (screen_border * 2)

    rect_x = screen_border
    rect_y = screen_border

    inside_rectangle = rect(rect_x, rect_y, rect_width, rect_height)

    screen.pen = color.smoke
    screen.rectangle(inside_rectangle)

    # We're going to set the image as a flat 60 x 60 pixels.
    picture_size = 60
    # Then we can use that - if we want the picture to be centred on the screen, we want its top left corner to be at half of the screen's width, minus half of the picture's width.
    picture_x = (screen.width / 2) - (picture_size / 2)
    # The top corner's y coordinate is just the border width, nice and simple.
    picture_y = screen_border
    # And then just like the border rectangle, we put all of these together in a rect.
    picture_rect = rect(picture_x, picture_y, picture_size, picture_size)

    # Finally, we'll use screen.blit() to "paint" that image onto our screen, passing it the image we loaded and the rect we just made as parameters.
    screen.blit(picture, picture_rect)
```

If you run your app now, you'll see the picture displaying. If you're a Badger user, you may find it doesn't look ideal, as a full colour picture broken down to the black/grey/grey/white screen of the Badger doesn't always look good. One thing you could do is edit your picture in GIMP or Photoshop, but a quick and easy way to improve things is to run `picture.dither()` right below `picture = image.load("assets/avatar.png")`. This will alter the image using an algorithm in the same way a newspaper photograph displays shades of grey using only black ink. You can see an example [here](/api/image.md#dither).

# Adding text

Now we'll add some text. We've got over 30 fantastic pixel fonts built in on Badgeware to choose from, and they can be seen [here](/api/pixel_font.md#font-gallery). I'm going to go with smart, but you choose whatever you think looks good and fits your text well. A lot of this will be familiar from placing the image. We'll come back and tweak the positioning of everything to look great later.

> Note: Blinky users especially will have to think carefully about what font to choose and how to lay things out.

```python
screen_border = 5
picture = image.load("assets/avatar.png")

def update():
    screen.pen = color.navy
    screen.clear()

    rect_width = screen.width - (screen_border * 2)
    rect_height = screen.height - (screen_border * 2)

    rect_x = screen_border
    rect_y = screen_border

    inside_rectangle = rect(rect_x, rect_y, rect_width, rect_height)

    screen.pen = color.smoke
    screen.rectangle(inside_rectangle)

    picture_size = 60
    picture_x = (screen.width / 2) - (picture_size / 2)
    picture_y = screen_border
    picture_rect = rect(picture_x, picture_y, picture_size, picture_size)

    screen.blit(picture, picture_rect)

    # First we'll change the pen and pick our font. Note we're now creating our own very dark blue-grey colour.
    screen.pen = color.rgb(40, 50, 80)
    screen.font = rom_font.smart

    # We're setting the text as a variable, because we want to measure how big it'll be before we write it to the screen.
    name_text = "Billy J. Pirate is:"
    # measure_text always returns two values, the width and height of the text written in the current font. We don't need height right now, but we'll be using it later.
    name_width, name_height = screen.measure_text(name_text)
    # Now we've got the text width, we can work out where to put the top left corner to centre it, just like we did with the picture.
    name_x = (screen.width / 2) - (name_width / 2)
    # And the top of the text will just be at the bottom of the picture, which we can work out simply:
    name_y = screen_border + picture_size

    # Finally we just write the text on the screen, using the currently selected pen and font.
    screen.text(name_text, name_x, name_y)
```

# Interaction

The next thing to do is some more text, very much like the first. The big difference is that the actual text of what we want to write isn't defined in the update() method, it's defined outside it, where the image is loaded. I'm using ignore for the font here because it's nice and big.

```python
screen_border = 5
picture = image.load("assets/avatar.png")
# Here's our text for our mood.
mood_text = "Happy"

def update():
    screen.pen = color.navy
    screen.clear()

    rect_width = screen.width - (screen_border * 2)
    rect_height = screen.height - (screen_border * 2)

    rect_x = screen_border
    rect_y = screen_border

    inside_rectangle = rect(rect_x, rect_y, rect_width, rect_height)

    screen.pen = color.smoke
    screen.rectangle(inside_rectangle)

    picture_size = 60
    picture_x = (screen.width / 2) - (picture_size / 2)
    picture_y = screen_border
    picture_rect = rect(picture_x, picture_y, picture_size, picture_size)

    screen.blit(picture, picture_rect)

    screen.pen = color.rgb(40, 50, 80)
    screen.font = rom_font.smart

    name_text = "Jimmy J. Pirate is:"
    name_width, name_height = screen.measure_text(name_text)
    name_x = (screen.width / 2) - (name_width / 2)
    name_y = screen_border + picture_size

    screen.text(name_text, name_x, name_y)

    screen.font = rom_font.ignore

    # All of this is just the same as the last line of text, but you can see we're using the height of the first line to calculate the y coordinate of this one. We don't need the height of this line, so we can just tell MicroPython to throw it away by assigning it to _ (underscore).
    mood_width, _ = screen.measure_text(mood_text)
    mood_x = (screen.width / 2) - (mood_width / 2)
    mood_y = screen_border + picture_size + name_height

    screen.text(mood_text, mood_x, mood_y)
```

Alright, that's most of the display part of the code done. But now we want to make it interactive. It's all very well to have a badge that says you're happy, but nobody's happy all the time. What if you could change what mood it displayed with a button press?

## Lists

You can think of a list as a group of objects collected together in a particular order. In MicroPython they're represented by putting the objects, separated by commas, into a set of square brackets. You can get the data back out of the list by asking for what's at a particular position. It's easier to show that than describe it, so let's convert our mood to a list rather than a single text variable.

```python-raw
mood_text = ["Happy", "Sad", "Angry", "Hungry", "Sleepy", "Silly", "Cuddly"]
```

If you try and run that, you'll run into issues, because the code in our update loop is wanting to write mood_text to the screen and now that's a whole list of things, not just one. So let's take the lines where it comes up and change them:

```python-raw
    mood_width, _ = screen.measure_text(mood_text[0])
    mood_x = (screen.width / 2) - (mood_width / 2)
    mood_y = screen_border + picture_size + name_height

    screen.text(mood_text[0], mood_x, mood_y)
```

See how we changed mood_text to mood_text[0]? That [0] is the index of which item in mood_text we want - in this case, the first one, because numbering starts with 0 rather than 1. So if you run your program again with this change, you'll still see it says "Happy", since that's the first item in the list. Let's make that into a variable:

```python-raw
screen_border = 5
picture = image.load("assets/avatar.png")
mood_text = ["Happy", "Sad", "Angry", "Hungry", "Sleepy", "Silly", "Cuddly"]
selected_mood = 0

...

    mood_width, _ = screen.measure_text(mood_text[selected_mood])
    mood_x = (screen.width / 2) - (mood_width / 2)
    mood_y = screen_border + picture_size + name_height

    screen.text(mood_text[selected_mood], mood_x, mood_y)
```

You can see we've turned that into a variable, and used the name of the variable inside the square brackets. That way if we change the one at the top of the file, it'll change everywhere.
Try messing around with that number to display the other entries. If you use a number that's too high you'll get an error, as you'd be asking for, say, the eighth item in a list of seven items.

But we don't want to go diving around in the code to change our mood, that would change our mood to grumpy very quickly. Let's do it with a button press.

# Button input

Every refresh, just before update() is called, the Badgeware software polls the hardware and asks it what buttons are pressed, and then compares it against what was pressed last update. This gives it lists of which buttons were pressed, released or held down between the last update and the current one. You can read more about it [here](/api/io.md#reading-button-state).

Right now, we're just going to check if a button's been pressed, and if it has, we can add one to that selected_mood variable. We need to do one more thing - now we're not just reading the selected_mood variable, we're wanting to change it, so we have to tell the program that it's a global variable. This means that when we ask it to add 1 to selected_mood, it knows that that's the selected_mood we're talking about.

```python
screen_border = 5
picture = image.load("assets/avatar.png")
mood_text = ["Happy", "Sad", "Angry", "Hungry", "Sleepy", "Silly", "Cuddly"]
selected_mood = 0

def update():
    global selected_mood

    # There's a fair bit to unpack here, we'll go over it below.
    if io.BUTTON_UP in io.pressed:
        # The += here is just a quicker way of saying selected_mood = selected_mood + 1.
        selected_mood += 1

    screen.pen = color.navy
    screen.clear()

    rect_width = screen.width - (screen_border * 2)
    rect_height = screen.height - (screen_border * 2)

    rect_x = screen_border
    rect_y = screen_border

    inside_rectangle = rect(rect_x, rect_y, rect_width, rect_height)

    screen.pen = color.smoke
    screen.rectangle(inside_rectangle)

    picture_size = 60
    picture_x = (screen.width / 2) - (picture_size / 2)
    picture_y = screen_border
    picture_rect = rect(picture_x, picture_y, picture_size, picture_size)

    screen.blit(picture, picture_rect)

    screen.pen = color.rgb(40, 50, 80)
    screen.font = rom_font.smart

    name_text = "Jimmy J. Pirate is:"
    name_width, name_height = screen.measure_text(name_text)
    name_x = (screen.width / 2) - (name_width / 2)
    name_y = screen_border + picture_size

    screen.text(name_text, name_x, name_y)

    screen.font = rom_font.ignore

    mood_width, _ = screen.measure_text(mood_text[selected_mood])
    mood_x = (screen.width / 2) - (mood_width / 2)
    mood_y = screen_border + picture_size + name_height

    screen.text(mood_text[selected_mood], mood_x, mood_y)
```

So if you run the above code, you'll see it will change which mood is displayed - for a few presses, at least. Don't worry, we'll fix it. But what did we just do? Well, that involves an incredibly important part of programming:

## The if statement

That's the first thing in those lines of code, and it might be obvious to some readers. In its basic form, it goes "if condition X is true, run code A." The condition X is the part right after the `if` and is followed by a colon. The code to run if the condition is true comes below, indented by one level just like we saw with methods. Everything that's indented to that level will only be executed if the condition is true, until you get to a line which goes back to the previous level of indentation.

An `if` statement doesn't always just come by itself either. You might see an `if` statement followed by an `else` statement, with its own code indented below it. This, as you might suspect, is what to do if the condition is false. "if condition X is true, run code A. Otherwise, run code B." The `else` statement is code B.

You can also chain if statements together with `elif`, which works like it sounds - "if condition X is true, run code A. Otherwise if condition Y is true, run code B. Otherwise, run code C". We're going to use `elif` later on.

## Back to the badge

So that if statement is checking `io.BUTTON_UP in io.pressed` to see whether it should advance through the list. But what does the `io.BUTTON_UP in io.pressed` part mean?

Basically, when the Badgeware software polls the buttons, it puts its findings in several lists - `io.pressed`, `io.released`, `io.held` and `io.changed`. These lists are just like the ones you made to hold the different mood words. `io.BUTTON_UP` is just the internal name for the Up button and `in` is a useful statement to check if a list contains a specified value, so in natural language we're asking "Is the Up button in the list of buttons pressed between last update and this update?" and then doing different things depending on the answer.

But you'll find that pressing the button still makes the program crash eventually. Not to worry...

# Fixing bugs

You've possibly guessed why it's crashing out when you press the button. If you just keep adding one to the index you're asking the list for, eventually you'll get to a point where you're asking for the eighth item in a seven item list, and that makes no sense. We need to make the list loop around, and there's a couple of ways of doing that. The most obvious one is to just check whether the index is too high and reset it to zero if it is, so that it loops around to the beginning of the list:

```python-raw
    if selected_mood > 6:
        selected_mood = 0
```

If you add that in right after the button check, you'll see it fixes the problem. But it's not very elegant. What if you add new moods? You'd have to remember to change the number there, otherwise it would just keep looping through the first seven in the list. Instead we can just get the length of the list and use that, and for that we use the list's `len()` method.

```python-raw
    if selected_mood >= len(mood_text):
        selected_mood = 0
```

Note that we've also changed that greater than sign to an equal or greater than sign - the list as we've written it is seven elements long and that's what `len()` returns, but because the list index starts at zero we need to loop around after index six.

Now we've got that, let's add the same to make the Down button subtract from selected_mood, and reset it to the list length minus one whenever it goes below 0. Note that we're using `elif`, so we're only checking the down button if the up button's not pressed. That clears up any ambiguity as to what might happen if both buttons were pressed. It doesn't really matter here, but it's good to get into the habit of thinking about as it's important in more complex programs. 

```python
screen_border = 5
picture = image.load("assets/avatar.png")
mood_text = ["Happy", "Sad", "Angry", "Hungry", "Sleepy", "Silly", "Cuddly"]
selected_mood = 0

def update():
    global selected_mood

    if io.BUTTON_UP in io.pressed:
        selected_mood += 1

    elif io.BUTTON_DOWN in io.pressed:
        selected_mood -= 1

    if selected_mood >= len(mood_text):
        selected_mood = 0

    if selected_mood < 0:
        selected_mood = len(mood_text) - 1

    screen.pen = color.navy
    screen.clear()

    rect_width = screen.width - (screen_border * 2)
    rect_height = screen.height - (screen_border * 2)

    rect_x = screen_border
    rect_y = screen_border

    inside_rectangle = rect(rect_x, rect_y, rect_width, rect_height)

    screen.pen = color.smoke
    screen.rectangle(inside_rectangle)

    picture_size = 60
    picture_x = (screen.width / 2) - (picture_size / 2)
    picture_y = screen_border
    picture_rect = rect(picture_x, picture_y, picture_size, picture_size)

    screen.blit(picture, picture_rect)

    screen.pen = color.rgb(40, 50, 80)
    screen.font = rom_font.smart

    name_text = "Jimmy J. Pirate is:"
    name_width, name_height = screen.measure_text(name_text)
    name_x = (screen.width / 2) - (name_width / 2)
    name_y = screen_border + picture_size

    screen.text(name_text, name_x, name_y)

    screen.font = rom_font.ignore

    mood_width, _ = screen.measure_text(mood_text[selected_mood])
    mood_x = (screen.width / 2) - (mood_width / 2)
    mood_y = screen_border + picture_size + name_height

    screen.text(mood_text[selected_mood], mood_x, mood_y)
```

That's one way to do it, but we could take four lines of code down to one using the `%` modulo sign. This gives us the remainder when one number is divided by another, so we could replace

```python-raw
    if selected_mood >= len(mood_text):
        selected_mood = 0

    if selected_mood < 0:
        selected_mood = len(mood_text) - 1
```

with

```python-raw
    selected_mood = selected_mood % len(mood_text)
```

This covers us going in both directions - if the index goes up to 7, what's the remainder when 7 is divided by 7? Zero, of course. And if it drops to -1, what's the remainder when -1 is divided by 7? Six.

# Cleaning up

Our badge is functionally complete. Now all that remains is to just clean up a few rough edges - we've got the text and picture all displaying nicely centred, but the gaps between them are a bit uneven. So just adding or subtracting a few pixels to the Y coordinates of each item, we finally get to this:

```python
screen_border = 5
picture = image.load("assets/avatar.png")
mood_text = ["Happy", "Sad", "Angry", "Hungry", "Sleepy", "Silly", "Cuddly"]
selected_mood = 0

def update():
    global selected_mood

    if io.BUTTON_UP in io.pressed:
        selected_mood += 1
    elif io.BUTTON_DOWN in io.pressed:
        selected_mood -= 1

    selected_mood = selected_mood % len(mood_text)

    screen.pen = color.navy
    screen.clear()

    rect_width = screen.width - (screen_border * 2)
    rect_height = screen.height - (screen_border * 2)

    rect_x = screen_border
    rect_y = screen_border

    inside_rectangle = rect(rect_x, rect_y, rect_width, rect_height)

    screen.pen = color.smoke
    screen.rectangle(inside_rectangle)

    picture_size = 60
    picture_x = (screen.width / 2) - (picture_size / 2)
    picture_y = screen_border + 5
    picture_rect = rect(picture_x, picture_y, picture_size, picture_size)

    screen.blit(picture, picture_rect)

    screen.pen = color.rgb(40, 50, 80)
    screen.font = rom_font.smart

    name_text = "Jimmy J. Pirate is:"
    name_width, name_height = screen.measure_text(name_text)
    name_x = (screen.width / 2) - (name_width / 2)
    name_y = screen_border + picture_size + 7

    screen.text(name_text, name_x, name_y)

    screen.font = rom_font.ignore

    mood_width, _ = screen.measure_text(mood_text[selected_mood])
    mood_x = (screen.width / 2) - (mood_width / 2)
    mood_y = screen_border + picture_size + name_height + 2

    screen.text(mood_text[selected_mood], mood_x, mood_y)
```

# Where to go from here

This is just a simple starting point - there's lots of ways you could go from here. You could:
- Spruce up the presentation, adding background images or effects.
- Switch to using vector fonts and get more control over text size.
- Expand the scope, for example to display more than one mood.
- Add extra functionality, for example getting it to display a different image for each mood.

This is the very beginning, you can do amazing things using Badgeware devices. Check out one of our other tutorials, or get out there and play!