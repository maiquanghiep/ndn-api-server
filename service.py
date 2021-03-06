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
    vnfs = params.get("vnfs") if params.get("vnfs") else []
    created_pods = []
    errmsg = ""
    for i in vnfs:
      try:
        self.k8s.create_pod(i)
        created_pods.append(i)
        # print(created_pods)
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
    ##vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    vnfs = params.get("vnfs") if params.get("vnfs") else []
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
    vnf_res = {}
    errmsg = ""
    try: 
      vnf_res = self.k8s.get_pod(namespace, vnf_name)
    except ApiException as e:
      body = json.loads(e.body)
      errmsg = body.get("message")

    have_pod = bool(vnf_res)
    vnf_info = {}

    if (have_pod):
      container = vnf_res.spec.containers[0] if len(vnf_res.spec.containers) else {}
      
      # status
      status = vnf_res.status.phase
      
      # port is nested in container["readiness"]["http_get"]["port"]
      readiness_probe = container.readiness_probe if container.readiness_probe else None
      http_get = readiness_probe.http_get if readiness_probe else None
      port = http_get.port if http_get else None
      is_vnc = bool(port)
      vnf_info = {
        "vnf_name": vnf_res.metadata.name,
        "namespace": vnf_res.metadata.namespace,
        "default_ip": vnf_res.metadata.annotations.get('default_ip'),
        "network_ips": json.loads(vnf_res.metadata.annotations.get('k8s.v1.cni.cncf.io/networks').replace("\'", "\"")) if vnf_res.metadata.annotations.get('k8s.v1.cni.cncf.io/networks') else [],
        "image": vnf_res.spec.containers[0].image if have_pod else "",
        "env":  list(map(lambda x: { "name": x.name, "value": x.value },vnf_res.spec.containers[0].env)) if (have_pod & (vnf_res.spec.containers[0].env is not None))  else [],
        "command": vnf_res.spec.containers[0].command if have_pod else [],
        "node_selector": vnf_res.spec.node_selector.get("kubernetes.io/hostname") if have_pod & (vnf_res.spec.node_selector is not None) else "",
        "is_vnc": is_vnc,
        "status": status
      }
    return {
      "vnf": vnf_info,
      "error": errmsg,
      "result": "OK" if have_pod else "ERROR"
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
    #vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    vnfs = params.get("vnfs") if params.get("vnfs") else []
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
            if face.get("neighbor_hostname"):
              face_create_req.neighbor_hostname = face.get("neighbor_hostname")
            if face.get("neighbor_ip"):
              face_create_req.neighbor_ip = face.get("neighbor_ip")
            if face.get("neighbor_site_route"):
              face_create_req.neighbor_site_route = face.get("neighbor_site_route")
              
            #print(face_create_req)
            grpc_res = grpc_client.NFDFaceCreate(face_create_req)
            #print(grpc_res)
            
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
          target= ip + ":50051",
          options=[("grpc.enable_retries", 0),
                    ("grpc.keepalive_timeout_ms", 10000)]) as channel:
      grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

      grpc_res = grpc_client.NFDFaceList(nfd_agent_pb2.NFDFaceIDReq(faceid=0))
      faces = grpc_res.faces
      result = []

      if grpc_res.ack.ack_code == 'ok':
        result= list(map(lambda f: { "faceid": f.faceid, "remote": f.remote, "local": f.local},faces))
        
      return {
        "faces": result
      }

  def delete(self, params):
    #vnfs = json.loads(params.get("vnfs")) if params.get("vnfs") else []
    vnfs = params.get("vnfs") if params.get("vnfs") else []
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

          if face.get("neighbor_hostname"):
            face_delete_req.neighbor_hostname = face.get("neighbor_hostname")
          if face.get("neighbor_ip"):
            face_delete_req.neighbor_ip = face.get("neighbor_ip")
          if face.get("neighbor_site_route"):
            face_delete_req.neighbor_site_route = face.get("neighbor_site_route")

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
    #templates = json.loads(params.get("templates")) if params.get("templates") else []
    templates = params.get("templates") if params.get("templates") else []
    errmsg = ""
    for template in templates:
      vnf_ip = template.get("vnf_ip") + ":50051" if template.get("vnf_ip") else "localhost:50051"
      with grpc.insecure_channel(
        target= vnf_ip,
        options=[("grpc.enable_retries", 0),
                  ("grpc.keepalive_timeout_ms", 10000)]) as channel:
        
        routes = template.get("route_add", [])
        grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
        for route in routes:
          route_req = nfd_agent_pb2.NFDRouteReq()
          if route.get("prefix"):
            route_req.prefix = route.get("prefix")
          if route.get("nexthop"):
            route_req.nexthop = route.get("nexthop")
          if route.get("origin"):
            route_req.origin = route.get("origin")
          if route.get("cost"):
            route_req.cost = route.get("cost")
          if route.get("expires"):
            route_req.expires = route.get("expires")
              
          grpc_res = grpc_client.NFDRouteAdd(route_req)
          ack_code = grpc_res.ack_code

          if ack_code == "err":
            errmsg = grpc_res.ack_msg
            break
          
    return {
      "id": params.get('id'),
      "result": "OK" if not errmsg else "ERROR",
      "errmsg": errmsg
    }

  def delete(self, params):
    templates = params.get("templates") if params.get("templates") else []
    errmsg = ""
    for template in templates:
      vnf_ip = template.get("vnf_ip") + ":50051" if template.get("vnf_ip") else "localhost:50051"
      with grpc.insecure_channel(
        target= vnf_ip,
        options=[("grpc.enable_retries", 0),
                  ("grpc.keepalive_timeout_ms", 10000)]) as channel:
        
        routes = template.get("route_del", [])
        grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
        for route in routes:
          route_req = nfd_agent_pb2.NFDRouteReq()
          if route.get("prefix"):
            route_req.prefix = route.get("prefix")
          if route.get("nexthop"):
            route_req.nexthop = route.get("nexthop")
              
          grpc_res = grpc_client.NFDRouteRemove(route_req)
          ack_code = grpc_res.ack_code

          if ack_code == "err":
            errmsg = grpc_res.ack_msg
            break
          
    return {
      "id": params.get('id'),
      "result": "OK" if not errmsg else "ERROR",
      "errmsg": errmsg
    }

  def get(self, ip):
    with grpc.insecure_channel(
          target= ip + ":50051",
          options=[("grpc.enable_retries", 0),
                    ("grpc.keepalive_timeout_ms", 10000)]) as channel:
      grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

      grpc_res = grpc_client.NFDRouteList(nfd_agent_pb2.NFDRouteListReq(nexthop='0', origin=''))
      fib_list = grpc_res.route
      result = []

      if grpc_res.ack.ack_code == 'ok':
        for fib in fib_list:
          prefix, nexthop, cost = ['','','']
          keys = fib.split()
          for key in keys:
            if 'prefix=' in key:
              prefix = key[len('prefix='):]
            if 'nexthop=' in key:
              nexthop = key[len('nexthop='):]
            if 'cost=' in key:
              cost = key[len('cost='):]
          result.append({ "prefix": prefix, "nexthops": nexthop, "cost": cost })
        
      return {
        "fib_list": result
      }

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

