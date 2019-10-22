from PIL import Image

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
BROWN    = (  76, 57,  29)

GROUND_VALUE = (140, 75, 28)
STONE_VALUE = (78, 78, 80)
SKY_VALUE = (0, 0, 255)
CRUST_VALUE = (140, 75, 170)

ANT_START_VALUE = (255, 0, 0)
ANT_END_VALUE = (0, 187, 63)


movement_substeps = 1
target_fps = 100.0
dt = 1.0/target_fps


im = Image.open('Ant_farm.png')
ANT_FARM_IMAGE = im.load()
play_area_height = im.size[1]
play_area_width = im.size[0]


SCALE_FACTOR = 8
MAX_ANTS = 10
TIMER = 1

ground_array = []

screen_size = [play_area_height * SCALE_FACTOR,play_area_height*SCALE_FACTOR]