import threading
import time
import urllib
import urllib2
import json

LOGIN = 'base1'
PASS = 'base1'
SERVER_URL = 'http://127.0.0.1:8000/base/'
GET_TASKS_URL = SERVER_URL + 'get_tasks/'
TIMER_SEC_INTERVAL = 10 # 5 minutes

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
	#def __init__(self, gb_id):
	#	self.gb_id = gb_id
	def __init__(self, gb_id, task_time, gb_x, gb_y, proportions,task_id):
		self.gb_id = gb_id
		self.time = task_time
		self.gb_x = gb_x,
		self.gb_y = gb_y,
		self.proportions = proportions
		self.id = task_id

	#def __del__(self):
	#	pass
		#print 'delete task {1}'.format(self.id)

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
		return True

class Base:
	def __init__(self, login, password):
		self.task_id = 0
		self.login = login
		self.password = password
		self.tasks = []

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
			task = Task(gb_id, task_time, gb_x, gb_y, proportions, self.task_id)
			self.tasks.append(task)
			self.task_id = self.task_id + 1

	def sort_tasks(self):
		print 'sort_tasks'
		for t in self.tasks:
			print t.id, t.gb_id, t.time, t.proportions
		pass

	def do_tasks(self):
		pass

# starts from here
base = Base(LOGIN, PASS)
timer = TimerThread(10)
timer.start()

while True:
	if(timer.timer_flag):
		base.get_tasks_json(GET_TASKS_URL)
		timer.timer_flag = False
		base.extract_tasks()
		base.sort_tasks()
	base.do_tasks()
		

		