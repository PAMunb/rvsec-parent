import json
import csv
import os
import shutil
from csv import DictReader

fdroid_spreadsheet = "fdroid/final_apps_to_download.csv"
x01_generic_file = "exp01_generic_results.json"
x01_jca_file = "exp01_jca_results.json"
x02_generic_file = "exp02_generic_results.json"
x02_jca_file = "exp02_jca_results.json"


def copy_apks(from_dir, to_dir, apks, fdroid):
    print("Copiando apks ...")
    for apk in apks:
        if apks[apk]["x01_generic"] and apks[apk]["x01_jca"] and fdroid[apk]["package"]:
            from_file = os.path.join(from_dir, apk)
            to_file = os.path.join(to_dir, apk)
            if os.path.exists(to_file):
                continue
            shutil.copy2(from_file, to_file)


def execute(out_file: str, from_dir, to_dir):
    apks = {}
    read_result(x01_generic_file, "x01_generic", apks)
    read_result(x01_jca_file, "x01_jca", apks)
    read_result(x02_generic_file, "x02_generic", apks)
    read_result(x02_jca_file, "x02_jca", apks)
    fdroid = read_fdroid()
    write_instrumentation_info(apks, out_file, fdroid)
    copy_apks(from_dir, to_dir, apks, fdroid)
    print("FIM DE FESTA !!!")


def read_result(results_file: str, field: str, apks: dict):
    print(f"Executando: {results_file}")
    with open(results_file, "r") as f:
        result = json.load(f)
        for apk in result:
            if apk not in apks:
                apks[apk] = {"x01_generic": False, "x01_jca": False, "x02_generic": False, "x02_jca": False}
            apks[apk][field] = True


def write_instrumentation_info(apks: dict, out_file: str, fdroid):
    print("Escrevendo resultado ...")
    data = []
    for apk in apks:
        data.append([apk, fdroid[apk]["package"], apks[apk]["x01_generic"], apks[apk]["x01_jca"],
                     apks[apk]["x02_generic"], apks[apk]["x02_jca"]])
    with open(out_file, "w", newline="") as csvfile:
        header = ["apk", "same_package", "x01_generic", "x01_jca", "x02_generic", "x02_jca"]
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)
        print(f"File saved: {out_file}")


def read_fdroid():
    apps = {}
    with open(fdroid_spreadsheet, 'r') as f:
        dict_reader = DictReader(f)
        list_of_dict = list(dict_reader)
        for app in list_of_dict:
            app['mop'] = False if app['mop'] == 'No' else True
            app['package'] = False if app['package'] == 'False' else True
            apps[app['file']] = app
    return apps


if __name__ == '__main__':
    all_apks_dir = "/home/pedro/desenvolvimento/RV_ANDROID/ALL_APKS_tmp"
    new_dir = "/home/pedro/desenvolvimento/RV_ANDROID/ALL_APKS"
    out_file = "/home/pedro/desenvolvimento/RV_ANDROID/instrument_info.csv"

    execute(out_file, all_apks_dir, new_dir)
