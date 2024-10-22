import evdev

class BarcodeScanner:
    def __init__(self, device_name='/dev/input/event0'):  # Adjust device name as needed
        self.device = evdev.InputDevice(device_name)

    def read_barcode(self):
        barcode = ""
        for event in self.device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                data = evdev.categorize(event)
                if data.keystate == 1:  # Key down event
                    if data.scancode == 28:  # Enter key
                        return barcode
                    else:
                        barcode += evdev.ecodes.KEY[data.scancode]
