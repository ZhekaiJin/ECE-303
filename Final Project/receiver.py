# Written by S. Mevawala, modified by D. Gitzel
# Edited by Scott Jin

import timeit
import time
import logging
from subprocess import check_call
import channelsimulator
import utils
import sys
import socket
from utility import *


class Receiver(object):

    def __init__(self, inbound_port=50005, outbound_port=50006, timeout=10, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

    def receive(self):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoReceiver(Receiver):
    ACK_DATA = bytes(123)

    def __init__(self):
        super(BogoReceiver, self).__init__()

    def receive(self):
        self.logger.info("Receiving on port: {} and replying with ACK on port: {}".format(self.inbound_port, self.outbound_port))
        while True:
            try:
                data = self.simulator.u_receive()  # receive data
                self.logger.info("Got data from socket: {}".format(
                data.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                sys.stdout.write(data)
                self.simulator.u_send(BogoReceiver.ACK_DATA)  # send ACK
            except socket.timeout:
                sys.exit()

class MyReceiver(Receiver):

    def __init__(self):
        super(MyReceiver, self).__init__(timeout=15)
    def receive(self):
        self.logger.info("Receiving on port: {} and replying with ACK on port: {}".format(self.inbound_port, self.outbound_port))
        expected_seq_id = 0
        while True:
            msg = self.simulator.u_receive()
            self.logger.info("Raw data: {}".format(msg))
            checksum = msg[:2]
            seq = chr(msg[2])
            data = msg[3:]

            if getchecksum(data) == checksum:
                    ack_msg = bytearray("ACK", "ascii")
                    ack_msg.append(int(seq))
                    ack_checksum = getchecksum(ack_msg)
                    self.logger.info("Checksum correct, calculating ack & sending ack: {} {}".format(
                        (list(ack_checksum)), (list(ack_msg))))
                    self.simulator.u_send(ack_checksum + ack_msg)
                    if seq == str(expected_seq_id):
                        self.logger.info("Got data from socket: {}".format(
                            data))  # note that ASCII will only decode bytes in the range 0-127
                        sys.stdout.write(data) #formmally
                        expected_seq_id = 1 - expected_seq_id
            else:
                nak = 1 - expected_seq_id
                nak_msg = bytearray("ACK", "ascii")
                nak_msg.append(nak)
                nak_checksum = getchecksum(nak_msg)
                self.logger.info("checksum incorrect, calculating nak & sending nak: {} {}".format(
                    (list(nak_checksum)), (list(nak_msg))))
                self.simulator.u_send(nak_checksum + nak_msg)


if __name__ == "__main__":
    rcvr = MyReceiver()
    start = time.time()
    try:
        rcvr.receive()
    except socket.timeout:
        done = time.time()
        elapsed = done - start
        rcvr.logger.info("Timeouted, took {} s.".format(elapsed))
        sys.stderr.write("Timeouted, plz check use make diff, if any output, wait till the process end[ps -a]. ")
        sys.stderr.write("Took {} s.".format(elapsed))

