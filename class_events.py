from onvif import ONVIFCamera
import random, string
import datetime

class Events_Test:
	def __init__(self,ip,port,user,passw):
		self.ip = ip
		self.port = port
		self.user = user
		self.passw = passw
		self.cam = ONVIFCamera(self.ip, self.port, self.user, self.passw)
	def GetEventProperties(self):
		event_service = self.cam.create_events_service()
		properties = event_service.GetEventProperties()
		if (len(properties)>0):
			return 'GetEventProperties works', properties
		else:
			return 'GetEventProperties does not work', properties
	def CreatePullPointSubscription(self):
		event_service = self.cam.create_events_service()
		subs = event_service.CreatePullPointSubscription()
		curr = subs.CurrentTime
		term = subs.TerminationTime
		delt = int((term-curr).total_seconds())
		if ((len(subs) > 0) & (delt >= 10)):
			return 'CreatePullPointSubscription works', subs
		else:
			return 'CreatePullPointSubscription does not work', subs
	def GetServiceCapabilities(self):
		event_service = self.cam.create_events_service()
		capabilities = event_service.GetServiceCapabilities()
		if (len(capabilities)>0):
			return 'GetServiceCapabilities works', capabilities
		else:
			return 'GetServiceCapabilities does not work', capabilities
	def PullMessages(self):
		self.cam.create_pullpoint_service()
   		service = self.cam.pullpoint.zeep_client._get_service('EventService')
		port = self.cam.pullpoint.zeep_client._get_port(service, 'PullPointSubscription')
		port.binding_options['address'] = onvif_camera.xaddrs['http://www.onvif.org/ver10/events/wsdl/PullPointSubscription']
		plp = onvif_camera.pullpoint.zeep_client.bind('EventService', 'PullPointSubscription')
		print plp.PullMessages(Timeout=timedelta(seconds=20), MessageLimit=100)


Inst = Events_Test('192.168.15.43', 80, 'admin', 'Supervisor')
print Inst.GetEventProperties()
print Inst.CreatePullPointSubscription()
print Inst.GetServiceCapabilities()
# Inst.PullMessages()
