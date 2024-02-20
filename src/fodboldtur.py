import cust_logging as lg
import misc
import customtkinter


# Maybe a bad initialization-function that sets up some useful global variables and loads plus display the saved data.
def bad_init(treeview_widget, log_frame_widget, progress_text, progress_bar):
    # Variable for the treeview-widget. Has to be accessed by the button-functions.
    global tree
    tree = treeview_widget

    # Variable of type dict[str, list[str, bool]]. Holds all the log-types so the user can filter the log.
    global logFilters
    logFilters = {
        "normPay": ["Indbetalinger for medlemmer", customtkinter.BooleanVar(value=True)],
        "normRetract": ["Udbetalinger for medlemmer", customtkinter.BooleanVar(value=True)],
        "normAddMem": ["Tilføjelse af medlem", customtkinter.BooleanVar(value=True)],
        "normRmvMem": ["Fjernelse af medlem", customtkinter.BooleanVar(value=True)],
        "fileLoadSuccess": ["Save-fil loadet succesfuldt", customtkinter.BooleanVar(value=True)],
        "fileLoadFail": ["Save-fil kan ikke\nloades/findes ikke", customtkinter.BooleanVar(value=True)],
        "debtClear": ["Fulde beløb betalt med rest", customtkinter.BooleanVar(value=True)],
        "insufficientFunds": ["Utilstrækkelig beløb for udbetaling", customtkinter.BooleanVar(value=True)],
    }

    # Total amount to be paid between all the members.
    global payGoal
    payGoal = 4500

    # Dictionary that holds the data: saved people and their amount paid.
    global footballTrip
    footballTrip, msg, logType = misc.load_data()
    lg.log(msg, logType)  # Logging the given msg returned when loading data.
    misc.update_treeview(tree, footballTrip, payGoal)  # Performs the initial population of the treeview-widget.

    # Variable for the log-widget. Has to be accessed by the button-functions.
    global logWidget
    logWidget = log_frame_widget
    lg.update_log_frame(logWidget, logFilters)  # Performs the initial population of the log-widget.

    # Variable for the state of the autosave button. Has to be accessed by the button-functions.
    global autoSave
    autoSave = customtkinter.BooleanVar(value=True)

    # StringVar for text displaying total progress.
    global progressText
    progressText = progress_text

    # Progressbar.
    global progressBar
    progressBar = progress_bar

    # Initial update of the progress text and bar.
    misc.update_progress(footballTrip, progressText, progressBar, payGoal)


# -------------------------- |
# ---- Button functions ---- |
# -------------------------- V
# These functions all follow the same general structure:
# - In a list, specify all the given validation-steps that has to be made for the user to have done the right thing
# - Pass this list to the validation handler and remember what it returns. The validation handler will apply the user
# input to the validation functions and return the inputs legitimacy. In example, if the user wrote letters in the
# entry-field for a transaction-amount the _vali_input_legitimacy() function would return false with an error-message.
# - Next we can test if there were any errors and return if there was.
# - If not we can log the return-message, update the log-widget and save the data if autosave is on.
# - Lastly the opened window will be closed and the various different widgets displaying progress will be updated.

# This is all done in an attempt to reuse the different validation-functions for each of the button-functions, while
# still keeping track of everything that goes right (the log) and wrong (error-messages).

# Function that gets called when you press the "foretag transaktion" button.
def make_transaction_button(window, error_label_text, person: str, amount: str, txn_type: str):
    validation = [lambda: _vali_person(person),
                  lambda: _vali_input_legitimacy(amount),
                  lambda: _vali_transaction(person, amount, txn_type)]
    success, msg, logType = misc.general_validation_handler(validation, error_label_text)
    if not success:
        return

    lg.log(msg, logType)
    lg.update_log_frame(logWidget, logFilters)
    if autoSave.get():
        misc.save_data(tree, footballTrip, payGoal)
    window.destroy()
    misc.update_progress(footballTrip, progressText, progressBar, payGoal)


# Function that gets called when you press the "tilføj medlem" button.
def add_member_button(window, error_label_text, person, start_amount):
    validation = [lambda: _vali_person(person, add=True),
                  lambda: _vali_input_legitimacy(start_amount),
                  lambda: _vali_add_member(person, start_amount)]
    success, msg, logType = misc.general_validation_handler(validation, error_label_text)
    if not success:
        return

    lg.log(msg, logType)
    lg.update_log_frame(logWidget, logFilters)
    if autoSave.get():
        misc.save_data(tree, footballTrip, payGoal)
    window.destroy()
    misc.update_progress(footballTrip, progressText, progressBar, payGoal)


# Function that gets called when you press the "fjern medlem" button.
def rem_member_button(window, error_label_text, person, keep_money: bool = False):
    validation = [lambda: _vali_person(person),
                  lambda: _vali_rmv_member(person, keep_money)]
    success, msg, logType = misc.general_validation_handler(validation, error_label_text)
    if not success:
        return

    lg.log(msg, logType)
    lg.update_log_frame(logWidget, logFilters)
    if autoSave.get():
        misc.save_data(tree, footballTrip, payGoal)
    window.destroy()
    misc.update_progress(footballTrip, progressText, progressBar, payGoal)


# Sorts the footballTrip dictionary that holds all the data and returns the 3 people with the lowest amount paid.
def leaderboard_of_shame_button():
    sortedDict: list = sorted(footballTrip.items(), key=lambda x: x[1])
    return sortedDict[:3]

