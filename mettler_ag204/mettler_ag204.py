import serial
import datetime
import time
import re
import json
from cyckei.plugins import cyp_base

EOL = b'\r\n'
weight_conversion = {'g': 1, 'mg': 0.001, 'kg': 1000., 'oz': 0.0352739619,
                     'lb': 0.00220462262}

default_config = json.loads(
    """
    {
        "name": "mettler_ag204",
        "enabled": true,
        "sources": [
            {
              "port": "COM6",
              "meta": null
            }
        ]
    }
    """
)


class PluginController(cyp_base.BaseController):
    def __init__(self, sources):
        super().__init__(
            "mettler-ag204",
            "Gets weight data from Mettler-Toledo AG204 scale."
        )

        # Create a PicoChannel object for each Device
        self.sources = self.load_sources(sources)

        self.logger.info(f"Connected {len(self.sources)} Mettler Scale(s)")

        # List of names to declare to Cyckei
        self.names = []
        for source in self.sources:
            self.names.append(str(source))

    def load_sources(self, config_sources):
        """
        Searches for available sources, and establishes source objects.

        Returns
        -------
        Dictionary of sources in format "name": SourceObject.
        """
        sources = {}
        for scale in config_sources:
            scale = MettlerLogger(self.logger, PORT=scale["port"])
            sources[scale.name] = scale

        return sources


class MettlerLogger(object):
    def __init__(self,
                 logger,
                 ACCEPTABLE_STATUS=['S', 'SD'],
                 TIMEFORMAT='%Y-%m-%d %H:%M:%S.%f',
                 PORT=None,
                 BAUDRATE=9600,
                 BYTESIZE=serial.EIGHTBITS,
                 PARITY=serial.PARITY_NONE,
                 XONXOFF=True,
                 NAME=None,
                 maxi=100000000000,
                 verbosity=1,
                 DRY_WEIGHT=None,
                 DENSITY=0.963):

        self.name = f"Mettler {PORT}"
        self.logger = logger
        timestamp_start = time.time()
        date_start = datetime.datetime.fromtimestamp(timestamp_start)
        date_start_str = date_start.strftime(TIMEFORMAT)

        self.options = {
            'description': 'Logfile of data. Header is JSON, data is CSV',
            'serial': {
                'port': PORT,
                'baudrate': BAUDRATE,
                'bytesize': BYTESIZE,
                'parity': PARITY,
                'xonxoff': XONXOFF},
            'date_start': date_start_str,
            'time_format': TIMEFORMAT,
            'timestamp': timestamp_start,
            'dry_weight': DRY_WEIGHT,
            'density': DENSITY,
            'data_columns': [
                {'index': 0,
                 'name': 'time',
                 'unit': 'seconds',
                 'description': 'time elapsed in seconds since date_start'},
                {'index': 1,
                 'name': 'weight',
                 'unit': 'grams',
                 'description': 'instantaneous weight in grams'},
                {'index': 2,
                 'name': 'status',
                 'unit': ' text',
                 'description': 'State, S stable state, SI transient state'}],
            'name': NAME,
            'verbosity': verbosity,
            'balance': {
                'model': None,
                'serial': None}
            }

    def communicate(self, command):
        '''
        open a connection, send command, read output, then close.
        return result. Returns Non on failure
        '''
        self.logger.debug(
            f"Sending {command} to {self.options['serial']['port']}")
        ser = serial.Serial(port=str(self.options['serial']['port']),
                            baudrate=self.options['serial']['baudrate'],
                            bytesize=self.options['serial']['bytesize'],
                            parity=self.options['serial']['parity'],
                            xonxoff=self.options['serial']['xonxoff'],
                            timeout=5)

        command = command.encode('utf-8')
        ser.write(command + EOL)
        s = ser.readline().decode('utf-8')
        ser.close()
        self.logger.debug(
            f"Got value of {s} from {self.options['serial']['port']}")
        return s

    def get_balance_model(self):
        try:
            t = self.communicate("I2")
            return re.search(r'"(.+)"', t).groups()[0]
        except Exception:
            return None

    def get_balance_serial(self):
        try:
            t = self.communicate("I4")
            return re.search(r'"(.+)"', t).groups()[0]
        except Exception:
            return None

    def read(self, command="SI"):
        '''
        Opens a connection with balance.
        Requests weight using command.
        Parses the balance's response.
        Closes connection.
        Returns the weight in grams.

        Parameters:
            command:
                command string to send to balance, defaults to SI, the
                immediate unequilibrated weight. End line characters should
                not be included

        Returns:
            weight:
                weight in grams or None on failure
        '''

        self.logger.debug(f"Reading {self.options['serial']['port']}")
        weight = None
        weight_d = {'Status': None, 'WeightValue': None, 'Unit': None}
        try:
            # Get a weight and close the connection
            s = self.communicate(command)

            if len(s.split()) == 4 or len(s.split()) == 3:
                pars = s.split()
                weight_d = {'Status': pars[0], 'WeightValue': float(pars[-2]),
                            'Unit': pars[-1]}
                weight = weight_d['WeightValue'] \
                    * weight_conversion[weight_d['Unit']]

        except (serial.SerialException) as e:
            if self.options['verbosity'] > 0:
                self.logger.error('Could not get Mettler data: %s' % e)
                weight = 0

        self.logger.debug(
            f"Weight of {self.options['serial']['port']} is {weight_d}")
        return weight


if __name__ == "__main__":
    sources = default_config["sources"]
    controller = PluginController(sources)
    print(cyp_base.read_all(controller))
