from tkinter import *
import math
import numpy as np
from colour import Color
import threading

canvas_width = 500
canvas_height = 500

minX = -2
maxX = 1
minY = -1.5
maxY = 1.5

num_threads = 4
maxIterations = 30
mandelbrotThreshold = 16

colors = []

class Point:
    x = 0
    y = 0
    n = 0

def paint(arg=0):

    global colors

    points = []

    xFactor = float(canvas_width) / abs(maxY - minY)
    yFactor = float(canvas_height) / abs(maxY - minY)
    midX = abs(maxY - minY) / 2
    midY = abs(maxY - minY) / 2

    # Split the points into equal-sized chunks 
    chunks = []

    # x1 = list(range(0, int(canvas_width / 2)))
    # y1 = list(range(0, int(canvas_height / 2)))
    # x2 = list(range(int(canvas_width / 2), canvas_width))
    # y2 = list(range(int(canvas_height / 2), canvas_height))

    # x1 = [minX + float(x / canvas_width) * difX for x in x1]
    # y1 = [minY + float(y / canvas_height) * difY for y in y1]
    # x2 = [minX + float(x / canvas_width) * difX for x in x2]
    # y2 = [minY + float(y / canvas_height) * difY for y in y2]

    chunks.append({"minX": minX,
                    "maxX": maxX - midX,
                    "minY": minY,
                    "maxY": maxY - midY})
    chunks.append({"minX": maxX - midX,
                    "maxX": maxX,
                    "minY": minY,
                    "maxY": maxY - midY})
    chunks.append({"minX": minX,
                    "maxX": maxX - midX,
                    "minY": maxY - midY,
                    "maxY": maxY})
    chunks.append({"minX": maxX - midX,
                    "maxX": maxX,
                    "minY": maxY - midY,
                    "maxY": maxY})

    # TESTING
    # x = []
    # y = []
    # for i in x1, x2:
    #     x.append(i)
    # for i in y1, y2:
    #     y.append(i)

    # print(x)

    # print([i for i in range(0, canvas_width) if i not in x])
    # print([i for i in range(0, canvas_height) if i not in y])

    # TESTING

    # chunks.append([[x, y] for x in x1 for y in y1])
    # chunks.append([[x, y] for x in x1 for y in y2])
    # chunks.append([[x, y] for x in x2 for y in y1])
    # chunks.append([[x, y] for x in x2 for y in y2])

    

    # points_per_thread = (canvas_width * canvas_height) / num_threads
    # chunks = [list(range(i * points_per_thread, (i + 1) * points_per_thread)) for i in range(num_threads)]
    # # Add any leftover points to the last chunk
    # chunks[-1].extend(range(num_threads * points_per_thread, canvas_width * canvas_height))

    # Define a function to process a chunk of points
    def process_chunk(chunk):
        for x in np.linspace(chunk["minX"], chunk["maxX"], int(canvas_width / 2)):
            for y in np.linspace(chunk["minY"], chunk["maxY"], int(canvas_height / 2)):
        
                p = Point()

                a = x
                b = y
                n = 0
                while n < maxIterations:
                    aa = a*a - b*b
                    bb = 2 * a * b
                    
                    a = aa + x
                    b = bb + y

                    if abs(a + b) > mandelbrotThreshold:
                        break

                    n += 1
                
                p.x = int(((abs(minX) + x)*xFactor))
                if minX > 0 and maxX > 0:
                    p.x = int(((x - minX)*xFactor))
                
                p.y = int(((abs(minY) + y)*yFactor))
                if minY > 0 and maxY > 0:
                    p.y = (int)((y - minY)*yFactor)
                
                p.n = n

                # print(f"appending point {p.x}, {p.y}, {p.n}")

                points.append(p)

    # Create threads to process each chunk of points
    threads = []
    for i, chunk in enumerate(chunks):
        thread = threading.Thread(target=process_chunk, args=(chunk,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    for p in points:
        canvas.create_line(p.x, p.y, p.x+1, p.y, fill=colors[p.n - 1])


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