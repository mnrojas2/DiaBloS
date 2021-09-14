import sys
import os
import pygame
import numpy as np
import time

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
        self.text_color = (255,   0,   0)
        self.font_size = 24

class Block:
    def __init__(self,sid,coords,in_ports,out_ports):
        self.name = "Block"+str(sid)    #Nombre del bloque
        self.sid = sid                  #id del bloque
        self.left = coords[0]           #Coordenada ubicación línea izquierda
        self.top = coords[1]            #Coordenada ubicación línea superior
        self.width = coords[2]          #Ancho bloque
        self.height = coords[3]         #Altura bloque
        
        self.port_radius = 10           #Radio circulo puertos
        self.height_base = self.height  #Variable que conserva valor de altura por defecto
        self.in_ports = in_ports        #Variable que contiene el número de puertos de entrada
        self.out_ports = out_ports      #Variable que contiene el número de puertos de salida

        self.in_coords = []             #Lista que contiene coordenadas para cada puerto de entrada
        self.out_coords = []            #Lista que contiene coordenadas para cada puerto de salida
        self.place_ports()              #Función que ubica las coordenadas de los puertos
        
        self.rectf = pygame.rect.Rect(self.left-self.port_radius,self.top,self.width+2*self.port_radius,self.height) #Rect que define la colisión del bloque
        self.dragging = False           #Booleano para determinar si el bloque se está moviendo
        self.selected = False           #Booleano para determinar si el bloque está seleccionado en el plano

        self.text = pygame.font.SysFont(None, font_size)
        self.text_display = self.text.render(self.name, True, RED)

    def draw_Block(self,place):
        #Dibuja el bloque y los puertos
        pygame.draw.rect(place,GREEN,(self.left, self.top, self.width, self.height))
        for port_in_location in self.in_coords:
            pygame.draw.circle(place,RED,port_in_location,self.port_radius)

        for port_out_location in self.out_coords:
            pygame.draw.circle(place,RED,port_out_location,self.port_radius)

    def update_Block(self):
        #Actualiza ubicación y dimensiones del bloque y número de puertos
        self.rectf.update((self.left-self.port_radius,self.top,self.width+2*self.port_radius,self.height))
        self.place_ports()

    def place_ports(self):
        #Función que ubica las coordenadas de los puertos
        self.in_coords = []
        self.out_coords = []

        #En caso que el número de puertos sea muy grande, se redimensiona el bloque
        port_height = max(self.out_ports,self.in_ports)*self.port_radius*2
        if port_height > self.height:
            self.height = port_height + 10
        elif port_height < self.height_base:
            self.height = self.height_base

        #Se ubican los puertos de forma simétrica en ambos lados
        if self.in_ports > 0:
            for i in range(self.in_ports):
                port_in = (self.left,self.top+self.height*(i+1)/(self.in_ports+1))
                self.in_coords.append(port_in)
        if self.out_ports > 0:
            for j in range(self.out_ports):
                port_out = (self.left+self.width,self.top+self.height*(j+1)/(self.out_ports+1))
                self.out_coords.append(port_out)

    def relocate_Block(self,new_coords): #new_coords = (left,top)
        #Función simple para reubicar el bloque en el plano, requiere coordenadas de la esquina superior izquierda
        self.left = new_coords[0]
        self.top = new_coords[1]
        self.update_Block()

    def resize_Block(self,new_coords): #new_dims = (width,height)
        #Función simple para redimensionar el bloque en el plano, requiere ancho y altura ingresado como tupla
        self.width = new_coords[0]
        self.height = new_coords[1]
        self.update_Block()

    def port_collision(self,m_coords):
        #Observa si el mouse toca alguno de los puertos de un bloque. Retorna una tupla con el tipo de puerto y su id.
        for i in range(len(self.in_coords)):
            p_coords = self.in_coords[i]
            distance = np.sqrt((m_coords[0]-p_coords[0])**2+(m_coords[1]-p_coords[1])**2)
            if distance <= self.port_radius:
                return ("i",i)
        for j in range(len(self.out_coords)):
            p_coords = self.out_coords[j]
            distance = np.sqrt((m_coords[0]-p_coords[0])**2+(m_coords[1]-p_coords[1])**2)
            if distance <= self.port_radius:
                return ("o",j)
        return (-1,-1)

    def draw_selected(self,place):
        #Dibuja linea de selección en torno a un bloque.
        #XHACER: ancho linea y espacio que cambiar por algo definido en clase default.
        l_width = 5  #ancho linea
        ls_width = 5 #ancho separacion linea-bloque
        pygame.draw.line(screen, BLACK, (self.left-ls_width,self.top-ls_width), (self.left+self.width+ls_width,self.top-ls_width), l_width)
        pygame.draw.line(screen, BLACK, (self.left-ls_width,self.top-ls_width), (self.left-ls_width,self.top+self.height+ls_width), l_width)
        pygame.draw.line(screen, BLACK, (self.left+self.width+ls_width,self.top+self.height+ls_width), (self.left+self.width+5,self.top-ls_width), l_width)
        pygame.draw.line(screen, BLACK, (self.left+self.width+ls_width,self.top+self.height+ls_width), (self.left-ls_width,self.top+self.height+ls_width), l_width)

    def change_number_ports(self,port_i,port_o):
        #Cambia el número de puertos de un bloque, con inputs desde el shell.
        #port_o = int(input("Numero puertos output: "))
        self.in_ports = port_i
        self.out_ports = port_o
        self.place_ports()
    
