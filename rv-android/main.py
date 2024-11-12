import argparse
import importlib
import json
import logging
import os
import sys
import time
from argparse import Namespace
from datetime import datetime

import utils
from experiment import config as experiment_config
from experiment import experiment_02
from tools.tool_spec import AbstractTool

available_tools: dict[str, AbstractTool] = {}

program_description = f'''
Executes the 'Experiment 02' ... 

Examples:    
$ python main.py --no_window -tools monkey droidbot -r 3 -t 120 300 600 900
$ python main.py --no_window -c PATH_TO_EXECUTION_FILE
$ python main.py --list-tools

'''


def run_cli():
    parser = create_argument_parser()
    args: Namespace = parser.parse_args()

    # Logging configuration
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger("androguard").setLevel(logging.WARNING)

    if args.list_tools:
        logging.info(" [Listing available tools] \n")
        for key in available_tools:
            print(" [{0}] {1} \n".format(key, available_tools[key].description))
        sys.exit(0)

    experiment_config.memory_file = args.c
    experiment_config.repetitions = args.r
    experiment_config.timeouts = args.t
    experiment_config.tools = get_selected_tools(args)
    experiment_config.generate_monitors = not args.skip_monitors
    experiment_config.instrument = not args.skip_instrument
    experiment_config.static_analysis = not args.skip_static_analysis
    experiment_config.no_window = args.no_window
    experiment_config.skip_experiment = args.skip_experiment

    validate_experiment_config()
    print_experiment_config()

    logging.info('############# STARTING EXPERIMENT #############')
    start = time.time()

    experiment_02.execute()

    end = time.time()
    elapsed = end - start
    logging.info('It took {0} to complete'.format(utils.to_readable_time(elapsed)))
    logging.info('############# ENDING EXPERIMENT #############')


def load_tools():
    """Load all available tools.

     A tool must be defined in a subdirectory within
     the tools folder, in a python module named tool.py.
     This module must also declare a class named ToolSpec,
     which should inherit from AbstractTool.
    """
    for subdir, dirs, files in os.walk('.' + os.sep + 'tools'):
        for filename in files:
            if filename == 'tool.py':
                tool_module = importlib.import_module(qualified_name(subdir + os.sep + filename))
                tool_class = getattr(tool_module, 'ToolSpec')
                tool_instance = tool_class()
                available_tools[tool_instance.name] = tool_instance
    experiment_config.available_tools = available_tools.values()


def get_selected_tools(args: Namespace):
    selected_tools = __get_tools(args.tools)
    if len(selected_tools) == 0 and not args.skip_experiment:
        print("No valid tools selected.")
        exit(1)
    return selected_tools


def __get_tools(names: list[str]) -> list[AbstractTool]:
    tools = set()
    for t in available_tools:
        for tool in names:
            if t == tool:
                tools.add(available_tools[t])
    return list(tools)


def qualified_name(p):
    return p.replace(".py", "").replace("./", "").replace("/", ".")


# def check_positive(value: int):
#     if value <= 0:
#         print("The value must be greater than zero: {}".format(value))
#         exit(1)

def create_argument_parser():
    # Start catching arguments
    parser = argparse.ArgumentParser(description=program_description, formatter_class=argparse.RawTextHelpFormatter)
    # list available tools
    parser.add_argument("--list-tools", help="list available tools", action="store_true")
    # List of test tools to be used in the experiment
    parser.add_argument('-tools', nargs='+', default=['monkey'],  help="List of test tools to be used in the experiment. Default: [monkey]. EX: -tools monkey droidbot")
    # List of the execution timeouts in the experiment
    parser.add_argument('-t', nargs='+', default=[60], help='List of the execution timeouts (in seconds) in the experiment. Default: [60]. EX: -t 120 300', type=int)
    # Number of repetitions used in the experiment
    parser.add_argument('-r', default=1, help='Number of repetitions used in the experiment. Default: 1. EX: -r 3', type=int, required=False)
    parser.add_argument('-c', default="", help='Path of the execution memory file (to continue an execution)', type=str)
    parser.add_argument("--no_window", help="Starts emulator with '-no-window'", action="store_true")
    # Enable DEBUG mode.
    parser.add_argument('--debug', help='Run in DEBUG mode (default: false)', dest='debug', action='store_true')
    parser.add_argument("--skip_monitors", help="Skip monitors generation", action="store_true")
    parser.add_argument("--skip_instrument", help="Skip instrumentation", action="store_true")
    parser.add_argument("--skip_experiment", help="Skip experiment execution", action="store_true")
    parser.add_argument("--skip_static_analysis", help="Skip static analysis", action="store_true")

    # parser.add_argument('-h', help='Show help message', action="store_true")

    return parser


