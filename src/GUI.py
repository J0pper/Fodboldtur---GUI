import tkinter as tk
from tkinter import ttk
import customtkinter

from PIL import Image

import fodboldtur as fb


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class FootballGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Fodboldtur GUI")
        self.geometry(f"{1080}x{675}")
        self.resizable(False, False)

        # configure grid layout
        self.grid_columnconfigure((1, 2), weight=1)

        # title
        self.titleFrame = customtkinter.CTkFrame(self, fg_color="#2b2b2b")
        self.titleFrame.grid(row=0, column=1, padx=20, pady=(10, 0))
        self.titleLabel = customtkinter.CTkLabel(self.titleFrame, text="Fodboldtur")
        self.titleLabel.grid(row=0, column=1, pady=10)
        self.titleLabel.configure(font=(None, 30))

        # settings button
        self.settingsIcon = customtkinter.CTkImage(dark_image=Image.open("../img/settings_icon_dark.png"), size=(25, 25))
        customtkinter.CTkButton(self,
                                image=self.settingsIcon,
                                text="",
                                width=40,
                                height=40,
                                anchor="c",
                                command=self.settings)\
            .grid(row=0, column=2)

        # progress bar
        progressText = customtkinter.StringVar(value="0/4500 rupees betalt")
        self.progressLabel = customtkinter.CTkLabel(self.titleFrame, textvariable=progressText)
        self.progressLabel.grid(row=1, column=1, pady=10, sticky="s")
        self.progressLabel.configure(font=(None, 20))

        self.progressBar = customtkinter.CTkProgressBar(self.titleFrame,
                                                        orientation="horizontal",
                                                        width=759,
                                                        height=8)
        self.progressBar.grid(row=2, column=1, sticky="s")

        # treeview style
        self.treeStyle = ttk.Style()
        self.treeStyle.theme_use('clam')
        self.treeStyle.configure("Treeview",
                                 background="#2b2b2b",
                                 foreground="white",
                                 fieldbackground="#2b2b2b",
                                 font=(None, 12),
                                 rowheight=30)

        # treeview selected color
        self.treeStyle.map('Treeview',
                           background=[('selected', '#1f6aa5')])

        # treeview header styling
        self.treeStyle.configure("Treeview.Heading",
                                 background="#242424",
                                 foreground="white",
                                 fieldbackground="#242424",
                                 borderwidth=0,
                                 font=(None, 12))

        # treeview
        self.tree = ttk.Treeview(self)
        self.tree.configure(columns=("paid_amount", "debt_amount"))
        self.tree.grid(row=3, column=1, rowspan=10, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # define headings
        self.tree.heading("#0", text="Navn", anchor="c")
        self.tree.heading("paid_amount", text="Indbetalt beløb", anchor="c")
        self.tree.heading("debt_amount", text="Resterende beløb", anchor="c")

        # configure columns
        self.tree.column("#0", anchor="c", minwidth=250)
        self.tree.column("paid_amount", anchor="c", minwidth=200)
        self.tree.column("debt_amount", anchor="c", minwidth=200)

        # create and format frame for action buttons
        self.buttonFrame = customtkinter.CTkScrollableFrame(self, label_text="Foretag handling", width=250)
        self.buttonFrame.grid(row=3, column=2, rowspan=3, columnspan=10, padx=(0, 10), pady=(20, 20), sticky="nse")

        # create and format action buttons
        self.makeTransactionButton = customtkinter.CTkButton(master=self.buttonFrame,
                                                             text="Foretag transaktion",
                                                             command=self.make_transaction)
        self.makeTransactionButton.grid(row=5, column=2, pady=10, padx=20)

        self.addMemberButton = customtkinter.CTkButton(master=self.buttonFrame,
                                                       text="Tilføj medlem",
                                                       command=self.add_member)
        self.addMemberButton.grid(row=6, column=2, pady=10, padx=20)

        self.removeMemberButton = customtkinter.CTkButton(master=self.buttonFrame,
                                                          text="Fjern medlem",
                                                          command=self.remove_member)
        self.removeMemberButton.grid(row=7, column=2, pady=10, padx=20)

        self.buttonGroupErrorMsgText = "hello"
        self.buttonGroupErrorMsg = customtkinter.CTkLabel(master=self.buttonFrame,
                                                          text=self.buttonGroupErrorMsgText)

        self.showLeaderBoardButton = customtkinter.CTkButton(master=self.buttonFrame,
                                                             text="Leaderboard of shame",
                                                             command=self.leaderboard)
        self.showLeaderBoardButton.grid(row=8, column=2, pady=10, padx=20)

        self.buttonGroupErrorMsg.grid(row=9, column=2)

        # create frame for the log
        self.logFrame = customtkinter.CTkScrollableFrame(master=self,
                                                         label_text="Log",
                                                         width=250)
        self.logFrame.grid(row=6, column=2, padx=(0, 10), pady=(0, 20), sticky="nse")

        # ------------------------------------------------------
        # ------- Run a terrible initialization function -------
        # ------------------------------------------------------
        fb.bad_init(self.tree, self.logFrame, progressText, self.progressBar)

    def new_window(self, title: str, width: int, height: int, resizable: bool):
        newWindow = customtkinter.CTkToplevel(self)  # create CTk window like you do with the Tk window
        newWindow.title(title)  # set the title of the window
        newWindow.geometry(f"{width}x{height}")  # set the size of the window
        newWindow.resizable(resizable, resizable)  # param1: width, param2: height
        newWindow.attributes('-topmost', 1)  # sets the window in top of the others and puts it in focus
        return newWindow

    def make_transaction(self):
        selected = fb.pass_get_selected(self.tree)

        title = "Foretag transaktion."
        makePaymentWindow = self.new_window(title=title, width=400, height=400, resizable=False)

        makePaymentWindow.grid_columnconfigure((0, 1, 2, 3), weight=1)
        makePaymentWindow.grid_rowconfigure((0, 1, 2, 3), weight=1)

        txnTypeVar = customtkinter.StringVar()
        customtkinter.CTkLabel(makePaymentWindow, text="Vælg transaktionstype.")\
            .grid(row=0, column=0, columnspan=4)
        customtkinter.CTkSegmentedButton(makePaymentWindow,
                                         values=["Indbetaling", "Udbetaling"],
                                         variable=txnTypeVar)\
            .grid(row=1, column=0, columnspan=4)

        infoLabelText = (f"{selected[0]} har indbetalt {selected[1]} kr.\n"
                         f"Vælg transaktionsbeløb.")
        customtkinter.CTkLabel(master=makePaymentWindow, text=infoLabelText)\
            .grid(row=2, column=0, columnspan=4)

        customtkinter.CTkLabel(master=makePaymentWindow,
                               text="Indtast beløb: ",)\
            .grid(row=3, column=0, sticky="e")

        entryVar = customtkinter.StringVar()
        customtkinter.CTkEntry(master=makePaymentWindow,
                               placeholder_text="Beløb",
                               textvariable=entryVar,
                               width=250)\
            .grid(row=3, column=1, columnspan=3)

        # Label for displaying error-message for entry-field
        errorLabelText = customtkinter.StringVar()
        customtkinter.CTkLabel(master=makePaymentWindow,
                               textvariable=errorLabelText,
                               text_color="red")\
            .grid(row=4, column=0, columnspan=4)

        customtkinter.CTkButton(master=makePaymentWindow,
                                text="Udfør",
                                command=lambda: fb.make_transaction_button(makePaymentWindow,
                                                                           errorLabelText,
                                                                           selected[0],
                                                                           entryVar.get(),
                                                                           txnTypeVar.get()))\
            .grid(row=5, column=0, columnspan=2, pady=(20, 20))

        customtkinter.CTkButton(master=makePaymentWindow,
                                text="Annuller",
                                fg_color="#666666",
                                hover_color="#333333",
                                command=makePaymentWindow.destroy)\
            .grid(row=5, column=2, columnspan=2, pady=(20, 20))

    def add_member(self):
        addMemberWindow = self.new_window(title="Tilføj medlem", width=400, height=300, resizable=False)

        addMemberWindow.grid_columnconfigure((0, 1, 2, 3), weight=1)
        addMemberWindow.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        addMemberWindow.grid_rowconfigure(5, weight=2)

        labelText = f"Du er nu i gang med at tilføje et klubmedlem."
        customtkinter.CTkLabel(master=addMemberWindow, text=labelText)\
            .grid(row=0, column=0, columnspan=4)

        customtkinter.CTkLabel(master=addMemberWindow, text="Fornavn: ")\
            .grid(row=1, column=0, columnspan=2)
        customtkinter.CTkLabel(master=addMemberWindow, text="Efternavn")\
            .grid(row=2, column=0, columnspan=2)
        customtkinter.CTkLabel(master=addMemberWindow, text="Startbeløb: ")\
            .grid(row=3, column=0, columnspan=2)

        firstName = customtkinter.StringVar()
        customtkinter.CTkEntry(master=addMemberWindow, placeholder_text="F.eks. Bo", textvariable=firstName)\
            .grid(row=1, column=2, columnspan=2)
        surName = customtkinter.StringVar()
        customtkinter.CTkEntry(master=addMemberWindow, textvariable=surName)\
            .grid(row=2, column=2, columnspan=2)
        startAmount = customtkinter.StringVar(value="0")
        customtkinter.CTkEntry(master=addMemberWindow, placeholder_text="F.eks. 1.000.000", textvariable=startAmount) \
            .grid(row=3, column=2, columnspan=2)

        # Label for displaying error-message for entry-field
        errorLabelText = customtkinter.StringVar()
        customtkinter.CTkLabel(master=addMemberWindow,
                               textvariable=errorLabelText,
                               text_color="red") \
            .grid(row=4, column=0, columnspan=4)

        customtkinter.CTkButton(master=addMemberWindow,
                                text="Tilføj",
                                command=lambda: fb.add_member_button(addMemberWindow,
                                                              errorLabelText,
                                                              firstName.get() + " " + surName.get(),
                                                              startAmount.get()))\
            .grid(row=5, column=0, columnspan=2)
        customtkinter.CTkButton(master=addMemberWindow,
                                text="Annuller",
                                fg_color="#666666",
                                hover_color="#333333",
                                command=addMemberWindow.destroy)\
            .grid(row=5, column=2, columnspan=2)

    def remove_member(self):
        removeMemberWindow = self.new_window(title="Fjern medlem", width=400, height=200, resizable=False)

        selected = fb.pass_get_selected(self.tree)

        removeMemberWindow.grid_columnconfigure(index=(0, 1), weight=1)
        removeMemberWindow.grid_rowconfigure(index=(0, 1, 2, 3), weight=1)

        headerLabelText = f"Du er ved fjerne {selected[0]} som indbetaler."
        customtkinter.CTkLabel(master=removeMemberWindow, text=headerLabelText)\
            .grid(row=0, column=0, columnspan=2)

        keepMoneyLabelText = f"Behold personens\nindbetalte beløb?"
        customtkinter.CTkLabel(master=removeMemberWindow, text=keepMoneyLabelText) \
            .grid(row=1, column=0)

        switchState = customtkinter.BooleanVar(value=False)
        customtkinter.CTkSwitch(master=removeMemberWindow,
                                text="# OUT OF ORDER #",
                                variable=switchState,
                                onvalue=1,
                                offvalue=0)\
            .grid(row=1, column=1)

        errorLabelText = customtkinter.StringVar()
        customtkinter.CTkLabel(master=removeMemberWindow,
                               textvariable=errorLabelText,
                               text_color="red")\
            .grid(row=2, column=0, columnspan=2)

        customtkinter.CTkButton(master=removeMemberWindow,
                                text="Ja",
                                command=lambda: fb.rem_member_button(removeMemberWindow,
                                                                     errorLabelText,
                                                                     selected[0],
                                                                     switchState.get()))\
            .grid(row=3, column=0)
        customtkinter.CTkButton(master=removeMemberWindow,
                                text="Annuller",
                                fg_color="#666666",
                                hover_color="#333333",
                                command=removeMemberWindow.destroy)\
            .grid(row=3, column=1)

    # Displays the 3 members who've paid the least.
    def leaderboard(self):
        leaderboardWindow = self.new_window(title="Leaderboard of shame", width=400, height=200, resizable=False)

        leaderboardWindow.grid_columnconfigure(index=0, weight=1)
        leaderboardWindow.grid_rowconfigure(index=(0, 1, 2, 3), weight=1)

        titleText: str = "Her kan du se fodboldklubbens 3 fattigste medlemmer."
        customtkinter.CTkLabel(master=leaderboardWindow,
                               text=titleText)\
            .grid(row=0, column=0)

        poorPeople: list = fb.leaderboard_of_shame_button()
        for person in poorPeople:
            labelText = f"{poorPeople.index(person)+1}: {person[0]}, {person[1]} kr."
            customtkinter.CTkLabel(master=leaderboardWindow, text=labelText)\
                .grid(row=poorPeople.index(person)+1, column=0, sticky="n")

    # Settings menu.
    def settings(self):
        settingsWindow = self.new_window(title="Indstillinger", width=670, height=300, resizable=False)

        saveSettFrame = customtkinter.CTkScrollableFrame(settingsWindow,
                                                         label_text="Save indstillinger",
                                                         width=250)
        saveSettFrame.grid(row=0, column=0, padx=(40, 20), pady=20)

        autoSaveSwitch = customtkinter.CTkSwitch(saveSettFrame,
                                                 text="Autosave",
                                                 variable=fb.autoSave)
        autoSaveSwitch.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        # -----------------------------------------------------------------------------------

        logSettFrame = customtkinter.CTkScrollableFrame(settingsWindow,
                                                        label_text="Log indstillinger",
                                                        width=250)
        logSettFrame.grid(row=0, column=1, padx=(20, 40), pady=20)

        autoLogSwitch = customtkinter.CTkSwitch(logSettFrame, text="Autolog - # OUT OF ORDER #")
        autoLogSwitch.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        filterLogLabel = customtkinter.CTkLabel(logSettFrame, text="Filtrér loggen")
        filterLogLabel.grid(row=2, column=0, padx=5, sticky="w")

        for i, (filterTag, filterProperties) in enumerate(fb.logFilters.items()):
            customtkinter.CTkSwitch(logSettFrame,
                                    text=filterProperties[0],
                                    variable=filterProperties[1],
                                    command=fb.pass_log_widget_update)\
                .grid(row=i+3, column=0, padx=5, pady=5, sticky="w")


if __name__ == "__main__":
    # create instance of the GUI class
    app = FootballGUI()
    # run the main GUI loop
    app.mainloop()
