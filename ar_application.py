import cv2
import numpy as np
import matplotlib.pyplot as plt
import pygame

pygame.init()
pygame.display.set_caption("AR Light Intensity Measurement")

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

cap = cv2.VideoCapture(0)

history_length = 100
intensity_history = []

def measure_light_intensity(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    average_intensity = np.mean(gray_frame)

    return average_intensity

def plot_light_intensity(intensity_history):
    plt.plot(intensity_history, color='blue')
    plt.xlabel('Time')
    plt.ylabel('Light Intensity')
    plt.title('Light Intensity Plot')
    plt.xlim(0, len(intensity_history))  # Set x-axis limit to the length of history
    plt.ylim(0, 255)  # Set y-axis limit to intensity range
    plt.gca().axes.get_xaxis().set_visible(False)  # Hide x-axis labels
    plt.gca().axes.get_yaxis().set_visible(False)  # Hide y-axis labels
    plt.savefig('plot.png')  # Save the plot as an image
    plt.close()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()


    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)


    frame = cv2.resize(frame, (width, height))


    intensity = measure_light_intensity(frame)


    intensity_history.append(intensity)
    if len(intensity_history) > history_length:  
        intensity_history.pop(0)
    plot_light_intensity(intensity_history)


    plot_surface = pygame.image.load('plot.png').convert_alpha()
    plot_surface = pygame.transform.scale(plot_surface, (int(width/3), int(height/3)))  # Resize the plot


    screen.fill((0, 0, 0))
    screen.blit(pygame.surfarray.make_surface(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), (0, 0))  # Webcam frame
    screen.blit(plot_surface, (width - int(width/3), 0)) 


    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Light Intensity: {int(intensity)}", True, (255, 255, 255))
    screen.blit(text, (10, 10))


    pygame.display.flip()


    clock.tick(30)


cap.release()
pygame.quit()
