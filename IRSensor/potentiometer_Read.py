from __future__ import division

import spidev

def bitstring(n):

	s = bin(n)[2:]

	return '0'*(8-len(s)) + s

def setup(spi_channel = 0):
	conn = spidev.SpiDev(0, spi_channel)
	conn.max_speed_hz = 1200000 # 1.2 MHz
	conn.mode = 0
	print "mode=", conn.mode
	return conn


def read(conn, adc_channel=0, spi_channel=0):

	cmd = 192 #start bit + single ended

	if adc_channel:

		cmd += 32 #set the ODD/SIGN bit to select channel number

	reply_bytes = conn.xfer2([cmd, 0])

	reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)

	reply = reply_bitstring[5:15]

	return int(reply, 2) / 2**10

if __name__ == '__main__':
	
	conn = setup()
	while True:
		print "Voltage:",
		volt = 5*read(conn)
		print volt
