from onvif import ONVIFCamera, exceptions
from time import sleep


class PTZTests:
    def __init__(self, cam):
        self.cam = cam
        self.event_service = self.cam.create_events_service()
        self.media = self.cam.create_media_service()

    def GetCompatibleConfigurations(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.media.GetProfiles()[0]._token
        ptz.create_type('GetCompatibleConfigurations')
        try:
            configs = ptz.GetCompatibleConfigurations({'ProfileToken': token})
        except exceptions.ONVIFError:
            return {'test_id': 1, 'name': 'GetCompatibleConfigurations', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'This method is not implemented by the device',
                               'response': ''}}
        if configs is None or len(configs) == 0:
            return {'test_id': 1, 'name': 'GetCompatibleConfigurations', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetCompatibleConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 1, 'name': 'GetCompatibleConfigurations', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetConfiguration(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        ptz_token = self.media.GetProfiles()[0].PTZConfiguration._token
        config = ptz.GetConfiguration({'PTZConfigurationToken': ptz_token})
        if config is None or len(config) == 0:
            return {'test_id': 2, 'name': 'GetConfiguration', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetConfigurationResponse message',
                               'response': ''}}
        else:
            return {'test_id': 2, 'name': 'GetConfiguration', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(config)}}

    def GetConfigurationOptions(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        ptz_token = self.media.GetProfiles()[0].PTZConfiguration._token
        configs = ptz.GetConfigurationOptions({'ConfigurationToken': ptz_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 3, 'name': 'GetConfigurationOptions', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetConfigurationOptionsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 3, 'name': 'GetConfigurationOptions', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetConfigurations(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        configs = ptz.GetConfigurations()
        if configs is None or len(configs) == 0:
            return {'test_id': 4, 'name': 'GetConfigurations', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 4, 'name': 'GetConfigurations', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetNodes(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        nodes = ptz.GetNodes()
        if nodes is None or len(nodes) == 0:
            return {'test_id': 5, 'name': 'GetNodes', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetNodesResponse message',
                               'response': ''}}
        else:
            return {'test_id': 5, 'name': 'GetNodes', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(nodes)}}

    def GetNode(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        node_token = ptz.GetConfigurations()[0].NodeToken
        node = ptz.GetNode({'NodeToken': node_token})
        if node is None or len(node) == 0:
            return {'test_id': 6, 'name': 'GetNode', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetNodeResponse message',
                               'response': ''}}
        else:
            return {'test_id': 6, 'name': 'GetNode', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(node)}}

    def AbsoluteMove(self):
        token = self.media.GetProfiles()[0]._token
        try:
            ptz = self.cam.create_ptz_service()
            ptz.create_type("AbsoluteMove")
        except exceptions.ONVIFError:
            return 'Device does not support PTZ service'
        try:
            pos = ptz.GetStatus({"ProfileToken": token}).Position
        except AttributeError:
            return 'Device does not support PTZ'
        try:
            try:
                pos.PanTilt._x
                pos.PanTilt._y
            except AttributeError:
                x_z = pos.Zoom._x
                if x_z + 0.1 < 1:
                    x_z1 = x_z + 0.1
                else:
                    x_z1 = x_z - 0.1
                ptz.AbsoluteMove({"ProfileToken": token, "Position": {"Zoom": {"_x": x_z1}}})
                sleep(3)
                pos = ptz.GetStatus({"ProfileToken": token}).Position
                x_z = pos.Zoom._x
                dif3 = (round((x_z1-x_z), 3))
                print dif3
                if dif3 == 0.0:
                    return 'AbsoluteMove supported partly, works only zoom. Current zoom coordinates: ' + str(x_z)
                else:
                    return 'AbsoluteMove is not supported'
            x_z, x, y = pos.Zoom._x, pos.PanTilt._x, pos.PanTilt._y
            if x + 0.1 < 1:
                x1 = x + 0.1
            else:
                x1 = x - 0.1
            if y + 0.1 < 1:
                y1 = y + 0.1
            else:
                y1 = y - 0.1
            if x_z + 0.1 < 1:
                x_z1 = x_z + 0.1
            else:
                x_z1 = x_z - 0.1
            # print x_z
            ptz.AbsoluteMove({"ProfileToken": token, "Position":
                                  {"PanTilt": {"_x": x1, "_y": y1}, "Zoom": {"_x": x_z1}}})
            sleep(3)
            pos = ptz.GetStatus({"ProfileToken": token}).Position
            x_z = pos.Zoom._x
            x = pos.PanTilt._x
            y = pos.PanTilt._y
            dif1 = (round((x1-x), 6))
            dif2 = (round((y1-y), 6))
            dif3 = (round((x_z1-x_z), 6))
            if dif1 == 0.0 and dif2 == 0.0 and dif3 == 0.0:
                result = 'AbsoluteMove is supported, current coordinates: ' + str(x) + ' ' + str(y) + ' ' + str(x_z)
                return {'test_id': 7, 'name': 'AbsoluteMove', 'service': 'PTZ',
                        'result': {'supported': True, 'extension': None, 'response': str(result)}}
            elif dif1 == 0.0 and dif2 == 0.0 and dif3 != 0.0:
                result = 'AbsoluteMove is supported, but Zoom does not work. Current coordinates: ' \
                           + str(x) + ' ' + str(y) + ' ' + str(x_z)
                return {'test_id': 7, 'name': 'AbsoluteMove', 'service': 'PTZ',
                        'result': {'supported': True, 'extension': 'AbsoluteMove partly supported',
                                   'response': str(result)}}
            else:
                return {'test_id': 7, 'name': 'AbsoluteMove', 'service': 'PTZ',
                        'result': {'supported': False, 'extension': 'AbsoluteMove is not supported, '
                                                                    'camera does not move', 'response': ''}}
        except AttributeError:
            return {'test_id': 7, 'name': 'AbsoluteMove', 'service': 'PTZ',
                    'result': {'supported': False, 'extension': 'AbsoluteMove is not supported, AttributeError ',
                               'response': ''}}
    def GetPresets(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.media.GetProfiles()[0]._token
        presets = ptz.GetPresets({'ProfileToken': token})
        print presets
        if presets is None or len(presets) == 0:
            return {'test_id': 8, 'name': 'GetPresets', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetPresetsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 8, 'name': 'GetPresets', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(presets)}}

    def CreatePresetTour(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.media.GetProfiles()[0]._token
        tour = ptz.CreatePresetTour({'ProfileToken': token})
        print tour
        ptz.RemovePresetTour({'ProfileToken': token, 'PresetTourToken': tour})
        if tour is None or len(tour) == 0:
            return {'test_id': 9, 'name': 'CreatePresetTour', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetPresetsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 9, 'name': 'CreatePresetTour', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': 'PresetTourToken: ' + str(tour)}}

    def GetPresetTour(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.media.GetProfiles()[0]._token
        tour_token = ptz.CreatePresetTour({'ProfileToken': token})
        tour = ptz.GetPresetTour({'ProfileToken': token, 'PresetTourToken': tour_token})
        ptz.RemovePresetTour({'ProfileToken': token, 'PresetTourToken': tour_token})
        if tour is None or len(tour) == 0:
            return {'test_id': 10, 'name': 'GetPresetTour', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetPresetTourResponse message',
                               'response': ''}}
        else:
            return {'test_id': 10, 'name': 'GetPresetTour', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(tour)}}

    def GetPresetTours(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.media.GetProfiles()[0]._token
        tours = ptz.GetPresetTours({'ProfileToken': token})
        if tours is None or len(tours) == 0:
            return {'test_id': 11, 'name': 'GetPresetTour', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetPresetToursResponse message',
                               'response': ''}}
        else:
            return {'test_id': 11, 'name': 'GetPresetTours', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(tours)}}

    def GetPresetTourOptions(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.media.GetProfiles()[0]._token
        tour_token = ptz.CreatePresetTour({'ProfileToken': token})
        tour = ptz.GetPresetTourOptions({'ProfileToken': token, 'PresetTourToken': tour_token})
        ptz.RemovePresetTour({'ProfileToken': token, 'PresetTourToken': tour_token})
        if tour is None or len(tour) == 0:
            return {'test_id': 12, 'name': 'GetPresetTourOptions', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetPresetTourOptionsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 12, 'name': 'GetPresetTourOptions', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(tour)}}

    def GetServiceCapabilities(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        caps = ptz.GetServiceCapabilities()
        if caps is None or len(caps) == 0:
            return {'test_id': 13, 'name': 'GetServiceCapabilities', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetServiceCapabilitiesResponse message',
                               'response': ''}}
        else:
            return {'test_id': 13, 'name': 'GetServiceCapabilities', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(caps)}}

    def GetStatus(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.media.GetProfiles()[0]._token
        status = ptz.GetStatus({'ProfileToken': token})
        if status is None or len(status) == 0:
            return {'test_id': 14, 'name': 'GetStatus', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetStatusResponse message',
                               'response': ''}}
        else:
            return {'test_id': 14, 'name': 'GetStatus', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(status)}}

    def RemovePresetTour(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.media.GetProfiles()[0]._token
        token_1 = ptz.GetPresetTours({'ProfileToken': token})[-1]._token
        tour_token = ptz.CreatePresetTour({'ProfileToken': token})
        tour = ptz.GetPresetTour({'ProfileToken': token, 'PresetTourToken': tour_token})
        remove = ptz.RemovePresetTour({'ProfileToken': token, 'PresetTourToken': tour_token})
        token_2 = ptz.GetPresetTours({'ProfileToken': token})[-1]._token
        if token_1 != token_2:
            return {'test_id': 15, 'name': 'RemovePresetTour', 'service': 'PTZ',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send RemovePresetTourResponse message',
                               'response': ''}}
        else:
            return {'test_id': 15, 'name': 'RemovePresetTour', 'service': 'PTZ',
                    'result': {'supported': True, 'extension': None, 'response': str(tour)}}


cam = ONVIFCamera('192.168.15.44', 8000, 'admin', 'Supervisor')
Inst = PTZTests(cam)
# print Inst.GetCompatibleConfigurations()
# print Inst.GetConfiguration()
# print Inst.GetConfigurationOptions()
# print Inst.GetConfigurations()
print Inst.GetNodes()
# print Inst.GetNode()
# print Inst.AbsoluteMove()
# print Inst.GetPresets()
# print Inst.CreatePresetTour()
# print Inst.GetPresetTour()
# print Inst.GetPresetTours()
# print Inst.GetPresetTourOptions()
# print Inst.GetServiceCapabilities()
# print Inst.GetStatus()
# print Inst.RemovePresetTour()
