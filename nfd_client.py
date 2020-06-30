# compile and testing infomation
# python -m grpc_tools.protoc -I/root/nfd-grpc --python_out=/root/nfd-grpc --grpc_python_out=/root/nfd-grpc /root/nfd-grpc/nfd_agent.proto
# python nfd_client.py --face list
# python nfd_client.py --face show --faceid 1
# python nfd_client.py --face create --remote udp://192.168.123.123 # case of udp4
# python nfd_client.py --face create --remote ether://[02:42:20:6f:af:7e] --local dev://eth0 --persistency permanent # case of L2
#
# python nfd_client.py --fib list
#
# python nfd_client.py --route list
# python nfd_client.py --route list --nexthop [FACEID|FACEURI] --origin [ORIGIN]
# python nfd_client.py --route list --nexthop 257 --origin app
# python nfd_client.py --route show --prefix /localhost/nfd
# python nfd_client.py --route add --prefix <PREFIX> --nexthop <FACEID|FACEURI> [--origin <ORIGIN>] [--cost <COST>] [--expires <EXPIRATION-MILLIS>]
# python nfd_client.py --route add --prefix /localhost/nfd/test --nexthop 257
# python nfd_client.py --route add --prefix /localhost/nfd/test --nexthop udp://192.168.123.123
# python nfd_client.py --route add --prefix /localhost/nfd/test --nexthop 257 --cost 100
# python nfd_client.py --route remove --prefix <PREFIX> --nexthop <FACEID|FACEURI> [--origin <ORIGIN>]
# python nfd_client.py --route remove --prefix /localhost/nfd/test --nexthop 257
# python nfd_client.py --route remove --prefix /localhost/nfd/test --nexthop udp://192.168.123.123
# python nfd_client.py --route remove --prefix /localhost/nfd/test --nexthop 257 --origin static
#
# python nfd_client.py --status report --format text # or xml
#
# python nfd_client.py --strategy list
# python nfd_client.py --strategy show --prefix /localhost
# python nfd_client.py --strategy set --prefix /localhost --strategyname /localhost/nfd/strategy/best-route/%FD%05
# python nfd_client.py --strategy unset --prefix /localhost
# python nfd_client.py --strategy unset --prefix /localhost
# python nfd_client.py --advertise set --mode advertise --prefix /test/test/1
# python nfd_client.py --lsdb list

from __future__ import print_function
import logging
import argparse

import grpc

import nfd_agent_pb2
import nfd_agent_pb2_grpc

from google.protobuf import empty_pb2

def nfd_face_list(nfd_stup, **kwargs):
    face_list = nfd_stup.NFDFaceList(nfd_agent_pb2.NFDFaceIDReq(faceid=kwargs.get('faceid', 0)))
    
    if face_list.ack.ack_code == 'ok':
        if len(face_list.faces) > 0:
            for face in face_list.faces:
                print("face list => faceid=%s, remote=%s, local=%s, "
                            "congestion=%s, mtu=%s, counters=%s, "
                            "out=%s, flags=%s" % 
                            (face.faceid, face.remote, face.local,
                            face.congestion, face.mtu, face.counters,
                            face.out, face.flags))
        else:
            print("No face list information")
    else:
        print("Failed to face list information")
        print("=>%s" % face_list.ack.ack_msg)


def nfd_face_create(nfd_stup, **kwargs):
    face_create_req = nfd_agent_pb2.NFDFaceCreateReq()
    if kwargs.get('remote'):
        face_create_req.remote = kwargs.get('remote')
    if kwargs.get('persistency'):
        face_create_req.persistency = kwargs.get('persistency')
    if kwargs.get('local'):
        face_create_req.local = kwargs.get('local')
    if kwargs.get('reliability'):
        face_create_req.reliability = kwargs.get('reliability')
    if kwargs.get('congestion_marking'):
        face_create_req.congestion_marking = kwargs.get('congestion_marking')
    if kwargs.get('congestion_marking_interval'):
        face_create_req.congestion_marking_interval = kwargs.get('congestion_marking_interval')
    if kwargs.get('congestion_marking_interval'):
        face_create_req.congestion_marking_interval = kwargs.get('congestion_marking_interval')
    if kwargs.get('default_congestion_threshold'):
        face_create_req.default_congestion_threshold = kwargs.get('default_congestion_threshold')
    if kwargs.get('mtu'):
        face_create_req.mtu = kwargs.get('mtu')

    ack_replay = nfd_stup.NFDFaceCreate(face_create_req)
    if ack_replay.ack_code == 'ok':
        print("Create a face information")
        print("=>%s" % ack_replay.ack_msg)
    else:
        print("Failed to create a face information")
        print("=>%s" % ack_replay.ack_msg)


