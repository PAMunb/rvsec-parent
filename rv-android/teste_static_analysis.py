import logging
import sys
import os
import utils
import analysis.static_analysis as static
from settings import INSTRUMENTED_DIR
# import analysis.methods_extractor as me
import utils
from commands.command import Command
from constants import EXTENSION_GESDA, EXTENSION_GATOR
# from task import Task
from settings import *
from app import App

def runXXX(apks_dir: str):
    apks = utils.get_apks(apks_dir)
    for apk in apks:
        logging.info("Analysing APK: {}".format(apk.name))
        gesda_file = os.path.join(apks_dir, "{}{}".format(apk.name, EXTENSION_GESDA))
        gator_file = os.path.join(apks_dir, "{}{}".format(apk.name, EXTENSION_GATOR))
        # print(f"gator_file={gator_file}")
        # TODO try/catch
        # static.run_gesda(apk, gesda_file)
        static.run_gator(apk, gator_file)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger("androguard").setLevel(logging.ERROR)

    runXXX("/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/apks_mini")

    print("FIM DE FESTA!!!")
