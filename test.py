
# import getopt
# import optparse
# import argparse
import sys
from optparse import OptionParser

def parse_args(argv):
    parser = OptionParser()
    parser.add_option('-p', '--provision', action='store_true', dest='provision',help='Start provision devices')
    parser.add_option('-r', '--reset', action='store_true',dest='reset' ,help='Reset to Base Configuration')
    parser.add_option('-f', '--final', action='store_true',dest='final', help='reset to Final Configuration')
    (options, args) = parser.parse_args()

    if options.provision:
        print("option is provision")
    elif options.reset:
        print("option is reset")
    elif options.final:
        print("optpion is final")

    # print(options)
    # print(args)
    # if options. == '-p':
    #
    #     print("option is -p")
    # else:
    #     print("not match")


    # print(opts, args)


    # parser.print_help()

if __name__=="__main__":
    parse_args(sys.argv[1:])

    # option = parse_args(sys.argv[1:])
    # print(option)