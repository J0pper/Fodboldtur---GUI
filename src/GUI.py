import tkinter as tk
from tkinter import ttk
import customtkinter

import fodboldtur as fb


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class FootballGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Fodboldtur GUI")
        self.geometry(f"{1200}x{680}")
        self.resizable(False, False)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=3)
        self.grid_rowconfigure(6, weight=1)

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
        self.tree.configure(columns='paid_amount')
        self.tree.grid(row=0, column=1, rowspan=10, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # define headings
        self.tree.heading('#0', text='Navn', anchor='c')
        self.tree.heading('paid_amount', text="Indbetalt beløb", anchor='c')

        # configure columns
        self.tree.column('#0', anchor='c', minwidth=550)
        self.tree.column('paid_amount', anchor='c', minwidth=150)

        # create and format frame for action buttons
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=0, column=2, rowspan=3, padx=(0, 20), pady=(20, 20), sticky="nsw")
        # create and format header text for button frame
        self.label_button_frame = customtkinter.CTkLabel(master=self.button_frame, text="Foretag handling")
        self.label_button_frame.grid(row=0, column=2, columnspan=1, padx=10, pady=10)
        # create and format action buttons
        self.makePaymentButton = customtkinter.CTkButton(master=self.button_frame,
                                                         text="Lav indbetaling",
                                                         command=lambda: self.make_transaction(True))
        self.makePaymentButton.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.retractPaymentButton = customtkinter.CTkButton(master=self.button_frame,
                                                            text="Lav udbetaling",
                                                            command=lambda: self.make_transaction(False))
        self.retractPaymentButton.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.showLeaderBoardButton = customtkinter.CTkButton(master=self.button_frame, text="Leaderboard of shame")
        self.showLeaderBoardButton.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        self.addMemberButton = customtkinter.CTkButton(master=self.button_frame, text="Tilføj medlem", command=self.add_member)
        self.addMemberButton.grid(row=4, column=2, pady=10, padx=20, sticky="n")

        self.removeMemberButton = customtkinter.CTkButton(master=self.button_frame,
                                                          text="Fjern medlem",
                                                          command=self.remove_member)
        self.removeMemberButton.grid(row=5, column=2, pady=10, padx=20, sticky="n")

        self.buttonGroupErrorMsgText = "hello"
        self.buttonGroupErrorMsg = customtkinter.CTkLabel(master=self.button_frame,
                                                          text=self.buttonGroupErrorMsgText)

        self.buttonGroupErrorMsg.grid(row=6, column=2)



        # create frame for the log
        self.logFrame = customtkinter.CTkScrollableFrame(master=self,
                                                         label_text="Log",
                                                         width=200,)
        self.logFrame.grid(row=3, column=2, padx=(0, 10), pady=(0, 10), sticky="nsew")

        # run a terrible initialization function
        fb.shiddy_init(self.tree, self.logFrame)

    def new_window(self, title, width, height, resizable):
        newWindow = customtkinter.CTkToplevel(self)  # create CTk window like you do with the Tk window
        newWindow.title(title)
        newWindow.geometry(f"{width}x{height}")
        newWindow.resizable(resizable, resizable)  # width, height
        newWindow.attributes('-topmost', 1)
        return newWindow

    def make_transaction(self, deposit: bool):
        selected = self.get_selected(self.tree)

        title = "Foretag transaktion."
        makePaymentWindow = self.new_window(title=title, width=400, height=250, resizable=False)

        makePaymentWindow.grid_columnconfigure((0, 1, 2, 3), weight=1)
        makePaymentWindow.grid_rowconfigure((0, 1, 2, 3), weight=1)

        keyWord: str = "tilføjes" if deposit else "fratrækkes"
        infoLabelText = (f"{selected[0]} har indbetalt {selected[1]} kr.\n"
                         f"Hvor meget skal der {keyWord}?")
        customtkinter.CTkLabel(master=makePaymentWindow, text=infoLabelText)\
            .grid(row=0, column=0, columnspan=4)

        customtkinter.CTkLabel(master=makePaymentWindow,
                               text="Indtast beløb: ",)\
            .grid(row=1, column=0, sticky="e")

        entryVar = customtkinter.StringVar()
        customtkinter.CTkEntry(master=makePaymentWindow,
                               placeholder_text="Beløb",
                               textvariable=entryVar,
                               width=250)\
            .grid(row=1, column=1, columnspan=3)

        # Label for displaying error-message for entry-field
        errorLabelText = customtkinter.StringVar()
        customtkinter.CTkLabel(master=makePaymentWindow,
                               textvariable=errorLabelText,
                               text_color="red")\
            .grid(row=2, column=0, columnspan=4)

        customtkinter.CTkButton(master=makePaymentWindow,
                                text="Udfør",
                                command=lambda: fb.make_payment(makePaymentWindow,
                                                                errorLabelText,
                                                                selected[0],
                                                                entryVar.get()) if deposit
                                else fb.retract_payment(makePaymentWindow,
                                                        errorLabelText,
                                                        selected[0],
                                                        entryVar.get()))\
            .grid(row=3, column=0, columnspan=2)

        customtkinter.CTkButton(master=makePaymentWindow,
                                text="Annuller",
                                fg_color="#666666",
                                hover_color="#333333",
                                command=makePaymentWindow.destroy)\
            .grid(row=3, column=2, columnspan=2)

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
                                command=lambda: fb.add_member(addMemberWindow,
                                                              errorLabelText,
                                                              firstName.get() + " " + surName.get(),
                                                              startAmount.get()))\
            .grid(row=5, column=0, columnspan=2)
        customtkinter.CTkButton(master=addMemberWindow, text="Annuller") \
            .grid(row=5, column=2, columnspan=2)

    def remove_member(self):
        removeMemberWindow = self.new_window(title="Fjern medlem", width=400, height=200, resizable=False)

        selected = self.get_selected(self.tree)

        removeMemberWindow.grid_columnconfigure((0, 1), weight=1)
        removeMemberWindow.grid_rowconfigure((0, 1, 2, 3), weight=1)

        headerLabelText = f"Du er ved fjerne {selected[0]} som indbetaler."
        customtkinter.CTkLabel(master=removeMemberWindow, text=headerLabelText)\
            .grid(row=0, column=0, columnspan=2)

        keepMoneyLabelText = f"Behold personens\nindbetalte beløb?"
        customtkinter.CTkLabel(master=removeMemberWindow, text=keepMoneyLabelText) \
            .grid(row=1, column=0)

        switchState = customtkinter.BooleanVar(value=False)
        customtkinter.CTkSwitch(master=removeMemberWindow,
                                text="",
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
                                command=lambda: fb.rem_member(removeMemberWindow,
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

    def get_selected(self, selected_from) -> tuple[str, int]:
        selected: list = []
        for i in selected_from.selection():
            selected = selected_from.item(i)
        return selected['text'], selected['values'][0]


if __name__ == "__main__":
    # create instance of the GUI class
    app = FootballGUI()
    # run the main GUI loop
    app.mainloop()