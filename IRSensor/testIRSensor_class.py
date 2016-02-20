import IRSensor as irs
try:
	irsensor1 = irs.IRSensor(0)
	irsensor2 = irs.IRSensor(1)
	while(1):
		5*irsensor1.updateRange()
		5*irsensor2.updateRange()
		print "Channel 0: %s \nChannel 1: %s" % (irsensor1.getRange(), irsensor2.getRange())
except KeyboardInterrupt:
	print "Exiting..."
