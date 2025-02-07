import os
from enum import Enum
from datetime import datetime
from rvandroid import utils
from rvandroid.constants import EXTENSION_LOGCAT, EXTENSION_TRACE

DEFAULT_DATETIME = utils.milliseconds_to_datetime(0)


class TaskStatus(Enum):
    CREATED = 1
    RUNNING = 2
    EXECUTED = 3


class Task:
    cont = 0

    def __init__(self, apk: str, repetition: int, timeout: int, tool: str, status=TaskStatus.CREATED, executed=False,
                 start_time=DEFAULT_DATETIME, finish_time=DEFAULT_DATETIME):
        Task.cont += 1
        self.id = Task.cont
        self.tool = tool
        self.timeout = timeout
        self.repetition = repetition
        self.apk = apk
        self.status = status
        self.executed = executed  # TODO deprecated ... fazer alteracoes para usar status
        self.start_time: datetime = start_time  # TODO inicializar com None
        self.finish_time: datetime = finish_time  # TODO inicializar com None
        self.time: int = 0  # time (in seconds) it took to run
        self.result: list[dict] = []  # TODO o q eh e onde esta sendo usado?
        self.coverage = {}  # TODO onde esta sendo usado?
        self.error = ""  # TODO onde esta sendo usado? e o q eh?
        self.results_dir = ""  # TODO onde esta sendo usado?
        self.logcat_file = ""
        self.log_file = ""

    def init(self, base_results_dir: str):
        self.start_time = datetime.now()
        self.status = TaskStatus.CREATED
        results_dir = os.path.join(base_results_dir, self.apk)
        self.results_dir = results_dir
        base_name = "{0}__{1}__{2}__{3}".format(self.apk, self.repetition, self.timeout, self.tool)
        self.logcat_file = os.path.join(results_dir, "{}{}".format(base_name, EXTENSION_LOGCAT))
        self.log_file = os.path.join(results_dir, "{}{}".format(base_name, EXTENSION_TRACE))

    def __str__(self):
        return "[id={}, apk={}, rep={}, timeout={}, tool={}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool)

    def __repr__(self):
        return "[{},{},{},{},{},{}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool, self.status)
