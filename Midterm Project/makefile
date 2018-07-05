ALL: 
	@gcc -o PortScanner PortScanner.c

.PHONY:debug,clean
debug:
	@gcc -o Portdebug  PortScanner.c -g
clean:
	rm -f *.dSYM
	rm Portdebug
	rm PortScanner
