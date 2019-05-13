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
        while i < 50:
            try:
                name = self.genpass(7)
                if a == 'chars':
                    self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genchar(i), 'UserLevel': 'User'}})
                elif a == 'digits':
                    self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.gendigits(i), 'UserLevel': 'User'}})
                elif a == 'chars+digits':
                    self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genpass(i), 'UserLevel': 'User'}})
                elif a == 'chars+digits+symbols':
                    self.cam.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genhardpass(i),'UserLevel': 'User'}})
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
        if users is not None:
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
            return 'No user has been created. Can not obtain username length properties Something is wrong'

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
            return 'Relative imaging is not supported'
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

    def videoencoding(self):
        media = self.cam.create_media_service()
        encoders = []
        try:
            configs = media.GetVideoEncoderConfigurations()
            for i in configs:
                encoders.append(i.Encoding)
            return list(set(encoders))
        except AttributeError:
            return 'AttributeError, something is wrong'

    def videoresolutions(self):
        media = self.cam.create_media_service()
        res = []
        try:
            configs = media.GetVideoEncoderConfigurations()
            for i in configs:
                res.append(str(i.Resolution.Width) + 'x' + str(i.Resolution.Height))
            return list(set(res))
        except AttributeError:
            return 'Attribute error, something is wrong'

    def audioencoding(self):
        media = self.cam.create_media_service()
        try:
            audio = []
            configs = media.GetAudioEncoderConfigurations()
            print configs
            for i in configs:
                audio.append(i.Encoding)
            return list(set(audio))
        except AttributeError:
            return 'Attribute error, something is wrong'

    def getbrightness(self):
        media = self.cam.create_media_service()
        imaging = self.cam.create_imaging_service()
        vstoken = media.GetVideoSources()[0]._token
        f1 = True
        f2 = True
        settings = imaging.GetImagingSettings({'VideoSourceToken': vstoken})
        options = imaging.GetOptions({'VideoSourceToken': vstoken})
        try:
            Min = options.Brightness.Min
            Max = options.Brightness.Max
        except AttributeError:
            f1 = False
        try:
            Curr = settings.Brightness
        except AttributeError:
            f2 = False
        if f1 and f2:
            return 'Min: ' + str(Min) + ' Curr: ' + str(Curr) + ' Max: ' + str(Max)
        elif f1 and not f2:
            return 'Min: ' + str(Min) + ' Curr: ' + 'NULL' + ' Max: ' + str(Max)
        elif not f1:
            return 'Brightness not supported'

    def setbrightness(self, value):
        media = self.cam.create_media_service()
        imaging = self.cam.create_imaging_service()
        vstoken = media.GetVideoSources()[0]._token
        options = imaging.GetOptions({'VideoSourceToken': vstoken})
        get0 = imaging.GetImagingSettings({'VideoSourceToken': vstoken})
        try:
            Min = options.Brightness.Min
            Max = options.Brightness.Max
            br0 = get0.Brightness
            if Min < value < Max:
                imaging.SetImagingSettings({'VideoSourceToken': vstoken, 'ImagingSettings': {'Brightness': value}})
            else:
                return 'Value given is out of range'
            get1 = imaging.GetImagingSettings({'VideoSourceToken': vstoken})
            br1 = get1.Brightness
            if br1 == value:
                imaging.SetImagingSettings({'VideoSourceToken': vstoken, 'ImagingSettings': {'Brightness': br0}})
                return 'Setbrightness works. Current value: ', br1
            else:
                return 'Setbrightness does not work'
        except AttributeError:
            return 'Setbrightness does not work, AttributeError'



    def stepbrightness(self):
        media = self.cam.create_media_service()
        imaging = self.cam.create_imaging_service()
        vstoken = media.GetVideoSources()[0]._token
        set1 = imaging.GetImagingSettings({'VideoSourceToken': vstoken})
        options = imaging.GetOptions({'VideoSourceToken': vstoken})
        # print set1
        step = 100000
        percmin = 1000000

        try:
            br0 = set1.Brightness
            br1 = br0
            perc = 0.0000001
            for h in range(6):
                n = 7
                for i in range(6):
                    k = 1
                    while k < 7:
                        br1 += perc
                        imaging.SetImagingSettings({'VideoSourceToken': vstoken, 'ImagingSettings': {'Brightness': br1}})
                        br2 = imaging.GetImagingSettings({'VideoSourceToken': vstoken}).Brightness
                        if round(br1, n) == round(br2, n):
                            # print 'br1 = ', br1, ' br2 = ', br2
                            # print 'Round Br1 = ', round(br1, n), 'Round Br2 = ', round(br2, n), 'N = ', n
                            percmin = k * (0.0000001 * pow(10, i))
                            # print 'K = ', k, ' I= ', i, 'N = ', n, 'Percmin = ', percmin
                            break
                        perc += 0.0000001 * pow(10, i)
                        #
                        k += 1
                    n -= 1
                    if percmin < step:
                        step = percmin
        except AttributeError:
            return 'AttributeError, try again'
        if step == 100000:
            return 'Step was not calculated, try again'
        else:
            return 'Step is ' + '{:.0e}'.format(float(step))






    def imagingsettings(self):
        media = self.cam.create_media_service()      # Creating media service
        imaging = self.cam.create_imaging_service()  # Creating imaging service
        vstoken = media.GetVideoSources()[0]._token  # Getting videosources token
        settings = imaging.GetImagingSettings({'VideoSourceToken': vstoken})
        # print settings
        options = imaging.GetOptions({'VideoSourceToken': vstoken})
        print options
        try:
            Backlight = ''
            Backlight.Min = options.BacklightCompensation.Level.Min
            Backlight.Max = options.BacklightCompenSharpnessevel.Max
            Backlight.Curr = settings.Backlight
        except AttributeError:
            pass
        try:
            ColorSaturation = ''
            ColorSaturation.Min = options.ColorSaturation.Min
            ColorSaturation.Max = options.ColorSaturation.Max
            ColorSaturation.Curr = settings.ColorSaturation
        except AttributeError:
            pass
        try:
            Contrast = ''
            Contrast.Min = options.Contrast.Min
            Contrast.Max = options.Contrast.Max
            Contrast.Curr = settings.Contrast
        except AttributeError:
            pass
        try:
            Sharpness = ''
            Sharpness.Min = options.Sharpness.Min
            Sharpness.Max = options.Sharpness.Max
            Sharpness.Curr = settings.Sharpness
        except AttributeError:
            pass
        try:
            WhiteBalance, WhiteBalance.YrGain, WhiteBalance.YbGain = '', '', ''
            WhiteBalance.YrGain.Min = options.WhiteBalance.YrGain.Min
            WhiteBalance.YrGain.Max = options.WhiteBalance.YrGain.Max
            WhiteBalance.YbGain.Min = options.WhiteBalance.YbGain.Min
            WhiteBalance.YbGain.Max = options.WhiteBalance.YbGain.Max
            WhiteBalance.YrGain.Curr = settings.WhiteBalance.YrGain
            WhiteBalance.YbGain.Curr = settings.WhiteBalance.YbGain
        except AttributeError:
            pass
        try:
            WideDynamicRange = ''
            WideDynamicRange.Mode = options.WideDynamicRange.Mode
        except AttributeError:
            pass






        try:
            features = ''
            for feature in settings:
                features += str(feature[0]) + '\n'
            return str(features[:-1])
        except AttributeError:
            return 'Attribute error, something is wrong'

    def currentposition(self):
        media = self.cam.create_media_service()
        token = media.GetProfiles()[0]._token
        vstoken = media.GetVideoSources()[0]._token  # Getting videosources token
        focus = ''
        try:
            imaging = self.cam.create_imaging_service()  # Creating imaging service
        except exceptions.ONVIFError:
            return 'Imaging service is not supported'
        try:
            focus = str(round(imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position, 2))
        except (AttributeError, exceptions.ONVIFError):
            focus = 'None'
        try:
            ptz = self.cam.create_ptz_service()
        except exceptions.ONVIFError:
            return 'PTZ service is not supported'

        try:
            pos = ptz.GetStatus({"ProfileToken": token}).Position
        except AttributeError:
            return 'AttributeError, something is wrong'
        try:
            pos.z = str(round(pos.Zoom._x, 2))
        except AttributeError:
            pos.z = 'None'
        try:
            pos.x, pos.y = str(round(pos.PanTilt._x, 2)), str(round(pos.PanTilt._y, 2))
        except AttributeError:
            pos.x, pos.y = 'None', 'None'
        return 'x: ' + pos.x + ' y: ' + pos.y + ' z: ' + pos.z + ' focus: ' + focus

    def relays(self):
        relays = self.cam.devicemgmt.GetRelayOutputs()
        if relays:
            token = relays[0]._token
            mode0 = relays[0].Properties.Mode
            if mode0 == 'Bistable':
                mode1 = 'Monostable'
            else:
                mode1 = 'Bistable'
            state = relays[0].Properties.IdleState
            if state == 'closed':
                state1 = ''
            self.cam.devicemgmt.SetRelayOutputSettings({'RelayOutput': {'token': token, 'Properties': {
                'Mode': mode1
            }}})
        return relays

    def dynamicdns(self):
        dns = self.cam.devicemgmt.GetDynamicDNS()
        if dns:
            return 'works', dns
        else:
            return 'dynamicdns is not supported'


Inst = EssentialTest('192.168.11.24', 80, 'admin', 'Supervisor')
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
# print Inst.relativeimaging()
# print Inst.videoencoding()
# print Inst.videoresolutions()
# print Inst.audioencoding()
# print Inst.imagingsettings()
# print Inst.getbrightness()
# print Inst.setbrightness(52)
print Inst.stepbrightness()
# print Inst.currentposition()
# print Inst.relays()
# print Inst.dynamicdns()
