import os
import pickle as pkl
import customtkinter
from typing import NoReturn

# Specifies the path to the log-file.
logFileName: str = "data/log.pkl"
# Specifies the list for the tkinter log-labels.
logLabels: list = []


# Takes the list of log-instances and updates the frame with the log-labels. First every label is destroyed and then
# drawn again with the most recent log-instance at the top.
def update_log_frame(log_widget, log_filters):
    for label in logLabels:
        label.destroy()

    logInfo = _read_log()
    for logInstance in logInfo:
        if not log_filters[logInstance[2]][1].get():
            continue
        logIndex, msg = logInstance[0], logInstance[1]
        logLabel = customtkinter.CTkLabel(master=log_widget, text=f"{logIndex}: {msg}", justify="left")
        logLabel.grid(row=logInfo.index(logInstance), padx=10, pady=(0, 5), sticky="w")
        logLabels.append(logLabel)


# Logs a certain message and log-type. If the log-file, for whatever reason, does not exist, a new one will be made.
def log(msg, log_type) -> list[tuple[str, str, str]]:
    if not os.path.isfile(logFileName):
        _log_init()

    logList: list[tuple[str, str, str]] = _read_log()
    _write_log(logList, msg, log_type)
    return _read_log()


# Passer-function for the private read-log function.
def load_log() -> list[tuple[str, str, str]]:
    return _read_log()


# Clears the log in case it becomes too large with too many log-instances.
def clear_log() -> list[tuple[str, str, str]]:
    with open(logFileName, "wb") as logFile:
        pkl.dump(list[tuple[str, str]], logFile)
    return _read_log()


# --------------------------- |
# ---- Private functions ---- |
# ------ Do not access ------ |
# --------- outside --------- |
# --------------------------- V

# Initializes a new log-file.
def _log_init():
    with open(logFileName, "wb") as logFile:
        pkl.dump([("log1", "Lavede ny log-fil.", "fileLoadFail")], logFile)


# Reads the log and passes a list of al log-instances.
def _read_log() -> list[tuple[str, str, str]]:
    with open(logFileName, "rb") as logFile:
        logList: list[tuple[str, str, str]] = pkl.load(logFile)
    return logList


# Writes to the logfile.
def _write_log(log_list: list[tuple[str, str, str]], msg: str, log_type: str) -> NoReturn:
    with open(logFileName, "wb") as logFile:
        log_list.insert(0, (f"log{len(log_list)+1}", msg, log_type))
        pkl.dump(log_list, logFile)
    return NoReturn

# --------------------------- ^
# ---- Private functions ---- |
# ------ Do not access ------ |
# --------- outside --------- |
# --------------------------- |
