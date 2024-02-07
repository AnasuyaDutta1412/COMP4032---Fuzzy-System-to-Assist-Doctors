# Made By - 
# Aditya Purswani - Student ID -> 20596344
# Anasuya Dutta - Student ID -> 20594248

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt
import math
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Taking Interval Inputs - Numeric Values
bt_input = float(input("Enter a Float Integer Value of body_temp:"))
head_input = float(input("Enter a Float Integer Value of headache (within 10):"))
age_input = int(input("Enter a Integer Integer Value of age:"))

#Defining Universe
body_temp = np.linspace(30, 41, 111)
headache = np.linspace(0, 10, 101)
age = np.linspace(0, 130, 131)
urgency = np.linspace(0, 100, 100001)

if(bt_input < 30 or bt_input>41):
    exit()
if(head_input < 0 or head_input>11):
    exit()
if(age_input<0 or age_input>130):
    exit()
# for plot inputs
bt = [0 if x!=bt_input else 1 for x in body_temp]
head = [0 if x!=head_input else 1 for x in headache]
age_person = [0 if x!=age_input else 1 for x in age]

bt_input = math.ceil((bt_input-30)*10)

# Body Temperature Membership Functions
body_temp_hypothermia = np.exp((-((body_temp - 30) / 1.7) ** 2)/2).round(3)
body_temp_normal = np.exp((-((body_temp - 36) / 0.5) ** 2)/2)
body_temp_elevated = np.exp((-((body_temp - 37.5) / 0.5) ** 2)/2)
body_temp_high = np.exp((-((body_temp - 41) / 1.2) ** 2)/2)

# Singleton Value Selection
z1=12.986
z2=50
z3=87.014
# for headache -> 3, 5
# for age -> 25, 35
def open_left_trapezoidal(x, a, b):
    if x<=a:
        return 1.0
    elif x>a and x<=b:
        return (b-x)/(b-a)
    else:
        return 0.0

# for headache -> 5, 7
# for age -> 60, 70
def open_right_trapezoidal(x, a, b):
    if x<=a:
        return 0.0
    elif x>a and x<=b:
        return (x-a)/(b-a)
    else:
        return 1.0

# for headache -> 3, 5, 7
# for age -> 25, 47, 70
def triangle(x, a, b, c):
    if x<a or x>=c:
        return 0.0
    elif x>=a and x<b:
        return (x-a)/(b-a)
    elif x>=b and x<c:
        return (c-x)/(c-b)

def none(x):
    if x!=z1:
        return 0
    else:
        return 1

def moderate(x):
    if x!=z2:
        return 0
    else:
        return 1

def high(x):
    if x!=z3:
        return 0
    else:
        return 1
    
# Urgency Membership Functions for Mamdani
urgency_none = [none(x) for x in urgency]
urgency_moderate = [moderate(x) for x in urgency]
urgency_extreme = [high(x) for x in urgency]

# Headache Membership Functions
headache_low = [open_left_trapezoidal(x, 3, 5) for x in headache]
headache_moderate = [triangle(x, 3, 5, 7) for x in headache]
headache_severe = [open_right_trapezoidal(x, 5, 7) for x in headache]

# Age Membership Functions
age_young = [open_left_trapezoidal(x, 25, 40) for x in age]
age_midlife = np.exp((-((age - 55) / 9) ** 2)/2)
age_old = [open_right_trapezoidal(x, 70, 100) for x in age]



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

# Plot showing all antecedents and consequents with singleton inputs
plt.figure(figsize=(12, 4))
plt.subplot(1, 4, 1)
plt.plot(body_temp, body_temp_hypothermia, label='Frost Bite')
plt.plot(body_temp, body_temp_normal, label='Normal Temp')
plt.plot(body_temp, body_temp_elevated, label='Higher Than Normal Temp')
plt.plot(body_temp, body_temp_high, label='High Fever')
plt.plot(body_temp, bt, label = 'Input', color ='black')
plt.title('Body Temperature')
plt.legend()

plt.subplot(1, 4, 2)
plt.plot(headache, headache_low, label='Low')
plt.plot(headache, headache_moderate, label='Moderate')
plt.plot(headache, headache_severe, label='Severe')
plt.plot(headache, head, label = 'Input', color ='black')
plt.title('Severity of Headache')
plt.legend()

plt.subplot(1, 4, 3)
plt.plot(age, age_young, label='Young')
plt.plot(age, age_midlife, label='Midlife')
plt.plot(age, age_old, label='Old')
plt.plot(age, age_person, label = 'Input', color ='black')
plt.title('Age of People')
plt.legend()

plt.subplot(1, 4, 4)
plt.plot(urgency, urgency_none, label='None')
plt.plot(urgency, urgency_moderate, label='Urgent')
plt.plot(urgency, urgency_extreme, label='Priority')
plt.title('Urgency of Case')
plt.legend()


