import pygame
from pygame.locals import *
import random
import sys, os, traceback
from settings import *
from collections import deque

class Ant(pygame.sprite.Sprite):
    """ This class represents the creature, the creature takes a speed and size. """
    def __init__(self,ground_array,pos,destination):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.pos = pos
        self.destination = destination
        
        self.start_pos = [self.pos[0],self.pos[1]]
        self.end_pos = [self.destination[0],self.destination[1]]

        self.image = pygame.Surface([1*SCALE_FACTOR, 1*SCALE_FACTOR])
        
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.speed = 1

        self.rand_dir = random.randint(1, 8)
        self.rethink_time = 40
        self.rethink_counter = 0

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.ground_array = ground_array

        self.destination = destination
        self.direction_map = []
        self.path = []

        self.reset_map()
        self.create_direction_map()
        self.reset_path()
    
    def go_here(self,destination):
        self.destination = destination
        self.reset_map()
        self.create_direction_map()
        self.reset_path()

    def reset_map(self):
        self.direction_map = []
        for row in range(0,play_area_height):
            self.direction_map.append([])
            for col in range(0,play_area_width):
                self.direction_map[row].append(sys.maxsize)

    def create_direction_map(self):
        path_q = deque()
        path_q.append([self.pos[0],self.pos[1]])
        self.direction_map[self.pos[0]][self.pos[1]] = 0
        found_dest = False
        while len(path_q) > 0:
            current_item = path_q.popleft()
            for i in range(-1,2):
                for j in range(-1,2):
                    # print(str(current_item[0]+i) + "," + str(current_item[1]+j))
                    if current_item[0]+i < play_area_width and current_item[1]+j < play_area_height and current_item[0]+i >=0  and current_item[1]+j >= 0:
                        if (i == 0 and j ==-1) or (i == 0 and j ==1) or (i == 1 and j ==0) or (i == -1 and j ==0):
                            # print([current_item[0]+i,current_item[1]+j])
                            if self.ground_array[current_item[0]+i][current_item[1]+j].diggable:
                                if self.direction_map[current_item[0]+i][current_item[1]+j] > self.direction_map[current_item[0]][current_item[1]] + 1:
                                    self.direction_map[current_item[0]+i][current_item[1]+j] = self.direction_map[current_item[0]][current_item[1]] + 1
                                    path_q.append([current_item[0]+i,current_item[1]+j])
                                    if [current_item[0]+i,current_item[1]+j] == self.destination:
                                        return None

    def reset_path(self):                
        self.path = []

        self.path.append(self.destination)

        for node in self.path:
            current_node = node
            for i in range(-1,2):
                for j in range(-1,2):
                    # print(self.direction_map[node[0]+i][node[1]+j])
                    if self.direction_map[node[0]+i][node[1]+j] < self.direction_map[current_node[0]][current_node[1]]:
                        current_node = [node[0]+i,node[1]+j]
            if(current_node != node):
                self.path.append(current_node)
        
        # print (self.path)

    def change_dir(self):
        self.rand_dir = random.randint(1, 8)
 
    def update(self):
        """ Move the creature. """
        # updated_sprites.add(self.ground_array[self.pos[0]][self.pos[1]])
            # self.rethink_counter += 1
            # if self.rethink_counter > self.rethink_time:
            #     self.rethink_counter = 1
            #     self.change_dir()
            # if self.rand_dir == 1 or self.rand_dir == 2 or self.rand_dir == 3:
            #     if not self.rect.y-self.speed < 1:
            #         self.rect.y -= self.speed
            #     else:
            #         self.change_dir()
            # if self.rand_dir == 1 or self.rand_dir == 4 or self.rand_dir == 6:
            #     if not self.rect.x-self.speed < 1:
            #         self.rect.x -= self.speed
            #     else:
            #         self.change_dir()
            # if self.rand_dir == 6 or self.rand_dir == 7 or self.rand_dir == 8:
            #     if not self.rect.y+self.speed > play_area_height-1:
            #         self.rect.y += self.speed
            #     else:
            #         self.change_dir()
            # if self.rand_dir == 3 or self.rand_dir == 5 or self.rand_dir == 8:
            #     if not self.rect.x+self.speed > play_area_width-1:
            #         self.rect.x += self.speed
            #     else:
            #         self.change_dir()
        
        # move to destination
            # if self.rect.x < self.destination[0]:
            #     self.rect.x+=1
            # if self.rect.y < self.destination[1]:
            #     self.rect.y+=1
            # if self.rect.x > self.destination[0]:
            #     self.rect.x-=1
            # if self.rect.x > self.destination[1]:
            #     self.rect.y-=1
        
        if len(self.path) != 0:
            temp = self.path.pop()
            self.pos[0] = temp[0]
            self.pos[1] = temp[1]
        else:
            if [self.pos[0],self.pos[1]] == self.end_pos:
                self.go_here(self.start_pos)
            else:
                self.go_here(self.end_pos)

        self.rect.x = self.pos[0]*SCALE_FACTOR
        self.rect.y = self.pos[1]*SCALE_FACTOR
        # self.ground_array[self.pos[0]][self.pos[1]].image.fill(((223, 191, 159)))
        # updated_sprites.add(self.ground_array[self.pos[0]][self.pos[1]])