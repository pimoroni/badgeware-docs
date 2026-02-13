---
title: "Tutorial 2: Dashboard"
summary: "Accessing Badgeware's hardware features"
icon: build
publish: true
---
# Tutorial 2: A Dashboard
For the second tutorial, we're going to dive deep into Badgeware's vector drawing system as well as some of the different things we can access in hardware. We'll make a page that shows charts for our flash usage and our battery power, as well as showing the current time and allowing us to test the rear case lighting.

## Setting the stage
First off, you'll need to create an app folder with an `__init__.py`, an `assets` folder and an `icon.png` just as you did in the first tutorial. Now let's go into `__init__.py` and create our main `update()` function:
```python
def update():
    pass
```
And just like the first time - yay, a blank screen!

Just like in the first tutorial, you don't have to use the same colours that are mentioned here - use whatever works on your badge and to your tastes. One thing that we'll do here though is make all of our dimensions relative to the screen dimensions, rather than fixed numbers of pixels - that way, it should display the same whether you're on Tufty or Badger. Blinky is tricky, of course, because of its resolution but many of the same techniques I'm doing here will still work. You might just have to leave out some text.

## Getting some dimensions
The main part of this dashboard will be two big arc shapes which we'll use as pie charts. We'll be writing a method which lets us draw one of these, but we'll need to pass it some dimensions. Here are the dimensions we want to calculate:

- The centre line of the screen vertically, which we'll call `centre_y`.
- The centre points of each pie chart horizontally, which we'll call `left_centre_x` and `right_centre_x`.
- The size of the pie charts, which we'll call `radius_outer` and `radius_inner`.

They're easy enough to work out. Let's say we're going to divide the screen into two, and have one pie in the centre of each half. That makes these positions quite easy to calculate.

The centre line of the screen is simply half of the height of the screen, so we can say `centre_y = screen.height / 2`.

The pie centres are also easy - if they're in the centre of each half, then they're at the one-quarter and three-quarters points across the screen. So we can say `left_centre_x = screen.width * 0.25` and `right_centre_x = screen.width * 0.75`.

And for the size of the pie charts, let's go with them taking up 80% of their respective screen half. 0.8 * 0.5 = 0.4, but then we have to halve that again since we need the radius of the pie chart, not the diameter. So in the end `radius_outer = screen.width * 0.2`.

Finally, we can work out the radius of the inner part of the ring from the outer part. Let's say that it's 60% of the outer radius, so `radius_inner = radius_outer * 0.6`.

Altogether that's:
```python
# Getting all our dimensions together
centre_y = screen.height / 2
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6

def update():
    pass
```
We're still not seeing anything on the screen, but that's okay - getting these dimensions together before we start is going to make things a lot easier down the road.

From here on, we're going to also make a unit of our own, which we'll call `du` for dimension unit. That way we can just use that for future dimensions and positions. It's going to be 1% of the screen width, and we'll add that in after our existing dimensions with
```python-raw
du = screen.width / 100
```

## Drawing a circle
The first thing we're going to draw is a circle for the background of each pie chart. For this and all the following drawing we're going to be using Badgeware's vector shapes. These display beautifully with antialiasing, and can be easily rotated, scaled and translated using matrix transformations to get wonderfully smooth animation.

First, let's define our vector shapes using `shape.circle()`.
```python
screen.antialias = image.X4

# Getting all our dimensions together
centre_y = screen.height / 2
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100

def update():
    left_pie_background = shape.circle(left_centre_x, centre_y, radius_outer)
    right_pie_background = shape.circle(right_centre_x, centre_y, radius_outer)
```
You can see these two shapes have the same vertical coordinate and radius, but different horizontal coordinates. But we're still not seeing anything on the screen! That's because we've defined these shapes, but we haven't drawn them yet. Let's finally add in some drawing commands to set the background, set the pen for each shape and finally draw them.

```python
screen.antialias = image.X4

# Getting all our dimensions together
centre_y = screen.height / 2
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)

def update():
    screen.pen = light_grey
    screen.clear()

    left_pie_background = shape.circle(left_centre_x, centre_y, radius_outer)
    right_pie_background = shape.circle(right_centre_x, centre_y, radius_outer)

    screen.pen = med_grey
    screen.shape(left_pie_background)
    screen.shape(right_pie_background)
```
Finally we're seeing something. You'll notice we added a few extra bits in there - we defined some colours to use now and later on, and we set `screen.antialias` to `X4` to get the highest image quality. You can experiment with `NONE`, `X2` and `X4` to see how this reduces the jaggedness in your vector shapes.

## Getting the data
If we're wanting to display fascinating stats about our badge, then we need to ask it what those stats are. The information we need can be found in the `badge` class and the `rtc` class, and we can ask them for an update every, well, every update. Once we've got it, we can start looking at how to display it.

> Note: We're going to assume that your badge already has the correct time set on the badge's RTC - if it doesn't it'll still display, just not the right time. You can quickly update the time by connecting to the internet and running the Clock app.

```python-raw
battery_percent = badge.battery_level()
battery_voltage = badge.battery_voltage()
total_flash, used_flash, _ = badge.disk_free()
year, month, day, hour, minute, second, _ = rtc.datetime()
```
You'll notice that for some of these we've got more than one variable before the `=` sign, and some of those are just an underscore `_`. If you've not run across this before, don't worry. Some of these functions return more than one value, or return a tuple containing several values. We don't necessarily need all of the values they return, but we still have to receive them or it'll throw an error. So, for the ones we don't need we can just assign them to `_`, which discards them.

Now we've got those values though, we need to represent them on screen.

## Drawing an arc
Badgeware has a vector shape which lets you draw an arc segment with a single command. It's called very simply:
```python-raw
my_arc = shape.arc(x, y, inner, outer, from, to)
```
Let's look at the arguments that takes.
- `x, y`: Position of the centre point
- `inner`: Inner radius
- `outer`: Outer radius
- `from`: Start angle (degrees)
- `to`: End angle (degrees)

Well, we've already worked out `x`, `y`, `inner` and `outer`, but that `from` and `to` still need calculating, and we'll need to do it for both charts. We could just do the calculations twice and in this case it's probably easiest to do so, but for the sake of the tutorial let's create a method we can call to convert a percentage into two pie sections. We'll add the following into our code right before our `update()` method:
```python-raw
def make_chart():
    pass
```
What we want is to give it the information we have, and for it to calculate the last two numbers we need and use them to make two shapes that it'll return. First let's add in all the parameters we want to send it.

```python-raw
def make_chart(x, y, inner, outer, percentage):
    pass
```
Now, we can use the first four as is, but that last one, `percentage`, needs to be converted into start and stop points for the slice in degrees. We'll make the starting point zero as that's nice and easy, and luckily the maths to convert to degrees is nice and easy:
```python-raw
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
```

Easy peasy. You'll see it says `seg_1` there - that's because we're going to return two `arc` shapes - one for the filled section of the chart and one for the unfilled part. We can fill in the rest easily though, as it just starts where the last one finished and goes all the way round to 360 degrees (or in this case 359.999 degrees, as we want to get very close without touching 360):
```python-raw
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999
```

