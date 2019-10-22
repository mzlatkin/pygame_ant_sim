import pygame
from pygame.locals import *

import sys, os, traceback
import random
from collections import deque
from settings import *
from GameBoard import *
from Astar import *
import time
# from Ant import *

if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

pygame.display.init()
pygame.font.init()

icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Ant Farm Sim")
surface = pygame.display.set_mode(screen_size)

all_sprites_list = pygame.sprite.Group()
all_ants_list = pygame.sprite.Group()
updated_sprites = pygame.sprite.Group()

# print (str(ANT_FARM_IMAGE[0,0]) + " ground")
# print (str(ANT_FARM_IMAGE[18,15]) + " stone")
# print (str(ANT_FARM_IMAGE[7,93]) + " sky")
# print (str(ANT_FARM_IMAGE[8,5]) + " end")
# print (str(ANT_FARM_IMAGE[9,16]) + " Start")

def setup_game():
    global ground_array
    ground_array = []
    ant_start = []
    ant_finish = []
    for row in range(0,play_area_height):
        ground_array.append([])
        for col in range(0,play_area_width):
            if ANT_FARM_IMAGE[row,col] == SKY_VALUE:
                new_ground_obj = Sky([row,col])
            elif ANT_FARM_IMAGE[row,col] == GROUND_VALUE:
                new_ground_obj = Ground([row,col])
            elif ANT_FARM_IMAGE[row,col] == STONE_VALUE:
                new_ground_obj = Stone([row,col])
            elif ANT_FARM_IMAGE[row,col] == CRUST_VALUE or ANT_FARM_IMAGE[row,col] == ANT_START_VALUE:
                new_ground_obj = Crust([row,col])
            else:
                new_ground_obj = Ground([row,col])
            
            if ANT_FARM_IMAGE[row,col] == ANT_START_VALUE:
                ant_start = [row,col]
            elif ANT_FARM_IMAGE[row,col] == ANT_END_VALUE:
                ant_finish = [row,col]
            all_sprites_list.add(new_ground_obj)
            ground_array[row].append(new_ground_obj)

    for i in range(0,1):
        all_ants_list.add(Ant(ground_array,ant_start,ant_finish))

    surface.fill((0,0,0))
    all_sprites_list.draw(surface)
    pygame.display.flip()


class Ant(pygame.sprite.Sprite):
    """ This class represents the creature, the creature takes a speed and size. """
    def __init__(self,ground_array,pos,destination):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.pos = pos
        self.destination = destination

        self.image = pygame.Surface([1*SCALE_FACTOR, 1*SCALE_FACTOR])
        
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.ground_array = ground_array


        self.path = []        
        self.path_index = 0
        self.new_path = []
        self.new_path_index = 0
        self.old_path_index = 0
        
        self.damage = 10

        self.entering_mine = True

        self.drop_off_dir = -1
    
    def go_here(self,destination):
        
        self.destination = destination
        if len(self.path) == 0:
            self.path = astar(self.ground_array, [self.pos[0],self.pos[1]], [self.destination[0],self.destination[1]])
            self.path_index = len(self.path)-1
            # print("path: "+ str(self.path))
        else:
            self.new_path = astar(self.ground_array, [self.pos[0],self.pos[1]], [self.destination[0],self.destination[1]])
            self.new_path_index = len(self.new_path)-1
            self.old_path_index = self.path_index
            # print("new_path: "+ str(self.new_path))
   
    def update(self):
        global updated_sprites
        updated_sprites.add(self.ground_array[self.pos[0]][self.pos[1]])

        if len(self.new_path) > 0:
            temp = self.new_path[self.new_path_index]            
            
            # print(temp)
            if self.new_path_index > 0:
                next_tile = get_ground_element(self.new_path[self.new_path_index-1])
                ground_collected = next_tile.dig(self.damage)                 
                if ground_collected:
                    self.new_path_index-=1
                else:
                    if next_tile.dug:
                        self.new_path_index-=1
                    if isinstance(next_tile, Crust):
                        temp = self.path.pop()
                temp = self.new_path[self.new_path_index]
                old_path = self.path[self.old_path_index]
                # print(temp == old_path)
                # removing old path steps from path on the way to a new destination
                if temp != old_path:
                    self.old_path_index+=1
                    if temp != self.path[self.old_path_index]:
                        # print("on new path")
                        temp_path_holder = []
                        for i in range(0,self.new_path_index + 1):
                            temp_path_holder.append(self.new_path[i])
                        for i in range(self.old_path_index-1,len(self.path)):
                            temp_path_holder.append(self.path[i])
                        # print("new_path: " + str(temp_path_holder))
                        self.path = temp_path_holder
                        self.path_index = self.new_path_index
                        self.new_path = []
                        # print(self.path)
            
            self.pos[0] = temp[0]
            self.pos[1] = temp[1]

        elif len(self.path) > 0:
            # print(self.path[self.path_index])
            # print(self.path_index)
            # print("entering mine: " + str(self.entering_mine))

            temp = self.path[self.path_index]
            if self.entering_mine:
                # print(self.path[self.path_index])
                if self.path_index > 0:
                    next_tile = get_ground_element(self.path[self.path_index-1])
                    ground_collected = next_tile.dig(self.damage) 

                    if ground_collected:
                        self.entering_mine = False
                        self.path_index-=1
                    else:
                        if next_tile.dug:
                            self.path_index-=1
                        # if isinstance(next_tile, Crust):
                        #     temp = self.path.pop()
                    temp = self.path[self.path_index]
                            
            else:
                if self.path_index < len(self.path)-1:
                    print(type(get_ground_element(self.path[self.path_index])))
                    if isinstance(get_ground_element(self.path[self.path_index]), Crust):
                        drop_off_dirt([temp[0]+self.drop_off_dir,temp[1]],self.drop_off_dir)
                        if self.drop_off_dir == 1: self.drop_off_dir = -1
                        else:                       self.drop_off_dir = 1
                        self.entering_mine = True
                    else:
                        self.path_index+=1
                        temp = self.path[self.path_index]
                else:
                    drop_off_dirt([temp[0]+self.drop_off_dir,temp[1]],self.drop_off_dir)
                    if self.drop_off_dir == 1: self.drop_off_dir = -1
                    else:                       self.drop_off_dir = 1
                    self.entering_mine = True
        
            self.pos[0] = temp[0]
            self.pos[1] = temp[1]
            # print("-------")
        self.rect.x = self.pos[0]*SCALE_FACTOR
        self.rect.y = self.pos[1]*SCALE_FACTOR
        
        self.ground_array[self.pos[0]][self.pos[1]].dig(self.damage)
        updated_sprites.add(self.ground_array[self.pos[0]][self.pos[1]])


