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

def create_grpc_connection(vnf_address):
    with grpc.insecure_channel(
            target= vnf_address,
            options=[("grpc.enable_retries", 0),
                     ("grpc.keepalive_timeout_ms", 10000)]) as channel:
      return nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

class NfdFace:
  def create(self, params):
    vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    result_vnfs = []
    for i in vnfs:
      vnf_address = i.get("vnf_address") + ":50051" if i.get("vnf_address") else "localhost:50051"
      # with grpc.insecure_channel(
      #       target= vnf_address,
      #       options=[("grpc.enable_retries", 0),
      #                ("grpc.keepalive_timeout_ms", 10000)]) as channel:
      #   grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
      grpc_client = create_grpc_connection(vnf_address)
      faces = i.get("faces") if i.get("faces") else []
      faces_created = []

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

        gpc_res = grpc_client.NFDFaceCreate(face_create_req)
        ack_msg = gpc_res.get("ack_msg")
        face_id = re.findall("id=(.*?) ", ack_msg)
        faces_created.append({ "remote": i.remote, "faceid": face_id })
      
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

  def delete(self, params):
    vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    result_vnfs = []
    for i in vnfs:
      vnf_address = i.get("vnf_address") + ":50051" if i.get("vnf_address") else "localhost:50051"
      grpc_client = GrpcClient(vnf_address)

      faces = i.get("faces") if i.get("faces") else []
      faces_deleted = []

      for face in faces:
        face_delete_req = nfd_agent_pb2.NFDFaceIDReq()
        face_delete_req.faceid = face.get("link_id")


        gpc_res = grpc_client.stub.NFDFaceDestroy(face_delete_req)
        ack_msg = gpc_res.get("ack_msg")
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

class NfdStrategy:
  def create(self, params):
    nfd_agent_ip = params.get("nfd_agent_ip") + ":50051" if params.get("nfd_agent_id") else "localhost:50051"
    grpc_client = GrpcClient(nfd_agent_ip)
    
    strategy_req = nfd_agent_pb2.NFDStrategyReq()
    if params.get("prefix"):
      strategy_req.prefix = params.get("prefix")
    if params.get("strategy"):
      strategy_req.strategy = params.get("strategy")

    ack_replay = grpc_client.stub.NFDStrategySet(strategy_req)
    return response(ack_replay)

def response(ack_replay):
  return { "ack_code": ack_replay.ack_code, "ack_msg": ack_replay.ack_msg }