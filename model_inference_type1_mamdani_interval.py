# Made By - 
# Aditya Purswani - Student ID -> 20596344
# Anasuya Dutta - Student ID -> 20594248

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

# Taking Interval Inputs - Give lower and upper bound
bt = list(map(float, input("Enter a Float Range of body_temp:").split()))
headache_inp = list(map(int, input("Enter a Int Range of headache:").split()))
age_inp = list(map(int, input("Enter a Int Range of age:").split()))

if(bt[0]<30 or bt[1]>41 or bt[1]<bt[0]):
    exit()
if(headache_inp[0]<0 or headache_inp[1]>10 or headache_inp[1]<headache_inp[0]):
    exit()
if(age_inp[0]<0 or age_inp[1]>130 or age_inp[1]<age_inp[0]):
    exit()
bt_low = math.ceil((bt[0]-30)*10)
bt_high = math.ceil((bt[1]-30)*10)

# Defining all elements in inputs in a list
lst_bt = np.arange(bt[0], bt[1]+0.1, 0.1)
lst_ha = np.arange(headache_inp[0], headache_inp[1]+0.1, 0.1)
lst_age = [x for x in range(age_inp[0], age_inp[1]+1)]

# Defining Universe
body_temp = np.linspace(30, 41, 111)
headache = np.linspace(0, 10, 101)
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
age_old = [open_right_trapezoidal(x, 70, 100) for x in age]

# Membership Functions for input range
def gaussian_bt(bt_input):
    mean = (bt_input[1] + bt_input[0])/2
    sd = np.abs(bt_input[1] - bt_input[0]) / (2 * 2.58) #99% confidence interval

    return np.exp((-((body_temp - mean) / sd) ** 2)/2)

def gaussian_headache(headache_inp):
    mean = (headache_inp[1] + headache_inp[0])/2
    sd = np.abs(headache_inp[1] - headache_inp[0]) / (2 * 2.58) #99% confidence interval
    return np.exp((-((headache - mean) / sd) ** 2)/2)

def gaussian_age(age_inp):
    mean = (age_inp[1] + age_inp[0])/2
    sd = np.abs(age_inp[1] - age_inp[0]) / (2 * 2.58) #99% confidence interval
    return np.exp((-((age - mean) / sd) ** 2)/2)

# Calculation for taking the centroid out
def get_centroid(lst1, lst2):
    centroid = 0
    area = 0
    for i in range(len(lst1)):
        centroid += lst1[i]*lst2[i]
    # print(centroid)
    for i in range(len(lst1)):
        area += lst1[i]
    if (area == 0):
        return -1
    return centroid/area

# Intersection function to calculate intersection area between input and antecedents
def intersection(lst1, lst2):
    mini = []
    for i in range(len(lst2)):
        if(lst1[i]>lst2[i]):
            mini.append(lst2[i])
        else:
            mini.append(lst1[i])
    return mini

# Intersection Outputs Centroids
print(len(gaussian_bt(bt)))
print(len(body_temp_hypothermia))
bt_hypo = get_centroid(intersection(gaussian_bt(bt), body_temp_hypothermia), body_temp)
if bt_hypo == -1: bt_hypo = (bt[0]+bt[1])/2
bt_normal = get_centroid(intersection(gaussian_bt(bt), body_temp_normal), body_temp)
if bt_normal == -1: bt_normal = (bt[0]+bt[1])/2
bt_elev = get_centroid(intersection(gaussian_bt(bt), body_temp_elevated), body_temp)
if bt_elev == -1: bt_elev = (bt[0]+bt[1])/2
bt_fever = get_centroid(intersection(gaussian_bt(bt), body_temp_high), body_temp)
if bt_fever == -1: bt_fever = (bt[0]+bt[1])/2

head_low = round(get_centroid(intersection(gaussian_headache(headache_inp), headache_low), headache), 1)
if head_low == -1: head_low = (headache_inp[0]+headache_inp[1])/2
head_mod = round(get_centroid(intersection(gaussian_headache(headache_inp), headache_moderate), headache), 1)
if head_mod == -1: head_mod = (headache_inp[0]+headache_inp[1])/2
head_sev = round(get_centroid(intersection(gaussian_headache(headache_inp), headache_severe), headache), 1)
if head_sev == -1: head_sev = (headache_inp[0]+headache_inp[1])/2

age_y = round(get_centroid(intersection(gaussian_age(age_inp), age_young), age))
if age_y == -1: age_y = (age_inp[0]+age_inp[1])//2
age_m = round(get_centroid(intersection(gaussian_age(age_inp), age_midlife), age))
if age_m == -1: age_m = (age_inp[0]+age_inp[1])//2
age_o = round(get_centroid(intersection(gaussian_age(age_inp), age_old), age))
if age_o == -1: age_o = (age_inp[0]+age_inp[1])//2
# print(headache_moderate)