def nfd_face_destroy(nfd_stup, **kwargs):
    if kwargs.get('faceid'):
        ack_replay = nfd_stup.NFDFaceDestroy(nfd_agent_pb2.NFDFaceIDReq(faceid=kwargs.get('faceid')))

        if ack_replay.ack_code == 'ok':
            print("Destroy a face information")
            print("=>%s" % ack_replay.ack_msg)
        else:
            print("Failed to delete a face information")
            print("=>%s" % ack_replay.ack_msg)
    else:
        print("No faceid parameter")


def nfd_fib_list(nfd_stup, **kwargs):
    fib_list = nfd_stup.NFDFibList(nfd_agent_pb2.NFDFaceIDReq(faceid=kwargs.get('faceid', 0)))
    
    if fib_list.ack.ack_code == 'ok':
        if len(fib_list.fib) > 0:
            for item in fib_list.fib:
                print("fib ==>%s" % item)
        else:
            print("No Fib information")
    else:
        print("Failed to fib information")
        print("=>%s" % fib_list.ack.ack_msg)


def nfd_route_list(nfd_stup, **kwargs):
    route_list = nfd_stup.NFDRouteList(
                            nfd_agent_pb2.NFDRouteListReq(
                                nexthop=kwargs.get('nexthop', '0'),
                                origin=kwargs.get('origin', '')))

    if route_list.ack.ack_code == 'ok':
        if len(route_list.route) > 0:
            for item in route_list.route:
                print("route list ==>%s" % item)
        else:
            print("No Route list information")
    else:
        print("Failed to route list information")
        print("=>%s" % route_list.ack.ack_msg)

def nfd_route_show(nfd_stup, **kwargs):
    route_show = nfd_stup.NFDRouteShow(
                            nfd_agent_pb2.NFDRouteShowReq(
                                prefix=kwargs.get('prefix')))

    if route_show.ack.ack_code == 'ok':
        if len(route_show.route) > 0:
            for item in route_show.route:
                print("route show ==>%s" % item)
        else:
            print("No Route show information")
    else:
        print("Failed to route show information")
        print("=>%s" % route_show.ack.ack_msg)

def nfd_route_add(nfd_stup, **kwargs):
    route_req = nfd_agent_pb2.NFDRouteReq()
    if kwargs.get('prefix'):
        route_req.prefix = kwargs.get('prefix')
    if kwargs.get('nexthop'):
        route_req.nexthop = kwargs.get('nexthop')
    if kwargs.get('origin'):
        route_req.origin = kwargs.get('origin')
    if kwargs.get('cost'):
        route_req.cost = kwargs.get('cost')
    if kwargs.get('expires'):
        route_req.expires = kwargs.get('expires')

    ack_replay = nfd_stup.NFDRouteAdd(route_req)
    if ack_replay.ack_code == 'ok':
        print("Add route information")
        print("=>%s" % ack_replay.ack_msg)
    else:
        print("Failed to add route information")
        print("=>%s" % ack_replay.ack_msg)

def nfd_route_remove(nfd_stup, **kwargs):
    route_req = nfd_agent_pb2.NFDRouteReq()
    if kwargs.get('prefix'):
        route_req.prefix = kwargs.get('prefix')
    if kwargs.get('nexthop'):
        route_req.nexthop = kwargs.get('nexthop')
    if kwargs.get('origin'):
        route_req.origin = kwargs.get('origin')

    ack_replay = nfd_stup.NFDRouteRemove(route_req)
    if ack_replay.ack_code == 'ok':
        print("Remove route information")
        print("=>%s" % ack_replay.ack_msg)
    else:
        print("Failed to remove route information")
        print("=>%s" % ack_replay.ack_msg)


