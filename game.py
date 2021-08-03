import pygame
from pygame.constants import K_DOWN
import pytmx
import pyscroll
from player import Player

class Game:
    
    def __init__(self):
        # create windows
        self.screen = pygame.display.set_mode((800, 600))
        self.map = "world"
        self.player = None
        pygame.display.set_caption("Hero game")
        self.exit_map = None
        self.walls = []
        self.switch_maps('world', 'house')

    
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] :
            self.player.move_up()
            self.player.change_animation('up')
        elif  pressed[pygame.K_DOWN] :
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT] :
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house(self):
        self.map = "home"
        # load card
        tmx_data = pytmx.util_pygame.load_pygame('assert//home.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # wall
        self.walls = []
        for obj in tmx_data.objects:
            # if obj.type == 'collision' :
            #     self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # enter house
        exit_house = tmx_data.get_object_by_name('exit_house')
        self.exit_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        spawn_house_point = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y  - 40
        self.group = pyscroll.PyscrollGroup(
                map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        
    def switch_world(self):
        self.map = "world"
        # load card
        tmx_data = pytmx.util_pygame.load_pygame('assert//card.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # wall
        self.walls = []
        for obj in tmx_data.objects:
            # if obj.type == 'collision' :
            #     self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type in ['collision','water']:
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # enter house
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        spawn_house_point = tmx_data.get_object_by_name("spawn_world")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y
        self.group = pyscroll.PyscrollGroup(
                map_layer=map_layer, default_layer=2)
        self.group.add(self.player)
        
    def switch_maps(self, map_name_current, old_map_name, pos=0):
        self.map = map_name_current
        # load card
        map_path= 'assert//{}.tmx'.format(map_name_current)
        print(map_path)
        tmx_data = pytmx.util_pygame.load_pygame(map_path)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())


        # # gen player
        if self.player is None:
            player_position = tmx_data.get_object_by_name("player")
            self.player = Player(player_position.x, player_position.y)


        # wall
        self.walls = []
        for obj in tmx_data.objects:
            # if obj.type == 'collision' :
            #     self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type in ['collision','water']:
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # enter house
        enter_house = tmx_data.get_object_by_name('enter_{}'.format(old_map_name))
        self.exit_map = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        spawn_house_point = tmx_data.get_object_by_name("spawn_{}".format(map_name_current))
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + pos
        self.group = pyscroll.PyscrollGroup(
                map_layer=map_layer, default_layer=2)
        self.group.add(self.player)   

    def update(self):
        self.group.update()

        # check enter hoouse
        if self.map == 'world' and self.player.feet.colliderect(self.exit_map):
            self.switch_maps("house", "world", -40)
            
        # check enter hoouse
        if self.map == 'house' and self.player.feet.colliderect(self.exit_map):
            self.switch_maps("world", "house")

        # check collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:   
                sprite.move_back()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(30)
        pygame.quit()


