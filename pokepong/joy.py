import pygame
def get_input(event):
    if event.type == pygame.JOYAXISMOTION:
        if event.axis == 0:
            if event.value >= 1:
                    return 'RIGHT'
            if event.value <= -1:
                    return 'LEFT'
        if event.axis == 1:
            if event.value >= 1:
                    return 'DOWN'
            if event.value <= -1:
                    return 'UP'
    if event.type == pygame.JOYBUTTONDOWN:
        if event.button == 0:
            return 'B'
        if event.button == 1:
            return 'A'
        if event.button == 6:
            return '2'
        if event.button == 7:
            return '3'
        if event.button == 8:
            return 'SELECT'
        if event.button == 9:
            return 'START'
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            return 'UP'
        if event.key == pygame.K_DOWN:
            return 'DOWN'
        if event.key == pygame.K_LEFT:
            return 'LEFT'
        if event.key == pygame.K_RIGHT:
            return 'RIGHT'
        if event.key == pygame.K_z:
            return 'A'
        if event.key == pygame.K_x:
            return 'B'
