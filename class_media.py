from onvif import ONVIFCamera, exceptions


# import random, string


class Media_Test:
    def __init__(self, ip, port, user, passw):
        self.ip = ip
        self.port = port
        self.user = user
        self.passw = passw
        self.cam = ONVIFCamera(self.ip, self.port, self.user, self.passw)

    def CreateProfile(self):  # 1
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        token1 = media.GetProfiles()[-1]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token2 = media.GetProfiles()[-1]._token
        if (token1 != token2):
            delete = media.DeleteProfile({'ProfileToken': token2})
            return 'CreateProfile works', create
        else:
            return 'DeleteProfile does not work', create

    def GetProfiles(self):  # 2
        media = self.cam.create_media_service()
        profiles = media.GetProfiles()
        if (len(profiles) > 0):
            return 'GetProfiles works', profiles
        else:
            return 'GetProfiles does not work', profiles

    def DeleteProfile(self):  # 3
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        token1 = media.GetProfiles()[-1]._token
        media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token2 = media.GetProfiles()[-1]._token
        if (token1 != token2):
            delete = media.DeleteProfile({'ProfileToken': token2})
            return 'DeleteProfile works', delete
        else:
            return 'DeleteProfile does not work', []

    def GetSnapshotUri(self):  # 4
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        uri = media.GetSnapshotUri({'ProfileToken': token})
        if (len(uri) > 0):
            return 'GetSnapshotUri works', uri
        else:
            return 'GetSnapshotUri does not work', uri

    def AddAudioDecoderConfiguration(self):  # 5
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token = media.GetProfiles()[-1]._token
        try:
            audio_token = media.GetProfiles()[0].AudioDecoderConfiguration._token
        except AttributeError:
            media.DeleteProfile({'ProfileToken': token})
            return 'AddAudioDecoderConfiguration does not work, AttributeError', []
        add_config = media.AddAudioDecoderConfiguration({'ProfileToken': token, 'ConfigurationToken': audio_token})
        audio_token2 = media.GetProfiles()[-1].AudioDecoderConfiguration._token
        media.DeleteProfile({'ProfileToken': token})
        if audio_token == audio_token2:
            return 'AddAudioDecoderConfiguration works', add_config
        else:
            return 'AddAudioDecoderConfiguration does not work', add_config

    def AddAudioEncoderConfiguration(self):  # 6
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token = media.GetProfiles()[-1]._token
        try:
            audio_token = media.GetProfiles()[0].AudioEncoderConfiguration._token
        except AttributeError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddAudioEncoderConfiguration does not work, AttributeError', []
        add_config = media.AddAudioEncoderConfiguration({'ProfileToken': token, 'ConfigurationToken': audio_token})
        audio_token2 = media.GetProfiles()[-1].AudioEncoderConfiguration._token
        delete = media.DeleteProfile({'ProfileToken': token})
        if (audio_token == audio_token2):
            return 'AddAudioEncoderConfiguration works', add_config
        else:
            return 'AddAudioEncoderConfiguration does not work', add_config

    def AddAudioOutputConfiguration(self):  # 7
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token = media.GetProfiles()[-1]._token
        try:
            audio_token = media.GetProfiles()[0].AudioOutputConfiguration._token
        except AttributeError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddAudioOutputConfiguration does not work, AttributeError', []
        add_config = media.AddAudioOutputConfiguration({'ProfileToken': token, 'ConfigurationToken': audio_token})
        audio_token2 = media.GetProfiles()[-1].AudioOutputConfiguration._token
        delete = media.DeleteProfile({'ProfileToken': token})
        if (audio_token == audio_token2):
            return 'AddAudioOutputConfiguration works', add_config
        else:
            return 'AddAudioOutputConfiguration does not work', add_config

    def AddAudioSourceConfiguration(self):  # 8
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token = media.GetProfiles()[-1]._token
        try:
            audio_token = media.GetProfiles()[0].AudioSourceConfiguration._token
        except AttributeError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddAudioSourceConfiguration does not work, AttributeError', []
        add_config = media.AddAudioSourceConfiguration({'ProfileToken': token, 'ConfigurationToken': audio_token})
        audio_token2 = media.GetProfiles()[-1].AudioSourceConfiguration._token
        delete = media.DeleteProfile({'ProfileToken': token})
        if (audio_token == audio_token2):
            return 'AddAudioSourceConfiguration works', add_config
        else:
            return 'AddAudioSourceConfiguration does not work', add_config

    def AddMetadataConfiguration(self):  # 9
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token = media.GetProfiles()[-1]._token
        try:
            metadata_token = media.GetMetadataConfigurations()[0]._token
        except AttributeError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddMetadataConfiguration does not work, AttributeError', []
        add_config = media.AddMetadataConfiguration({'ProfileToken': token, 'ConfigurationToken': metadata_token})
        metadata_token2 = media.GetProfiles()[-1].MetadataConfiguration._token
        delete = media.DeleteProfile({'ProfileToken': token})
        if (metadata_token == metadata_token2):
            return 'AddMetadataConfiguration works', add_config
        else:
            return 'AddMetadataConfiguration does not work', add_config

    def AddPTZConfiguration(self):  # 10
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token = media.GetProfiles()[-1]._token
        try:
            ptz_token = media.GetProfiles()[0].PTZConfiguration._token
        except AttributeError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddPTZConfiguration does not work, AttributeError', []
        add_config = media.AddPTZConfiguration({'ProfileToken': token, 'ConfigurationToken': ptz_token})
        ptz_token2 = media.GetProfiles()[-1].PTZConfiguration._token
        delete = media.DeleteProfile({'ProfileToken': token})
        if (ptz_token == ptz_token2):
            return 'AddPTZConfiguration works', add_config
        else:
            return 'AddPTZConfiguration does not work', add_config

    def AddVideoAnalyticsConfiguration(self):  # 11
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token = media.GetProfiles()[-1]._token
        try:
            vid_token = media.GetProfiles()[0].VideoAnalyticsConfiguration._token
            add_config = media.AddVideoAnalyticsConfiguration({'ProfileToken': token, 'ConfigurationToken': vid_token})
            vid_token2 = media.GetProfiles()[-1].VideoAnalyticsConfiguration._token
        except AttributeError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddVideoAnalyticsConfiguration does not work, AttributeError', []
        except exceptions.ONVIFError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddVideoAnalyticsConfiguration does not work, ONVIFError: new settings conflicts with other uses of configuration', []
        delete = media.DeleteProfile({'ProfileToken': token})
        if (vid_token == vid_token2):
            return 'AddVideoAnalyticsConfiguration works', add_config
        else:
            return 'AddVideoAnalyticsConfiguration does not work', add_config

    def AddVideoEncoderConfiguration(self):  # 12
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
        token = media.GetProfiles()[-1]._token
        try:
            vid_token = media.GetProfiles()[0].VideoEncoderConfiguration._token
            add_config = media.AddVideoEncoderConfiguration({'ProfileToken': token, 'ConfigurationToken': vid_token})
            vid_token2 = media.GetProfiles()[-1].VideoEncoderConfiguration._token
        except AttributeError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddVideoEncoderConfiguration does not work, AttributeError', []
        except exceptions.ONVIFError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddVideoEncoderConfiguration does not work, ONVIFError: new settings conflicts with other uses of configuration', []
        delete = media.DeleteProfile({'ProfileToken': token})
        if (vid_token == vid_token2):
            return 'AddVideoEncoderConfiguration works', add_config
        else:
            return 'AddVideoEncoderConfiguration does not work', add_config

    def AddVideoSourceConfiguration(self):  # 13
        media = self.cam.create_media_service()
        token0 = media.GetProfiles()[0]._token
        create = media.CreateProfile({'Name': 'Test', 'ProfileToken': token0})
        token = media.GetProfiles()[-1]._token
        try:
            source_token = media.GetProfiles()[0].VideoSourceConfiguration._token  # 'vscname_7'
        except AttributeError:
            delete = media.DeleteProfile({'ProfileToken': token})
            return 'AddVideoSourceConfiguration does not work, AttributeError', []
        addvid = media.AddVideoSourceConfiguration({'ProfileToken': token, 'ConfigurationToken': source_token})
        source_token2 = media.GetProfiles()[-1].VideoSourceConfiguration._token
        delete = media.DeleteProfile({'ProfileToken': token})
        if (source_token == source_token2):
            return 'AddVideoSourceConfiguration works', addvid
        else:
            return 'AddVideoSourceConfiguration does not work', addvid

    def GetVideoSourceConfiguration(self):  # 14
        media = self.cam.create_media_service()
        try:
            config_token = media.GetProfiles()[0].VideoSourceConfiguration._token
            config = media.GetVideoSourceConfiguration({'ConfigurationToken': config_token})
        except AttributeError:
            return 'GetVideoSourceConfiguration does not work, AttributeError', []
        except IndexError:
            return 'GetVideoSourceConfiguration may be working, but there is no VideoSourceConfigurations availible', []
        return 'GetVideoSourceConfiguration works', config

    def GetAudioOutputConfigurations(self):  # 15
        media = self.cam.create_media_service()
        try:
            configs = media.GetAudioOutputConfigurations()
            token = configs[0]._token
        except AttributeError:
            return 'GetAudioOutputConfigurations does not work, AttributeError', configs
        except IndexError:
            return 'GetAudioOutputConfigurations may be working, but there is no AudioOutputConfigurations availible', configs
        return 'GetAudioOutputConfigurations works', configs

    def GetAudioDecoderConfigurations(self):  # 16
        media = self.cam.create_media_service()
        try:
            configs = media.GetAudioDecoderConfigurations()
            token = configs[0]._token
        except AttributeError:
            return 'GetAudioDecoderConfigurations does not work, AttributeError', configs
        except IndexError:
            return 'GetAudioDecoderConfigurations may be working, but there is no AudioDecoderConfigurations availible', configs
        return 'GetAudioDecoderConfigurations works', configs

    def GetAudioDecoderConfigurationOptions(self):  # 17
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        try:
            config_token = media.GetAudioDecoderConfigurations()[0]._token
            options = media.GetAudioDecoderConfigurationOptions(
                {'ConfigurationToken': config_token, 'ProfileToken': token})
        except AttributeError:
            return 'GetAudioDecoderConfigurationOptions does not work, AttributeError', []
        except IndexError:
            return 'GetAudioDecoderConfigurationOptions may be working, but there is no AudioDecoderConfigurations availible', []
        return 'GetAudioDecoderConfigurationOptions', options

    def GetAudioDecoderConfiguration(self):  # 18
        media = self.cam.create_media_service()
        try:
            config_token = media.GetAudioDecoderConfigurations()[0]._token
            config = media.GetAudioDecoderConfiguration({'ConfigurationToken': config_token})
        except AttributeError:
            return 'GetAudioDecoderConfiguration does not work, AttributeError', []
        except IndexError:
            return 'GetAudioDecoderConfiguration may be working, but there is no AudioDecoderConfigurations availible', []
        return 'GetAudioDecoderConfiguration', config

    def GetAudioEncoderConfigurations(self):  # 19
        media = self.cam.create_media_service()
        try:
            configs = media.GetAudioEncoderConfigurations()
            token = configs[0]._token
        except AttributeError:
            return 'GetAudioEncoderConfigurations does not work, AttributeError', configs
        except IndexError:
            return 'GetAudioEncoderConfigurations may be working, but there is no AudioEncoderConfigurations availible', configs
        return 'GetAudioEncoderConfigurations works', configs

    def GetAudioEncoderConfigurationOptions(self):  # 20
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        try:
            config_token = media.GetAudioEncoderConfigurations()[0]._token
            options = media.GetAudioEncoderConfigurationOptions(
                {'ConfigurationToken': config_token, 'ProfileToken': token})
        except AttributeError:
            return 'GetAudioEncoderConfigurationOptions does not work, AttributeError', []
        except IndexError:
            return 'GetAudioEncoderConfigurationOptions may be working, but there is no AudioEncoderConfigurations availible', []
        return 'GetAudioEncoderConfigurationOptions', options

    def GetAudioEncoderConfiguration(self):  # 21
        media = self.cam.create_media_service()
        try:
            config_token = media.GetAudioEncoderConfigurations()[0]._token
            config = media.GetAudioEncoderConfiguration({'ConfigurationToken': config_token})
        except AttributeError:
            return 'GetAudioEncoderConfiguration does not work, AttributeError', []
        except IndexError:
            return 'GetAudioEncoderConfiguration may be working, but there is no AudioEncoderConfigurations availible', []
        return 'GetAudioEncoderConfiguration', config

    def GetAudioOutputConfigurations(self):  # 22
        media = self.cam.create_media_service()
        try:
            configs = media.GetAudioOutputConfigurations()
            token = configs[0]._token
        except AttributeError:
            return 'GetAudioOutputConfigurations does not work, AttributeError', configs
        except IndexError:
            return 'GetAudioOutputConfigurations may be working, but there is no AudioOutputConfigurations availible', configs
        return 'GetAudioOutputConfigurations works', configs

    def GetAudioOutputConfigurationOptions(self):  # 23
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        try:
            config_token = media.GetAudioOutputConfigurations()[0]._token
            options = media.GetAudioOutputConfigurationOptions(
                {'ConfigurationToken': config_token, 'ProfileToken': token})
        except AttributeError:
            return 'GetAudioOutputConfigurationOptions does not work, AttributeError', []
        except IndexError:
            return 'GetAudioOutputConfigurationOptions may be working, but there is no AudioOutputConfigurations availible', []
        return 'GetAudioOutputConfigurationOptions', options

    def GetAudioOutputConfiguration(self):  # 24
        media = self.cam.create_media_service()
        try:
            config_token = media.GetAudioOutputConfigurations()[0]._token
            config = media.GetAudioOutputConfiguration({'ConfigurationToken': config_token})
        except AttributeError:
            return 'GetAudioOutputConfiguration does not work, AttributeError', []
        except IndexError:
            return 'GetAudioOutputConfiguration may be working, but there is no AudioOutputConfigurations availible', []
        return 'GetAudioOutputConfiguration', config

    def GetAudioOutputs(self):  # 25
        media = self.cam.create_media_service()
        try:
            outputs = media.GetAudioOutputs()
            token = outputs[0]._token
        except AttributeError:
            return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did send GetNetworkInterfacesResponse message. The DUT scope list does not have one or more mandatory scope entry.',
                               'response': str(outputs)}}
        except IndexError:
            return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did send GetNetworkInterfacesResponse message, The DUT scope list does not have one or more mandatory scope entry.',
                               'response': str(outputs)}}
        if outputs is None or len(outputs) == 0:
            return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetNetworkInterfacesResponse message',
                               'response': ''}}
        else:
            return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(outputs)}}

    def GetAudioSourceConfiguration(self):  # 26
        media = self.cam.create_media_service()
        try:
            audio_token = media.GetProfiles()[0].AudioSourceConfiguration._token
        except AttributeError:
            return {'test_id': 26, 'name': 'GetAudioSourceConfiguration', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT scope list does not have one or more mandatory scope entry.',
                               'response': ''}}
        configs = media.GetAudioSourceConfiguration({'ConfigurationToken': audio_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 26, 'name': 'GetAudioSourceConfiguration', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetNetworkInterfacesResponse message',
                               'response': str(configs)}}
        else:
            return {'test_id': 26, 'name': 'GetAudioSourceConfiguration', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetAudioSourceConfigurationOptions(self):  # 27
        media = self.cam.create_media_service()
        try:
            audio_token = media.GetProfiles()[0].AudioSourceConfiguration._token
        except AttributeError:
            return {'test_id': 27, 'name': 'GetAudioSourceConfigurationOptions', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT scope list does not have one or more mandatory scope entry.',
                               'response': ''}}
        configs = media.GetAudioSourceConfigurationOptions({'ConfigurationToken': audio_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 27, 'name': 'GetAudioSourceConfigurationOptions', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetNetworkInterfacesResponse message',
                               'response': str(configs)}}
        else:
            return {'test_id': 27, 'name': 'GetAudioSourceConfigurationOptions', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetAudioSourceConfigurations(self):  # 28
        media = self.cam.create_media_service()
        configs = media.GetAudioSourceConfigurations()
        if configs is None or len(configs) == 0:
            return {'test_id': 28, 'name': 'GetAudioSourceConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetNetworkInterfacesResponse message',
                               'response': str(configs)}}
        else:
            return {'test_id': 28, 'name': 'GetAudioSourceConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetAudioSources(self):  # 25
        media = self.cam.create_media_service()
        try:
            sources = media.GetAudioSources()
            token = sources[0]._token
        except AttributeError:
            return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did send GetAudioSourcesResponse message. The DUT scope list does not have one or more mandatory scope entry.',
                               'response': str(sources)}}
        except IndexError:
            return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did send GetAudioSourcesResponse message, The DUT scope list does not have one or more mandatory scope entry.',
                               'response': str(sources)}}
        if sources is None or len(sources) == 0:
            return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetAudioSourcesResponse message',
                               'response': ''}}
        else:
            return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}

    def GetCompatibleAudioDecoderConfigurations(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        sources = media.GetCompatibleAudioDecoderConfigurations({'ProfileToken': token})
        if sources is None or len(sources) == 0:
            return {'test_id': 30, 'name': 'GetCompatibleAudioDecoderConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetCompatibleAudioDecoderConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 30, 'name': 'GetCompatibleAudioDecoderConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}

    def GetCompatibleAudioOutputConfigurations(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        sources = media.GetCompatibleAudioOutputConfigurations({'ProfileToken': token})
        if sources is None or len(sources) == 0:
            return {'test_id': 31, 'name': 'GetCompatibleAudioOutputConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetCompatibleAudioOutputConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 31, 'name': 'GetCompatibleAudioOutputConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}

    def GetCompatibleAudioSourceConfigurations(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        sources = media.GetCompatibleAudioSourceConfigurations({'ProfileToken': token})
        if sources is None or len(sources) == 0:
            return {'test_id': 32, 'name': 'GetCompatibleAudioSourceConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetCompatibleAudioSourceConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 32, 'name': 'GetCompatibleAudioSourceConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}
    
    def GetCompatibleMetadataConfigurations(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        sources = media.GetCompatibleMetadataConfigurations({'ProfileToken': token})
        if sources is None or len(sources) == 0:
            return {'test_id': 33, 'name': 'GetCompatibleMetadataConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetCompatibleMetadataConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 33, 'name': 'GetCompatibleMetadataConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}
    
    def GetCompatibleVideoAnalyticsConfigurations(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        sources = media.GetCompatibleVideoAnalyticsConfigurations({'ProfileToken': token})
        if sources is None or len(sources) == 0:
            return {'test_id': 34, 'name': 'GetCompatibleVideoAnalyticsConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetCompatibleVideoAnalyticsConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 34, 'name': 'GetCompatibleVideoAnalyticsConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}
    
    def GetCompatibleVideoEncoderConfigurations(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        sources = media.GetCompatibleVideoEncoderConfigurations({'ProfileToken': token})
        if sources is None or len(sources) == 0:
            return {'test_id': 35, 'name': 'GetCompatibleVideoEncoderConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetCompatibleVideoEncoderConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 35, 'name': 'GetCompatibleVideoEncoderConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}
    
    def GetCompatibleVideoSourceConfigurations(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        sources = media.GetCompatibleVideoSourceConfigurations({'ProfileToken': token})
        if sources is None or len(sources) == 0:
            return {'test_id': 36, 'name': 'GetCompatibleVideoSourceConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetCompatibleVideoSourceConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 36, 'name': 'GetCompatibleVideoSourceConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}

    def GetGuaranteedNumberOfVideoEncoderInstances(self):
        media = self.cam.create_media_service()
        try:
            config_token = media.GetProfiles()[0].VideoSourceConfiguration._token  # 'vscname_7'
        except AttributeError:
            return {'test_id': 37, 'name': 'GetGuaranteedNumberOfVideoEncoderInstances', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did send GetGuaranteedNumberOfVideoEncoderInstancesResponse message. The DUT scope list does not have one or more mandatory scope entry.',
                               'response': ''}}
        configs = media.GetGuaranteedNumberOfVideoEncoderInstances({'ConfigurationToken': config_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 37, 'name': 'GetGuaranteedNumberOfVideoEncoderInstances', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetGuaranteedNumberOfVideoEncoderInstancesResponse message',
                               'response': ''}}
        else:
            return {'test_id': 37, 'name': 'GetGuaranteedNumberOfVideoEncoderInstances', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetMetadataConfiguration(self):
        media = self.cam.create_media_service()
        try:
            metadata_token = media.GetMetadataConfigurations()[0]._token
        except AttributeError:
            return {'test_id': 38, 'name': 'GetMetadataConfiguration', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did send GetMetadataConfiguration message. The DUT scope list does not have one or more mandatory scope entry.',
                               'response': ''}}
        configs = media.GetMetadataConfiguration({'ConfigurationToken': metadata_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 38, 'name': 'GetMetadataConfiguration', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetMetadataConfigurationResponse message',
                               'response': ''}}
        else:
            return {'test_id': 38, 'name': 'GetMetadataConfiguration', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetMetadataConfigurationOptions(self):
        media = self.cam.create_media_service()
        try:
            metadata_token = media.GetMetadataConfigurations()[0]._token
        except AttributeError:
            return {'test_id': 39, 'name': 'GetMetadataConfigurationOptions', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did send GetMetadataConfiguration message. The DUT scope list does not have one or more mandatory scope entry.',
                               'response': ''}}
        configs = media.GetMetadataConfigurationOptions({'ConfigurationToken': metadata_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 39, 'name': 'GetMetadataConfigurationOptions', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetMetadataConfigurationOptionsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 39, 'name': 'GetMetadataConfigurationOptions', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}

    def GetMetadataConfigurations(self):
        media = self.cam.create_media_service()
        configs = media.GetMetadataConfigurations()
        if configs is None or len(configs) == 0:
            return {'test_id': 40, 'name': 'GetMetadataConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetMetadataConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 40, 'name': 'GetMetadataConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetOSDs(self):
        media = self.cam.create_media_service()
        source_token = media.GetProfiles()[0].VideoSourceConfiguration._token
        osds = media.GetOSDs({'ConfigurationToken': source_token})
        if osds is None or len(osds) == 0:
            return {'test_id': 41, 'name': 'GetOSDs', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetOSDsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 41, 'name': 'GetOSDs', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(osds)}}
    
    def GetOSD(self):
        media = self.cam.create_media_service()
        source_token = media.GetProfiles()[0].VideoSourceConfiguration._token
        osd_token = media.GetOSDs({'ConfigurationToken': source_token})[0]._token
        osd = media.GetOSD({'OSDToken': osd_token})
        if osd is None or len(osd) == 0:
            return {'test_id': 42, 'name': 'GetOSD', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetOSDResponse message',
                               'response': ''}}
        else:
            return {'test_id': 42, 'name': 'GetOSD', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(osd)}}
    
    def GetOSDOptions(self):
        media = self.cam.create_media_service()
        source_token = media.GetProfiles()[0].VideoSourceConfiguration._token
        options = media.GetOSDOptions({'ConfigurationToken': source_token})
        if options is None or len(options) == 0:
            return {'test_id': 43, 'name': 'GetOSDOptions', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetOSDOptionsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 43, 'name': 'GetOSDOptions', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(options)}}
    
    def GetProfile(self):
    	media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        profile = media.GetProfile({'ProfileToken': token})
        if profile is None or len(profile) == 0:
            return {'test_id': 44, 'name': 'GetProfile', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetProfileResponse message',
                               'response': ''}}
        else:
            return {'test_id': 44, 'name': 'GetProfile', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(profile)}}
    
    def GetServiceCapabilities(self):
        media = self.cam.create_media_service()
        capabilities = media.GetServiceCapabilities()
        if capabilities is None or len(capabilities) == 0:
            return {'test_id': 45, 'name': 'GetServiceCapabilities', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetServiceCapabilitiesResponse message',
                               'response': ''}}
        else:
            return {'test_id': 45, 'name': 'GetServiceCapabilities', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(capabilities)}}

    def GetStreamUri(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        uri =  media.GetStreamUri({'StreamSetup': {'Stream': 'RTP_unicast', 'Transport' : {'Protocol': 'UDP'}} , 'ProfileToken': token})
        print uri
        if uri is None or len(uri) == 0:
            return {'test_id': 46, 'name': 'GetStreamUri', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetStreamUriResponse message',
                               'response': ''}}
        else:
            return {'test_id': 46, 'name': 'GetStreamUri', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(uri)}}
    
    def GetVideoAnalyticsConfiguration(self):
        media = self.cam.create_media_service()
        vid_token = media.GetProfiles()[0].VideoAnalyticsConfiguration._token
        configs = media.GetVideoAnalyticsConfiguration({'ConfigurationToken': vid_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 47, 'name': 'GetVideoAnalyticsConfiguration', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoAnalyticsConfigurationResponse message',
                               'response': ''}}
        else:
            return {'test_id': 47, 'name': 'GetVideoAnalyticsConfiguration', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetVideoAnalyticsConfigurations(self):
        media = self.cam.create_media_service()
        configs = media.GetVideoAnalyticsConfigurations()
        if configs is None or len(configs) == 0:
            return {'test_id': 48, 'name': 'GetVideoAnalyticsConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoAnalyticsConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 48, 'name': 'GetVideoAnalyticsConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetVideoEncoderConfiguration(self):
        media = self.cam.create_media_service()
        enc_token = media.GetProfiles()[0].VideoEncoderConfiguration._token
        configs = media.GetVideoEncoderConfiguration({'ConfigurationToken': enc_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 49, 'name': 'GetVideoEncoderConfiguration', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoEncoderConfigurationResponse message',
                               'response': ''}}
        else:
            return {'test_id': 49, 'name': 'GetVideoEncoderConfiguration', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetVideoEncoderConfigurationOptions(self):
        media = self.cam.create_media_service()
        enc_token = media.GetProfiles()[0].VideoEncoderConfiguration._token
        configs = media.GetVideoEncoderConfigurationOptions({'ConfigurationToken': enc_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 50, 'name': 'GetVideoEncoderConfigurationOptions', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoEncoderConfigurationOptionsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 50, 'name': 'GetVideoEncoderConfigurationOptions', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetVideoEncoderConfigurations(self):
        media = self.cam.create_media_service()
        configs = media.GetVideoEncoderConfigurations()
        if configs is None or len(configs) == 0:
            return {'test_id': 51, 'name': 'GetVideoEncoderConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoEncoderConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 51, 'name': 'GetVideoEncoderConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetVideoSourceConfiguration(self):
        media = self.cam.create_media_service()
        source_token = media.GetProfiles()[0].VideoSourceConfiguration._token
        configs = media.GetVideoSourceConfiguration({'ConfigurationToken': source_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 52, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoSourceConfigurationResponse message',
                               'response': ''}}
        else:
            return {'test_id': 52, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetVideoSourceConfigurationOptions(self):
        media = self.cam.create_media_service()
        source_token = media.GetProfiles()[0].VideoSourceConfiguration._token
        configs = media.GetVideoSourceConfigurationOptions({'ConfigurationToken': source_token})
        if configs is None or len(configs) == 0:
            return {'test_id': 53, 'name': 'GetVideoSourceConfigurationOptions', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoSourceConfigurationOptionsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 53, 'name': 'GetVideoSourceConfigurationOptions', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetVideoSourceConfigurations(self):
        media = self.cam.create_media_service()
        configs = media.GetVideoSourceConfigurations()
        if configs is None or len(configs) == 0:
            return {'test_id': 54, 'name': 'GetVideoSourceConfigurations', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoSourceConfigurationsResponse message',
                               'response': ''}}
        else:
            return {'test_id': 54, 'name': 'GetVideoSourceConfigurations', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(configs)}}
    
    def GetVideoSourceModes(self):
        media = self.cam.create_media_service()
        source_token =  media.GetVideoSources()[0]._token
        print source_token
        sources = media.GetVideoSourceModes({'VideoSourceToken': source_token})
        if sources is None or len(sources) == 0:
            return {'test_id': 55, 'name': 'GetVideoSourceModes', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoSourceModesResponse message',
                               'response': ''}}
        else:
            return {'test_id': 55, 'name': 'GetVideoSourceModes', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}
    
    def GetVideoSources(self):
    	media = self.cam.create_media_service()
        sources = media.GetVideoSources()
        if sources is None or len(sources) == 0:
            return {'test_id': 56, 'name': 'GetVideoSources', 'service': 'Media',
                    'result': {'supported': False,
                               'extension': 'The DUT did not send GetVideoSourcesResponse message',
                               'response': ''}}
        else:
            return {'test_id': 56, 'name': 'GetVideoSources', 'service': 'Media',
                    'result': {'supported': True, 'extension': None, 'response': str(sources)}}



Inst = Media_Test('192.168.15.47', 80, 'admin', 'Supervisor')
# print Inst.CreateProfile()
# print Inst.GetProfiles()
# print Inst.GetSnapshotUri()
# print Inst.DeleteProfile()
# print Inst.AddAudioDecoderConfiguration()
# print Inst.AddVideoSourceConfiguration()
# print Inst.GetVideoSourceConfiguration()
# print Inst.GetAudioDecoderConfigurations()
# print Inst.GetAudioOutputConfigurations()
# print Inst.AddAudioEncoderConfiguration()
# print Inst.AddAudioOutputConfiguration()
# print Inst.AddAudioSourceConfiguration()
# print Inst.AddMetadataConfiguration()
# print Inst.AddPTZConfiguration()
# print Inst.AddVideoAnalyticsConfiguration()
# print Inst.AddVideoEncoderConfiguration()
# print Inst.GetAudioDecoderConfigurationOptions()
# print Inst.GetAudioDecoderConfiguration()
# print Inst.GetAudioEncoderConfigurations()
# print Inst.GetAudioEncoderConfigurationOptions()
# print Inst.GetAudioEncoderConfiguration()
# print Inst.GetAudioOutputConfigurations()
# print Inst.GetAudioOutputConfigurationOptions()
# print Inst.GetAudioOutputConfiguration()
# print Inst.GetAudioOutputs()
# print Inst.GetAudioSourceConfiguration()
# print Inst.GetAudioSourceConfigurationOptions()
# print Inst.GetAudioSourceConfigurations()
# print Inst.GetAudioSources()
# print Inst.GetCompatibleAudioDecoderConfigurations()
# print Inst.GetCompatibleAudioOutputConfigurations()
# print Inst.GetCompatibleAudioSourceConfigurations()
# print Inst.GetCompatibleMetadataConfigurations()
# print Inst.GetCompatibleVideoAnalyticsConfigurations()
# print Inst.GetCompatibleVideoEncoderConfigurations()
# print Inst.GetCompatibleVideoSourceConfigurations()
# print Inst.GetGuaranteedNumberOfVideoEncoderInstances()
# print Inst.GetMetadataConfiguration()
# print Inst.GetMetadataConfigurationOptions()
# print Inst.GetMetadataConfigurations()
# print Inst.GetOSDs()
# print Inst.GetOSD()
# print Inst.GetOSDOptions()
# print Inst.GetProfile()
# print Inst.GetServiceCapabilities()
# print Inst.GetStreamUri()
# print Inst.GetVideoAnalyticsConfiguration()
# print Inst.GetVideoAnalyticsConfigurations()
# print Inst.GetVideoEncoderConfiguration()
# print Inst.GetVideoEncoderConfigurationOptions()
# print Inst.GetVideoEncoderConfigurations()
# print Inst.GetVideoSourceConfiguration()
# print Inst.GetVideoSourceConfigurationOptions()
# print Inst.GetVideoSourceConfigurations()
# print Inst.GetVideoSourceModes()
# print Inst.GetVideoSources()