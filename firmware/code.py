import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
from toggle_module import ToggleModule

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())

# ==== START MOD: Subclass EncoderHandler for callbacks ====
class MyEncoderHandler(EncoderHandler):
    def __init__(self):
        super().__init__()
        self.on_rotate = None
        self.on_press = None

    def on_move_do(self, keyboard, encoder_id, state):
        if self.on_rotate:
            self.on_rotate(keyboard, encoder_id, state['direction'] > 0)
        else:
            super().on_move_do(keyboard, encoder_id, state)

    def on_button_do(self, keyboard, encoder_id, state):
        if self.on_press:
            self.on_press(keyboard, encoder_id, state['is_pressed'])
        else:
            super().on_button_do(keyboard, encoder_id, state)
# ==== END MOD ====

encoder_handler = MyEncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = (
    (board.D9, board.D6, board.D10, False),
)

# Disable default KMK encoder behavior
encoder_handler.map = [
    ((KC.NO, KC.NO, KC.NO),)
]

toggle_module = ToggleModule(
    pins=[board.D3, board.D4, board.D5],
)
keyboard.modules.append(toggle_module)

keyboard.col_pins = ()
keyboard.row_pins = ()
keyboard.keymap = [[]]

# ==== START MOD: Helper functions ====
def send_encoder_hid(hid_device, code):
    try:
        hid_device.send_report(bytes([code]))
    except Exception as e:
        print("Encoder HID send failed:", e)

def encoder_callback(keyboard, encoder, clockwise):
    if toggle_module.all_toggles_on():
        if clockwise:
            keyboard.tap_key(KC.VOLD)
        else:
            keyboard.tap_key(KC.VOLU)
        return

    hid = toggle_module.hid_device
    if not hid:
        return

    if clockwise:
        send_encoder_hid(hid, 0b11000000) # Volume Down
    else:
        send_encoder_hid(hid, 0b11000001)  # Volume Up

def encoder_press_callback(keyboard, encoder, is_pressed):
    if is_pressed is False:
        return

    if toggle_module.all_toggles_on():
        keyboard.tap_key(KC.MUTE)
        return

    hid = toggle_module.hid_device
    if hid:
        send_encoder_hid(hid, 0b10000000)  # Toggle Mute

# Assign the callbacks
encoder_handler.on_rotate = encoder_callback
encoder_handler.on_press = encoder_press_callback
# ==== END MOD ====

if __name__ == '__main__':
    keyboard.go()