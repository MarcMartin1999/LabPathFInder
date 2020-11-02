import pygame
import math
from queue import PriorityQueue
from random import randint
WIDTH = 800
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("LaberinthSolver")


BLACK=(0,0,0)
WHITE = (255,255,255)
RED = (253,115,85)

class Vertex:
	def __init__(self, row, column, width, height ,total_rows, total_columns):

		self.row = row
		self.x = width*column
		self.y = height*row
		self.column = column
		self.width = width
		self.height = height
		self.total_columns = total_columns
		self.total_rows = total_rows
		self.color = WHITE
		self.neighbors = []
		self.open = False

	def get_pos(self):
		return self.column, self.row

	def is_open(self):
		return self.open

	def is_wall(self):
		return self.color == BLACK

	def is_clean(self):
		return self.color == WHITE

	def is_red(self):
		return self.color == RED

	def reset(self):
		self.color = WHITE
		self.open = False

	def make_open(self):
		self.open = True
	
	def make_closed(self):
		self.open = False
	
	def make_wall(self):
		self.color = BLACK

	def make_goal(self):
		self.color = RED

	def make_start(self):
		self.color = RED

	def make_path(self):
		self.color = RED

	def draw(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))

	def update_neighbors(self,grid):
		self.neighbors = []

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_wall():
			self.neighbors.append(grid[self.row + 1][self.column])

		if self.row > 0  and not grid[self.row - 1][self.column].is_wall():
			self.neighbors.append(grid[self.row - 1][self.column])

		if self.column < self.total_columns - 1 and not grid[self.row][self.column+1].is_wall():
			self.neighbors.append(grid[self.row][self.column+1])

		if self.column > 0  and not grid[self.row ][self.column-1].is_wall():
			self.neighbors.append(grid[self.row - 1][self.column])


	def __lt__(self,other):
		return False

def h(p1,p2):
	x1, y1 = p1 
	x2, y2 = p2 

	return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows,columns,width,height):
	grid = []

	x_base = width/columns
	y_base = height/rows
	for i in range(rows):
		grid.append([])
		for j in range(columns):
			vertex = Vertex(i,j,x_base,y_base,rows,columns)
			grid[i].append(vertex)

	return grid

def list_walls(grid):
	walls=[]
	for row in grid:
		for vertex in row:
			if vertex.is_wall:
				walls.append(vertex)
	return walls

def update_all_neighbors(grid):
	for row in grid:
		for vertex in row:
			vertex.update_neighbors(grid)

def its_red_neighbor(vertex):

	for neighbor in vertex.neighbors:
		if neighbor.is_red():
			return True
	return False

def lab_algorithm(grid,rows,columns,win):
	walls = list_walls(grid)
	direction =0
	update_all_neighbors(grid)
	random_branch = columns*rows//10
	for x in range(0,random_branch):
		random_length = randint(3,rows//7)
		walls = list_walls(grid)
		wall = walls[randint(0, len(walls)-1)]
		length_wall = len(wall.neighbors)-1
		while length_wall <= 2:
			wall = walls[randint(0, len(walls)-1)]
			length_wall = len(wall.neighbors)-1
		direction = randint(0,length_wall)
		for y in range(0,random_length):
			length_wall = len(wall.neighbors)-1
			if not direction >length_wall:
				neighbor = wall.neighbors[direction]
				if neighbor.is_wall() or neighbor.is_red() or its_red_neighbor(neighbor):
					pass
				else:
					neighbor.make_wall()
					wall = neighbor
		update_all_neighbors(grid)
		draw(win, grid)
	



	
	update_all_neighbors(grid)

def reconstruct_path(came_from,current,draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def path_algorithm(draw,grid,start,end):

	count = 0
	open_set = PriorityQueue()
	open_set.put((0,count,start))
	came_from = {}
	g_score = {vertex:float("inf")for row in grid for vertex in row}
	g_score[start] = 0
	f_score ={vertex:float("inf")for row in grid for vertex in row}
	f_score[start]= h(start.get_pos(),end.get_pos())

	open_set_hash={start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from,end,draw)

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1


			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor],count,neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_closed()
		draw()

		if current != start:
			current.make_closed



def draw(win,grid):
	win.fill(WHITE)
	for col in grid:
		for vertex in col:
			vertex.draw(win)
	pygame.display.update()

def reset_grid(grid,win):
	win.fill(WHITE)
	for col in grid:
		for vertex in col:
			vertex.reset()
	pygame.display.update()


def create_lab(columns,rows,grid,win,start,goal):
	for i in range(0,columns):
		for j in range(0,rows):
			if i == 0:
				grid[j][i].make_wall()
			if j == 0:
				grid[j][i].make_wall()
			if j == rows-1:
				grid[j][i].make_wall()
			if i == columns-1:
				grid[j][i].make_wall()

	random_row = randint(1,rows)-2
	grid[random_row][columns-1].reset()
	grid[random_row][columns-1].make_goal()
	goal = grid[random_row][columns-1]
	random_row = randint(1,rows)-2
	grid[random_row][0].reset()
	grid[random_row][0].make_goal()
	start =grid[random_row][0]
	print()
	draw(win, grid)
	lab_algorithm(grid,rows,columns,win)
	path_algorithm(lambda:draw(win,grid), grid, start, goal)

def main(win,width,height):
	rows = 50
	columns = 100
	grid = make_grid(rows,columns,width,height)
	run = True

	start = None
	goal = None

	win.fill(WHITE)
	while run:
		draw(win,grid)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0] :
				reset_grid(grid,win)
				create_lab(columns,rows,grid,win,start,goal)
				

	pygame.quit()
main(WIN,WIDTH,HEIGHT)
