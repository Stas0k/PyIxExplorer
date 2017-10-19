"""
TestCenter package tests that require actual Ixia chassis and active ports.

Test setup:
Two Ixia ports connected back to back.

@author yoram@ignissoft.com
"""

from os import path
import time

from ixexplorer.ixe_statistics_view import IxePortsStats, IxeStreamsStats
from ixexplorer.test.test_base import IxeTestBase


class IxeTestOnline(IxeTestBase):

    def testStats(self):
        cfg1 = path.join(path.dirname(__file__), 'configs/stats_config_1.prt')
        cfg2 = path.join(path.dirname(__file__), 'configs/stats_config_2.prt')
        self._load_config(cfg1, cfg2)

        self.ixia.session.start_transmit()

        port_stats = IxePortsStats()
        port_stats.read_stats()

        stream_stats = IxeStreamsStats()
        stream_stats.read_stats()

        print '++++'
        for port, stats in port_stats.statistics.items():
            print '{}\n\t{}'.format(port, stats)
        for stream, stats in stream_stats.statistics.items():
            print '{}\n\t{}'.format(stream, stats)
        print '++++'

        self.ixia.session.stop_transmit()

        self.ports[self.port1].start_transmit()
        port_stats.read_stats()
        stream_stats.read_stats()
        print '++++'
        for port, stats in port_stats.statistics.items():
            print '{}\n\t{}'.format(port, stats)
        for stream, stats in stream_stats.statistics.items():
            print '{}\n\t{}'.format(stream, stats)
        print '++++'
        self.ports[self.port1].stop_transmit()

    def testCapture(self):
        cfg1 = path.join(path.dirname(__file__), 'configs/cap_cpnfig.prt')
        cfg2 = path.join(path.dirname(__file__), 'configs/cap_cpnfig.prt')
        self._load_config(cfg1, cfg2)

        self.ixia.session.start_capture()
        self.ixia.session.start_transmit()
        time.sleep(4)
        self.ixia.session.stop_transmit()
        self.ixia.session.stop_capture(cap_file_name='c:/temp/ixia_cap')

    def testStreamStats(self):
        cfg1 = path.join(path.dirname(__file__), 'configs/stats_config_1.prt')
        cfg2 = path.join(path.dirname(__file__), 'configs/stats_config_2.prt')
        self._load_config(cfg1, cfg2)

        self.ixia.session.start_transmit()

        stream_stats = IxeStreamsStats()
        time.sleep(2)
        self.ixia.session.stop_transmit()
        stream_stats.read_stats()

        print '++++'
        for stream, stats in stream_stats.statistics.items():
            print '{}\n\t{}\n\t{}'.format(stream, stats['tx'], {str(p): s for p, s in stats['rx'].items()})
        print '++++'
