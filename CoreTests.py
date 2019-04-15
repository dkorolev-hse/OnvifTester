from onvif import ONVIFCamera, ONVIFError
from utils.probe_match import probe_match


class CoreTests:
    def __init__(self, cam):
        self.cam = cam

    def GetSupportedServices(self):
        services_list = [
            'Devicemgmt', 'Media', 'Imaging', 'Analytics', 
            'PTZ', 'DeviceIO', 'Events', 'Replay', 
            'Recording', 'Search', 'Pullpoint', 'Receiver'
        ]

        services_status = []

        for service_name in services_list:
            name = service_name.lower()
            try:
                service = self.cam.get_service(name)
                services_status.append({
                    "name": service_name,
                    "supported": service is not None
                })
            except ONVIFError as e:
                services_status.append({
                    "name": service_name,
                    "supported": False
                })

        return {
            'test_id': 0, # do we really need it?
            'service': 'Core',
            'name': 'GetSupportedServices',
            'result': {
                'supported': True,
                'extension': None,
                'services_status': services_status
            }

        }


    def GetCapabilities(self):
        capabilities = self.cam.devicemgmt.GetCapabilities()
        if (len(capabilities) > 0):
            return {'test_id': 1, 'name': 'GetCapabilities', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(capabilities)}}
        else:
            return {'test_id': 1, 'name': 'GetCapabilities', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetCapabilitiesResponse message',
            'response': str(capabilities)}}

    def GetDiscoveryMode(self):
        request = self.cam.devicemgmt.GetDiscoveryMode()
        if (request):
            return {'test_id': 2, 'name': 'GetDiscoveryMode', 'service': 'Core',
            'result': {'supported': True, 'extension': 'This operation got the discovery mode of a device',
             'response': str(request)}}
         
        else:
            return {'test_id': 2, 'name': 'GetDiscoveryMode', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetDiscoveryModeResponse message',
            'response': str(request)}}

    def SetDiscoveryMode(self):
        get1 = self.cam.devicemgmt.GetDiscoveryMode()
        if (get1 == 'Discoverable'):
            set1 = self.cam.devicemgmt.SetDiscoveryMode({'DiscoveryMode': 'NonDiscoverable'})
            get2 = self.cam.devicemgmt.GetDiscoveryMode()
            self.cam.devicemgmt.SetDiscoveryMode({'DiscoveryMode': get1})
            if (get1 != get2 ):
                return {'test_id': 3, 'name': 'SetDiscoveryMode', 'service': 'Core',
                'result': {'supported': True, 'extension': 'Was Discoverable, Set NonDiscoverable, Left Discoverable',
                'response': str(set1)}}
            else:
                return {'test_id': 3, 'name': 'SetDiscoveryMode', 'service': 'Core',
                'result': {'supported': False, 'extension': 'DiscoveryMode was Discoverable, the DUT did not SetDiscoveryMode as NonDiscoverable',
                'response': str(set1)}}
        elif (get1 == 'NonDiscoverable'):
            set1 = self.cam.devicemgmt.SetDiscoveryMode({'DiscoveryMode': 'Discoverable'})
            get2 = self.cam.devicemgmt.GetDiscoveryMode()
            self.cam.devicemgmt.SetDiscoveryMode({'DiscoveryMode': get1})
            if (get1 != get2):
                return {'test_id': 3, 'name': 'SetDiscoveryMode', 'service': 'Core',
                'result': {'supported': True, 'extension': 'Was NonDiscoverable, Set Discoverable, Left NonDiscoverable',
                'response': str(set1)}}
            else:
                return {'test_id': 3, 'name': 'SetDiscoveryMode', 'service': 'Core',
                'result': {'supported': False, 'extension': 'DiscoveryMode was NonDiscoverable, the DUT did not SetDiscoveryMode as Discoverable',
                'response': str(set1)}}
        else:
            return {'test_id': 3, 'name': 'SetDiscoveryMode', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send SetDiscoveryModeResponse message',
            'response': str(set1)}}

    def GetScopes(self):
        response = self.cam.devicemgmt.GetScopes()
        if (len(response) > 0):
            return {'test_id': 4, 'name': 'GetScopes', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(response)}}
        else:
            return {'test_id': 4, 'name': 'GetScopes', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetScopesResponse message. The DUT scope list does not have one or more mandatory scope entry.',
            'response': str(response)}}

    def AddScopes(self):
        item = "onvif://www.onvif.org/add/scope"
        add = self.cam.devicemgmt.AddScopes({'ScopeItem': item})
        probe_match()
        gett = self.cam.devicemgmt.GetScopes()
        if (gett != []):
            gett = self.cam.devicemgmt.GetScopes()[-1].ScopeItem
        probe_match()
        self.cam.devicemgmt.RemoveScopes({'ScopeItem': item})
        if (item == gett and add is not None):
            return {'test_id': 5, 'name': 'AddScopes', 'service': 'Core',
            'result': {'supported': True, 'extension': 'Added new Configurable Scope: {}'.format(item), 'response': str(add)}}
        if (item == gett and add is None):
            return {'test_id': 5, 'name': 'AddScopes', 'service': 'Core',
            'result': {'supported': True, 'extension': 'Added new Configurable Scope: {}, but DUT did not send a valid AddScopesResponse Message.'.format(item), 'response': str(add)}}
        else:
            return {'test_id': 5, 'name': 'AddScopes', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not add new scope, {}'.format(item), 'response': str(add)}}
            
    def RemoveScopes(self):
        item = "onvif://www.onvif.org/remove/scope"
        add = self.cam.devicemgmt.AddScopes({'ScopeItem': item})
        probe_match()
        remove = self.cam.devicemgmt.RemoveScopes({'ScopeItem': item})
        probe_match()
        gett = self.cam.devicemgmt.GetScopes()
        if (gett != []):
            gett = self.cam.devicemgmt.GetScopes()[-1].ScopeItem
        if (item != gett and remove is not None):
            return {'test_id': 6, 'name': 'RemoveScopes', 'service': 'Core',
            'result': {'supported': True, 'extension': 'Removed added Configurable Scope: {}'.format(item), 'response': str(remove)}}
        if (item != gett and remove is None):
            return {'test_id': 6, 'name': 'RemoveScopes', 'service': 'Core',
            'result': {'supported': True, 'extension': 'Removed added Configurable Scope: {}, but DUT did not send a valid RemoveScopesResponse Message.'.format(item), 'response': str(remove)}}    
        else:
            return {'test_id': 6, 'name': 'RemoveScopes', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not removed new scope, {}'.format(item), 'response': str(remove)}}
      

    def GetHostname(self):
        name = self.cam.devicemgmt.GetHostname()
        if (name):
            return {'test_id': 7, 'name': 'GetHostname', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(name)}}
        else:
            return {'test_id': 7, 'name': 'GetHostname', 'service': 'Core',
            'result': {'supported': False, 'extension': 'DUT did not send GetHostnameResponse message.', 'response': str(name)}}

    def SetHostname(self):
        get1 = self.cam.devicemgmt.GetHostname().Name
        name = "Onviftest1"
        set1 = self.cam.devicemgmt.SetHostname({'Name': name})
        get2 = self.cam.devicemgmt.GetHostname().Name
        self.cam.devicemgmt.SetHostname({'Name': get1})
        if (get1 != get2):
            return {'test_id': 8, 'name': 'SetHostname', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT returned "Onvif_test1" as its Hostname after SetHostname.', 'response': str(get2)}}
        else:
            return {'test_id': 8, 'name': 'SetHostname', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not SetHostname to "Onvif_test1"', 'response': str(set1)}}

    def GetNetworkInterfaces(self):
        interfaces = self.cam.devicemgmt.GetNetworkInterfaces()
        if (interfaces != []):
            return {'test_id': 9, 'name': 'GetNetworkInterfaces', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(interfaces)}}
        else:
            return {'test_id': 9, 'name': 'GetNetworkInterfaces', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetNetworkInterfacesResponse message',
            'response': str(interfaces)}}

    def GetDNS(self):
        dns = self.cam.devicemgmt.GetDNS()
        #print dns
        if (len(dns) > 0):
            return {'test_id': 10, 'name': 'GetDNS', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(dns)}}
        else:
            return {'test_id': 10, 'name': 'GetDNS', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetDNSResponse message.',
            'response': str(dns)}}

    def GetNetworkProtocols(self):
        protocols = self.cam.devicemgmt.GetNetworkProtocols()
        protocols_list = []
        for item in protocols:
            protocols_list.append(str(item.Name))
        print protocols_list
        if (protocols != []):
            return {'test_id': 11, 'name': 'GetNetworkProtocols', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(protocols)}}
        elif((protocols != []) and ("HTTP" not in protocols_list)):
            return {'test_id': 11, 'name': 'GetNetworkProtocols', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT did not send correct information in the GetNetworkProtocolsResponse message. Mandatory HTTP protocol is not present on the list.',
            'response': str(protocols)}}
        elif((protocols != []) and ("RTSP" not in protocols_list)):
            return {'test_id': 11, 'name': 'GetNetworkProtocols', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT did not send correct information in the GetNetworkProtocolsResponse message. RTSP protocol is not present on the list.',
            'response': str(protocols)}}
        else:
            return {'test_id': 11, 'name': 'GetNetworkProtocols', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetNetworkProtocolsResponse message',
            'response': str(protocols)}}

    def GetNetworkDefaultGateway(self):
        gateways = self.cam.devicemgmt.GetNetworkDefaultGateway()
        if (gateways != []):
            return {'test_id': 12, 'name': 'GetNetworkDefaultGateway', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(gateways)}}
        else:
            return {'test_id': 12, 'name': 'GetNetworkDefaultGateway', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetNetworkDefaultGatewayResponse message',
            'response': str(gateways)}}

    def SetNetworkDefaultGateway(self): #"192.168.11.1"
        default = str(self.cam.devicemgmt.GetNetworkDefaultGateway().IPv4Address[0])
        new = '10.1.0.1'
        set1 = self.cam.devicemgmt.SetNetworkDefaultGateway({'IPv4Address': new})
        get1 = str(self.cam.devicemgmt.GetNetworkDefaultGateway().IPv4Address[0])
        set2 = self.cam.devicemgmt.SetNetworkDefaultGateway({'IPv4Address': default})
        if (get1 == new):
            return {'test_id': 13, 'name': 'SetNetworkDefaultGateway', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT set new NetworkDefaultGateway IPv4Address as {}'.format(new), 'response': str(set1)}}
        else:
            return {'test_id': 13, 'name': 'SetNetworkDefaultGateway', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not set new NetworkDefaultGateway',
            'response': str(set1)}}

    def GetDeviceInformation(self):
        info = self.cam.devicemgmt.GetDeviceInformation()
        if (info != []):
            return {'test_id': 14, 'name': 'GetDeviceInformation', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(info)}}
        if ((not(hasattr(info, 'Manufacturer'))) or (not(hasattr(info, 'Model'))) or (not(hasattr(info, 'SerialNumber'))) or (not(hasattr(info, 'HardwareId'))) or (not(hasattr(info, 'FirmwareVersion')))):
            return {'test_id': 14, 'name': 'GetDeviceInformation', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT did not send one or more mandatory information items in the GetDeviceInformationResponse message',
            'response': str(info)}}
        else:
            return {'test_id': 14, 'name': 'GetDeviceInformation', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetDeviceInformationResponse message',
            'response': str(info)}}

    def GetUsers(self):
        users = self.cam.devicemgmt.GetUsers()
        if (users != []):
            return {'test_id': 15, 'name': 'GetUsers', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(users)}}
        else:
            return {'test_id': 15, 'name': 'GetUsers', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetUsersResponse message.',
            'response': str(users)}}
        
    def CreateUsers(self):
        i = 0
        f1 = False
        set1 = self.cam.devicemgmt.CreateUsers({'User':{'Username': 'lalalal', 'Password': 'lXj2N_iP9=1dD', 'UserLevel': 'User'}})
        get1 = self.cam.devicemgmt.GetUsers()
        for i in range(len(get1)):
            if get1[i].Username == 'lalalal':
                f1 = True
        if f1:
            delete = self.cam.devicemgmt.DeleteUsers({'Username':'lalalal'})
            return {'test_id': 16, 'name': 'CreateUsers', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT created an user with {}'.format('Username: lalalal'), 'response': str(set1)}}
        else:
            return {'test_id': 16, 'name': 'CreateUsers', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT could not create a new user', 'response': str(set1)}}

    def DeleteUsers(self):
        i = 0
        f1 = False
        set1 = self.cam.devicemgmt.CreateUsers({'User':{'Username': 'lalalal', 'Password': 'lXj2N_iP9=1dD', 'UserLevel': 'User'}})
        get1 = self.cam.devicemgmt.GetUsers()
        for i in range(len(get1)):
            if get1[i].Username == 'lalalal':
                f1 = True
        if f1:
            delete = self.cam.devicemgmt.DeleteUsers({'Username':'lalalal'})
            return {'test_id': 17, 'name': 'DeleteUsers', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT deleted created user with {}'.format('Username: lalalal'), 'response': str(delete)}}
        else:
            return {'test_id': 17, 'name': 'DeleteUsers', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not delete created user', 'response': str(delete)}}

    def GetNTP(self):
        ntp = self.cam.devicemgmt.GetNTP()
        if (ntp != []):
            return {'test_id': 18, 'name': 'GetNTP', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(ntp)}}
        else:
            return {'test_id': 18, 'name': 'GetNTP', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetNTPResponse message.',
            'response': str(ntp)}}

    def GetServices(self):
        services = self.cam.devicemgmt.GetServices({'IncludeCapability': False})
        cap_services = self.cam.devicemgmt.GetServices({'IncludeCapability': True})
        if (services != [] and cap_services != []):
            return {'test_id': 19, 'name': 'GetServices', 'service': 'Core',
            'result': {'supported': True, 'extension': 'The DUT send a valid response in both cases(IncludeCapability)', 'response': str(services)}}
        else:
            return {'test_id': 19, 'name': 'GetServices', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetServicesResponse message',
            'response': str(services)}}

    def GetSystemDateAndTime(self):
        datetime = self.cam.devicemgmt.GetSystemDateAndTime()
        if (datetime != []):
            return {'test_id': 20, 'name': 'GetSystemDateAndTime', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(datetime)}}
        else:
            return {'test_id': 20, 'name': 'GetSystemDateAndTime', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetSystemDateAndTimeResponse message',
            'response': str(datetime)}}

    def GetSystemUris(self):
        uri = self.cam.devicemgmt.GetSystemUris()
        if (uri != []):
            return {'test_id': 21, 'name': 'GetSystemUris', 'service': 'Core',
            'result': {'supported': True, 'extension': None, 'response': str(uri)}}
        else:
            return {'test_id': 21, 'name': 'GetSystemUris', 'service': 'Core',
            'result': {'supported': False, 'extension': 'The DUT did not send GetSystemUrisResponse message',
            'response': str(uri)}}
    
		