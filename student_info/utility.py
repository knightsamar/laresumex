from django.shortcuts import redirect
from laresumex.settings import ROOT

def errorMaker(msg,fatal=False):
    '''displays the given error message nicely and if it's fatal exits'''
    '''I think Apoorva,u can make this better -- i can't find the function u used in change_agent'''
    print msg;
    if fatal:
        exit
    else:
        return;

def debugger(msg):
    '''handles debugging'''
    
    #currently we only print
    print "DEBUG[%s]: %s" % ('Calling function',msg)
    return
def our_redirect(path):
    return redirect(ROOT+path)
