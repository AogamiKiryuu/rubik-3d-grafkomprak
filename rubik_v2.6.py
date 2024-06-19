from ursina import *
import datetime

display = {}

app = Ursina()

window.exit_button.enabled = False
window.fullscreen = True

# Check Utility
game_mode = False
shuffle_mode = False
last_shuffle_check = False
popup_menu = False
shuffle_steps = 0
kesulitan = None
waktu_delay = datetime.timedelta(milliseconds=420)
waktu_bermain = None
detik = None
if window.fullscreen:
    detik = datetime.timedelta(milliseconds=16)
else:
    detik = datetime.timedelta(milliseconds=30)

# Main Menu
def display_main_menu():
    display['title_bg'] = Animation('assets\\rubik_bg')

    display['main_title'] = Text("Rubik 3D", scale=3, origin=(0.05, -5))

    display['play_btn'] = Button("Play", color=color.white, highlight_color=color.rgba(0, 1, 0, 0.8), pressed_color=color.green, text_color=color.black, scale=(0.25, 0.1), origin=(0, -1))
    display['play_btn'].on_click = change_to_select_mode


    display['quit_btn'] = Button("Quit", color=color.white, highlight_color=color.red, pressed_color=color.red, text_color=color.black, scale=(0.25, 0.1), origin=(0, 1))
    display['quit_btn'].on_click = application.quit

def change_to_main_menu():
    global game_mode
    global popup_menu
    game_mode = False
    popup_menu = False
    destroy_displayed_entity()
    display_main_menu()

# Select Mode
def display_select_mode():
    display['title_bg'] = Animation('assets\\rubik_bg', )

    display['main_title'] = Text("Rubik 3D", scale=3, origin=(0.05, -5))

    display['free_mode_btn'] = Button("Free Mode", color=color.white, highlight_color=color.white66, pressed_color=color.white, text_color=color.black, scale=(0.25, 0.1), origin=(0, -1.5))
    display['free_mode_btn'].on_click = change_to_free_mode

    display['time_challenge_btn'] = Button("Time Challenge", color=color.white, highlight_color=color.white66, pressed_color=color.white, text_color=color.black, scale=(0.25, 0.1), origin=(0, 0))
    display['time_challenge_btn'].on_click = change_to_time_challenge

    display['back_btn'] = Button("Back", color=color.white, highlight_color=color.light_gray, pressed_color=color.gray, text_color=color.black, scale=(0.25, 0.1), origin=(0, 1.5))
    display['back_btn'].on_click = change_to_main_menu

def change_to_select_mode():
    global game_mode
    game_mode = False
    destroy_displayed_entity()
    display_select_mode()

