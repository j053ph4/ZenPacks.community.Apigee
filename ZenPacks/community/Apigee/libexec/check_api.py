#!/usr/bin/env python
from ZenPacks.community.ConstructionKit.libexec.CustomCheckCommand import *
from ZenPacks.community.Apigee.lib.HTTPHandler import *
import uuid, pprint
from time import time

class ApiMethodCheck(CustomCheckCommand):
    '''''' 
    def __init__(self):
        CustomCheckCommand.__init__(self)
        self.http = HTTPHandler()
        self.sessionid = 0
        self.start = time()
        self.duration = 0
        
    def getUUID(self):
        uid = uuid.uuid1()
        UUID = str(uid)
        self.agero_correlation = "uuid%s" % UUID
        self.agero_session = "uuidWEB_%s" % UUID
    
    def getSession(self):
        #print "getSession"
        self.http.headers = {
                             'Content-type': 'application/json',
                             'AAS-API-Key': self.options.apikey,
                             }
        
        data = {'authenticate': {
                                'userid': self.options.user, 
                                'password': self.options.password,
                                'brand-s' : 'I',
                                'language-s' : 'EN',
                                'country': 'US'
                                }
                }
        self.http.connect(self.options.sessionurl)
        self.http.post(data)
        self.http.outputheaders = True
        self.http.submit()
        self.http.getresponse()
        self.sessionid =  self.http.response.get('AAS-User-Session-ID')
    
    def getToken(self):
        data = { 'key': self.sessionid, "language":"EN", "country":"US"}
        self.http.connect(self.options.tokenurl)
        self.http.post(data)
        self.http.outputheaders = False
        self.http.submit()
        self.http.getresponse()
        self.token = self.http.response['token']
    
    def runTest(self):
        self.http.headers = {
                             'Content-type': 'application/json',
                             'X-agero-correlation-id': self.agero_correlation,
                             'X-agero-session-id': self.agero_session,
                             'X-agero-security-token' : self.token,
                             'Authorization' : self.options.oemkey
                             }
        self.http.connect(self.options.methodurl)
        self.http.submit()
        self.http.getresponse()
    
    def initialize(self):
        #print 'initialize'
        self.getUUID()
        try:
            self.getSession()
        except:
            self.message = "CRITICAL:  Could not acquire session with: %s|duration=%s" % ( self.options.sessionurl, time() - self.start)
            self.status = 2
            self.finished()
        try:
            self.getToken()
        except:
            self.message = "CRITICAL:  Could not acquire token from: %s|duration=%s" % ( self.options.tokenurl, time() - self.start)
            self.status = 2
            self.finished()
        self.runTest()
        
    def evalStatus(self):
        self.duration = time() - self.start
        try:
            check = self.http.response[self.options.responsekey]
            msg = "OK: JSON output exists for key: %s" % self.options.responsekey
        except:
            self.status = 2
            msg = "CRITICAL: JSON output not found for key: %s" % self.options.responsekey
        self.message ="%s|duration=%s" % (msg, self.duration)
    
    def buildOptions(self):
        """
        """
        ZenScriptBase.buildOptions(self)
        self.parser.add_option('--apikey', dest='apikey',
            help='Apigee API Key')
        self.parser.add_option('--user', dest='user',
            help='Apigee User')
        self.parser.add_option('--password', dest='password',
            help='Apigee Password')
        self.parser.add_option('--oemkey', dest='oemkey',
            help='OEM API Key', default=None)
        self.parser.add_option('--sessionurl', dest='sessionurl',
            help='OEM Session URL', default=None)
        self.parser.add_option('--tokenurl', dest='tokenurl',
            help='Agero Token URL', default=None)
        self.parser.add_option('--methodurl', dest='methodurl',
            help='Agero Method URL', default=None)
        self.parser.add_option('--responsekey', dest='responsekey',
            help='Response key check', default=None)

if __name__ == "__main__":
    u = ApiMethodCheck()
    u.run()
