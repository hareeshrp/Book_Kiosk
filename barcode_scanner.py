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
                                return barcode
                            else:
                                barcode += evdev.ecodes.KEY[data.scancode]
            else:
                # Timeout occurred
                return None
