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
    expected_string = None
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
        self.file1 = NamedTemporaryFile(mode='w')
        self.file2 = NamedTemporaryFile(mode='w')

        self.file1.write(y1)
        self.file2.write(y2)

        self.expected_string = y1 + y2

    def test_merge_yaml(self):
        merged_file = merge_yaml(self.file1.name, self.file2.name)

        with open(merged_file, 'r') as merged:
            print(merged.read())
            self.assertTrue(merged.read() == self.expected_string)


    def tearDown(self):
        self.file1.close()
        self.file2.close()

class TestFolderMergeYaml(TestCase):
    def setUp(self):
        pass
    def test_folder_merge_yaml(self):
        pass
    def tearDown(self):
        pass
