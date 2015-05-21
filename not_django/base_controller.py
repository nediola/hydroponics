import RPi.GPIO as GPIO
import threading
import time
import urllib
import urllib2
import json

LOGIN = 'base1'
PASS = 'base1'
SERVER_URL = 'http://192.168.10.45:5000/base/'
GET_TASKS_URL = SERVER_URL + 'get_tasks/'
TIMER_SEC_INTERVAL = 10 # 5 minutes
PIN_SENSOR = 4


#---------Settings--------------------#
GPIO.setmode(GPIO.BCM)

#---------Sensor functions------------#
def bin2dec(string_num):
	return str(int(string_num, 2))

def get_temperature_and_humidity():
	data = []
	
	GPIO.setup(PIN_SENSOR,GPIO.OUT)
	GPIO.output(PIN_SENSOR,GPIO.HIGH)
	time.sleep(0.025)
	GPIO.output(PIN_SENSOR,GPIO.LOW)
	time.sleep(0.02)
        
	GPIO.setup(PIN_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	 
	for i in range(0,500):
		data.append(GPIO.input(PIN_SENSOR))
	bit_count = 0
	tmp = 0
	count = 0
	HumidityBit = ""
	TemperatureBit = ""
	crc = ""

	try:
		while data[count] == 1:
			tmp = 1
			count = count + 1
		for i in range(0, 32):
			bit_count = 0
			while data[count] == 0:
				tmp = 1
				count = count + 1
			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1
			if bit_count > 3:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "1"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "1"
			else:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "0"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "0"										
	except:
		#print "SENSOR_ERR_RANGE"
		return {}

	try:
		for i in range(0, 8):
			bit_count = 0
			while data[count] == 0:
				tmp = 1
				count = count + 1
								  
			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1
									   
			if bit_count > 3:
				crc = crc + "1"
			else:
				crc = crc + "0"
	except:
		#print "SENSOR_ERR_RANGE"
		return {}
						 
	Humidity = bin2dec(HumidityBit)
	Temperature = bin2dec(TemperatureBit)
	data_from_sensor = {}					  
	if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
		data_from_sensor['humidity'] = Humidity
		print "Humidity:"+ Humidity +"%"
		data_from_sensor['temperature'] = Temperature
		print "Temperature:"+ Temperature +"C"
	#else:
		#print "SENSOR_ERR_CRC"
	return data_from_sensor

class TimerThread(threading.Thread):
	def __init__(self,interval):
		threading.Thread.__init__(self)
		self.daemon = True
		self.interval = interval
		self.timer_flag = False
	
	def run(self):
		while True:
			self.timer_flag = True
			print("The time is %s" % time.ctime())
			time.sleep(self.interval)

class Task:
	def __init__(self, gb_id=0, task_time=0, gb_x=0, gb_y=0, proportions={}, 
		rbt_id = 0, rbt_tank_v = 0, rbt_ip='', multiply=False, ord_tasks=[]):
		self.gb_id = gb_id
		self.time = task_time
		self.gb_x = gb_x
		self.gb_y = gb_y
		self.rbt_id = rbt_id
		self.rbt_tank_v = rbt_tank_v
		self.rbt_ip = rbt_ip
		self.proportions = proportions
		self.multiply = multiply
		self.ordinary_tasks = ord_tasks

	def equals(self, task):
		if self.gb_id != task.gb_id:
			return False
		if self.time != task.time:
			return False
		if self.gb_x != task.gb_x:
			return False
		if self.gb_y != task.gb_y:
			return False
		if self.proportions != task.proportions:
			return False
		if self.rbt_id != task.rbt_id:
			return False
		if self.rbt_tank_v != task.rbt_tank_v:
			return False
		if self.rbt_ip != task.rbt_ip:
			return False
		return True
#-------------------------DEBUG_FUNCTIONS____________________#	
def print_fields(task):
	print_dict = {}
	print_dict['gardenbed_id'] = task.gb_id
	print_dict['time'] = task.time
	print_dict['gb_x'] = task.gb_x
	print_dict['gb_y'] = task.gb_y
	print_dict['proportions'] = task.proportions
	print_dict['rbt_id'] = task.rbt_id
	print_dict['rbt_tank_v'] = task.rbt_tank_v
	print_dict['rbt_ip'] = task.rbt_ip
	print print_dict
	if task.multiply:
		print_fields_ord(task.ordinary_tasks)
	return

def print_fields_ord(tasks):
	print 'Multiply({0}):'.format(len(tasks))
	for task in tasks:
		print_dict = {}
		print_dict['gardenbed_id'] = task.gb_id
		print_dict['time'] = task.time
		print_dict['gb_x'] = task.gb_x
		print_dict['gb_y'] = task.gb_y
		print_dict['proportions'] = task.proportions
		print_dict['rbt_id'] = task.rbt_id
		print_dict['rbt_tank_v'] = task.rbt_tank_v
		print_dict['rbt_ip'] = task.rbt_ip
		print '     ', print_dict
	return
#-------------------------END_DEBUG_FUNCTIONS-------------------#


class Base:
	def __init__(self, login, password):
		self.login = login
		self.password = password
		self.tasks = []
		self.sorted_tasks = {}
		for i in xrange(0,24):
			self.sorted_tasks[i] = []

	def has_task(self, task):
		for t in self.tasks:
			if t.equals(task):
				return True
		return False
	
	def get_tasks_json(self, url):
		print 'get_tasks'
		values = {'client' : 'base', 'login' : self.login, 'password' : self.password}
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		str_json = response.read()
		self.decoded_json = json.loads(str_json)
		#print self.decoded_json
		#self.robot_tank_volume = decoded_json['robot_volume']
		return self.decoded_json
	
	def make_request(self, url, values):
		print 'make_request({0}):{1}'.format(url, values)
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		str_json = response.read()
		self.decoded_json = json.loads(str_json)
		#print self.decoded_json
		#self.robot_tank_volume = decoded_json['robot_volume']
		return self.decoded_json

	def extract_tasks(self):
		print 'extract_tasks'
		gardenbed_ids = self.decoded_json['gardenbed_ids']
		if not gardenbed_ids:
			return
		old_tasks = []
		for t in self.tasks:
			if t.gb_id not in gardenbed_ids:
				old_tasks.append(t)
		self.tasks = old_tasks
		for task_dict in self.decoded_json['tasks']:
			decoded_task_dict = json.loads(task_dict)
			#print decoded_task_dict
			gb_id = decoded_task_dict['gardenbed_id']
			task_time = decoded_task_dict['time']
			gb_x = decoded_task_dict['gardenbed_posx']
			gb_y = decoded_task_dict['gardenbed_posy']
			proportions = decoded_task_dict['proportions']
			rbt_id = decoded_task_dict['robot_id']
			rbt_tank_v = decoded_task_dict['robot_tank_volume']
			rbt_ip = decoded_task_dict['robot_ip']
			task = Task(gb_id, task_time, gb_x, gb_y, proportions, rbt_id, rbt_tank_v, rbt_ip, False, [])
			#print 't:', task.gb_id, task.gb_x, task.gb_y
			self.tasks.append(task)
		return

	def sort_tasks(self):
		self.sorted_tasks = {}
		for i in xrange(0,24):
			self.sorted_tasks[i] = []
		# add tasks to shell
		for task in self.tasks:
			self.sorted_tasks[int(task.time)].append(task) #ordinary tasks
		print 'SORTED_TASKS:'
		for key, values in self.sorted_tasks.iteritems():
			if (values):
				print 'Time:{0}'.format(key)
				for v in values:
					print_fields(v) #nediola
		#sort tasks in shell
		for key_hour in self.sorted_tasks.keys():
			hour_tasks = self.sorted_tasks[key_hour]
			self.sorted_tasks[key_hour] = self.group_tasks(hour_tasks) #now can be multiply tasks

		print 'GROUPED_TASKS:'
		for key, values in self.sorted_tasks.iteritems():
			if (values):
				print 'Time:{0}'.format(key)
				for v in values:
					print_fields(v) #nediola
		return

	def group_tasks(self, tasks):
		grouped_tasks = []
		for i in xrange(len(tasks)): # ordinary tasks
			task = tasks[i]
			tank_ids = task.proportions.keys()
			found = False
			for j in xrange(len(grouped_tasks)): #can be multiply tasks
				g_task = grouped_tasks[j] 
				if ((g_task.proportions.keys() == tank_ids) 
				and (g_task.rbt_id == task.rbt_id)
				and (g_task.rbt_tank_v == task.rbt_tank_v)
				and (g_task.rbt_ip == task.rbt_ip)):
					new_task = self.try_group(g_task, task)
					if new_task:
						#print 'add new task:'
						#print_fields(new_task)
						grouped_tasks[j] = new_task
					else:
						#print 'add to back (cant group):'
						grouped_tasks.append(task)
					found = True
					break;
			if not found:
				#print 'add to back (not found):'
				grouped_tasks.append(task)
		return grouped_tasks

	def try_group(self, gtask1, task2):
		total_amount = 0
		new_proportions = {}
		for key in gtask1.proportions.keys():
			new_proportion = gtask1.proportions[key] + task2.proportions[key]
			new_proportions[key] = new_proportion
			total_amount = total_amount + new_proportion;
		if total_amount > gtask1.rbt_tank_v:
			return None
		else:
			if gtask1.multiply:
				ord_tasks = gtask1.ordinary_tasks
				ord_tasks.append(task2)
				new_task = Task(0, gtask1.time, 0, 0, new_proportions, gtask1.rbt_id, gtask1.rbt_tank_v, gtask1.rbt_ip, True, ord_tasks)
			else:
				ord_tasks = []
				ord_tasks.append(gtask1)
				ord_tasks.append(task2)
				new_task = Task(gtask1.gb_id, gtask1.time, gtask1.gb_x, gtask1.gb_y, new_proportions, gtask1.rbt_id, gtask1.rbt_tank_v, gtask1.rbt_ip, True, ord_tasks)
			return new_task
	
	def do_tasks(self):
		pass

# starts from here
base = Base(LOGIN, PASS)
timer = TimerThread(10)
timer.start()

while True:
	if(timer.timer_flag):
		values = {'client' : 'base', 'login' : base.login, 'password' : base.password}
		sensor_data = {}
		for i in xrange(100):
			sensor_data = get_temperature_and_humidity()
			if(sensor_data):
				break
		print 'SENSOR_DATA:', sensor_data
		if (sensor_data):
			values['temperature'] = sensor_data['temperature']
			values['humidity'] = sensor_data['humidity']
			values['sensor_time'] = time.ctime()
		base.make_request(GET_TASKS_URL, values)
		timer.timer_flag = False
		base.extract_tasks()
		base.sort_tasks()
	base.do_tasks()
		

		
