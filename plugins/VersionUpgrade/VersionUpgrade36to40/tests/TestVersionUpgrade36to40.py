# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

import configparser #To parse the resulting config files.
import pytest #To register tests with.

import VersionUpgrade36to40 #The module we're testing.

##  Creates an instance of the upgrader to test with.
@pytest.fixture
def upgrader():
    return VersionUpgrade36to40.VersionUpgrade34to35()

test_upgrade_test_cases = [
    {"file_name": "Empty config file",
     "file_data": """[general]
    version = 4
    [metadata]
    type = quality
    setting_version = 5

    [values]
""",
     "is_experimental": False,
     },

    {"file_name": "um3_aa0.8_CPEP_Superdraft_Print",
     "file_data": """[general]
        version = 4
        [metadata]
        type = quality
        setting_version = 5

        [values]
    """,
     "is_experimental": True,
     },
]


##  Tests whether the version numbers are updated.
@pytest.mark.parametrize("test_case", test_upgrade_test_cases)
def test_upgradeQuality(test_case, upgrader):
    file_name = test_case["file_name"]
    file_data = test_case["file_data"]
    is_experimental = test_case["is_experimental"]

    _, upgraded_instances = upgrader.upgradeInstanceContainer(file_data, file_name)
    upgraded_instance = upgraded_instances[0]
    parser = configparser.ConfigParser(interpolation = None)
    parser.read_string(upgraded_instance)

    # Check the new version.
    assert parser["general"]["version"] == "4"
    assert parser["metadata"]["setting_version"] == "6"

    # Check "is_experimental" flag
    result_is_experimental = False
    if parser.has_option("metadata", "is_experimental"):
        result_is_experimental = bool(parser["metadata"]["is_experimental"])
    assert result_is_experimental == is_experimental
