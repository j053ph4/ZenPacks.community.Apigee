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
        self.http.headers = {'Content-type': 'application/json'}
        self.sessionid = 0
        self.start = time()
        self.duration = 0
    
    def getSXMToken(self):
        '''get token from SXM'''
        data = { 
                'client_id': self.options.client_id, 
                'client_secret': self.options.client_secret, 
                'grant_type':'client_credentials'
                }
        self.http.connect(self.options.sxm_token_url)
        self.http.post(data)
        self.http.outputheaders = False
        self.http.submit()
        self.http.getresponse()
        self.sxmtoken = self.http.response['access_token']
    
    def getTMSToken(self):
        '''get token from TMS'''
        self.http.headers = {'Content-type': 'application/json'}
        data = { 
                'username': self.options.tms_user, 
                'password':self.options.tms_password, 
                }
        self.http.connect(self.options.tms_token_url)
        self.http.post(data)
        self.http.outputheaders = False
        self.http.submit()
        self.http.getresponse()
        self.tmstoken = self.http.response['token']
    
    def runTest(self):
        '''perform final functionality test'''
        self.http.headers = {
                             'Content-type': 'application/json',
                             'Authorization': 'Bearer %s' % self.sxmtoken,
                             'X-client-token': self.tmstoken,
                             }
        self.http.connect(self.options.methodurl)
        self.http.submit()
        self.http.getresponse()
    
    def initialize(self):
        '''perform the series of tests'''
        # get SXM Token
        try: 
            self.getSXMToken()
        except:
            self.message = "CRITICAL:  Could not acquire SXM Token with: %s|duration=%s" % ( self.options.sxm_token_url, time() - self.start)
            self.status = 2
            self.finished()
        # get TMS Token
        try:
            self.getTMSToken()
        except:
            self.message = "CRITICAL:  Could not acquire TMS Token from: %s|duration=%s" % ( self.options.tms_token_url, time() - self.start)
            self.status = 2
            self.finished()
        # get Vehicles
        try:
            self.runTest()
        except:
            self.message = "CRITICAL:  Could not test method from: %s|duration=%s" % ( self.options.methodurl, time() - self.start)
            self.status = 2
            self.finished()
    
    def evalStatus(self):
        '''test the final output for validity'''
        self.duration = time() - self.start
        if self.http.response == []:  msg = "OK: Valid response found"
        else: msg = "CRITICAL: Valid response NOT found"
        self.message ="%s|duration=%s" % (msg, self.duration)
    
    def buildOptions(self):
        """
        """
        ZenScriptBase.buildOptions(self)
        self.parser.add_option('--sxm_token_url', dest='sxm_token_url',
            help='SXM Token URL', default='https://api.telematics.net/v1/oauth2/token')
        self.parser.add_option('--client_id', dest='client_id',
            help='SXM Client ID', default='dM91jt9vqMdcIAMONaDPBR7y2DLvzroF')
        self.parser.add_option('--client_secret', dest='client_secret',
            help='SXM Client Secret', default='1AoerLnY1mFvcCjj')
        self.parser.add_option('--tms_token_url', dest='tms_token_url',
            help='TMS Token URL', default='https://telematicsservice.toyota.com/v1/authenticate')
        self.parser.add_option('--tms_user', dest='tms_user',
            help='TMS User', default='SxmApiMontoring')
        self.parser.add_option('--tms_password', dest='tms_password',
            help='TMS Password', default='apimon0987')
        self.parser.add_option('--methodurl', dest='methodurl',
            help='TMS Method URL', default='https://api.telematics.net/v1/keyoff/accounts/SxmApiMontoring/vehicles')

if __name__ == "__main__":
    u = ApiMethodCheck()
    u.run()