class NFDStrategy:
  def get(self, ip):
    with grpc.insecure_channel(
          target= ip + ":50051",
          options=[("grpc.enable_retries", 0),
                    ("grpc.keepalive_timeout_ms", 10000)]) as channel:
      grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

      grpc_res = grpc_client.NFDStrategyList(empty_pb2.Empty())
      strategy_list = grpc_res.strategies
      result = []

      if grpc_res.ack.ack_code == 'ok':
        for item in strategy_list:
          prefix, strategy = ['','']
          keys = item.split()
          for key in keys:
            if 'prefix=' in key:
              prefix = key[len('prefix='):]
            if 'strategy=' in key:
              strategy = key[len('strategy='):]
          result.append({ "prefix": prefix, "strategy": strategy })
        
      return {
        "strategy_list": result
      }
  def create(self,params):
    templates = params.get("templates") if params.get("templates") else []
    errmsg = ""
    for template in templates:
      vnf_ip = template.get("vnf_ip") + ":50051" if template.get("vnf_ip") else "localhost:50051"
      with grpc.insecure_channel(
        target= vnf_ip,
        options=[("grpc.enable_retries", 0),
                  ("grpc.keepalive_timeout_ms", 10000)]) as channel:
        
        strtegies = template.get("strategy_set", [])
        grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
        for strategy in strtegies:
          strategy_req = nfd_agent_pb2.NFDStrategyReq()
          if strategy.get('prefix'):
              strategy_req.prefix = strategy.get('prefix')
          if strategy.get('strategyname'):
              strategy_req.strategy = strategy.get('strategyname')
              
          grpc_res = grpc_client.NFDStrategySet(strategy_req)
          ack_code = grpc_res.ack_code

          if ack_code == "err":
            errmsg = grpc_res.ack_msg
            break
          
    return {
      "id": params.get('id'),
      "result": "OK" if not errmsg else "ERROR",
      "errmsg": errmsg
    }
    
  def unset(self, params):
    templates = params.get("templates") if params.get("templates") else []
    errmsg = ""
    for template in templates:
      vnf_ip = template.get("vnf_ip") + ":50051" if template.get("vnf_ip") else "localhost:50051"
      strategy_unset = template.get("strategy_unset", [])
      errmsg = ""
      with grpc.insecure_channel(
        target= vnf_ip,
        options=[("grpc.enable_retries", 0),
                  ("grpc.keepalive_timeout_ms", 10000)]) as channel:
         
        grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
        for strategy in strategy_unset:
          strategy_req = nfd_agent_pb2.NFDStrategyReq()
          if strategy.get("prefix"):
            strategy_req.prefix = strategy.get("prefix")
            grpc_res = grpc_client.NFDStrategyUnset(strategy_req)
            ack_code = grpc_res.ack_code
      
            if ack_code == "err":
              errmsg = grpc_res.ack_msg
              break
    return {
      "vnf_ip": params.get('vnf_ip'),
      "result": "OK" if not errmsg else "ERROR",
      "errmsg": errmsg
    }

