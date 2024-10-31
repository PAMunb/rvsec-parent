import logging as logging_api
import os
import time
from contextlib import contextmanager

import utils
from app import App
from commands.command import Command
from settings import ANDROID_PLATFORMS_DIR

logging = logging_api.getLogger(__name__)


class Android:

    @classmethod
    @contextmanager
    def create_emulator(cls, avd_name, no_window=False):
        # Code to acquire resource, e.g.:
        emulator = cls.start_emulator(avd_name, no_window)
        try:
            yield emulator
        finally:
            # Code to release resource, e.g.:
            cls.kill_emulator(avd_name)

    @classmethod
    def start_emulator(cls, avd_name: str, no_window: bool):
        logging.info('Starting emulator')

        args = ['-avd', avd_name,
                '-writable-system',   # make system & vendor image writable after 'adb remount'
                '-wipe-data',         # reset the user data image (copy it from initdata)
                '-no-boot-anim',      # disable animation for faster boot
                '-noaudio',           # disable audio support
                '-no-snapshot-save',  # do not auto-save to snapshot on exit: abandon changed state
                '-delay-adb']         # delay adb communication till boot completes
        if no_window:
            args.append('-no-window') # disable graphical window display

        start_emulator_cmd = Command('emulator', args)
        emulator_proc = start_emulator_cmd.invoke_as_deamon()

        cls._wait_for_boot()

    @classmethod
    def kill_emulator(cls, avd_name):
        logging.info("Killing emulator ...")
        kill_emulator_cmd = Command('adb', ['-s', 'emulator-5554', 'emu', 'kill'])
        kill_emulator_cmd.invoke()
        kill_server_cmd = Command('adb', ['-s', 'emulator-5554', 'kill-server'])
        kill_server_cmd.invoke()
        kill_locks_cmd = Command('rm', ['~/.android/avd/{}.avd/*.lock'.format(avd_name)])
        kill_locks_cmd.invoke()
        time.sleep(10)
        logging.info('Emulator has been killed')

    @staticmethod
    def _wait_for_boot():
        timeout = 90  # seconds
        start = time.time()
        logging.info('Waiting for emulator to boot')
        check_emulator_cmd = Command('adb', ['-s', 'emulator-5554', 'shell', 'getprop', 'init.svc.bootanim'], timeout)
        check_result = check_emulator_cmd.invoke()
        while check_result.stdout.strip().decode('ascii') != 'stopped':
            time.sleep(5)
            logging.info('Waiting for emulator to boot')
            check_result = check_emulator_cmd.invoke()
        wait_emulator_cmd = Command('adb', ['wait-for-device', 'shell',
                                            "'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done;'"], timeout)
        wait_emulator_cmd.invoke()

        root_cmd = Command('adb', ['wait-for-device', 'root'], timeout)
        while root_cmd.invoke().stderr.strip().decode('ascii'):
            time.sleep(5)

        adb_remount = Command('adb', ['wait-for-device', 'remount'], timeout)
        while adb_remount.invoke().stderr.strip().decode('ascii'):
            time.sleep(5)

        logging.info('Emulator booted!')
        end = time.time()
        elapsed = end - start
        logging.info('Emulator took {0} to boot'.format(utils.to_readable_time(elapsed)))

    @classmethod
    def simulate_reboot(cls):
        logging.info('Starting reboot simulation')
        sim_reboot_cmd = Command('adb', ['shell', 'am', 'broadcast', '-a', 'android.intent.action.BOOT_COMPLETED'], 15)
        sim_reboot_cmd.invoke()
        time.sleep(1)
        cls._wait_for_boot()

    @classmethod
    def install_with_permissions(cls, app: App):
        cls.install_apk(app)
        cls.grant_permissions(app)

    @classmethod
    def install_apk(cls, app: App):
        logging.info("Installing APK: {0}".format(app.name))
        root_cmd = Command('adb', ['root'])
        result = root_cmd.invoke()
        readlink_cmd = Command('readlink', ['-f', app.path])
        readlink_result = readlink_cmd.invoke()
        install_cmd = Command('adb', [
            '-s',
            'emulator-5554',
            'install',
            '-r',
            readlink_result.stdout.strip().decode('ascii')
        ])
        install_cmd.invoke()

    @classmethod
    def uninstall_apk(cls, app: App):
        logging.info("Uninstalling APK: {}".format(app.name))
        uninstall_cmd = Command('adb', ['-s', 'emulator-5554', 'uninstall', app.package_name])
        uninstall_cmd.invoke()

    @classmethod
    def grant_permissions(cls, app: App):
        for permission in app.permissions:
            logging.info("Granting permission {}".format(permission))
            grant_cmd = Command('adb', ['shell', 'pm', 'grant', app.package_name, permission])
            grant_cmd.invoke()

    @staticmethod
    def install_platform(number: str):
        logging.info("Installing android platform: {}".format(number))

        platform_dir = os.path.join(ANDROID_PLATFORMS_DIR, "android-{}".format(number))
        if os.path.exists(platform_dir):
            logging.info("Platform already exists.")
            return

        platform = "platforms;android-" + number
        install_cmd = Command('sdkmanager', ['--install', platform])
        install_cmd.invoke()
        logging.info("Android platform installed!")

    @staticmethod
    def list_installed_platforms():
        platforms_list = []
        for f in os.listdir(ANDROID_PLATFORMS_DIR):
            file = os.path.join(ANDROID_PLATFORMS_DIR, f)
            if os.path.isdir(file):
                platform = f.split('-')
                if len(platform) == 2:
                    platforms_list.append(platform[1].strip())
        return platforms_list
