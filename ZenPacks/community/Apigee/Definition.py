from ZenPacks.community.ConstructionKit.BasicDefinition import *
from ZenPacks.community.ConstructionKit.Construct import *

BASE = "Apigee"
VERSION = Version(1, 0, 0)
ZPROPS = []

DATA = {
        'version' : VERSION,
        'zenpackbase': BASE,
        'component' : 'APIMethod',
        'componentData' : {
                          'singular': 'API Method',
                          'plural': 'API Methods',
                          'properties': {
                                        'eventComponent' : addProperty('Alias',default='MethodName', optional=False),
                                        'apigeeApiKey': addProperty('Apigee API Key'),
                                        'apigeeUserID': addProperty('Apigee User ID'),
                                        'apigeePassword': addProperty('Apigee Password', ptype='password'),
                                        'oemApiKey': addProperty('OEM API Key'),
                                        'oemSessionURL' : addProperty('OEM Session URL'),
                                        'ageroTokenURL' : addProperty('Agero Token URL'),
                                        'methodURL' : addProperty('API Method URL', optional=False),
                                        'responseKey' : addProperty('Response Key Check'),
                                        'eventClass' : getEventClass('/App/APIMethod')
                                        },
                          },
        'addManual' :  True,
        }

ApigeeDefinition = type('ApigeeDefinition', (BasicDefinition,), DATA)