class Line:
    def __init__(self, sid, srcblock, srcport, points, dstblock, dstport, zorder):
        self.name = "Line"+str(sid) #Nombre de la línea
        self.sid = sid              #id de la línea
        self.srcblock = srcblock    #Nombre del bloque de origen
        self.srcport = srcport      #ID del puerto de origen del bloque
        self.points = points        #puntos de vertice para la línea(?) ((a,b),(c,d),(e,f),...)
        self.dstblock = dstblock    #Nombre del bloque de origen
        self.dstport = dstport      #ID del puerto de origen del bloque
        self.zorder = zorder        #ID de prioridad al momento de dibujar el bloque
        self.selected = False

    def draw_line(self):
        #Dibuja la línea con los datos del init
        for i in range(len(self.points)-1):
            if self.selected == True:
                line_width = 5
            else:
                line_width = 2
            pygame.draw.line(screen, BLACK, self.points[i], self.points[i+1], line_width)

    def update_line(self,block_list):
        #Actualiza el valor de la línea según la ubicación y tamaño del bloque
        for block in block_list:
            if block.name == self.srcblock:
                startline = block.out_coords[self.srcport]
            if block.name == self.dstblock:
                endline = block.in_coords[self.dstport]
        self.points = (startline,endline)

    def collision(self,m_coords):
        min_dst = 10
        line_A = np.array(self.points[0])
        line_B = np.array(self.points[1])
        m_coords = np.array(m_coords)
        
        if all(line_A == m_coords) or all(line_B == m_coords):
            distance_to_line = 0.0
        elif np.arccos(np.dot((m_coords - line_A)/np.linalg.norm(m_coords - line_A),(line_B - line_A)/np.linalg.norm(line_B - line_A))) > np.pi/2:
            distance_to_line = np.linalg.norm(m_coords - line_A)
        elif np.arccos(np.dot((m_coords - line_B)/np.linalg.norm(m_coords - line_B),(line_A - line_B)/np.linalg.norm(line_A - line_B))) > np.pi/2:
            distance_to_line = np.linalg.norm(m_coords - line_B)
        else:
            distance_to_line = np.linalg.norm(np.cross(line_A-line_B, line_A-m_coords))/np.linalg.norm(line_B-line_A)
        
        if distance_to_line > min_dst:
            return False
        else:
            return True

    def __str__(self):
        #Imprime en el shell, el nombre de la línea y su origen y destino
        return self.name+": From "+str(self.srcblock)+", port "+str(self.srcport)+" to "+str(self.dstblock)+", port "+str(self.dstport)

# --- functions --- (lower_case names)

def print_lines(linelist):
    #Dibuja las líneas a partir de una lista
    for line in linelist:
        line.draw_line()

def update_lines(blocklist,linelist):
    #Actualiza la ubicación de las líneas a partir de la ubicación de los bloques
    for line in linelist:
        line.update_line(blocklist)
        
def blockScreen(block_list,zone):
    #Dibuja los bloques incluyendo al seleccionado
    for b_elem in block_list:
        if b_elem.selected == True:
            b_elem.draw_selected(zone)
        b_elem.draw_Block(zone)
        zone.blit(b_elem.text_display, (b_elem.left+20, b_elem.top+5))

def port_availability(dst_line,linelist):
    #Comprueba si es que el puerto a conectar está libre para ello
    for line in linelist:
        if line.dstblock == dst_line[0] and line.dstport == dst_line[1]:
            return False
    return True

def check_line_block(line,b_delete_list):
    #Comprueba si es que hay lineas a bloques recientemente eliminados
    for b_del in b_delete_list:
        if line.srcblock == b_del.name or line.dstblock == b_del.name:
            return True
        else:
            return False

def check_line_port(line,block):
    #Comprueba si es que hay lineas a puertos recientemente eliminados
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

def draw_textbox(zone, color, block, rect, pointer):
    pygame.draw.rect(zone, color, block, width=2) 
    screen.blit(img_i, (block.left+20, block.top+20))
    screen.blit(img_edi, (block.left+20, block.top+40))
    screen.blit(img_o, (block.left+20, block.top+60))
    screen.blit(img_edo, (block.left+20, block.top+80))

    if pointer == 0:
        rect.topleft = (block.left+20, block.top+40)
    elif pointer == 1:
        rect.topleft = (block.left+20, block.top+80)
    cursor = pygame.Rect(rect.topright, (3, rect.height))

    if time.time() % 1 > 0.5:
        pygame.draw.rect(zone, color, cursor)

def key_data(event, text, img, pointer):
    if event.key == pygame.K_BACKSPACE:
        if len(text)>0:
            text = text[:-1]
    elif pygame.K_0 <= event.key <= pygame.K_9:
        text += event.unicode
    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
        pointer +=1
    img = font.render(text, True, BLACK)
    rect = img.get_rect()
    return text, img, pointer, rect
    
# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PySimSnide")

sysfont = pygame.font.get_default_font()
font_size = 24

# - objects -
block = pygame.rect.Rect(60, 40, 120, 80)
submenu_block = pygame.rect.Rect(20, 520, 210, 180)

blocks_list = []            #Lista de bloques existente 
line_list = []              #Lista de lineas existente
line_creation = 0           #Booleano (3 estados) para creación de una línea
srcLine = ("",0,(0,0))      #Tupla con datos de origen para línea
dstLine = ("",0,(0,0))      #Tupla con datos de destino para línea
only_one = False            #Booleano para impedir que más de un bloque puede efectuar una operación
enable_line_selection = False

# - test new stuff -

ed_text = False
text_size = 24
text_i = "# input ports:"
text_o = "# output ports:"
text_edi = "-"
text_edo = "-"

font = pygame.font.SysFont(None, text_size)

img_i = font.render(text_i, True, RED)
img_o = font.render(text_o, True, RED)
img_edi = font.render(text_edi, True, RED)
img_edo = font.render(text_edo, True, RED)

# - mainloop -

clock = pygame.time.Clock()
running = True

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and ed_text == False:
                if block.collidepoint(event.pos):               
                    val, block_id = assign_id(block_id) 
                    new_block = Block(val,(60, 40, 120, 80),1,1)
                    blocks_list.append(new_block)
                        
            elif event.button == 1:                
                for b_elem in blocks_list:
                    if b_elem.rectf.collidepoint(event.pos):
                        b_elem.selected = True
                        enable_line_selection = False
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

                b_sel = [x for x in blocks_list if x.selected == True]
                if len(b_sel) == 0:
                    enable_line_selection = True
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            for b_elem in blocks_list:
                if event.button == 1: 
                    b_elem.dragging = False
                    only_one = False
                    update_lines(blocks_list,line_list)

            if enable_line_selection == True:
                for line in line_list:
                    if event.button == 1:
                        if (line.collision(event.pos)):
                            line.selected = True
                        else:
                            line.selected = False

        elif event.type == pygame.MOUSEMOTION:
            for b_elem in blocks_list:
                if b_elem.dragging == True and only_one == True:
                    mouse_x, mouse_y = event.pos
                    b_elem.relocate_Block((mouse_x + offset_x,mouse_y + offset_y))

        elif event.type == pygame.KEYDOWN:
            #Eliminar un bloque y las líneas asociadas
            if ed_text == False and event.key == pygame.K_DELETE:
                b_del = [x for x in blocks_list if x.selected == True]
                if len(b_del) > 0:
                    l_del = [x for x in line_list if check_line_block(x,b_del)]
                    block_id = get_id_back(block_id,b_del)
                    line_id = get_id_back(line_id,l_del)
                    blocks_list = [x for x in blocks_list if not (x.selected == True)]
                    line_list = [x for x in line_list if not check_line_block(x,b_del)]
                else:
                    l_del = [x for x in line_list if x.selected == True]
                    line_id = get_id_back(line_id,l_del)
                    line_list = [x for x in line_list if x.selected == False]

            #Cambiar el número de puertos de un bloque (parte 2)       
            elif ed_text == True:
                if input_pointer == 0:
                    text_edi, img_edi, input_pointer, rectc = key_data(event, text_edi, img_edi, input_pointer)
                elif input_pointer == 1:
                    text_edo, img_edo, input_pointer, rectc = key_data(event, text_edo, img_edo, input_pointer)
                    if input_pointer == 2:
                        for b_elem in blocks_list:
                            if b_elem.name == b_text:
                                ed_text = False
                                input_pointer = 0
                                b_elem.change_number_ports(int(text_edi),int(text_edo))
                                line_list = [x for x in line_list if not check_line_port(x,b_elem)]

    #Ctrl + click para cambiar el número de puertos de un bloque (parte 1)
    if pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.mouse.get_pressed() == (1,0,0):
        for b_elem in blocks_list:
            if b_elem.rectf.collidepoint(event.pos) and ed_text == False:
                text_edi = str(b_elem.in_ports)
                text_edo = str(b_elem.out_ports)
                img_edi = font.render(text_edi, True, BLACK)
                img_edo = font.render(text_edo, True, BLACK)
                rectc = img_edi.get_rect()
                ed_text = True
                input_pointer = 0
                b_text = b_elem.name

    # - updates (without draws) -

    # empty

    # - draws (without updates) -
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, block)
    pygame.draw.line(screen, BLACK, [250, 0], [250, 720], 2)
    blockScreen(blocks_list,screen)
    print_lines(line_list)

    if ed_text == True:
        draw_textbox(screen,BLACK,submenu_block,rectc,input_pointer)

    ###########################################
    #FUNCION DISPLAY SUBMENU HERE
    ###########################################
    
    pygame.display.flip()

    # - constant game speed / FPS -
    clock.tick(FPS)

# - end -

pygame.quit()
