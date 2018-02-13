from tempfile import NamedTemporaryFile
from ruamel.yaml import YAML
from unittest import TestCase

import carme.modules.yamltools

class TestMergeYaml(TestCase):
    file1 = ""
    file2 = ""
    def setup(self):
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
        tf1 = NamedTemporaryFile()
        tf2 = NamedTemporaryFile()
        yaml = YAML()

        yaml.dump(y1, tf1)
        yaml.dump(y2, tf2)

        self.file1 = tf1.name
        self.file2 = tf2.name

    def test_merge_yaml(self):
        yamltools.merge_yaml(self.file1, self.file2)

class TestFolderMergeYaml(TestCase):
    def run(self):
        pass
