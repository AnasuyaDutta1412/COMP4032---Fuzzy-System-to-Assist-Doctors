# Antecedents -> Sensor 1 and Sensor 2
## Linguistic Variables -> Far, Near

# Consequent -> Movement - Turns
## Linguistic Terms -> Hard left, straight, Hard right

# Rules
## -> If S1 NEAR and S2 NEAR then turn LEFT
## -> If S1 FAR and S2 NEAR then turn LEFT
## -> If S1 NEAR and S2 FAR then turn RIGHT
## -> if S1 FAR and S2 FAR then move straight

## Membership functions

## Universe of Discourse -> Input [0, 50]
## Universe of Discourse -> Output [0, 100]

## Partitions -> Input
# Near -> Open Left MF (a = 10, b = 20)
# Far -> Open Right MF (a = 10, b = 20)

## Partitions -> Output
# Hard Left -> Triangular
# Hard Right -> Traingular
# Center -> Gaussian OR Gaussian and Traingle Mixture

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt
import math

# Universe variables
distance_universe = np.linspace(0, 50, 51)
steering_universe = np.linspace(0, 100, 101)
print(distance_universe)

# Open left trapezoidal function
def open_left_trapezoidal(x):
    if x <= 10:
        return 1.0
    elif x > 10 and x <= 20:
        return (20 - x) / 10
    else:
        return 0.0

# Open right trapezoidal function
def open_right_trapezoidal(x):
    if x <= 10:
        return 0.0
    elif x > 10 and x <= 20:
        return (x - 10) /  10
    else:
            return 1.0

# Fuzzy sets for distance
distance_close = []
distance_far = []

input_distance1 = float(input("Enter the distance from sensor 1: "))
input_distance2 = float(input("Enter the distance from sensor 2: "))

# if(input_distance1<=5 and input_distance2<=5):
#     print("The robot will definitely collide")
#     exit()

for i in distance_universe: 
    distance_close.append(open_left_trapezoidal(i))
    distance_far.append(open_right_trapezoidal(i))

# Fuzzy sets for steering
steering_hard_left = np.exp((-((steering_universe - 0) / 16.677) ** 2)/2)
steering_straight = np.exp((-((steering_universe - 50) / 16.677) ** 2)/2)
steering_hard_right = np.exp((-((steering_universe - 100) / 16.67) ** 2)/2)

# Visualize the membership functions
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.plot(distance_universe, distance_close, label='Close')
plt.plot(distance_universe, distance_far, label='Far')
plt.title('Distance Membership Functions Sensor One')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(distance_universe, distance_close, label='Close')
plt.plot(distance_universe, distance_far, label='Far')
plt.title('Distance Membership Functions Sensor 2')
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(steering_universe, steering_hard_left, label='Hard Left')
plt.plot(steering_universe, steering_straight, label='Straight')
plt.plot(steering_universe, steering_hard_right, label='Hard Right')
plt.title('Steering Membership Functions')
plt.legend()

plt.show()

#Rule 1 Plot

# Visualize the inputs on the antecedent fuzzy sets
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.plot(distance_universe, distance_close, label='Close')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(distance_universe, distance_close, label='Close')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(steering_universe, steering_hard_left, label='Left')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.show()

#Defuzz Calculation for Rule 1
rule1 = 0
mini = min(open_left_trapezoidal(input_distance1), open_left_trapezoidal(input_distance2))
for i in range(len(steering_universe)):
    if(steering_hard_left[i] > mini):
        rule1 += steering_universe[i]*mini
    else:
        rule1 += steering_universe[i]*steering_hard_left[i]

area1 = 0
for i in range(len(steering_hard_left)):
    if(steering_hard_left[i] >= mini):
        area1+=mini
    else:
        area1+=steering_hard_left[i]


#Rule 2 Plot
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.plot(distance_universe, distance_far, label='Far')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(distance_universe, distance_far, label='Far')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(steering_universe, steering_straight, label='Straight')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.show()

