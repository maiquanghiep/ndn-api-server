from kubernetes import client, config
from kubernetes.client.rest import ApiException
# Configs can be set in Configuration class directly or using helper utility


class K8s:
    def __init__(self):
        config.load_kube_config()
        self.client = client
        self.v1Api = client.CoreV1Api()
    def create_pod(self):
        namespace = 'viscnet'
        body = self.client.V1Pod()
        try:
            api_response = self.v1Api.create_namespaced_pod(namespace, body)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)
    
test_create_pod = K8s()
test_create_pod.create_pod()