import re
from datetime import datetime
from log.log import RvError, RvCoverage
from typing import Dict
from constants import *


def parse_logcat_file(log_file: str):
    called_methods: dict[str, dict[str, dict[str, RvCoverage]]] = {}
    rvsec_error_msgs = set()
    errors: list[RvError] = []
    for entry in __parse_logcat(log_file):
        message = entry["message"]
        date = __to_datetime(entry["date"], entry["time"])
        if "RVSEC" == entry["tag"]:
            error = __parse_error(message)
            error.time_occurred = date
            error.original_msg = entry["original"]
            unique_msg = error.unique_msg
            if unique_msg not in rvsec_error_msgs:
                rvsec_error_msgs.add(unique_msg)
                errors.append(error)
        elif "RVSEC-COV" == entry["tag"]:
            cov: RvCoverage = __parse_coverage(message)
            if cov.clazz not in called_methods:
                called_methods[cov.clazz] = {METHODS: {}}
            if cov.method not in called_methods[cov.clazz][METHODS]:
                cov.time_occurred = date
                cov.original_msg = entry["original"]
                called_methods[cov.clazz][METHODS][cov.method] = cov
                #     {
                #     # "date": utils.datetime_to_milliseconds(date),
                #     "date": date,
                #     "params": params,
                #     "original": entry["original"]
                # }
            # called_methods[clazz].add(sig)
            # called_methods[clazz].add(method)
    return errors, called_methods


def __parse_logcat(log_file: str):
    pattern = r"(\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}\.\d{3})\s+(\d+)\s+(\d+)\s+(\w)\s+(\S+)\s*:\s*(.*)"
    with open(log_file, 'r') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                date, time, pid, tid, level, tag, message = match.groups()
                yield {
                    "date": date,
                    "time": time,
                    "pid": pid,
                    "tid": tid,
                    "level": level,
                    "tag": tag,
                    "message": message,
                    "original": line.strip()
                }


def __parse_coverage(message: str) -> RvCoverage:
    sp = message.split(":::")

    clazz = sp[0].strip()
    method = sp[1].strip()
    params = sp[2].strip()

    return RvCoverage(clazz, method, params)


def __parse_error(message: str) -> RvError:
    # if generic spec
    if message.endswith("went into an error state."):
        generic = __parse_error_generic_spec(message)
        return RvError(generic["spec"], generic["spec"], generic["class"],
                       generic["method"], generic["file_name"], generic["message"])
    else:
        # JCA spec
        s = message.split(",")
        return RvError(s[0], s[5], s[1], s[3], s[4], " ".join(s[6:]))


def __parse_error_generic_spec(log_line):
    pattern = r"(.*)\.(.*)\((.*):(.*)\) ::: (.*) went into an error state."
    match = re.match(pattern, log_line)

    if match:
        class_name, method_name, file_name, line_number, spec = match.groups()
        # file_name, line_number = file_info.split(":")
        return {
            "class": class_name,
            "method": method_name,
            "file_name": file_name,
            "line_number": int(line_number),
            "spec": spec,
            "message": "{} went into an error state.".format(spec)
        }
    else:
        return None


def __to_datetime(date: str, time: str) -> datetime:
    # date: MONTH-DAY (logcat threadtime tag does not print year)
    year = datetime.now().year
    # TODO remover depois de gerar as planilhas
    if year == 2025:
        year = 2024
    # %f = microseconds (6 digits)
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_str = f"{year}-{date} {time}"
    return datetime.strptime(date_str, date_format)
