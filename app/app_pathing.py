# Created by alanhu at 8/30/23
import sys
import os
from pathlib import Path

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_script_directory)

# Append the parent directory to sys.path
sys.path.append(parent_directory)


class pathing_module:
    def __init__(self):
        # Get the directory of the current script
        self.current_script_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the parent directory
        self.parent_directory = os.path.dirname(self.current_script_directory)

        self.base_path = self.parent_directory
        self.base_path = Path(self.base_path)

        # get app path
        app = Path("app")
        self.app_path = self.base_path / app
        # get config path
        config = Path("config")
        self.config_path = self.base_path / config

        # get tests path
        tests = Path("tests")
        self.tests_path = self.base_path / tests
        # get the log path
        log = Path("log")
        self.log_path = self.base_path / log

        self.generate_project_folders()

    def generate_project_folders(self):
        if not os.path.exists(self.app_path):
            os.makedirs(self.app_path)
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)
        if not os.path.exists(self.tests_path):
            os.makedirs(self.tests_path)
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

    def get_path(self, path_name):
        if path_name == "base":
            return self.base_path
        elif path_name == "app":
            return self.app_path
        elif path_name == "config":
            return self.config_path
        elif path_name == "tests":
            return self.tests_path
        elif path_name == "log":
            return self.log_path
        else:
            return None

    def set_path(self, path_name, path):
        if path_name == "base":
            self.base_path = path
        elif path_name == "app":
            self.app_path = path
        elif path_name == "config":
            self.config_path = path
        elif path_name == "tests":
            self.tests_path = path
        elif path_name == "log":
            self.log_path = path
        else:
            return None


pathing = pathing_module()
print(pathing.get_path("base"))
print(pathing.get_path("app"))
print(pathing.get_path("config"))
print(pathing.get_path("tests"))
print(pathing.get_path("log"))
