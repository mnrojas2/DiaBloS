import sys
import os
import pygame
import numpy as np

# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

FPS = 60

block_id = [0,1,2,3,4]
line_id = [0,1,2,3,4]

# --- classes --- (CamelCase names)
class Default_settings:
    def __init__(self):
        self.line_width = 2

class Block:
    def __init__(self,sid,coords,in_ports,out_ports):
        self.name = "Block"+str(sid)
        self.sid = sid
        self.left = coords[0]
        self.top = coords[1]
        self.width = coords[2]
        self.height = coords[3]
        self.port_diameter = 10

        self.in_ports = in_ports    # numero de puertos de entrada
        self.out_ports = out_ports  # numero de puertos de salida

        self.in_coords = []
        self.out_coords = []
        self.place_ports()
        
        self.rectf = pygame.rect.Rect(self.left-self.port_diameter,self.top,self.width+2*self.port_diameter,self.height) 
        self.dragging = False
        self.selected = False

    def draw_Block(self,place): #Dibujar figura
        pygame.draw.rect(place,GREEN,(self.left, self.top, self.width, self.height))
        for port_in_location in self.in_coords:
            pygame.draw.circle(place,RED,port_in_location,self.port_diameter)

        for port_out_location in self.out_coords:
            pygame.draw.circle(place,RED,port_out_location,self.port_diameter)

    def update_Block(self): #Reubicar puertos figura
        self.rectf.update((self.left-self.port_diameter,self.top,self.width+2*self.port_diameter,self.height))
        self.place_ports()

    def place_ports(self): #Reubicar circulos segun bloque
        self.in_coords = []
        self.out_coords = []
        if self.in_ports > 0:
            for i in range(self.in_ports):
                port_in = (self.left,self.top+self.height*(i+1)/(self.in_ports+1))
                self.in_coords.append(port_in)
        if self.out_ports > 0:
            for j in range(self.out_ports):
                port_out = (self.left+self.width,self.top+self.height*(j+1)/(self.out_ports+1))
                self.out_coords.append(port_out)

    def relocate_Block(self,new_coords): #new_coords = (left,top)
        self.left = new_coords[0]
        self.top = new_coords[1]
        self.update_Block()

    def resize_Block(self,new_coords): #new_dims = (width,height)
        self.width = new_coords[0]
        self.height = new_coords[1]
        self.update_Block()

    def port_collision(self,m_coords):
        #usar for para calcular distancias con todos los puertos (diferenciando entre entrada y salida), retorna el tipo de puerto y su id o simplemente nada (-1,-1)
        for i in range(len(self.in_coords)):
            p_coords = self.in_coords[i]
            distance = np.sqrt((m_coords[0]-p_coords[0])**2+(m_coords[1]-p_coords[1])**2)
            if distance <= self.port_diameter:
                return ("i",i)
        for j in range(len(self.out_coords)):
            p_coords = self.out_coords[j]
            distance = np.sqrt((m_coords[0]-p_coords[0])**2+(m_coords[1]-p_coords[1])**2)
            if distance <= self.port_diameter:
                return ("o",j)
        return (-1,-1)

    def draw_selected(self,place):
        #ancho lina y espacio que cambiar por algo definido en clase default
        l_width = 5  #ancho linea
        ls_width = 5 #ancho separacion linea-bloque
        pygame.draw.line(screen, BLACK, (self.left-ls_width,self.top-ls_width), (self.left+self.width+ls_width,self.top-ls_width), l_width)
        pygame.draw.line(screen, BLACK, (self.left-ls_width,self.top-ls_width), (self.left-ls_width,self.top+self.height+ls_width), l_width)
        pygame.draw.line(screen, BLACK, (self.left+self.width+ls_width,self.top+self.height+ls_width), (self.left+self.width+5,self.top-ls_width), l_width)
        pygame.draw.line(screen, BLACK, (self.left+self.width+ls_width,self.top+self.height+ls_width), (self.left-ls_width,self.top+self.height+ls_width), l_width)

    def change_port_number(self):
        port_i = int(input("Numero puertos input: "))
        port_o = int(input("Numero puertos output: "))
        self.in_ports = port_i
        self.out_ports = port_o
        self.place_ports()
    
class Line:
    def __init__(self, sid, srcblock, srcport, points, dstblock, dstport, zorder):
        self.name = "Line"+str(sid)#id linea
        self.sid = sid
        self.srcblock = srcblock    #bloque origen
        self.srcport = srcport      #puerto origen del bloque
        self.points = points        #puntos de vertice(?) ((a,b),(c,d),(e,f),...)
        self.dstblock = dstblock    #bloque destino
        self.dstport = dstport      #puerto destino
        self.zorder = zorder        #Orden dibujado elemento

    def draw_line(self):
        for i in range(len(self.points)-1):
            pygame.draw.line(screen, BLACK, self.points[i], self.points[i+1], 2)

    def update_line(self,block_list): ######## POR TERMINAR
        for block in block_list:
            if block.name == self.srcblock:
                startline = block.out_coords[self.srcport]
            if block.name == self.dstblock:
                endline = block.in_coords[self.dstport]
        self.points = (startline,endline)

    def __str__(self):
        return self.name+": From "+str(self.srcblock)+", port "+str(self.srcport)+" to "+str(self.dstblock)+", port "+str(self.dstport)

# --- functions --- (lower_case names)

def print_lines(pointlist):
    for line in pointlist:
        line.draw_line()

def update_lines(blocklist,pointlist):
    for line in pointlist:
        line.update_line(blocklist)
        
