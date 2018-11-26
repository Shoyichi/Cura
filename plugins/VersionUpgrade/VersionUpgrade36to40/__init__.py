# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from typing import Any, Dict, TYPE_CHECKING

from . import VersionUpgrade36to40

if TYPE_CHECKING:
    from UM.Application import Application

upgrade = VersionUpgrade36to40.VersionUpgrade34to35()

def getMetaData() -> Dict[str, Any]:
    return {
        "version_upgrade": {
            # From                           To                              Upgrade function
            ("preferences", 6000005):        ("preferences", 6000006,        upgrade.upgradePreferences),

            ("definition_changes", 4000005): ("definition_changes", 4000006, upgrade.upgradeInstanceContainer),
            ("variant", 4000005):            ("variant", 4000006,            upgrade.upgradeInstanceContainer),
            ("quality_changes", 4000005):    ("quality_changes", 4000006,    upgrade.upgradeInstanceContainer),
            ("quality", 4000005):            ("quality", 4000006,            upgrade.upgradeInstanceContainer),
            ("user", 4000005):               ("user", 4000006,               upgrade.upgradeInstanceContainer),

            ("machine_stack", 4000005):      ("machine_stack", 4000006,      upgrade.upgradeStack),
            ("extruder_train", 4000005):     ("extruder_train", 4000006,     upgrade.upgradeStack),
        },
        "sources": {
            "preferences": {
                "get_version": upgrade.getCfgVersion,
                "location": {"."}
            },
            "machine_stack": {
                "get_version": upgrade.getCfgVersion,
                "location": {"./machine_instances"}
            },
            "extruder_train": {
                "get_version": upgrade.getCfgVersion,
                "location": {"./extruders"}
            },
            "definition_changes": {
                "get_version": upgrade.getCfgVersion,
                "location": {"./definition_changes"}
            },
            "variant": {
                "get_version": upgrade.getCfgVersion,
                "location": {"./variants"}
            },
            "quality_changes": {
                "get_version": upgrade.getCfgVersion,
                "location": {"./quality_changes"}
            },
            "quality": {
                "get_version": upgrade.getCfgVersion,
                "location": {"./quality"}
            },
            "user": {
                "get_version": upgrade.getCfgVersion,
                "location": {"./user"}
            }
        }
    }


def register(app: "Application") -> Dict[str, Any]:
    return { "version_upgrade": upgrade }