And now we've got all the information to make the shapes and return them. The new lines take the values we worked out or passed in, and feed them into an `arc()` method to generate the shapes.
```python-raw
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section
```

Now we've made that - and you'll see that it's one of those methods we just saw with more than one return value - then we can call it inside our `update()` loop. Battery level will be on the left, and flash usage on the right.
```python
badge.mode(HIRES)
screen.antialias = image.X4

# Getting all our dimensions together
centre_y = screen.height / 2
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)

# Takes in a percentage and dimensions to make two pie chart segments
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section

def update():
    battery_percent = badge.battery_level()
    battery_voltage = badge.battery_voltage()
    total_flash, used_flash, _ = badge.disk_free("/system")
    year, month, day, hour, minute, second, _ = rtc.datetime()

    screen.pen = light_grey
    screen.clear()

    left_pie_background = shape.circle(left_centre_x, centre_y, radius_outer)
    right_pie_background = shape.circle(right_centre_x, centre_y, radius_outer)

    screen.pen = med_grey
    screen.shape(left_pie_background)
    screen.shape(right_pie_background)

    left_pie_filled, left_pie_unfilled = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, battery_percent)
    
    memory_percent = (used_flash / total_flash) * 100
    right_pie_filled, right_pie_unfilled = make_chart(right_centre_x, centre_y, radius_inner, radius_outer, memory_percent)
    
    screen.pen = light_red
    screen.shape(left_pie_filled)
    screen.pen = dark_red
    screen.shape(left_pie_unfilled)

    screen.pen = light_blue
    screen.shape(right_pie_filled)
    screen.pen = dark_blue
    screen.shape(right_pie_unfilled)
```
Not bad. You might find that the battery level is just showing a solid ring if you're at 100% battery of course.

## Tweaking the looks
That circle background isn't bad, but it's not the most inspiring thing ever. We could switch it out for something cooler, though - what about a drop shadow for the dials instead?

First, let's add another new dimension, in the same place as the others, and we'll say it's 2 distance units:
```python-raw
shadow_distance = 2 * du
```
You can alter that value until you get it just the distance you want. Now, let's get rid of the lines where we draw the circles. Delete the following lines:
```python-raw
    left_pie_background = shape.circle(left_centre_x, centre_y, radius_outer)
    right_pie_background = shape.circle(right_centre_x, centre_y, radius_outer)

    screen.pen = med_grey
    screen.shape(left_pie_background)
    screen.shape(right_pie_background)
```

Instead, we're going to do some more drawing after we've worked out the shapes of the graphs, but before we draw them. We want to use the shapes we've already made, but have them shifted down and to the right by `shadow_distance` pixels. For this we'll use a `mat3` to transform the shape.

`mat3` is a transformation matrix. It combines any of translation (movement), rotation and scaling into one set of numbers that get applied to the points of a shape. We're going to make a simple `mat3` which we can reuse for other elements, which represents moving down and to the right by `shadow_distance` pixels. Then we can apply that matrix to any shape by setting the shape's `transform` property to the matrix.

```python-raw
shadow_matrix = mat3().translate(shadow_distance, shadow_distance)
```
The `mat3()` here creates a blank matrix. Then running the `translate()` method on it gives it a translation by the amounts we've provided for x and y. We're going to put this line just after we work out our dimensions, as it won't change as the program's being run.

In our `update()` method, we want to apply this matrix to the shapes we generate with our `make_chart()` method, draw them in a shadow colour, and then remove the matrix again so we can draw the charts themselves in the right place. Let's make a method that'll easily do that. You can put this below `make_chart()`.

```python-raw
def draw_drop_shadow(shape, colour, matrix):
    old_pen = screen.pen
    shape.transform = matrix
    screen.pen = colour
    screen.shape(shape)
    shape.transform = mat3()
    screen.pen = old_pen
```
Let's go through this line by line. First, we're remembering whtever colour the pen was set to, so the method can clean up after itself. Next we're applying the matrix to the shape - both of these, as well as the colour, get passed in using the method's parameters. Then we're setting the pen to the shadow colour, drawing the shape to the screen, and then we're cleaning up after ourselves by setting the pen back to what it was and setting the shape's transformation back to a blank matrix.

This is a pretty simple method, and there are a couple of things which you could customise to improve it. For example, this would currently only work on something that didn't already have a transformation applied to it. It also always draws to `screen` - both of these things are fixable, but they're not necessary for what we're doing here so let's move on.

Now we've made our method, we just need to call it. We have to call it after making the shapes, because we need to use them, but also before drawing the charts, because then the shadow would appear over the top of them. That leaves one place we can do it:

```python
screen.antialias = image.X4

# Getting all our dimensions together
centre_y = screen.height / 2
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100
shadow_distance = 2 * du

shadow_matrix = mat3().translate(shadow_distance, shadow_distance)

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)

# Takes in a percentage and dimensions to make two pie chart segments
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section

def draw_drop_shadow(shape, colour, matrix):
    old_pen = screen.pen
    shape.transform = matrix
    screen.pen = colour
    screen.shape(shape)
    shape.transform = mat3()
    screen.pen = old_pen

def update():
    battery_percent = badge.battery_level()
    battery_voltage = badge.battery_voltage()
    total_flash, used_flash, _ = badge.disk_free("/system")
    year, month, day, hour, minute, second, _ = rtc.datetime()

    screen.pen = light_grey
    screen.clear()

    left_pie_filled, left_pie_unfilled = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, battery_percent)
    
    memory_percent = (used_flash / total_flash) * 100
    right_pie_filled, right_pie_unfilled = make_chart(right_centre_x, centre_y, radius_inner, radius_outer, memory_percent)
    
    draw_drop_shadow(left_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(left_pie_unfilled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_unfilled, med_grey, shadow_matrix)

    screen.pen = light_red
    screen.shape(left_pie_filled)
    screen.pen = dark_red
    screen.shape(left_pie_unfilled)

    screen.pen = light_blue
    screen.shape(right_pie_filled)
    screen.pen = dark_blue
    screen.shape(right_pie_unfilled)
```

There we go, looking good.

## Writing on the wall
It's time to get some text onto the screen. We're going to be using vector fonts for this as they'll scale nicely. There are three vector fonts in .af format here, but you can find more at [the Alright Fonts GitHub repository](https://github.com/lowfatcode/alright-fonts). We're using one called Mona Sans.

First, we'll load the font in at the very top of the file with the following line:
```python-raw
monasans = font.load("/system/assets/fonts/MonaSans-Medium.af")
```

Then we need to calculate a size for it. We'll create three variables we can choose from, and they're once again going to be based on one of our existing dimensions - that way everything still scales along with the screen size. You can test this out at any time by putting the line `badge.mode(HIRES)` at the very beginning of your python file to put the badge into high resolution mode. You'll see things are sharper, but nothing should move about or change size on the screen. To go back to low resolution mode, just remove that line. You can use whichever mode you want during the tutorial, it should work just the same with either.

