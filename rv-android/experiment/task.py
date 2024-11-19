from enum import Enum
from datetime import datetime
import utils


DEFAULT_DATETIME = utils.milliseconds_to_datetime(0)


class Task:
    cont = 0

    def __init__(self, apk: str, repetition: int, timeout: int, tool: str, executed=False, start_time=DEFAULT_DATETIME, finish_time=DEFAULT_DATETIME):
        Task.cont += 1
        self.id = Task.cont
        self.tool = tool
        self.timeout = timeout
        self.repetition = repetition
        self.apk = apk
        self.executed = executed
        self.start_time: datetime = start_time # TODO inicializar com None
        self.finish_time: datetime = finish_time # TODO inicializar com None
        self.time: int = 0  # time (in seconds) it took to run
        self.result: list[dict] = []
        self.coverage = {}
        self.error = ""
        self.results_dir = ""
        self.logcat_file = ""
        self.log_file = ""

    def __str__(self):
        return "[id={}, apk={}, rep={}, timeout={}, tool={}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool)

    def __repr__(self):
        return "[{},{},{},{},{},{}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool, self.executed)
