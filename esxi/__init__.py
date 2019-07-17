from optparse import OptionParser
from sys import exit, stderr
import os

from . import models

Client = models.Client


def parse_options(usage='Usage: %prog [options] -H ESXI_HOST -u ESXI_USER'):
    parser = OptionParser(usage=usage)
    parser.add_option('-H', '--host', dest='host', help='hostname of ESXi (Mandatory)')
    parser.add_option('-u', '--user', dest='user', help='username to access ESXi (Mandatory)')
    (options, args) = parser.parse_args()

    if options.host is None:
        print("Error: Option \"-H\" is required\n", file=stderr)
        parser.print_help(file=stderr)
        exit(1)

    if options.user is None:
        print("Error: Option \"-u\" is required\n", file=stderr)
        parser.print_help(file=stderr)
        exit(1)

    setattr(options, 'password', os.getenv('PASSWORD', None))

    if options.password is None:
        print("Environment variable \"PASSWORD\" is required", file=stderr)
        exit(1)

    return options, args
