class Lightbulb:
    def __init__(self):
        self.state = "off"

    def change_state(self):
        self.state = "on" if self.state == "off" else "off"
        print(f"Turning the light {self.state}")