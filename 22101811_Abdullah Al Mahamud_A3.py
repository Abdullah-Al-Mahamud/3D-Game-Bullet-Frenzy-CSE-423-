from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random

class GameConfig:
    ARENA_SIZE = 15
    TILE_SIZE = 1.0
    TOTAL_ENEMIES = 5
    PROJECTILE_VELOCITY = 0.3

class CameraConfig:
    def __init__(self):
        self.angle = 0
        self.radius = 15
        self.elevation = 18
        self.mode = "3rd"

class PlayerState:
    def __init__(self):
        self.x = GameConfig.ARENA_SIZE / 2
        self.z = GameConfig.ARENA_SIZE / 2
        self.rotation = 0
        self.health = 5
        self.points = 0
        self.shots_missed = 0
        self.auto_mode = False
        self.fire_delay = 0
        self.target_index = 0

class GameState:
    def __init__(self):
        self.is_finished = False
        self.hostile_units = []
        self.shot_list = []

class ColorScheme:
    WHITE = (1.0, 1.0, 1.0)
    PURPLE = (0.8, 0.6, 0.95)
    BLUE = (0.0, 0.0, 1.0)
    GREEN = (0.0, 1.0, 0.0)
    CYAN = (0.0, 1.0, 1.0)
    MAGENTA = (1.0, 0.0, 1.0)
    RED = (1.0, 0.0, 0.0)
    BLACK = (0.0, 0.0, 0.0)
    BROWN = (0.8, 0.4, 0.0)
    SKIN = (0.96, 0.8, 0.69)
    GRAY = (0.5, 0.5, 0.5)
    OLIVE = (0.4, 0.5, 0.2)

