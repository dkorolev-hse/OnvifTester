from onvif import ONVIFCamera, exceptions
from time import sleep, ctime
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
        except (exceptions.ONVIFError, AttributeError):
            return 'Device does not support PTZ service'
        try:
            try:
                x = pos.PanTilt._x
                y = pos.PanTilt._y
                x_z = pos.Zoom._x
            except AttributeError:
                try:
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
                except AttributeError:
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
                return 'AbsoluteMove is supported, current coordinates: ' + str(x) + ' ' + str(y) + ' ' + str(x_z)
            elif dif1 == 0.0 and dif2 == 0.0 and dif3 != 0.0:
                return 'AbsoluteMove is partly supported, only PatTilt works. Current PanTilt coordinates: ' \
                           + str(x) + ' ' + str(y)
            elif dif1 != 0.0 and dif2 != 0.0 and dif3 == 0.0:
                return 'AbsoluteMove is partly supported, only Zoom works. Current Zoom coordinates: ' + str(x_z)
            else:
                return 'AbsoluteMove may be supported, but it cannot be checked. ' \
                       'Potential error with coordinates from GetStatus()'
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

        def left(req_move, req_stop, ptz, token):
            sleep(0.3)
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x
            req_move.Velocity.Zoom._x = 0.0
            req_move.Velocity.PanTilt._x = -0.5
            req_move.Velocity.PanTilt._y = 0.0
            ptz.ContinuousMove(req_move)
            sleep(1)
            ptz.Stop(req_stop)
            sleep(0.3)
            pos2 = self.returnpos(ptz, token).x
            # print pos1 - pos2
            return pos1 - pos2

        def right(req_move, req_stop, ptz, token):
            sleep(0.3)
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x
            req_move.Velocity.Zoom._x = 0.0
            req_move.Velocity.PanTilt._x = 0.5
            req_move.Velocity.PanTilt._y = 0.0
            ptz.ContinuousMove(req_move)
            sleep(1)
            ptz.Stop(req_stop)
            sleep(0.3)
            pos2 = self.returnpos(ptz, token).x
            # print pos1 - pos2
            return pos1 - pos2

        def zoom_in(req_move, req_stop, ptz, token):
            sleep(0.3)
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x_z
            req_move.Velocity.PanTilt._x = 0.0
            req_move.Velocity.PanTilt._y = 0.0
            req_move.Velocity.Zoom._x = 0.1
            ptz.ContinuousMove(req_move)
            sleep(1)
            ptz.Stop(req_stop)
            sleep(0.3)
            pos2 = self.returnpos(ptz, token).x_z
            return pos1 - pos2

        def zoom_out(req_move, req_stop, ptz, token):
            sleep(0.3)
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x_z
            req_move.Velocity.PanTilt._x = 0.0
            req_move.Velocity.PanTilt._y = 0.0
            req_move.Velocity.Zoom._x = -0.1
            ptz.ContinuousMove(req_move)
            sleep(1)
            ptz.Stop(req_stop)
            sleep(0.3)
            pos2 = self.returnpos(ptz, token).x_z
            return pos1 - pos2

        pos = self.returnpos(ptz, token)
        # print 'x ', pos.x, ' y ', pos   .y, ' z ', pos.x_z
        if pos is False:
            return 'PTZ service is not supported'
        elif pos.x is not False and pos.y is not False:
            if round(left(req_move, req_stop, ptz, token), 1) + round(right(req_move, req_stop, ptz, token), 1) == 0:
                if pos.x_z is False:
                    return 'ContinuousMove is partly supported, zoom does not work'
                elif round(zoom_in(req_move, req_stop, ptz, token), 1) + round(zoom_out(req_move, req_stop, ptz, token), 1) == 0:
                    return 'ContinuousMove is supported'
                elif round(zoom_out(req_move, req_stop, ptz, token), 1) + round(zoom_in(req_move, req_stop, ptz, token), 1) == 0:
                    return 'ContinuousMove is supported'
                else:
                    return 'ContinuousMove is partly supported, zoom does not work'
            elif round(right(req_move, req_stop, ptz, token), 1) + round(left(req_move, req_stop, ptz, token), 1) == 0:
                if pos.x_z is False:
                    return 'ContinuousMove is partly supported, zoom does not work'
                elif round(zoom_in(req_move, req_stop, ptz, token), 1) + round(zoom_out(req_move, req_stop, ptz, token), 1) == 0:
                    return 'ContinuousMove is supported'
                elif round(zoom_out(req_move, req_stop, ptz, token), 1) + round(zoom_in(req_move, req_stop, ptz, token), 1) == 0:
                    return 'ContinuousMove is supported'
                else:
                    return 'ContinuousMove is not supported'
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

    def relativemove(self):
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'
        token = self.cam.create_media_service().GetProfiles()[0]._token
        rel_move = ptz.create_type('RelativeMove')
        rel_move.ProfileToken = token
        req_stop = ptz.create_type('Stop')
        req_stop.ProfileToken = token

        node = ptz.GetNodes()[0]

        # zoom_min = node.SupportedPTZSpaces.RelativeZoomTranslationSpace[0].XRange.Min
        # zoom_max = node.SupportedPTZSpaces.RelativeZoomTranslationSpace[0].XRange.Max
        # pan_min = node.SupportedPTZSpaces.RelativePanTiltTranslationSpace[0].XRange.Min
        # pan_max = node.SupportedPTZSpaces.RelativePanTiltTranslationSpace[0].XRange.Max
        # tilt_min = node.SupportedPTZSpaces.RelativePanTiltTranslationSpace[0].YRange.Min
        # tilt_max = node.SupportedPTZSpaces.RelativePanTiltTranslationSpace[0].YRange.Max

        def move_x(x, token, req_stop, rel_move, ptz):
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x
            rel_move.Translation.PanTilt._x = x
            rel_move.Translation.PanTilt._y = 0
            rel_move.Translation.Zoom._x = 0
            ptz.RelativeMove(rel_move)
            sleep(1)
            ptz.Stop(req_stop)
            pos2 = self.returnpos(ptz, token).x
            # print 'Pan ' + str(pos1 - pos2)
            return pos1 - pos2

        def move_y(y, token, req_stop, rel_move, ptz):
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).y
            rel_move.Translation.PanTilt._x = 0
            rel_move.Translation.PanTilt._y = y
            rel_move.Translation.Zoom._x = 0
            ptz.RelativeMove(rel_move)
            sleep(1)
            ptz.Stop(req_stop)
            pos2 = self.returnpos(ptz, token).y
            # print 'Tilt ' + str(pos1 - pos2)
            return pos1 - pos2
       
        def move_z(z, token, req_stop, rel_move, ptz):
            ptz.Stop(req_stop)
            pos1 = self.returnpos(ptz, token).x_z
            rel_move.Translation.PanTilt._x = 0
            rel_move.Translation.PanTilt._y = 0
            rel_move.Translation.Zoom._x = z
            ptz.RelativeMove(rel_move)
            sleep(1)
            ptz.Stop(req_stop)
            pos2 = self.returnpos(ptz, token).x_z
            # print 'Zoom ' + str(pos1 - pos2)
            return pos1 - pos2 

        d = 0.05
        pos = self.returnpos(ptz, token)
        movx = movy = movz = False
        if pos is False:
            return 'PTZ service is not supported'
        if pos.x is not False:
            try:
                mov1 = round(move_x(d, token, req_stop, rel_move, ptz), 2)
                mov2 = round(move_x(-d, token, req_stop, rel_move, ptz), 2)
                if mov1 + mov2 == 0 and not mov1 == mov2 == 0:
                    movx = True
                else:
                    mov3 = round(move_x(-d, token, req_stop, rel_move, ptz), 2)
                    mov4 = round(move_x(d, token, req_stop, rel_move, ptz), 2)
                    if mov3 + mov4 == 0 and not mov3 == mov4 == 0:
                        movx = True
            except exceptions.ONVIFError:
                movx = False
        if pos.y is not False:
            try:
                mov1 = round(move_y(d, token, req_stop, rel_move, ptz), 2)
                mov2 = round(move_y(-d, token, req_stop, rel_move, ptz), 2)
                if mov1 + mov2 == 0 and not mov1 == mov2 == 0:
                    movy = True
                else:
                    mov3 = round(move_y(-d, token, req_stop, rel_move, ptz), 2)
                    mov4 = round(move_y(d, token, req_stop, rel_move, ptz), 2)
                    if mov3 + mov4 == 0 and not mov3 == mov4 == 0:
                        movy = True
            except exceptions.ONVIFError:
                movy = False
        if pos.x_z is not False:
            try:
                mov1 = round(move_z(-0.2, token, req_stop, rel_move, ptz), 2)
                mov2 = round(move_z(0.2, token, req_stop, rel_move, ptz), 2)
                # print 'mov1 ' + str(mov1) + ' mov2 ' + str(mov2)
                if mov1 + mov2 == 0 and not mov1 == mov2 == 0:
                    movz = True
                else:
                    mov3 = round(move_z(0.2, token, req_stop, rel_move, ptz), 2)
                    mov4 = round(move_z(-0.2, token, req_stop, rel_move, ptz), 2)
                    if mov3 + mov4 == 0 and not mov3 == mov4 == 0:
                        movz = True
            except exceptions.ONVIFError:
                movz = False

        if movx and movz and movy:
            return 'RelativeMove is supported'
        elif movx and movy and not movz:
            return 'RelativeMove is supported partly, only PanTilt works'
        elif movx and movz and not movy:
            return 'RelativeMove is supported partly, only PanZoom works'
        elif movy and movz and not movx:
            return 'RelativeMove is supported partly, only TiltZoom works'
        elif movz and not movx and not movy:
            return 'RelativeMove is supported partly, only Zoom works'
        elif movy and not movx and not movz:
            return 'RelativeMove is supported partly, only Tilt works'
        elif movx and not movy and not movz:
            return 'RelativeMove is supported partly, only Pan works'
        else:
            return 'RelativeMove is not supported'

    def absoluteimaging(self):
        media = self.cam.create_media_service()      # Creating media service
        imaging = self.cam.create_imaging_service()  # Creating imaging service
        vstoken = media.GetVideoSources()[0]._token  # Getting videosources token
        options = imaging.GetMoveOptions({'VideoSourceToken': vstoken})
        imaging.create_type('Move')                  # Creating new type of imaging
        try:
            options.Absolute
        except AttributeError:
            return 'Absolute imaging is not supported, AttributeError'
        imaging.SetImagingSettings({'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'MANUAL'}}})
        imaging.Stop({'VideoSourceToken': vstoken}) 
        try:
            imaging.GetStatus({'VideoSourceToken': vstoken})
        except exceptions.ONVIFError:
            return 'ONVIFError 400 while calling GetStatus(), try again later'
        x0 = round(imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position, 2)
        max_x = options.Absolute.Position.Max
        if x0 + (max_x/2) < max_x:
            x1 = x0 + max_x/2
        else:
            x1 = x0 - max_x/2
        try:
            imaging.Move({'VideoSourceToken': vstoken, 'Focus': {'Absolute': {'Position': x1, 'Speed': 0.8}}})
            sleep(2)  # waiting
            imaging.Stop({'VideoSourceToken': vstoken})  # stopping imaging
            x2 = round(imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position, 2)
            # print 'x0 ', x0, ' x1 ', x1, ' x2 ', x2
            if abs(x1-x2) == 0 and not x0 == x2 == 0:
                imaging.SetImagingSettings(
                    {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                return 'Absolute imaging is supported'
            else:
                imaging.SetImagingSettings(
                    {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                return 'Absolute imaging may be supported, but it cannot be checked. ' \
                       'Potential error with coordinates from GetStatus()'
        except AttributeError:          # Catching error
            imaging.SetImagingSettings(
                {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
            return 'Absolute Imaging is not supported, AttributeError'

    def continuousimaging(self):
        media = self.cam.create_media_service()      # Creating media service
        imaging = self.cam.create_imaging_service()  # Creating imaging service
        vstoken = media.GetVideoSources()[0]._token  # Getting videosources token
        options = imaging.GetMoveOptions({'VideoSourceToken': vstoken})
        imaging.create_type('Move')
        try:
            options.Continuous
        except AttributeError:
            return 'Continuous imaging is not supported'
        max_speed = options.Continuous.Speed.Max

        imaging.SetImagingSettings({'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'MANUAL'}}})
        imaging.Stop({'VideoSourceToken': vstoken})
        try:
            imaging.GetStatus({'VideoSourceToken': vstoken})
        except exceptions.ONVIFError:
            return 'ONVIFError 400 while calling GetStatus(), try again later'
        x0 = round(imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position, 2)
        if x0 + (max_speed/2) < max_speed:
            x1 = x0 + max_speed/2
        else:
            x1 = x0 - max_speed/2
        try:
            imaging.Move({'VideoSourceToken': vstoken, 'Focus': {'Continuous': {'Speed': x1}}})
            sleep(1)
            imaging.Stop({'VideoSourceToken': vstoken})
            x2 = round(imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position, 2)
            # print 'x0 ', x0, ' x1 ', x1, ' x2 ', x2
            if abs(x1 - x2) == 0 and not x0 == x2 == 0:
                imaging.SetImagingSettings(
                    {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                return 'Continuous imaging is supported'
            else:
                imaging.SetImagingSettings(
                    {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                return 'Continuous imaging may be supported, but it cannot be checked. ' \
                       'Potential error with coordinates from GetStatus()'
        except AttributeError:  # Catching error
            imaging.SetImagingSettings(
                {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
            return 'Continuous Imaging is not supported, AttributeError'

    def relativeimaging(self):
        media = self.cam.create_media_service()      # Creating media service
        imaging = self.cam.create_imaging_service()  # Creating imaging service
        vstoken = media.GetVideoSources()[0]._token  # Getting videosources token
        options = imaging.GetMoveOptions({'VideoSourceToken': vstoken})
        imaging.create_type('Move')
        try:
            options.Relative
        except AttributeError:
            return 'Continuous imaging is not supported'
        imaging.SetImagingSettings({'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'MANUAL'}}})
        imaging.Stop({'VideoSourceToken': vstoken})
        x0 = round(imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position, 2)
        max_x = options.Relative.Distance.Max
        if x0 + (max_x/2) < max_x:
            x1 = x0 + max_x/2
        else:
            x1 = x0 - max_x/2
        try:
            imaging.Move({'VideoSourceToken': vstoken, 'Focus': {'Relative': {'Distance': x1, 'Speed': 0.8}}})
            sleep(2)  # waiting
            imaging.Stop({'VideoSourceToken': vstoken})  # stopping imaging
            x2 = round(imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position, 2)
            # print 'x0 ', x0, ' x1 ', x1, ' x2 ', x2
            if abs(x1-x2) == 0 and not x0 == x2 == 0:
                imaging.SetImagingSettings(
                    {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                return 'Relative imaging is supported'
            else:
                imaging.SetImagingSettings(
                    {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                return 'Relative imaging may be supported, but it cannot be checked. ' \
                       'Potential error with coordinates from GetStatus()'
        except AttributeError:          # Catching error
            imaging.SetImagingSettings(
                {'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
            return 'Relative Imaging is not supported, AttributeError'


Inst = EssentialTest('192.168.15.43', 80, 'admin', 'Supervisor')
# print Inst.getusers()
# print Inst.maxminpass()
# print Inst.maxminuser()
# print Inst.maxusers()
# print Inst.absolutemove()
# print Inst.gotohomeposition()
# print Inst.continiousmove()
# print Inst.relativemove()
# print Inst.absoluteimaging()
# print Inst.continuousimaging()
print Inst.relativeimaging()