def validate_experiment_config():
    # print(f"experiment_config.repetitions={experiment_config.repetitions}")
    # print(f"experiment_config.timeouts={experiment_config.timeouts}")
    # print(f"experiment_config.tools={len(experiment_config.tools)}")
    # print(f"experiment_config.generate_monitors={experiment_config.generate_monitors}")
    # print(f"experiment_config.instrument={experiment_config.instrument}")
    # print(f"experiment_config.static_analysis={experiment_config.static_analysis}")
    # print(f"experiment_config.skip_experiment={experiment_config.skip_experiment}")
    # print(f"experiment_config.memory_file={experiment_config.memory_file}")
    # print(f"experiment_config.no_window={experiment_config.no_window}")
    errors = []
    if experiment_config.memory_file:
        if not os.path.isfile(experiment_config.memory_file):
            errors.append(f"Invalid execution memory file: {experiment_config.memory_file}")
    elif not experiment_config.skip_experiment:
        __validate_repetitions(errors)
        __validate_timeouts(errors)
        __validate_tools(errors)
    if errors:
        print("Errors in experiment configuration:")
        for error in errors:
            print(error)
        exit(1)


def print_experiment_config():
    tools_names = []
    for tool in experiment_config.tools:
        tools_names.append(tool.name)

    config_str = (
        f"Original/Partial experiment config:\n"
        f"  - repetitions={experiment_config.repetitions}\n"
        f"  - timeouts={experiment_config.timeouts}\n"
        f"  - tools={tools_names}\n"
        f"  - pre-process=[generate_monitors={experiment_config.generate_monitors}, instrument={experiment_config.instrument}, static_analysis={experiment_config.static_analysis}]\n"
        f"  - skip_experiment={experiment_config.skip_experiment}\n"
        f"  - memory_file={experiment_config.memory_file}\n"
        f"  - no_window={experiment_config.no_window}"
    )

    logging.info(config_str)


def __validate_repetitions(errors):
    if experiment_config.repetitions <= 0:
        errors.append(f"Invalid 'repetitions': {experiment_config.repetitions}")


def __validate_tools(errors):
    if len(experiment_config.available_tools) == 0:
        errors.append("No available tools")
    elif len(experiment_config.tools) == 0:
        errors.append("Invalid 'tools': 0")


def __validate_timeouts(errors):
    visited = []
    if len(experiment_config.timeouts) == 0:
        errors.append(f"Invalid 'timeouts': {experiment_config.timeouts}")
    else:
        for timeout in experiment_config.timeouts:
            if timeout <= 0:
                errors.append(f"Invalid 'timeout': {timeout}")
            elif timeout in visited:
                errors.append(f"Duplicated timeout: {timeout}")
            visited.append(timeout)


def run_local():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger("androguard").setLevel(logging.ERROR)

    # experiment_config.repetitions = 3
    # experiment_config.timeouts = [60, 90, 120, 180, 300]
    # experiment_config.tools = __get_tools(
    #     ["monkey", "droidbot", "droidbot_dfs_greedy", "droidbot_bfs_naive", "droidbot_bfs_greedy", "humanoid",
    #      "droidmate", "ape", "ares", "fastbot", "qtesting"])

    _min = 60
    _5_min = 5 * _min
    _10_min = 2 * _5_min
    _30_min = 3 * _10_min
    _1_hour = 60 * _min
    _3_hour = 3 * _1_hour

    experiment_config.repetitions = 1
    experiment_config.timeouts = [_min]
    experiment_config.tools = __get_tools(["qtesting"])
    # "ape", "fastbot", "droidbot_dfs_greedy", "ares",
    # testados: monkey, ape, fastbot, droidmate
    # "droidbot", "droidbot_dfs_greedy", "droidbot_bfs_naive", "droidbot_bfs_greedy", "humanoid"
    # ares
    # PROBLEMA qtesting

    experiment_config.generate_monitors = False
    experiment_config.instrument = False
    experiment_config.static_analysis = False
    experiment_config.no_window = False
    experiment_config.skip_experiment = False

    experiment_config.memory_file = ""
    # base_dir = "/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/results"
    # experiment_config.memory_file = os.path.join(base_dir, "20241106124331", "execution_memory.json")

    validate_experiment_config()
    print_experiment_config()

    experiment_02.execute()

    print("FIM DE FESTA!!!")


if __name__ == '__main__':
    load_tools()

    # run_cli()
    run_local()