# Plot showing all antecedents and consequents
plt.figure(figsize=(12, 4))
plt.subplot(1, 4, 1)
plt.plot(body_temp, body_temp_hypothermia, label='Frost Bite')
plt.plot(body_temp, body_temp_normal, label='Normal Temp')
plt.plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
plt.plot(body_temp, body_temp_high, label='High Fever')
plt.title('Body Temperature')
plt.legend()

plt.subplot(1, 4, 2)
plt.plot(headache, headache_low, label='Low')
plt.plot(headache, headache_moderate, label='Moderate')
plt.plot(headache, headache_severe, label='Severe')
plt.title('Severity of Headache')
plt.legend()

plt.subplot(1, 4, 3)
plt.plot(age, age_young, label='Young')
plt.plot(age, age_midlife, label='Midlife')
plt.plot(age, age_old, label='Old')
plt.title('Age of People')
plt.legend()

plt.subplot(1, 4, 4)
plt.plot(urgency, urgency_none, label='None')
plt.plot(urgency, urgency_moderate, label='Urgent')
plt.plot(urgency, urgency_extreme, label='Priority')
plt.title('Urgency of Case')
plt.legend()


plt.show()

# Plot showing all antecedents and consequents with input ranges
plt.figure(figsize=(12, 4))
plt.subplot(1, 4, 1)
plt.plot(body_temp, body_temp_hypothermia, label='Frost Bite')
plt.plot(body_temp, body_temp_normal, label='Normal Temp')
plt.plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
plt.plot(body_temp, body_temp_high, label='High Fever')
plt.plot(body_temp, gaussian_bt(bt), label='Input', color='black')
plt.title('Body Temperature')
plt.legend()

plt.subplot(1, 4, 2)
plt.plot(headache, headache_low, label='Low')
plt.plot(headache, headache_moderate, label='Moderate')
plt.plot(headache, headache_severe, label='Severe')
plt.plot(headache, gaussian_headache(headache_inp), label='Input', color='black')
plt.title('Severity of Headache')
plt.legend()

plt.subplot(1, 4, 3)
plt.plot(age, age_young, label='Young')
plt.plot(age, age_midlife, label='Midlife')
plt.plot(age, age_old, label='Old')
plt.plot(age, gaussian_age(age_inp), label='Input', color='black')
plt.title('Age of People')
plt.legend()

plt.subplot(1, 4, 4)
plt.plot(urgency, urgency_none, label='None')
plt.plot(urgency, urgency_moderate, label='Urgent')
plt.plot(urgency, urgency_extreme, label='Priority')
plt.title('Urgency of Case')
plt.legend()


plt.show()

# Rules Inference and calculations for aggregated output membership
#Rule1
mini = min(triangle(head_mod, 3, 5, 7), open_right_trapezoidal(age_o, 70, 100))
out_mem_update(urgency, urgency_moderate, mini)

#Rule2
mini = min(open_right_trapezoidal(head_sev, 5, 7), open_right_trapezoidal(age_o, 70, 100))
out_mem_update(urgency, urgency_extreme, mini)

#Rule 3
mini = body_temp_hypothermia[math.ceil(bt_hypo-30)*10]
out_mem_update(urgency, urgency_extreme, mini)

#Rule4
mini = min(body_temp_high[math.ceil(bt_fever-30)*10], open_right_trapezoidal(age_o, 70, 100))
out_mem_update(urgency, urgency_extreme, mini)

#Rule5
mini = min(body_temp_normal[math.ceil(bt_normal-30)*10], min(open_right_trapezoidal(age_o, 70, 100),open_left_trapezoidal(head_low, 3, 5)))
out_mem_update(urgency, urgency_none, mini)

#Rule6
mini = min(body_temp_elevated[math.ceil(bt_elev-30)*10], open_right_trapezoidal(age_o, 70, 100))
out_mem_update(urgency, urgency_moderate, mini)

#Rule7
mini = min(body_temp_normal[math.ceil(bt_normal-30)*10], min(open_left_trapezoidal(age_y, 25, 40),open_left_trapezoidal(head_low, 3, 5)))
out_mem_update(urgency, urgency_none, mini)

#Rule8
mini = min(body_temp_normal[math.ceil(bt_normal-30)*10], min(open_left_trapezoidal(age_y, 25, 40), triangle(head_mod, 3, 5, 7)))
out_mem_update(urgency, urgency_none, mini)

