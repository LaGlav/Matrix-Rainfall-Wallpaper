import pygame
import random
import cv2
import numpy as np
from datetime import datetime

# Initialize Pygame
pygame.init()

# Get system resolution
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Set colors
background_color = (0, 0, 0)
matrix_green = (200, 20, )
matrix_dark_green = (0, 50, 0)

# Set character properties
font_size = 25
column_width = width // font_size
rows = height // font_size
max_char_speed = 1

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Matrix Rain Wallpaper')
clock = pygame.time.Clock()

# Use the Consolas font
font = pygame.font.Font('consolas.ttf', font_size)

class RainDrop:
    def __init__(self, x, y, depth):
        self.x = x
        self.y = y
        self.depth = depth
        self.char = chr(random.randint(33, 126))

    def draw(self, surface):
        green_brightness = int(255 * (1 - self.depth))
        color = (0, green_brightness, 0)
        char_surface = font.render(self.char, True, color)
        surface.blit(char_surface, (self.x * font_size, self.y * font_size))

class Trail:
    def __init__(self, x, depth):
        self.x = x
        self.depth = depth
        self.speed = random.uniform(0.5, max_char_speed) * depth
        self.raindrops = [RainDrop(x, i - random.randint(10, 20), depth) for i in range(rows)]

    def update(self):
        for drop in self.raindrops:
            drop.y += self.speed
            drop.char = chr(random.randint(33, 126))
            if drop.y >= rows:
                drop.y = random.randint(-rows // 2, 0)

                # Check if it's the last raindrop in the trail
                if drop == self.raindrops[-1]:
                    self.x = random.randint(0, column_width - 1)
                    for d in self.raindrops:
                        d.x = self.x

    def draw(self, surface):
        for drop in self.raindrops:
            drop.draw(surface)


def toggle_fullscreen():
    """Toggle fullscreen mode."""
    screen = pygame.display.get_surface()
    if not screen:
        return
    is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
    if is_fullscreen:
        screen = pygame.display.set_mode((width, height))
    else:
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Create trails
trails = [Trail(random.randint(0, column_width - 1), random.uniform(0.2, 1)) for _ in range(column_width * 2)]

# Video related variables
is_recording = False
video_writer = None

# HUD related variables
hud_visible = False
hud_font = pygame.font.Font('consolas.ttf', 20)
hud_color = (200, 200, 200)


is_record=False
is_capture=False
# Main loop
running = True
while running:
    screen.fill(background_color)

    for trail in trails:
        trail.update()
        trail.draw(screen)
        
    if(is_capture):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pygame.image.save(screen, f"frame_{timestamp}.png")
        is_capture=False

    # Draw HUD if visible
    if hud_visible and not is_recording:
        hud_text = f"Press [C] to capture frame | Press [R] to start/stop recording"
        hud_surface = hud_font.render(hud_text, True, hud_color)
        screen.blit(hud_surface, (width // 2 - hud_surface.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                hud_visible = not hud_visible
            elif event.key == pygame.K_c:  # Capture frame with "C" key
                is_capture=True
            elif event.key == pygame.K_r:  # Start/stop recording with "R" key
                if not is_recording:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    video_writer = cv2.VideoWriter(f"matrix_{timestamp}.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (width, height))
                    is_recording = True
                else:
                    video_writer.release()
                    video_writer = None
                    is_recording = False
            elif event.key == pygame.K_f:
                toggle_fullscreen()

    if is_recording:
        frame = pygame.surfarray.array3d(screen)
        frame = cv2.cvtColor(np.array(frame).swapaxes(0, 1), cv2.COLOR_RGB2BGR)
        video_writer.write(frame)

if video_writer is not None:
    video_writer.release()
    

print("Matrix Rainfail Wallpaper\nBy LaGlavVei\nPress '1' to view the hud, 'r' to record and stop recording and finally 'c' to capture a frame of the animation")

pygame.quit()