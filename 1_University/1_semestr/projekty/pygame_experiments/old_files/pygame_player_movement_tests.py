import pygame

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
delta_time = 0


# map setup

map_background = pygame.Surface.convert(pygame.image.load(
    fr"C:\Users\matbx\OneDrive\Dokumenty\Coding\Python\1.University\projekty\pygame_experiments\Mapa_RPG-P.V._v1.0.0.png"
    ))

wall_1 = pygame.Rect(200, 260, 30, 200)




map_hitboxes = {"map_border" : pygame.Rect(5, 5, 1270, 710),
                "wall_1" : wall_1
                }




# player vars and constants
player_position = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
BASE_PLAYER_SPEED = 200

player_image = pygame.Surface.convert(pygame.image.load(
    fr"C:\Users\matbx\OneDrive\Dokumenty\Coding\Python\1.University\projekty\pygame_experiments\tucnak_warm.png"
    ))
#player_hitboxes = pygame.Rect(player_position[0], player_position[1], player_image.get_width, player_image.get_height)





# custom functions

def speed_normalization(movement_keys, player_speed, delta_time):
    number_of_pressed_keys = 0
    speed_normalizer = 1

    for key in movement_keys:
        if key == True : number_of_pressed_keys += 1

        if number_of_pressed_keys > 1:
            speed_normalizer = 2**(1/2)
            break
    distance_coefitient = player_speed * delta_time / speed_normalizer
    return distance_coefitient

# collidedict()
# test if one rectangle in a dictionary intersects
# collidedict(rect_dict) -> (key, value)
# collidedict(rect_dict) -> None
# collidedict(rect_dict, values=False) -> (key, value)
# collidedict(rect_dict, values=False) -> None
# Returns the first key and value pair that intersects with the calling Rect object. If no collisions are found, None is returned.
# If values is False (default) then the dict's keys will be used in the collision detection, otherwise the dict's values will be used.

# Note Rect objects cannot be used as keys in a dictionary (they are not hashable), so they must be converted to a tuple. e.g. rect.collidedict({tuple(key_rect) : value})
# Changed in pygame-ce 2.4.0: values is now accepted as a keyword argument. Type Stub updated to use boolean True or False, but any truthy or falsy value will be valid.


def where_did_i_crash(player_hitboxes: pygame.Rect, map_hitboxes: pygame.Rect):
    ...




while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frames
    # screen.fill("purple")
    screen.blit(map_background, (0, 0))
    pygame.draw.rect(screen, "black", map_hitboxes["wall_1"])
    movement_time = True

    if movement_time == True:

        pygame.draw.circle(screen, "blue", player_position, 10)
        screen.blit(player_image, player_position)


        keys = pygame.key.get_pressed()
        movement_keys = [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]

        distance_coefitient = speed_normalization(movement_keys, BASE_PLAYER_SPEED, delta_time)

        if keys[pygame.K_w]:
            player_position.y = pygame.math.clamp(player_position.y - distance_coefitient, 0, screen.get_height()) 
        if keys[pygame.K_s]:
            player_position.y = pygame.math.clamp(player_position.y + distance_coefitient, 0, screen.get_height())
        if keys[pygame.K_a]:
            player_position.x = pygame.math.clamp(player_position.x - distance_coefitient, 0, screen.get_width())
        if keys[pygame.K_d]:
            player_position.x = pygame.math.clamp(player_position.x + distance_coefitient, 0, screen.get_width())


    pygame.display.flip()

    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    delta_time = clock.tick(60) / 1000

pygame.quit()