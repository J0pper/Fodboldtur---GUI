import logging as lg
import misc


def shiddy_init(treeview_widget, log_frame_widget):
    global tree
    tree = treeview_widget

    global footballTrip
    footballTrip, msg = misc.load_data()
    lg.log(msg)

    misc.update_treeview(tree, footballTrip)

    global log_widget
    log_widget = log_frame_widget
    lg.update_logframe(log_widget)


def make_transaction(window, error_label_text, person, amount, txn_type: str):
    validation = [lambda: _vali_person(person),
                  lambda: _vali_input_legitimacy(amount),
                  lambda: _vali_transaction(person, amount, txn_type)]
    success, msg = misc.general_validation_handler(validation, error_label_text)
    if not success:
        return

    lg.log(msg)
    lg.update_logframe(log_widget)
    misc.save_data(tree, footballTrip)
    window.destroy()


def add_member(window, error_label_text, person, start_amount):
    validation = [lambda: _vali_person(person, add=True),
                  lambda: _vali_input_legitimacy(start_amount),
                  lambda: _vali_add_member(person, start_amount)]
    success, msg = misc.general_validation_handler(validation, error_label_text)
    if not success:
        return

    lg.log(msg)
    lg.update_logframe(log_widget)
    misc.save_data(tree, footballTrip)
    window.destroy()


def rem_member(window, error_label_text, person, keep_money: bool = False):
    validation = [lambda: _vali_person(person),
                  lambda: _vali_rem_member(person, keep_money)]
    success, msg = misc.general_validation_handler(validation, error_label_text)
    if not success:
        return

    lg.log(msg)
    lg.update_logframe(log_widget)
    misc.save_data(tree, footballTrip)
    window.destroy()


# -------------------------- |
# ----- Error handling ----- |
# -------------------------- v
def _vali_person(person, add=False) -> tuple[bool, str]:
    # If the person isn't in the dictionary, an error has occurred and the function return with and error-message.
    if person not in footballTrip.keys():
        if add:
            return True, "The person is safe to be added."
        return False, "you make stupid error, no person with that name."
    else:
        return True, "Completion case - my method bad :(. Everything went smoothly."


def _vali_input_legitimacy(amount) -> tuple[bool, str]:
    # If the user pressed the confirm button without writing anything.
    if amount == "":
        return False, "Du har jo ikke skrevet noget... -_-."

    # Try to convert the string from the entry-field to an integer number.
    try:
        amount = int(amount)
    except ValueError:
        return False, ("Forventede et heltal men modtog: " + '"' + f"{amount}" + '"' +
                       "\nTjek lige dit beløb for bogstaver eller decimaltal.")

    # If the amount is less than zero, return with error.
    if amount < 0:
        return False, "Negative beløb er ikke tilladt."
    else:
        return True, "Completion case - my method bad :(. Everything went smoothly."
# -------------------------- ^
# ----- Error handling ----- |
# -------------------------- |


def _vali_transaction(person, amount, txn_type: str) -> tuple[bool, str]:
    match txn_type:
        case "Indbetaling":
            print("indbetaling")
            return _vali_amount_deposit(person, amount)
        case "Udbetaling":
            print("udbetaling")
            return _vali_amount_retract(person, amount)
        case _:
            return False, "Vælg en transaktionstype."


def _vali_amount_deposit(person, amount) -> tuple[bool, str]:
    # Variable for storing the current amount of money each person should pay.
    totalPerPerson: float = misc.total_per_person(footballTrip)
    amount = float(amount)

    # If the person has already paid the full amount, the function returns.
    if footballTrip[person] == totalPerPerson:
        return False, "Personen har allerede betalt det fulde beløb."
    # If the amount to be paid is larger than the debt, only the debt will be paid and the function will return with a
    elif (footballTrip[person] + amount) > totalPerPerson:
        newAmount: float = totalPerPerson
        footballTrip[person] = newAmount
        return True, f"Det forsøgte beløb på {amount} kr. var for stort. Indbetalte {newAmount} kr. for {person}."
    else:
        footballTrip[person] += amount
        return True, f"Indbetalte {amount} kr. for {person}."


def _vali_amount_retract(person, amount) -> tuple[bool, str]:
    # Variable for storing the current amount of money each person should pay.
    totalPerPerson: float = misc.total_per_person(footballTrip)

    amount = float(amount)

    # If the person haven't paid anything yet.
    if footballTrip[person] <= 0:
        return False, f"{person} har intet indbetalt beløb."
    # If the amount to be retracted is larger than the amount paid, only the amount paid will be retracted.
    elif (footballTrip[person] - amount) < totalPerPerson:
        newAmount = footballTrip[person]
        footballTrip[person] -= newAmount
        return True, f"Det forsøgte beløb på {amount} kr. var for stort. Fratrak {newAmount} kr. for {person}."
    else:
        footballTrip[person] -= amount
        return True, f"Fratrak {amount} kr. for {person}."


# Add a member from the football club to the system.
# The user decides whether the person will have a start-amount paid in their name.
def _vali_add_member(person, start_amount: int = 0) -> tuple[bool, str]:
    person = misc.format_string(person, with_space=True)

    if person in footballTrip.keys():
        return False, f"{person} er allerede en indbetaler.\nOvervej eventuelt at bruge et kælenavn."
    else:
        footballTrip[person] = start_amount
        return True, f"{person} er nu indlagt som en indbetaler med et startbeløb på {start_amount} kr."


# Remove a member from the football club from the system.
# The user decides whether the member is able to get their money back.
def _vali_rem_member(person, keep_money: bool = False) -> tuple[bool, str]:
    footballTrip.__delitem__(person)
    return True, f"{person} er blevet fjernet som medlem."


# Sorter dictionary efter størrelse af nøglerne respektive værdier og print de tre individer, der har indbetalt mindst.
def poor_people_leaderboard(dictionary: dict):
    sortedDict: list = sorted(dictionary.items(), key=lambda x: x[1])
    for i in range(3):
        print(sortedDict[i])
