import os
import pickle as pkl
import customtkinter

logFileName: str = "data/log.pkl"


def update_logframe(log_widget):
    logInfo = _read_log()
    for logInstance in logInfo:
        logIndex, msg = logInstance
        customtkinter.CTkLabel(master=log_widget, text=f"{logIndex}: {msg}")\
            .grid(row=logInfo.index(logInstance), padx=10, pady=(0, 5), sticky="w")


def log(msg) -> list[tuple[str, str]]:
    if not os.path.isfile(logFileName):
        _log_init()

    logList: list[tuple[str, str]] = _read_log()
    _write_log(logList, msg)
    return _read_log()


def load_log() -> list[tuple[str, str]]:
    return _read_log()


def clear_log() -> list[tuple[str, str]]:
    with open(logFileName, "wb") as logFile:
        pkl.dump(list[tuple[str, str]], logFile)
    return _read_log()


# --------------------------- |
# ---- Private functions ---- |
# ------ Do not access ------ |
# --------- outside --------- |
# --------------------------- V

def _log_init():
    with open(logFileName, "wb") as logFile:
        pkl.dump([("log1", "Lavede ny log-fil.")], logFile)


def _read_log() -> list[tuple[str, str]]:
    with open(logFileName, "rb") as logFile:
        logList: list[tuple[str, str]] = pkl.load(logFile)
    return logList


def _write_log(log_list: list[tuple[str, str]], msg: str):
    with open(logFileName, "wb") as logFile:
        log_list.insert(0, (f"log{len(log_list)+1}", msg))
        pkl.dump(log_list, logFile)

# --------------------------- ^
# ---- Private functions ---- |
# ------ Do not access ------ |
# --------- outside --------- |
# --------------------------- |
