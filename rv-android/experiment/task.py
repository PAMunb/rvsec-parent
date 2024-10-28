from enum import Enum

class TaskStatus(Enum):
    NOT_EXECUTED = 1
    EXECUTING = 2
    EXECUTED = 3
    ERROR = 4

class Task:
    cont = 0

    def __init__(self, apk: str, repetition: int, timeout: int, tool: str, executed=False):
        Task.cont += 1
        self.id = Task.cont
        self.tool = tool
        self.timeout = timeout
        self.repetition = repetition
        self.apk = apk
        self.executed = executed
        self.time: int = 0 # time it took to run
        self.result = {}
        self.coverage = {}

    def __str__(self):
        return "[id={}, apk={}, rep={}, timeout={}, tool={}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool)

    def __repr__(self):
        return "[{},{},{},{},{}]".format(self.id, self.apk, self.repetition, self.timeout, self.tool)
