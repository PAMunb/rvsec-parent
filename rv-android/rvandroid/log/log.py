from datetime import datetime

from rvandroid import utils


class RvError:

    def __init__(self, spec: str, error_type: str, class_full_name: str, method: str, source: str, message: str):
        self.spec = spec
        self.error_type = error_type
        self.class_full_name = class_full_name
        self.method = method
        self.source = source
        self.message = message
        #################################
        self.unique_msg: str = "{}:::{}:::{}:::{}:::{}"\
            .format(class_full_name, method, spec, error_type, message)
        self.original_msg: str = ""
        # self.time = time or int(datetime.now().timestamp())
        self.time_occurred: datetime = datetime.now()
        self.time_since_task_start: int = 0  # in seconds

    def to_json(self):
        return {
            'spec': self.spec,
            'error_type': self.error_type,
            'class_full_name': self.class_full_name,
            'method': self.method,
            'message': self.message,
            "time_occurred": utils.datetime_to_milliseconds(self.time_occurred),
            "time_since_task_start": self.time_since_task_start
            # "unique_msg": self.unique_msg
            # 'recorded_at': utils.datetime_to_milliseconds(self.time_occurred),
            # "delay": self.time_since_task_start
        }

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def __str__(self):
        return f"RvError(spec={self.spec}, type={self.error_type}, classFullName={self.class_full_name}, method={self.method}, message={self.message}, time_occurred={self.time_occurred}, time_since_task_start={self.time_since_task_start})"

    def __repr__(self):
        return f"{self.unique_msg}:{self.time_occurred}"

    def __hash__(self):
        return hash(self.unique_msg)

    def __eq__(self, other):
        if not isinstance(other, RvError):
            return NotImplemented
        return self.unique_msg == other.unique_msg


class RvCoverage:

    def __init__(self, clazz: str, method: str, params: str):
        self.clazz = clazz
        self.method = method
        self.params = params
        #################################
        self.unique_msg: str = "{}:::{}:::{}" \
            .format(clazz, method, params)
        self.original_msg: str = ""
        self.time_occurred: datetime = datetime.now()
        self.time_since_task_start: int = 0  # in seconds

    @property
    def signature(self):
        return "{}.{}{}" \
            .format(self.clazz, self.method, self.params)

    def __str__(self):
        return f"RvCoverage(clazz={self.clazz}, method={self.method}, params={self.params}, time_occurred={self.time_occurred}, time_since_task_start={self.time_since_task_start})"

    def __repr__(self):
        return f"{self.unique_msg}:{self.time_occurred}"

    def __hash__(self):
        return hash(self.unique_msg)

    def __eq__(self, other):
        if not isinstance(other, RvCoverage):
            return NotImplemented
        return self.unique_msg == other.unique_msg
