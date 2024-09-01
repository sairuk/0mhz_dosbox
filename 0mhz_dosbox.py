#!/usr/bin/env python3

#
# hacked together by sairuk
#

import os, sys
import configparser
import argparse
from lxml import etree

app_name = '0mhz_dosbox'
dosbox_confdir = app_name
dosbox_confdir_defaults = f"{app_name}.conf"

class DosBox(object):
    def __init__(self):
        self.autorun = []
        self.conf = configparser.ConfigParser()
        return

    def drive(self, id):
        drive_map = {
            '0': 'a',
            '1': 'b',
            '2': 'c',
            '4': 'd',
            '5': 'e',
            '6': 'f',
            '7': 'g'
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
    
    def autoexec_cmds(self):
        return

def main(args):
    dosbox = DosBox()

    zmhz_path = args.mgls
    dosbox_path = args.dosbox_base
    conf_dosbox_default_conf = os.path.join(dosbox_confdir_defaults,"dosbox-x.conf")

    # read the default config
    if os.path.exists(conf_dosbox_default_conf):
        print(f"Reading: {conf_dosbox_default_conf}")
        dosbox.conf.read(conf_dosbox_default_conf)

    if not os.path.exists(zmhz_path):
        print(f"Failed to find input folder: {zmhz_path}", file=sys.stderr)
        exit(1)

    if not os.path.exists(dosbox_confdir):
        os.mkdir(dosbox_confdir)

    for root, dirs, files in os.walk(zmhz_path):
        for filename in files:
            autoexec = []
            boot = "c"
            bootlook = True
            autoexec_cmd = ""
            abs_path = os.path.join(root, filename)
            basename = os.path.splitext(filename)[0]
            conf_dosbox = os.path.join(dosbox_confdir,f"{basename}.conf")
            conf_dosbox_default_game = os.path.join(dosbox_confdir_defaults,f"{app_name}_{basename}.conf")

            if os.path.exists(conf_dosbox_default_game):
                print(f"Reading: {conf_dosbox_default_game}")
                dosbox.conf.read(conf_dosbox_default_game)

            dosbox.template()

            try:
                xml = etree.parse(abs_path)
            except etree.XMLSyntaxError:
                print(f"Invalid XML: {filename}", file=sys.stderr)
                next
            elements = xml.getroot().xpath("//file")
            dev_dosbox = None
            for element in elements:
                index = element.attrib["index"]
                file_ao486 = element.attrib["path"]
                filetype = os.path.splitext(file_ao486)[-1][1:]
                devtype_ao486 = element.attrib["type"]
                dev_dosbox = dosbox.device(filetype)
                drv = dosbox.drive(index)
                if dev_dosbox is None:
                    print(f"Failed to lookup device map for: {filetype} in {filename} ({abs_path})", file=sys.stderr)
                    break

                autoexec.append(f'imgmount {drv} "{dosbox_path}/{file_ao486}" -t {dev_dosbox}')

                if index == "0" or index == "1":
                    print(f"Game {filename} has a floppy type image at index {index} if you have trouble booting this may be why", file=sys.stderr)

                # Wizardry I didn't like this
                #if bootlook and index == "0":
                #    boot = dosbox.drive(index)
                #    bootlook = False

            if dev_dosbox is None:
                next

            autoexec.append(f'boot -l {boot} \n')
            autoexec_cmd = f'{os.linesep}'.join(autoexec)

            # write config
            with open(conf_dosbox, 'w') as d:
                dosbox.conf.write(d)
                d.write(autoexec_cmd)
            #break

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert 0mhz A0486 mgl files to dosbox configs.')

    parser.add_argument('--mgls', type=str, help='path to 0mhz AO486 mgls for processing', required=True)
    parser.add_argument('--dosbox-base', type=str, help='dosbox base part, where will dosbox see the 0mhz vhd/chd/img etc files', required=True)

    args = parser.parse_args()
    main(args)