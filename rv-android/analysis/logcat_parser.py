import re
from datetime import datetime
import utils

def parse_logcat_file(log_file: str):
    called_methods = {}
    rvsec_error_msgs = set()
    errors = []
    for entry in __parse_logcat(log_file):
        message = entry["message"]
        date = __to_datetime(entry["date"], entry["time"])
        if "RVSEC" == entry["tag"]:
            error = __parse_error(message)
            # error["date"] = utils.datetime_to_milliseconds(date)
            error["date"] = date
            error["original"] = entry["original"]
            unique_msg = error["unique_msg"]
            if unique_msg not in rvsec_error_msgs:
                rvsec_error_msgs.add(unique_msg)
                errors.append(error)
        elif "RVSEC-COV" == entry["tag"]:
            clazz, method, params = __parse_coverage(message)
            # sig = method + params
            # called_methods.setdefault(clazz, set()).add({
            #     "date": date,
            #     "method": method,
            #     "params": params,
            #     "original": entry["original"]
            # })

            # original_message = entry["original"]
            # if original_message not in

            if clazz not in called_methods:
                called_methods[clazz] = {"methods": {}}
            if method not in called_methods[clazz]["methods"]:
                called_methods[clazz]["methods"][method] = {
                    # "date": utils.datetime_to_milliseconds(date),
                    "date": date,
                    "params": params,
                    "original": entry["original"]
                }
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


def __parse_coverage(message: str):
    sp = message.split(":::")

    clazz = sp[0].strip()
    method = sp[1].strip()
    params = sp[2].strip()

    return clazz, method, params


def __parse_error(message: str):
    s = message.split(",")
    msg = " ".join(s[6:])
    unique_msg = "{}:::{}:::{}:::{}:::{}".format(s[1], s[3], s[0], s[5], msg)

    error = {
        "spec": s[0],
        "classFullName": s[1],
        "class": s[2],
        "method": s[3],
        "source": s[4],
        "type": s[5],
        "message": msg,
        "unique_msg": unique_msg
    }

    return error


def __to_datetime(date: str, time: str):
    # date: MONTH-DAY (logcat threadtime tag does not print year)
    year = datetime.now().year
    # %f = microseconds (6 digits)
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_str = f"{year}-{date} {time}"
    return datetime.strptime(date_str, date_format)