def drop_off_dirt(position,dir):
    global updated_sprites
    corner_tile = ground_array[position[0]+dir][position[1]+1]
    current_tile = ground_array[position[0]][position[1]]
    ubove_tile = ground_array[position[0]][position[1]-1]
    if isinstance(corner_tile, Ground) and not isinstance(current_tile, Ground):
        temp = Ground(position)
        ground_array[position[0]][position[1]] = temp
        updated_sprites.add(temp)
        return None
    elif isinstance(current_tile, Ground):
        drop_off_dirt(ubove_tile.pos,dir)
    elif isinstance(current_tile, Sky) or isinstance(current_tile, Crust):
        drop_off_dirt(corner_tile.pos,dir)


        
def get_ground_element(point):
    return ground_array[point[0]][point[1]]

def get_input():
    # keys_pressed = pygame.key.get_pressed()
    # mouse_buttons = pygame.mouse.get_pressed()
    # mouse_position = pygame.mouse.get_pos()
    # mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_r: setup_game() #reset
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            for ant in all_ants_list:
                ant.go_here([int(mousex/SCALE_FACTOR), int(mousey/SCALE_FACTOR)])

    return True

def update():
    global TIMER
    global ground_array
    global updated_sprites
    updated_sprites = pygame.sprite.Group()
    # TIMER += 1
    # if TIMER % 10 == 0 and TIMER < 10*MAX_ANTS:
    #     all_ants_list.add(Ant(ground_array, [2,22],[22,2]))
    for ant in all_ants_list:
        ant.update()
    return None

def collision_detect():
    return None
    

def draw():
    updated_sprites.draw(surface)
    all_ants_list.draw(surface)
    pygame.display.flip()

def main():
    setup_game()
    clock = pygame.time.Clock()
    while True:
        if not get_input(): break
        update()

        # collision_detect()
        draw()
        clock.tick(target_fps)
    pygame.quit()
    
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()




 # old pathing (BFS)
# def reset_map(self):
#     self.direction_map = []
#     for row in range(0,play_area_height):
#         self.direction_map.append([])
#         for col in range(0,play_area_width):
#             self.direction_map[row].append(sys.maxsize)

# def create_direction_map(self):
#     path_q = deque()
#     path_q.append([self.pos[0],self.pos[1]])
#     self.direction_map[self.pos[0]][self.pos[1]] = 0
#     found_dest = False
#     while len(path_q) > 0:
#         current_item = path_q.popleft()
#         for i in range(-1,2):
#             for j in range(-1,2):
#                 # print(str(current_item[0]+i) + "," + str(current_item[1]+j))
#                 if current_item[0]+i < play_area_height and current_item[1]+j < play_area_width and current_item[0]+i >=0  and current_item[1]+j >= 0:
#                     if (i == 0 and j ==-1) or (i == 0 and j ==1) or (i == 1 and j ==0) or (i == -1 and j ==0):
#                         # print([current_item[0]+i,current_item[1]+j])
#                         if self.ground_array[current_item[0]+i][current_item[1]+j].diggable:
#                             if self.direction_map[current_item[0]+i][current_item[1]+j] > self.direction_map[current_item[0]][current_item[1]] + 1:
#                                 self.direction_map[current_item[0]+i][current_item[1]+j] = self.direction_map[current_item[0]][current_item[1]] + 1
#                                 path_q.append([current_item[0]+i,current_item[1]+j])
#                                 if [current_item[0]+i,current_item[1]+j] == self.destination:
#                                     return None

# def reset_path(self):     
#     self.path = []

#     self.path.append(self.destination)

#     for node in self.path:
#         current_node = node
#         for i in range(-1,2):
#             for j in range(-1,2):
#                 # print(self.direction_map[node[0]+i][node[1]+j])
#                 if self.direction_map[node[0]+i][node[1]+j] < self.direction_map[current_node[0]][current_node[1]]:
#                     current_node = [node[0]+i,node[1]+j]
#         if(current_node != node):
#             self.path.append(current_node)
    
#     # print (self.path)
