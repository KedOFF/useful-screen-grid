import pygame
import sys
import win32api
import win32con
import win32gui

# Получаем размеры экрана через WinAPI
SCREEN_WIDTH = win32api.GetSystemMetrics(0)
SCREEN_HEIGHT = win32api.GetSystemMetrics(1)

# Инициализация Pygame
pygame.init()

# Создаем окно без рамки
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Perfect Grid Overlay")

# Устанавливаем прозрачность
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | 
                       win32con.WS_EX_LAYERED | 
                       win32con.WS_EX_TRANSPARENT)

# Используем цветовой ключ для прозрачности (черный цвет будет прозрачным)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

# Настройки сетки
GRID_SIZE = 50  # Размер ячейки в пикселях
GRID_COLOR = (0, 255, 0)  # Ярко-зеленый цвет
CENTER_COLOR = (255, 0, 0)  # Ярко-красный для центра

# Рассчитываем смещение для идеальных линий
offset_x = (SCREEN_WIDTH % GRID_SIZE) // 2
offset_y = (SCREEN_HEIGHT % GRID_SIZE) // 2

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                GRID_SIZE = min(200, GRID_SIZE + 1)  # Увеличить сетку на 1
                # Пересчитываем смещение при изменении размера
                offset_x = (SCREEN_WIDTH % GRID_SIZE) // 2
                offset_y = (SCREEN_HEIGHT % GRID_SIZE) // 2
            elif event.key == pygame.K_MINUS:
                GRID_SIZE = max(1, GRID_SIZE - 1)  # Уменьшить сетку на 1
                # Пересчитываем смещение при изменении размера
                offset_x = (SCREEN_WIDTH % GRID_SIZE) // 2
                offset_y = (SCREEN_HEIGHT % GRID_SIZE) // 2
    
    # Очищаем экран черным цветом (который будет прозрачным)
    screen.fill((0, 0, 0))
    
    # Рисуем вертикальные линии
    for x in range(offset_x, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
    
    # Рисуем горизонтальные линии
    for y in range(offset_y, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
    
    # Центральные линии (толще и ярче)
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    pygame.draw.line(screen, CENTER_COLOR, (center_x, 0), (center_x, SCREEN_HEIGHT), 2)
    pygame.draw.line(screen, CENTER_COLOR, (0, center_y), (SCREEN_WIDTH, center_y), 2)
    
    # Показываем размер сетки в углу
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Grid: {GRID_SIZE}px (Press +/- to adjust)", True, (200, 200, 200))
    screen.blit(text, (10, SCREEN_HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()