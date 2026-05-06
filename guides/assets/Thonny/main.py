def update():
    screen.pen = color.navy
    screen.clear()
    screen.pen = color.white
    screen.font = rom_font.smart
    screen.text("Running from Thonny", 10, 50)
run(update)