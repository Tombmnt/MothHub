

class Data_Handler():
    def __init__(self) -> None:
        #TODO: implement innerworkings properly
        self.speed = 0

    #TODO: make this return actual speed
    def get_speed(self) -> int:
        self.speed += 1
        return self.speed