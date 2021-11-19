import pygame

from classes import *

# --- constants --- (UPPER_CASE names)
sim_init = InitSim()

# - init -

pygame.init()

# Se inicializa la ventana
screen = pygame.display.set_mode((sim_init.SCREEN_WIDTH, sim_init.SCREEN_HEIGHT))
pygame.display.set_caption("PySimSnide")

# - objects -

# Se inicializan los bloques base
sim_init.base_blocks_init()

# - mainloop -

clock = pygame.time.Clock()
running = True

while running:

    # - events -
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # Se termina la simulación
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Agregar bloque
            if event.button == 3 and sim_init.holding_CTRL == False:
                for block in sim_init.base_blocks:
                    if block.collision.collidepoint(event.pos):
                        sim_init.add_block(block, event.pos)


            elif event.button == 1 and sim_init.holding_CTRL == False:
                for b_elem in sim_init.blocks_list:
                    if b_elem.rectf.collidepoint(event.pos):
                        b_elem.selected = True
                        sim_init.enable_line_selection = False
                        p_col = b_elem.port_collision(event.pos)

                        # Mover bloque
                        if p_col[0] == -1 and sim_init.only_one == False:
                            b_elem.dragging = True
                            sim_init.only_one = True
                            mouse_x, mouse_y = event.pos
                            offset_x = b_elem.left - mouse_x
                            offset_y = b_elem.top - mouse_y

                        # Conectar puerto entrada bloque
                        elif p_col[0] == 'i':
                            dstLine = (b_elem.name, p_col[1], b_elem.in_coords[p_col[1]])  # block name, port number, port location
                            if sim_init.port_availability(dstLine) == True:
                                if sim_init.line_creation == 0:
                                    sim_init.line_creation = 2
                                elif sim_init.line_creation == 1:
                                    sim_init.add_line(srcLine, dstLine)
                                    sim_init.line_creation = 0

                        #Conectar puerto salida bloque
                        elif p_col[0] == 'o':
                            srcLine = (b_elem.name, p_col[1], b_elem.out_coords[p_col[1]])  # block name, port number, port location
                            if sim_init.line_creation == 0:
                                sim_init.line_creation = 1
                            elif sim_init.line_creation == 2:
                                sim_init.add_line(srcLine, dstLine)
                                sim_init.line_creation = 0
                    else:
                        b_elem.selected = False

                # Se determina si algún bloque ha sido seleccionado en la pantalla
                b_sel = [x for x in sim_init.blocks_list if x.selected == True]
                if len(b_sel) == 0:
                    sim_init.enable_line_selection = True

            # Ctrl + click derecho para cambiar el número de puertos de un bloque
            elif event.button == 3 and sim_init.holding_CTRL == True:
                for b_elem in sim_init.blocks_list:
                    if b_elem.rectf.collidepoint(event.pos):
                        b_elem.change_port_numbers()
                        #sim_init.line_list = [x for x in sim_init.line_list if not sim_init.check_line_port(x, b_elem)]
                        sim_init.line_list = [x for x in sim_init.line_list if not sim_init.check_line_port(x, b_elem)]

            # Ctrl + click izquierdo para cambiar los parametros de un bloque
            elif event.button == 1 and sim_init.holding_CTRL == True:
                for b_elem in sim_init.blocks_list:
                    if b_elem.rectf.collidepoint(event.pos):
                        b_elem.change_params()

        elif event.type == pygame.MOUSEBUTTONUP:
            # Se deja de mover un bloque y se actualizan las lineas conectadas a sus puertos
            for b_elem in sim_init.blocks_list:
                if event.button == 1:
                    b_elem.dragging = False
                    sim_init.only_one = False
                    sim_init.update_lines()

            # Se observa si alguna linea se ha seleccionado
            if sim_init.enable_line_selection == True:
                for line in sim_init.line_list:
                    if event.button == 1:
                        if (line.collision(event.pos)):
                            line.selected = True
                        else:
                            line.selected = False

        elif event.type == pygame.MOUSEMOTION:
            # Se mueve un bloque si es que está seleccionado
            for b_elem in sim_init.blocks_list:
                if b_elem.dragging == True and sim_init.only_one == True:
                    mouse_x, mouse_y = event.pos
                    b_elem.relocate_Block((mouse_x + offset_x, mouse_y + offset_y))

        elif event.type == pygame.KEYDOWN:
            # Eliminar un bloque y las líneas asociadas
            if event.key == pygame.K_DELETE:
                sim_init.remove_block_and_lines()

            # Indicar si es que la tecla Control está presionada
            elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                sim_init.holding_CTRL = True

            elif sim_init.holding_CTRL == True:
                # Ctrl + G para guardar los bloques en un archivo
                if event.key == pygame.K_g:
                    sim_init.save()

                # Ctrl + A para cargar los bloques desde un archivo
                elif event.key == pygame.K_a:
                    sim_init.open()

                # Limpiar la pantalla de bloques para iniciar de nuevo
                elif event.key == pygame.K_n:
                    sim_init.clear_all()

                # Iniciar la ejecución de datos asociados a los bloques
                elif event.key == pygame.K_e:
                    sim_init.execution_init()

        elif event.type == pygame.KEYUP:
            # Indicar que la tecla Control se dejó de presionar
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                sim_init.holding_CTRL = False

    # - updates (without draws) -

    # - draws (without updates) -
    screen.fill(sim_init.colors['white'])

    sim_init.draw_base_blocks(screen)           # Se dibujan los bloques base
    sim_init.blockScreen(screen)                # Se dibujan los bloques de ejecución
    sim_init.print_lines(screen)                # Se dibujan las lineas

    if sim_init.run_initialized == True:        # Si es que ya se corrió la primera iteración, iniciar el loop.
        sim_init.execution_loop()

    pygame.display.flip()

    # - constant game speed / FPS -
    clock.tick(sim_init.FPS)

# - end -

pygame.quit()

print("Sim done =D")