Right after our existing dimensions, let's put:
```python-raw
text_size_l = 10 * du
text_size_m = 8 * du
text_size_s = 6 * du
```
These have given good results for us, but you can play about with them and see what works for you.

Finally, let's get some text on the screen. Almost all of the text we'll want to display will be centred on a point, so we'll want to write something that'll let us centre text. We're not using the more advanced text functions in the `text` class here, but instead drawing straight onto the image as it's faster and allows us to position the text more easily.

Let's make another new method just above `update()`:
```python-raw
def centred_text(text, x, y, size):
    width, height = screen.measure_text(text, size)
    new_x = x - (width / 2)
    new_y = y - height
    screen.text(text, new_x, new_y, size)
```
Going through this line by line, we can see that `screen.measure_text()` gives us the dimensions of the specified text at the specified font size. Then we're taking the centre point we passed into the method, and we're subtracting half of the width from x, and all of the height from y, so that the baseline of the text will be at the point we specified, with the text centred horizontally. Finally we're drawing the text to the screen at the specified size, using these new x and y coordinates.

Let's try using this to write the battery percentage as a number in the middle of its chart. We'll convert it into a string and add a percent sign, then pass it into our new method, specifying the centre point of that left pie chart:

```python
badge.mode(HIRES)
screen.antialias = image.X4

monasans = font.load("/system/assets/fonts/MonaSans-Medium.af")

# Getting all our dimensions together
centre_y = screen.height / 2
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100
shadow_distance = 2 * du
text_size_l = 10 * du
text_size_m = 8 * du
text_size_s = 6 * du

shadow_matrix = mat3().translate(shadow_distance, shadow_distance)

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)

# Takes in a percentage and dimensions to make two pie chart segments
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section

def draw_drop_shadow(shape, colour, matrix):
    old_pen = screen.pen
    shape.transform = matrix
    screen.pen = colour
    screen.shape(shape)
    shape.transform = mat3()
    screen.pen = old_pen

def centred_text(text, x, y, size):
    width, height = screen.measure_text(text, size)
    new_x = x - (width / 2)
    new_y = y - height
    screen.text(text, new_x, new_y, size)

def update():
    battery_percent = badge.battery_level()
    battery_voltage = badge.battery_voltage()
    total_flash, used_flash, _ = badge.disk_free("/system")
    year, month, day, hour, minute, second, _ = rtc.datetime()

    screen.pen = light_grey
    screen.clear()

    left_pie_filled, left_pie_unfilled = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, battery_percent)
    
    memory_percent = (used_flash / total_flash) * 100
    right_pie_filled, right_pie_unfilled = make_chart(right_centre_x, centre_y, radius_inner, radius_outer, memory_percent)
    
    draw_drop_shadow(left_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(left_pie_unfilled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_unfilled, med_grey, shadow_matrix)

    screen.pen = light_red
    screen.shape(left_pie_filled)
    screen.pen = dark_red
    screen.shape(left_pie_unfilled)

    screen.pen = light_blue
    screen.shape(right_pie_filled)
    screen.pen = dark_blue
    screen.shape(right_pie_unfilled)

    screen.pen = color.black
    screen.font = monasans

    battery_text = str(battery_percent) + "%"
    centred_text(battery_text, left_centre_x, centre_y, text_size_l)
```
That's not bad, but we can probably tweak it. Now we've got it there, we can move its position around by adding or subtracting multiples of `du` to its position coordinates.

We'll add various other bits of text to the dashboard - they will all work in the same way, and all use variables we've already made:
```python
screen.antialias = image.X4

monasans = font.load("/system/assets/fonts/MonaSans-Medium.af")

# Getting all our dimensions together
centre_x = screen.width * 0.5
centre_y = screen.height * 0.42
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100
shadow_distance = 2 * du
text_size_l = 10 * du
text_size_m = 8 * du
text_size_s = 6 * du

shadow_matrix = mat3().translate(shadow_distance, shadow_distance)

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)

# Takes in a percentage and dimensions to make two pie chart segments
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section

def draw_drop_shadow(shape, colour, matrix):
    old_pen = screen.pen
    shape.transform = matrix
    screen.pen = colour
    screen.shape(shape)
    shape.transform = mat3()
    screen.pen = old_pen

def centred_text(text, x, y, size):
    width, height = screen.measure_text(text, size)
    new_x = x - (width / 2)
    new_y = y - height
    screen.text(text, new_x, new_y, size)

def update():
    battery_percent = badge.battery_level()
    battery_voltage = badge.battery_voltage()
    total_flash, used_flash, _ = badge.disk_free("/system")
    year, month, day, hour, minute, second, _ = rtc.datetime()

    screen.pen = light_grey
    screen.clear()

    left_pie_filled, left_pie_unfilled = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, battery_percent)
    
    memory_percent = (used_flash / total_flash) * 100
    right_pie_filled, right_pie_unfilled = make_chart(right_centre_x, centre_y, radius_inner, radius_outer, memory_percent)
    
    draw_drop_shadow(left_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(left_pie_unfilled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_unfilled, med_grey, shadow_matrix)

    screen.pen = light_red
    screen.shape(left_pie_filled)
    screen.pen = dark_red
    screen.shape(left_pie_unfilled)

    screen.pen = light_blue
    screen.shape(right_pie_filled)
    screen.pen = dark_blue
    screen.shape(right_pie_unfilled)

    screen.pen = color.black
    screen.font = monasans

    # Caption for the battery.
    centred_text("Battery", left_centre_x, centre_y - (2 * du), text_size_s)

    # Adding the percent sign to the battery level before drawing it.
    battery_text = str(battery_percent) + "%"
    centred_text(battery_text, left_centre_x, centre_y + (5.5 * du), text_size_l)

    # This just makes sure that once we round the voltage to two decimal places,
    # there's still a trailing zero where necessary.
    voltage_text = "{:.2f}".format(battery_voltage) + "V"
    centred_text(voltage_text, left_centre_x, centre_y + (27 * du), text_size_s)

    # Caption for the flash capacity.
    centred_text("Flash", right_centre_x, centre_y - (2 * du), text_size_s)

    # Adding the percent sign to the memory level before drawing it.
    memory_text = str(round(memory_percent)) + "%"
    centred_text(memory_text, right_centre_x, centre_y + (5.5 * du), text_size_l)

    # Converting the memory usage from bytes into MB, then drawing it.
    total_flash_mb = total_flash / 1048576
    used_flash_mb = used_flash / 1048576
    flash_text = "{:.2f}".format(used_flash_mb) + "MB /" + "{:.2f}".format(total_flash_mb) + "MB"
    centred_text(flash_text, right_centre_x, centre_y + (27 * du), text_size_s)

    # Here we just format each part of the time with the right number
    # of digits and no decimal places, then write it too.
    day_text = "{:02.0f}".format(day)
    month_text = "{:02.0f}".format(month)
    year_text = "{:04.0f}".format(year)
    hour_text = "{:02.0f}".format(hour)
    minute_text = "{:02.0f}".format(minute)
    second_text = "{:02.0f}".format(second)
    time_text = f"{day_text}/{month_text}/{year_text} {hour_text}:{minute_text}:{second_text}"

    # The y position of the time, we're defining it here
    # because we want to use it again later
    time_y = screen.height - (5 * du)

    centred_text(time_text, centre_x, time_y, text_size_l)

    centred_text("BADGEWARE DASHBOARD", centre_x, (7 * du), text_size_m)
```

