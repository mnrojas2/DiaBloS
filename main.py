from classes import *

# --- constants --- (UPPER_CASE names)
sim_init = InitSim()

# - init -

pygame.init()

screen = pygame.display.set_mode((sim_init.SCREEN_WIDTH, sim_init.SCREEN_HEIGHT))
pygame.display.set_caption("PySimSnide")
sub_test = SubMenu()

# - objects -
base_block_coords = (60, 40, 120, 80)
block = pygame.rect.Rect(base_block_coords)

base_submenu_block_coords = (20, 520, 210, 180)
submenu_block = pygame.rect.Rect(base_submenu_block_coords)

line_creation = 0  # Booleano (3 estados) para creación de una línea
srcLine = ("", 0, (0, 0))  # Tupla con datos de origen para línea
dstLine = ("", 0, (0, 0))  # Tupla con datos de destino para línea
only_one = False  # Booleano para impedir que más de un bloque puede efectuar una operación
enable_line_selection = False

# - mainloop -

clock = pygame.time.Clock()
running = True

while running:

    # - events -
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and sub_test.enabled == False:#ed_text == False:
                if block.collidepoint(event.pos):
                    sim_init.add_block(block)

            elif event.button == 1:
                for b_elem in sim_init.blocks_list:
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
                            dstLine = (b_elem.name, p_col[1], b_elem.in_coords[p_col[1]])  # block name, port number, port location
                            if sim_init.port_availability(dstLine) == True:
                                if line_creation == 0:
                                    line_creation = 2
                                elif line_creation == 1:
                                    sim_init.add_line(srcLine, dstLine, 1)
                                    line_creation = 0

                        elif p_col[0] == 'o':
                            srcLine = (b_elem.name, p_col[1], b_elem.out_coords[p_col[1]])  # block name, port number, port location
                            if line_creation == 0:
                                line_creation = 1
                            elif line_creation == 2:
                                sim_init.add_line(srcLine, dstLine, 1)
                                line_creation = 0
                    else:
                        b_elem.selected = False

                b_sel = [x for x in sim_init.blocks_list if x.selected == True]
                if len(b_sel) == 0:
                    enable_line_selection = True

        elif event.type == pygame.MOUSEBUTTONUP:
            for b_elem in sim_init.blocks_list:
                if event.button == 1:
                    b_elem.dragging = False
                    only_one = False
                    sim_init.update_lines()

            if enable_line_selection == True:
                for line in sim_init.line_list:
                    if event.button == 1:
                        if (line.collision(event.pos)):
                            line.selected = True
                        else:
                            line.selected = False

        elif event.type == pygame.MOUSEMOTION:
            for b_elem in sim_init.blocks_list:
                if b_elem.dragging == True and only_one == True:
                    mouse_x, mouse_y = event.pos
                    b_elem.relocate_Block((mouse_x + offset_x, mouse_y + offset_y))

        elif event.type == pygame.KEYDOWN:
            # Eliminar un bloque y las líneas asociadas
            if sub_test.enabled == False and event.key == pygame.K_DELETE:
                b_del = [x for x in sim_init.blocks_list if x.selected == True]
                sim_init.remove_block(b_del)
                if len(b_del) > 0:
                    l_del = [x for x in sim_init.line_list if check_line_block(x, b_del)]
                    sim_init.get_line_id_back(l_del)
                    sim_init.line_list = [x for x in sim_init.line_list if not check_line_block(x, b_del)]
                else:
                    l_del = [x for x in sim_init.line_list if x.selected == True]
                    sim_init.get_line_id_back(l_del)
                    sim_init.line_list = [x for x in sim_init.line_list if x.selected == False]

            # Cambiar el número de puertos de un bloque (parte 2)
            elif sub_test.enabled == True:
                if sub_test.pointer == 0:
                    sub_test.key_data(event)
                elif sub_test.pointer == 1:
                    sub_test.key_data(event)
                    if sub_test.pointer == 2:
                        for b_elem in sim_init.blocks_list:
                            if b_elem.name == sub_test.ref_block:
                                b_elem.change_number_ports(int(sub_test.p1_value), int(sub_test.p2_value))
                                sim_init.line_list = [x for x in sim_init.line_list if not check_line_port(x, b_elem)]
                                sub_test.reset()

    # Ctrl + click para cambiar el número de puertos de un bloque (parte 1)
    if pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.mouse.get_pressed() == (1, 0, 0):
        for b_elem in sim_init.blocks_list:
            if b_elem.rectf.collidepoint(event.pos) and sub_test.enabled == False:
                sub_test.initial(b_elem.name,"i/o",[str(b_elem.in_ports),str(b_elem.out_ports)])

    # - updates (without draws) -

    # empty

    # - draws (without updates) -
    screen.fill(sim_init.WHITE)
    pygame.draw.rect(screen, sim_init.GREEN, block)
    pygame.draw.line(screen, sim_init.BLACK, [250, 0], [250, 720], 2)
    sim_init.blockScreen(screen)
    sim_init.print_lines(screen)

    if sub_test.enabled == True:
        sub_test.draw_SubMenu(screen)

    pygame.display.flip()

    # - constant game speed / FPS -
    clock.tick(sim_init.FPS)

# - end -

pygame.quit()
