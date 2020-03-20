from k8s_client import K8s
import nfd_agent_pb2
import nfd_agent_pb2_grpc
import grpc
import json
from google.protobuf import empty_pb2

class VIcsnf:
  def __init__(self):
    self.k8s = K8s()
  def create(self, params):
      # Maybe a list of POD -> Create pod parallel
    return self.k8s.create_pod(params)

class GrpcClient:
  def __init__(self, nfd_agent_ip):
    with grpc.insecure_channel(
            target= nfd_agent_ip,
            options=[('grpc.enable_retries', 0),
                     ('grpc.keepalive_timeout_ms', 10000)]) as channel:
      self.stub = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

class NfdFace:
  def create(self, params):
    nfd_agent_ip = params.get('nfd_agent_ip') + ':50051' if params.get('nfd_agent_id') else 'localhost:50051'
    grpc_client = GrpcClient(nfd_agent_ip)

    face_create_req = nfd_agent_pb2.NFDFaceCreateReq()
    if params.get('remote'):
      face_create_req.remote = params.get('remote')
    if params.get('persistency'):
      face_create_req.persistency = params.get('persistency')
    if params.get('local'):
      face_create_req.local = params.get('local')
    if params.get('reliability'):
      face_create_req.reliability = params.get('reliability')
    if params.get('congestion_marking'):
      face_create_req.congestion_marking = params.get('congestion_marking')
    if params.get('congestion_marking_interval'):
      face_create_req.congestion_marking_interval = params.get('congestion_marking_interval')
    if params.get('congestion_marking_interval'):
      face_create_req.congestion_marking_interval = params.get('congestion_marking_interval')
    if params.get('default_congestion_threshold'):
      face_create_req.default_congestion_threshold = params.get('default_congestion_threshold')
    if params.get('mtu'):
      face_create_req.mtu = params.get('mtu')

    ack_replay = grpc_client.stub.NFDFaceCreate(face_create_req)
    
    return response(ack_replay)

class NfdRoute:
  def create(self, params):
    nfd_agent_ip = params.get('nfd_agent_ip') + ':50051' if params.get('nfd_agent_id') else 'localhost:50051'
    grpc_client = GrpcClient(nfd_agent_ip)
    
    route_req = nfd_agent_pb2.NFDRouteReq()
    if params.get('prefix'):
      route_req.prefix = params.get('prefix')
    if params.get('nexthop'):
      route_req.nexthop = params.get('nexthop')
    if params.get('origin'):
      route_req.origin = params.get('origin')
    if params.get('cost'):
      route_req.cost = params.get('cost')
    if params.get('expires'):
      route_req.expires = params.get('expires')

    ack_replay = grpc_client.stub.NFDRouteAdd(route_req)
    
    return response(ack_replay)

class NfdStrategy:
  def create(self, params):
    nfd_agent_ip = params.get('nfd_agent_ip') + ':50051' if params.get('nfd_agent_id') else 'localhost:50051'
    grpc_client = GrpcClient(nfd_agent_ip)
    
    strategy_req = nfd_agent_pb2.NFDStrategyReq()
    if params.get('prefix'):
      strategy_req.prefix = params.get('prefix')
    if params.get('strategy'):
      strategy_req.strategy = params.get('strategy')

    ack_replay = grpc_client.stub.NFDStrategySet(strategy_req)
    return response(ack_replay)

def response(ack_replay):
  return { 'ack_code': ack_replay.ack_code, 'ack_msg': ack_replay.ack_msg }