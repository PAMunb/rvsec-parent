import json
import logging as logging_api
import os

import analysis.coverage as cov
import log.logcat_parser as parser
import analysis.reachable_methods_mop as reach
import utils
from constants import *
from constants import EXTENSION_LOGCAT, EXTENSION_METHODS, EXECUTION_MEMORY_FILENAME
from experiment.memory import Memory

logging = logging_api.getLogger(__name__)


def process_results(results_dir: str, save_file=True):
    logging.info("Processing results in: {}".format(results_dir))

    memory_file = os.path.join(results_dir, EXECUTION_MEMORY_FILENAME)
    print(f"process_results:::memory_file={memory_file}")
    memory = Memory.read(memory_file)

    results = initialize_results(results_dir, memory)
    for apk in results:
        process_apk(results[apk])

    if save_file:
        results_file = os.path.join(results_dir, RESULTS_FILENAME)
        json_formatted_str = json.dumps(results, indent=2)
        with open(results_file, "w") as outfile:
            outfile.write(json_formatted_str)
        logging.info("Results saved in: {}".format(results_file))

    return results


def process_apk(result):
    rvsec_errors = set()
    rvsec_methods_called = set()

    for rep in result[REPETITIONS]:
        err, met = process_execution(result[REPETITIONS][rep])
        rvsec_errors.update(err)
        rvsec_methods_called.update(met)

    result[RVSEC_ERRORS] = list(rvsec_errors)
    result[RVSEC_METHODS_CALLED] = list(rvsec_methods_called)


def process_execution(result):
    rvsec_errors = set()
    rvsec_methods_called = set()

    for timeout in result[TIMEOUTS]:
        err, met = process_timeout(result[TIMEOUTS][timeout])
        rvsec_errors.update(err)
        rvsec_methods_called.update(met)

    result[RVSEC_ERRORS] = list(rvsec_errors)
    result[RVSEC_METHODS_CALLED] = list(rvsec_methods_called)

    return rvsec_errors, rvsec_methods_called


def process_timeout(result):
    rvsec_errors = set()
    rvsec_methods_called = set()
    sum_act_cov = 0
    sum_method_cov = 0
    sum_method_jca_reachable_cov = 0

    for t in result[TOOLS]:
        tool = result[TOOLS][t]

        # tmp = tool[RVSEC_ERRORS]
        # c = tool[RVSEC_METHODS_CALLED]
        # print(tmp)
        # print(c)
        # print("")
        #
        # for e in tool[RVSEC_ERRORS]:
        #     if e["unique_msg"] not in rvsec_error_msgs:
        #         rvsec_error_msgs.add(e["unique_msg"])
        #         # rvsec_errors.append(e)
        #         rvsec_errors.append({
        #             "spec": e["spec"],
        #             "type": e["type"],
        #             "classFullName": e["classFullName"],
        #             "method": e["method"],
        #             "message": e["message"],
        #             ############ TODO guardar apenas o tempo (em sec) q levou pra achar ... task.start_time - e["date"]
        #             "time": utils.datetime_to_milliseconds(e["date"]),
        #             "unique_msg": e["unique_msg"]
        #         })
        rvsec_errors.update(tool[RVSEC_ERRORS]["messages"])
        rvsec_methods_called.update((tool[RVSEC_METHODS_CALLED]))
        sum_act_cov += tool[SUMMARY][ACTIVITIES_COVERAGE]
        sum_method_cov += tool[SUMMARY][METHOD_COVERAGE]
        sum_method_jca_reachable_cov += tool[SUMMARY][METHODS_JCA_COVERAGE]

    result[SUMMARY] = {ACTIVITIES_COVERAGE_AVG: (sum_act_cov / len(result[TOOLS])),
                       METHOD_COVERAGE_AVG: (sum_method_cov / len(result[TOOLS])),
                       METHODS_JCA_COVERAGE_AVG: (sum_method_jca_reachable_cov / len(result[TOOLS])),
                       RVSEC_ERRORS_COUNT: len(rvsec_errors)}
    # result[RVSEC_ERRORS] = {
    #     "total": len(rvsec_error_msgs),
    #     "messages": list(rvsec_error_msgs),
    #     "details": rvsec_errors
    # }
    result[RVSEC_ERRORS] = list(rvsec_errors)
    result[RVSEC_METHODS_CALLED] = list(rvsec_methods_called)

    return rvsec_errors, rvsec_methods_called


