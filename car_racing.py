import pygame
import random

def start_car_racing():
    pygame.init()

    screen_width, screen_height = 1600, 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Car Racing")

    road_img = pygame.image.load("2roads.jpg").convert()
    road_img = pygame.transform.scale(road_img, (screen_width, screen_height))

    car_width, car_height = 100, 150

    player_car_img = pygame.image.load("GREENCAR.png").convert_alpha()
    player_car_img = pygame.transform.scale(player_car_img, (car_width, car_height))

    obstacle_car_img = pygame.image.load("BLUECAR.png").convert_alpha()
    obstacle_car_img = pygame.transform.scale(obstacle_car_img, (car_width, car_height))

    player_speed = 7
    obstacle_speed = 7

    lane_centers = [
        screen_width // 2 - car_width - 100,  # Left lane
        screen_width // 2 - car_width // 2,   # Middle lane
        screen_width // 2 + 100               # Right lane
    ]

    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 50)

    def get_non_overlapping_position(obstacles, lane_centers, car_width, car_height):
        max_attempts = 20
        for _ in range(max_attempts):
            lane_x = random.choice(lane_centers)
            y_pos = random.randint(-car_height * 10, -car_height)
            new_rect = pygame.Rect(lane_x, y_pos, car_width, car_height)

            overlap = False
            for obs in obstacles:
                if new_rect.colliderect(obs):
                    overlap = True
                    break

            if not overlap:
                return lane_x, y_pos

        return lane_x, y_pos

    def draw_button(surface, rect, text, font, bg_color, text_color):
        pygame.draw.rect(surface, bg_color, rect)
        text_surf = font.render(text, True, text_color)
        surface.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2,
                                 rect.y + (rect.height - text_surf.get_height()) // 2))

    def game_loop():
        player_rect = pygame.Rect(screen_width // 2 - car_width // 2, screen_height - car_height - 20, car_width, car_height)

        obstacles = []
        num_obstacles = 5
        for i in range(num_obstacles):
            lane_x = random.choice(lane_centers)
            y_pos = -car_height * (i * 5)
            obstacles.append(pygame.Rect(lane_x, y_pos, car_width, car_height))

        current_obstacle_speed = obstacle_speed
        road_y1 = 0
        road_y2 = -screen_height

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False 

            road_y1 += current_obstacle_speed
            road_y2 += current_obstacle_speed

            if road_y1 >= screen_height:
                road_y1 = -screen_height
            if road_y2 >= screen_height:
                road_y2 = -screen_height

            screen.blit(road_img, (0, road_y1))
            screen.blit(road_img, (0, road_y2))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
                player_rect.x += player_speed

            if current_obstacle_speed < 20:
                current_obstacle_speed += 0.001

            for i, obstacle_rect in enumerate(obstacles):
                obstacle_rect.y += int(current_obstacle_speed)
                if obstacle_rect.top > screen_height:
                    x, y = get_non_overlapping_position(obstacles, lane_centers, car_width, car_height)
                    obstacles[i].x = x
                    obstacles[i].y = y

            collision_padding_x = 10
            collision_padding_y = 15
            player_collision_rect = player_rect.inflate(-collision_padding_x * 2, -collision_padding_y * 2)

            for obstacle_rect in obstacles:
                obstacle_collision_rect = obstacle_rect.inflate(-collision_padding_x * 2, -collision_padding_y * 2)
                if player_collision_rect.colliderect(obstacle_collision_rect):
                    return True  
            screen.blit(player_car_img, player_rect)
            for obstacle_rect in obstacles:
                screen.blit(obstacle_car_img, obstacle_rect)

            pygame.display.update()
            clock.tick(60)

    def game_over_screen():
        restart_button = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 50, 140, 60)
        quit_button = pygame.Rect(screen_width // 2 + 10, screen_height // 2 + 50, 140, 60)

        while True:
            screen.fill((30, 30, 30))
            text = font_large.render("GAME OVER!", True, (255, 0, 0))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 100))

            draw_button(screen, restart_button, "Restart", font_medium, (0, 200, 0), (255, 255, 255))
            draw_button(screen, quit_button, "Quit", font_medium, (0, 0, 255), (255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button.collidepoint(event.pos):
                        return True  # Restart game
                    elif quit_button.collidepoint(event.pos):
                        return False  # Quit game (return to caller)

            pygame.display.update()
            clock.tick(60)

    while True:
        result = game_loop()
        if result is False:  # User closed window or quit from game loop
            break

        restart = game_over_screen()
        if not restart:
            break

    pygame.quit()
   