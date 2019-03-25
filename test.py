import pygame

pygame.init()

sc = pygame.display.set_mode((400, 300))
sc.fill((100, 150, 200))

dog_surf = pygame.image.load('img/dog.png')
dog_rect = dog_surf.get_rect(bottomright=(400, 300))
print(dog_rect)
sc.blit(dog_surf, dog_rect)

pygame.display.update()
