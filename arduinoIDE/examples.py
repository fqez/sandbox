import os
from pathlib import Path

class Examples():

	def __init__(self):
		self.lcd_examples = []			#key lcd
		self.led_examples = []			#key led
		self.buz_examples = []			#key buz
		self.pot_examples = []			#key pot
		self.light_examples = []		#key light
		self.keys_examples = []			#key keys
		self.motors_examples = []		#key motors
		self.ultra_examples = []		#key ultra
		self.ir_examples = []			#key ir
		self.behaviour_examples = []			#key beh

		self.examples = {}
		self.examples['lcd'] = self.lcd_examples 
		self.examples['led'] = self.led_examples
		self.examples['buz'] = self.buz_examples 
		self.examples['pot'] = self.pot_examples 
		self.examples['light'] = self.light_examples 
		self.examples['keys'] = self.keys_examples 
		self.examples['motors'] = self.motors_examples
		self.examples['ultra'] = self.ultra_examples
		self.examples['ir'] = self.ir_examples
		self.examples['behaviour'] = self.behaviour_examples

		self.loadExamples()


	def loadExamples(self):		
		path = 'examples'
		for root, dirs, files in os.walk(path):
			for file in files:
				if file.endswith(".py"):
					path_file = os.path.join(root,file)
					parent = os.path.relpath(root, path)
					#print (os.path.relpath(root, 'examples'), file)
					if parent in self.examples:
						self.examples[parent].append(file)
					
	def getExample(self, key):

		if key in self.examples:
			lr = []
			for e in self.examples[key]:
				e = os.path.splitext(e)[0]
				lr.append(e)
			return lr
		else:
			print("The key does not exists")




if __name__ == "__main__":

	o = Examples()
	l = o.getExample('behaviour')
	print(l)
	