#Rule9
mini = min(body_temp_normal[math.ceil(bt_normal-30)*10], min(open_left_trapezoidal(age_y, 25, 40),open_right_trapezoidal(head_sev, 5, 7)))
out_mem_update(urgency, urgency_moderate, mini)

#Rule10
mini = min(body_temp_elevated[math.ceil(bt_elev-30)*10], min(open_left_trapezoidal(age_y, 25, 40),open_left_trapezoidal(head_low, 3, 5)))
out_mem_update(urgency, urgency_none, mini)

#Rule11
mini = min(body_temp_elevated[math.ceil(bt_elev-30)*10], min(open_left_trapezoidal(age_y, 25, 40),triangle(head_mod, 3, 5, 7)))
out_mem_update(urgency, urgency_none, mini)

#Rule12
mini = min(body_temp_elevated[math.ceil(bt_elev-30)*10], min(open_left_trapezoidal(age_y, 25, 40),open_right_trapezoidal(head_sev, 5, 7)))
out_mem_update(urgency, urgency_moderate, mini)

#Rule13
mini = min(body_temp_high[math.ceil(bt_fever-30)*10], min(open_left_trapezoidal(age_y, 25, 40),open_left_trapezoidal(head_low, 3, 5)))
out_mem_update(urgency, urgency_moderate, mini)

#Rule14

mini = min(body_temp_high[math.ceil(bt_fever-30)*10], min(open_left_trapezoidal(age_y, 25, 40),triangle(head_mod, 3, 5, 7)))
out_mem_update(urgency, urgency_moderate, mini)

#Rule15
mini = min(body_temp_high[math.ceil(bt_fever-30)*10], min(open_left_trapezoidal(age_y, 25, 40),open_right_trapezoidal(head_sev, 5, 7)))
out_mem_update(urgency, urgency_extreme, mini)

#Rule16
mini = min(body_temp_normal[math.ceil(bt_normal-30)*10], min((age_midlife[age_m]),open_left_trapezoidal(head_low, 3, 5)))
out_mem_update(urgency, urgency_none, mini)

#Rule17
mini = min(body_temp_normal[math.ceil(bt_normal-30)*10], min((age_midlife[age_m]),triangle(head_mod, 3, 5, 7)))
out_mem_update(urgency, urgency_none, mini)

#Rule18
mini = min(body_temp_normal[math.ceil(bt_normal-30)*10], min((age_midlife[age_m]),open_right_trapezoidal(head_sev, 5, 7)))
out_mem_update(urgency, urgency_moderate, mini)

#Rule19
mini = min(body_temp_elevated[math.ceil(bt_elev-30)*10], min((age_midlife[age_m]),open_left_trapezoidal(head_low, 3, 5)))
out_mem_update(urgency, urgency_none, mini)

#Rule20
mini = min(body_temp_elevated[math.ceil(bt_elev-30)*10], min((age_midlife[age_m]),triangle(head_mod, 3, 5, 7)))
out_mem_update(urgency, urgency_none, mini)

#Rule21
mini = min(body_temp_elevated[math.ceil(bt_elev-30)*10], min((age_midlife[age_m]), open_right_trapezoidal(head_sev, 5, 7)))
out_mem_update(urgency, urgency_moderate, mini)

#Rule22
mini = min(body_temp_high[math.ceil(bt_fever-30)*10], min((age_midlife[age_m]), open_left_trapezoidal(head_low, 3, 5)))
out_mem_update(urgency, urgency_moderate, mini)

#Rule23
mini = min(body_temp_high[math.ceil(bt_fever-30)*10], min((age_midlife[age_m]),triangle(head_mod, 3, 5, 7)))
out_mem_update(urgency, urgency_moderate, mini)

#Rule24
mini = min(body_temp_high[math.ceil(bt_fever-30)*10], min((age_midlife[age_m]),open_right_trapezoidal(head_sev, 5, 7)))
out_mem_update(urgency, urgency_extreme, mini)

# Centroid Defuzzification
sum_tot = 0
for i in range(len(urgency)):
    sum_tot += urgency[i]*out_mem[i]

defuzz = sum_tot/sum(out_mem)
print("Centroid Defuzzification", defuzz)

#First, Mean, Last, Middle of Maxima
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

# Centre of Largest Area Defuzz
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

# Plot for Rules
class ScrollableWindow(QtWidgets.QMainWindow):
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])
        self.windowSize = (1200, 1600)
        self.posXY = (200, 40)
        QtWidgets.QMainWindow.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.setGeometry(*self.posXY, *self.windowSize)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0, 0, 0, 0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        self.show()
        exit(self.qapp.exec_())

