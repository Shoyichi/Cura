# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

import configparser
import io
import os
from typing import Dict, List, Tuple

from UM.VersionUpgrade import VersionUpgrade

_EXPERIMENTAL_QUALITY_PROFILES = {
    "um3_aa0.25_PC_Normal_Quality",
    "um3_aa0.25_PP_Normal_Quality",
    "um3_aa0.8_CPEP_Fast_Print",
    "um3_aa0.8_CPEP_Superdraft_Print",
    "um3_aa0.8_CPEP_Verydraft_Print",
    "um3_aa0.8_PC_Fast_Print",
    "um3_aa0.8_PC_Superdraft_Print",
    "um3_aa0.8_PC_Verydraft_Print",
    "um_s5_aa0.25_PC_Normal_Quality",
    "um_s5_aa0.25_PP_Normal_Quality",
    "um_s5_aa0.8_CPEP_Fast_Print",
    "um_s5_aa0.8_CPEP_Superdraft_Print",
    "um_s5_aa0.8_CPEP_Verydraft_Print",
    "um_s5_aa0.8_PC_Fast_Print",
    "um_s5_aa0.8_PC_Superdraft_Print",
    "um_s5_aa0.8_PC_Verydraft_Print",
    "um_s5_aa0.8_aluminum_CPEP_Fast_Print",
    "um_s5_aa0.8_aluminum_PC_Fast_Print",
}  # type: Dict[str, str]


##  Upgrades configurations from the state they were in at version 3.4 to the
#   state they should be in at version 3.5.
class VersionUpgrade34to35(VersionUpgrade):
    ##  Gets the version number from a CFG file in Uranium's 3.3 format.
    #
    #   Since the format may change, this is implemented for the 3.3 format only
    #   and needs to be included in the version upgrade system rather than
    #   globally in Uranium.
    #
    #   \param serialised The serialised form of a CFG file.
    #   \return The version number stored in the CFG file.
    #   \raises ValueError The format of the version number in the file is
    #   incorrect.
    #   \raises KeyError The format of the file is incorrect.
    def getCfgVersion(self, serialised: str) -> int:
        parser = configparser.ConfigParser(interpolation = None)
        parser.read_string(serialised)
        format_version = int(parser.get("general", "version")) #Explicitly give an exception when this fails. That means that the file format is not recognised.
        setting_version = int(parser.get("metadata", "setting_version", fallback = "0"))
        return format_version * 1000000 + setting_version

    ##  Upgrades Preferences to have the new version number.
    def upgradePreferences(self, serialized: str, filename: str) -> Tuple[List[str], List[str]]:
        parser = configparser.ConfigParser(interpolation = None)
        parser.read_string(serialized)

        # Need to show the data collection agreement again because the data Cura collects has been changed.
        if parser.has_option("info", "asked_send_slice_info"):
            parser.set("info", "asked_send_slice_info", "False")
        if parser.has_option("info", "send_slice_info"):
            parser.set("info", "send_slice_info", "True")

        # Update version number.
        parser["general"]["version"] = "6"
        if "metadata" not in parser:
            parser["metadata"] = {}
        parser["metadata"]["setting_version"] = "6"

        result = io.StringIO()
        parser.write(result)
        return [filename], [result.getvalue()]

    ##  Upgrades stacks to have the new version number.
    def upgradeStack(self, serialized: str, filename: str) -> Tuple[List[str], List[str]]:
        parser = configparser.ConfigParser(interpolation = None)
        parser.read_string(serialized)

        # Update version number.
        parser["general"]["version"] = "4"
        parser["metadata"]["setting_version"] = "6"

        result = io.StringIO()
        parser.write(result)
        return [filename], [result.getvalue()]

    ##  Upgrades instance containers to have the new version
    #   number.
    def upgradeInstanceContainer(self, serialized: str, filename: str) -> Tuple[List[str], List[str]]:
        parser = configparser.ConfigParser(interpolation = None)
        parser.read_string(serialized)

        # Update version number.
        parser["general"]["version"] = "4"
        parser["metadata"]["setting_version"] = "6"

        # Add "is_experimental = True" for experimental quality profiles
        if parser["metadata"]["type"] == "quality":
            base_filename = os.path.basename(filename).strip()
            if base_filename.endswith(".inst.cfg"):
                base_filename = base_filename[:len(base_filename) - len(".inst.cfg")]
            if base_filename in _EXPERIMENTAL_QUALITY_PROFILES:
                parser["metadata"]["is_experimental"] = str(True)

        result = io.StringIO()
        parser.write(result)
        return [filename], [result.getvalue()]