#Defuzz Calculation for Rule 2
rule2 = 0
mini = min(open_right_trapezoidal(input_distance1), open_right_trapezoidal(input_distance2))
for i in range(len(steering_universe)):
    if(steering_straight[i] > mini):
        rule2 += steering_universe[i]*mini
    else:
        rule2 += steering_universe[i]*steering_straight[i]
print(rule1)
area2 = 0
for i in range(len(steering_straight)):
    if(steering_straight[i] >= mini):
        area2+=mini
    else:
        area2+=steering_straight[i]


# Rule 3 Plot 
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.plot(distance_universe, distance_close, label='Close')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(distance_universe, distance_far, label='Far')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(steering_universe, steering_hard_right, label='Right')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

print(steering_hard_right)
plt.show()

#Defuzz Calculation for Rule 3
rule3 = 0
mini = min(open_left_trapezoidal(input_distance1), open_right_trapezoidal(input_distance2))
for i in range(len(steering_universe)):
    if(steering_hard_right[i] > mini):
        rule3 += steering_universe[i]*mini
    else:
        rule3 += steering_universe[i]*steering_hard_right[i]

area3 = 0
for i in range(len(steering_hard_right)):
    if(steering_hard_right[i] >= mini):
        area3+=mini
    else:
        area3+=steering_hard_right[i]


# Rule 4 Plot
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.plot(distance_universe, distance_far, label='Far')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(distance_universe, distance_close, label='Close')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(steering_universe, steering_hard_left, label='Left')
plt.title('Distance Membership Functions with Inputs')
plt.legend()

plt.show()

#Defuzz Calculation for Rule 4
rule4 = 0
mini = min(open_right_trapezoidal(input_distance1), open_left_trapezoidal(input_distance2))
for i in range(len(steering_universe)):
    if(steering_hard_left[i] > mini):
        rule4 += steering_universe[i]*mini
    else:
        rule4 += steering_universe[i]*steering_hard_left[i]
    
area4 = 0
for i in range(len(steering_hard_left)):
    if(steering_hard_left[i] >= mini):
        area4+=mini
    else:
        area4+=steering_hard_left[i]


#Overall Defuzzification
if(input_distance1>50 or input_distance2>50):
    print("Invalid: Input", "Out of Range")
    exit()
else:
    if(area1 != 0 and area4 != 0):
        defuzz = (rule2+ rule3 + rule4)/(area1 + area2 + area3)
    elif(area1==0 and area4!=0):
        defuzz = (rule2+ rule3 + rule4)/(area2 + area3 + area4)
    elif(area1!=0 and area4==0):
        defuzz = (rule2+ rule3 + rule1)/(area1 + area3 + area2)
    else:
        defuzz = (rule1 + rule2 + rule3 + rule4)/(area1 + area2 + area3 + area4)
    print("Defuzzication Output", defuzz) 

y1 = 0

if(input_distance1 <= 10):
    y1 = open_left_trapezoidal(input_distance1)
elif(input_distance1 > 10 and input_distance1<=20):
    y1 = min(open_left_trapezoidal(input_distance1), open_right_trapezoidal(input_distance1))
else:
    y1 = open_right_trapezoidal(input_distance1)
plt.subplot(1, 3, 1)
plt.plot(distance_universe, distance_close, label='Close')
plt.plot(distance_universe, distance_far, label='Far')
plt.scatter(input_distance1, y1, color='r', label='Input Sensor 1')
plt.legend()

y2 = 0
if(input_distance2 <= 10):
    y2 = open_left_trapezoidal(input_distance2)
elif(input_distance2 > 10 and input_distance2<20):
    y2 = min(open_left_trapezoidal(input_distance2), open_right_trapezoidal(input_distance2))
else:
    y2 = open_right_trapezoidal(input_distance2)
plt.subplot(1, 3, 2)
plt.plot(distance_universe, distance_close, label='Close')
plt.plot(distance_universe, distance_far, label='Far')
plt.scatter(input_distance2, y2, color='g', label='Input Sensor 2')
plt.legend()

