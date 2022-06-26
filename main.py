"""
main.py - Module to run the simulator interface
"""

import pygame
import sys
sys.path.append('./lib/')
from lib import *

def main_execution():
    """
    Function that manages keyboard and mouse inputs, block positions and line connections. It's focused on the user-interface.
    """

    pygame.init()
    sim_init = InitSim()

    # Window Initialization
    screen = pygame.display.set_mode((sim_init.SCREEN_WIDTH, sim_init.SCREEN_HEIGHT))
    pygame.display.set_caption("PySimGraph")

    # Menu block and UI buttons initialization
    sim_init.menu_blocks_init()
    sim_init.main_buttons_init()

    # Button identification
    new_b = sim_init.buttons_list[0]
    load_b = sim_init.buttons_list[1]
    save_b = sim_init.buttons_list[2]
    sim_b = sim_init.buttons_list[3]
    pp_b = sim_init.buttons_list[4]
    st_b = sim_init.buttons_list[5]
    sh_sc = sim_init.buttons_list[6]


    # - mainloop -
    clock = pygame.time.Clock()
    running = True

    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # Simulation end
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and sim_init.holding_CTRL == False:
                    # Press UI button
                    for button in sim_init.buttons_list:
                        if button.collision.collidepoint(event.pos):
                            button.pressed = True

                    # Add block
                    for block in sim_init.menu_blocks:
                        if block.collision.collidepoint(event.pos):
                            sim_init.add_block(block, event.pos)

                    # Select block
                    for b_elem in sim_init.blocks_list[::-1]:
                        if b_elem.rectf.collidepoint(event.pos) and sim_init.only_one == False:
                            b_elem.selected = True
                            sim_init.only_one = True
                            sim_init.enable_line_selection = False
                            p_col = b_elem.port_collision(event.pos)

                            # Move block
                            if p_col[0] == -1:
                                b_elem.dragging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = b_elem.left - mouse_x
                                offset_y = b_elem.top - mouse_y

                            # Connect input port
                            elif p_col[0] == 'i':
                                dstLine = (b_elem.name, p_col[1], b_elem.in_coords[p_col[1]])  # block name, port number, port location
                                if sim_init.port_availability(dstLine) == True:
                                    if sim_init.line_creation == 0:
                                        sim_init.line_creation = 2
                                    elif sim_init.line_creation == 1:
                                        sim_init.add_line(srcLine, dstLine)
                                        sim_init.line_creation = 0

                            #Connect output port
                            elif p_col[0] == 'o':
                                srcLine = (b_elem.name, p_col[1], b_elem.out_coords[p_col[1]])  # block name, port number, port location
                                if sim_init.line_creation == 0:
                                    sim_init.line_creation = 1
                                elif sim_init.line_creation == 2:
                                    sim_init.add_line(srcLine, dstLine)
                                    sim_init.line_creation = 0
                        else:
                            b_elem.selected = False

                    # Check if a block has been clicked/selected
                    b_sel = [x for x in sim_init.blocks_list if x.selected == True]
                    if len(b_sel) == 0:
                        sim_init.enable_line_selection = True

                # Right click to change parameters or input/output port numbers (if applicable)
                elif event.button == 3:
                    # Change internal parameters
                    if sim_init.holding_CTRL == False:
                        for b_elem in sim_init.blocks_list:
                            if b_elem.rectf.collidepoint(event.pos):
                                b_elem.change_params()
                                b_elem.load_external_data()
                                sim_init.line_list = [x for x in sim_init.line_list if not sim_init.check_line_port(x, b_elem)]

                    # Change input/outputs
                    elif sim_init.holding_CTRL == True:
                        for b_elem in sim_init.blocks_list:
                            if b_elem.rectf.collidepoint(event.pos):
                                b_elem.change_port_numbers()
                                sim_init.line_list = [x for x in sim_init.line_list if not sim_init.check_line_port(x, b_elem)]

            # UI button functionality
            elif event.type == pygame.MOUSEBUTTONUP:
                # New page (delete all)
                if new_b.collision.collidepoint(event.pos) and new_b.active == True:
                    new_b.pressed = False
                    sim_init.clear_all()
                # Load saved file
                elif load_b.collision.collidepoint(event.pos) and load_b.active == True:
                    load_b.pressed = False
                    sim_init.open()
                # Save file
                elif save_b.collision.collidepoint(event.pos) and save_b.active == True:
                    save_b.pressed = False
                    sim_init.save()
                # Start graph simulation
                elif sim_b.collision.collidepoint(event.pos) and sim_b.active == True:
                    sim_b.pressed = False
                    sim_init.execution_init()
                # Pause graph simulation
                elif pp_b.collision.collidepoint(event.pos) and pp_b.active == True:
                    if sim_init.execution_pause == True:
                        sim_init.execution_pause = False
                        pp_b.pressed = False
                        print("EXECUTION: PLAY")
                    elif sim_init.execution_pause == False:
                        sim_init.execution_pause = True
                        print("\nEXECUTION: PAUSED")
                # Stop graph simulation
                elif st_b.collision.collidepoint(event.pos) and st_b.active == True:
                    st_b.pressed = False
                    sim_init.execution_stop = True
                # Plot graph simulation (if enabled)
                elif sh_sc.collision.collidepoint(event.pos) and sh_sc.active == True:
                    sh_sc.pressed = False
                    sim_init.plot_again()


                # Update lines after a block was moved
                for b_elem in sim_init.blocks_list:
                    if event.button == 1:
                        if b_elem.left < sim_init.canvas_left_limit or b_elem.top < sim_init.canvas_top_limit:
                            sim_init.remove_block_and_lines()
                        else:
                            b_elem.dragging = False
                        sim_init.only_one = False
                        sim_init.update_lines()

                # Check if line has been selected
                if sim_init.enable_line_selection == True:
                    for line in sim_init.line_list:
                        if event.button == 1:
                            if (line.collision(event.pos)):
                                line.selected = True
                            else:
                                line.selected = False

            elif event.type == pygame.MOUSEMOTION:
                # Move block if selected
                for b_elem in sim_init.blocks_list:
                    if b_elem.dragging == True and sim_init.only_one == True:
                        mouse_x, mouse_y = event.pos
                        b_elem.relocate_Block((mouse_x + offset_x, mouse_y + offset_y))

            elif event.type == pygame.KEYDOWN:
                # Delete block if it is selected
                if event.key == pygame.K_DELETE:
                    sim_init.remove_block_and_lines()

                # Check if CTRL key is pressed (in keyboard)
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    sim_init.holding_CTRL = True

                # Special commands for CTRL shortcuts
                elif sim_init.holding_CTRL == True:
                    # Save file
                    if event.key == pygame.K_s:
                        sim_init.save()

                    # Load file
                    elif event.key == pygame.K_a:
                        sim_init.open()

                    # Clear canvas (New)
                    elif event.key == pygame.K_n:
                        sim_init.clear_all()

                    # Start graph simulation
                    elif event.key == pygame.K_e:
                        sim_init.execution_init()

            elif event.type == pygame.KEYUP:
                # Check if CTRL key is not pressed anymore
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    sim_init.holding_CTRL = False

                # Change line color if selected
                elif event.key == pygame.K_UP:
                    for line in sim_init.line_list:
                        if line.selected == True:
                            line.change_color(1)

                # Change line color if selected
                elif event.key == pygame.K_DOWN:
                    for line in sim_init.line_list:
                        if line.selected == True:
                            line.change_color(-1)

        # Display in interface
        screen.fill(sim_init.colors['white'])

        sim_init.display_menu_blocks(screen)       # Display block menu
        sim_init.display_buttons(screen)           # Display buttons
        sim_init.display_blocks(screen)            # Display blocks
        sim_init.display_lines(screen)             # Display lines

        # Continue graph simulation if execution was initialized
        if sim_init.execution_initialized == True:
            sim_init.execution_loop()

        pygame.display.flip()
        clock.tick(sim_init.FPS)

    # Close interface
    pygame.quit()
    print("Sim done =D")

if __name__ == "__main__":
    main_execution()
