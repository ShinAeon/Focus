import json
import os
import sys

import pprint as pp

from os import path

focusDbPath = path.join(path.expanduser('~'), '.focus')
focusDbFilePath = path.join(focusDbPath, 'focusDb.json')

# Interacts with the Focus db file storing and retrieving workspaces and foci
# methods for creating, getting, and updating the focus DB
def setupFocusDb():
    if not path.exists(focusDbPath):
        os.mkdir(focusDbPath)
    if not path.exists(focusDbFilePath):
        baseDb = {
            'cws' : '',
            'workspaces' : {}
        }
        jsonStr = json.dumps(baseDb)
        with open(focusDbFilePath, 'w') as dbf:
            dbf.write(jsonStr)

def getFocusDb():
    retVal = None
    if not path.exists(focusDbFilePath):
        setupFocusDb()
    with open(focusDbFilePath, 'r') as dbf:
        retVal = json.loads(''.join(dbf.readlines()))
    return retVal

def publishFocusDb(db):
    jsonStr = json.dumps(db)
    with open(focusDbFilePath, 'w') as dbf:
        dbf.write(jsonStr)

# Workspace control methods
def workspaceExists(name):
    db = getFocusDb()
    return name in db['workspaces'].keys()

def addWorkspace(name):
    db = getFocusDb()
    if not workspaceExists(name):
        db['workspaces'][name] = {}
    publishFocusDb(db)

def removeWorkspace(name):
    db = getFocusDb()
    if workspaceExists(name):
        del(db['workspaces'][name])
        if db['cws'] == name:
            db['cws'] = ''
    publishFocusDb(db)

def setCurrentWorkspace(name=None, create=False):
    '''
    Call without specifying any arguments to unset the current workspace
    '''
    db = getFocusDb()
    if not name:
        name = ''
    elif not workspaceExists(name):
        if create:
            addWorkspace(name)
        else:
            print(f'No registered workspace named {name}.')
            print(f'Specify -r or use \'reg ws\' tool to register a new workspace')
            sys.exit()
    db['cws'] = name
    publishFocusDb(db)

def getCurrentWorkspace():
    db = getFocusDb()
    if db['cws'] == '':
        print(f'No workspace has been activated, activate one with \'ws\' command first')
        sys.exit()
    return db['cws']


# Focus control methods
def focusExists(name, ws=None):
    ''' THIS ASSUMES ws EXISTS WHEN SPECIFIED'''
    if not ws:
        ws = getCurrentWorkspace()
    elif not workspaceExists(ws):
        print(f'Error: specified workspace {ws} not found.')
        sys.exit()
    
    db = getFocusDb()
    return name in db['workspaces'][ws].keys()

def addFocus(name, ws=None, focusPath=None, create=False):
    if not focusPath:
        focusPath = path.abspath(path.curdir)
    else:
        if not path.exists(focusPath):
            if create:
                os.mkdir(focusPath)
            else:
                print(f'Focus path {focusPath} does not exist.')
                print(f'Specify -c/--create when registering or create first.')
                sys.exit()

    if not ws:
        ws = getCurrentWorkspace()
    elif not workspaceExists(ws):
            if create:
                addWorkspace(ws)

    if not focusExists(name, ws):
        db = getFocusDb()
        db['workspaces'][ws][name] = focusPath
        publishFocusDb(db)

def removeFocus(name, ws=None):
    if not ws:
        ws = getCurrentWorkspace()
    elif not workspaceExists(ws):
        print (f'no namespace \'{ws}\' found')
    
    if focusExists():
        db = getFocusDb()
        del(db['workspaces'][ws][name])
        publishFocusDb(db)

def getFocusPath(name, ws=None, focusPath=None, create=False):
    db = getFocusDb()

    if not ws:
        ws = getCurrentWorkspace()
    else:
        setCurrentWorkspace(ws, create)

    if not focusExists(name, ws):
        if create:
            addFocus(name, ws, focusPath, create)
    return db['workspaces'][ws][name]

if __name__ == '__main__':
    db = getFocusDb()
    pp.pprint(db)
