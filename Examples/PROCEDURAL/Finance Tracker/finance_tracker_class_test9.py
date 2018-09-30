from tkinter import *
from tkinter import ttk
from datetime import date
import csv
import time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


date = date.today() #Get today's date
date = str(date) #Convert to string
month = date[5:7] #Get the month
year = date[0:4] #Get the year
day = date[8:10]
currentBGDS = True
currentLGDS = False
currentBGMI = False
currentBGPS = False
currentBGSI = False

#Convert numerical month to letterical month
Months = {"01":"January", 
          "02":"February",
          "03":"March",
          "04":"April",
          "05":"May",
          "06":"June",
          "07":"July",
          "08":"August",
          "09":"September",
          "10":"October",
          "11":"November",
          "12":"December"}

MonthsReverse =  {"January":"01", 
                  "February":"02",
                  "March":"03",
                  "April":"04",
                  "May":"05",
                  "June":"06",
                  "July":"07",
                  "August":"08",
                  "September":"09",
                  "October":"10",
                  "November":"11",
                  "December":"12"}

dayInMonths ={"01":31, 
              "02":{0:28,
                 1:29},
              "03":31,
              "04":30,
              "05":31,
              "06":30,
              "07":31,
              "08":31,
              "09":30,
              "10":31,
              "11":30,
              "12":31}

DateOfCurrentExpenses = "MonthlyExpense" + month + year + ".txt"
UsedExpensesFile = "UsedExpenses" + month + year + ".txt"
MonthlyItemsFile = "Items" + month + year + ".csv"
TotalDailyExpenditureFile = "DailyExpenditure" + month + year + ".csv"
Title = "Finance Tracker: " + Months[month] + " " + year
CurrentCurrency = "Currency" + month + year + ".txt"

def ReadMonthlyExpense(fileName):
    with open(fileName,"r") as file:
        monthlyExpense = file.read()
        file.close()
    return monthlyExpense

def ReadUsedExpenses(fileName):
    with open(fileName,"r") as file:
        usedExpenses = file.read()
        file.close()
    return usedExpenses

def ReadTDEF(fileName):
    with open(fileName, "r") as TDEF:
        a = csv.reader(TDEF)
        TDEFlist = list(a)
        TDEF.close()
    return TDEFlist

def WriteTDEF(List):
    with open (TotalDailyExpenditureFile, "w", newline='') as TDEF:
        Save = csv.writer(TDEF)
        Save.writerows(List)
        TDEF.close()
        
def ReadMonthlyItems(fileName):
    with open (fileName, "r") as MIF:
        a = csv.reader(MIF)
        MIFlist = list(a)
        MIF.close()
    return MIFlist

def WriteMonthlyItems(List):
    with open (MonthlyItemsFile, "w", newline='') as MIF:
        Save = csv.writer(MIF)
        Save.writerows(List)
        MIF.close()

def UpperFirsts(s):
    ProperVal = ""
    Skip = True
    ProperVal += s[0].upper()
    Length = len(s)
    for x in range(Length):
        if not Skip:
            ProperVal += s[x]
            if s[x] == " " or s[x] == "/" or s[x] == "-" or s[x] == "_":
                Skip = True
                ProperVal += s[x+1].upper()
        else:
            Skip = False
    return ProperVal

def StringToFloat(List):
    for x in range(len(List)):
        List[x] = float(List[x])
    return List

def maxMessage(List, day):
    print(List[1])
    List[1] = StringToFloat(List[1])
    expensivestIndex = List[1].index(max(List[1]))
    expensivest = List[0][expensivestIndex]
    if day == True:
        expensivestMessage = "The most expensive day \n this month is: "+ "Day " + expensivest +"!"
    else:
        expensivest = UpperFirsts(expensivest)
        expensivestMessage = "The most expensive item you \n bought this month is: "+ expensivest +"!"
    return expensivestMessage

def plotGraph(List, plots, xtitle, ytitle, mainTitle, BGDS, LGDS, BGMI, BGPS, BGSI, barTrue, lineTrue):
    global currentBGDS
    global currentLGDS
    global currentBGMI
    global currentBGPS
    global currentBGSI
    print("behairi")
    print(List[1])
    maxCost = int(max(List[1]))
    remainder = maxCost % 20
    highestYTick = maxCost + (20-remainder)
    increments = int(highestYTick / 20)
    if barTrue == True:
        plots.bar(range(len(List[0])), List[1])
    else:
        plots.plot(range(len(List[0])), List[1])
    plots.set_xticks(range(len(List[0])), minor=False)
    plots.set_xticklabels(List[0], fontdict=None, minor=False)
    if maxCost > 20:
        plots.set_yticks(range(0,highestYTick+1,increments))
    plots.set_xlabel(xtitle)
    plots.set_ylabel(ytitle)
    plots.set_title(mainTitle)
    currentBGDS = BGDS
    currentLGDS = LGDS
    currentBGMI = BGMI
    currentBGPS = BGPS
    currentBGSI = BGSI