class GameRenderer:
    
    @staticmethod
    def render_floor_grid():
        for row in range(GameConfig.ARENA_SIZE):
            for col in range(GameConfig.ARENA_SIZE):
                tile_color = ColorScheme.WHITE if (row + col) % 2 == 0 else ColorScheme.PURPLE
                glColor3f(*tile_color)
                glBegin(GL_QUADS)
                glVertex3f(row * GameConfig.TILE_SIZE, 0, col * GameConfig.TILE_SIZE)
                glVertex3f((row + 1) * GameConfig.TILE_SIZE, 0, col * GameConfig.TILE_SIZE)
                glVertex3f((row + 1) * GameConfig.TILE_SIZE, 0, (col + 1) * GameConfig.TILE_SIZE)
                glVertex3f(row * GameConfig.TILE_SIZE, 0, (col + 1) * GameConfig.TILE_SIZE)
                glEnd()

    @staticmethod
    def render_boundary_walls():
        wall_height = 1
        wall_depth = 0.2
        arena_length = GameConfig.ARENA_SIZE * GameConfig.TILE_SIZE

        # Bottom wall - blue
        glColor3f(*ColorScheme.BLUE)
        GameRenderer._render_wall(arena_length / 2, wall_height / 2, wall_depth / 2, 
                                arena_length, wall_height, wall_depth)

        # Top wall - green
        glColor3f(*ColorScheme.GREEN)
        GameRenderer._render_wall(arena_length / 2, wall_height / 2, arena_length - wall_depth / 2, 
                                arena_length, wall_height, wall_depth)

        # Left wall - cyan
        glColor3f(*ColorScheme.CYAN)
        GameRenderer._render_wall(wall_depth / 2, wall_height / 2, arena_length / 2, 
                                wall_depth, wall_height, arena_length)

        # Right wall - magenta
        glColor3f(*ColorScheme.MAGENTA)
        GameRenderer._render_wall(arena_length - wall_depth / 2, wall_height / 2, arena_length / 2, 
                                wall_depth, wall_height, arena_length)

    @staticmethod
    def _render_wall(x, y, z, width, height, depth):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(width, height, depth)
        glutSolidCube(1)
        glPopMatrix()

    @staticmethod
    def render_player(player):
        glPushMatrix()
        glTranslatef(player.x, 0, player.z)
        glRotatef(player.rotation, 0, 1, 0)
        glScalef(0.9, 0.9, 0.9)

        if game_state.is_finished:
            glRotatef(90, 1, 0, 0)

        GameRenderer._render_player_legs()
        GameRenderer._render_player_torso()
        GameRenderer._render_player_arms()
        GameRenderer._render_player_weapon()
        GameRenderer._render_player_head()

        glPopMatrix()

    @staticmethod
    def _render_player_legs():
        glColor3f(*ColorScheme.BLUE)
        for leg_offset in [-0.2, 0.2]:
            glPushMatrix()
            glTranslatef(leg_offset, 0.4, 0)
            glRotatef(-90, 1, 0, 0)
            leg_quad = gluNewQuadric()
            gluCylinder(leg_quad, 0.1, 0.05, 0.4, 20, 20)
            gluDeleteQuadric(leg_quad)
            glPopMatrix()

    @staticmethod
    def _render_player_torso():
        glColor3f(*ColorScheme.OLIVE)
        glPushMatrix()
        glTranslatef(0, 1.0, 0)
        glScalef(0.4, 0.6, 0.2)
        glutSolidCube(1)
        glPopMatrix()

    @staticmethod
    def _render_player_arms():
        glColor3f(*ColorScheme.SKIN)
        for arm_offset in [-0.15, 0.15]:
            glPushMatrix()
            glTranslatef(arm_offset, 1.2, 0.1)
            arm_quad = gluNewQuadric()
            gluCylinder(arm_quad, 0.1, 0.05, 0.4, 20, 20)
            gluDeleteQuadric(arm_quad)
            glPopMatrix()

    @staticmethod
    def _render_player_weapon():
        glColor3f(*ColorScheme.GRAY)
        glPushMatrix()
        glTranslatef(0, 1.2, 0.1)
        weapon_quad = gluNewQuadric()
        gluCylinder(weapon_quad, 0.08, 0.0, 0.8, 20, 20)
        gluDeleteQuadric(weapon_quad)
        glPopMatrix()

    @staticmethod
    def _render_player_head():
        glColor3f(*ColorScheme.BLACK)
        glPushMatrix()
        glTranslatef(0, 1.65, 0)
        glutSolidSphere(0.2, 20, 20)
        glPopMatrix()

    @staticmethod
    def render_projectiles():
        glColor3f(0.8, 0.33, 0.0)
        for projectile in game_state.shot_list:
            glPushMatrix()
            glTranslatef(projectile['x'], 1.2, projectile['z'])
            glScalef(0.15, 0.15, 0.15)
            glutSolidCube(1)
            glPopMatrix()

    @staticmethod
    def render_enemies():
        for enemy in game_state.hostile_units:
            glPushMatrix()
            glTranslatef(enemy['x'], 0.4, enemy['z'])
            glScalef(enemy['scale'], enemy['scale'], enemy['scale'])

            # Enemy head
            glColor3f(*ColorScheme.RED)
            glPushMatrix()
            glTranslatef(0, 0.2, 0)
            glutSolidSphere(0.2, 20, 20)
            glPopMatrix()

            # Enemy body
            glColor3f(*ColorScheme.BLACK)
            glPushMatrix()
            glTranslatef(0, 0.45, 0)
            glutSolidSphere(0.12, 20, 20)
            glPopMatrix()

            glPopMatrix()

    @staticmethod
    def render_ui_overlay():
        if game_state.is_finished:
            GameRenderer._render_game_over_screen()
        else:
            GameRenderer._render_game_stats()

    @staticmethod
    def _render_game_over_screen():
        glColor3f(1, 0, 0)
        GameRenderer._render_text(10, 770, f"GAME OVER. Your Score is {player.points}", GLUT_BITMAP_TIMES_ROMAN_24)
        GameRenderer._render_text(10, 750, "Press 'R' to Restart the Game", GLUT_BITMAP_TIMES_ROMAN_24)

    @staticmethod
    def _render_game_stats():
        glColor3f(1, 1, 1)
        GameRenderer._render_text(10, 770, f"Game Score: {player.points}", GLUT_BITMAP_HELVETICA_18)
        GameRenderer._render_text(10, 750, f"Player life remaining: {player.health}", GLUT_BITMAP_HELVETICA_18)
        GameRenderer._render_text(10, 730, f"Player Bullet Missed: {player.shots_missed}", GLUT_BITMAP_HELVETICA_18)

    @staticmethod
    def _render_text(x_pos, y_pos, message, font=GLUT_BITMAP_HELVETICA_18):
        glColor3f(1, 1, 1)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glRasterPos2f(x_pos, y_pos)
        for character in message:
            glutBitmapCharacter(font, ord(character))

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

