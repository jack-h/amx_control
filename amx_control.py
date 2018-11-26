import telnetlib
import time

OK = 0
ERROR = 1

RESPONSE_DELAY_MS = 100

class AMXNMX(object):
    def __init__(self, host, port=50002, response_delay_ms=RESPONSE_DELAY_MS):
        self.conn = telnetlib.Telnet(host, port=port)
        self.response_delay_sec = response_delay_ms / 1000.
        self._initialize()

    def _initialize(self):
        pass

    def _wait_for_response(self):
        time.sleep(self.response_delay_sec)

    def _send_command(self, cmd):
        self.conn.write(cmd + '\n')
        self._wait_for_response()

    def _send_command_with_check(self, cmd, key, val):
        """
        Send a command and check that the response includes
        response_dict[key] == val
        """
        r = self._send_command_return_response(cmd)
        if r[key] == val:
            return OK
        else:
            return ERROR

    def _get_response(self):
        raw = self.conn.read_very_eager()
        lines = raw.split('\r')[0:-1] #Ignore last empty line
        r_dict = {}
        for line in lines:
            key, val = line.split(':',1)
            r_dict[key] = val
        return r_dict

    def _send_command_return_response(self, cmd):
        self._send_command(cmd)
        return self._get_response()

    def get_status(self):
        return self._send_command_return_response("getStatus")

class AMXDecoder(AMXNMX):
    def hdmi_off(self):
        self._send_command_with_check("hdmiOff", "DVIOFF", "on")

    def hdmi_on(self):
        self._send_command_with_check("hdmiOn", "DVIOFF", "off")

    def set_stream(self, stream):
        self._send_command_with_check("set:%d" % stream, "STREAM", "%d" % stream)

class AMXEncoder(AMXNMX):
    def _initialize(self):
        self.stream_id = int(self.get_status()["STREAM"])