You'll notice we created a new dimension - `centre_x` - to centre the date and time on the screen, and we also moved `centre_y` so that it's 42% of the way down the screen, not the exact centre. Because all of our graphs and their text are positioned relative to `centre_y`, they all move up together. The positions we've arrived at are based on trying different distances and sizes out until we find something that looks good.

## A backing for the clock
That clock looks a bit sparse, down there at the bottom of the screen. What if we put it inside a box, and reused the drop shadow method we made earlier to give it a shadow of its own?

To make the box, we really need to know the dimensions of the text so we can fit around it. We can find that out just like we did in the `centred_text()` method, just using `screen.measure_text()`:
```python-raw
time_width, time_height = screen.measure_text(time_text)
```
We'll insert that in after creating the string for the date and time, but before we draw it - we need to draw the box first, or else it'll be drawn over the top of the text. Right after that line, we can create the shape. We'll start by getting the x coordinate and the width:
```python-raw
time_box_x = centre_x - (time_width / 2) - (3 * du)
time_box_w = time_width + (6 * du)
```
We're going to put a 3 du border around the text, so for the x coordinate - the top left corner of the box - we'll take the centre point of the screen, minus half the text's width, minus the border. The width of the box will be the width of the text plus the width of both borders.

The y coordinate and height are going to be trickier. The height returned by `measure_text()` is the height of the entire glyph - basically, the height of the tallest letter in that font. There are taller glyphs than the numbers, because it includes things like accents and diacritics - so if we just worked out the y coordinate similarly to the x, we'd end up with a lot of extra space above the text. So for the top of the box and the height of it, we're going to have to try values and see what looks right for this font. You can try your own if you don't think it looks right or if you're using a different font:
```python-raw
time_box_y = time_y - time_height + (2 * du)
time_box_h = time_height + (0 * du)
```

Finally we can create the shape:
```python-raw
time_box = shape.rounded_rectangle(time_box_x, time_box_y, time_box_w, time_box_h, (3 * du))
```
We're using a `rounded_rectangle`, which takes in x, y, width and height just like a rectangle, but also takes in one or more values for the radius of the corners. We're making all the corners the same radius and setting it to 3 du.

Now we've got that, we can draw a shadow with it, just like we did for the pie charts:
```python-raw
draw_drop_shadow(time_box, med_grey, shadow_matrix)
```
Then we can just change the pen to black, draw the box itself, change the pen to white, write the text and finally change the pen back to black for the main header caption. That gives us this:
```python
screen.antialias = image.X4

monasans = font.load("/system/assets/fonts/MonaSans-Medium.af")

# Getting all our dimensions together
centre_x = screen.width * 0.5
centre_y = screen.height * 0.42
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100
shadow_distance = 2 * du
text_size_l = 10 * du
text_size_m = 8 * du
text_size_s = 6 * du

shadow_matrix = mat3().translate(shadow_distance, shadow_distance)

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)

# Takes in a percentage and dimensions to make two pie chart segments
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section

def draw_drop_shadow(shape, colour, matrix):
    old_pen = screen.pen
    shape.transform = matrix
    screen.pen = colour
    screen.shape(shape)
    shape.transform = mat3()
    screen.pen = old_pen

def centred_text(text, x, y, size):
    width, height = screen.measure_text(text, size)
    new_x = x - (width / 2)
    new_y = y - height
    screen.text(text, new_x, new_y, size)

def update():
    battery_percent = badge.battery_level()
    battery_voltage = badge.battery_voltage()
    total_flash, used_flash, _ = badge.disk_free("/system")
    year, month, day, hour, minute, second, _ = rtc.datetime()

    screen.pen = light_grey
    screen.clear()

    left_pie_filled, left_pie_unfilled = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, battery_percent)
    
    memory_percent = (used_flash / total_flash) * 100
    right_pie_filled, right_pie_unfilled = make_chart(right_centre_x, centre_y, radius_inner, radius_outer, memory_percent)
    
    draw_drop_shadow(left_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(left_pie_unfilled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_unfilled, med_grey, shadow_matrix)

    screen.pen = light_red
    screen.shape(left_pie_filled)
    screen.pen = dark_red
    screen.shape(left_pie_unfilled)

    screen.pen = light_blue
    screen.shape(right_pie_filled)
    screen.pen = dark_blue
    screen.shape(right_pie_unfilled)

    screen.pen = color.black
    screen.font = monasans

    # Caption for the battery.
    centred_text("Battery", left_centre_x, centre_y - (2 * du), text_size_s)

    # Adding the percent sign to the battery level before drawing it.
    battery_text = str(battery_percent) + "%"
    centred_text(battery_text, left_centre_x, centre_y + (5.5 * du), text_size_l)

    # This just makes sure that once we round the voltage to two decimal places,
    # there's still a trailing zero where necessary.
    voltage_text = "{:.2f}".format(battery_voltage) + "V"
    centred_text(voltage_text, left_centre_x, centre_y + (27 * du), text_size_s)

    # Caption for the flash capacity.
    centred_text("Flash", right_centre_x, centre_y - (2 * du), text_size_s)

    # Adding the percent sign to the memory level before drawing it.
    memory_text = str(round(memory_percent)) + "%"
    centred_text(memory_text, right_centre_x, centre_y + (5.5 * du), text_size_l)

    # Converting the memory usage from bytes into MB, then drawing it.
    total_flash_mb = total_flash / 1048576
    used_flash_mb = used_flash / 1048576
    flash_text = "{:.2f}".format(used_flash_mb) + "MB /" + "{:.2f}".format(total_flash_mb) + "MB"
    centred_text(flash_text, right_centre_x, centre_y + (27 * du), text_size_s)

    # Here we just format each part of the time with the right number
    # of digits and no decimal places, then write it too.
    day_text = "{:02.0f}".format(day)
    month_text = "{:02.0f}".format(month)
    year_text = "{:04.0f}".format(year)
    hour_text = "{:02.0f}".format(hour)
    minute_text = "{:02.0f}".format(minute)
    second_text = "{:02.0f}".format(second)
    time_text = f"{day_text}/{month_text}/{year_text} {hour_text}:{minute_text}:{second_text}"

    # The y position of the time, we're defining it here
    # because we want to use it again later
    time_y = screen.height - (5 * du)

    time_width, time_height = screen.measure_text(time_text, text_size_l)
    time_box_x = centre_x - (time_width / 2) - (3 * du)
    time_box_w = time_width + (6 * du)
    time_box_y = time_y - time_height + (2 * du)
    time_box_h = time_height + (0 * du)

    time_box = shape.rounded_rectangle(time_box_x, time_box_y, time_box_w, time_box_h, (3 * du))
    draw_drop_shadow(time_box, med_grey, shadow_matrix)

    screen.pen = color.black
    screen.shape(time_box)

    screen.pen = color.white
    centred_text(time_text, centre_x, time_y, text_size_l)

    screen.pen = color.black
    centred_text("BADGEWARE DASHBOARD", centre_x, (7 * du), text_size_m)
```