class GameLogic:
    
    @staticmethod
    def update_projectiles():
        if player.auto_mode:
            GameLogic._execute_auto_targeting()

        updated_shots = []
        for projectile in game_state.shot_list:
            angle_radians = math.radians(projectile['angle'])
            projectile['x'] += GameConfig.PROJECTILE_VELOCITY * math.sin(angle_radians)
            projectile['z'] += GameConfig.PROJECTILE_VELOCITY * math.cos(angle_radians)

            if GameLogic._is_projectile_in_bounds(projectile):
                if not GameLogic._check_enemy_hit(projectile):
                    updated_shots.append(projectile)
            else:
                if not player.auto_mode:
                    player.shots_missed += 1
                    print(f"Projectile missed: {player.shots_missed}")

        game_state.shot_list = updated_shots

    @staticmethod
    def _is_projectile_in_bounds(projectile):
        return 0 <= projectile['x'] <= GameConfig.ARENA_SIZE and 0 <= projectile['z'] <= GameConfig.ARENA_SIZE

    @staticmethod
    def _check_enemy_hit(projectile):
        for enemy_unit in game_state.hostile_units:
            distance_x = projectile['x'] - enemy_unit['x']
            distance_z = projectile['z'] - enemy_unit['z']
            if math.sqrt(distance_x * distance_x + distance_z * distance_z) < 0.5:
                player.points += 10
                game_state.hostile_units.remove(enemy_unit)
                return True
        return False

    @staticmethod
    def _execute_auto_targeting():
        rotation_increment = 2
        player.rotation = (player.rotation + rotation_increment) % 360
        
        if player.fire_delay > 0:
            player.fire_delay -= 1

        if player.fire_delay == 0 and len(game_state.hostile_units) > 0:
            enemy_target = game_state.hostile_units[player.target_index % len(game_state.hostile_units)]
            target_x = enemy_target['x'] - player.x
            target_z = enemy_target['z'] - player.z
            firing_angle = math.degrees(math.atan2(target_x, target_z))
            
            game_state.shot_list.append({
                'x': player.x,
                'z': player.z,
                'angle': firing_angle
            })
            player.target_index += 1
            player.fire_delay = 60

    @staticmethod
    def update_enemies():
        for enemy in game_state.hostile_units[:]:
            GameLogic._move_enemy(enemy)
            GameLogic._animate_enemy(enemy)
            GameLogic._check_player_collision(enemy)

        GameLogic._maintain_enemy_count()

    @staticmethod
    def _move_enemy(enemy): 
        direction_x = player.x - enemy['x']
        direction_z = player.z - enemy['z']
        total_distance = math.hypot(direction_x, direction_z)
        if total_distance > 0:
            enemy['x'] += 0.0015 * direction_x / total_distance
            enemy['z'] += 0.0015 * direction_z / total_distance

    @staticmethod
    def _animate_enemy(enemy):
        if enemy['shrinking']:
            enemy['scale'] -= 0.002
            if enemy['scale'] <= 0.6:
                enemy['shrinking'] = False
        else:
            enemy['scale'] += 0.002
            if enemy['scale'] >= 1.2:
                enemy['shrinking'] = True

    @staticmethod
    def _check_player_collision(enemy):
        distance_x = enemy['x'] - player.x
        distance_z = enemy['z'] - player.z
        if (distance_x ** 2 + distance_z ** 2) ** 0.5 < 0.5:
            if player.health > 0:
                player.health -= 1
                print(f"Remaining player health: {player.health}")
            game_state.hostile_units.remove(enemy)

    @staticmethod
    def _maintain_enemy_count():
        while len(game_state.hostile_units) < GameConfig.TOTAL_ENEMIES:
            game_state.hostile_units.append(GameLogic._spawn_enemy())

    @staticmethod
    def _spawn_enemy():
        while True:
            spawn_x = random.uniform(1, GameConfig.ARENA_SIZE - 1)
            spawn_z = random.uniform(1, GameConfig.ARENA_SIZE - 1)
            if abs(spawn_x - player.x) > 3 and abs(spawn_z - player.z) > 3:
                return {'x': spawn_x, 'z': spawn_z, 'scale': 1.0, 'shrinking': True}

    @staticmethod
    def check_game_over():
        if player.health <= 0 or player.shots_missed >= 10:
            game_state.is_finished = True

class GameManager:
    
    @staticmethod
    def reset_game():
        player.points = 0
        player.health = 5
        player.shots_missed = 0
        player.x = GameConfig.ARENA_SIZE / 2
        player.z = GameConfig.ARENA_SIZE / 2
        player.rotation = 0
        camera.mode = "3rd"
        game_state.is_finished = False
        game_state.shot_list.clear()
        GameManager._generate_initial_enemies()

    @staticmethod
    def _generate_initial_enemies():
        game_state.hostile_units = []
        for _ in range(GameConfig.TOTAL_ENEMIES):
            while True:
                spawn_x = random.uniform(1, GameConfig.ARENA_SIZE - 1)
                spawn_z = random.uniform(1, GameConfig.ARENA_SIZE - 1)
                if abs(spawn_x - player.x) > 2 and abs(spawn_z - player.z) > 2:
                    game_state.hostile_units.append({
                        'x': spawn_x, 'z': spawn_z, 'scale': 1.0, 'shrinking': True
                    })
                    break

