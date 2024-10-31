import logging
import sys

import analysis.static_analysis as static
from settings import INSTRUMENTED_DIR


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger("androguard").setLevel(logging.ERROR)

    static.runXXX(INSTRUMENTED_DIR)

    print("FIM DE FESTA!!!")
