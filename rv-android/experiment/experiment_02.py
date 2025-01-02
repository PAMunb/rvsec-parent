import logging as logging_api
import os.path
import shutil

# import analysis.methods_extractor as me
from experiment.memory import Memory
import analysis.reachable_methods_mop as reach
import analysis.results_analysis as res
import utils
from android import Android
from app import App
from commands.command import Command
from constants import EXTENSION_APK
from constants import EXTENSION_METHODS
from experiment import config as x
from experiment.execution import ExecutionManager
# from task import Task
from experiment.task import Task
from rvandroid import RvAndroid
from rvsec import RVSec
from settings import *
from tools.tool_spec import AbstractTool
from datetime import datetime

logging = logging_api.getLogger(__name__)

apks_map: dict[str, App] = {}
tools_map: dict[str, AbstractTool] = {}
rerun = True


def execute():
    _execute(x.repetitions, x.timeouts, x.tools, x.memory_file, x.generate_monitors,
             x.instrument, x.static_analysis, x.skip_experiment, x.no_window)


def _execute(repetitions: int, timeouts: list[int], tools: list[AbstractTool], memory_file="", generate_monitors=True,
             instrument=True, static_analysis=True, skip_experiment=False, no_window=False):
    logging.info("Executing Experiment ...")

    # memory_file indicates whether to
    #  - resume the experiment run (based on file content), OR
    #  - start a new run (blank value)
    # If you are going to continue an execution, it is not necessary to pre-process the apks again ...
    if not memory_file:
        # generate monitors, instrument APKs and run static analysis
        pre_process_apks(generate_monitors, instrument, static_analysis, INSTRUMENTED_DIR)

    if not skip_experiment:
        # run experiment
        exec_manager = run_experiment(repetitions, timeouts, tools, memory_file, no_window)
        # post processing
        post_process(exec_manager.base_results_dir)

    logging.info('Finished !!!')


def run_experiment(repetitions: int, timeouts: list[int], tools: list[AbstractTool], memory_file: str, no_window: bool):
    # retrieve the instrumented apks
    apks: list[App] = utils.get_apks(INSTRUMENTED_DIR)
    logging.info(f"Instrumented APKs: {len(apks)}")

    # creates map between names and objects
    init_maps(apks)

    # initialize execution memory
    exec_manager = ExecutionManager()
    # exec_order = lambda x: (x.repetition, x.timeout, x.tool, x.apk)
    exec_order = lambda x: (x.apk, x.repetition, x.timeout, x.tool)
    exec_manager.create_memory(apks, repetitions, timeouts, tools, memory_file, exec_order)

    # execute tasks
    for task in exec_manager.tasks:
        if task.executed:
            logging.info(f"Skipping already executed task: {task}")
        else:
            run(task, exec_manager, no_window)
    logging.info(f"Execution memory file: {exec_manager.memory_file}")

    logging.info(f"Verifying execution status: {exec_manager.statistics()}")
    for _ in range(3):  # 3 retries
        status = exec_manager.statistics()
        if status["pct"] == 100:
            break
        for task in exec_manager.tasks:
            if not task.executed:
                run(task, exec_manager, no_window)

    return exec_manager


def run(task, exec_manager, no_window):
    try:
        exec_manager.start_task(task)
        run_task(task, no_window)
        post_process_task(task)
        exec_manager.finish_task(task)
        logging.info(f"Status: {exec_manager.statistics()}")
    except Exception as ex:
        exec_manager.task_error(task, ex)
        error_msg = f"Error while running task: {task}. {ex}"
        logging.error(error_msg)


def run_task(task: Task, no_window: bool):
    logging.info(f"Running: {task}")

    logcat_cmd = Command("adb", ["logcat", "-v", "threadtime", "-s", "RVSEC", "RVSEC-COV"])

    app = apks_map[task.apk]

    time.sleep(5)
    android = Android()
    with android.create_emulator(AVD_NAME, no_window) as _:
        android.install_with_permissions(app)
        with open(task.logcat_file, "wb") as log_cat:
            proc = logcat_cmd.invoke_as_deamon(stdout=log_cat)
            tool = tools_map[task.tool]
            task.start_time = datetime.now()  # update start_time (after emulator is up)
            tool.execute(app, task.timeout, task.log_file)
            proc.kill()


def pre_process_apks(generate_monitors: bool, instrument: bool, static_analysis: bool, base_results_dir: str):
    logging.info("Pre-processing APKs ...")
    logging.debug(f"Generate monitors? {generate_monitors}")
    logging.debug(f"Instrument APKs? {instrument}")
    logging.debug(f"Run static analysis? {static_analysis}")
    if generate_monitors:
        rvsec = RVSec()
        rvsec.generate_monitors()
    if instrument:
        rvandroid = RvAndroid()
        rvandroid.instrument_apks(results_dir=base_results_dir)
    if static_analysis:
        extract_all_methods()


def post_process_task(task: Task):
    logging.debug(f"Post-processing task: {task}")
    # import analysis.logcat_parser as logcat_parser
    #
    # print(f"logcat_file={task.logcat_file}")
    #
    # rvsec_errors, called_methods = logcat_parser.parse_logcat_file(task.logcat_file)
    #
    # print(f"ERROS ({len(rvsec_errors)}) ................................................")
    # errors = []
    # for error in rvsec_errors:
    #     print(error)
    #     errors.append({
    #         "date": error["date"],
    #         "error": error["original"]
    #     })
    # # task.result = errors
    #
    # # import analysis.coverage as cov
    # # methods_file_name = task.apk + EXTENSION_METHODS
    # # methods_file = os.path.join(task.results_dir, methods_file_name)
    # # if os.path.exists(methods_file):
    # #     all_methods = reach.read_reachable_methods(methods_file)
    # #     task.coverage = cov.process_coverage(called_methods, all_methods)
    # coverage = []
    # print("CALLED_METHODS ..........................................")
    # print(called_methods)
    # for clazz in called_methods:
    #     for method_name in called_methods[clazz]["methods"]:
    #         method = called_methods[clazz]["methods"][method_name]
    #         method_str = "{}.{}".format(clazz, method_name)
    #         coverage.append({
    #             "date": method["date"],
    #             "original": method["original"]
    #         })
    # # task.coverage = coverage
    #
    # print(f"post_process_task={task}")


def post_process(base_results_dir: str):
    logging.info("Processing results")
    res.process_results(base_results_dir)


def extract_all_methods():
    logging.info("Extracting methods")
    for file in os.listdir(INSTRUMENTED_DIR):
        if file.casefold().endswith(EXTENSION_APK):
            app = App(os.path.join(APKS_DIR, file))
            methods_file_name = app.name + EXTENSION_METHODS
            methods_file = os.path.join(INSTRUMENTED_DIR, methods_file_name)
            if not os.path.exists(methods_file):
                # class,is_activity,method,reachable,use_jca
                reach.extract_reachable_methods(app.path, methods_file)


def init_maps(apps: list[App]):
    for apk in apps:
        apks_map[apk.name] = apk
    for tool in x.available_tools:
        tools_map[tool.name] = tool


def copy_methods_file(app: App, app_results_dir: str):
    methods_file_name = app.name + EXTENSION_METHODS
    methods_file = os.path.join(INSTRUMENTED_DIR, methods_file_name)
    if os.path.exists(methods_file):
        shutil.copy(methods_file, app_results_dir)
    else:
        # TODO excecao? ... nao tem como tratar a cobertura depois
        pass