def nfd_status_report(nfd_stup, **kwargs):
    status_report = nfd_stup.NFDStatusReport(
                        nfd_agent_pb2.NFDStatusReportReq(
                            format=kwargs.get('format', 'text')))

    if status_report.ack.ack_code == 'ok':
        print("status ==>%s" % status_report.report)
    else:
        print("Failed to status report information")
        print("=>%s" % status_report.ack.ack_msg)


def nfd_strategy_list(nfd_stup, **kwargs):
    strategy_list = nfd_stup.NFDStrategyList(empty_pb2.Empty())

    if strategy_list.ack.ack_code == 'ok':
        if len(strategy_list.strategies) > 0:
            for item in strategy_list.strategies:
                print("strategy list ==>%s" % item)
        else:
            print("No strategy list information")
    else:
        print("Failed to strategy list information")
        print("=>%s" % strategy_list.ack.ack_msg)


def nfd_strategy_show(nfd_stup, **kwargs):
    strategy_show = nfd_stup.NFDStrategyShow(
                        nfd_agent_pb2.NFDStrategyReq(
                            prefix=kwargs.get('prefix')))

    if strategy_show.ack.ack_code == 'ok':
        print("strategy show ==>%s" % strategy_show.strategy)
    else:
        print("Failed to strategy show information")
        print("=>%s" % strategy_show.ack.ack_msg)


def nfd_strategy_set(nfd_stup, **kwargs):
    strategy_req = nfd_agent_pb2.NFDStrategyReq()
    if kwargs.get('prefix'):
        strategy_req.prefix = kwargs.get('prefix')
    if kwargs.get('strategy'):
        strategy_req.strategy = kwargs.get('strategy')

    ack_replay = nfd_stup.NFDStrategySet(strategy_req)
    if ack_replay.ack_code == 'ok':
        print("Set strategy information")
        print("=>%s" % ack_replay.ack_msg)
    else:
        print("Failed to set strategy information")
        print("=>%s" % ack_replay.ack_msg)


def nfd_strategy_unset(nfd_stup, **kwargs):
    strategy_req = nfd_agent_pb2.NFDStrategyReq()
    if kwargs.get('prefix'):
        strategy_req.prefix = kwargs.get('prefix')

    ack_replay = nfd_stup.NFDStrategyUnset(strategy_req)
    if ack_replay.ack_code == 'ok':
        print("Unset strategy information")
        print("=>%s" % ack_replay.ack_msg)
    else:
        print("Failed to unset strategy information")
        print("=>%s" % ack_replay.ack_msg)


def nlsr_advertise_name(nfd_stup, **kwargs):
    advertise_req = nfd_agent_pb2.NLSRAdvertiseReq()
    if kwargs.get('mode'):
        advertise_req.mode = kwargs.get('mode')
    if kwargs.get('prefix'):
        advertise_req.prefix = kwargs.get('prefix')
    if kwargs.get('save'):
        advertise_req.save = kwargs.get('save')


    ack_replay = nfd_stup.NLSRAdvertiseName(advertise_req)
    if ack_replay.ack_code == 'ok':
        print("nlsr advertise information")
        print("=>%s" % ack_replay.ack_msg)
    else:
        print("Failed to nlsr advertise information")
        print("=>%s" % ack_replay.ack_msg)

def nlsr_lsdb_list(nfd_stup, **kwargs):
    lsdb_list = nfd_stup.NLSRLsdbList(empty_pb2.Empty())
    
    if lsdb_list.ack.ack_code == 'ok':
        if len(lsdb_list.lsdbs) > 0:
            for item in lsdb_list.lsdbs:
                print("lsdb ==>%s" % item)
        else:
            print("No lsdb information")
    else:
        print("Failed to lsdb information")
        print("=>%s" % lsdb_list.ack.ack_msg)