That looks great, but we're not done yet. Let's add some interactivity and give the user some control over the rear lighting.

## Lights on, lights off
The case lighting is controlled with one command, `badge.caselights()`. You can use this without parameters to get the current values, or plug in parameters to set them. First of all, let's make another method to toggle the case lights. After `centred_text()`, let's create this:
```python-raw
def toggle_caselights():
    caselight, _, _, _ = badge.caselights()
    if caselight > 0:
        badge.caselights(0)
    else:
        badge.caselights(255)
```
Going through this line by line, first we're getting the current brightness values of the LEDs. `badge.caselights()` returns four values, one for each LED, but since we're doing the same thing with all of the LEDs, they should all be the same so we can just take the value of the first one and discard the other three. The next lines just check the existing brightness and set the LEDs accordingly - if they're at anything above zero (which should most likely be 255, the maximum), set them to zero. And if they're at zero, set them to 255.

All we need to get this working is to hook it up to a button. That's very easy on Badgeware - all we need to do is ask if Button A was pressed between the last update and this one. We do this like so - this line goes at the very end of the program, inside `update()`:
```python-raw
    if badge.pressed(BUTTON_A):
        toggle_caselights()
```

`BUTTON_A` is a constant representing, you guessed it, the A button. `pressed()` is one of several methods in `badge` for checking the button status - if you pass them a button constant, they'll return True or False depending on the status of that button. If you call them without giving them a button, they'll return a tuple containing all of the buttons which would return True. Using `pressed()`, the LEDs will toggle on or off on the frame the button is pressed down. If you wanted to do it every time the button was released instead, you could use `released()` instead of pressed.

To have the LED come on only while the button was held down, you might think you'd use `held()`. But that detects whether the button is held, and with the code as it is that would mean that it would detect that the button was held down every frame, and so would toggle the light every frame. The LEDs would flash as fast as `update()` was looping, and we'd need to put an epilepsy warning on this tutorial.

Instead, we have `changed()`. This, as you might expect, returns True if the button has changed state, so if it has been pressed OR released. Using `changed()` instead of `pressed()`, you'll see that the LED is on while you have the button pressed and switches off when it is released. Have a play about with the different commands and see how they work.

## Chasing bugs
This dashboard is looking good. But there's a few annoying little things that we need to fix. For a start, you'll see that while the badge is plugged in, the battery level indicator shoots straight up to 100% or almost 100%, regardless of how much juice is in the battery. You also might have noticed that the dial wobbles and wiggles when it's on the cusp between two percentage points. We'll fix both of those things.

### The wobble
This isn't exactly the gauge reading wrong - it's just because the battery level readout is based on the voltage coming from the battery, and that voltage reading doesn't have unlimited precision. Still, we can easily stop it by only taking a reading of the battery level, say, every couple of seconds.

To do this, we'll first need to make the battery level a global variable, so that in those updates where we're not taking a fresh reading, we still have something to tell us how to draw the pie chart and so on. While we're at it, let's do this with all of our readings we're taking except for the time, as it'll save just a little processing power.

We're going to copy these lines:
```python-raw
    battery_percent = badge.battery_level()
    battery_voltage = badge.battery_voltage()
    total_flash, used_flash, _ = badge.disk_free("/system")
```
They'll be going outside `update()`, after our colours and before our `make_chart()` method. Since we're defining these variables up there now and reusing them for each cycle of `update()`, we'll need to tell `update()` to use these ones. Add the following line at the very top of `update()`:
```python-raw
    global battery_percent, battery_voltage, total_flash, used_flash
```

Now we have to modify `update()` so that it's only refreshing those values every couple of seconds. To start we need to make another global variable, in the same place we copied the other variables to:
```python-raw
last_refresh = badge.ticks
```
And add `last_refresh` to the list in the line we just wrote beginning with `global`.

`last_refresh` is for our timing. It's set up using `badge.ticks`, which is the number of milliseconds since the badge was powered on. We're going to check `badge.ticks` every time we go round `update()` and see if it's been more than 2000 ticks since `last_refresh` - if it has, then that means two seconds have passed. In that case we'll refresh the battery and memory values, and set `last_refresh` to the current `badge.ticks`. That way, the whole cycle will repeat again every two seconds.

In practice, that means modifying the beginning of our `update()` to look like this:
```python-raw
def update():
    global battery_percent, battery_voltage, total_flash, used_flash, last_update

    if badge.ticks - last_update > 2000:
        battery_percent = badge.battery_level()
        battery_voltage = badge.battery_voltage()
        total_flash, used_flash, _ = badge.disk_free("/system")
        last_update = badge.ticks

    year, month, day, hour, minute, second, _ = rtc.datetime()
```
This should now update the graphs every two seconds and get rid of that annoying wobble.

