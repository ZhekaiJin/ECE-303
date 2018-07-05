# Written by S. Mevawala, modified by D. Gitzel
# Edited by Scott Jin

import time
import logging
import socket
from subprocess import check_call
import channelsimulator
import utils
from utility import *
import sys

class Sender(object):

    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=10, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoSender(Sender):

    def __init__(self):
        super(BogoSender, self).__init__()

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        while True:
            try:
                self.simulator.u_send(data)  # send data
                ack = self.simulator.u_receive()  # receive ACK
                self.logger.info("Got ACK from socket: {}".format(
                    ack.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                break
            except socket.timeout:
                pass


class MySender(Sender):
    def __init__(self):
        super(MySender, self).__init__()

    def send(self, data):
        start = time.time()
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        frame_list = slice_window(data)
        self.logger.info("Length of packets: {} number of frames to send: {}".format(len(data),(len(frame_list))))
        seq_id = 0
        count = 0
        for frame in frame_list:
            count += 1
            self.logger.info("sending frame num: {}".format(count))
            ack_received = False
            while not ack_received:
                prefix = bytearray(getchecksum(frame) + str(seq_id))
                self.simulator.u_send(prefix + frame)
                try:
                    msg = self.simulator.u_receive()
                except socket.timeout:
                    self.logger.info(" Timeouted. ")
                    sys.stderr.write(" Sender Timeouted. if this messege loops, receiver timeout need to be longer.")
                else:
                    checksum = msg[:2] #2 bytes checksum acquired
                    self.logger.info("checksum get: {} messege look like {} , seq_id: {}".format(list(checksum),list(msg),msg[5]))
                    seq_ack = msg[5]
                    if getchecksum(msg[2:])==checksum and seq_ack == seq_id:
                        ack_received = True;
            seq_id = 1 - seq_id #alternating between 0 & 1
        sys.stderr.write(" File sent, sender exited. Plz wait the receiver timeout to make diff.")
        done = time.time()
        elapsed = done - start
        self.logger.info(" Sent, took {} s. ".format(elapsed))
        sys.stderr.write(" Sent, took {} s. ".format(elapsed))
        sys.exit(0)

if __name__ == "__main__":
    # test out mySender
    DATA = bytearray(sys.stdin.read())
    sndr = MySender()
    sndr.send(DATA)
    #check_call(["pkill", "-9", "-f", 'receiver.py'])
