from kubernetes import client, config
from kubernetes.client.rest import ApiException
# Configs can be set in Configuration class directly or using helper utility


class K8s:
    def __init__(self):
        config.load_kube_config()
        self.client = client
        self.v1Api = client.CoreV1Api()
    def create_pod(self):
        # Default value. TODO: get values from request
        namespace = 'vicsnet'
        name = "testPythonClient"
        image = "192.168.103.250:5000/icn-dtn-base-0.6.5:1.0"
        commands = ["/bin/bash", "-c", "/root/start_vicsnf.sh; sleep 30d;"]
        env = self.client.V1EnvVar("LC_ALL", "C.UTF-8")

        # Create a body which stores the information of the pod to create
        body = self.client.V1Pod()

        # Specify meta of a POD. TODO: specify default ip and networks in medata
        body.metadata = client.V1ObjectMeta(namespace=namespace, name=name)


        """
         Specify spec including: 
            - containers (name, image, env, command) https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md 
            - nodeSelector 
        """
        container = self.client.V1Container(command=commands, image=image, env=env, name=name)
        node_selector = { "kubernetes.io/hostname": "vicsnet-edge1"}
        body.spec = self.client.V1PodSpec(containers= [container], node_selector=node_selector)


        try:
            api_response = self.v1Api.create_namespaced_pod(namespace, body)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)

    
test_create_pod = K8s()
test_create_pod.create_pod()