# Free Mode
def display_free_mode():
    global popup_menu

    display['bg_music'] = Audio('pokemon.wav', 1.0, loop=True)

    display['LEFT'] = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
    display['BOTTOM'] = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
    display['FACE'] = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
    display['BACK'] = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
    display['TOP'] = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
    display['RIGHT'] = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
    display['CENTER_X'] = {Vec3(0, y, z) for y in range(-1, 2) for z in range(-1, 2)}
    display['CENTER_Y'] = {Vec3(x, 0, z) for x in range(-1, 2) for z in range(-1, 2)}
    display['CENTER_Z'] = {Vec3(x, y, 0) for x in range(-1, 2) for y in range(-1, 2)}

    display['SIDE_POSITIONS'] = display['LEFT'] | display['BOTTOM'] | display['FACE'] | display['BACK'] | display['TOP'] | display['RIGHT'] | display['CENTER_X'] | display['CENTER_Y'] | display['CENTER_Z']

    display['sky'] = Entity(model='quad', scale=60, texture='white_cube', texture_scaler=(60, 60), rotation_x=90, y=-5, color=color.light_gray)

    display['ground'] = Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)

    display['parent'] = Entity()

    display['CUBES'] = [Entity(model='models/custom_cube', texture='textures/rubik_texture', position=pos) for pos in display['SIDE_POSITIONS']]

    display['popup'] = WindowPanel(
        'Kesulitan',
        content=(
            Button("Mudah", color=color.azure),
            Button("Medium", color=color.azure),
            Button("Sulit", color=color.azure),
            Button("Kembali ke Menu", color=color.red)
        ),
        lock=Vec3(1, 1, 1)
    )
    display['popup'].y = display['popup'].panel.scale_y / 2 * display['popup'].scale_y
    display['popup'].content[0].on_click = mudah_option
    display['popup'].content[1].on_click = medium_option
    display['popup'].content[2].on_click = sulit_option
    display['popup'].content[3].on_click = change_to_main_menu

    popup_menu = True

    display['original_position'] = [{'pos': cube.world_position, 'rot': cube.world_rotation} for cube in display['CUBES']]

    display['rotation_axes'] = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z', 'CENTER_X': 'x', 'CENTER_Y': 'y', 'CENTER_Z': 'z'}

    display['cubes_side_positions'] = {'LEFT': display['LEFT'], 'BOTTOM': display['BOTTOM'], 'RIGHT': display['RIGHT'], 'FACE': display['FACE'], 'BACK': display['BACK'], 'TOP': display['TOP'], 'CENTER_X': display['CENTER_X'], 'CENTER_Y': display['CENTER_Y'], 'CENTER_Z': display['CENTER_Z']}

    display['animation_time'] = 0.3

    display['action_trigger'] = True

    display['info_text'] = Text("Shuffle", color=color.light_gray, origin=(9, -18.3))
    display['info_text'].enabled = False

    display['front_text'] = Text("Front View (Red Side)", scale=15, position=Vec3(1.3, 0, -20), rotation_y=180)
    display['front_text'].parent = scene

    display['left_text'] = Text("Left View (Yellow Side)", scale=15, position=Vec3(20, 0, 1.3), rotation_y=90)
    display['left_text'].parent = scene

    display['right_text'] = Text("Right View (White Side)", scale=15, position=Vec3(-20, 0, -1.3), rotation_y=-90)
    display['right_text'].parent = scene

    display['back_text'] = Text("Back View (Orange Side)", scale=15, position=Vec3(-1.3, 0, 20))
    display['back_text'].parent = scene

    display['timer'] = Text(str(waktu_bermain).split(".")[0], origin=(0, -18), color=color.white)
    display['timer'].create_background(0.035, radius=0.010)

    display['minus_volume_btn'] = Button("-", scale=(0.05, 0.05), origin=(1.05, 9))
    display['minus_volume_btn'].on_click = reduce_volume
    display['minus_volume_btn'].enabled = False

    display['volume_value'] = Text(display['bg_music'].volume, origin=(0, 18), color=color.black)
    display['volume_value'].enabled = False

    display['volume_title'] = Text("Volume", origin=(0, 16), color=color.black)
    display['volume_title'].enabled = False

    display['plus_volume_btn'] = Button("+", scale=(0.05, 0.05), origin=(-1.05, 9), enabled=True)
    display['plus_volume_btn'].on_click = add_volume
    display['plus_volume_btn'].enabled = False

    display['back_to_menu'] = Button('Back to Menu', scale=(0.2, 0.06), origin=(-3.3, 7.5))
    display['back_to_menu'].on_click = change_to_main_menu
    display['back_to_menu'].enabled = False

    display['editor_camera'] = EditorCamera()
    camera.world_position = (0, 0, 15)

def change_to_free_mode():
    global game_mode
    global waktu_bermain

    waktu_bermain = datetime.timedelta()
    game_mode = 'Free'
    destroy_displayed_entity()
    display_free_mode()

