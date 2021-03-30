import argparse
import sys

import focus as fc

def regWs(args):
    if args.delete:
        fc.removeWorkspace(args.workspace)
    else:
        fc.addWorkspace(args.workspace)

def regFocus(args):
    if args.delete:
        fc.removeFocus(args.focus, args.workspace)        
    else:
        fc.addFocus(args.focus, args.workspace, args.path, args.register)
        

def parseArgs():
    dString = 'Tool for handling registration/removal of workspaces and foci'

    spTString = 'Available subcommands'

    # string data for workspace registration
    wsHelpStr = 'Resgister a workspace'
    wsArgStr = 'workspace name to register(no spaces!)'
    wsDArgStr = 'Delete specified workspace and all associated foci'

    # string data for focus registration
    focusHelpStr = 'Register a focus'
    focusArgStr = 'Name of focus to register'
    focusPArgStr = 'Path to focus. Defaults to current directory'
    focusWArgStr = 'Workspace with which to associate new focus. Defaults to current active workspace.'
    focusRArgStr = 'Create path or workspace if needed to register focus'
    focusDArgStr = 'Delete focus from specified workspace(defaults to current workspace)'

    # create the top level parser
    parser = argparse.ArgumentParser(description=dString)
    parser.set_defaults(func=None)
    sp = parser.add_subparsers(title=spTString)

    # Argument parser for workspaces
    wsParser = sp.add_parser('ws', help=wsHelpStr)
    wsParser.add_argument('workspace', type=str, action='store', help=wsArgStr)
    wsParser.add_argument('-d','--delete', action='store_true', help=wsDArgStr)
    wsParser.set_defaults(func=regWs)

    # argument parser for foci
    fParser = sp.add_parser('focus', help=focusHelpStr)
    fParser.add_argument('focus', help=focusArgStr)
    fParser.add_argument('-p', '--path', type=str, help=focusArgStr, action='store', default=None)
    fParser.add_argument('-w', '--workspace', type=str, help=focusArgStr, action='store', default=None)
    fParser.add_argument('-r', '--register', help=focusArgStr, action='store_true')
    fParser.add_argument('-d','--delete', action='store_true', help=focusDArgStr)
    fParser.set_defaults(func=regFocus)

    args=parser.parse_args()
    if args.func:
        args.func(args)

def main():
    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    parseArgs()

if __name__ == '__main__':
    main()
