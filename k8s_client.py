from kubernetes import client, config
from kubernetes.client.rest import ApiException
# Configs can be set in Configuration class directly or using helper utility
import json

class K8s:
    def __init__(self):
        config.load_kube_config()
        self.client = client
        self.v1Api = client.CoreV1Api()
    def create_pod(self, params):
        vnf_name = params.get('vnf_name') if params.get('vnf_name') else "testpythonclient"
        namespace = params.get('namespace') if params.get('namespace') else 'vicsnet'
        default_ip = params.get('default_ip') if params.get('default_ip') else None
        network_ips = params.get('network_ips') if params.get('network_ips') else []
        image = params.get('image') if params.get('image') else "192.168.103.250:5000/icn-dtn-base-0.6.5:1.0"
        command = params.get('command') if params.get('command') else ["/bin/bash", "-c", "/root/start_vicsnf.sh; sleep 30d;"]
        envs = params.get('env')if params.get('env') else []
        envs = list(map(lambda x: self.client.V1EnvVar(x.get("name"), x.get("value")), envs))
        node_selector = params.get('node_selector') if params.get('node_selector') else None
        is_vnc = params.get('is_vnc') if params.get('is_vnc') else False

        #if (is_vnc):
        # TODO add is_vnc


        # Create a body which stores the information of the pod to create
        body = self.client.V1Pod()

        # Specify meta of a POD.
        annotations = {}
        if default_ip:
            annotations['default_ip'] = default_ip
        if len(network_ips):
            annotations['k8s.v1.cni.cncf.io/networks'] = str(network_ips)
        body.metadata = client.V1ObjectMeta(namespace=namespace, name=vnf_name, annotations= annotations)

        """
         Specify spec including: 
            - containers (name, image, env, command) https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md 
            - nodeSelector 
        """
        container = self.client.V1Container(command=command, image=image, env=envs, name=vnf_name, working_dir='/root')
        node_selector = { "kubernetes.io/hostname": node_selector } if node_selector else None
        body.spec = self.client.V1PodSpec(containers= [container], node_selector=node_selector)

        try:
            api_response = self.v1Api.create_namespaced_pod(namespace, body)
            print(api_response)

        except ApiException as e:
            raise

    def delete_pod(self, params):
        vnf_name = params.get('vnf_name')
        namespace = params.get('namespace')
        try:
            self.v1Api.delete_namespaced_pod(name=vnf_name, namespace= namespace)
        except ApiException as e:
            raise
    def get_pod(self, namespace, vnf_name):
        try:
            return self.v1Api.read_namespaced_pod(namespace=namespace, name=vnf_name)
        except ApiException as e:
            raise