### The plug bug
Now we'll tackle what the battery indicator does when you're plugged in. The easiest thing would probably be to just display a plug icon instead when it's plugged in, so let's do that. First, let's rearrange things so that all of the lines regarding the left hand graph and its text are together. That gives us this:
```python
screen.antialias = image.X4

monasans = font.load("/system/assets/fonts/MonaSans-Medium.af")

# Getting all our dimensions together
centre_x = screen.width * 0.5
centre_y = screen.height * 0.42
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100
shadow_distance = 2 * du
text_size_l = 10 * du
text_size_m = 8 * du
text_size_s = 6 * du

shadow_matrix = mat3().translate(shadow_distance, shadow_distance)

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)

battery_percent = badge.battery_level()
battery_voltage = badge.battery_voltage()
total_flash, used_flash, _ = badge.disk_free("/system")
last_update = badge.ticks

# Takes in a percentage and dimensions to make two pie chart segments
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section

def draw_drop_shadow(shape, colour, matrix):
    old_pen = screen.pen
    shape.transform = matrix
    screen.pen = colour
    screen.shape(shape)
    shape.transform = mat3()
    screen.pen = old_pen

def centred_text(text, x, y, size):
    width, height = screen.measure_text(text, size)
    new_x = x - (width / 2)
    new_y = y - height
    screen.text(text, new_x, new_y, size)

def toggle_caselights():
    caselight, _, _, _ = badge.caselights()
    if caselight > 0:
        badge.caselights(0)
    else:
        badge.caselights(255)

def update():
    global battery_percent, battery_voltage, total_flash, used_flash, last_update, i

    if badge.ticks - last_update > 2000:
        battery_percent = badge.battery_level()
        battery_voltage = badge.battery_voltage()
        total_flash, used_flash, _ = badge.disk_free("/system")
        last_update = badge.ticks

    year, month, day, hour, minute, second, _ = rtc.datetime()

    screen.pen = light_grey
    screen.clear()

    # BATTERY READOUT STARTS HERE

    left_pie_filled, left_pie_unfilled = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, battery_percent)
    
    draw_drop_shadow(left_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(left_pie_unfilled, med_grey, shadow_matrix)

    screen.pen = light_red
    screen.shape(left_pie_filled)
    screen.pen = dark_red
    screen.shape(left_pie_unfilled)

    screen.pen = color.black
    screen.font = monasans

    # Caption for the battery.
    centred_text("Battery", left_centre_x, centre_y - (2 * du), text_size_s)

    # Adding the percent sign to the battery level before drawing it.
    battery_text = str(battery_percent) + "%"
    centred_text(battery_text, left_centre_x, centre_y + (5.5 * du), text_size_l)

    # This just makes sure that once we round the voltage to two decimal places,
    # there's still a trailing zero where necessary.
    voltage_text = "{:.2f}".format(battery_voltage) + "V"
    centred_text(voltage_text, left_centre_x, centre_y + (27 * du), text_size_s)

    # MEMORY READOUT STARTS HERE

    memory_percent = (used_flash / total_flash) * 100
    right_pie_filled, right_pie_unfilled = make_chart(right_centre_x, centre_y, radius_inner, radius_outer, memory_percent)
    
    draw_drop_shadow(right_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_unfilled, med_grey, shadow_matrix)

    screen.pen = light_blue
    screen.shape(right_pie_filled)
    screen.pen = dark_blue
    screen.shape(right_pie_unfilled)

    screen.pen = color.black
    screen.font = monasans

    # Caption for the flash capacity.
    centred_text("Flash", right_centre_x, centre_y - (2 * du), text_size_s)

    # Adding the percent sign to the memory level before drawing it.
    memory_text = str(round(memory_percent)) + "%"
    centred_text(memory_text, right_centre_x, centre_y + (5.5 * du), text_size_l)

    # Converting the memory usage from bytes into MB, then drawing it.
    total_flash_mb = total_flash / 1048576
    used_flash_mb = used_flash / 1048576
    flash_text = "{:.2f}".format(used_flash_mb) + "MB /" + "{:.2f}".format(total_flash_mb) + "MB"
    centred_text(flash_text, right_centre_x, centre_y + (27 * du), text_size_s)

    # Here we just format each part of the time with the right number
    # of digits and no decimal places, then write it too.
    day_text = "{:02.0f}".format(day)
    month_text = "{:02.0f}".format(month)
    year_text = "{:04.0f}".format(year)
    hour_text = "{:02.0f}".format(hour)
    minute_text = "{:02.0f}".format(minute)
    second_text = "{:02.0f}".format(second)
    time_text = f"{day_text}/{month_text}/{year_text} {hour_text}:{minute_text}:{second_text}"

    # The y position of the time, we're defining it here
    # because we want to use it again later
    time_y = screen.height - (5 * du)

    time_width, time_height = screen.measure_text(time_text, text_size_l)
    time_box_x = centre_x - (time_width / 2) - (3 * du)
    time_box_w = time_width + (6 * du)
    time_box_y = time_y - time_height + (2 * du)
    time_box_h = time_height + (0 * du)

    time_box = shape.rounded_rectangle(time_box_x, time_box_y, time_box_w, time_box_h, (3 * du))
    draw_drop_shadow(time_box, med_grey, shadow_matrix)

    screen.pen = color.black
    screen.shape(time_box)

    screen.pen = color.white
    centred_text(time_text, centre_x, time_y, text_size_l)

    screen.pen = color.black
    centred_text("BADGEWARE DASHBOARD", centre_x, (7 * du), text_size_m)

    if badge.pressed(BUTTON_A):
        toggle_caselights()
```
This should work exactly the same, but now all of the battery stuff is separated out into one place. You'll notice we've also duplicated the line where we're setting the font and text colour.