def client_to_agent(command_opt, **kwargs):
    with grpc.insecure_channel(
            target='localhost:50051',
            options=[('grpc.enable_retries', 0),
                     ('grpc.keepalive_timeout_ms', 10000)]) as channel:
        stub = nfd_agent_pb2_grpc.NFDRouterAgentStub(channel)

        #############################
        ## face command
        if command_opt == 'face list':
            nfd_face_list(nfd_stup=stub, **kwargs)
        elif command_opt == 'face show':
            nfd_face_list(nfd_stup=stub, **kwargs)
        elif command_opt == 'face create':
            nfd_face_create(nfd_stup=stub, **kwargs)
        elif command_opt == 'face destroy':
            nfd_face_destroy(nfd_stup=stub, **kwargs)

        #############################
        ## fib command
        elif command_opt == 'fib list':
            nfd_fib_list(nfd_stup=stub, **kwargs)

        #############################
        ## route command
        elif command_opt == 'route list':
            nfd_route_list(nfd_stup=stub, **kwargs)
        elif command_opt == 'route show':
            nfd_route_show(nfd_stup=stub, **kwargs)
        elif command_opt == 'route add':
            nfd_route_add(nfd_stup=stub, **kwargs)
        elif command_opt == 'route remove':
            nfd_route_remove(nfd_stup=stub, **kwargs)

        #############################
        ## status command
        elif command_opt == 'status report':
            nfd_status_report(nfd_stup=stub, **kwargs)

        #############################
        ## status command
        elif command_opt == 'strategy list':
            nfd_strategy_list(nfd_stup=stub, **kwargs)
        elif command_opt == 'strategy show':
            nfd_strategy_show(nfd_stup=stub, **kwargs)
        elif command_opt == 'strategy set':
            nfd_strategy_set(nfd_stup=stub, **kwargs)
        elif command_opt == 'strategy unset':
            nfd_strategy_unset(nfd_stup=stub, **kwargs)

        #############################
        ## nlsr advertise or withdraw
        elif command_opt == 'advertise name':
            nlsr_advertise_name(nfd_stup=stub, **kwargs)
        elif command_opt == 'lsdb list':
            nlsr_lsdb_list(nfd_stup=stub, **kwargs)

        else:
            print("Currently, %s command is not support" % command_opt)

