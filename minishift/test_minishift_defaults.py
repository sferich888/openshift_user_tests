import unittest

#import yaml
from kubernetes import client, config
from openshift.dynamic import DynamicClient
import requests, time

class TestMiniShiftCreateApplication(unittest.TestCase):

    def setUp(self):
        k8s_client = config.new_client_from_config()
        self.oc = DynamicClient(k8s_client)
        self.pod = self.oc.resources.get(api_version='v1', kind='Pod')


    def tearDown(self):
        self.pod.delete(name='hello-openshift', namespace='myproject')


    def test_crate_application(self):
        url = 'https://raw.githubusercontent.com/openshift/origin/master/examples/hello-openshift/hello-pod.json'

        r = requests.get(url)
        pod_definition = r.json()

        self.pod.create(body=pod_definition, namespace='myproject')

        time.sleep(5)

        pods = self.pod.get(namespace='myproject')

        found_pods = []
        for pod in pods.items:
            found_pods.append(pod.metadata.name)

        self.assertIn('hello-openshift', found_pods)


class TestMiniShiftDefaults(unittest.TestCase):

    def setUp(self):
        k8s_client = config.new_client_from_config()
        self.oc = DynamicClient(k8s_client)


    def tearDown(self):
        pass


    def test_default_project(self):
        default_project = 'myproject'
        projects = self.oc.resources.get(api_version='project.openshift.io/v1', 
                kind='Project').get(verify=False)

        found_projects = []
        for project in projects.items:
            found_projects.append(project.metadata.name)

        self.assertIn(default_project, found_projects)
