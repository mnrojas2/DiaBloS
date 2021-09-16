import pygame
import numpy as np
import time

class InitSim:
    def __init__(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.FPS = 60

        self.block_id = [0, 1, 2, 3, 4]
        self.line_id = [0, 1, 2, 3, 4]

        self.blocks_list = []  # Lista de bloques existente
        self.line_list = []  # Lista de lineas existente

    def assign_block_id(self):
        # asignacion de id a partir de una lista de valores disponibles
        sid = self.block_id[0]
        self.block_id = self.block_id[1:]
        self.block_id.append(self.block_id[-1] + 1)
        return sid

    def assign_line_id(self):
        # asignacion de id a partir de una lista de valores disponibles
        sid = self.line_id[0]
        self.line_id = self.line_id[1:]
        self.line_id.append(self.line_id[-1] + 1)
        return sid

    def remove_block(self, del_list):
        # recuperacion de un id liberado por un elemento eliminado
        for id_elem in del_list:
            self.block_id.append(id_elem.sid)
        self.block_id.sort()
        if len(self.block_id) > self.block_id[-1] + 1:
            self.block_id = self.block_id[:self.block_id[-1]]
        elif len(self.block_id) == self.block_id[-1] + 1:
            self.block_id = self.block_id[:5]
        # eliminacion de los bloques de la lista
        self.blocks_list = [x for x in self.blocks_list if not (x.selected == True)]

    def get_line_id_back(self, del_list):
        # recuperacion de un id liberado por un elemento eliminado
        for id_elem in del_list:
            self.line_id.append(id_elem.sid)
        self.line_id.sort()
        if len(self.line_id) > self.line_id[-1] + 1:
            self.line_id = self.line_id[:self.line_id[-1]]
        elif len(self.line_id) == self.line_id[-1] + 1:
            self.line_id = self.line_id[:5]

    def print_lines(self, zone):
        # Dibuja las líneas a partir de una lista
        for line in self.line_list:
            line.draw_line(zone)

    def update_lines(self):
        # Actualiza la ubicación de las líneas a partir de la ubicación de los bloques
        for line in self.line_list:
            line.update_line(self.blocks_list)

    def blockScreen(self, zone):
        # Dibuja los bloques incluyendo al seleccionado
        for b_elem in self.blocks_list:
            if b_elem.selected == True:
                b_elem.draw_selected(zone)
            b_elem.draw_Block(zone)
            zone.blit(b_elem.text_display, (b_elem.left + 20, b_elem.top + 5))

    def port_availability(self, dst_line):
        # Comprueba si es que el puerto a conectar está libre para ello
        for line in self.line_list:
            if line.dstblock == dst_line[0] and line.dstport == dst_line[1]:
                return False
        return True


class Block(InitSim):
    def __init__(self, sid, coords, in_ports=1, out_ports=1, font_size=24):
        super().__init__()
        self.name = "Block" + str(sid)  # Nombre del bloque
        self.sid = sid  # id del bloque
        self.left = coords[0]  # Coordenada ubicación línea izquierda
        self.top = coords[1]  # Coordenada ubicación línea superior
        self.width = coords[2]  # Ancho bloque
        self.height = coords[3]  # Altura bloque

        self.port_radius = 10  # Radio circulo puertos
        self.height_base = self.height  # Variable que conserva valor de altura por defecto
        self.in_ports = in_ports  # Variable que contiene el número de puertos de entrada
        self.out_ports = out_ports  # Variable que contiene el número de puertos de salida

        self.in_coords = []  # Lista que contiene coordenadas para cada puerto de entrada
        self.out_coords = []  # Lista que contiene coordenadas para cada puerto de salida
        self.place_ports()  # Función que ubica las coordenadas de los puertos

        self.rectf = pygame.rect.Rect(self.left - self.port_radius, self.top, self.width + 2 * self.port_radius,
                                      self.height)  # Rect que define la colisión del bloque
        self.dragging = False  # Booleano para determinar si el bloque se está moviendo
        self.selected = False  # Booleano para determinar si el bloque está seleccionado en el plano

        self.text = pygame.font.SysFont(None, font_size)
        self.text_display = self.text.render(self.name, True, self.RED)

    def draw_Block(self, place):
        # Dibuja el bloque y los puertos
        pygame.draw.rect(place, self.GREEN, (self.left, self.top, self.width, self.height))
        for port_in_location in self.in_coords:
            pygame.draw.circle(place, self.RED, port_in_location, self.port_radius)

        for port_out_location in self.out_coords:
            pygame.draw.circle(place, self.RED, port_out_location, self.port_radius)

    def update_Block(self):
        # Actualiza ubicación y dimensiones del bloque y número de puertos
        self.rectf.update((self.left - self.port_radius, self.top, self.width + 2 * self.port_radius, self.height))
        self.place_ports()

    def place_ports(self):
        # Función que ubica las coordenadas de los puertos
        self.in_coords = []
        self.out_coords = []

        # En caso que el número de puertos sea muy grande, se redimensiona el bloque
        port_height = max(self.out_ports, self.in_ports) * self.port_radius * 2
        if port_height > self.height:
            self.height = port_height + 10
        elif port_height < self.height_base:
            self.height = self.height_base

        # Se ubican los puertos de forma simétrica en ambos lados
        if self.in_ports > 0:
            for i in range(self.in_ports):
                port_in = (self.left, self.top + self.height * (i + 1) / (self.in_ports + 1))
                self.in_coords.append(port_in)
        if self.out_ports > 0:
            for j in range(self.out_ports):
                port_out = (self.left + self.width, self.top + self.height * (j + 1) / (self.out_ports + 1))
                self.out_coords.append(port_out)

    def relocate_Block(self, new_coords):  # new_coords = (left,top)
        # Función simple para reubicar el bloque en el plano, requiere coordenadas de la esquina superior izquierda
        self.left = new_coords[0]
        self.top = new_coords[1]
        self.update_Block()

    def resize_Block(self, new_coords):  # new_dims = (width,height)
        # Función simple para redimensionar el bloque en el plano, requiere ancho y altura ingresado como tupla
        self.width = new_coords[0]
        self.height = new_coords[1]
        self.update_Block()

    def port_collision(self, m_coords):
        # Observa si el mouse toca alguno de los puertos de un bloque. Retorna una tupla con el tipo de puerto y su id.
        for i in range(len(self.in_coords)):
            p_coords = self.in_coords[i]
            distance = np.sqrt((m_coords[0] - p_coords[0]) ** 2 + (m_coords[1] - p_coords[1]) ** 2)
            if distance <= self.port_radius:
                return ("i", i)
        for j in range(len(self.out_coords)):
            p_coords = self.out_coords[j]
            distance = np.sqrt((m_coords[0] - p_coords[0]) ** 2 + (m_coords[1] - p_coords[1]) ** 2)
            if distance <= self.port_radius:
                return ("o", j)
        return (-1, -1)

    def draw_selected(self, zone):
        # Dibuja linea de selección en torno a un bloque.
        # XHACER: ancho linea y espacio que cambiar por algo definido en clase default.
        l_width = 5  # ancho linea
        ls_width = 5  # ancho separacion linea-bloque
        pygame.draw.line(zone, self.BLACK, (self.left - ls_width, self.top - ls_width),
                         (self.left + self.width + ls_width, self.top - ls_width), l_width)
        pygame.draw.line(zone, self.BLACK, (self.left - ls_width, self.top - ls_width),
                         (self.left - ls_width, self.top + self.height + ls_width), l_width)
        pygame.draw.line(zone, self.BLACK, (self.left + self.width + ls_width, self.top + self.height + ls_width),
                         (self.left + self.width + 5, self.top - ls_width), l_width)
        pygame.draw.line(zone, self.BLACK, (self.left + self.width + ls_width, self.top + self.height + ls_width),
                         (self.left - ls_width, self.top + self.height + ls_width), l_width)

    def change_number_ports(self, port_i, port_o):
        # Cambia el número de puertos de un bloque, con inputs desde el shell.
        # port_o = int(input("Numero puertos output: "))
        self.in_ports = port_i
        self.out_ports = port_o
        self.place_ports()


class Line(InitSim):
    def __init__(self, sid, srcblock, srcport, points, dstblock, dstport, zorder):
        super().__init__()
        self.name = "Line" + str(sid)  # Nombre de la línea
        self.sid = sid  # id de la línea
        self.srcblock = srcblock  # Nombre del bloque de origen
        self.srcport = srcport  # ID del puerto de origen del bloque
        self.points = points  # puntos de vertice para la línea(?) ((a,b),(c,d),(e,f),...)
        self.dstblock = dstblock  # Nombre del bloque de origen
        self.dstport = dstport  # ID del puerto de origen del bloque
        self.zorder = zorder  # ID de prioridad al momento de dibujar el bloque
        self.selected = False

    def draw_line(self,zone):
        # Dibuja la línea con los datos del init
        for i in range(len(self.points) - 1):
            if self.selected == True:
                line_width = 5
            else:
                line_width = 2
            pygame.draw.line(zone, self.BLACK, self.points[i], self.points[i + 1], line_width)

    def update_line(self, block_list):
        # Actualiza el valor de la línea según la ubicación y tamaño del bloque
        for block in block_list:
            if block.name == self.srcblock:
                startline = block.out_coords[self.srcport]
            if block.name == self.dstblock:
                endline = block.in_coords[self.dstport]
        self.points = (startline, endline)

    def collision(self, m_coords):
        min_dst = 10
        line_A = np.array(self.points[0])
        line_B = np.array(self.points[1])
        m_coords = np.array(m_coords)

        if all(line_A == m_coords) or all(line_B == m_coords):
            distance_to_line = 0.0
        elif np.arccos(np.dot((m_coords - line_A) / np.linalg.norm(m_coords - line_A),
                              (line_B - line_A) / np.linalg.norm(line_B - line_A))) > np.pi / 2:
            distance_to_line = np.linalg.norm(m_coords - line_A)
        elif np.arccos(np.dot((m_coords - line_B) / np.linalg.norm(m_coords - line_B),
                              (line_A - line_B) / np.linalg.norm(line_A - line_B))) > np.pi / 2:
            distance_to_line = np.linalg.norm(m_coords - line_B)
        else:
            distance_to_line = np.linalg.norm(np.cross(line_A - line_B, line_A - m_coords)) / np.linalg.norm(
                line_B - line_A)

        if distance_to_line > min_dst:
            return False
        else:
            return True

    def __str__(self):
        # Imprime en el shell, el nombre de la línea y su origen y destino
        return self.name + ": From " + str(self.srcblock) + ", port " + str(self.srcport) + " to " + str(
            self.dstblock) + ", port " + str(self.dstport)


# --- functions --- (lower_case names)
def check_line_block(line, b_delete_list):
    # Comprueba si es que hay lineas a bloques recientemente eliminados
    for b_del in b_delete_list:
        if line.srcblock == b_del.name or line.dstblock == b_del.name:
            return True
        else:
            return False


def check_line_port(line, block):
    # Comprueba si es que hay lineas a puertos recientemente eliminados
    if line.srcblock == block.name and line.srcport > block.out_ports - 1:
        return True
    elif line.dstblock == block.name and line.dstport > block.in_ports - 1:
        return True
    else:
        return False


def draw_textbox(zone, color, font_t, block, img_edi, img_edo, rect, pointer):
    pygame.draw.rect(zone, color, block, width=2)

    text_i = "# input ports:"
    text_o = "# output ports:"
    img_i = font_t.render(text_i, True, color)
    img_o = font_t.render(text_o, True, color)

    zone.blit(img_i, (block.left + 20, block.top + 20))
    zone.blit(img_o, (block.left + 20, block.top + 60))

    zone.blit(img_edi, (block.left + 20, block.top + 40))
    zone.blit(img_edo, (block.left + 20, block.top + 80))

    if pointer == 0:
        rect.topleft = (block.left + 20, block.top + 40)
    elif pointer == 1:
        rect.topleft = (block.left + 20, block.top + 80)
    cursor = pygame.Rect(rect.topright, (3, rect.height))

    if time.time() % 1 > 0.5:
        pygame.draw.rect(zone, color, cursor)


def key_data(event, color, text, font, pointer):
    if event.key == pygame.K_BACKSPACE:
        if len(text) > 0:
            text = text[:-1]
    elif pygame.K_0 <= event.key <= pygame.K_9:
        text += event.unicode
    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
        pointer += 1
    img = font.render(text, True, color)
    rect = img.get_rect()
    return text, img, pointer, rect