def blockScreen(block_list,zone):
    for block_elem in block_list:
        if block_elem.selected == True:
            block_elem.draw_selected(zone)
        block_elem.draw_Block(zone)

def port_availability(dst_line,linelist):
    for line in linelist:
        if line.dstblock == dst_line[0] and line.dstport == dst_line[1]:
            return False
    return True

def check_line_block(line,b_delete_list):
    for b_del in b_delete_list:
        if line.srcblock == b_del.name or line.dstblock == b_del.name:
            return True
        else:
            return False

def check_line_port(line,block):
    if line.srcblock == block.name and line.srcport > block.out_ports-1:
        return True
    elif line.dstblock == block.name and line.dstport > block.in_ports-1:
        return True
    else:
        return False

def assign_id(id_list):
    #asignacion de id a partir de una lista de valores disponibles
    sid = id_list[0]
    id_list = id_list[1:]
    id_list.append(id_list[-1]+1)
    return sid, id_list

def get_id_back(id_list,del_list):
    #recuperacion de un id liberado por un elemento eliminado
    for id_elem in del_list:
        id_list.append(id_elem.sid)
    id_list.sort()
    if len(id_list) > id_list[-1]+1:
        id_list = id_list[:id_list[-1]]
    elif len(id_list) == id_list[-1]+1:
        id_list = id_list[:5]
    return id_list
            
# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption("PySimSnide")

# - objects -
block = pygame.rect.Rect(60, 40, 120, 80)

blocks_list = []
line_list = []

cod = (520,320,120,80)
val, block_id = assign_id(block_id)
fig_test = Block(val,cod,2,1)
blocks_list.append(fig_test)

cod2 = (720,520,120,80)
val, block_id = assign_id(block_id)
gain_test = Block(val,cod2,1,2)
blocks_list.append(gain_test)

cod3 = (320,520,120,80)
val, block_id = assign_id(block_id)
asd_test = Block(val,cod3,1,1)
blocks_list.append(asd_test)

# - mainloop -

clock = pygame.time.Clock()

running = True
line_creation = 0
srcLine = ("",0,(0,0))
dstLine = ("",0,(0,0))
only_one = False

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if block.collidepoint(event.pos):               
                    val, block_id = assign_id(block_id) 
                    new_block = Block(val,(60, 40, 120, 80),1,1)
                    blocks_list.append(new_block)
                        
            elif event.button == 1:                
                for b_elem in blocks_list:
                    if b_elem.rectf.collidepoint(event.pos):
                        b_elem.selected = True
                        p_col = b_elem.port_collision(event.pos)
                        if p_col[0] == -1 and only_one == False:
                            b_elem.dragging = True
                            only_one = True
                            mouse_x, mouse_y = event.pos
                            offset_x = b_elem.left - mouse_x
                            offset_y = b_elem.top - mouse_y

                        elif p_col[0] == 'i':
                            dstLine = (b_elem.name, p_col[1], b_elem.in_coords[p_col[1]]) #block name, port number, port location
                            dst_available = port_availability(dstLine,line_list)
                            if dst_available == True:
                                if line_creation == 0:
                                    line_creation = 2
                                elif line_creation == 1:
                                    cords = (srcLine[2],dstLine[2])
                                    lval, line_id = assign_id(line_id)
                                    line = Line(lval, srcLine[0], srcLine[1], cords, dstLine[0], dstLine[1], 1) #zorder sin utilizar todavia
                                    line_list.append(line)
                                    line_creation = 0

                        elif p_col[0] == 'o':
                            srcLine = (b_elem.name, p_col[1], b_elem.out_coords[p_col[1]]) #block name, port number, port location
                            if line_creation == 0:
                                line_creation = 1
                            elif line_creation == 2:
                                cords = (srcLine[2],dstLine[2])
                                lval, line_id = assign_id(line_id)
                                line = Line(lval, srcLine[0], srcLine[1], cords, dstLine[0], dstLine[1], 1) #zorder sin utilizar todavia
                                line_list.append(line)
                                line_creation = 0
                    else:
                        b_elem.selected = False
                        #line_creation = 0

            elif event.button == 4:
                print("Ruedita arriba")

            elif event.button == 5:
                print("Ruedita abajo")
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            for b_elem in blocks_list:
                if event.button == 1: 
                    b_elem.dragging = False
                    only_one = False
                    update_lines(blocks_list,line_list)

        elif event.type == pygame.MOUSEMOTION:
            for b_elem in blocks_list:
                if b_elem.dragging == True and only_one == True:
                    mouse_x, mouse_y = event.pos
                    b_elem.relocate_Block((mouse_x + offset_x,mouse_y + offset_y))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                b_del = [x for x in blocks_list if x.selected == True]
                l_del = [x for x in line_list if check_line(x,b_del)]
                block_id = get_id_back(block_id,b_del)
                line_id = get_id_back(line_id,l_del)
                print(block_id,line_id)
                blocks_list = [x for x in blocks_list if not (x.selected == True)]
                line_list = [x for x in line_list if not check_line_block(x,b_del)]

    if pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.mouse.get_pressed() == (1,0,0):
        for b_elem in blocks_list:
            if b_elem.rectf.collidepoint(event.pos):
                b_elem.change_port_number()
                line_list = [x for x in line_list if not check_line_port(x,b_elem)]

    # - updates (without draws) -

    # empty

    # - draws (without updates) -
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, block)
    pygame.draw.line(screen, BLACK, [250, 0], [250, 720], 2)
    
    blockScreen(blocks_list,screen)
    print_lines(line_list)
    pygame.display.flip()

    # - constant game speed / FPS -
    clock.tick(FPS)

# - end -

pygame.quit()
