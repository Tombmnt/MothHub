from typing import List
import numpy as np
import threading
import pyglet
from ..generic_peripheral import Generic_Peripheral
from ..types.peripherals import peripheral_types

class Mock_Display_Peripheral(Generic_Peripheral):
    def __init__(self, w, h, periph_name: str, host_ip: str, port: int = None) -> None:
        super().__init__(peripheral_types.display, periph_name, host_ip, port)

        self.width = w
        self.height = h
        self.frame_data = np.zeros((h, w, 3), dtype=np.ubyte)
        self.frame_data[0:h, 0:w] = [150, 150, 150]
        
        self.speed = 0

        self.display = threading.Thread(target=self.display_thread, daemon=True).start()

    def convert_frame(self) -> List:
        raw_data = self.frame_data.flatten()
        return (pyglet.gl.glu.GLubyte * len(raw_data))(*raw_data)

    def run(self) -> None:
        while(1):
            data = self.socket_client.recieve_data()
            if(data):
                if(data["command"] == "square"):
                    self.add_colored_quare(data["pos_x"], data["pos_y"], data["width"], data["height"], data["color"])
                elif(data["command"] == "speed"):
                    self.speed = data["value"]

    # Draws a colored square on the screen
    # requires a "command" as a dict:
    #{
    #    "command":"square",
    #    "pos_x":0,
    #    "pos_y":0,
    #    "width":20,
    #    "height":20,
    #    "color":[255, 255, 255]
    #}
    def add_colored_quare(self, pos_x: int, pos_y: int, w: int, h: int, color) -> None:
        for x in range(0, w):
            for y in range(0, h):
                if(((x + pos_x) < self.width) and ((y + pos_y) < self.height)):
                    self.frame_data[y + pos_y, x + pos_x] = color

    def update_speed(self, new_speed) -> None:
        self.speed = new_speed

    def display_thread(self):
        window = pyglet.window.Window(self.width, self.height)
        speed_label = pyglet.text.Label(text='Speed: '+str(self.speed), font_size=36, color=(0, 0, 150, 255),
            anchor_x='center', anchor_y='center', x=window.width//2, y=window.height//2)

        @window.event
        def on_draw():
            window.clear()
            scr = pyglet.image.ImageData(self.width, self.height, 'RGB', self.convert_frame())
            scr.blit(0, 0)
            speed_label.draw()

        def update(dt):
            speed_label.text = 'Speed: '+str(self.speed)
            
        pyglet.clock.schedule_interval(update, 1/60)
        pyglet.app.run()