class NLSR:
  def get(self, ip):
    with grpc.insecure_channel(
          target= ip + ":50051",
          options=[("grpc.enable_retries", 0),
                    ("grpc.keepalive_timeout_ms", 10000)]) as channel:
      grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

      grpc_res = grpc_client.NLSRLsdbList(empty_pb2.Empty())
      lsdbs = grpc_res.lsdbs
      result = []

      if grpc_res.ack.ack_code == 'ok':
        result= list(map(lambda lsdb: { "origin_router": lsdb.origin_router, "prefix": lsdb.prefix}, lsdbs))

      return {
        "lsdb_list": result
      }
      
  def advertise(self,params):
    templates = params.get("templates") if params.get("templates") else []
    errmsg = ""
    for template in templates:
      vnf_ip = template.get("vnf_ip") + ":50051" if template.get("vnf_ip") else "localhost:50051"
      with grpc.insecure_channel(
        target= vnf_ip,
        options=[("grpc.enable_retries", 0),
                  ("grpc.keepalive_timeout_ms", 10000)]) as channel:
        
        advertises = template.get("advertise_set", [])
        grpc_client = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)
        for advertise in advertises:
          advertise_req = nfd_agent_pb2.NLSRAdvertiseReq()
          if advertise.get('mode'):
              advertise_req.mode = advertise.get('mode')
          if advertise.get('prefix'):
              advertise_req.prefix = advertise.get('prefix')
          if advertise.get('save'):
              advertise_req.save = advertise.get('save')
              
          grpc_res = grpc_client.NLSRAdvertiseName(advertise_req)
          ack_code = grpc_res.ack_code

          if ack_code == "err":
            errmsg = grpc_res.ack_msg
            break
          
    return {
      "id": params.get('id'),
      "result": "OK" if not errmsg else "ERROR",
      "errmsg": errmsg
    }