Now, we can just toggle whether or not we draw any of the battery info based on an `if` statement. But what's the statement checking? Well, Badgeware has a built in function called `badge.usb_connected()` which is perfect for our needs - it simply returns True if the USB is connected, and False if not. Let's apply that to the code:
```python
screen.antialias = image.X4

monasans = font.load("/system/assets/fonts/MonaSans-Medium.af")

# Getting all our dimensions together
centre_x = screen.width * 0.5
centre_y = screen.height * 0.42
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100
shadow_distance = 2 * du
text_size_l = 10 * du
text_size_m = 8 * du
text_size_s = 6 * du

shadow_matrix = mat3().translate(shadow_distance, shadow_distance)

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)

battery_percent = badge.battery_level()
battery_voltage = badge.battery_voltage()
total_flash, used_flash, _ = badge.disk_free("/system")
last_update = badge.ticks

# Takes in a percentage and dimensions to make two pie chart segments
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section

def draw_drop_shadow(shape, colour, matrix):
    old_pen = screen.pen
    shape.transform = matrix
    screen.pen = colour
    screen.shape(shape)
    shape.transform = mat3()
    screen.pen = old_pen

def centred_text(text, x, y, size):
    width, height = screen.measure_text(text, size)
    new_x = x - (width / 2)
    new_y = y - height
    screen.text(text, new_x, new_y, size)

def toggle_caselights():
    caselight, _, _, _ = badge.caselights()
    if caselight > 0:
        badge.caselights(0)
    else:
        badge.caselights(255)

def update():
    global battery_percent, battery_voltage, total_flash, used_flash, last_update, i

    if badge.ticks - last_update > 2000:
        battery_percent = badge.battery_level()
        battery_voltage = badge.battery_voltage()
        total_flash, used_flash, _ = badge.disk_free("/system")
        last_update = badge.ticks

    year, month, day, hour, minute, second, _ = rtc.datetime()

    screen.pen = light_grey
    screen.clear()

    # BATTERY READOUT STARTS HERE

    if badge.usb_connected():
        left_pie_filled, left_pie_unfilled = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, battery_percent)
        
        draw_drop_shadow(left_pie_filled, med_grey, shadow_matrix)
        draw_drop_shadow(left_pie_unfilled, med_grey, shadow_matrix)

        screen.pen = light_red
        screen.shape(left_pie_filled)
        screen.pen = dark_red
        screen.shape(left_pie_unfilled)

        screen.pen = color.black
        screen.font = monasans

        # Caption for the battery.
        centred_text("Battery", left_centre_x, centre_y - (2 * du), text_size_s)

        # Adding the percent sign to the battery level before drawing it.
        battery_text = str(battery_percent) + "%"
        centred_text(battery_text, left_centre_x, centre_y + (5.5 * du), text_size_l)

        # This just makes sure that once we round the voltage to two decimal places,
        # there's still a trailing zero where necessary.
        voltage_text = "{:.2f}".format(battery_voltage) + "V"
        centred_text(voltage_text, left_centre_x, centre_y + (27 * du), text_size_s)

    # MEMORY READOUT STARTS HERE

    memory_percent = (used_flash / total_flash) * 100
    right_pie_filled, right_pie_unfilled = make_chart(right_centre_x, centre_y, radius_inner, radius_outer, memory_percent)
    
    draw_drop_shadow(right_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_unfilled, med_grey, shadow_matrix)

    screen.pen = light_blue
    screen.shape(right_pie_filled)
    screen.pen = dark_blue
    screen.shape(right_pie_unfilled)

    screen.pen = color.black
    screen.font = monasans

    # Caption for the flash capacity.
    centred_text("Flash", right_centre_x, centre_y - (2 * du), text_size_s)

    # Adding the percent sign to the memory level before drawing it.
    memory_text = str(round(memory_percent)) + "%"
    centred_text(memory_text, right_centre_x, centre_y + (5.5 * du), text_size_l)

    # Converting the memory usage from bytes into MB, then drawing it.
    total_flash_mb = total_flash / 1048576
    used_flash_mb = used_flash / 1048576
    flash_text = "{:.2f}".format(used_flash_mb) + "MB /" + "{:.2f}".format(total_flash_mb) + "MB"
    centred_text(flash_text, right_centre_x, centre_y + (27 * du), text_size_s)

    # Here we just format each part of the time with the right number
    # of digits and no decimal places, then write it too.
    day_text = "{:02.0f}".format(day)
    month_text = "{:02.0f}".format(month)
    year_text = "{:04.0f}".format(year)
    hour_text = "{:02.0f}".format(hour)
    minute_text = "{:02.0f}".format(minute)
    second_text = "{:02.0f}".format(second)
    time_text = f"{day_text}/{month_text}/{year_text} {hour_text}:{minute_text}:{second_text}"

    # The y position of the time, we're defining it here
    # because we want to use it again later
    time_y = screen.height - (5 * du)

    time_width, time_height = screen.measure_text(time_text, text_size_l)
    time_box_x = centre_x - (time_width / 2) - (3 * du)
    time_box_w = time_width + (6 * du)
    time_box_y = time_y - time_height + (2 * du)
    time_box_h = time_height + (0 * du)

    time_box = shape.rounded_rectangle(time_box_x, time_box_y, time_box_w, time_box_h, (3 * du))
    draw_drop_shadow(time_box, med_grey, shadow_matrix)

    screen.pen = color.black
    screen.shape(time_box)

    screen.pen = color.white
    centred_text(time_text, centre_x, time_y, text_size_l)

    screen.pen = color.black
    centred_text("BADGEWARE DASHBOARD", centre_x, (7 * du), text_size_m)

    if badge.pressed(BUTTON_A):
        toggle_caselights()
```
Well, that's certainly done something, but it's the wrong way round - the graph is displaying when the cable is connected, and that's when we want it to disappear. We could of course just change it to `if not badge.usb_connected():`, but we want to display something else when it is connected so instead let's make this `if` into an `if...else` and put our graph drawing code into the `else` bit:
```python-raw
    if badge.usb_connected():
        pass
    else:
        # graph-drawing code
```

What are we going to do with that `else` section? We could blit an image in the graph's place, but we're trying to keep everything as vectors right now, so let's draw one using the different `shape` primitives - we've worked this one out, but you can experiment and create your own:
```python-raw
    if badge.usb_connected():
        plug1, _ = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, 100)
        plug2 = shape.circle(left_centre_x, centre_y, (4 * du))
        plug3 = shape.rectangle(left_centre_x - (4 * du), centre_y - (4 * du), 8 * du, 4 * du)
        plug4 = shape.line(left_centre_x - (2 * du), centre_y, left_centre_x - (2 * du), centre_y - (8 * du), (2 * du))
        plug5 = shape.line(left_centre_x + (2 * du), centre_y, left_centre_x + (2 * du), centre_y - (8 * du), (2 * du))
        plug6 = shape.line(left_centre_x, centre_y, left_centre_x, centre_y + (8 * du), (2 * du))

        draw_drop_shadow(plug1, med_grey, shadow_matrix)

        screen.pen = light_green
        screen.shape(plug1)

        screen.pen = color.black
        screen.shape(plug2)
        screen.shape(plug3)
        screen.shape(plug4)
        screen.shape(plug5)
        screen.shape(plug6)
```
We're also adding a couple of new colours:
```python-raw
dark_green = color.rgb(0, 125, 0)
light_green = color.rgb(42, 255, 42)
```
There's just one finishing touch. Badgeware also offers a function, `badge.is_charging()` which returns whether or not the unit is fully charging. Let's add a text line, in the same place as the voltage readout when unplugged, to say "Charging" or "Fully Charged" and change the colour accordingly:
```python-raw
    if badge.usb_connected():
        plug1, _ = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, 100)
        plug2 = shape.circle(left_centre_x, centre_y, (4 * du))
        plug3 = shape.rectangle(left_centre_x - (4 * du), centre_y - (4 * du), 8 * du, 4 * du)
        plug4 = shape.line(left_centre_x - (2 * du), centre_y, left_centre_x - (2 * du), centre_y - (8 * du), (2 * du))
        plug5 = shape.line(left_centre_x + (2 * du), centre_y, left_centre_x + (2 * du), centre_y - (8 * du), (2 * du))
        plug6 = shape.line(left_centre_x, centre_y, left_centre_x, centre_y + (8 * du), (2 * du))

        draw_drop_shadow(plug1, med_grey, shadow_matrix)

        if badge.is_charging():
            screen.pen = dark_green
            charge_status_text = "Charging..."
        else:
            screen.pen = light_green
            charge_status_text = "Fully charged"

        screen.shape(plug1)

        screen.pen = color.black
        centred_text(charge_status_text, left_centre_x, centre_y + (27 * du), text_size_s)

        screen.shape(plug2)
        screen.shape(plug3)
        screen.shape(plug4)
        screen.shape(plug5)
        screen.shape(plug6)
```