plt.show()


# Rules Inference and calculations for weighted average

mini = min(triangle(head_input, 3, 5, 7), open_right_trapezoidal(age_input, 70, 100))
rule1 = z2*mini
area1 = mini

mini = min(open_right_trapezoidal(head_input, 5, 7), open_right_trapezoidal(age_input, 70, 100))
rule2 = z3*mini
area1 += mini

mini = body_temp_hypothermia[bt_input]
rule3 = z3*mini
area1 += mini

mini = min(body_temp_high[bt_input], open_right_trapezoidal(age_input, 70, 100))
rule4 = z3*mini
area1 += mini

mini = min(body_temp_normal[bt_input], min(open_right_trapezoidal(age_input, 70, 100),open_left_trapezoidal(head_input, 3, 5)))
rule5 = z1*mini
area1 += mini

mini = min(body_temp_elevated[bt_input], open_right_trapezoidal(age_input, 70, 100))
rule6 = z2*mini
area1 += mini

mini = min(body_temp_normal[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_left_trapezoidal(head_input, 3, 5)))
rule7= z1*mini
area1 += mini

mini = min(body_temp_normal[bt_input], min(open_left_trapezoidal(age_input, 25, 40), triangle(head_input, 3, 5, 7)))
rule8 = z1*mini
area1 += mini

mini = min(body_temp_normal[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_right_trapezoidal(head_input, 5, 7)))
rule9 = z2*mini
area1 += mini

mini = min(body_temp_elevated[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_left_trapezoidal(head_input, 3, 5)))
rule10 = z1*mini
area1 += mini

mini = min(body_temp_elevated[bt_input], min(open_left_trapezoidal(age_input, 25, 40),triangle(head_input, 3, 5, 7)))
rule11 = z1*mini
area1 += mini

mini = min(body_temp_elevated[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_right_trapezoidal(head_input, 5, 7)))
rule12 = z2*mini
area1 += mini

mini = min(body_temp_high[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_left_trapezoidal(head_input, 3, 5)))
rule13 = z2*mini
area1 += mini

mini = min(body_temp_high[bt_input], min(open_left_trapezoidal(age_input, 25, 40),triangle(head_input, 3, 5, 7)))
rule14 = z2*mini
area1 += mini

mini = min(body_temp_high[bt_input], min(open_left_trapezoidal(age_input, 25, 40),open_right_trapezoidal(head_input, 5, 7)))
rule15 = z3*mini
area1 += mini

mini = min(body_temp_normal[bt_input], min(age_midlife[age_input],open_left_trapezoidal(head_input, 3, 5)))
rule16 = z1*mini
area1 += mini

mini = min(body_temp_normal[bt_input], min(age_midlife[age_input],triangle(head_input, 3, 5, 7)))
rule17 = z1*mini
area1 += mini

mini = min(body_temp_normal[bt_input], min(age_midlife[age_input],open_right_trapezoidal(head_input, 5, 7)))
rule18 = z2*mini
area1 += mini

mini = min(body_temp_elevated[bt_input], min(age_midlife[age_input],open_left_trapezoidal(head_input, 3, 5)))
rule19 = z1*mini
area1 += mini

mini = min(body_temp_elevated[bt_input], min(age_midlife[age_input],triangle(head_input, 3, 5, 7)))
rule20 = z1*mini
area1 += mini

mini = min(body_temp_elevated[bt_input], min(age_midlife[age_input], open_right_trapezoidal(head_input, 5, 7)))
rule21 = z2*mini
area1 += mini

mini = min(body_temp_high[bt_input], min(age_midlife[age_input], open_left_trapezoidal(head_input, 3, 5)))
rule22 = z2*mini
area1 += mini

mini = min(body_temp_high[bt_input], min(age_midlife[age_input],triangle(head_input, 3, 5, 7)))
rule23= z2*mini
area1+= mini

mini = min(body_temp_high[bt_input], min(age_midlife[age_input],open_right_trapezoidal(head_input, 5, 7)))
rule24 = z3*mini
area1+= mini

# Weighted Average
defuzz = (rule1+rule2+rule3+rule4+rule5+rule6+rule7+rule8+rule9+rule10+rule11+rule12+rule13+rule14+rule15+rule16+rule17+rule18+rule19+rule20+rule21+rule22+rule23+rule24)/area1
print(defuzz)

# Plot for all Rules
class ScrollableWindow(QtWidgets.QMainWindow):
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])
        self.windowSize = (1200, 1600)
        self.posXY = (200, 40)
        self.font = QFont('Arial', 14)
        QtWidgets.QMainWindow.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.setGeometry(*self.posXY, *self.windowSize)
        self.setFont(self.font)
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

# Rule Plots
fig, axs = plt.subplots(24, 4, figsize=(12, 40))
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

a = ScrollableWindow(fig)