# Time Challenge Mode
def display_time_challenge_mode():
    global popup_menu

    display['bg_music'] = Audio('pokemon.wav', 1.0, loop=True)

    display['LEFT'] = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
    display['BOTTOM'] = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
    display['FACE'] = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
    display['BACK'] = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
    display['TOP'] = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
    display['RIGHT'] = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
    display['CENTER_X'] = {Vec3(0, y, z) for y in range(-1, 2) for z in range(-1, 2)}
    display['CENTER_Y'] = {Vec3(x, 0, z) for x in range(-1, 2) for z in range(-1, 2)}
    display['CENTER_Z'] = {Vec3(x, y, 0) for x in range(-1, 2) for y in range(-1, 2)}

    display['SIDE_POSITIONS'] = display['LEFT'] | display['BOTTOM'] | display['FACE'] | display['BACK'] | display['TOP'] | display['RIGHT'] | display['CENTER_X'] | display['CENTER_Y'] | display['CENTER_Z']

    display['sky'] = Entity(model='quad', scale=60, texture='white_cube', texture_scaler=(60, 60), rotation_x=90, y=-5, color=color.light_gray)

    display['ground'] = Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)

    display['parent'] = Entity()

    display['CUBES'] = [Entity(model='models/custom_cube', texture='textures/rubik_texture', position=pos) for pos in display['SIDE_POSITIONS']]

    display['popup'] = WindowPanel(
        'Kesulitan',
        content=(
            Button("Mudah", color=color.azure),
            Button("Medium", color=color.azure),
            Button("Sulit", color=color.azure),
            Button("Kembali ke Menu", color=color.red)
        ),
        lock=Vec3(1, 1, 1)
    )
    display['popup'].y = display['popup'].panel.scale_y / 2 * display['popup'].scale_y
    display['popup'].content[0].on_click = mudah_option
    display['popup'].content[1].on_click = medium_option
    display['popup'].content[2].on_click = sulit_option
    display['popup'].content[3].on_click = change_to_main_menu

    popup_menu = True

    display['original_position'] = [{'pos': cube.world_position, 'rot': cube.world_rotation} for cube in display['CUBES']]

    display['rotation_axes'] = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z', 'CENTER_X': 'x', 'CENTER_Y': 'y', 'CENTER_Z': 'z'}

    display['cubes_side_positions'] = {'LEFT': display['LEFT'], 'BOTTOM': display['BOTTOM'], 'RIGHT': display['RIGHT'], 'FACE': display['FACE'], 'BACK': display['BACK'], 'TOP': display['TOP'], 'CENTER_X': display['CENTER_X'], 'CENTER_Y': display['CENTER_Y'], 'CENTER_Z': display['CENTER_Z']}

    display['animation_time'] = 0.3

    display['action_trigger'] = True

    display['info_text'] = Text("Shuffle", color=color.light_gray, origin=(9, -18.3))
    display['info_text'].enabled = False

    display['front_text'] = Text("Front View (Red Side)", scale=15, position=Vec3(1.3, 0, -20), rotation_y=180)
    display['front_text'].parent = scene

    display['back_text'] = Text("Back View (Orange Side)", scale=15, position=Vec3(-1.3, 0, 20))
    display['back_text'].parent = scene

    display['timer'] = Text(str(waktu_bermain).split(".")[0], origin=(0, -18), color=color.white)
    display['timer'].create_background(0.035, radius=0.010)

    display['minus_volume_btn'] = Button("-", scale=(0.05, 0.05), origin=(1.05, 9))
    display['minus_volume_btn'].on_click = reduce_volume
    display['minus_volume_btn'].enabled = False

    display['volume_value'] = Text(display['bg_music'].volume, origin=(0, 18), color=color.black)
    display['volume_value'].enabled = False

    display['volume_title'] = Text("Volume", origin=(0, 16), color=color.black)
    display['volume_title'].enabled = False

    display['plus_volume_btn'] = Button("+", scale=(0.05, 0.05), origin=(-1.05, 9), enabled=True)
    display['plus_volume_btn'].on_click = add_volume
    display['plus_volume_btn'].enabled = False

    display['back_to_menu'] = Button('Back to Menu', scale=(0.2, 0.06), origin=(-3.3, 7.5))
    display['back_to_menu'].on_click = change_to_main_menu
    display['back_to_menu'].enabled = False

    display['editor_camera'] = EditorCamera()
    camera.world_position = (0, 0, 15)

def change_to_time_challenge():
    global game_mode
    global waktu_bermain

    waktu_bermain = datetime.timedelta()
    game_mode = 'Time'
    destroy_displayed_entity()
    display_time_challenge_mode()