def makeGraph(self, BGDS, LGDS, BGMI, BGPS, BGSI, col, rw, rowsp, colsp, TDEfileName, MIfileName, chosenStore):
    graphFigure = Figure(figsize=(10,5), dpi=100)
    dataPlots = graphFigure.add_subplot(111)
    canvas = FigureCanvasTkAgg(graphFigure, self)
##    toolbar = NavigationToolbar2TkAgg(canvas, self)
##    toolbar.update()
##    toolbar.pack()
    canvas.show()
    canvas.get_tk_widget().grid(column=col,row=rw, rowspan=rowsp, columnspan=colsp)

    
    dataPlots.clear()
    if BGDS == True:
        TDEFlist = ReadTDEF(TDEfileName)
        TDEFlist[1] = StringToFloat(TDEFlist[1])
        plotGraph(TDEFlist, dataPlots, "Day", "Expenditure", "Daily Spendings", True, False, False, False, False, True, False)
        return canvas

    elif LGDS == True:
        TDEFlist = ReadTDEF(TDEfileName)
        TDEFlist[1] = StringToFloat(TDEFlist[1])
        plotGraph(TDEFlist, dataPlots, "Day", "Expenditure", "Daily Spendings", False, True, False, False, False, False, True)
        return canvas
        
    elif BGMI == True:
        MIFlist = ReadMonthlyItems(MIfileName)
        itemsList = []
        for x in range(len(MIFlist[0])):
            item = UpperFirsts(MIFlist[0][x])
            itemsList.append(item)
        MIFlist[0] = itemsList
        MIFlist[1] = StringToFloat(MIFlist[1])
        plotGraph(MIFlist, dataPlots, "Items", "Expenditure", "Monthly Spendings per Item", False, False, True, False, False, True, False)
        return canvas

    elif BGPS == True:
        MIFlist = ReadMonthlyItems(MIfileName)
        storeList = [[],[]]
        for x in range(2, len(MIFlist)):
            store = UpperFirsts(MIFlist[x][0])
            storeTotalPrice = MIFlist[x][1]
            storeList[0].append(store)
            storeList[1].append(storeTotalPrice)
        storeList[1] = StringToFloat(storeList[1])
        print(storeList)
        plotGraph(storeList, dataPlots, "Stores", "Expenditure", "Monthly Spendings per Store", False, False, False, True, False, True, False)
        return canvas
        
        

    elif BGSI == True:
        MIFlist = ReadMonthlyItems(MIfileName)
        itemsList = [[],[]]
        for x in range(2,len(MIFlist)):
            if MIFlist[x][0] == chosenStore:
                for y in range(2, len(MIFlist[x]), 2):
                    itemsList[0].append(MIFlist[x][y])
                    itemsList[1].append(MIFlist[x][y+1])
                break
        itemsList[1] = StringToFloat(itemsList[1])
        xtitle = "Items From " + chosenStore
        plotGraph(itemsList, dataPlots, xtitle, "Expenditure", "Monthly Spendings per Store Item", False, False, False, False, True, True, False)
        return canvas



