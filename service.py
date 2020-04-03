from k8s_client import K8s
import nfd_agent_pb2
import nfd_agent_pb2_grpc
import grpc
import json
from google.protobuf import empty_pb2
import concurrent.futures
from kubernetes.client.rest import ApiException
import re
class VIcsnf:
  def __init__(self):
    self.k8s = K8s()
  def create(self, params):
    """ sample API
    vnfs = [
      { 
        "vnf_name": "testpod",
        "namespace": "vicsnet",
        "default_ip": "10.10.8.108",
        "network_ips": [
          {"name": "kuryr-ndn-99", "namespace": "default", "ips": ["10.10.99.99"]}
        ],
        "image": "192.168.103.250:5000/icn-dtn-base-0.6.5:1.0",
        "command":  ["/bin/bash", "-c", "/root/start_vicsnf.sh; sleep 30d;"],
        "env": [
          { 
            "name": "LC_ALL",
            "value": "C.UTF-8",
          }
        ],
        "node_selector": "vicsnet-edge1",
      }
    ]
    """
    vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    created_pods = []
    errmsg = ""

    for i in vnfs:
      try:
        self.k8s.create_pod(i)
        created_pods.append(i)
        print(created_pods)
      except ApiException as e:
        # Rollback created pod
        body = json.loads(e.body)
        errmsg = body.get("message")
        for i in created_pods:
          self.k8s.delete_pod(i)
        created_pods = []
        break
  
    return { 
      "topology_id": params.get("topology_id"),
      "result": "OK" if errmsg == "" else "ERROR",
      "errmsg": errmsg,
      "vnfs": list(map(lambda x: { "vnf_name": x.get("vnf_name"), "status": "created"}, created_pods))
    }
    #with concurrent.futures.ProcessPoolExecutor() as executor:
    #  executor.map(self.k8s.create_pod, vicsnets) 
    #  return { }
  #
  def delete(self, params):
    """ sample API
    vnfs = [
      { 
        "vnf_name": "testpod",
        "namespace": "vicsnet"
      }
    ]
    """
    vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    errmsg = ""
    for i in vnfs:
      try:
        self.k8s.delete_pod(i)
      except ApiException as e:
        body = json.loads(e.body)
        errmsg = body.get("message")

    return { 
      "topology_id": params.get("topology_id"),
      "result": "OK" if errmsg == "" else "ERROR",
      "errmsg": errmsg,
      "vnfs": list(map(lambda x: { "vnf_name": x.get("vnf_name"), "status": "deleted"}, vnfs))
    }
  
  def get(self, namespace, vnf_name):
    vnf_res = self.k8s.get_pod(namespace, vnf_name)
    have_pod = bool(len(vnf_res.spec.containers))
    return {
      "vnf_name": vnf_res.metadata.name,
      "namespace": vnf_res.metadata.namespace,
      "default_ip": vnf_res.metadata.annotations.get('default_ip'),
      "network_ips": json.loads(vnf_res.metadata.annotations.get('k8s.v1.cni.cncf.io/networks').replace("\'", "\"")) if vnf_res.metadata.annotations.get('k8s.v1.cni.cncf.io/networks') else [],
      "image": vnf_res.spec.containers[0].image if have_pod else "",
      "env":  list(map(lambda x: { "name": x.name, "value": x.value },vnf_res.spec.containers[0].env)) if (have_pod & (vnf_res.spec.containers[0].env is not None))  else [],
      "command": vnf_res.spec.containers[0].command if have_pod else [],
      "node_selector": vnf_res.spec.node_selector.get("kubernetes.io/hostname") if have_pod & (vnf_res.spec.node_selector is not None) else "",
      "is_vnc": True
    }

class GrpcClient:
  def __init__(self, nfd_agent_ip):
    with grpc.insecure_channel(
            target= nfd_agent_ip,
            options=[("grpc.enable_retries", 0),
                     ("grpc.keepalive_timeout_ms", 10000)]) as channel:
      self.stub = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

