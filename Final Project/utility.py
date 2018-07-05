# Written by Scott Jin

import channelsimulator
import sys
BufferSize = channelsimulator.ChannelSimulator.BUFFER_SIZE - 3

def getchecksum(data):
    if not isinstance(data, bytearray):
        print ("data is not in bytearray format")
        exit(-1)
    #print("calculate checksum for data:"), (data)
    result = sum(data)
    return bytearray([(result // 256)%256,result % 256])

def bprint(data):
    if not isinstance(data, bytearray):
        sys.stderr.write("data is not in bytearray format")
        exit(-1)
    print(list(data))

def slice_window(data_bytes):
    frames = list()
    num_bytes = len(data_bytes)
    extra = 1 if num_bytes % BufferSize else 0

    for i in xrange(num_bytes / BufferSize + extra):
        # split data into 1024 byte frames
        frames.append(
            data_bytes[
            i * BufferSize:
            i * BufferSize + BufferSize
            ]
        )
    return frames

# def bytetoint(byte):




   # convert it to string mode first
    # if isinstance(data, bytearray):
    #     data = data.decode("ascii")
    # print("calcualte check sum for :  " + data)
    # pos = len(data)
    # if (pos & 1):  # If odd...
    #     pos -= 1
    #     sum = ord(data[pos])  # Prime the sum with the odd end byte
    # else:
    #     sum = 0
    # while pos > 0:
    #     pos -= 2
    #     sum += (ord(data[pos + 1]) << 8) + ord(data[pos])
    #
    # sum = (sum >> 16) + (sum & 0xffff)
    # sum += (sum >> 16)
    # result = (~ sum) & 0xffff  # Keep lower 16 bits
    # result = result >> 8 | ((result & 0xff) << 8)  # Swap bytes