def NewData(itemEntry, storeEntry, costEntry, passController, RElabel, UElabel, EDlabel, EIlabel, self, BGDS, LGDS, BGMI, BGPS, BGSI):
    item = itemEntry.get()
    store = storeEntry.get()
    totalCost = costEntry.get()

    item = item.lower()
    store = store.lower()

    textfile = open(CurrentCurrency, "r")
    currence = textfile.read()
    
    try:
        totalCost = float(totalCost)
        try:
            MIFlist = ReadMonthlyItems(MonthlyItemsFile)
            rows = len(MIFlist)
            if item not in MIFlist[0]:
                MIFlist[0].append(item)
                MIFlist[1].append(totalCost)
                for x in range(rows):
                    if store == MIFlist[x][0]:
                        if item not in MIFlist[x]:
                            MIFlist[x].append(item)
                            MIFlist[x].append(totalCost)
                            MIFlist[x][1] = float(MIFlist[x][1]) + totalCost
                            
                        break
                    else:
                        if x == rows-1:
                            MIFlist.append([store, totalCost, item, totalCost])
                
            else:
                itemIndex = MIFlist[0].index(item)
                for x in range(rows):
                    if store == MIFlist[x][0]:
                        if item not in MIFlist[x]:
                            MIFlist[x].append(item)
                            MIFlist[x].append(totalCost)
                            MIFlist[x][1] = float(MIFlist[x][1]) + totalCost
                        break
                    else:
                        if x == rows-1:
                            MIFlist.append([store, totalCost, item, totalCost])
                MIFlist[1][itemIndex] = float(MIFlist[1][itemIndex]) + totalCost
       
                
                    

            WriteMonthlyItems(MIFlist)

            ######


            TDEFlist = ReadTDEF(TotalDailyExpenditureFile)
            dayIndex = TDEFlist[0].index(str(int(day)))
            TDEFlist[1][dayIndex] = float(TDEFlist[1][dayIndex]) + totalCost                
            WriteTDEF(TDEFlist)


            #######

            usedExpense = float(ReadUsedExpenses(UsedExpensesFile))
            newUsedExpense = usedExpense + totalCost
            with open(UsedExpensesFile, "w") as UEF:
                UEF.write(str(newUsedExpense))
                UEF.close()

            remainingExpenses = str(float(ReadMonthlyExpense(DateOfCurrentExpenses)) - newUsedExpense)
            remainingExpensesMessage = "You have: " + currence + remainingExpenses + "\n remaining this month!"
            usedExpensesMessage = "You have spent: " + currence + str(newUsedExpense) + "\n this month!"
            TDEFlist = ReadTDEF(TotalDailyExpenditureFile)
            expensivestDayMessage = maxMessage(TDEFlist, True)
            MIFlist = ReadMonthlyItems(MonthlyItemsFile)
            expensivestItemMessage = maxMessage(MIFlist, False)


            #Resets the Entry fields and also updates the info labels at bottom of graph
            itemEntry.delete(0,END)
            storeEntry.delete(0,END)
            costEntry.delete(0,END)
            
            UpdateItems = []
            for x in range(len(MIFlist[0])):
                UpdateItems.append(UpperFirsts(MIFlist[0][x]))
            itemEntry['values'] = UpdateItems
            UpdateStores = []
            for x in range(2, len(MIFlist)):
                UpdateStores.append(UpperFirsts(MIFlist[x][0]))
            storeEntry['values'] = UpdateStores
            
            RElabel.config(text=str(remainingExpensesMessage))
            UElabel.config(text=usedExpensesMessage)
            EDlabel.config(text=expensivestDayMessage)
            EIlabel.config(text=expensivestItemMessage)

            
            makeGraph(self, BGDS, LGDS, BGMI, BGPS, BGSI, 2, 0, 17, 10, TotalDailyExpenditureFile, MonthlyItemsFile, "Kappa")
            

        except:
            newList = [[item], [totalCost], [store, totalCost, item, totalCost]]
            WriteMonthlyItems(newList)

            newList2 = [[],[]]
            if month == "02":
                isItLeapYear = int(year) % 4
                if isItLeapYear == 0:
                    numberOfDays = dayInMonths[month][1]
                else:
                    numberOfDays = dayInMonths[month][0]
            else:
                numberOfDays = dayInMonths[month]
            for x in range(1, (numberOfDays + 1)):
                newList2[0].append(x)
                newList2[1].append(0)
            dayIndex = newList2[0].index(int(day))
            newList2[1][dayIndex] = float(newList2[1][dayIndex]) + totalCost
            WriteTDEF(newList2)
            
            
            ###

            remainingExpensesMessage = "You have: " + currence + str(float(ReadMonthlyExpense(DateOfCurrentExpenses)) - totalCost) + "\n remaining this month!"
            usedExpensesMessage = "You have spent: " + currence + str(totalCost) + "\n this month!"
            TDEFlist = ReadTDEF(TotalDailyExpenditureFile)
            expensivestDayMessage = maxMessage(TDEFlist, True)
            MIFlist = ReadMonthlyItems(MonthlyItemsFile)
            expensivestItemMessage = maxMessage(MIFlist, False)

            
            with open (UsedExpensesFile, "w") as UEF:
                UEF.write(str(totalCost))
                UEF.close()

            #Resets the Entry fields and also updates the info labels at bottom of graph
            itemEntry.delete(0,END)
            storeEntry.delete(0,END)
            costEntry.delete(0,END)

            UpdateItems = []
            for x in range(len(MIFlist[0])):
                UpdateItems.append(UpperFirsts(MIFlist[0][x]))
            itemEntry['values'] = UpdateItems
            UpdateStores = []
            for x in range(2, len(MIFlist)):
                UpdateStores.append(UpperFirsts(MIFlist[x][0]))
            storeEntry['values'] = UpdateStores
            
            RElabel.config(text=remainingExpensesMessage)
            UElabel.config(text=usedExpensesMessage)
            EDlabel.config(text=expensivestDayMessage)
            EIlabel.config(text=expensivestItemMessage)

            makeGraph(self, BGDS, LGDS, BGMI, BGPS, BGSI, 2, 0, 17, 10, TotalDailyExpenditureFile, MonthlyItemsFile, "Kappa")

    except:
        messagebox.showerror(title="Input Error!",message="Please input correctly!")


