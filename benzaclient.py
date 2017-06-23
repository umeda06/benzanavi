import wiringpi as pi
import time
import redis

name = "5WS1"
trig = 17
echo = 18
interval = 1
ttl = 60

pi.wiringPiSetupGpio()
pi.pinMode(trig, pi.OUTPUT)
pi.pinMode(echo, pi.INPUT)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

while True:
	time.sleep(interval)
	is_break = False

	# start the pulse on the trig pin
	pi.digitalWrite(trig, pi.HIGH)
	time.sleep(0.00001) # wait 10 micro seconds
	pi.digitalWrite(trig, pi.LOW)

	# listen to the echo pin
	count = 0
	while pi.digitalRead(echo) == pi.LOW:
		if count == 10000:
			is_break = True
			break
		count += 1
		t_start = time.time()
	if is_break:
		continue

	count = 0
	while pi.digitalRead(echo) == pi.HIGH:
		if count == 10000:
			is_break = True
			break
		count += 1
		t_end = time.time()
	if is_break:
		continue

	# calculate the distance
	distance = (t_end - t_start) * 17000
	print(distance, "cm")

	# set the vacant:0/occupied:1 to redis
	if distance < 20:
		r.setex(name, ttl, 0)
	else:
		r.setex(name, ttl, 1)
