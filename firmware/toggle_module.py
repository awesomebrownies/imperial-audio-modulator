from kmk.modules import Module
import digitalio
import usb_hid

class ToggleModule(Module):
    def __init__(self, pins, actions=None):
        self.pins = pins
        self.toggles = []
        self.last_states = []
        
        # Find or create custom HID device
        self.hid_device = None
        for device in usb_hid.devices:
            if device.usage == 0x10:  # Custom usage
                self.hid_device = device
                break
        
        for pin in pins:
            sw = digitalio.DigitalInOut(pin)
            sw.switch_to_input(pull=digitalio.Pull.UP)
            self.toggles.append(sw)
            self.last_states.append(sw.value)
    
    def during_bootup(self, keyboard):
        return
    
    def before_matrix_scan(self, keyboard):
        return
    
    def after_matrix_scan(self, keyboard):
        state_changed = False
        for i, toggle in enumerate(self.toggles):
            current = toggle.value
            if current != self.last_states[i]:
                self.last_states[i] = current
                state_changed = True
        
        if state_changed and self.hid_device:
            self.send_toggle_report()
        
        return
        
    def send_toggle_report(self):
        state = 0
        for i, toggle_state in enumerate(self.last_states):
            if not toggle_state:
                state |= (1 << i)
        
        try:
            self.hid_device.send_report(bytes([state]))
        except Exception as e:
            print(f"Failed to send HID report: {e}")

    # ==== START MOD ====
    def all_toggles_on(self):
        # Pulled LOW == ON
        for state in self.last_states:
            if state:  # HIGH == OFF
                return False
        return True
    # ==== END MOD ====
    
    def before_hid_send(self, keyboard):
        return
    
    def after_hid_send(self, keyboard):
        return
