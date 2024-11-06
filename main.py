# Example file showing a circle moving on screen
import json
import pygame
import random
import time


WIDTH = 1280
HEIGHT = 720

# pygame setup
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('UI/music/Stream Loops 2024-02-21_01.ogg')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = 'fonts/PublicPixel-z84yD.ttf'
font_color = 0, 204, 255

game_state = 'start'
start_life = 9
highscore = 0
point_score = 0
spaceship = 1
maps = 1
maps_list = ['black', 'blue', 'darkPurple', 'purple']
prev_mouse_state = None
background = 'darkPurple.png'
last_hit_time = 0

spaceship_file = 'player/characters/player.png'
background_file = 'background/darkPurple.png'


#player projectiles
shooting_sound = pygame.mixer.Sound("player/sounds/sfx_laser1.ogg")
player_image_projectile = pygame.image.load("player/projectiles/laserBlue01.png").convert_alpha() #player projectiles
projectiles = pygame.sprite.Group()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
entities = pygame.sprite.Group()
explosion_images = []  # Load explosion images outside the class
for i in range(0, 8):
    img = pygame.image.load(f"entity/effects/explosion0{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (64, 64))
    explosion_images.append(img)

class GameScreen:
    @staticmethod
    def start_menu(font, font_color):
        title_font = pygame.font.Font(font, 60)
        title = title_font.render('Space Champion 64', True, (font_color))
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/6))
        screen.blit(title, title_rect)

        start_font = pygame.font.Font(font, 40)
        start = start_font.render('Start', True, (font_color))
        start_rect = start.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(start, start_rect)

        leaderboard_font = pygame.font.Font(font, 40)
        leaderboard = leaderboard_font.render('Leaderboard', True, (font_color))
        leaderboard_rect = leaderboard.get_rect(center=(WIDTH/2, HEIGHT/1.72))
        screen.blit(leaderboard, leaderboard_rect)

        customize_font = pygame.font.Font(font, 40)
        customize = customize_font.render('Customize', True, (font_color))
        customize_rect = customize.get_rect(center=(WIDTH/2, HEIGHT/1.5))
        screen.blit(customize, customize_rect)
        
        quit_font = pygame.font.Font(font, 40)
        quit = quit_font.render('Quit', True, (font_color))
        quit_rect = quit.get_rect(center=(WIDTH/2, HEIGHT/1.1))
        screen.blit(quit, quit_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        global game_state
        if start_rect.collidepoint(mouse_pos):
            start = start_font.render('Start', True, (255,255,255))
            start_rect = start.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(start, start_rect)
            if mouse_clicked:
                game_state = 'game' 
        elif leaderboard_rect.collidepoint(mouse_pos):
            leaderboard = leaderboard_font.render('Leaderboard', True, (255,255,255))
            leaderboard_rect = leaderboard.get_rect(center=(WIDTH/2, HEIGHT/1.72))
            screen.blit(leaderboard, leaderboard_rect)
            if mouse_clicked:
                game_state = 'leaderboard'
        elif customize_rect.collidepoint(mouse_pos):
            customize = customize_font.render('Customize', True, (255,255,255))
            customize_rect = customize.get_rect(center=(WIDTH/2, HEIGHT/1.5))
            screen.blit(customize, customize_rect)
            if mouse_clicked:
                game_state = 'custom'
        elif quit_rect.collidepoint(mouse_pos):
            quit = quit_font.render('Quit', True, (138,3,3))
            quit_rect = quit.get_rect(center=(WIDTH/2, HEIGHT/1.1))
            screen.blit(quit, quit_rect)
            if mouse_clicked:
                game_state = 'quit'
        pygame.display.update()
        
    @staticmethod
    def game_over(font, font_color=(138,3,3)):
        title_font = pygame.font.Font(font, 60)
        title = title_font.render('Game Over', True, (font_color))
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/6))
        screen.blit(title, title_rect)
        
        title_font = pygame.font.Font(font, 40)
        title = title_font.render('Score', True, (255,255,255))
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/3.5))
        screen.blit(title, title_rect)
        score_font = pygame.font.Font(font, 40)
        score = score_font.render(str(point_score), True, (255,255,255))
        score_rect = score.get_rect(center=(WIDTH/2, HEIGHT/3.5 + title.get_height() + 20))
        screen.blit(score, score_rect)
        
        restart_font = pygame.font.Font(font, 40)
        restart = restart_font.render('Restart', True, (font_color))
        restart_rect = restart.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(restart, restart_rect)

        leaderboard_font = pygame.font.Font(font, 40)
        leaderboard = leaderboard_font.render('Leaderboard', True, (font_color))
        leaderboard_rect = leaderboard.get_rect(center=(WIDTH/2, HEIGHT/1.72))
        screen.blit(leaderboard, leaderboard_rect)
        
        back_font = pygame.font.Font(font, 40)
        back = back_font.render('Main menu', True, (font_color))
        back_rect = back.get_rect(center=(WIDTH/2, HEIGHT/1.1))
        screen.blit(back, back_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        global game_state
        if restart_rect.collidepoint(mouse_pos):
            restart = restart_font.render('Restart', True, (255,255,255))
            restart_rect = restart.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(restart, restart_rect)
            if mouse_clicked:
                game_state = 'game'
        elif leaderboard_rect.collidepoint(mouse_pos):
            leaderboard = leaderboard_font.render('Leaderboard', True, (255,255,255))
            leaderboard_rect = leaderboard.get_rect(center=(WIDTH/2, HEIGHT/1.72))
            screen.blit(leaderboard, leaderboard_rect)
            if mouse_clicked:
                game_state = 'leaderboard'
        elif back_rect.collidepoint(mouse_pos):
            back = back_font.render('Main menu', True, (255,255,255))
            back_rect = back.get_rect(center=(WIDTH/2, HEIGHT/1.1))
            screen.blit(back, back_rect)
            if mouse_clicked:
                game_state = 'start'
        pygame.display.update()
        
    def leaderboard(font, font_color):
        title_font = pygame.font.Font(font, 60)
        title = title_font.render('Leaderboard', True, font_color)
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/6))
        screen.blit(title, title_rect)
        
        with open('db.json', 'r') as file:
            scoreboard_data = json.load(file)
        scoreboard = scoreboard_data['scoreBoard']
        entry_height = 45  # Adjust this value as needed for proper spacing
        
        y_position = HEIGHT / 3.8  # Starting position for the first entry
        
        for index, (position, score) in enumerate(scoreboard.items(), start=1):
            score_item_font = pygame.font.Font(font, 40)
            score_item = score_item_font.render(f'{index}: {score}', True, font_color)
            score_item_rect = score_item.get_rect(center=(WIDTH/2, y_position))
            screen.blit(score_item, score_item_rect)
            
            # Move to the next entry position
            y_position += entry_height
            
        # Draw the 'Return' button
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        back_font = pygame.font.Font(font, 40)
        back = back_font.render('Return', True, font_color)
        back_rect = back.get_rect(center=(WIDTH/2, HEIGHT/1.1))
        screen.blit(back, back_rect)
        
        global game_state
        if back_rect.collidepoint(mouse_pos):
            back = back_font.render('Return', True, (255, 255, 255))
            back_rect = back.get_rect(center=(WIDTH/2, HEIGHT/1.1))
            screen.blit(back, back_rect)
            if mouse_clicked:
                time.sleep(0.7)
                game_state = 'start'

    class customize():
        def menu(font, font_color):
            title_font = pygame.font.Font(font, 60)
            title = title_font.render('Customize', True, (font_color))
            title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/6))
            screen.blit(title, title_rect)
            
            ships_font = pygame.font.Font(font, 40)
            ships = ships_font.render('Spaceships', True, (font_color))
            ships_rect = ships.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(ships, ships_rect) 
        
            maps_font = pygame.font.Font(font, 40)
            maps = maps_font.render('Maps', True, (font_color))
            maps_rect = maps.get_rect(center=(WIDTH/2, HEIGHT/1.72))
            screen.blit(maps, maps_rect)
            
            back_font = pygame.font.Font(font, 40)
            back = back_font.render('Return', True, (font_color))
            back_rect = back.get_rect(center=(WIDTH/2, HEIGHT/1.5))
            screen.blit(back, back_rect)

            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            global game_state
            if ships_rect.collidepoint(mouse_pos):
                ships = ships_font.render('Spaceships', True, (255,255,255))
                ships_rect = ships.get_rect(center=(WIDTH/2, HEIGHT/2))
                screen.blit(ships, ships_rect)
                if mouse_clicked:
                    game_state = 'ships'
            elif maps_rect.collidepoint(mouse_pos):
                maps = maps_font.render('Maps', True, (255,255,255))
                maps_rect = maps.get_rect(center=(WIDTH/2, HEIGHT/1.72))
                screen.blit(maps, maps_rect)
                if mouse_clicked:
                    game_state = 'maps'
            elif back_rect.collidepoint(mouse_pos):
                back = back_font.render('Return', True, (255,255,255))
                back_rect = back.get_rect(center=(WIDTH/2, HEIGHT/1.5))
                screen.blit(back, back_rect)
                if mouse_clicked:
                    time.sleep(.7)
                    game_state = 'start'
            
        def ships(font, font_color):
            global spaceship  # Declare spaceship as global inside the function
            global prev_mouse_state
            global spaceship_file

            Background.create('background/purple.png')
            
            title_font = pygame.font.Font(font, 60)
            title = title_font.render('Spaceships', True, (font_color))
            title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/6))
            screen.blit(title, title_rect)
                        
            navigate_left_img = pygame.image.load(f"UI/navigation/switch_left_outline.png").convert_alpha()
            navigate_left_rect = navigate_left_img.get_rect(center=(WIDTH / 4, HEIGHT / 2))
            screen.blit(navigate_left_img, navigate_left_rect)
            
            navigate_right_img = pygame.image.load(f"UI/navigation/switch_right_outline.png").convert_alpha()
            navigate_right_rect = navigate_right_img.get_rect(center=(WIDTH / 1.35, HEIGHT / 2))
            screen.blit(navigate_right_img, navigate_right_rect)
            
            border = pygame.image.load(f"UI/border/blue_pressed.png").convert_alpha()
            border = pygame.transform.scale(border, (310, 310))
            border_rect = border.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(border, border_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            spaceship_img = pygame.image.load(f"player/characters/playerShip{spaceship}.png").convert_alpha()
            spaceship_img = pygame.transform.scale(spaceship_img, (128, 128))
            spaceship_img_rect = spaceship_img.get_rect(center=(WIDTH / 2, HEIGHT / 2))

            if navigate_left_rect.collidepoint(mouse_pos):
                if mouse_clicked and not prev_mouse_state:
                    if spaceship == 1:  # Check if spaceship is currently at 1
                        spaceship = 12  # Set spaceship to 12
                    else:
                        spaceship -= 1  # Decrement spaceship
                    
            if navigate_right_rect.collidepoint(mouse_pos):
                if mouse_clicked and not prev_mouse_state:
                    if spaceship > 11:  # Check if spaceship is currently at 1
                        spaceship = 1
                    else:
                        spaceship += 1  # Decrement spaceship
            prev_mouse_state = mouse_clicked

            # Blit the spaceship image onto the screen
            screen.blit(spaceship_img, spaceship_img_rect)
            
            confirm_font = pygame.font.Font(font, 40)
            confirm = confirm_font.render('OK', True, (255,255,255))
            confirm_rect = confirm.get_rect(center=(WIDTH/2, HEIGHT/1.1))
            screen.blit(confirm, confirm_rect)
            
            global game_state
            if confirm_rect.collidepoint(mouse_pos):
                confirm = confirm_font.render('OK', True, (57,255,20))
                confirm_rect = confirm.get_rect(center=(WIDTH/2, HEIGHT/1.1))
                screen.blit(confirm, confirm_rect)
                if mouse_clicked:
                    spaceship_file = f'player/characters/playerShip{spaceship}.png'
                    game_state = 'custom'
                    
        
        def maps(font, font_color):
            global maps  # Declare spaceship as global inside the function
            global prev_mouse_state
            global background_file

            Background.create('background/purple.png')
            
            title_font = pygame.font.Font(font, 60)
            title = title_font.render('Maps', True, (font_color))
            title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/6))
            screen.blit(title, title_rect)

            navigate_left_img = pygame.image.load(f"UI/navigation/switch_left_outline.png").convert_alpha()
            navigate_left_rect = navigate_left_img.get_rect(center=(WIDTH / 4, HEIGHT / 2))
            screen.blit(navigate_left_img, navigate_left_rect)
            
            navigate_right_img = pygame.image.load(f"UI/navigation/switch_right_outline.png").convert_alpha()
            navigate_right_rect = navigate_right_img.get_rect(center=(WIDTH / 1.35, HEIGHT / 2))
            screen.blit(navigate_right_img, navigate_right_rect)
            
            border = pygame.image.load(f"UI/border/blue_pressed.png").convert_alpha()
            border = pygame.transform.scale(border, (310, 310))
            border_rect = border.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(border, border_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            maps_img = pygame.image.load(f"background/{maps_list[maps-1]}.png").convert_alpha()
            maps_img = pygame.transform.scale(maps_img, (256, 256))
            maps_img_rect = maps_img.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            
            if navigate_left_rect.collidepoint(mouse_pos):
                if mouse_clicked and not prev_mouse_state:
                    if maps == 1:  # Check if spaceship is currently at 1
                        maps = 4  # Set spaceship to 12
                    else:
                        maps -= 1  # Decrement spaceship
                    
            if navigate_right_rect.collidepoint(mouse_pos):
                if mouse_clicked and not prev_mouse_state:
                    if maps > 3:  # Check if spaceship is currently at 1
                        maps = 1
                    else:
                        maps += 1  # Decrement spaceship
            prev_mouse_state = mouse_clicked
            screen.blit(maps_img, maps_img_rect)
            
            confirm_font = pygame.font.Font(font, 40)
            confirm = confirm_font.render('OK', True, (255,255,255))
            confirm_rect = confirm.get_rect(center=(WIDTH/2, HEIGHT/1.1))
            screen.blit(confirm, confirm_rect)
            
            global game_state
            if confirm_rect.collidepoint(mouse_pos):
                confirm = confirm_font.render('OK', True, (57,255,20))
                confirm_rect = confirm.get_rect(center=(WIDTH/2, HEIGHT/1.1))
                screen.blit(confirm, confirm_rect)
                if mouse_clicked:
                    background_file = f"background/{maps_list[maps-1]}.png"
                    game_state = 'custom'

class Background:
    @staticmethod
    def create(background):
        background = pygame.image.load(background).convert_alpha()
        horizontal_tiles = WIDTH // background.get_width() + 1
        vertical_tiles = HEIGHT // background.get_height() + 1
        for x in range(horizontal_tiles):
            for y in range(vertical_tiles):
                screen.blit(background, (x * background.get_width(), y * background.get_height()))

class ScoreBoard:
    @staticmethod
    def add_new_score(point_score:int):
        print(f'NEW SCORE: {point_score}')
        with open('db.json', 'r') as file:
            scoreboard_data = json.load(file)
        scoreboard = scoreboard_data['scoreBoard']
        updated = False
        for position, score in scoreboard.items():
            if point_score > score:
                # Update the scoreboard with the new score
                scoreboard[position] = point_score
                updated = True
                break  # Exit the loop after updating the scoreboard for the highest position

        if updated:
            sorted_scoreboard = dict(sorted(scoreboard.items(), key=lambda x: x[1], reverse=True))

            # Write the updated scoreboard back to the JSON file
            with open('db.json', 'w') as file:
                # Update the scoreboard data with the sorted scoreboard
                scoreboard_data['scoreBoard'] = sorted_scoreboard
                # Write the updated data back to the file
                json.dump(scoreboard_data, file, indent=4)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(spaceship_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width() / 2
        self.rect.bottom = screen.get_height() - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        keystate = pygame.key.get_pressed()
        self.speedx = 0
        self.speedy = 0
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8  # Decrease y-coordinate to move up
        if keystate[pygame.K_DOWN]:
            self.speedy = 8   # Increase y-coordinate to move down
        self.rect.x += self.speedx
        self.rect.y += self.speedy  # Update y-coordinate for vertical movement
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
        if self.rect.top < 0:
            self.rect.top = 0
            
    def render_life(self):
        global life
        life_image = pygame.image.load(f"UI/numbers/numeral{life}.png").convert_alpha()
        life_image = pygame.transform.scale(life_image, (64, 64))

        life_x_image = pygame.image.load(f"UI/numbers/numeralX.png").convert_alpha()
        life_x_image = pygame.transform.scale(life_x_image, (64, 64))
        screen.blit(life_image, (WIDTH - life_image.get_width() - 10, HEIGHT - life_image.get_height() - 10))
        screen.blit(life_x_image, (WIDTH - life_image.get_width() - life_x_image.get_width() - 20, HEIGHT - life_image.get_height() - 10))
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shooting_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image_projectile
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image_color = ['Black', 'Blue', 'Green', 'Red']
        self.image = pygame.image.load(f"entity/character/Enemies/enemy{random.choice(image_color)}{random.randint(1,5)}.png").convert_alpha()
        self.shoot_delay = random.randrange (1, 3) * 1000
        self.last_shot = pygame.time.get_ticks()
        self.rect = self.image.get_rect(center=player_pos)
        self.rect.x = random.randrange(screen.get_width() - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > screen.get_height() + 10 or self.rect.left < -25 or self.rect.right > screen.get_width() + 20:
            self.rect.x = random.randrange(screen.get_width() - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
        shooting_sound.play()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("entity/projectiles/laserRed04.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = 5  # Adjust the speed as needed

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image_size = [f'med{random.randint(1,2)}', f'big{random.randint(1,4)}']
        image_color = ['Brown', 'Grey']
        self.image = pygame.image.load(f"entity/character/Meteors/meteor{random.choice(image_color)}_{random.choice(image_size)}.png").convert_alpha()
        self.rect = self.image.get_rect(center=player_pos)
        self.rect.x = random.randrange(screen.get_width() - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > screen.get_height() + 10 or self.rect.left < -25 or self.rect.right > screen.get_width() + 20:
            self.rect.x = random.randrange(screen.get_width() - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

class EntityExplosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=player_pos)
        self.rect.center = center
        self.animation_frames = 2
        self.current_frame = 0
        
    def update(self):
        if self.current_frame < len(self.explosion_images):
            self.image = self.explosion_images[self.current_frame]
            self.current_frame += 1
        else:
            self.kill() 

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.animation_frames = 2
        self.current_frame = 0
        self.explosion_images = []  # Add your explosion images here
        for i in range(0, 8):
            img = pygame.image.load(f"entity/effects/explosion0{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (64, 64))
            self.explosion_images.append(img)
        self.current_frame = 0

    def update(self):
        if self.current_frame < len(self.explosion_images):
            self.image = self.explosion_images[self.current_frame]
            self.current_frame += 1
        else:
            self.kill()   

while game_state != 'quit':
    clock.tick(60)
    pygame.mixer.music.play(-1)
    if game_state == 'start':
        Background.create('background/purple.png')
        while game_state == 'start':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = 'quit'
            GameScreen.start_menu(font, font_color)
            pygame.display.flip()
        
    elif game_state == 'game_over':
        ScoreBoard.add_new_score(point_score)
        Background.create('background/black.png')
        while game_state == 'game_over':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = 'quit'
            GameScreen.game_over(font)
            pygame.display.flip()

    elif game_state == 'leaderboard':
        Background.create('background/purple.png')
        while game_state == 'leaderboard':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = 'quit'
            GameScreen.leaderboard(font, font_color)
            pygame.display.flip()
        
    elif game_state == 'custom':
        time.sleep(.7)
        Background.create('background/purple.png')
        while game_state == 'custom':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = 'quit'
            GameScreen.customize.menu(font, font_color)
            pygame.display.flip()
            
    elif game_state == 'ships':
        time.sleep(.7)
        Background.create('background/purple.png')
        while game_state == 'ships':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = 'quit'
            GameScreen.customize.ships(font, font_color)
            pygame.display.flip()
            
    elif game_state == 'maps':
        time.sleep(.7)
        while game_state == 'maps':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = 'quit'
            GameScreen.customize.maps(font, font_color)
            pygame.display.flip()
            
    elif game_state == 'game':
        title_font = pygame.font.Font(font, 40)
        title = title_font.render('Score', True, (font_color))
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/6))
        score_font = pygame.font.Font(font, 40)
        score = score_font.render(str(point_score), True, (font_color))
        score_rect = score.get_rect(center=(WIDTH/2, HEIGHT/6 + title.get_height() + 20))
        point_score = 0
        life = start_life
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        enemy = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(3):
            m = Entity()
            all_sprites.add(m)
            mobs.add(m)
            
        for i in range(5):
            e = Enemy()
            all_sprites.add(e)
            enemy.add(e)
        while game_state == 'game':
            Background.create(background_file)

            screen.blit(title, title_rect)
            score = score_font.render(str(point_score), True, (font_color))
            score_rect = score.get_rect(center=(WIDTH/2, HEIGHT/6 + title.get_height() + 20))
            screen.blit(score, score_rect)


            player.render_life()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = 'quit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        game_state = 'start'
            
            if len(enemy) == 0:
                for i in range(1):
                    e = Enemy()
                    all_sprites.add(e)
                    enemy.add(e) 
                    
                
            hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
            for hit in hits:
                point_score += 10
                explosion = Explosion(hit.rect.center)
                all_sprites.add(explosion)
            
            hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
            for hit in hits:
                explosion = Explosion(hit.rect.center)
                all_sprites.add(explosion)


            hits = pygame.sprite.spritecollide(player, enemy_bullets, False)
            if hits:
                current_time = pygame.time.get_ticks()              
                if current_time - last_hit_time > 1000:
                    if life == 1:
                        player.kill()
                        game_state = 'game_over'
                    else:
                        life -= 1                    
                    last_hit_time = current_time

            hits = pygame.sprite.spritecollide(player, mobs, False)
            if hits:
                current_time = pygame.time.get_ticks()                
                if current_time - last_hit_time > 1000:
                    if life == 1:
                        player.kill()
                        game_state = 'game_over'
                    else:
                        life -= 1                    
                    last_hit_time = current_time

            clock.tick(60)
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
pygame.quit()