# Rules Plot and Output Plot
fig, axs = plt.subplots(25, 4, figsize=(12, 40))
# fig.update_layout( title='title', autosize=True, height=2000 ) 
# fig.update_xaxes(rangeslider=dict(visible=False)) 
# fig.show()
fig.suptitle("Rules For The Application")
axs[0, 0].set_title('Body Temperature')
axs[0, 1].plot(headache, headache_moderate, label='Moderate')
axs[0, 1].set_title('Severity of Headache')
axs[0, 1].legend()
axs[0, 2].plot(age, age_old, label='Old')
axs[0, 2].set_title('Age of People')
axs[0, 2].legend()
axs[0, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[0, 3].set_title('Urgency of Case')
axs[0, 3].legend()

axs[1, 1].plot(headache, headache_severe, label='Severe')
axs[1, 1].legend()
axs[1, 2].plot(age, age_old, label='Old')
axs[1, 2].legend()
axs[1, 3].plot(urgency, urgency_extreme, label='Priority', color='r')
axs[1, 3].legend()

axs[2, 0].plot(body_temp, body_temp_hypothermia, label='Frost Bite')
axs[2, 0].legend()
axs[2, 3].plot(urgency, urgency_extreme, label='Priority', color='r')
axs[2, 3].legend()

axs[3, 0].plot(body_temp, body_temp_high, label='High Fever')
axs[3, 0].legend()
axs[3, 2].plot(age, age_old, label='Old')
axs[3, 2].legend()
axs[3, 3].plot(urgency, urgency_extreme, label='Priority', color='r')
axs[3, 3].legend()

axs[4, 0].plot(body_temp, body_temp_normal, label='Normal Temp')
axs[4, 0].legend()
axs[4, 1].plot(headache, headache_low, label='Low')
axs[4, 1].legend()
axs[4, 2].plot(age, age_old, label='Old')
axs[4, 2].legend()
axs[4, 3].plot(urgency, urgency_none, label='None', color='r')
axs[4, 3].legend()

axs[5, 0].plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
axs[5, 0].legend()
axs[5, 2].plot(age, age_old, label='Old')
axs[5, 2].legend()
axs[5, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[5, 3].legend()

axs[6, 0].plot(body_temp, body_temp_normal, label='Normal Temp')
axs[6, 0].legend()
axs[6, 1].plot(headache, headache_low, label='Low')
axs[6, 1].legend()
axs[6, 2].plot(age, age_young, label='Young')
axs[6, 2].legend()
axs[6, 3].plot(urgency, urgency_none, label='None', color='r')
axs[6, 3].legend()

axs[7, 0].plot(body_temp, body_temp_normal, label='Normal Temp')
axs[7, 0].legend()
axs[7, 1].plot(headache, headache_moderate, label='Moderate')
axs[7, 1].legend()
axs[7, 2].plot(age, age_young, label='Young')
axs[7, 2].legend()
axs[7, 3].plot(urgency, urgency_none, label='None', color='r')
axs[7, 3].legend()

axs[8, 0].plot(body_temp, body_temp_normal, label='Normal Temp')
axs[8, 0].legend()
axs[8, 1].plot(headache, headache_severe, label='Severe')
axs[8, 1].legend()
axs[8, 2].plot(age, age_young, label='Young')
axs[8, 2].legend()
axs[8, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[8, 3].legend()

axs[9, 0].plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
axs[9, 0].legend()
axs[9, 1].plot(headache, headache_low, label='Low')
axs[9, 1].legend()
axs[9, 2].plot(age, age_young, label='Young')
axs[9, 2].legend()
axs[9, 3].plot(urgency, urgency_none, label='None', color='r')
axs[9, 3].legend()

axs[10, 0].plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
axs[10, 0].legend()
axs[10, 1].plot(headache, headache_moderate, label='Moderate')
axs[10, 1].legend()
axs[10, 2].plot(age, age_young, label='Young')
axs[10, 2].legend()
axs[10, 3].plot(urgency, urgency_none, label='None', color='r')
axs[10, 3].legend()

axs[11, 0].plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
axs[11, 0].legend()
axs[11, 1].plot(headache, headache_severe, label='Severe')
axs[11, 1].legend()
axs[11, 2].plot(age, age_young, label='Young')
axs[11, 2].legend()
axs[11, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[11, 3].legend()

axs[12, 0].plot(body_temp, body_temp_high, label='High Fever')
axs[12, 0].legend()
axs[12, 1].plot(headache, headache_low, label='Low')
axs[12, 1].legend()
axs[12, 2].plot(age, age_young, label='Young')
axs[12, 2].legend()
axs[12, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[12, 3].legend()

axs[13, 0].plot(body_temp, body_temp_high, label='High Fever')
axs[13, 0].legend()
axs[13, 1].plot(headache, headache_moderate, label='Moderate')
axs[13, 1].legend()
axs[13, 2].plot(age, age_young, label='Young')
axs[13, 2].legend()
axs[13, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[13, 3].legend()

axs[14, 0].plot(body_temp, body_temp_high, label='High Fever')
axs[14, 0].legend()
axs[14, 1].plot(headache, headache_severe, label='Severe')
axs[14, 1].legend()
axs[14, 2].plot(age, age_young, label='Young')
axs[14, 2].legend()
axs[14, 3].plot(urgency, urgency_extreme, label='Priority', color='r')
axs[14, 3].legend()

axs[15, 0].plot(body_temp, body_temp_normal, label='Normal Temp')
axs[15, 0].legend()
axs[15, 1].plot(headache, headache_low, label='Low')
axs[15, 1].legend()
axs[15, 2].plot(age, age_midlife, label='Midlife')
axs[15, 2].legend()
axs[15, 3].plot(urgency, urgency_none, label='None', color='r')
axs[15, 3].legend()

axs[16, 0].plot(body_temp, body_temp_normal, label='Normal Temp')
axs[16, 0].legend()
axs[16, 1].plot(headache, headache_moderate, label='Moderate')
axs[16, 1].legend()
axs[16, 2].plot(age, age_midlife, label='Midlife')
axs[16, 2].legend()
axs[16, 3].plot(urgency, urgency_none, label='None', color='r')
axs[16, 3].legend()

axs[17, 0].plot(body_temp, body_temp_normal, label='Normal Temp')
axs[17, 0].legend()
axs[17, 1].plot(headache, headache_severe, label='Severe')
axs[17, 1].legend()
axs[17, 2].plot(age, age_midlife, label='Midlife')
axs[17, 2].legend()
axs[17, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[17, 3].legend()

axs[18, 0].plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
axs[18, 0].legend()
axs[18, 1].plot(headache, headache_low, label='Low')
axs[18, 1].legend()
axs[18, 2].plot(age, age_midlife, label='Midlife')
axs[18, 2].legend()
axs[18, 3].plot(urgency, urgency_none, label='None', color='r')
axs[18, 3].legend()

axs[19, 0].plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
axs[19, 0].legend()
axs[19, 1].plot(headache, headache_moderate, label='Moderate')
axs[19, 1].legend()
axs[19, 2].plot(age, age_midlife, label='Midlife')
axs[19, 2].legend()
axs[19, 3].plot(urgency, urgency_none, label='None', color='r')
axs[19, 3].legend()

axs[20, 0].plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
axs[20, 0].legend()
axs[20, 1].plot(headache, headache_severe, label='Severe')
axs[20, 1].legend()
axs[20, 2].plot(age, age_midlife, label='Midlife')
axs[20, 2].legend()
axs[20, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[20, 3].legend()

axs[21, 0].plot(body_temp, body_temp_high, label='High Fever')
axs[21, 0].legend()
axs[21, 1].plot(headache, headache_low, label='Low')
axs[21, 1].legend()
axs[21, 2].plot(age, age_midlife, label='Midlife')
axs[21, 2].legend()
axs[21, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[21, 3].legend()

axs[22, 0].plot(body_temp, body_temp_high, label='High Fever')
axs[22, 0].legend()
axs[22, 1].plot(headache, headache_moderate, label='Moderate')
axs[22, 1].legend()
axs[22, 2].plot(age, age_midlife, label='Midlife')
axs[22, 2].legend()
axs[22, 3].plot(urgency, urgency_moderate, label='Urgent', color='r')
axs[22, 3].legend()

axs[23, 0].plot(body_temp, body_temp_high, label='High Fever')
axs[23, 0].legend()
axs[23, 1].plot(headache, headache_severe, label='Severe')
axs[23, 1].legend()
axs[23, 2].plot(age, age_midlife, label='Midlife')
axs[23, 2].legend()
axs[23, 3].plot(urgency, urgency_extreme, label='Priority', color='r')
axs[23, 3].legend()

axs[24, 3].plot(urgency, out_mem, label='output', color='y')
axs[24, 3].set_ylim(top = 1)
axs[24, 3].legend()


# lst.append(defuzz)
# dataset['Defuzzification'] = lst
# print(dataset)    
a = ScrollableWindow(fig)