class NfdFace:
  def create(self, params):
    vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    result_vnfs = []

    for i in vnfs:
      faces = i.get("faces") if i.get("faces") else []
      faces_created = []
      vnf_address = i.get("vnf_address") + ":50051" if i.get("vnf_address") else "localhost:50051"
      with grpc.insecure_channel(
          target= vnf_address,
          options=[("grpc.enable_retries", 0),
                    ("grpc.keepalive_timeout_ms", 10000)]) as channel:
        grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
        for face in faces:
            face_create_req = nfd_agent_pb2.NFDFaceCreateReq()
            if face.get("remote"):
              face_create_req.remote = face.get("remote")
            if face.get("persistency"):
              face_create_req.persistency = face.get("persistency")
            if face.get("local"):
              face_create_req.local = face.get("local")
            if face.get("reliability"):
              face_create_req.reliability = face.get("reliability")
            if face.get("congestion_marking"):
              face_create_req.congestion_marking = face.get("congestion_marking")
            if face.get("congestion_marking_interval"):
              face_create_req.congestion_marking_interval = face.get("congestion_marking_interval")
            if face.get("congestion_marking_interval"):
              face_create_req.congestion_marking_interval = face.get("congestion_marking_interval")
            if face.get("default_congestion_threshold"):
              face_create_req.default_congestion_threshold = face.get("default_congestion_threshold")
            if face.get("mtu"):
              face_create_req.mtu = face.get("mtu")

            grpc_res = grpc_client.NFDFaceCreate(face_create_req)
            ack_msg = grpc_res.ack_msg
            face_id = re.findall("id=(.*?) ", ack_msg)
            faces_created.append({ "remote": i.get("remote"), "faceid": face_id })
      
      result_vnfs.append({
        "vnf_name": i.get("vnf_name"),
        "vnf_address": i.get("vnf_address"),
        "faces": faces_created
      })
    
    return {
      "id": params.get('id'),
      "vnfs": result_vnfs,
      "result": "OK",
      "errmsg": ""
    }

  def get(self, ip):
    with grpc.insecure_channel(
          target= ip,
          options=[("grpc.enable_retries", 0),
                    ("grpc.keepalive_timeout_ms", 10000)]) as channel:
      grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

      grpc_res = grpc_client.NFDFaceList(nfd_agent_pb2.NFDFaceIDReq(faceid=0))
      faces = grpc_res.faces
      result = []

      if grpc_res.ack.ack_code == 'ok':
        result= list(map(lambda f: { "faceid": f.faceid, "remote": f.remote, "local": f.local}), faces)
        
      return {
        "faces": result
      }

  def delete(self, params):
    vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    result_vnfs = []
    for i in vnfs:

      faces = i.get("faces") if i.get("faces") else []
      faces_deleted = []
      vnf_address = i.get("vnf_address") + ":50051" if i.get("vnf_address") else "localhost:50051"
      with grpc.insecure_channel(
          target= vnf_address,
          options=[("grpc.enable_retries", 0),
                    ("grpc.keepalive_timeout_ms", 10000)]) as channel:
        grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
        for face in faces:
          face_delete_req = nfd_agent_pb2.NFDFaceIDReq()
          face_delete_req.faceid = int(face.get("link_id"))


          grpc_res = grpc_client.NFDFaceDestroy(face_delete_req)
          ack_msg = grpc_res.ack_msg
          face_id = re.findall("id=(.*?) ", ack_msg)
          faces_deleted.append({ "faceid": face_id, "status": "deleted" })
      
      result_vnfs.append({
        "vnf_name": i.get("vnf_name"),
        "vnf_address": i.get("vnf_address"),
        "faces": faces_deleted
      })
    
    return {
      "id": params.get('id'),
      "vnfs": result_vnfs,
      "result": "OK",
      "errmsg": ""
    }

class NfdRoute:
  def create(self, params):
    nfd_agent_ip = params.get("nfd_agent_ip") + ":50051" if params.get("nfd_agent_id") else "localhost:50051"
    grpc_client = GrpcClient(nfd_agent_ip)
    
    route_req = nfd_agent_pb2.NFDRouteReq()
    if params.get("prefix"):
      route_req.prefix = params.get("prefix")
    if params.get("nexthop"):
      route_req.nexthop = params.get("nexthop")
    if params.get("origin"):
      route_req.origin = params.get("origin")
    if params.get("cost"):
      route_req.cost = params.get("cost")
    if params.get("expires"):
      route_req.expires = params.get("expires")

    ack_replay = grpc_client.stub.NFDRouteAdd(route_req)
    
    return response(ack_replay)

class NfdNameTemplate:
  def create(self, params):
   template = json.loads(params.get("template")) if params.get("template") else []
    
  # result_route = []
  # for i in vnfs:
  #   routes = i.get("route_add") if i.get("route_add") else []
  #   routes_added = []
  #   vnf_address = i.get("vnf_address") + ":50051" if i.get("vnf_address") else "localhost:50051"
  #   with grpc.insecure_channel(
  #       target= vnf_address,
  #       options=[("grpc.enable_retries", 0),
  #                 ("grpc.keepalive_timeout_ms", 10000)]) as channel:
  #     grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
  #     for route in routes:
  #         route_create_req = nfd_agent_pb2.NFDRouteReq()
  #         if route.get("prefix"):
  #           route_create_req.remote = route.get("prefix")
  #         if route.get("nexthop"):
  #           route_create_req.persistency = route.get("nexthop")

  #         grpc_res = grpc_client.NFDRouteAdd(face_create_req)
  #         ack_msg = grpc_res.ack_msg
  #         face_id = re.findall("id=(.*?) ", ack_msg)
  #         faces_created.append({ "remote": i.get("remote"), "faceid": face_id })
    
  
  # return {
  #   "id": params.get('id'),
  #   "vnfs": result_vnfs,
  #   "result": "OK",
  #   "errmsg": ""
  # }
def response(ack_replay):
  return { "ack_code": ack_replay.ack_code, "ack_msg": ack_replay.ack_msg }