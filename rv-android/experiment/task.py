from enum import Enum


# class TaskStatus(Enum):
#     NOT_EXECUTED = 1
#     EXECUTING = 2
#     EXECUTED = 3
#     ERROR = 4


class Task:
    cont = 0

    def __init__(self, apk: str, repetition: int, timeout: int, tool: str, executed=False, start_time=0):
        Task.cont += 1
        self.id = Task.cont
        self.tool = tool
        self.timeout = timeout
        self.repetition = repetition
        self.apk = apk
        self.executed = executed
        self.start_time = start_time  # time.time(): Return the current time in seconds since the Epoch
        self.finish_time = 0
        self.time: int = 0  # time (in seconds) it took to run
        self.result: list[dict] = []
        self.coverage = {}
        self.error = {}
        self.results_dir = ""
        self.logcat_file = ""
        self.log_file = ""

    def __str__(self):
        return "[id={}, apk={}, rep={}, timeout={}, tool={}]".format(self.id, self.apk, self.repetition, self.timeout,
                                                                     self.tool)

    def __repr__(self):
        return "[{},{},{},{},{},{}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool, self.executed)
