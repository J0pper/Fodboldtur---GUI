import os
import pickle as pkl
import tkinter as tk
import re


data_file_name: str = "data/betalinger.pk"


def load_data() -> tuple[dict, str]:
    if not os.path.isfile(data_file_name):
        _data_init(data_file_name)
        return {}, "Den tidligere datafil blev ikke fundet, så en ny er blevet lavet og indlæst."

    with open(data_file_name, "rb") as dataFile:
        footballTrip: dict = pkl.load(dataFile)
    return footballTrip, "Data loadet succesfuldt."


def save_data(treeview, modded_fb_trip: dict) -> tuple[dict, str]:
    if not os.path.isfile(data_file_name):
        _data_init(data_file_name)
        return {}, "Den tidligere datafil blev ikke fundet, så en ny er blevet lavet og indlæst."

    with open(data_file_name, "wb") as dataFile:
        pkl.dump(modded_fb_trip, dataFile)

    update_treeview(treeview, load_data()[0])
    return load_data()[0], "Data gemt succesfuldt."


def _data_init(file_name):
    with open(file_name, "wb") as dataFile:
        pkl.dump({}, dataFile)


def update_treeview(treeview, content: dict):
    for item in treeview.get_children():
        treeview.delete(item)

    information: list = []
    for key, val in content.items():
        information.append((key, val, total_per_person(content)-int(val)))

    for info in information:
        treeview.insert('', index=tk.END, text=info[0], values=(info[1], info[2]))


def general_validation_handler(funcs_to_validate: list, error_label_text) -> tuple[bool, str]:
    for func in funcs_to_validate:
        success, msg = func()
        if not success:
            error_label_text.set(msg)
            return success, msg
    return success, msg


# Calculated the amount each member has to pay for the trip. The amount varies depending on the number of members.
def total_per_person(dic: dict):
    memberAmount: int = len(dic.items())
    return 4500 / memberAmount


# Formats a string to only capitalize the first letters of each word.
# The user can specify if they want the name as one or two words.
def format_string(text: str, with_space: bool = False) -> str:
    text = text.lower().title().replace(" ", "")
    if with_space:
        return re.sub(r"(?<=\w)([A-Z])", r" \1", text)
    return text
