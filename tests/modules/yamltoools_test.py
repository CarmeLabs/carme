import os, sys
import logging
from tempfile import NamedTemporaryFile
from ruamel.yaml import YAML
from unittest import TestCase

from src.modules import yamltools

class TestMergeYaml(TestCase):
    file1 = None
    file2 = None
    yaml = YAML()
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

        self.yaml.dump(y1, self.file1)
        self.yaml.dump(y2, self.file2)

    def test_merge_yaml(self):
        FORMAT = 'carme: [%(levelname)s] %(message)s'
        logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

        file = yamltools.merge_yaml(self.file1.name, self.file2.name)

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
        merged_yaml = self.yaml.load(os.path.abspath(file))
        expected_yaml = self.yaml.load(expected_string)
        logging.debug(merged_yaml)
        self.assertTrue(merged_yaml == expected_yaml)

    def tearDown(self):
        self.file1.close
        self.file2.close

class TestFolderMergeYaml(TestCase):
    def test_folder_merge_yaml(self):
        pass