if __name__ == '__main__':
    logging.basicConfig()
    parser = argparse.ArgumentParser(description='nfd-client for gRPC')
    ###########################
    ## face command
    parser.add_argument('--face', required=False, help='face list or [show, create, destroy]')
    #==> face create subcommand
    parser.add_argument('--remote', required=False, help='face create remote [udp://127.0.0.1]')
    parser.add_argument('--persistency', required=False, help='face create ... persistency [persistent(the default) or permanent]')
    parser.add_argument('--local', required=False, help='face create ... local [dev://eth0]')
    parser.add_argument('--mtu', required=False, help='face create ... mtu [4000]')
    #==> face show and destroy subcommand or fib list
    parser.add_argument('--faceid', required=False, help='face uses show or destroy[faceid]')

    ###########################
    ## fib command
    parser.add_argument('--fib', required=False, help='fib list')

    ###########################
    ## route command
    parser.add_argument('--route', required=False, help='route list or [show, add, remove]')
    #==> route list or add subcommand
    parser.add_argument('--nexthop', required=False, help='list|add nexthop <FACEID|FACEURI>')
    parser.add_argument('--origin', required=False, help='list|add origin <ORIGIN:static>')
    #==> route show or add subcommand
    parser.add_argument('--prefix', required=False, help='show|add prefix <PREFIX:/localhost/nfd>')
    #==> route add subcommand
    parser.add_argument('--cost', required=False, help='add ... cost <COST:100>')
    parser.add_argument('--expires', required=False, help='add ... expires <EXPIRATION-MILLIS>')

    ###########################
    ## status report command
    parser.add_argument('--status', required=False, help='nfd status report [format <text|xml>]')
    parser.add_argument('--format', required=False, help='status ... format <text|xml>')

    ###########################
    ## strategy command
    parser.add_argument('--strategy', required=False, help='strategy list or [show set unset] --prefix [PREFIX]')
    parser.add_argument('--strategyname', required=False, help='set ... strategy <STRATEGY>')
    ###########################
    ## nlsrc command
    parser.add_argument('--advertise', required=False, help='set')
    parser.add_argument('--mode', required=False, help='advertise|withdraw')
    parser.add_argument('--save', required=False, help='save|delete')
    parser.add_argument('--lsdb', required=False, help='list')
    ###########################
    args = parser.parse_args()
    #print(args.__dict__)

    ###########################
    ## face command
    if args.face == 'list':
        client_to_agent(command_opt='face list', faceid=0)
    elif args.face == 'show':
        if args.faceid:
            try:
                faceid = int(args.faceid)
            except ValueError:
                faceid = 0
                print('faceid only number')
            else:
                client_to_agent(command_opt='face show', faceid=faceid)
        else:
            print('need faceid : --faceid [NUMBER]')
    elif args.face == 'create':
        args_dict={'remote': args.remote, 'persistency': args.persistency,
                   'local': args.local, 'mtu': args.mtu}
        client_to_agent(command_opt='face create', **args_dict)
    elif args.face == 'destroy':
        client_to_agent(command_opt='face destroy', faceid=int(args.faceid))
    elif args.fib == 'list':
        if not args.faceid:
            faceid = 0
        else:
            try:
                faceid = int(args.faceid)
            except ValueError:
                faceid = 0
        client_to_agent(command_opt='fib list', faceid=faceid)

    ###########################
    ## route command
    elif args.route == 'list':
        nexthop, origin = ['0', '']
        if args.nexthop: nexthop = args.nexthop
        if args.origin: origin = args.origin
        client_to_agent(command_opt='route list', nexthop=nexthop, origin=origin)
    elif args.route == 'show':
        if args.prefix:
            client_to_agent(command_opt='route show', prefix=args.prefix)
        else:
            print('need prefix : --prefix [PREFIX]')
    elif args.route == 'add':
        if args.prefix and args.nexthop:
            client_to_agent(command_opt='route add', prefix=args.prefix, nexthop=args.nexthop)
        else:
            print('need prefix and nexthop : --prefix [PREFIX] --nexthop [FACEID|FACEURI]')
    elif args.route == 'remove':
        if args.prefix and args.nexthop:
            client_to_agent(command_opt='route remove', prefix=args.prefix, nexthop=args.nexthop)
        else:
            print('need prefix and nexthop : --prefix [PREFIX] --nexthop [FACEID|FACEURI]')
    ###########################
    ## status command
    elif args.status == 'report':
        client_to_agent(command_opt='status report', format=args.format)

    ###########################
    ## strategy command
    elif args.strategy == 'list':
        client_to_agent(command_opt='strategy list', prefix='')
    elif args.strategy == 'show':
        if args.prefix:
            client_to_agent(command_opt='strategy show', prefix=args.prefix)
        else:
            print('need prefix : --prefix [PREFIX]')
    elif args.strategy == 'set':
        if args.prefix and args.strategyname:
            client_to_agent(command_opt='strategy set', prefix=args.prefix, strategy=args.strategyname)
        else:
            print('need prefix : --prefix [PREFIX] --strategyname [STRATEGY]')
    elif args.strategy == 'unset':
        if args.prefix:
            client_to_agent(command_opt='strategy unset', prefix=args.prefix)
        else:
            print('need prefix : --prefix [PREFIX]')

    ###########################
    ## nlsrc command
    elif args.advertise == 'set':
        if args.mode: mode = args.mode
        if args.prefix: prefix = args.prefix
        save = ''
        if args.save: save = args.save
        client_to_agent(command_opt='advertise name', mode=mode, prefix=prefix, save=save)
    elif args.lsdb == 'list':
        client_to_agent(command_opt='lsdb list')

    else:
        print('usage: python nfd_client.py -h')
