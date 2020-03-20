# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT! 
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import nfd_agent_pb2 as nfd__agent__pb2


class NFDRouterAgentStub(object):
  """NFD and NLSR exported by the server.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.NFDHostNotify = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDHostNotify',
        request_serializer=nfd__agent__pb2.NFDHost.SerializeToString,
        response_deserializer=nfd__agent__pb2.AckReply.FromString,
        )
    self.NFDFaceList = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDFaceList',
        request_serializer=nfd__agent__pb2.NFDFaceIDReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.NFDFaceListRes.FromString,
        )
    self.NFDFaceCreate = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDFaceCreate',
        request_serializer=nfd__agent__pb2.NFDFaceCreateReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.AckReply.FromString,
        )
    self.NFDFaceDestroy = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDFaceDestroy',
        request_serializer=nfd__agent__pb2.NFDFaceIDReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.AckReply.FromString,
        )
    self.NFDFibList = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDFibList',
        request_serializer=nfd__agent__pb2.NFDFaceIDReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.NFDFibListRes.FromString,
        )
    self.NFDRouteList = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDRouteList',
        request_serializer=nfd__agent__pb2.NFDRouteListReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.NFDRouteListRes.FromString,
        )
    self.NFDRouteShow = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDRouteShow',
        request_serializer=nfd__agent__pb2.NFDRouteShowReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.NFDRouteShowRes.FromString,
        )
    self.NFDRouteAdd = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDRouteAdd',
        request_serializer=nfd__agent__pb2.NFDRouteReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.AckReply.FromString,
        )
    self.NFDRouteRemove = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDRouteRemove',
        request_serializer=nfd__agent__pb2.NFDRouteReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.AckReply.FromString,
        )
    self.NFDStatusReport = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDStatusReport',
        request_serializer=nfd__agent__pb2.NFDStatusReportReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.NFDStatusReportRes.FromString,
        )
    self.NFDStrategyList = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDStrategyList',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=nfd__agent__pb2.NFDStrategyListRes.FromString,
        )
    self.NFDStrategyShow = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDStrategyShow',
        request_serializer=nfd__agent__pb2.NFDStrategyReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.NFDStrategyShowRes.FromString,
        )
    self.NFDStrategySet = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDStrategySet',
        request_serializer=nfd__agent__pb2.NFDStrategyReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.AckReply.FromString,
        )
    self.NFDStrategyUnset = channel.unary_unary(
        '/nfd.NFDRouterAgent/NFDStrategyUnset',
        request_serializer=nfd__agent__pb2.NFDStrategyReq.SerializeToString,
        response_deserializer=nfd__agent__pb2.AckReply.FromString,
        )


class NFDRouterAgentServicer(object):
  """NFD and NLSR exported by the server.
  """

  def NFDHostNotify(self, request, context):
    """A agent-to-external
    Advertisement NFD Infomation
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDFaceList(self, request, context):
    """A external-to-agent
    face command
    rpc NFDFaceList(NFDFaceIDReq) returns (stream NFDFaceListRes) {}
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDFaceCreate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDFaceDestroy(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDFibList(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDRouteList(self, request, context):
    """route command
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDRouteShow(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDRouteAdd(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDRouteRemove(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDStatusReport(self, request, context):
    """status command
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDStrategyList(self, request, context):
    """strategy command
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDStrategyShow(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDStrategySet(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def NFDStrategyUnset(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_NFDRouterAgentServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'NFDHostNotify': grpc.unary_unary_rpc_method_handler(
          servicer.NFDHostNotify,
          request_deserializer=nfd__agent__pb2.NFDHost.FromString,
          response_serializer=nfd__agent__pb2.AckReply.SerializeToString,
      ),
      'NFDFaceList': grpc.unary_unary_rpc_method_handler(
          servicer.NFDFaceList,
          request_deserializer=nfd__agent__pb2.NFDFaceIDReq.FromString,
          response_serializer=nfd__agent__pb2.NFDFaceListRes.SerializeToString,
      ),
      'NFDFaceCreate': grpc.unary_unary_rpc_method_handler(
          servicer.NFDFaceCreate,
          request_deserializer=nfd__agent__pb2.NFDFaceCreateReq.FromString,
          response_serializer=nfd__agent__pb2.AckReply.SerializeToString,
      ),
      'NFDFaceDestroy': grpc.unary_unary_rpc_method_handler(
          servicer.NFDFaceDestroy,
          request_deserializer=nfd__agent__pb2.NFDFaceIDReq.FromString,
          response_serializer=nfd__agent__pb2.AckReply.SerializeToString,
      ),
      'NFDFibList': grpc.unary_unary_rpc_method_handler(
          servicer.NFDFibList,
          request_deserializer=nfd__agent__pb2.NFDFaceIDReq.FromString,
          response_serializer=nfd__agent__pb2.NFDFibListRes.SerializeToString,
      ),
      'NFDRouteList': grpc.unary_unary_rpc_method_handler(
          servicer.NFDRouteList,
          request_deserializer=nfd__agent__pb2.NFDRouteListReq.FromString,
          response_serializer=nfd__agent__pb2.NFDRouteListRes.SerializeToString,
      ),
      'NFDRouteShow': grpc.unary_unary_rpc_method_handler(
          servicer.NFDRouteShow,
          request_deserializer=nfd__agent__pb2.NFDRouteShowReq.FromString,
          response_serializer=nfd__agent__pb2.NFDRouteShowRes.SerializeToString,
      ),
      'NFDRouteAdd': grpc.unary_unary_rpc_method_handler(
          servicer.NFDRouteAdd,
          request_deserializer=nfd__agent__pb2.NFDRouteReq.FromString,
          response_serializer=nfd__agent__pb2.AckReply.SerializeToString,
      ),
      'NFDRouteRemove': grpc.unary_unary_rpc_method_handler(
          servicer.NFDRouteRemove,
          request_deserializer=nfd__agent__pb2.NFDRouteReq.FromString,
          response_serializer=nfd__agent__pb2.AckReply.SerializeToString,
      ),
      'NFDStatusReport': grpc.unary_unary_rpc_method_handler(
          servicer.NFDStatusReport,
          request_deserializer=nfd__agent__pb2.NFDStatusReportReq.FromString,
          response_serializer=nfd__agent__pb2.NFDStatusReportRes.SerializeToString,
      ),
      'NFDStrategyList': grpc.unary_unary_rpc_method_handler(
          servicer.NFDStrategyList,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=nfd__agent__pb2.NFDStrategyListRes.SerializeToString,
      ),
      'NFDStrategyShow': grpc.unary_unary_rpc_method_handler(
          servicer.NFDStrategyShow,
          request_deserializer=nfd__agent__pb2.NFDStrategyReq.FromString,
          response_serializer=nfd__agent__pb2.NFDStrategyShowRes.SerializeToString,
      ),
      'NFDStrategySet': grpc.unary_unary_rpc_method_handler(
          servicer.NFDStrategySet,
          request_deserializer=nfd__agent__pb2.NFDStrategyReq.FromString,
          response_serializer=nfd__agent__pb2.AckReply.SerializeToString,
      ),
      'NFDStrategyUnset': grpc.unary_unary_rpc_method_handler(
          servicer.NFDStrategyUnset,
          request_deserializer=nfd__agent__pb2.NFDStrategyReq.FromString,
          response_serializer=nfd__agent__pb2.AckReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'nfd.NFDRouterAgent', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))