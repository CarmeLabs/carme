import os, sys
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from ruamel.yaml import YAML
from unittest import TestCase

from src.modules.yamltools import merge_yaml, folder_merge_yaml 

# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

# setup global yaml
yaml = YAML()

class TestMergeYaml(TestCase):
    file1 = None
    file2 = None
    merged_file = None
    def setUp(self):
        y1 = """
        version: '3'
        services:
            svc1:
                image: hello-world
                deploy:
                    labels:
                        - label1=100
        networks:
            net1:
                external: true
        """
        y2 = """
        version: '3'
        services:
            svc2:
                image: hello-world-other
                volumes:
                    - vol1:/hello
                deploy:
                    labels:
                        - label1=100
        volumes:
            vol1:
        networks:
            net1:
                external: true
        """
        self.file1 = NamedTemporaryFile()
        self.file2 = NamedTemporaryFile()

        yaml.dump(y1, self.file1)
        yaml.dump(y2, self.file2)

    def test_merge_yaml(self):
        self.merged_file = merge_yaml(self.file1.name, self.file2.name)

        expected_string = """
        version: '3'
        services:
            svc1:
                image: hello-world
                deploy:
                    labels:
                        - label1=100
            svc2:
                image: hello-world-other
                volumes:
                    - vol1:/hello
                deploy:
                    labels:
                        - label1=100
        volumes:
            vol1:
        networks:
            net1:
                external: true
        """
        merged_yaml = yaml.load(self.merged_file)
        expected_yaml = yaml.load(expected_string)
        with open('output.yaml', 'w') as f:
            yaml.dump(merged_yaml, f)
        self.assertTrue(merged_yaml == expected_yaml)

    def tearDown(self):
        self.file1.close()
        self.file2.close()
        self.merged_file.close()

class TestFolderMergeYaml(TestCase):
    def test_folder_merge_yaml(self):
        pass
