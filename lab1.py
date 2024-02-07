import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.animation import FFMpegWriter
import tkinter as tk
from tkinter import ttk

# Input from Users

name =input("Enter the name \n")
height = int(input("Enter the height of the person \n"))

# Initializing TkInter Window
window = tk.Tk()
window.title("Membership of Height")
height_var = tk.IntVar()
label1 = tk.Label(window, text="Enter the name of the person")
label2 = tk.Label(window, text="Enter the height of the person")

n = tk.Entry(window)
h = tk.Entry(window)

label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
n.grid(row=0, column=2)
h.grid(row=1, column=2)
n.insert(0, name)
h.insert(0, str(height))

#Height Fuzzy Functions
def short_height(x):
    if x <= 150:
        return 1.0
    elif x > 150 and x <= 170:
        return (170 - x) / 20
    else:
        return 0.0

def average_height(x):
    if x <= 150 or x >= 190:
        return 0.0
    elif x > 150 and x <= 175:
        return (x - 150) / 25.0
    else:
        return (190 - x) / 15.0

def tall_height(x):
    if x <= 180:
        return 0.0
    elif x > 180 and x <= 210:
        return (x - 180) /  30
    else:
            return 1.0
    

# name = n.get()
# # global height
# # height_of_human = h.get()
# # height = int(height_of_human)
# # def intget(val):
# #      number = val
# #      global num
# #      num = int(number)
# #      return num
# height = h.get()

#Assigning range for the functions [0, 250]
height_range = np.arange(0, 251, 1)

# Storing membership values in list
short_height_values = []
average_height_values = []
tall_height_values = []
for i in height_range:
    short_height_values.append(short_height(i))
    average_height_values.append(average_height(i))
    tall_height_values.append(tall_height(i))



# Plotting Graphs
def plot_graph():
    # ruth = 155
    # rishi = 170
    # yao = 229

    # print(short_height(ruth), average_height(ruth), tall_height(ruth))
    # print(short_height(rishi), average_height(rishi), tall_height(rishi))
    # print(short_height(yao), average_height(yao), tall_height(yao))
    heights = [height]*4
    membership = [1]
    membership.append(short_height(height))
    membership.append(average_height(height))
    membership.append(tall_height(height))
    plt.figure(figsize=(8, 6))
    plt.plot(height_range, short_height_values, label='Short', color='r')
    plt.plot(height, short_height(int(height)), 'r*')
    plt.text(height, short_height(height), f"Short Membership {short_height(height).__round__(2)}", horizontalalignment="left")
    plt.plot(height_range, tall_height_values, label='Tall', color='g')
    plt.plot(height, average_height(int(height)), 'b*')
    plt.text(height, average_height(height), f"Average Membership {average_height(height).__round__(2)}" , horizontalalignment="right")
    plt.plot(height_range, average_height_values, label='Average', color='b')
    plt.plot(height, tall_height(int(height)), "g*")
    plt.text(height, tall_height(height), f"Tall Membership {tall_height(height).__round__(2)}", horizontalalignment="right")
    plt.plot(heights, membership, label="Membership Line", c="black")
    plt.title('Membership Function for Height')
    plt.xlabel('Height (cm)')
    plt.ylabel('Membership Value')
    plt.legend()
    plt.show()

    Label1 = tk.Label(text="Membership Functions for {}".format(name)).grid(row=3, column=1)
    Label2 = tk.Label(text = "Short Fuzzy {}".format(str(short_height(int(height))))).grid(row=4, column=1)
    Label3 = tk.Label(text="Average Fuzzy {}".format(str(average_height(int(height))))).grid(row=5, column=1)
    Label4 = tk.Label(text="Tall Fuzzy {}".format(str(tall_height(int(height))))).grid(row=6, column=1)

graph = tk.Button(window, text="Plot Graph", command=plot_graph)
graph.grid(row=2, column=1)

print("Membership Functions for {}".format(name))
print("Short Fuzzy {}".format(str(short_height(int(height)))))
print("Average Fuzzy {}".format(str(average_height(int(height)))))
print("Tall Fuzzy {}".format(str(tall_height(int(height)))))

window.mainloop()