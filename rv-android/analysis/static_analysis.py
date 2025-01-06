import logging as logging_api
import os.path
import sys

from app import App
from commands.command import Command
from settings import *

logging = logging_api.getLogger(__name__)


class StaticAnalysisException(Exception):
    pass


def run_gesda(app: App, gesda_file: str):
    gesda_jar = os.path.join(LIB_DIR, "gesda", "rvsec-gesda.jar")
    gesda_cmd = Command("java", [
        "-jar",
        gesda_jar,
        "--android-dir",
        ANDROID_PLATFORMS_DIR,
        "--rt-jar",
        RT_JAR,
        "--output",
        gesda_file,
        "--apk",
        app.path
    ])
    __run(app, gesda_file, "GESDA", gesda_cmd)


def run_gator(app: App, gator_file: str):
    gator_dir = os.path.join(LIB_DIR, "gator")
    gator_python = os.path.join(gator_dir, "gator")
    gator_client_jar = os.path.join(gator_dir, "rvsec-gator-client.jar")
    gator_cmd = Command("python", [
        gator_python,
        "a",
        "-p",
        app.path,
        "--client-jar",
        gator_client_jar,
        "--out",
        gator_file,
        "-client",
        "RvsecWtgClient"
    ])
    __run(app, gator_file, "GATOR", gator_cmd)


def __run(app: App, result_file: str, name: str, command: Command):
    if os.path.isfile(result_file):
        logging.info("Skipping APK already analyzed with {}: {}".format(name, app.name))
        return
    logging.info("Executing analysis on apk '{}': {}".format(app.name, name))
    cmd_result = command.invoke(stdout=sys.stdout)
    if cmd_result.code != 0:
        raise StaticAnalysisException("Error while executing {0}: {1}. {2}".format(name, cmd_result.code,
                                                                                   cmd_result.stderr))


def run_reachability():
    pass
