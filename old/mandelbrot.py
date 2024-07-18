from tkinter import *
import math
import numpy as np
from colour import Color

canvas_width = 200
canvas_height = 200

minX = -2
maxX = 1
minY = -1.5
maxY = 1.5

maxIterations = 30

colors = []

def paint(arg = 0):

    global colors

    # print(f"Started painting")
            
    xFactor = float(canvas_width)/abs(maxY - minY)
    yFactor = float(canvas_height)/abs(maxY - minY)

    px = 0
    py = 0

    for x in np.linspace(minX, maxX, canvas_width):
        for y in np.linspace(minY, maxY, canvas_height):
            a = x
            b = y
            n = 0
            while n < maxIterations:
                aa = a*a - b*b
                bb = 2 * a * b
                
                a = aa + x
                b = bb + y

                if abs(a + b) > 16:
                    break

                n += 1
            
            px = int(((abs(minX) + x)*xFactor))
            if minX > 0 and maxX > 0:
                px = int(((x - minX)*xFactor))
            
            py = int(((abs(minY) + y)*yFactor))
            if minY > 0 and maxY > 0:
                py = (int)((y - minY)*yFactor)

            # print(f"Printing {px}, {py}, {n}")
                
            canvas.create_line(px, py, px+1, py, fill=colors[n - 1])

    # print("Finished painting...")

def click(event):

    global minX
    global maxX
    global minY
    global maxY

    difX = abs(maxY - minY)
    difY = abs(maxY - minY)

    xClicked = np.linspace(minX, maxX, num=canvas_width)[event.x]
    yClicked = np.linspace(minY, maxY, num=canvas_height)[event.y]

    # print(f"Click at {xClicked}, {yClicked}")

    minX = xClicked - difX / 4
    maxX = xClicked + difX / 4
    minY = yClicked - difY / 4
    maxY = yClicked + difY / 4

    paint()

def reset(event):

    global minX
    global maxX
    global minY
    global maxY

    minX = -2
    maxX = 1
    minY = -1.5
    maxY = 1.5

    paint()

def quit(event):
    exit()

colorSetting = input("1. Black and White\n2. Blue and Green\n3. Pink and Purple\nPlease choose colour option: ")


if int(colorSetting) == 1:
    colors = list(Color("white").range_to(Color("black"),maxIterations))
elif int(colorSetting) == 2:
    colors = list(Color("blue").range_to(Color("green"),maxIterations))
elif int(colorSetting) == 3:
    colors = list(Color("pink").range_to(Color("purple"),maxIterations))

else:
    colors = list(Color("white").range_to(Color("black"),maxIterations))


master = Tk()
master.title( "Mandelbrot" )
canvas = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
canvas.pack(expand = YES, fill = BOTH)

master.bind("<Button>", click)
master.bind("r", reset)
master.bind("q", quit)

paint()
mainloop()