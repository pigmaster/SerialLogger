__author__ = 'phil'

from threading import Thread
from time import sleep
import serial
from serial.tools import list_ports
import os

def logger():
    boot_counter = 0
    while(True):
        line = ser.readline()
        #print line
        if "Welcome to QNX Neutrino 6.3.2 on the JCI SH7761 Platform:PRIMARY OS" in line:
            print "Booted up" + str(boot_counter)
            boot_counter+=1
        if "Generic: Info Process 81933 (mqueue) terminated SIGTERM code=0 by process 249871 value=0." in line:
            print line
        logfile.write(line)

def printer():
    while(True):
        ser.write("resetboard\n")
        sleep(10)


def serial_ports():
    """
    Returns a generator for all available serial ports
    """
    if os.name == 'nt':
        # windows
        for i in range(256):
            try:
                s = serial.Serial(i)
                s.close()
                yield 'COM' + str(i + 1)
            except serial.SerialException:
                pass
    else:
        # unix
        for port in list_ports.comports():
            if "USB" in port[0]:
                yield port[0]



if __name__ == "__main__":

    # Initializing Serial Ports

    print(list(serial_ports()))
    com_port = 'COM4'
    list_com_ports = list(serial_ports())


    #while (any(com_port in s for s in list_com_ports)):
    #    com_port = str(raw_input("What COM Port to connect to: "))
    try:
            ser = serial.Serial(port = com_port, baudrate = 115200,timeout = 1) #port = "/dev/ttyS30"
    except IOError as e:
        print "I/O Error - Could not connect to COM Port".format(e.errno, e.strerror)




    # Creating Child Threads
    loop_counter = 0
    #while(True):
    logfile = open("SCI_LOG_" + str(loop_counter) +".txt",'w')
    thread1 = Thread(target = logger)
    thread2 = Thread(target = printer)
    thread1.start()
    thread2.start()
    #    sleep(30)
    #    thread2.close()
    #    logfile.close()
    #    loop_couter+=1
