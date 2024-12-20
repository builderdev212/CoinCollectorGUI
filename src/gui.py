import tkinter
from tkinter import ttk, scrolledtext, Menu, Spinbox, messagebox
from time import sleep
import traceback

from coinDatabase import coinDatabase
from coinTypes import Coin


class gui:
    def __init__(self):
        self.win = tkinter.Tk()
        self.win.title("Coin Database")

        self.createWidgets()

    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    def createWidgets(self):
        self.tabCtrl = ttk.Notebook(self.win)

        self.connectTabSetup()
        self.overviewTabSetup()
        self.viewTabSetup()
        self.addOrRemoveTabSetup()
        self.searchTabSetup()
        self.menuSetup()

        self.tabCtrl.pack(expand=1, fill="both")
        self.tabCtrl.tab(0, state="normal")
        self.tabCtrl.tab(1, state="disabled")
        self.tabCtrl.tab(2, state="disabled")
        self.tabCtrl.tab(3, state="disabled")
        self.tabCtrl.tab(4, state="disabled")

    def connectTabSetup(self):
        self.connectTab = ttk.Frame(self.tabCtrl)
        self.tabCtrl.add(self.connectTab, text="Connection")

        self.connectGroup = ttk.LabelFrame(self.connectTab, text=" Connect ")
        self.connectGroup.grid(column=0, row=0, padx=8, pady=4)

        ttk.Label(self.connectGroup, text="Database Name:").grid(
            column=0, row=0, padx=2, pady=2
        )

        self.databaseName = tkinter.StringVar()
        self.databaseNameEntry = ttk.Entry(
            self.connectGroup, width=20, textvariable=self.databaseName
        )
        self.databaseNameEntry.grid(column=1, row=0, padx=2, pady=2)

        self.connectToDatabase = ttk.Button(
            self.connectGroup, text="Connect", command=self.connect
        )
        self.connectToDatabase.grid(column=0, row=1, padx=2, pady=2, columnspan=2)

    def connect(self):
        try:
            self.db = coinDatabase(self.databaseName.get())
        except Exception:
            messagebox.showerror("Database Error", traceback.format_exc())
        else:
            self.tabCtrl.tab(0, state="disabled")
            self.tabCtrl.tab(1, state="normal")
            self.tabCtrl.tab(2, state="normal")
            self.tabCtrl.tab(3, state="normal")
            self.tabCtrl.tab(4, state="normal")

            self.viewAllInitialUpdate()
            self.overviewTabInitialUpdate()

    def overviewTabSetup(self):
        self.overviewTab = ttk.Frame(self.tabCtrl)
        self.tabCtrl.add(self.overviewTab, text="Overview")

    def overviewTabInitialUpdate(self):
        coinCountTxt = f"You have {self.db.size()} coins in your database."
        self.cointCountLabel = ttk.Label(self.overviewTab, text=coinCountTxt)
        self.cointCountLabel.grid(column=0, row=0, padx=2, pady=2)

        oldestYearTxt = "Your oldest coin is from {}.".format(self.db.oldestYear())
        self.oldestYearLabel = ttk.Label(self.overviewTab, text=oldestYearTxt)
        self.oldestYearLabel.grid(column=0, row=1, padx=2, pady=2)

        valueTxt = f"Your collection of coins is worth ${self.db.totalValue()}. Your most expensive coin is worth ${self.db.highestValue()}."
        self.valueLabel = ttk.Label(self.overviewTab, text=valueTxt)
        self.valueLabel.grid(column=0, row=2, padx=2, pady=2, columnspan=2)

        self.kindGroup = ttk.LabelFrame(self.overviewTab, text=" Coins by type: ")
        self.kindGroup.grid(column=0, row=3)
        self.mintGroup = ttk.LabelFrame(self.overviewTab, text=" Coins by mint: ")
        self.mintGroup.grid(column=1, row=3)

        kindAmount = self.db.size(byKind=True)
        kinds = [
            "Penny",
            "Nickel",
            "Dime",
            "Quarter",
            "Half Dollar",
            "Dollar",
            "Other",
        ]
        kindLabelTxt = ""
        for n in range(len(kinds)):
            kindLabelTxt += f"{kinds[n]} - {kindAmount[kinds[n]]}\n"
        self.kindLabel = ttk.Label(self.kindGroup, text=kindLabelTxt)
        self.kindLabel.grid(column=0, row=0, padx=2, pady=2)

        mintAmount = self.db.size(byMint=True)
        mints = [
            "P",
            "D",
            "S",
            "W",
            "Other",
        ]
        mintLabelText = ""
        for n in range(5):
            mintLabelText += f"{mints[n]} - {mintAmount[mints[n]]}\n"
        self.mintLabel = ttk.Label(self.mintGroup, text=mintLabelText)
        self.mintLabel.grid(column=0, row=0, padx=2, pady=2)

        self.updateOverview = ttk.Button(
            self.overviewTab, text="Update Information", command=self.overviewTabUpdate
        )
        self.updateOverview.grid(column=0, row=4, padx=2, pady=2)

    def overviewTabUpdate(self):
        self.cointCountLabel.destroy()
        self.oldestYearLabel.destroy()
        self.valueLabel.destroy()
        self.kindLabel.destroy()
        self.mintLabel.destroy()

        self.overviewTabInitialUpdate()

    def viewTabSetup(self):
        self.viewAll = ttk.Frame(self.tabCtrl)
        self.tabCtrl.add(self.viewAll, text="View All Coins")

        self.updateViewAllCoins = ttk.Button(
            self.viewAll, text="Update View", command=self.viewAllUpdate
        )
        self.updateViewAllCoins.grid(column=0, row=0, padx=2, pady=2)

        self.viewAllCoins = scrolledtext.ScrolledText(
            self.viewAll, width=70, height=19, wrap=tkinter.WORD, state="disabled"
        )
        self.viewAllCoins.grid(column=0, row=1)

    def viewAllInitialUpdate(self):
        try:
            result = self.db.dump()
        except Exception:
            messagebox.showerror("Database Error", traceback.format_exc())
        else:
            output = "Your results:\n"
            for id, kind, year, mint, description, condition, value in result:
                output += "{} - {} - {} - {} - {} - {} - {}\n".format(
                    id, kind, year, mint, description, condition, value
                )
            output += "\n"

            self.viewAllCoins.configure(state="normal")
            self.viewAllCoins.insert(tkinter.INSERT, output)
            self.viewAllCoins.configure(state="disabled")

    def viewAllUpdate(self):
        self.viewAllCoins.configure(state="normal")
        self.viewAllCoins.delete("0.0", tkinter.END)
        self.viewAllCoins.configure(state="disabled")

        self.viewAllInitialUpdate()

    def addOrRemoveTabSetup(self):
        self.addOrRemoveTab = ttk.Frame(self.tabCtrl)
        self.tabCtrl.add(self.addOrRemoveTab, text="Add/Remove Coin")

        self.addTabSetup()
        self.removeTabSetup()

        self.addOrRemoveOutputTxt = scrolledtext.ScrolledText(
            self.addOrRemoveTab, width=48, height=9, wrap=tkinter.WORD, state="disabled"
        )
        self.addOrRemoveOutputTxt.grid(column=0, row=2, columnspan=4)

    def addTabSetup(self):
        self.addGroup = ttk.LabelFrame(self.addOrRemoveTab, text=" Add Coin ")
        self.addGroup.grid(column=0, row=0, padx=8, pady=4)

        ttk.Label(self.addGroup, text="Kind:").grid(column=0, row=0)
        ttk.Label(self.addGroup, text="Year:").grid(column=1, row=0)
        ttk.Label(self.addGroup, text="Mint:").grid(column=2, row=0)
        ttk.Label(self.addGroup, text="Condition:").grid(column=3, row=0)
        ttk.Label(self.addGroup, text="Value:").grid(column=4, row=0)
        ttk.Label(self.addGroup, text="Description:").grid(column=0, row=2)

        self.kindTxt = tkinter.StringVar()
        self.kindChoice = ttk.Combobox(
            self.addGroup, width=10, textvariable=self.kindTxt, state="readonly"
        )
        self.kindChoice["values"] = (
            "Penny",
            "Nickel",
            "Dime",
            "Quarter",
            "Half Dollar",
            "Dollar",
            "Other",
        )
        self.kindChoice.grid(column=0, row=1, padx=2, pady=2)

        self.yearInt = tkinter.IntVar()
        self.yearChoice = ttk.Entry(self.addGroup, width=4, textvariable=self.yearInt)
        self.yearChoice.grid(column=1, row=1, padx=2, pady=2)

        self.mintTxt = tkinter.StringVar()
        self.mintChoice = ttk.Combobox(
            self.addGroup, width=4, textvariable=self.mintTxt, state="readonly"
        )
        self.mintChoice["values"] = ("P", "D", "S", "W", "Other")
        self.mintChoice.grid(column=2, row=1, padx=2, pady=2)

        self.conditionTxt = tkinter.StringVar()
        self.conditionChoice = ttk.Combobox(
            self.addGroup, width=4, textvariable=self.conditionTxt, state="readonly"
        )
        self.conditionChoice["values"] = (
            "PR",
            "FA",
            "AG",
            "G",
            "VG",
            "F",
            "VF",
            "XF",
            "AU",
            "U",
            "MS",
            "PR",
            "Other",
        )
        self.conditionChoice.grid(column=3, row=1, padx=2, pady=2)

        self.valueInt = tkinter.IntVar()
        self.valueChoice = ttk.Entry(self.addGroup, width=6, textvariable=self.valueInt)
        self.valueChoice.grid(column=4, row=1, padx=2, pady=2)

        self.descriptionTxt = tkinter.StringVar()
        self.descriptionChoice = ttk.Entry(
            self.addGroup, width=50, textvariable=self.descriptionTxt
        )
        self.descriptionChoice.grid(column=0, row=3, columnspan=5, padx=2, pady=2)

        self.addCoinButton = ttk.Button(
            self.addGroup, text="Add Coin", command=self.addCoin
        )
        self.addCoinButton.grid(column=0, row=4, padx=2, pady=2)

    def addCoin(self):
        if (
            self.kindTxt.get() == ""
            or self.conditionTxt.get() == ""
            or self.descriptionTxt.get() == ""
        ):
            messagebox.showwarning(
                "Blank Values",
                "You have failed to either give this entry a type, condition, or description.",
            )
        else:
            try:
                self.db.add(
                    coin=Coin(
                        self.kindTxt.get(),
                        self.yearInt.get(),
                        self.mintTxt.get(),
                        self.descriptionTxt.get(),
                        self.conditionTxt.get(),
                        self.valueInt.get(),
                    )
                )
            except Exception:
                messagebox.showerror("Database Error", traceback.format_exc())
            else:
                self.addOrRemoveOutputTxt.configure(state="normal")
                self.addOrRemoveOutputTxt.insert(tkinter.INSERT, "Coin added.\n")
                self.addOrRemoveOutputTxt.configure(state="disabled")
                self.kindChoice.set("")
                self.mintChoice.set("")
                self.conditionChoice.set("")
                self.yearChoice.delete(0, "end")
                self.descriptionChoice.delete(0, "end")
                self.valueChoice.delete(0, "end")

    def removeTabSetup(self):
        self.removeGroup = ttk.LabelFrame(self.addOrRemoveTab, text=" Remove Coin ")
        self.removeGroup.grid(column=0, row=1, pady=4, columnspan=4)

        ttk.Label(self.removeGroup, text="Coin ID:").grid(
            column=0, row=0, padx=2, pady=2
        )

        self.idInt = tkinter.IntVar()
        self.idChoice = ttk.Entry(self.removeGroup, width=4, textvariable=self.idInt)
        self.idChoice.grid(column=2, row=0, padx=2, pady=2)

        self.removeCoinButton = ttk.Button(
            self.removeGroup, text="Remove Coin", command=self.removeCoin
        )
        self.removeCoinButton.grid(column=3, row=0, padx=2, pady=2)

    def removeCoin(self):
        try:
            self.db.remove(id=self.idInt.get())
        except:
            messagebox.showwarning("Database Error", traceback.format_exc())
        else:
            self.addOrRemoveOutputTxt.configure(state="normal")
            self.addOrRemoveOutputTxt.insert(
                tkinter.INSERT, "Coin {} removed.\n".format(self.idInt.get())
            )
            self.addOrRemoveOutputTxt.configure(state="disabled")
            self.idChoice.delete(0, "end")

    def searchTabSetup(self):
        self.searchTab = ttk.Frame(self.tabCtrl)
        self.tabCtrl.add(self.searchTab, text="Search Coins")

        self.searchGroup = ttk.LabelFrame(self.searchTab, text=" Search Coin Database ")
        self.searchGroup.grid(column=0, row=0, padx=8, pady=4)

        ttk.Label(self.searchGroup, text="Type:").grid(column=0, row=0, padx=2, pady=2)
        ttk.Label(self.searchGroup, text="Year:").grid(column=1, row=0, padx=2, pady=2)
        ttk.Label(self.searchGroup, text="Mint:").grid(column=2, row=0, padx=2, pady=2)
        ttk.Label(self.searchGroup, text="Condition:").grid(
            column=3, row=0, padx=2, pady=2
        )
        ttk.Label(self.searchGroup, text="Description:").grid(
            column=0, row=2, padx=2, pady=2
        )

        self.searchTypeTxt = tkinter.StringVar()
        self.searchType = ttk.Combobox(
            self.searchGroup,
            width=10,
            textvariable=self.searchTypeTxt,
            state="readonly",
        )
        self.searchType["values"] = (
            "",
            "Penny",
            "Nickel",
            "Dime",
            "Quarter",
            "Half Dollar",
            "Dollar",
            "Other",
        )
        self.searchType.grid(column=0, row=1, padx=2, pady=2)

        self.searchYearTxt = tkinter.StringVar()
        self.searchYear = ttk.Entry(
            self.searchGroup, width=4, textvariable=self.searchYearTxt
        )
        self.searchYear.grid(column=1, row=1, padx=2, pady=2)

        self.searchMintTxt = tkinter.StringVar()
        self.searchMint = ttk.Combobox(
            self.searchGroup, width=4, textvariable=self.searchMintTxt, state="readonly"
        )
        self.searchMint["values"] = ("", "P", "D", "S", "W", "Other")
        self.searchMint.grid(column=2, row=1, padx=2, pady=2)

        self.searchConditionTxt = tkinter.StringVar()
        self.searchCondition = ttk.Combobox(
            self.searchGroup,
            width=4,
            textvariable=self.searchConditionTxt,
            state="readonly",
        )
        self.searchCondition["values"] = (
            "",
            "PR",
            "FA",
            "AG",
            "G",
            "VG",
            "F",
            "VF",
            "XF",
            "AU",
            "U",
            "MS",
            "PR",
        )
        self.searchCondition.grid(column=3, row=1, padx=2, pady=2)

        self.searchDescriptionTxt = tkinter.StringVar()
        self.searchDescription = ttk.Entry(
            self.searchGroup, width=50, textvariable=self.searchDescriptionTxt
        )
        self.searchDescription.grid(column=0, row=3, columnspan=4, padx=2, pady=2)

        self.searchCoinDatabase = ttk.Button(
            self.searchTab, text="Search!", command=self.searchDatabase
        )
        self.searchCoinDatabase.grid(column=1, row=0, padx=2, pady=2)

        self.sortGroup = ttk.LabelFrame(self.searchTab, text=" Sort By ")
        self.sortGroup.grid(column=0, row=1, padx=8, pady=4, columnspan=2)

        self.sortBy = tkinter.IntVar()
        self.sortValue = tkinter.Radiobutton(
            self.sortGroup, text="Value", variable=self.sortBy, value=5
        )
        self.sortValue.grid(column=5, row=0)
        self.sortKind = tkinter.Radiobutton(
            self.sortGroup, text="Kind", variable=self.sortBy, value=1
        )
        self.sortKind.grid(column=1, row=0)
        self.sortYear = tkinter.Radiobutton(
            self.sortGroup, text="Year", variable=self.sortBy, value=2
        )
        self.sortYear.grid(column=2, row=0)
        self.sortMint = tkinter.Radiobutton(
            self.sortGroup, text="Mint", variable=self.sortBy, value=3
        )
        self.sortMint.grid(column=3, row=0)
        self.sortCondition = tkinter.Radiobutton(
            self.sortGroup, text="Condition", variable=self.sortBy, value=4
        )
        self.sortCondition.grid(column=4, row=0)
        self.sortId = tkinter.Radiobutton(
            self.sortGroup, text="ID", variable=self.sortBy, value=0
        )
        self.sortId.grid(column=0, row=0)

        self.sortResults = scrolledtext.ScrolledText(
            self.searchTab, width=70, height=11, wrap=tkinter.WORD, state="disabled"
        )
        self.sortResults.grid(column=0, row=3, columnspan=4)

    def searchDatabase(self):
        self.sortResults.configure(state="normal")
        self.sortResults.delete("0.0", tkinter.END)
        self.sortResults.configure(state="disabled")

        if self.sortBy.get() == 0:
            sort = "id"
        elif self.sortBy.get() == 1:
            sort = "kind"
        elif self.sortBy.get() == 2:
            sort = "year"
        elif self.sortBy.get() == 3:
            sort = "mint"
        elif self.sortBy.get() == 4:
            sort = "condition"
        elif self.sortBy.get() == 5:
            sort = "value"
        else:
            sort = ""

        try:
            result = self.db.search(
                coin=Coin(
                    self.searchTypeTxt.get(),
                    self.searchYearTxt.get(),
                    self.searchMintTxt.get(),
                    self.searchDescriptionTxt.get(),
                    self.searchConditionTxt.get(),
                    -1,
                ),
                order=sort,
            )
        except Exception:
            messagebox.showerror("Database Error", traceback.format_exc())
        else:
            output = "Your results:\n"

            for id, kind, year, mint, description, condition, value in result:
                output += "{} - {} - {} - {} - {} - {} - {}\n".format(
                    id, kind, year, mint, description, condition, value
                )
            output += "\n"

            self.sortResults.configure(state="normal")
            self.sortResults.insert(tk.INSERT, output)
            self.sortResults.configure(state="disabled")

    def menuSetup(self):
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)

        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Exit", command=self._quit)
        menuBar.add_cascade(label="File", menu=fileMenu)
