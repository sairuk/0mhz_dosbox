#!/usr/bin/env python3

#
# hacked together by sairuk
#

import os, sys
import argparse
from dosbox import DOSBox
from lxml import etree

app_name = '0mhz_dosbox'

def main(args):
    zmhz_path = args.mgls
    dosbox_path = args.dosbox_base
    dosbox = DOSBox(app_name)
    dosbox.pconf(dosbox.conf_dosbox_default_conf)

    if not os.path.exists(zmhz_path):
        print(f"Failed to find input folder: {zmhz_path}", file=sys.stderr)
        exit(1)

    if not os.path.exists(dosbox.dosbox_confdir):
        os.mkdir(dosbox.dosbox_confdir)

    for root, dirs, files in os.walk(zmhz_path):
        for filename in files:
            abs_path = os.path.join(root, filename)
            basename = os.path.splitext(filename)[0]

            dosbox.autoexec = []
            dosbox.conf_dosbox = os.path.join(dosbox.dosbox_confdir,f"{basename}.conf")
            dosbox.conf_dosbox_default_game = os.path.join(dosbox.dosbox_confdir_defaults,f"{app_name}_{basename}.conf")
            dosbox.pconf(dosbox.conf_dosbox_default_game)
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

                dosbox.autoexec.append(f'imgmount {drv} "{dosbox_path}/{file_ao486}" -t {dev_dosbox}')

                if index == "0" or index == "1":
                    print(f"Game {filename} has a floppy type image at index {index} if you have trouble booting this may be why", file=sys.stderr)

            if dev_dosbox is None:
                next

            dosbox.cmd_boot()
            dosbox.wconf()

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert 0mhz A0486 mgl files to dosbox configs.')

    parser.add_argument('--mgls', type=str, help='path to 0mhz AO486 mgls for processing', required=True)
    parser.add_argument('--dosbox-base', type=str, help='dosbox base part, where will dosbox see the 0mhz vhd/chd/img etc files', required=True)

    args = parser.parse_args()
    main(args)