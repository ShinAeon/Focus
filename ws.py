import argparse

import focus as fc

def setCurrentWorkspace(args):
    fc.setCurrentWorkspace(args.workspace, args.register)

def parseArgs():
    dStr = 'Sets current workspace'
    wsHelpStr = 'workspace name to set'
    wsArgHelpStr = 'Creates workspace if it doesn\'t exist already'

    parser = argparse.ArgumentParser(description=dStr)
    parser.add_argument('workspace', help=wsHelpStr, type=str, action='store')
    parser.add_argument('-r', '--register', help=wsArgHelpStr, action='store_true')
    args = parser.parse_args()
    setCurrentWorkspace(args)

def main():
    parseArgs()

if __name__ == '__main__':
    main()