# --- Utility for Gameplay ---
def toggle_animation_trigger():
    if game_mode:
        global display
        global shuffle_mode
        global last_shuffle_check
        global popup_menu
        display['action_trigger'] = not display['action_trigger']

        if display['action_trigger'] and not shuffle_mode:
            if last_shuffle_check:
                last_shuffle_check = False
            elif is_solved():
                popup_menu = True
                display['popup_win'] = WindowPanel(
                    'Selamat !',
                    content=(
                        Text("Kamu Berhasil Menyelesaikan Rubik"),
                        Text("Waktu:"),
                        Text(str(waktu_bermain).split(".")[0]),
                        Button("Kembali ke Menu", color=color.azure)
                    ),
                    lock=Vec3(1, 1, 1)
                )

                display['popup_win'].y = display['popup_win'].panel.scale_y / 2 * display['popup_win'].scale_y
                display['popup_win'].content[3].on_click = change_to_main_menu

def is_solved():
    solved = True
    for cube, original_cube in zip(display['CUBES'], display['original_position']):
        if (not is_vector3_same(cube.world_position, original_cube['pos'])) and (not is_vector3_same(cube.world_rotation, original_cube['rot'])):
            solved = False

    return solved

def is_vector3_same(vector1: Vec3, vector2: Vec3):
    same = True
    if round(vector1.x) != round(vector2.x):
        same = False
    if round(vector1.y) != round(vector2.y):
        same = False
    if round(vector1.z) != round(vector2.z):
        same = False
    
    return same

def reparent_to_scene():
    if game_mode:
        global display
        for cube in display['CUBES']:
            if cube.parent == display['parent']:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot

        display['parent'].rotation = 0

def rotate_side(side_name):
    if game_mode:
        global display
        display['action_trigger'] = False
        cube_positions = display['cubes_side_positions'][side_name]
        rotation_axis = display['rotation_axes'][side_name]
        reparent_to_scene()
        for cube in display['CUBES']:
            if cube.position in cube_positions:
                cube.parent = display['parent']
                if rotation_axis == 'x':
                    display['parent'].animate_rotation((90, 0, 0), display['animation_time'])
                elif rotation_axis == 'y':
                    display['parent'].animate_rotation((0, 90, 0), display['animation_time'])
                else:
                    display['parent'].animate_rotation((0, 0, 90), display['animation_time'])
        invoke(toggle_animation_trigger, delay=display['animation_time'] + 0.11)

def rotate_side_reverse(side_name):
    if game_mode:
        global display
        display['action_trigger'] = False
        cube_positions = display['cubes_side_positions'][side_name]
        rotation_axis = display['rotation_axes'][side_name]
        reparent_to_scene()
        for cube in display['CUBES']:
            if cube.position in cube_positions:
                cube.parent = display['parent']
                if rotation_axis == 'x':
                    display['parent'].animate_rotation((-90, 0, 0), display['animation_time'])
                elif rotation_axis == 'y':
                    display['parent'].animate_rotation((0, -90, 0), display['animation_time'])
                else:
                    display['parent'].animate_rotation((0, 0, -90), display['animation_time'])
        invoke(toggle_animation_trigger, delay=display['animation_time'] + 0.11)

def get_combined_key(key):
    return ''.join(e+'+' for e in ('control', 'shift', 'alt') if held_keys[e] and not e == key) + key

def input(key):
    if game_mode and not popup_menu:
        global display
        key = get_combined_key(key)
        keys = {
            'a': 'LEFT',
            's': 'CENTER_X',
            'd': 'RIGHT',
            'q': 'TOP',
            'w': 'CENTER_Y',
            'e': 'BOTTOM',
            'z': 'FACE',
            'x': 'CENTER_Z',
            'c': 'BACK',
        }

        keys_reverse = {
            'shift+a': 'LEFT',
            'shift+s': 'CENTER_X',
            'shift+d': 'RIGHT',
            'shift+q': 'TOP',
            'shift+w': 'CENTER_Y',
            'shift+e': 'BOTTOM',
            'shift+z': 'FACE',
            'shift+x': 'CENTER_Z',
            'shift+c': 'BACK',
        }

        if key in keys and display['action_trigger'] and not shuffle_mode:
            rotate_side(keys[key])
        if key in keys_reverse and display['action_trigger'] and not shuffle_mode:
            rotate_side_reverse(keys_reverse[key])

