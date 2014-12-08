#!/usr/bin/env python3

import asyncio
import argparse

from artiq.management.pc_rpc import Server
from artiq.management.scheduler import Scheduler


def _get_args():
    parser = argparse.ArgumentParser(description="ARTIQ master")
    parser.add_argument(
        "--bind", default="::1",
        help="hostname or IP address to bind to")
    parser.add_argument(
        "--port", default=8888, type=int,
        help="TCP port to listen to")
    return parser.parse_args()


def main():
    args = _get_args()
    loop = asyncio.get_event_loop()
    try:
        scheduler = Scheduler("ddb.pyon", "pdb.pyon")
        loop.run_until_complete(scheduler.start())
        try:
            server = Server(scheduler, "master")
            loop.run_until_complete(server.start(args.bind, args.port))
            try:
                loop.run_forever()
            finally:
                loop.run_until_complete(server.stop())
        finally:
            loop.run_until_complete(scheduler.stop())
    finally:
        loop.close()

if __name__ == "__main__":
    main()
