import pygame
KILL = []
def get_input(event):
    global KILL
    KILL = KILL[-10:]
    if KILL == ['L','L','L','R','R','R','B','B','B','S']:
        pygame.quit()
    if event.type == pygame.JOYAXISMOTION:
        if event.axis == 0:
            if event.value >= 1:
                KILL.append('R')
                return 'RIGHT'
            if event.value <= -1:
                KILL.append('L')
                return 'LEFT'
        if event.axis == 1:
            if event.value >= 1:
                KILL = []
                return 'DOWN'
            if event.value <= -1:
                KILL = []
                return 'UP'
    if event.type == pygame.JOYBUTTONDOWN:
        if event.button == 0:
            KILL.append('B')
            return 'B'
        if event.button == 1:
            KILL = []
            return 'A'
        if event.button == 6:
            return '2'
        if event.button == 7:
            return '3'
        if event.button == 8:
            return 'SELECT'
        if event.button == 9:
            KILL.append('S')
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
        if event.key == pygame.K_c:
            return 'START'
