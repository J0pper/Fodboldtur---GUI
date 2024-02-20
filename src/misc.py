import os
import pickle as pkl
import tkinter as tk
import re
from typing import NoReturn


data_file_name: str = "../data/betalinger.pk"

def load_data() -> tuple[dict, str, str]:
    if not os.path.isfile(data_file_name):
        _data_init(data_file_name)
        return {}, "Den tidligere datafil blev ikke fundet, så en ny er blevet lavet og indlæst.", "fileLoadFail"

    with open(data_file_name, "rb") as dataFile:
        footballTrip: dict = pkl.load(dataFile)
    return footballTrip, "Data loadet succesfuldt.", "fileLoadSuccess"


def save_data(treeview, modded_fb_trip: dict, pay_goal: int) -> tuple[dict, str, str]:
    if not os.path.isfile(data_file_name):
        _data_init(data_file_name)
        return {}, "Den tidligere datafil blev ikke fundet, så en ny er blevet lavet og indlæst.", "fileLoadFail"

    with open(data_file_name, "wb") as dataFile:
        pkl.dump(modded_fb_trip, dataFile)

    update_treeview(treeview, load_data()[0], pay_goal)
    return load_data()[0], "Data gemt succesfuldt.", "saveSuccess"


def _data_init(file_name):
    with open(file_name, "wb") as dataFile:
        pkl.dump({}, dataFile)


def update_treeview(treeview, content: dict, pay_goal: int):
    for item in treeview.get_children():
        treeview.delete(item)

    information: list = []
    for key, val in content.items():
        information.append((key, val, total_per_person(content, pay_goal)-int(val)))

    for info in information:
        treeview.insert('', index=tk.END, text=info[0], values=(info[1], info[2]))


def general_validation_handler(funcs_to_validate: list, error_label_text) -> tuple[bool, str, str]:
    # pycharm doesn't like that I may not have initialized these variables
    success, msg, logType = None, None, None

    for func in funcs_to_validate:
        success, msg, logType = func()
        if not success:
            error_label_text.set(msg)
            return success, msg, logType
    return success, msg, logType


# Calculated the amount each member has to pay for the trip. The amount varies depending on the number of members.
def total_per_person(dic: dict, pay_goal: int) -> int:
    memberAmount: int = len(dic.items())
    return round(pay_goal / memberAmount)


# Formats a string to only capitalize the first letters of each word.
# The user can specify if they want the name as one or two words.
def format_string(text: str, with_space: bool = False) -> str:
    text = text.lower().title().replace(" ", "")
    if with_space:
        return re.sub(r"(?<=\w)([A-Z])", r" \1", text)
    return text


# Gets the selected item from a treeview-widget.
def get_selected(selected_from) -> tuple[str, int]:
    selected: list = []
    for i in selected_from.selection():
        selected = selected_from.item(i)
    return selected['text'], selected['values'][0]


# Updates the progressbar and label displaying the total amount paid.
def update_progress(data: dict, progress_text, progress_bar, pay_goal: int) -> NoReturn:
    totalPaid: int = 0
    for amount in data.values():
        totalPaid += amount
    progress_text.set(f"{totalPaid}/{pay_goal} rupees indsamlet.")
    progress_bar.set(totalPaid / pay_goal)
    return NoReturn