class MainFrame(Tk):

    def __init__(self):
        Tk.__init__(self)

        Tk.title(self, Title)
        Tk.iconbitmap(self, default="fticon2.ico")
        
        window = Frame(self)
        window.pack(side="top",fill="both",expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for x in (NewMonth, Standard, LoadOldDataPage):
            frame = x(window, self)
            self.frames[x] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        try:
            monthlyExpense = ReadMonthlyExpense(DateOfCurrentExpenses)
            self.show_frame(Standard)
        except:
            self.show_frame(NewMonth)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class NewMonth(Frame): #Completed 100%, perhaps make it look nice

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        standardCurrency = ["$","$", "£", "€", "₹", "¥", "₩", "IDR", "OMR", "AED"]
        currency2 = StringVar()
        currency2.set(standardCurrency[0])
        self.currencyOption = ttk.OptionMenu(self, currency2, *standardCurrency)
        
        self.label = ttk.Label(self, text="What is your monthly expenses?").pack()
        self.entry = ttk.Entry(self)
        self.label2 = ttk.Label(self, text="Please enter your currency:")
        
        self.button = ttk.Button(self, text="ENTER",command=lambda: self.GET(controller, currency2))
        self.entry.pack()
        self.label2.pack()
        self.currencyOption.pack()
        self.button.pack()



    def GET(self,controller, currency2):
        monthlyExpense = self.entry.get()
        standardCurrency = ["$", "£", "€", "IDR", "OMR"]
        currency = currency2.get()
        with open(DateOfCurrentExpenses,"w") as file:
            file.write(monthlyExpense)
            file.close()
        if monthlyExpense == "" and currency == "":
            Pass = False
        else:
            Pass = True
        if Pass:
            try:
                monthlyExpenseINT = int(monthlyExpense)
                if monthlyExpenseINT <= 0:
                    messagebox.showerror(title="Input Error!",message="You can't have minus or zero monthly expenses!")
                else:
                    with open(DateOfCurrentExpenses,"w") as file:
                        file.write(monthlyExpense)
                        file.close()
                    controller.show_frame(Standard)
                    textfile = open(CurrentCurrency, "w")
                    textfile.write(currency)
                    textfile.close()
                    changeInitialLabels()
                    controller.show_frame(Standard)
                    
            except:
                messagebox.showerror(title="Input Error!",message="That is not a number!")
        else:
            messagebox.showerror(title="Input Error!",message="You have left a field blank!")

def changeInitialLabels():
    textfile = open(CurrentCurrency, "r")
    currence = textfile.read()
    monthlyExpense = ReadMonthlyExpense(DateOfCurrentExpenses)
    monthlyExpense = "This month's expenses: " + currence + monthlyExpense
    label2.config(text=monthlyExpense)
    originalMoneys = ReadMonthlyExpense(DateOfCurrentExpenses)
    expenditureLeft = "The expenses you have remaining this month:\n" + currence + originalMoneys +"!"
    RElabel.config(text=expenditureLeft)
    aaa = "The expenses you have used this month:\n" + currence + "0" +"!"
    UElabel.config(text=aaa)


class Standard(ttk.Frame):
    def __init__(self, parent, controller):
        global label2
        global RElabel
        global UElabel
        ttk.Frame.__init__(self, parent)

        try:
            textfile = open(CurrentCurrency, "r")
            currence = textfile.read()
        except:
            currence = "tr"

        #Label texts
        try:
            monthlyExpense = ReadMonthlyExpense(DateOfCurrentExpenses)
            monthlyExpense = "This month's expenses: " + currence + monthlyExpense
        except:
            monthlyExpense="dsa"
            
        todayDate = "Today is: " + day + "/" + month + "/" + year
        
        empty = 40*"_"
        #value = StringVar()
       
        label = ttk.Label(self, text=todayDate)
        label.grid(column=0,row=1, columnspan=2)

        label2 = ttk.Label(self, text=monthlyExpense)
        label2.grid(column=0,row=2, columnspan=2)

        itemLabel = ttk.Label(self, text="Item Name")
        itemLabel.grid(column=0,row=3, columnspan=2)

        StoreLabel = ttk.Label(self, text="Store Name")
        StoreLabel.grid(column=0,row=5, columnspan=2)

        

        try:
            MIFlist = ReadMonthlyItems(MonthlyItemsFile)
            NewVal = []
            itemEntry = ttk.Combobox(self, textvariable=StringVar())
            for x in range(len(MIFlist[0])):
                NewVal.append(UpperFirsts(MIFlist[0][x]))
            itemEntry['values'] = NewVal
            itemEntry.grid(column=0,row=4, columnspan=2)
            NewVal = []
            storeEntry = ttk.Combobox(self, textvariable=StringVar())
            for x in range(2, len(MIFlist)):
                NewVal.append(UpperFirsts(MIFlist[x][0]))
            storeEntry['values'] = NewVal
            storeEntry.grid(column=0, row=6, columnspan=2)
            
        except:        
            itemEntry = ttk.Combobox(self, textvariable=StringVar())
            itemEntry.grid(column=0,row=4, columnspan=2)
            print("gay fucker")

            storeEntry = ttk.Combobox(self, textvariable=StringVar())
            storeEntry.grid(column=0, row=6, columnspan=2)
            

        costLabel = ttk.Label(self, text="Total Cost")
        costLabel.grid(column=0,row=7, columnspan=2)

        costEntry = ttk.Entry(self)
        costEntry.grid(column=0,row=8, columnspan=2)

    
        enterButton = ttk.Button(self, text="ENTER", command=lambda: NewData(itemEntry, storeEntry, costEntry, controller, RElabel, UElabel, EDlabel, EIlabel, self, currentBGDS, currentLGDS, currentBGMI, currentBGPS, currentBGSI))
        enterButton.grid(column=0,row=9, columnspan=2)

        ####bottom left corner
        label12 = ttk.Label(self, text=empty)
        label12.grid(column=0,row=10, columnspan=2)

        GraphControlsLabel = ttk.Label(self, text="Graph Controls")
        GraphControlsLabel.grid(column=0,row=11, columnspan=2)

        GSBbutton = ttk.Button(self, text="Show General Spendings (BG)", command=lambda: self.GraphWork(True, False, False, False, False, 2, 0, 17, 10, TotalDailyExpenditureFile, MonthlyItemsFile, "Kappa"))
        GSBbutton.grid(column=0,row=12, columnspan=2)

        GSLbutton = ttk.Button(self, text="Show General Spendings (LG)", command=lambda: self.GraphWork(False, True, False, False, False, 2, 0, 17, 10, TotalDailyExpenditureFile, MonthlyItemsFile, "Kappa"))
        GSLbutton.grid(column=0,row=13, columnspan=2)

        SPIbutton = ttk.Button(self, text="Show Spendings per Item", command=lambda: self.GraphWork(False, False, True, False, False, 2, 0, 17, 10, TotalDailyExpenditureFile, MonthlyItemsFile, "Kappa"))
        SPIbutton.grid(column=0,row=14, columnspan=2)

        SPSbutton = ttk.Button(self, text="Show Spendings per Store",command=lambda: self.GraphWork(False, False, False, True, False, 2, 0, 17, 10, TotalDailyExpenditureFile, MonthlyItemsFile, "Kappa"))
        SPSbutton.grid(column=0,row=15,columnspan=2)

        SSISbutton = ttk.Button(self, text="Show Spendings per Store Item",command=lambda: self.StorePerItem())
        SSISbutton.grid(column=0,row=16,columnspan=2)        

        LPSbutton = ttk.Button(self, text="Load Past Spendings", command=lambda: controller.show_frame(LoadOldDataPage))
        LPSbutton.grid(column=0,row=17, columnspan=2)

        #### end blc


        ####bottom most row

        dash = ttk.Label(self, text=5*"|\n")
        dash.grid(column=2, row=17, rowspan=2, sticky="w")

        try:
            remainingExpenses = str(float(ReadMonthlyExpense(DateOfCurrentExpenses)) - float(ReadUsedExpenses(UsedExpensesFile)))
            remainingExpensesMessage = "You have: " + currence + remainingExpenses + "\n remaining this month!"
            RElabel = Label(self, text=remainingExpensesMessage, borderwidth=2, relief="solid", bg="yellow")
            RElabel.grid(column=3, row=17, rowspan=2)
        except:
            try:
                remainingExpenses = str(float(ReadMonthlyExpense(DateOfCurrentExpenses)))
                remainingExpensesMessage = "You have: " + currence + remainingExpenses + "\n remaining this month!"
                RElabel = Label(self, text=remainingExpensesMessage, borderwidth=2, relief="solid", bg="yellow")
                RElabel.grid(column=3, row=17, rowspan=2)
            except:
                originalMoneys = "32"
                expenditureLeft = "You have: " + currence + originalMoneys + "\n remaining this month!"
                RElabel = Label(self, text=expenditureLeft, borderwidth=2, relief="solid", bg="yellow")
                RElabel.grid(column=3, row=17, rowspan=2)

        try:
            usedExpenses = ReadUsedExpenses(UsedExpensesFile)
            usedExpensesMessage = "You have spent: " + currence + str(usedExpenses) + "\n this month!"
            UElabel = Label(self, text=usedExpensesMessage, borderwidth=2, relief="solid", bg="yellow")
            UElabel.grid(column=5, row=17, rowspan=2)
        except:
            usedExpenses = "0"
            usedExpensesMessage = "You have spent: " + currence + str(usedExpenses) + "\n this month!"
            UElabel = Label(self, text=usedExpensesMessage, borderwidth=2, relief="solid", bg="yellow")
            UElabel.grid(column=5, row=17, rowspan=2)

        try:
            TDEFlist = ReadTDEF(TotalDailyExpenditureFile)
            expensivestDayMessage = maxMessage(TDEFlist, True)
            EDlabel = Label(self, text=expensivestDayMessage, borderwidth=2, relief="solid", bg="yellow")
            EDlabel.grid(column=7, row=17, rowspan=2)
        except:
            expensivestDayMessage = "You haven't spent anything this month!"
            EDlabel = Label(self, text=expensivestDayMessage, borderwidth=2, relief="solid", bg="yellow")
            EDlabel.grid(column=7, row=17, rowspan=2)

        try:
            MIFlist = ReadMonthlyItems(MonthlyItemsFile)
            expensivestItemMessage = maxMessage(MIFlist, False)
            EIlabel = Label(self, text=expensivestItemMessage, borderwidth=2, relief="solid", bg="yellow")
            EIlabel.grid(column=9, row=17, rowspan=2)
        except:
            expensivestItemMessage = "You haven't bought anything this month!"
            EIlabel = Label(self, text=expensivestItemMessage, borderwidth=2, relief="solid", bg="yellow")
            EIlabel.grid(column=9, row=17, rowspan=2)

        ######Canvas and graph time!
        try:
            self.canvas = makeGraph(self, True, False, False, False, False, 2, 0, 17, 14, TotalDailyExpenditureFile, MonthlyItemsFile, "Kappa")
        except:
            self.canvas = Canvas(self, height=500,width=1000,bg="white")
            self.canvas.grid(column=2,row=0, rowspan=17, columnspan=14)

    def GraphWork(self, BGDS, LGDS, BGMI, BGPS, BGSI, col, rw, rowsp, colsp, TDEfileName, MIfileName, lolz):
        self.canvas.get_tk_widget().destroy()
        self.canvas = makeGraph(self, BGDS, LGDS, BGMI, BGPS, BGSI, 2, 0, 17, 14, TotalDailyExpenditureFile, MonthlyItemsFile, lolz)

    def StorePerItem(self):
        self.canvas.get_tk_widget().destroy()
        
        self.SPIlabel = Label(self, text="Select Store to View")
        MIFlist = ReadMonthlyItems(MonthlyItemsFile)
        storeList = [MIFlist[2][0]]
        for x in range(2, len(MIFlist)):
            storeList.append(MIFlist[x][0])
        print(storeList)
        ShowingStore = StringVar()
        ShowingStore.set(storeList[0])
        self.StoreMenu = ttk.OptionMenu(self, ShowingStore, *storeList)
        self.SPIlabel.grid(column=7, row=6, rowspan=2)
        self.StoreMenu.grid(column=7, row=8, rowspan=2)
        self.SPIbutton = ttk.Button(self, text="ENTER", command=lambda: self.GetStoreAndProceed(ShowingStore))
        self.SPIbutton.grid(column=7, row=10, rowspan=2)

    def GetStoreAndProceed(self, ShowingStore):
        chosenStore = ShowingStore.get()
        self.SPIlabel.destroy()
        self.StoreMenu.destroy()
        self.SPIbutton.destroy()
        self.GraphWork(False, False, False, False, True, 2, 0, 17, 10, TotalDailyExpenditureFile, MonthlyItemsFile, chosenStore)


        


class LoadOldDataPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.Options(controller)
        
    def Options(self, controller):
        MonthsPure = ["January","January","February","March","April","May", "June", "July", "August",
                      "September", "October", "November", "December"]
        YearsPure = ["2013"]
        Years = 2013
        yearINT = int(year)
        for x in range(yearINT - Years + 1):
            YearsPure.append(str(Years))
            Years += 1
        ShowingMonth = StringVar()
        ShowingMonth.set(MonthsPure[0])
        ShowingYear = StringVar()
        ShowingYear.set(YearsPure[0])
        self.label = Label(self, text="Which data would you like to see from?")
        self.MonthMenu = ttk.OptionMenu(self, ShowingMonth, *MonthsPure)
        self.YearMenu = ttk.OptionMenu(self, ShowingYear, *YearsPure)
        self.button = ttk.Button(self, text="ENTER", command=lambda: self.loadGraph(ShowingMonth, ShowingYear, controller))
        self.backButton = ttk.Button(self, text="BACK",command=lambda: controller.show_frame(Standard))
        self.label.pack()
        self.MonthMenu.pack()
        self.YearMenu.pack()
        self.button.pack()
        self.backButton.pack()


    def loadGraph(self,ShowingMonth, ShowingYear,controller):
        selectedMonth = ShowingMonth.get()
        selectedYear = ShowingYear.get()

        selectedMonthN = MonthsReverse[selectedMonth]

        DateOfOldExpenses = "MonthlyExpense" + selectedMonthN + selectedYear + ".txt"
        OldUsedExpensesFile = "UsedExpenses" + selectedMonthN + selectedYear + ".txt"
        self.OldMonthlyItemsFile = "Items" + selectedMonthN + selectedYear + ".csv"
        OldTotalDailyExpenditureFile = "DailyExpenditure" + selectedMonthN + selectedYear + ".csv"
        OldCurrency = "Currency" + selectedMonthN + selectedYear + ".txt"

        try:
            MI2file = ReadMonthlyItems(self.OldMonthlyItemsFile)
            oldExpense = ReadMonthlyExpense(DateOfOldExpenses)
            oldUsedExpense = ReadUsedExpenses(OldUsedExpensesFile)
            TDE2file = ReadTDEF(OldTotalDailyExpenditureFile)

            textfile = open(OldCurrency, "r")
            currence = textfile.read()
            
            self.label.destroy()
            self.MonthMenu.destroy()
            self.YearMenu.destroy()
            self.button.destroy()
            self.backButton.destroy()

            self.returnButton = ttk.Button(self, text="Return", command=lambda: self.Graph2Options(controller))
            self.DSBG = ttk.Button(self, text="Show General Spendings (BG)", command=lambda: self.InitiateGraph(0, OldTotalDailyExpenditureFile,  self.OldMonthlyItemsFile))
            self.DSLG = ttk.Button(self, text="Show General Spendings (LG)", command=lambda: self.InitiateGraph(1, OldTotalDailyExpenditureFile,  self.OldMonthlyItemsFile))
            self.SIBG = ttk.Button(self, text="Show Spendings per Item", command=lambda: self.InitiateGraph(2, OldTotalDailyExpenditureFile,  self.OldMonthlyItemsFile))
            self.SpS = ttk.Button(self, text="Show Spendings per Store", command=lambda: self.InitiateGraph(3, OldTotalDailyExpenditureFile,  self.OldMonthlyItemsFile))
            self.SpSI = ttk.Button(self, text="Show Spendings per Store Item", command=lambda: self.InitiateGraph(4, OldTotalDailyExpenditureFile,  self.OldMonthlyItemsFile))
            self.returnButton.grid(column=0,row=0, columnspan=2)
            self.graphL = Label(self, text="Graph Controls")
            self.graphL.grid(column=0,row=2, columnspan=2)
            self.DSBG.grid(column=0,row=3, columnspan=2)
            self.DSLG.grid(column=0,row=4, columnspan=2)
            self.SIBG.grid(column=0,row=5, columnspan=2)
            self.SpS.grid(column=0,row=6, columnspan=2)
            self.SpSI.grid(column=0,row=7, columnspan=2)

            
            print("n")
            self.canvas = makeGraph(self, True, False, False, False, False, 2, 0, 17, 14, OldTotalDailyExpenditureFile,  self.OldMonthlyItemsFile, "Kappa")
            print("n")
            oldRemainingExpenses = str(float(oldExpense) - float(oldUsedExpense))
            print("n")
            saved = "You saved " + currence + oldRemainingExpenses + " this month!"
            print("n")
            spent = "You spent " + currence + str(oldUsedExpense) + " this month!"
            print("n")
            expensivestDay = maxMessage(TDE2file, True)
            print("n")
            expensivestItem = maxMessage(MI2file, False)
            



            self.ODlabel = Label(self, text=saved, borderwidth=2, relief="solid", bg="yellow")
            self.ODlabel2 = Label(self, text=spent, borderwidth=2, relief="solid", bg="yellow")
            self.ODlabel3 = Label(self, text=expensivestDay, borderwidth=2, relief="solid", bg="yellow")
            self.ODlabel4 = Label(self, text=expensivestItem, borderwidth=2, relief="solid", bg="yellow")
            self.ODlabel.grid(column=0, row=9, columnspan=2)
            self.ODlabel2.grid(column=0, row=11, columnspan=2)
            self.ODlabel3.grid(column=0, row=13, columnspan=2)
            self.ODlabel4.grid(column=0, row=15, columnspan=2)
        
            
        except:
            messagebox.showerror(title="Files not found!",message="You do not have any data in this time period!")


    def InitiateGraph(self, a, fileA, fileB):
        self.canvas.get_tk_widget().destroy()
        if a == 0:
            self.canvas = makeGraph(self, True, False, False, False, False, 2, 0, 17, 14, fileA,  fileB, "Kappa")
        elif a == 1:
            self.canvas = makeGraph(self, False, True, False, False, False, 2, 0, 17, 14, fileA,  fileB, "Kappa")
        elif a == 2:
            self.canvas = makeGraph(self, False, False, True, False, False, 2, 0, 17, 14, fileA,  fileB, "Kappa")
        elif a == 3:
            self.canvas = makeGraph(self, False, False, False, True, False, 2, 0, 17, 14, fileA,  fileB, "Kappa")
        else:
            self.StorePerItem(fileA)


        
    def Graph2Options(self, controller):
        self.returnButton.destroy()
        self.graphL.destroy()
        self.DSBG.destroy()
        self.DSLG.destroy()
        self.SIBG.destroy()
        self.SpS.destroy()
        self.SpSI.destroy()
        self.canvas.get_tk_widget().destroy()
        self.ODlabel.destroy()
        self.ODlabel2.destroy()
        self.ODlabel3.destroy()
        self.ODlabel4.destroy()
        self.Options(controller)

    def StorePerItem(self, TotalDailyExpenditureFile):
        self.canvas.get_tk_widget().destroy()
        
        self.SPIlabel = Label(self, text="Select Store to View")
        MIFlist = ReadMonthlyItems(self.OldMonthlyItemsFile)
        storeList = [MIFlist[2][0]]
        for x in range(2, len(MIFlist)):
            storeList.append(MIFlist[x][0])
        print(storeList)
        ShowingStore = StringVar()
        ShowingStore.set(storeList[0])
        self.StoreMenu = ttk.OptionMenu(self, ShowingStore, *storeList)
        self.SPIlabel.grid(column=7, row=6, rowspan=2)
        self.StoreMenu.grid(column=7, row=8, rowspan=2)
        self.SPIbutton = ttk.Button(self, text="ENTER", command=lambda: self.GetStoreAndProceed(ShowingStore, TotalDailyExpenditureFile))
        self.SPIbutton.grid(column=7, row=10, rowspan=2)

    def GetStoreAndProceed(self, ShowingStore, TotalDailyExpenditureFile):
        chosenStore = ShowingStore.get()
        self.SPIlabel.destroy()
        self.StoreMenu.destroy()
        self.SPIbutton.destroy()
        self.canvas = makeGraph(self, False, False, False, False, True, 2, 0, 17, 10, TotalDailyExpenditureFile, self.OldMonthlyItemsFile, chosenStore)


        
        




        
app = MainFrame()
app.mainloop()

raise SystemExit(0)