def update():
    if game_mode:
        global shuffle_mode
        global waktu_delay
        global shuffle_steps
        global waktu_bermain
        global popup_menu
        if shuffle_mode:
            if waktu_delay.total_seconds() >= 0:
                waktu_delay -= detik
            else:
                waktu_delay = datetime.timedelta(milliseconds=420)

                side_name = random.choice(list(display['rotation_axes'].keys()))
                move = random.choice(['forward', 'reverse'])

                if move == 'forward':
                    rotate_side(side_name)
                else:
                    rotate_side_reverse(side_name)
                
                shuffle_steps -= 1

                if shuffle_steps == 0:
                    shuffle_mode = False
                    display['info_text'].text = "Play"
                    display['info_text'].origin = (15.5, -18.3)
                    display['info_text'].color = color.white

        elif game_mode == 'Free' and not popup_menu:
            waktu_bermain += detik
            display['timer'].text = str(waktu_bermain).split(".")[0]
        elif game_mode == 'Time' and not popup_menu:
            if waktu_bermain.total_seconds() > 0.1:
                waktu_bermain -= detik
                display['timer'].text = str(waktu_bermain).split(".")[0]
            else:
                popup_menu = True
                display['popup_lose'] = WindowPanel(
                    'Gagal !',
                    content=(
                        Text("Kamu Gagal Menyelesaikan Rubik"),
                        Button("Kembali ke Menu", color=color.red)
                    ),
                    lock=Vec3(1, 1, 1)
                )

                display['popup_lose'].y = display['popup_lose'].panel.scale_y / 2 * display['popup_lose'].scale_y
                display['popup_lose'].content[1].on_click = change_to_main_menu

# --- Gameplay Button ---
def mudah_option():
    global kesulitan
    global popup_menu
    global display

    if game_mode == 'Time':
        global waktu_bermain
        waktu_bermain = datetime.timedelta(minutes=15)
    popup_menu = False
    kesulitan = "Mudah"
    destroy(display['popup'])
    del display['popup']
    for entitas in display:
        if hasattr(display[entitas], 'enabled') and display[entitas].enabled != True:
            display[entitas].enabled = True
    shuffle_rubic()

def medium_option():
    global kesulitan
    global popup_menu
    global display

    if game_mode == 'Time':
        global waktu_bermain
        waktu_bermain = datetime.timedelta(minutes=10)
    popup_menu = False
    kesulitan = "Medium"
    destroy(display['popup'])
    del display['popup']
    for entitas in display:
        if hasattr(display[entitas], 'enabled') and display[entitas].enabled != True:
            display[entitas].enabled = True
    shuffle_rubic()

def sulit_option():
    global kesulitan
    global popup_menu
    global display

    if game_mode == 'Time':
        global waktu_bermain
        waktu_bermain = datetime.timedelta(minutes=7)
    popup_menu = False
    kesulitan = "Sulit"
    destroy(display['popup'])
    del display['popup']
    for entitas in display:
        if hasattr(display[entitas], 'enabled') and display[entitas].enabled != True:
            display[entitas].enabled = True
    shuffle_rubic()

def shuffle_rubic():
    if game_mode:
        global shuffle_steps
        global shuffle_mode
        global last_shuffle_check
        global kesulitan

        shuffle_mode = True
        last_shuffle_check = True

        if kesulitan == 'Mudah':
            shuffle_steps = random.randint(7, 10)
        elif kesulitan == 'Medium':
            shuffle_steps = random.randint(15, 20)
        else:
            shuffle_steps = random.randint(30, 40)

def add_volume():
    if game_mode:
        global display
        if display['bg_music'].volume < 10:
            display['bg_music'].volume += 0.5
            display['volume_value'].text = display['bg_music'].volume

def reduce_volume():
    if game_mode:
        global display
        if display['bg_music'].volume > 0:
            display['bg_music'].volume -= 0.5

            if display['bg_music'].volume == 0:
                display['volume_value'].text = "0"
            else:
                display['volume_value'].text = display['bg_music'].volume

# --- Utility ---
def destroy_displayed_entity():
    for key in display.copy():
        if key == 'CUBES':
            for cube in display[key]:
                destroy(cube)
            del display[key]
        else:
            if hasattr(display[key], 'eternal'):
                destroy(display[key])
            del display[key]

def destroy_entity(entitas: str):
    destroy(display[entitas])
    del display[entitas]

# Start the Game
display_main_menu()

app.run()