Phew! That's it, we're done. Here's the full code for your `__init__.py` - every single thing you draw to the screen is in this file.
```python
screen.antialias = image.X4

monasans = font.load("/system/assets/fonts/MonaSans-Medium.af")

# Getting all our dimensions together
centre_x = screen.width * 0.5
centre_y = screen.height * 0.42
left_centre_x = screen.width * 0.25
right_centre_x = screen.width * 0.75
radius_outer = screen.width * 0.2
radius_inner = radius_outer * 0.6
du = screen.width / 100
shadow_distance = 2 * du
text_size_l = 10 * du
text_size_m = 8 * du
text_size_s = 6 * du

shadow_matrix = mat3().translate(shadow_distance, shadow_distance)

# Defining some colours too
light_grey = color.rgb(240, 240, 240)
med_grey = color.rgb(192, 192, 192)
dark_red = color.rgb(125, 0, 0)
light_red = color.rgb(255, 42, 42)
dark_blue = color.rgb(12, 60, 212)
light_blue = color.rgb(87, 147, 240)
dark_green = color.rgb(0, 125, 0)
light_green = color.rgb(42, 255, 42)

battery_percent = badge.battery_level()
battery_voltage = badge.battery_voltage()
total_flash, used_flash, _ = badge.disk_free("/system")
last_update = badge.ticks

# Takes in a percentage and dimensions to make two pie chart segments
def make_chart(x, y, inner, outer, percentage):
    seg_1_start = 0
    seg_1_end = (percentage / 100) * 359.999
    seg_2_start = seg_1_end
    seg_2_end = 359.999

    filled_section = shape.arc(x, y, inner, outer, seg_1_start, seg_1_end)
    unfilled_section = shape.arc(x, y, inner, outer, seg_2_start, seg_2_end)

    return filled_section, unfilled_section

def draw_drop_shadow(shape, colour, matrix):
    old_pen = screen.pen
    shape.transform = matrix
    screen.pen = colour
    screen.shape(shape)
    shape.transform = mat3()
    screen.pen = old_pen

def centred_text(text, x, y, size):
    width, height = screen.measure_text(text, size)
    new_x = x - (width / 2)
    new_y = y - height
    screen.text(text, new_x, new_y, size)

def toggle_caselights():
    caselight, _, _, _ = badge.caselights()
    if caselight > 0:
        badge.caselights(0)
    else:
        badge.caselights(255)

def update():
    global battery_percent, battery_voltage, total_flash, used_flash, last_update, i

    if badge.ticks - last_update > 2000:
        battery_percent = badge.battery_level()
        battery_voltage = badge.battery_voltage()
        total_flash, used_flash, _ = badge.disk_free("/system")
        last_update = badge.ticks

    year, month, day, hour, minute, second, _ = rtc.datetime()

    screen.pen = light_grey
    screen.clear()

    # BATTERY READOUT STARTS HERE

    if badge.usb_connected():
        plug1, _ = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, 100)
        plug2 = shape.circle(left_centre_x, centre_y, (4 * du))
        plug3 = shape.rectangle(left_centre_x - (4 * du), centre_y - (4 * du), 8 * du, 4 * du)
        plug4 = shape.line(left_centre_x - (2 * du), centre_y, left_centre_x - (2 * du), centre_y - (8 * du), (2 * du))
        plug5 = shape.line(left_centre_x + (2 * du), centre_y, left_centre_x + (2 * du), centre_y - (8 * du), (2 * du))
        plug6 = shape.line(left_centre_x, centre_y, left_centre_x, centre_y + (8 * du), (2 * du))

        draw_drop_shadow(plug1, med_grey, shadow_matrix)

        if badge.is_charging():
            screen.pen = dark_green
            charge_status_text = "Charging..."
        else:
            screen.pen = light_green
            charge_status_text = "Fully charged"

        screen.shape(plug1)

        screen.pen = color.black
        centred_text(charge_status_text, left_centre_x, centre_y + (27 * du), text_size_s)

        screen.shape(plug2)
        screen.shape(plug3)
        screen.shape(plug4)
        screen.shape(plug5)
        screen.shape(plug6)
    else:
        left_pie_filled, left_pie_unfilled = make_chart(left_centre_x, centre_y, radius_inner, radius_outer, battery_percent)
        
        draw_drop_shadow(left_pie_filled, med_grey, shadow_matrix)
        draw_drop_shadow(left_pie_unfilled, med_grey, shadow_matrix)

        screen.pen = light_red
        screen.shape(left_pie_filled)
        screen.pen = dark_red
        screen.shape(left_pie_unfilled)

        screen.pen = color.black
        screen.font = monasans

        # Caption for the battery.
        centred_text("Battery", left_centre_x, centre_y - (2 * du), text_size_s)

        # Adding the percent sign to the battery level before drawing it.
        battery_text = str(battery_percent) + "%"
        centred_text(battery_text, left_centre_x, centre_y + (5.5 * du), text_size_l)

        # This just makes sure that once we round the voltage to two decimal places,
        # there's still a trailing zero where necessary.
        voltage_text = "{:.2f}".format(battery_voltage) + "V"
        centred_text(voltage_text, left_centre_x, centre_y + (27 * du), text_size_s)

    # MEMORY READOUT STARTS HERE

    memory_percent = (used_flash / total_flash) * 100
    right_pie_filled, right_pie_unfilled = make_chart(right_centre_x, centre_y, radius_inner, radius_outer, memory_percent)
    
    draw_drop_shadow(right_pie_filled, med_grey, shadow_matrix)
    draw_drop_shadow(right_pie_unfilled, med_grey, shadow_matrix)

    screen.pen = light_blue
    screen.shape(right_pie_filled)
    screen.pen = dark_blue
    screen.shape(right_pie_unfilled)

    screen.pen = color.black
    screen.font = monasans

    # Caption for the flash capacity.
    centred_text("Flash", right_centre_x, centre_y - (2 * du), text_size_s)

    # Adding the percent sign to the memory level before drawing it.
    memory_text = str(round(memory_percent)) + "%"
    centred_text(memory_text, right_centre_x, centre_y + (5.5 * du), text_size_l)

    # Converting the memory usage from bytes into MB, then drawing it.
    total_flash_mb = total_flash / 1048576
    used_flash_mb = used_flash / 1048576
    flash_text = "{:.2f}".format(used_flash_mb) + "MB /" + "{:.2f}".format(total_flash_mb) + "MB"
    centred_text(flash_text, right_centre_x, centre_y + (27 * du), text_size_s)

    # Here we just format each part of the time with the right number
    # of digits and no decimal places, then write it too.
    day_text = "{:02.0f}".format(day)
    month_text = "{:02.0f}".format(month)
    year_text = "{:04.0f}".format(year)
    hour_text = "{:02.0f}".format(hour)
    minute_text = "{:02.0f}".format(minute)
    second_text = "{:02.0f}".format(second)
    time_text = f"{day_text}/{month_text}/{year_text} {hour_text}:{minute_text}:{second_text}"

    # The y position of the time, we're defining it here
    # because we want to use it again later
    time_y = screen.height - (5 * du)

    time_width, time_height = screen.measure_text(time_text, text_size_l)
    time_box_x = centre_x - (time_width / 2) - (3 * du)
    time_box_w = time_width + (6 * du)
    time_box_y = time_y - time_height + (2 * du)
    time_box_h = time_height + (0 * du)

    time_box = shape.rounded_rectangle(time_box_x, time_box_y, time_box_w, time_box_h, (3 * du))
    draw_drop_shadow(time_box, med_grey, shadow_matrix)

    screen.pen = color.black
    screen.shape(time_box)

    screen.pen = color.white
    centred_text(time_text, centre_x, time_y, text_size_l)

    screen.pen = color.black
    centred_text("BADGEWARE DASHBOARD", centre_x, (7 * du), text_size_m)

    if badge.pressed(BUTTON_A):
        toggle_caselights()
```

Finally we're at the end of this tutorial. In the next one, we'll look at making things MOVE.