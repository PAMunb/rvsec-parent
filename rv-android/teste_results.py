import json
import logging
import os
import sys

import analysis.coverage as cov
from constants import EXTENSION_METHODS
from experiment.memory import Memory

import analysis.results_analysis as res

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    result_dir = "/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/results/20241101134620"

    res.process_results(result_dir)
