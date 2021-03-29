import json
import os
import sys

from os import path

# Interacts with the Focus db file storing and retrieving workspaces and foci
# methods for creating, getting, and updating the focus DB
def setupFocusDb():
    if not path.exists('~/.focus'):
        os.mkdir('~/.focus')
    if not path.exists('~/.focus/focusDb.json')
        baseDb = {
            'cws' : '',
            'cf' : '',
            'workspaces' : {}
        }
        jsonStr = json.dumps(baseDb)
        with open('~/.focus/focusDb.json', 'w') as dbf:
            dbf.write(jsonStr)

def getFocusDb():
    retVal = None
    if not path.exists('~/.focus/focusDb.json'):
        setupFocusDb()
    with open('~/.focus/focusDb.json', 'w') as dbf:
        retVal = json.loads(dbf.readlines())
    return retVal

def publishFocusDb(db):
    jsonStr = json.dumps(db)
    with open('~/.focus/focusDb.json', 'w') as dbf:
        dbf.write(jsonStr)

# Workspace control methods
def addWorkspace(name):
    db = getFocusDb()
    if name not in db['workspaces'].keys():        
        db['workspaces'][name] = {}
    publishFocusDb(db)

def removeWorkspace(name):
    db = getFocusDb()
    if name in db['workspaces'].keys():
        del(db['workspaces'][name])
    publishFocusDb(db)

def setCurrentWorkspace(name=None, create=False):
    '''
    Call without specifying any arguments to unset the current workspace
    '''
    db = getFocusDb()
    if not name:
        name = ''
    elif not name in db['workspaces'].keys():
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
def addFocus(name, ws=None, focusPath=None, create=False):
    db = getFocusDb()
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
    elif ws not in db['workspaces'].keys():
            if create:
                addWorkspace(ws)

    db['workspaces'][ws][name] = focusPath
    publishFocusDb(db)

def removeFocus(name, ws=None):
    db = getFocusDb()
    if not ws:
        ws = getCurrentWorkspace()
    elif ws not in db['workspaces'].keys():
        print (f'no namespace \'{ws}\' found')
    
    if name in db['workspaces'][ws].keys():
        del(db['workspaces'][ws][name])
    publishFocusDb(db)

def getFocusPath(name, ws=None, focusPath=None, create=False):
    db = getFocusDb()

    if not ws:
        ws = getCurrentWorkspace()
    else:
        setCurrentWorkspace(ws, create)

    if not name in db['workspaces'][ws].keys():
        if create:
            addFocus(name, ws, focusPath, create)
    return db['workspaces'][ws][name]