# -------------------------- ^
# ---- Button functions ---- |
# -------------------------- |


# Passer-function thingy ma-jig for log filter switches.
def pass_log_widget_update() -> list[tuple[str, str, str]]:
    return lg.update_log_frame(logWidget, logFilters)


# Passer-function thingy ma-jig for selected tree-view item.
def pass_get_selected(selected_from) -> tuple[str, int]:
    return misc.get_selected(selected_from)


# -------------------------- |
# ----- Error handling ----- |
# -------------------------- v

# Validates the legitimacy of the person. Makes sure that nothing went wrong and that the person actually exists or not,
# respectively in the cases of for example making a transaction or adding a person.
def _vali_person(person, add=False) -> tuple[bool, str, str]:
    # If the person isn't in the dictionary, an error has occurred and the function return with and error-message.
    if person not in footballTrip.keys():
        if add:
            return True, "The person is safe to be added.", "safeAdd"
        return False, "you make stupid error, no person with that name.", "nameNoExist"
    else:
        return True, "Completion case - my method bad :(.\nEverything went smoothly.", "compCase"


# Validates that the money-amount specified by the user is valid; no negative numbers, letters or decimals.
def _vali_input_legitimacy(amount) -> tuple[bool, str, str]:
    # If the user pressed the confirm button without writing anything.
    if amount == "":
        return False, "Du har jo ikke skrevet noget... -_-.", "noUserInput"

    # Try to convert the string from the entry-field to an integer number.
    try:
        amount = int(amount)
    except ValueError:
        return False, ("Forventede et heltal men modtog: " + '"' + f"{amount}" + '"' +
                       "\nTjek lige dit beløb for bogstaver eller decimaltal."), "noInt"

    # If the amount is less than zero, return with error.
    if amount < 0:
        return False, "Negative beløb er ikke tilladt.", "negInt"
    else:
        return True, "Completion case - my method bad :(.\nEverything went smoothly.", "compCase"

# -------------------------- ^
# ----- Error handling ----- |
# -------------------------- |


# -------------------------- |
# ----- Main validation ---- |
# -------------------------- V

# Calls the correct function depending on what transaction-type the user has chosen.
def _vali_transaction(person, amount, txn_type: str) -> tuple[bool, str, str]:
    match txn_type:
        case "Indbetaling":
            return _vali_amount_deposit(person, amount)
        case "Udbetaling":
            return _vali_amount_retract(person, amount)
        case _:
            return False, "Vælg en transaktionstype.", "selTxnType"


# Validates if the amount specified by the user is able to be deposited into the account.
def _vali_amount_deposit(person, amount) -> tuple[bool, str, str]:
    # Variable for storing the current amount of money each person should pay.
    totalPerPerson: int = misc.total_per_person(footballTrip, payGoal)
    amount = int(amount)
    print(footballTrip[person])
    # If the person has already paid the full amount, the function returns.
    if footballTrip[person] == totalPerPerson:
        return False, "Personen har allerede betalt\ndet fulde beløb.", "noDebt"
    # If the amount to be paid is larger than the debt, only the debt will be paid.
    elif (footballTrip[person] + amount) > totalPerPerson:
        newAmount: int = totalPerPerson
        footballTrip[person] = newAmount
        return True, (f"Det forsøgte beløb på {amount} kr.\nvar for stort. "
                      f"Indbetalte {newAmount} kr.\nfor {person}."), "debtClear"
    else:
        footballTrip[person] += amount
        return True, f"Indbetalte {amount} kr. for\n{person}.", "normPay"


# Validates if the amount specified by the user is able to be retracted from the account.
def _vali_amount_retract(person, amount) -> tuple[bool, str, str]:
    amount = int(amount)

    # If the person haven't paid anything yet.
    if footballTrip[person] <= 0:
        return False, f"{person} har intet indbetalt beløb.", "noPayments"
    # If the amount to be retracted is larger than the amount paid, only the amount paid will be retracted.
    elif (footballTrip[person] - amount) < 0:
        newAmount = footballTrip[person]
        footballTrip[person] -= newAmount
        return True, (f"Det forsøgte beløb på {amount} kr.\nvar for stort. "
                      f"Fratrak {newAmount} kr. for\n{person}."), "insufficientFunds"
    else:
        footballTrip[person] -= amount
        return True, f"Fratrak {amount} kr. for\n{person}.", "normRetract"


# Add a member from the football club to the system.
# The user decides whether the person will have a start-amount paid in their name.
def _vali_add_member(person, start_amount: int = 0) -> tuple[bool, str, str]:
    person = misc.format_string(person, with_space=True)

    if person in footballTrip.keys():
        return False, f"{person} er allerede en indbetaler.\nOvervej eventuelt at bruge et kælenavn.", "dupePerson"
    else:
        footballTrip[person] = int(start_amount)
        return True, f"{person} er nu indlagt som en\nindbetaler med et startbeløb på {start_amount} kr.", "normAddMem"


# Remove a member from the football club from the system.
# The user decides whether the member is able to get their money back.
def _vali_rmv_member(person: str, keep_money: bool = False) -> tuple[bool, str, str]:
    footballTrip.__delitem__(person)
    return True, f"{person} er blevet fjernet\nsom medlem.", "normRmvMem"

# -------------------------- ^
# ----- Main validation ---- |
# -------------------------- |
