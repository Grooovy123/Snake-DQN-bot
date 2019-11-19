import time
import random
from tqdm import tqdm
import os
from PIL import Image
import cv2
import numpy as np
from collections import deque

class Snake():	

	def __init__(self, size, colour):
		self.colour = colour
		self.size = size
		self.x = random.randint(size/3, (size/3)*2)
		self.y = random.randint(size/3, (size/3)*2)	
		self.body = [[self.y, self.x]]			
		self.temp_x = self.body[0][1]
		self.temp_y = self.body[0][0]
		self.temp_pos = self.body[0]

	def action(self, choice):
		if choice == 0: #UP
			self.move(x=0, y=-1)
		elif choice == 1: #LEFT
			self.move(x=-1, y=0)
		elif choice == 2: #RIGHT
			self.move(x=1, y=0)
		elif choice == 3: #DOWN
			self.move(x=0, y=1)
		self.pre_action = choice

	def move(self, x=False, y=False):
		self.temp_pos = (self.body[0][0],self.body[0][1])
		print(self.temp_pos)
		# If no value for x, move randomly
		if not x:
			# for i in range(len(self.body)):				
			# 	self.body[i][1] += np.random.randint(-1, 2)
			pass			
		else:							
			self.body[0][1] += x			
			
			for i in range(len(self.body)-1):				
				self.body[i+1][1] = self.temp_pos[1]
				self.temp_pos = self.body[i+1]
	
        # If no value for y, move randomly
		if not y:
			# for i in range(len(self.body)):				
			# 	self.body[i][0] += np.random.randint(-1, 2)
			pass			
		else:								
			self.body[0][0] += y
			for i in range(len(self.body)-1):
				self.body[i+1][0] = self.temp_pos[0]
				self.temp_pos = self.body[i+1]

		if self.body[0][1] < 0:							
			self.body[0][1] = 0
		elif self.body[0][1] > self.size-1:			
			self.body[0][1] = self.size-1

		if self.body[0][0] < 0:			
			self.body[0][0] = 0
		elif self.body[0][0] > self.size-1:			
			self.body[0][0] = self.size-1

	def add_tail(self, SCORE):
		print(f"SCORE = {SCORE}")
		print(f"length of body is {len(self.body)}")
		if SCORE == len(self.body):
			#print(self.body[SCORE])			
			self.body.append([self.temp_pos[0], self.temp_pos[1]])
			print(f"y:{self.temp_y}")
			print(f"x:{self.temp_x}")
			return self.body			

class Food():

	def __init__(self, size, colour):
		self.size = size
		self.colour = colour
		self.x = random.randint(1, size-1)
		self.y = random.randint(1, size-1)	
		self.food_list=[self.x, self.y]
		print(f"Food location: {self.food_list}")		

class Environment():
	SIZE = 12
	RETURN_IMAGES = True    
	EAT_YOURSELF_PENALTY = 300
	FOOD_REWARD = 25
	OUT_OF_BOUNDS_PENALTY = 250
	MOVE_PENALTY = 1
	OBSERVATION_SPACE_VALUES = (SIZE, SIZE, 3)  # 4
	ACTION_SPACE_SIZE = 4
	SCORE = 0

	def reset(self):		
		self.snake = Snake(self.SIZE, (255, 255, 255))
		self.food = Food(self.SIZE, (0, 255, 0))		
		self.SCORE = 0

		while self.food == self.snake:
		    self.food = Food(self.SIZE)        

		self.episode_step = 0

		if self.RETURN_IMAGES:
		    observation = np.array(self.get_image())

		return observation

	def step(self, action):
		self.episode_step += 1
		self.snake.action(action)

		if self.RETURN_IMAGES:
		    new_observation = np.array(self.get_image())

		if self.snake.body[0] == self.food.food_list:
		 	reward = self.FOOD_REWARD
		 	self.SCORE += 1
		 	self.snake.add_tail(self.SCORE)
		 	self.food = Food(self.SIZE, (0, 255, 0))
		 	print("snake ate the food")		
		else:
			reward = -self.MOVE_PENALTY

		done = False
		if reward == self.FOOD_REWARD or reward == -self.EAT_YOURSELF_PENALTY or self.episode_step >= 200:			
			done = True
			if self.episode_step >= 200:
				print("No food eaten")
				env.reset()


		return new_observation, reward, done
	

	def render(self):
		img = self.get_image()
		img = img.resize((300, 300))  # resizing so we can see our agent in all its glory.
		cv2.imshow("image", np.array(img))  # show it!
		cv2.waitKey(100)
				

    # FOR CNN #
	def get_image(self):
		env = np.zeros((self.OBSERVATION_SPACE_VALUES), dtype=np.uint8) # starts an rbg of our size
		env[self.food.x][self.food.y] = self.food.colour  # sets the food location tile to colour green		
		for i in range(len(self.snake.body)):
			env[self.snake.body[i][0]][self.snake.body[i][1]] = self.snake.colour # sets the snake location tile to colour white
			#print(f"Y:{self.snake.body[i][0]}")
			#print(f"X:{self.snake.body[i][1]}")		
		img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho colour definitions are bgr. ???

		return img

env = Environment()
env.reset()

while True:
	#time.sleep(0.068)	
	done = False
	env.render()
	Action = input("Enter a direction\n")
	if Action == "w":		
		new_observation, reward, done = env.step(0)
	elif Action == "a":		
		new_observation, reward, done = env.step(1)
	elif Action == "d":		
		new_observation, reward, done = env.step(2)
	elif Action == "s":		
		new_observation, reward, done = env.step(3)
	else:
		print("Not a valid key")

	
	# if done == True:
	# 	env.reset()		
	
