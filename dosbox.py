#!/usr/bin/env python3

import os
import configparser

class DOSBox(object):
    def __init__(self, app_name):
        self.autoexec = []
        self.conf = configparser.ConfigParser()
        self.dosbox_confdir = app_name
        self.dosbox_confdir_defaults = f"{app_name}.conf"
        self.conf_dosbox = ""
        self.conf_dosbox_default_conf = os.path.join(self.dosbox_confdir_defaults,"dosbox-x.conf")
        self.conf_dosbox_default_game = ""
        self.bootdrive = "c"
        return

    def pconf(self, config):
        if os.path.exists(config):
            print(f"Reading: {config}")
            self.conf.read(config)
        return

    def drive(self, id):
        drive_map = {
            '0': 'a',
            '1': 'b',
            '2': 'c',
            '3': 'd',
            '4': 'e',
            '5': 'f',
            '6': 'g'
        }
        if id in drive_map:
            return drive_map[id]
        return

    def device(self, dev):
        device_map = {
            "vhd": "hdd",
            "chd": "iso",
            "img": "floppy"
        }
        
        if dev in device_map:
            return device_map[dev]
        return None

    def template(self):
        self.conf["dosbox"] = { "quit warning": "false" }
        self.conf["dos"] = { "ver": "7.0" }
        self.conf["autoexec"] = {}

    def cmd_boot(self):
        self.autoexec.append(f'boot -l {self.bootdrive} \n')
        return

    def wconf(self):
        with open(self.conf_dosbox, 'w') as d:
            self.conf.write(d)
            d.write(f'{os.linesep}'.join(self.autoexec))
        return
