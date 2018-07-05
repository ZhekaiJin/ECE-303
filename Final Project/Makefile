INPUT ?= ./file_1MB.txt
OUTPUT ?= ./output.txt


test:
	time python2 receiver.py > $(OUTPUT) & time python2 sender.py < $(INPUT) &
diff:
	diff $(INPUT) $(OUTPUT)
kill:
	kill -9 -f sender.py \
    kill -9 Python \
	pkill -9 -f Python \
    pkill python2
clean:
	rm *.log $(OUTPUT) *.pyc
