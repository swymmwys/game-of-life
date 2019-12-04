import sys
import pygame
import math
import time
from game_field import GameField

def main():
    play = False
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Game Of Life")
    rect = screen.get_rect()
    cells_surface = pygame.Surface(screen.get_size())
    grid_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    bg_color = (230, 230, 230)
    cell_color = (0, 0, 0)
    cells_surface.fill(bg_color) 
    game_field = GameField(50)
    lines = game_field.size + 1
    cell_size = min(rect.height, rect.width) / game_field.size
    line_width = 1
    inner_cell_size = cell_size - line_width
    line_color = (200, 200, 200)
    
    def update_screen():
        screen.blit(cells_surface, (0, 0))
        screen.blit(grid_surface, (0, 0))
        
    def draw_rect(x, y, color):
        pygame.draw.rect(
            cells_surface, 
            color, 
            pygame.Rect(
                int(x * cell_size + line_width),
                int(y * cell_size + line_width),
                int(inner_cell_size), 
                int(inner_cell_size)
            )
        )
        
        return not cell
        
    def init_grid(lines):
        for i in range(lines):
            step = int(i * cell_size)
            pygame.draw.line(grid_surface, line_color, (0, step), (rect.width, step), line_width)
            pygame.draw.line(grid_surface, line_color, (step, 0), (step, rect.height), line_width)
    
    init_grid(lines)
    update_screen()
    
    while True:
        if play:
            game_field.update()
            cells_surface.fill(bg_color)
            
            if len(game_field.live_cells) == 0:
                play = False
                update_screen()
                continue
            
            for cell in game_field.live_cells:
                draw_rect(cell.x, cell.y, cell_color)
            
            update_screen()
            time.sleep(.1)          
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                play = not play
                
            
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                play = False
                game_field.reset()
                cells_surface.fill(bg_color)
                update_screen()
                
            if event.type == pygame.MOUSEBUTTONUP and not play:
                pos = event.pos
                x_cell = int(pos[0] / cell_size)
                y_cell = int(pos[1] / cell_size)

                cell = game_field.get_cell_at(x_cell, y_cell)
                color = cell_color if cell == None else bg_color
                
                if cell == None:
                    game_field.add_cell_at(x_cell, y_cell)
                else:
                    game_field.remove_cell_at(x_cell, y_cell)
                
                draw_rect(x_cell, y_cell, color)
                update_screen()    
                     
        pygame.display.flip()

###        
main()
