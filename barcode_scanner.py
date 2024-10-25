import evdev
import select

class BarcodeScanner:
    def __init__(self, device_name='/dev/input/event0'):  # Adjust device name as needed
        self.device = evdev.InputDevice(device_name)

    def read_barcode(self, timeout=1):
        barcode = ""
        while True:
            r, w, x = select.select([self.device], [], [], timeout)
            if r:
                for event in self.device.read():
                    if event.type == evdev.ecodes.EV_KEY:
                        data = evdev.categorize(event)
                        if data.keystate == 1:  # Key down event
                            if data.scancode == 28:  # Enter key
                                return self.clean_isbn(barcode)
                            else:
                                key = evdev.ecodes.KEY[data.scancode]
                                if key.isdigit() or key in 'X':
                                    barcode += key
            else:
                # Timeout occurred
                return None

    def clean_isbn(self, isbn):
        # Remove any non-digit or 'X' characters
        cleaned = ''.join(char for char in isbn if char.isdigit() or char == 'X')
        # Ensure it's either 10 or 13 digits long
        if len(cleaned) in (10, 13):
            return cleaned
        return None
