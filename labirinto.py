import pygame
from pyamaze import maze
from tkinter import Tk, messagebox

# Inicializa o labirinto
rows, cols = 10, 10
labirinto = maze(rows, cols)
labirinto.CreateMaze()

# Configurações do pygame
pygame.init()
cell_size = 40  # Tamanho de cada célula no grid
screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
pygame.display.set_caption("Labirinto com Pygame")
clock = pygame.time.Clock()

# Posições inicial e final
agent_pos = (rows, cols)  # Começa no canto inferior direito
goal_pos = (1, 1)  # Meta no canto superior esquerdo

# Função para desenhar o labirinto
def draw_maze():
    screen.fill((0, 128, 0))  # Fundo verde
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            x, y = (c - 1) * cell_size, (r - 1) * cell_size
            cell = labirinto.maze_map[(r, c)]
            # Desenhar paredes
            if cell['E'] == 0:  # Sem abertura para o Leste
                pygame.draw.line(screen, (0, 0, 0), (x + cell_size, y), (x + cell_size, y + cell_size), 2)
            if cell['W'] == 0:  # Sem abertura para o Oeste
                pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + cell_size), 2)
            if cell['N'] == 0:  # Sem abertura para o Norte
                pygame.draw.line(screen, (0, 0, 0), (x, y), (x + cell_size, y), 2)
            if cell['S'] == 0:  # Sem abertura para o Sul
                pygame.draw.line(screen, (0, 0, 0), (x, y + cell_size), (x + cell_size, y + cell_size), 2)

# Função para desenhar um quadrado (agente ou objetivo)
def draw_square(pos, color):
    x, y = (pos[1] - 1) * cell_size, (pos[0] - 1) * cell_size
    padding = 5  # Distância do quadrado às bordas da célula
    pygame.draw.rect(
        screen,
        color,
        (x + padding, y + padding, cell_size - 2 * padding, cell_size - 2 * padding)
    )

# Função para verificar movimento válido
def is_valid_move(current_pos, direction):
    r, c = current_pos
    if direction == 'UP' and labirinto.maze_map[current_pos]['N']:
        return (r - 1, c)
    if direction == 'DOWN' and labirinto.maze_map[current_pos]['S']:
        return (r + 1, c)
    if direction == 'LEFT' and labirinto.maze_map[current_pos]['W']:
        return (r, c - 1)
    if direction == 'RIGHT' and labirinto.maze_map[current_pos]['E']:
        return (r, c + 1)
    return current_pos

# Função para verificar se o agente chegou ao objetivo
def check_victory(agent, goal):
    return agent == goal

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                agent_pos = is_valid_move(agent_pos, 'UP')
            elif event.key == pygame.K_DOWN:
                agent_pos = is_valid_move(agent_pos, 'DOWN')
            elif event.key == pygame.K_LEFT:
                agent_pos = is_valid_move(agent_pos, 'LEFT')
            elif event.key == pygame.K_RIGHT:
                agent_pos = is_valid_move(agent_pos, 'RIGHT')

    # Desenha o labirinto, agente e objetivo
    draw_maze()
    draw_square(agent_pos, (255, 0, 0))  # Quadrado vermelho para o agente
    draw_square(goal_pos, (0, 0, 255))  # Quadrado azul para o objetivo
    pygame.display.flip()

    # Verifica se o agente chegou ao objetivo
    if check_victory(agent_pos, goal_pos):
        pygame.quit()
        # Exibe o pop-up usando tkinter
        root = Tk()
        root.withdraw()  # Oculta a janela principal
        messagebox.showinfo("Parabéns!", "Você venceu o jogo!")
        root.destroy()
        break

    clock.tick(30)

pygame.quit()
  