class InputHandler:
    
    @staticmethod
    def handle_special_keys(key, x, y):
        if game_state.is_finished:
            return
            
        if key == GLUT_KEY_LEFT:
            camera.angle = (camera.angle - 5) % 360
        elif key == GLUT_KEY_RIGHT:
            camera.angle = (camera.angle + 5) % 360
        elif key == GLUT_KEY_DOWN:
            camera.radius = min(camera.radius + 1, 30)
            camera.elevation = min(camera.elevation + 1, 20)
        elif key == GLUT_KEY_UP:
            camera.radius = max(camera.radius - 1, 10)
            camera.elevation = max(camera.elevation - 1, 12)
        
        glutPostRedisplay()

    @staticmethod
    def handle_keyboard(key, x, y):
        if game_state.is_finished:
            if key == b'r':
                GameManager.reset_game()
            return

        if key == b'c':
            player.auto_mode = not player.auto_mode
            return

        InputHandler._handle_movement(key)
        InputHandler._apply_boundary_constraints()
        glutPostRedisplay()

    @staticmethod
    def _handle_movement(key):
        movement_step = 0.2
        if key == b'w':
            angle_radians = math.radians(player.rotation)
            player.x += movement_step * math.sin(angle_radians)
            player.z += movement_step * math.cos(angle_radians)
        elif key == b's':
            angle_radians = math.radians(player.rotation)
            player.x -= movement_step * math.sin(angle_radians)
            player.z -= movement_step * math.cos(angle_radians)
        elif key == b'a':
            player.rotation = (player.rotation - 5) % 360
        elif key == b'd':
            player.rotation = (player.rotation + 5) % 360

    @staticmethod
    def _apply_boundary_constraints():
        boundary_min = 0.5
        boundary_max = GameConfig.ARENA_SIZE - 0.5
        player.x = max(min(player.x, boundary_max), boundary_min)
        player.z = max(min(player.z, boundary_max), boundary_min)

    @staticmethod
    def handle_mouse(button, state, x, y):
        if game_state.is_finished:
            return
            
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            print("Character projectile fired!")
            game_state.shot_list.append({
                'x': player.x,
                'z': player.z,
                'angle': player.rotation
            })
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            camera.mode = "1st" if camera.mode == "3rd" else "3rd"

class GraphicsManager:
    
    @staticmethod
    def initialize():
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    @staticmethod
    def setup_viewport(width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def setup_camera():
        if camera.mode == "3rd":
            camera_x = GameConfig.ARENA_SIZE / 2 + camera.radius * math.sin(math.radians(camera.angle))
            camera_z = GameConfig.ARENA_SIZE / 2 + camera.radius * math.cos(math.radians(camera.angle))
            gluLookAt(camera_x, camera.elevation, camera_z, 
                     GameConfig.ARENA_SIZE / 2, 0, GameConfig.ARENA_SIZE / 2, 0, 1, 0)
        else:
            angle_radians = math.radians(player.rotation)
            pos_x = player.x
            pos_y = 1
            pos_z = player.z
            look_x = pos_x + math.sin(angle_radians)
            look_y = pos_y
            look_z = pos_z + math.cos(angle_radians)
            gluLookAt(pos_x, pos_y, pos_z, look_x, look_y, look_z, 0, 1, 0)

def main_display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    GraphicsManager.setup_camera()
    
    GameRenderer.render_floor_grid()
    GameRenderer.render_boundary_walls()
    GameRenderer.render_player(player)
    GameRenderer.render_projectiles()
    GameRenderer.render_enemies()

    if not game_state.is_finished:
        GameLogic.update_projectiles()
        GameLogic.update_enemies()
        GameLogic.check_game_over()

    glDisable(GL_LIGHTING)
    GameRenderer.render_ui_overlay()
    
    glutSwapBuffers()
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutCreateWindow(b"Combat Arena")
    
    GraphicsManager.initialize()
    GameManager._generate_initial_enemies()
    
    glutDisplayFunc(main_display)
    glutReshapeFunc(GraphicsManager.setup_viewport)
    glutSpecialFunc(InputHandler.handle_special_keys)
    glutKeyboardFunc(InputHandler.handle_keyboard)
    glutMouseFunc(InputHandler.handle_mouse)
    
    glutMainLoop()


camera = CameraConfig()
player = PlayerState()
game_state = GameState()

if __name__ == "__main__":
    main()