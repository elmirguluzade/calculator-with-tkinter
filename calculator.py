from tkinter import *
import math

# Constants
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
BTN_COLOR = "#FFF"

# Initialize
root = Tk()
root.title("Calculator")
root.geometry("350x450")
root.resizable(True, False)

# !Main Code
totalExp = ""
currentExp = ""
isClicked = False
isEnough = False

# Main Frames
displayFrame = Frame(root, height=200, bg=LIGHT_GRAY)
buttonsFrame = Frame(root, height=250)
displayFrame.pack(expand=True, fill="both")
buttonsFrame.pack(expand=True, fill="both")

# Expression Labels
totalLabel = Label(displayFrame, text=totalExp, anchor=E,
                   padx=24, fg=LABEL_COLOR, bg=LIGHT_GRAY, font=("Arial", 16))
currentLabel = Label(displayFrame, text=currentExp, anchor=E, padx=24,
                     fg=LABEL_COLOR, bg=LIGHT_GRAY, font=("Arial", 40, "bold"))
totalLabel.pack(expand=True, fill="both")
currentLabel.pack(expand=True, fill="both")

# Button dict
digits = {
    7: (1, 1), 8: (1, 2), 9: (1, 3),
    4: (2, 1), 5: (2, 2), 6: (2, 3),
    1: (3, 1), 2: (3, 2), 3: (3, 3),
    0: (4, 2), ".": (4, 1)
}
operators = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
advanced_operators = {"fact": "x!", "pow": "x\u00b2", "sqrt": "\u221ax", "log": "log", "sign": "\u00b1"}

def advancedCalc(oper):
    global currentExp
    result = ''
    if currentExp == "": return
    try:
        if oper == "pow": result = float(currentExp) ** 2
        elif oper == "sqrt":
            if float(currentExp) <= 0:
                currentExp = "Error"
                return
            result = float(currentExp) ** (1/2)
        elif oper == "sign": result = float(currentExp) * -1
        elif oper == "log": result = math.log(float(currentExp), 2)
        elif oper == "fact":
            if int(currentExp) < 0:
                currentExp = "Error"
                updateCurrent()
                return
            currentExp = math.factorial(int(currentExp))
            print(currentExp)
        if result != "":
            tempRes = result
            result = str(result).split(".")
            if result[len(result) - 1] == "0": currentExp = result[0]
            else: currentExp = str(round(float(tempRes), 6))
    except: currentExp = "Error"
    updateCurrent()

# Button functionality
def addExpression(val):
    global currentExp
    if currentExp == "Error":
        currentExp = ""
    currentExp += str(val)
    updateCurrent()

def addOperator(oper):
    global currentExp, totalExp, isClicked, isEnough
    if currentExp == "": return
    currentExp += oper
    if isClicked == True:
        totalExp = ""
    isEnough = False
    totalExp += currentExp
    currentExp = ""
    updateCurrent()
    updateTotal()

def evaluate():
    isValid = False
    global totalExp, currentExp, isClicked, isEnough
    for symbol, _  in operators.items():
        if totalExp[len(totalExp) - 1] == symbol: isValid = True
    if isValid == True:
        totalExp += currentExp
        try:
            currentExp = str(eval(totalExp))
            currentExp = isfloat(currentExp)
        except:
            currentExp = "Error"
        finally:
            isClicked = True
            isEnough = True
            updateCurrent()
            updateTotal()

# Creating button
def digitButtons():
    for digit, grid in digits.items():
        button = Button(buttonsFrame, text=str(digit), bg="#FFF", fg=LABEL_COLOR, font=(
            "Arial", 20, "bold"), borderwidth=0, command=lambda val=digit: addExpression(val))
        button.grid(row=grid[0], column=grid[1], sticky=NSEW)
digitButtons()

# Creating operators
def operatorButtons():
    i = 0
    j = 0
    for operator, symbol in operators.items():
        button = Button(buttonsFrame, text=symbol, bg="#F8FaFF", fg=LABEL_COLOR, font=(
            "Arial", 20), borderwidth=0, command=lambda oper=operator: addOperator(oper))
        button.grid(row=i, column=4, sticky=NSEW)
        i += 1
    for operator, symbol in advanced_operators.items():
        button = Button(buttonsFrame, text=symbol, bg=BTN_COLOR, fg=LABEL_COLOR, font=(
            "Arial", 20), borderwidth=0, command=lambda oper=operator: advancedCalc(oper))
        button.grid(row=j, column=0, sticky=NSEW)
        j += 1
operatorButtons()

# Clear button
def clearAll():
    global currentExp, totalExp, isClicked, isEnough
    currentExp = ""
    totalExp = ""
    isClicked = False
    isEnough = False
    updateCurrent()
    updateTotal()

clearBtn = Button(buttonsFrame, text="C", bg=BTN_COLOR, fg=LABEL_COLOR, font=(
    "Arial", 20), borderwidth=0, command=clearAll)
clearBtn.grid(row=0, column=2, columnspan=2, sticky=NSEW)

# Undo button
def undo():
    global currentExp, totalExp, isEnough
    if currentExp == "Error":
        currentExp = ""
        updateCurrent()
        return
    if (len(totalExp) >= 3 or len(totalExp) == 0) and isEnough == True:
        totalExp = ""
        updateTotal()
    else:
        try:
            currentExp = currentExp[:len(currentExp)-1]
            updateCurrent()
        except: ""

undoBtn = Button(buttonsFrame, text="\u232b", bg=BTN_COLOR,
                 fg=LABEL_COLOR, font=("Arial", 20), borderwidth=0, command=undo)
undoBtn.grid(row=0, column=1, sticky=NSEW)

# Equal button
equalsBtn = Button(buttonsFrame, text="=", bg="#CCEDFF", fg=LABEL_COLOR, font=(
    "Arial", 20), borderwidth=0, command=evaluate)
equalsBtn.grid(row=4, column=3, columnspan=2, sticky=NSEW)

# Managing grid
for x in range(5):
    buttonsFrame.rowconfigure(x, weight=1)
    buttonsFrame.columnconfigure(x, weight=1)

# Updating label values
def updateCurrent():
    global currentExp
    currentLabel.config(text=currentExp)

def updateTotal():
    global totalExp
    expr = totalExp
    for operator, symbol in operators.items():
        expr = expr.replace(operator, f' {symbol} ')
    totalLabel.config(text=expr)

# Error handling
def isfloat(num):
    try:
        result = num.split('.')
        if result[1] == "0":
            return str(int(result[0]))
        else:
            return str(round(float(num), 6))
    except: return num

# !Run
root.mainloop()