plt.subplot(1, 3, 3)
if(area1!=0 or area4!=0):
    lst=[]
    mini = min(open_right_trapezoidal(input_distance1), open_left_trapezoidal(input_distance2))
    plt.plot(steering_universe, steering_hard_left, label='Left')
    for i in range(len(steering_universe)):
        if(steering_hard_left[i] > mini):
            lst.append(mini)
        else:
            lst.append(steering_hard_left[i])
    plt.plot(steering_universe, lst, c='black')
if(area2!=0):
    lst = []
    plt.plot(steering_universe, steering_straight, label='Straight')
    mini = min(open_right_trapezoidal(input_distance1), open_right_trapezoidal(input_distance2))
    for i in range(len(steering_universe)):
        if(steering_straight[i] > mini):
            lst.append(mini)
        else:
            lst.append(steering_straight[i])
    plt.plot(steering_universe, lst, c='black')
if(area3!=0):
    lst = []
    mini = min(open_left_trapezoidal(input_distance1), open_right_trapezoidal(input_distance2))
    plt.plot(steering_universe, steering_hard_right, label='Right')
    for i in range(len(steering_universe)):
        if(steering_hard_right[i] > mini):
            lst.append(mini)
        else:
            lst.append(steering_hard_right[i])
    plt.plot(steering_universe, lst, c='black') 

# 

plt.legend()

plt.show()

X, Y = np.meshgrid(distance_universe, distance_universe)

# Calculate the Z values for the 3D plot
Z = np.zeros(X.shape)
for i in range(len(distance_universe)-1):
    for j in range(len(distance_universe)-1):
        rule1 = 0
        mini = min(open_left_trapezoidal(i), open_left_trapezoidal(j))
        for x in range(len(steering_universe)):
            if(steering_hard_left[x] > mini):
                rule1 += steering_universe[x]*mini
            else:
                rule1 += steering_universe[x]*steering_hard_left[x]
        area1 = 0
        for x in range(len(steering_hard_left)):
            if(steering_hard_left[x] >= mini):
                area1+=mini
            else:
                area1+=steering_hard_left[x]

        rule2 = 0
        mini = min(open_right_trapezoidal(i), open_right_trapezoidal(j))
        for x in range(len(steering_universe)):
            if(steering_straight[x] > mini):
                rule2 += steering_universe[x]*mini
            else:
                rule2 += steering_universe[x]*steering_straight[x]
        area2 = 0
        for x in range(len(steering_straight)):
            if(steering_straight[x] >= mini):
                area2+=mini
            else:
                area2+=steering_straight[x]

        rule3 = 0
        mini = min(open_left_trapezoidal(i), open_right_trapezoidal(j))
        for x in range(len(steering_universe)):
            if(steering_hard_right[x] > mini):
                rule3 += steering_universe[x]*mini
            else:
                rule3 += steering_universe[x]*steering_hard_right[x]
        area3 = 0
        for x in range(len(steering_hard_right)):
            if(steering_hard_right[x] >= mini):
                area3+=mini
            else:
                area3+=steering_hard_right[x]

        rule4 = 0
        mini = min(open_right_trapezoidal(i), open_left_trapezoidal(j))
        for x in range(len(steering_universe)):
            if(steering_hard_left[x] > mini):
                rule4 += steering_universe[x]*mini
            else:
                rule4 += steering_universe[x]*steering_hard_left[x]
        area4 = 0
        for x in range(len(steering_hard_left)):
            if(steering_hard_left[x] >= mini):
                area4+=mini
            else:
                area4+=steering_hard_left[x]
        
        Z[i][j] = (rule1 + rule2 + rule3 + rule4)/(area1 + area2 + area3 + area4)
        

# Create mini 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('Distance')
ax.set_ylabel('Distance')
ax.set_zlabel('Steering')

plt.show()