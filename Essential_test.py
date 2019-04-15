from onvif import ONVIFCamera, exceptions
from time import sleep
import string
from random import choice


class EssentialTest:
    def __init__(self, ip, port, user, passw):
        self.ip = ip
        self.port = port
        self.user = user
        self.passw = passw
        self.cam = ONVIFCamera(self.ip, self.port, self.user, self.passw)
        self.event_service = self.cam.create_events_service()
        self.media = self.cam.create_media_service()

    def genpass(self, length=8, chars=string.ascii_letters + string.digits):
        return ''.join([choice(chars) for k in range(length)])

    def genchar(self, length=8, chars=string.ascii_letters):
        return ''.join([choice(chars) for k in range(length)])

    def gendigits(self, length=8, chars=string.digits):
        return ''.join([choice(chars) for k in range(length)])

    def genhardpass(self, length=8, chars=string.ascii_letters + string.digits + string.punctuation):
        return ''.join([choice(chars) for k in range(length)])

    def test(self, a):
        i = 4
        k = 1000
        z = 0
        create = ''
        while i < 50:
            try:
                name = self.genpass(7)
                if a == 'chars':
                    create = self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genchar(i), 'UserLevel': 'User'}})
                elif a == 'digits':
                    create = self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.gendigits(i), 'UserLevel': 'User'}})
                elif a == 'chars+digits':
                    create = self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genpass(i), 'UserLevel': 'User'}})
                elif a == 'chars+digits+symbols':
                    create = self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genhardpass(i),'UserLevel': 'User'}})
                # sleep(1)
                if self.cam.devicemgmt.GetUsers()[-1].Username == name:
                    if i < k:
                        k = i
                    if i > z:
                        z = i
                    self.cam.devicemgmt.DeleteUsers({'Username': name})
                    i += 1
                else:
                    break
            except exceptions.ONVIFError:
                # print create
                i += 1
        if k != 1000 and z != 0:
            return 'The range for password length is from ' + str(k) + ' to ' + str(z) + ' for ' + a
        else:
            return 'No user has been created. Password with ' + str(a) + ' does not work'

    def maxminpass(self):
        result = []
        for m in ['chars', 'digits', 'chars+digits', 'chars+digits+symbols']:
            result.append(self.test(m))
        return result
    
    def getusers(self):
        users = self.cam.devicemgmt.GetUsers()
        if users is None:
            return str(users)
        else:
            return 'Function does not work, sorry'

    def maxminuser(self):
        i = 1
        k = 100
        z = 0
        while i < 32:
            try:
                name = self.genpass(i)
                self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genpass(9), 'UserLevel': 'User'}})
                if self.cam.devicemgmt.GetUsers()[-1].Username == name:
                    if i < k:
                        k = i
                    if i > z:
                        z = i
                # print self.cam.devicemgmt.GetUsers()[-1].Username, name
                self.cam.devicemgmt.DeleteUsers({'Username': name})
                i += 1
            except exceptions.ONVIFError:
                i += 1
        if k != 1000 and z != 0:
            return 'The range for username length is from ' + str(k) + ' to ' + str(z)
        else:
            return 'No user has been created. Something is wrong'

    def maxusers(self):
        k = []
        n, z, i, max1 = 1, 1, 1, 0
        for item in self.cam.devicemgmt.GetUsers():
            max1 += 1
        while i <= 100:
            k += [self.genpass(8)]
            i += 1
        while n < i-1:
            try:
                self.cam.devicemgmt.CreateUsers({'User': {'Username': k[n], 'Password': self.genpass(), 'UserLevel': 'User'}})
                if self.cam.devicemgmt.GetUsers()[-1].Username == k[n]:
                    n += 1
                    max1 += 1
                else:
                    break
            except exceptions.ONVIFError:
                break
        if n == i:
            return 'No user has been created. Something is wrong'
        # print self.cam.devicemgmt.GetUsers()
        while z < n:
            self.cam.devicemgmt.DeleteUsers({'Username': k[z]})
            z += 1
        if n != 1:
            return 'Camera supports ' + str(max1) + ' max users'
        else:
            return 'No user has been created. Something is wrong'

    def absolutemove(self):
        token = self.media.GetProfiles()[0]._token
        try:
            ptz = self.cam.create_ptz_service()
            ptz.create_type("AbsoluteMove")
            pos = ptz.GetStatus({"ProfileToken": token}).Position
        except exceptions.ONVIFError, AttributeError:
            return 'Device does not support PTZ service'
        try:
            try:
                x = pos.PanTilt._x
                y = pos.PanTilt._y
                x_z = pos.Zoom._x
            except AttributeError:
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
            # x_z, x, y = pos.Zoom._x, pos.PanTilt._x, pos.PanTilt._y
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
            ptz.AbsoluteMove({"ProfileToken": token, "Position": {"PanTilt": {"_x": x1, "_y": y1}, "Zoom": {"_x": x_z1}}})
            sleep(3)
            pos = ptz.GetStatus({"ProfileToken": token}).Position
            x_z = pos.Zoom._x
            x = pos.PanTilt._x
            y = pos.PanTilt._y
            dif1 = (round((x1-x), 3))
            dif2 = (round((y1-y), 3))
            dif3 = (round((x_z1-x_z), 3))
            x_z, x, y = round(x_z, 2), round(x, 2), round(y, 2)
            if dif1 == 0.0 and dif2 == 0.0 and dif3 == 0.0:
                result = 'AbsoluteMove is supported, current coordinates: ' + str(x) + ' ' + str(y) + ' ' + str(x_z)
                return str(result)
            elif dif1 == 0.0 and dif2 == 0.0 and dif3 != 0.0:
                result = 'AbsoluteMove is supported, but Zoom does not work. Current coordinates: ' \
                           + str(x) + ' ' + str(y) + ' ' + str(x_z)
                return str(result)
            else:
                return 'AbsoluteMove may be supported, but camera does not move'
        except AttributeError:
            return 'AbsoluteMove is not supported, AttributeError '

    def gotohomeposition(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        try:
            if ptz.GetNodes()[0].HomeSupported:
                return 'GoToHomePosition supported'
        except AttributeError:
            return 'GoToHomePosition is not supported'

    def returnpos(self, ptz, token):

        try:
            pos = ptz.GetStatus({"ProfileToken": token}).Position
        except AttributeError:
            return False
        try:
            pos.x_z = pos.Zoom._x
        except AttributeError:
            pos.x_z = False
        try:
            pos.x = pos.PanTilt._x
            pos.y = pos.PanTilt._y
        except AttributeError:
            pos.x = False
            pos.y = False
        return pos
    
    def continiousmove(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.cam.create_media_service().GetProfiles()[0]._token

        req_move = ptz.create_type('ContinuousMove')
        req_move.ProfileToken = token

        req_stop = ptz.create_type('Stop')
        req_stop.ProfileToken = token

        req_goto_home = ptz.create_type('GotoHomePosition')
        req_goto_home.ProfileToken = token

        def left(req_move, req_stop, ptz, token):
            pos1 = self.returnpos(ptz, token).x
            req_move.Velocity.Zoom._x = 0.0
            req_move.Velocity.PanTilt._x = -0.5
            req_move.Velocity.PanTilt._y = 0.0
            ptz.ContinuousMove(req_move)
            sleep(1)
            ptz.Stop(req_stop)
            pos2 = self.returnpos(ptz, token).x
            # print pos1 - pos2
            return pos1 - pos2

        def right(req_move, req_stop, ptz, token):
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x
            req_move.Velocity.Zoom._x = 0.0
            req_move.Velocity.PanTilt._x = 0.5
            req_move.Velocity.PanTilt._y = 0.0
            ptz.ContinuousMove(req_move)
            sleep(1)
            ptz.Stop(req_stop)
            pos2 = self.returnpos(ptz, token).x
            # print pos1 - pos2
            return pos1 - pos2

        def zoom_in(req_move, req_stop, ptz, token):
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x_z
            req_move.Velocity.PanTilt._x = 0.0
            req_move.Velocity.PanTilt._y = 0.0
            req_move.Velocity.Zoom._x = 0.5
            ptz.ContinuousMove(req_move)
            sleep(1)
            ptz.Stop(req_stop)
            pos2 = self.returnpos(ptz, token).x_z
            return pos1 - pos2

        def zoom_out(req_move, req_stop, ptz, token):
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x_z
            req_move.Velocity.PanTilt._x = 0.0
            req_move.Velocity.PanTilt._y = 0.0
            req_move.Velocity.Zoom._x = -0.5
            ptz.ContinuousMove(req_move)
            sleep(1)
            ptz.Stop(req_stop)
            pos2 = self.returnpos(ptz, token).x_z
            return pos1 - pos2

        pos = self.returnpos(ptz, token)
        if pos is False:
            return 'PTZ service is not supported'
        elif pos.x and pos.y:
            if round(left(req_move, req_stop, ptz, token), 1) + round(right(req_move, req_stop, ptz, token), 1) == 0:
                if pos.x_z is False:
                    return 'ContinuousMove is partly supported, zoom does not work'
                else:
                    return 'ContinuousMove is supported'
            elif round(right(req_move, req_stop, ptz, token), 1) + round(left(req_move, req_stop, ptz, token), 1) == 0:
                if pos.x_z is False:
                    return 'ContinuousMove is partly supported, zoom does not work'
                else:
                    return 'ContinuousMove is supported'
            else:
                return 'ContinuousMove is not supported. Camera does not move'
        elif pos.x is False and pos.y is False and pos.x_z >= 0:
            if round(zoom_in(req_move, req_stop, ptz, token), 1) + round(zoom_out(req_move, req_stop, ptz, token), 1) == 0:
                return 'ContinuousMove is partly supported, only zoom works'
            elif round(zoom_out(req_move, req_stop, ptz, token), 1) + round(zoom_in(req_move, req_stop, ptz, token), 1) == 0:
                return 'ContinuousMove is partly supported, only zoom works'
            else:
                return 'ContinuousMove is not supported'
        else:
            return 'ContinuousMove is not supported'


Inst = EssentialTest('192.168.15.47', 80, 'admin', 'Supervisor')
# print Inst.getusers()
# print Inst.maxminpass()
# print Inst.maxminuser()
# print Inst.maxusers()
# print Inst.absolutemove()
# print Inst.gotohomeposition()
print Inst.continiousmove()
