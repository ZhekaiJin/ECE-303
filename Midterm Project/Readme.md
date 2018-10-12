# RDT TRANSMITTER
### Scott Jin 
## Usage
The Program was a simple implementation of RDT(Reliable Data Transfer) 3.0 MODEL. It works by using finite state machime model combined with timeout on transmitter and receiver model in application layer to add security to transport layer UDP.

    USAGE: make test
    TEST: PlZ wait two time[unix command] result, then use make diff
    INPUT: /
	FUNCTION :reliable data transfer over a man-made noisy channel which can drop, randomize, swap order on packets.
	OUTPUT : rendered in output.txt should match the sent file [defualt to "file_1MB.txt"] .

## Screenshot
![proper testing](/Users/scott/Desktop/proper_test_image.png)
	
## Notes
make test give a simple description for prompting, but several scenarios may appear and worth noting:

1. Sender exited prompt sugguest the time that sender used to transmit all the file contents. Because the receiver wait a full timeout to quit(15 secs), the whole process performance depends on the first time result `time python2 sender.py < ./file_1MB.txt`
Note the makefile is modified from initial kickstart implementation, user should wait two unix `time` command to use make diff to see the output.txt [make diff].

2. If sender timout keeps prompting, and a timeout appeared before the loop, it means receiver exited because timeout, and the timeout window in receiver [default to 15 secs] should be modifed to a larger value to allow successful transmition.

3. default port number was used, it the port is already used in your host, plz change the API settting in the channelsimulator.py.

## Diffuculties
The sender should be able to kill the receiver to reduce the whole process time, but the receiver seems not be able to write the last messege to file before it gets killed, so I instead still use a receiver timeout to quit. Still, sender time result should be used for evaluation. 

## Implementation
1. The transmitter model was coded to mimic the action of FSM as following: 
	![](/Users/scott/Desktop/rdt3_sender_fsm.png)
2. The receiver mode FSM is depicted as following: 
	![](/Users/scott/Desktop/Jbz6a.png)
3. transmition in action:
	![](/Users/scott/Desktop/rdt30_examples.gif)
