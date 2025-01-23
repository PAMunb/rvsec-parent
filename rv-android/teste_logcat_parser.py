from datetime import datetime
import re


def parse_logcat(log_file: str):
    pattern = r"(\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}\.\d{3})\s+(\d+)\s+(\d+)\s+(\w)\s+(\S+)\s*:\s*(.*)"
    with open(log_file, 'r') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                date, time, pid, tid, level, tag, message = match.groups()
                yield {
                    "date": date,
                    "time": time,
                    "datetime": to_datetime(date, time),
                    "pid": pid,
                    "tid": tid,
                    "level": level,
                    "tag": tag,
                    "message": message
                }


def parse_error(error: str):
    # MessageDigestSpec,br.unb.cic.cryptoapp.messagedigest.MessageDigestUtil,MessageDigestUtil,hash,Unknown Source:1,UnsafeAlgorithm,expecting one of {SHA-256, SHA-384, SHA-512} but found MD5.
    # pattern = r"(\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}\.\d{3})\s+(\d+)\s+(\d+)\s+(\w)\s+(\S+)\s*:\s*(.*)"
    pattern = r"(\w+),(\w+),(\w+),(\w+),(\w+),(\w+),\s*(.*)"

    match = re.match(pattern, error)
    if match:
        print(match.groups())


def execute(log_file):
    called_methods = {}
    rvsec_errors = set()
    for entry in parse_logcat(log_file):
        print(entry)
        if "RVSEC" == entry["tag"]:
            rvsec_errors.add(entry["message"])
        elif "RVSEC-COV" == entry["tag"]:
            clazz, method, params = __cov_method_sig(entry["message"])
            # sig = method + params
            if clazz not in called_methods:
                called_methods[clazz] = set()
            # called_methods[clazz].add(sig)
            called_methods[clazz].add(method)
    return rvsec_errors, called_methods


def __cov_method_sig(text: str):
    sp = text.split(":::")

    clazz = sp[0].strip()
    method = sp[1].strip()
    params = sp[2].strip()

    return clazz, method, params



def parse_log_message(message):
    """Parses a log message and extracts relevant information.

    Args:
        message (str): The log message to parse.

    Returns:
        dict: A dictionary containing the extracted information.
    """

    pattern = r"(?P<specification>\w+),(?P<class_full_name>.+),(?P<class_name>\w+),(?P<method_name>\w+),(?P<source>.+),(?P<type>\w+),(?P<message>.+)"
    match = re.match(pattern, message)

    if match:
        result = match.groupdict()
        # Extract additional information from the "message" field
        unsafe_algorithm_match = re.search(r"expecting one of ({.*}) but found (\w+)", result["message"])
        if unsafe_algorithm_match:
            result["expected_algorithms"] = unsafe_algorithm_match.group(1).split(", ")
            result["found_algorithm"] = unsafe_algorithm_match.group(2)
        return result
    else:
        return {}


def tmp00(msg):
    s = msg.split(",")
    erro = {
        "spec": s[0],
        "classFullName": s[1],
        "class": s[2],
        "method": s[3],
        "source": s[4],
        "type": s[5],
        "message": " ".join(s[6:])
    }

    return erro


def to_datetime(date: str, time: str):
    year = datetime.now().year
    # %f = microseconds (6 digits)
    date_format = "%Y-%m-%d %H:%M:%S.%f"

    date_str = f"{year}-{date} {time}"
    return datetime.strptime(date_str, date_format)




if __name__ == '__main__':

    #
    #
    # # print(to_datetime("10-29", "08:31:14.504"))
    # # print(to_datetime("10-29", "08:31:21.696"))
    # tmp = to_datetime("10-29", "08:31:21.696")
    # print(tmp)
    # print(type(tmp))
    # milliseconds = int(round(tmp.timestamp() * 1000))
    # print(milliseconds)
    #
    # milliseconds = utils.datetime_to_milliseconds(tmp)
    # print(milliseconds)
    # date = utils.milliseconds_to_datetime(milliseconds)
    # print(date)
    # print(type(tmp))
    #
    # exit(1)

    # log_messages = [
    #     "MessageDigestSpec,br.unb.cic.cryptoapp.messagedigest.MessageDigestUtil,MessageDigestUtil,hash,Unknown Source:1,InvalidSequenceOfMethodCalls,unknown",
    #     "CipherSpec,br.unb.cic.cryptoapp.cipher.CipherUtil,CipherUtil,des,Unknown Source:1,InvalidSequenceOfMethodCalls,unknown",
    #     "KeyGeneratorSpec,br.unb.cic.cryptoapp.cipher.CipherUtil,CipherUtil,des,Unknown Source:1,UnsafeAlgorithm,expecting one ofAES,HmacSHA256,HmacSHA384,HmacSHA512,HMAC-SHA256,HMAC/SHA256,HMAC-SHA384,HMAC/SHA384,HMAC/SHA512,HMAC-SHA512 but found DES."
    # ]
    #
    # for message in log_messages:
    #     print(tmp00(message))
    #     # parsed_data = parse_log_message(message)
    #     # print(parsed_data)

    # error = "MessageDigestSpec,br.unb.cic.cryptoapp.messagedigest.MessageDigestUtil,MessageDigestUtil,hash,Unknown Source:1,UnsafeAlgorithm,expecting one of {SHA-256, SHA-384, SHA-512} but found MD5."
    # parse_error(error)


    log_file = "/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/results/20241102083427/cryptoapp.apk/cryptoapp.apk__1__600__ape.logcat"  # Substitua pelo nome do seu arquivo
    # rvsec_errors, called_methods = execute(log_file)
    import log.logcat_parser as parser
    rvsec_errors, called_methods, _ = parser.parse_logcat_file(log_file)

    print("ERROS: {}".format(len(rvsec_errors)))
    for erro in rvsec_errors:
        print(erro)

    print("\n\nMETODOS ...........")
    for clazz in called_methods:
        print(clazz)
        for metodo in called_methods[clazz]["methods"]:
            m = called_methods[clazz]["methods"][metodo]
            print("   - {} ::: {}".format(metodo, m))


    # log = "/home/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/results/20231212113846/com.example.openpass_1.apk/com.example.openpass_1.apk__1__120__monkey.logcat"
    #
    # rvsec_errors, called_methods = logcat_parser.parse_logcat_file(log)
    #
    # for clazz in called_methods:
    #     print(clazz)
    #     for m in called_methods[clazz]:
    #         print("   - {}".format(m))
