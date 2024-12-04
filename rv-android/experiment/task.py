import os
from enum import Enum
from datetime import datetime
import utils
from constants import EXTENSION_LOGCAT, EXTENSION_TRACE, EXTENSION_METHODS, EXECUTION_MEMORY_FILENAME

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

    def init(self, base_results_dir: str):
        self.start_time = datetime.now()
        results_dir = os.path.join(base_results_dir, self.apk)
        self.results_dir = results_dir
        base_name = "{0}__{1}__{2}__{3}".format(self.apk, self.repetition, self.timeout, self.tool)
        self.logcat_file = os.path.join(results_dir, "{}{}".format(base_name, EXTENSION_LOGCAT))
        self.log_file = os.path.join(results_dir, "{}{}".format(base_name, EXTENSION_TRACE))

    def __str__(self):
        return "[id={}, apk={}, rep={}, timeout={}, tool={}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool)

    def __repr__(self):
        return "[{},{},{},{},{},{}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool, self.executed)