def initialize_results(results_dir: str, memory: Memory):
    results = {}
    if os.path.exists(results_dir) and os.path.isdir(results_dir):
        for apk_folder in os.listdir(results_dir):
            apk_folder_path = os.path.join(results_dir, apk_folder)
            if os.path.isdir(apk_folder_path):
                # read list_of.methods (CSV: class,is_activity,method,reachable,use_jca)
                all_methods = parse_all_methods_file(results_dir, apk_folder)
                for file in os.listdir(apk_folder_path):
                    if file.casefold().endswith(EXTENSION_LOGCAT):
                        # recupera informacoes contidas no nome do arquivo
                        apk, rep, timeout, tool = parse_filename(file)

                        if apk not in results:
                            results[apk] = {REPETITIONS: {}, SUMMARY: {},
                                            METHODS_JCA_REACHABLE: list(get_methods_jca_reachable(all_methods))}

                        if rep not in results[apk][REPETITIONS]:
                            results[apk][REPETITIONS][rep] = {TIMEOUTS: {}, SUMMARY: {}}

                        if timeout not in results[apk][REPETITIONS][rep][TIMEOUTS]:
                            results[apk][REPETITIONS][rep][TIMEOUTS][timeout] = {TOOLS: {}, SUMMARY: {}}

                        if tool not in results[apk][REPETITIONS][rep][TIMEOUTS][timeout][TOOLS]:
                            # le o arquivo de log e retorna:
                            # - o conjunto de erros (crypto misuse) encontrados
                            # - um mapa contendo os métodos chamados durante a execução (não conta a quantidade de vezes que foi chamado, apenas se foi chamado)
                            #   as chaves são os nomes das classes e o valor é o conjunto dos métodos chamados
                            rvsec_errors, called_methods = parser.parse_logcat_file(os.path.join(apk_folder_path, file))
                            task = memory.get_task(apk, rep, timeout, tool)
                            # print(f"task={task}")
                            rvsec_error_msgs = set()
                            errors = []
                            for err in rvsec_errors:
                                if err.unique_msg not in rvsec_error_msgs and task and task.executed:
                                    elapsed = (err.time_occurred - task.start_time).total_seconds()
                                    err.time_since_task_start = int(elapsed)

                                    rvsec_error_msgs.add(err.unique_msg)
                                    errors.append(err.to_json())

                            # TODO calcula a cobertura de codigo
                            coverage = cov.process_coverage(called_methods, all_methods)

                            results[apk][SUMMARY][TOTAL_CLASSES] = coverage[SUMMARY][TOTAL_CLASSES]
                            results[apk][SUMMARY][TOTAL_ACTIVITIES] = coverage[SUMMARY][TOTAL_ACTIVITIES]
                            results[apk][SUMMARY][TOTAL_METHODS] = coverage[SUMMARY][TOTAL_METHODS]
                            results[apk][SUMMARY][TOTAL_METHODS_JCA_REACHABLE] = coverage[SUMMARY][TOTAL_METHODS_JCA_REACHABLE]

                            summary = {CALLED_ACTIVITIES: coverage[SUMMARY][CALLED_ACTIVITIES],
                                       CALLED_METHODS: coverage[SUMMARY][CALLED_METHODS],
                                       CALLED_METHODS_JCA_REACHABLE: coverage[SUMMARY][CALLED_METHODS_JCA_REACHABLE],
                                       ACTIVITIES_COVERAGE: coverage[SUMMARY][ACTIVITIES_COVERAGE],
                                       METHOD_COVERAGE: coverage[SUMMARY][METHOD_COVERAGE],
                                       METHODS_JCA_COVERAGE: coverage[SUMMARY][METHODS_JCA_COVERAGE],
                                       RVSEC_ERRORS_COUNT: len(rvsec_errors)}

                            jca_methods_called = set()
                            for clazz in called_methods:
                                # TODO se a classe nao estiver em coverage provavelmente declarou um pacote no manifest e implementou as coisas em outro pacote
                                if clazz in coverage:
                                    methods = called_methods[clazz][METHODS]
                                    for method in methods:
                                        sig = "{}.{}".format(clazz, method)
                                        if sig not in jca_methods_called and \
                                                method in coverage[clazz][METHODS].keys() and \
                                                coverage[clazz][METHODS][method][CALLED] and \
                                                coverage[clazz][METHODS][method][USE_JCA]:
                                            jca_methods_called.add(sig)
                            rvsec_errors_dict = {
                                "total": len(rvsec_error_msgs),
                                "messages": list(rvsec_error_msgs),
                                "details": errors
                            }
                            tool_dict = {SUMMARY: summary,
                                         "start_time": utils.datetime_to_milliseconds(task.start_time),
                                         RVSEC_ERRORS: rvsec_errors_dict,
                                         RVSEC_METHODS_CALLED: list(jca_methods_called)}
                            results[apk][REPETITIONS][rep][TIMEOUTS][timeout][TOOLS][tool] = tool_dict
    return results


def get_methods_jca_reachable(all_methods):
    methods = set()
    for clazz in all_methods:
        for m in all_methods[clazz][METHODS]:
            if all_methods[clazz][METHODS][m][REACHABLE] and all_methods[clazz][METHODS][m][USE_JCA]:
                sig = "{}.{}".format(clazz, m)
                methods.add(sig)
    return methods


def parse_filename(name: str):
    # print("Parsing file: {}".format(name))
    parts = name.split("__")
    return parts[0], parts[1], parts[2], parts[3][:-len(EXTENSION_LOGCAT)]


def parse_all_methods_file(results_dir, apk_name):
    all_methods_file_name = apk_name + EXTENSION_METHODS
    all_methods_file = os.path.join(results_dir, apk_name, all_methods_file_name)
    all_methods = {}
    if os.path.exists(all_methods_file):
        all_methods = reach.read_reachable_methods(all_methods_file)
    return all_methods
