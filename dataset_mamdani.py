import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt
import math
import pandas as pd
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


dataset = pd.read_csv('emergency_dataset.csv')
bt = dataset['Temperature']
head = dataset['Headache']
age_p = dataset['Age']
de = []
for i in range(len(bt)):
# Taking Interval Inputs - Give lower and upper bound
    bt_input = bt[i]
    head_input = head[i]
    age_input = age_p[i]
    bt_input = math.ceil((bt_input-30)*10)

    # Defining Universe 
    body_temp = np.linspace(30, 41, 111)
    headache = np.linspace(0, 10, 11)
    age = np.linspace(0, 130, 131)
    urgency = np.linspace(0, 100, 101)

    # Body Temperature Membership Functions
    body_temp_hypothermia = np.exp((-((body_temp - 30) / 1.7) ** 2)/2).round(3)
    body_temp_normal = np.exp((-((body_temp - 36) / 0.5) ** 2)/2)
    body_temp_elevated = np.exp((-((body_temp - 37.5) / 0.5) ** 2)/2)
    body_temp_high = np.exp((-((body_temp - 41) / 1.2) ** 2)/2)

    # Urgency Membership Functions for Mamdani
    urgency_none = np.exp((-((urgency - 0) / 16.677) ** 2)/2)
    urgency_moderate = np.exp((-((urgency - 50) / 16.677) ** 2)/2)
    urgency_extreme = np.exp((-((urgency - 100) / 16.677) ** 2)/2)


    out_mem = [0]*len(urgency)
    # Updating the output aggregation for each rule
    def out_mem_update(uni, uni_mem, mini):
        for i in range(len(uni)):
            if(uni_mem[i] > mini):
                if(out_mem[i]<=mini):
                    out_mem[i] = mini
            else:
                if(out_mem[i]<=uni_mem[i]):
                    out_mem[i]=uni_mem[i]

    # for headache -> 3, 5
    # for age -> 30, 40
    def open_left_trapezoidal(x, a, b):
        if x<=a:
            return 1.0
        elif x>a and x<=b:
            return (b-x)/(b-a)
        else:
            return 0.0

    # for headache -> 5, 7
    # for age -> 80, 100
    def open_right_trapezoidal(x, a, b):
        if x<=a:
            return 0.0
        elif x>a and x<=b:
            return (x-a)/(b-a)
        else:
            return 1.0

    # for headache -> 3, 5, 7
    # for age -> 30, 55, 80
    def triangle(x, a, b, c):
        if x<a or x>=c:
            return 0.0
        elif x>=a and x<b:
            return (x-a)/(b-a)
        elif x>=b and x<c:
            return (c-x)/(c-b)
        
    # Headache Membership Functions
    headache_low = [open_left_trapezoidal(x, 3, 5) for x in headache]
    headache_moderate = [triangle(x, 3, 5, 7) for x in headache]
    headache_severe = [open_right_trapezoidal(x, 5, 7) for x in headache]

    # Age Membership Functions
    age_young = [open_left_trapezoidal(x, 25, 40) for x in age]
    age_midlife = np.exp((-((age - 55) / 9) ** 2)/2)
    print(age_midlife)
    age_old = [open_right_trapezoidal(x, 70, 100) for x in age]

    # print(headache_moderate)

    # Rules Inference calculations for aggregated output membership

    #Rule1
    mini = min(triangle(head_input, 3, 5, 7), open_right_trapezoidal(age_input, 70, 100))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule2
    mini = min(open_right_trapezoidal(head_input, 5, 7), open_right_trapezoidal(age_input, 70, 100))
    out_mem_update(urgency, urgency_extreme, mini)

    #Rule 3
    mini = body_temp_hypothermia[bt_input]
    out_mem_update(urgency, urgency_extreme, mini)

    #Rule4
    mini = min(body_temp_high[bt_input], open_right_trapezoidal(age_input, 70, 100))
    out_mem_update(urgency, urgency_extreme, mini)

    #Rule5
    mini = min(body_temp_normal[bt_input], min(open_right_trapezoidal(age_input, 70, 100),open_left_trapezoidal(head_input, 3, 5)))
    out_mem_update(urgency, urgency_none, mini)

    #Rule6
    mini = min(body_temp_elevated[bt_input], open_right_trapezoidal(age_input, 70, 100))
    out_mem_update(urgency, urgency_moderate, mini)


    #Rule7
    mini = min(body_temp_normal[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_left_trapezoidal(head_input, 3, 5)))
    out_mem_update(urgency, urgency_none, mini)

    #Rule8
    mini = min(body_temp_normal[bt_input], min(open_left_trapezoidal(age_input, 25, 40), triangle(head_input, 3, 5, 7)))
    out_mem_update(urgency, urgency_none, mini)

    #Rule9
    mini = min(body_temp_normal[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_right_trapezoidal(head_input, 5, 7)))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule10
    mini = min(body_temp_elevated[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_left_trapezoidal(head_input, 3, 5)))
    out_mem_update(urgency, urgency_none, mini)

    #Rule11
    mini = min(body_temp_elevated[bt_input], min(open_left_trapezoidal(age_input, 25, 40),triangle(head_input, 3, 5, 7)))
    out_mem_update(urgency, urgency_none, mini)

    #Rule12
    mini = min(body_temp_elevated[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_right_trapezoidal(head_input, 5, 7)))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule13
    mini = min(body_temp_high[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_left_trapezoidal(head_input, 3, 5)))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule14

    mini = min(body_temp_high[bt_input], min(open_left_trapezoidal(age_input, 25, 40),triangle(head_input, 3, 5, 7)))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule15
    mini = min(body_temp_high[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_right_trapezoidal(head_input, 5, 7)))
    out_mem_update(urgency, urgency_extreme, mini)

    #Rule16
    mini = min(body_temp_normal[bt_input], min(age_midlife[age_input],open_left_trapezoidal(head_input, 3, 5)))
    out_mem_update(urgency, urgency_none, mini)

    #Rule17
    mini = min(body_temp_normal[bt_input], min((age_midlife[age_input]),triangle(head_input, 3, 5, 7)))
    out_mem_update(urgency, urgency_none, mini)


    #Rule18
    mini = min(body_temp_normal[bt_input], min((age_midlife[age_input]),open_right_trapezoidal(head_input, 5, 7)))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule19
    mini = min(body_temp_elevated[bt_input], min((age_midlife[age_input]),open_left_trapezoidal(head_input, 3, 5)))
    out_mem_update(urgency, urgency_none, mini)

    #Rule20
    mini = min(body_temp_elevated[bt_input], min((age_midlife[age_input]),triangle(head_input, 3, 5, 7)))
    out_mem_update(urgency, urgency_none, mini)

    #Rule21
    mini = min(body_temp_elevated[bt_input], min((age_midlife[age_input]), open_right_trapezoidal(head_input, 5, 7)))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule22
    mini = min(body_temp_high[bt_input], min((age_midlife[age_input]), open_left_trapezoidal(head_input, 3, 5)))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule23
    mini = min(body_temp_high[bt_input], min((age_midlife[age_input]),triangle(head_input, 3, 5, 7)))
    out_mem_update(urgency, urgency_moderate, mini)

    #Rule24
    mini = min(body_temp_high[bt_input], min((age_midlife[age_input]),open_right_trapezoidal(head_input, 5, 7)))
    out_mem_update(urgency, urgency_extreme, mini)

    # Centroid Defuzzification
    sum_tot = 0
    for i in range(len(urgency)):
        sum_tot += urgency[i]*out_mem[i]

    defuzz = sum_tot/sum(out_mem)
    print("Centroid Defuzzification", defuzz)

    #First, Mean , Last, Middle of Maxima
    maxima = []
    maximum = max(out_mem)
    for i in range(len(urgency)):
        if(out_mem[i] == maximum):
            maxima.append(i)

    mom_defuzz = sum(maxima)/len(maxima)
    print("Mean of Maxima:", mom_defuzz)

    fom_defuzz = maxima[0]
    lom_defuzz = maxima[-1]
    print("First of Maxima:", fom_defuzz)
    print("Last of Maxima:", lom_defuzz)
    print("Middle of Maxima", (fom_defuzz+lom_defuzz)/2)

    # Centre of Largest Area Defuzzification
    # numerator = 0
    # denominator = 0
    # minima = min(out_mem)
    # counter = 0
    # for i in range(len(urgency)):
    #     if out_mem[i] <= minima:
    #         counter += 1
    #     else:
    #         numerator += out_mem[i]*urgency[i]
    #         denominator += out_mem[i]
        
    #     if(counter == 2):
    #         break

    # print("Center of Largest Area Defuzzification", numerator/denominator)

    #Linguistic Defuzzification
    d = round(defuzz)
    un = urgency_none[d-1]
    um = urgency_moderate[d-1]
    ue = urgency_extreme[d-1]

    maxi = max(un, max(um, ue))
    if(un==maxi):
        print("The case is not urgent")
    elif(um == maxi):
        print("Someone should be with the patient all the time")
    elif(ue == maxi):
        print("The case is extreme and patient must be taken to hospital asap")

    de.append(defuzz)

    print(len(de))

dataset['Defuzzification'] = de
dataset.to_csv('emergency_dataset.csv', index=False)