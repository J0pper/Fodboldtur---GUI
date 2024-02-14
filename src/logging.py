import os
import pickle as pkl
import customtkinter

logFileName: str = "data/log.pkl"


def update_logframe(log_widget):
    log_info = _read_log()
    for logIndex, msg in log_info.items():
        customtkinter.CTkLabel(master=log_widget, text=f"{logIndex}: {msg}")\
            .grid(row=list(log_info.keys()).index(logIndex), padx=10, pady=(0, 5), sticky="w")


def log(msg) -> dict:
    if not os.path.isfile(logFileName):
        _log_init(msg)
    else:
        logDict: dict = _read_log()
        _write_log(logDict, msg)
    return _read_log()


def load_log() -> dict:
    return _read_log()


def clear_log() -> dict:
    with open(logFileName, "wb") as logFile:
        pkl.dump({}, logFile)
    return _read_log()


# ---------------------------
# ---- Private functions ----
# ------ Do not access ------
# --------- outside ---------
# ---------------------------
def _log_init(msg: str):
    with open(logFileName, "wb") as logFile:
        pkl.dump({"log1": msg}, logFile)


def _read_log() -> dict:
    with open(logFileName, "rb") as logFile:
        logDict: dict = pkl.load(logFile)
    return logDict


def _write_log(log_dict: dict, msg: str):
    with open(logFileName, "wb") as logFile:
        log_dict[f"log{len(log_dict.keys()) + 1}"] = msg
        pkl.dump(log_dict, logFile)
