import matplotlib

class PICCodeGenerator:
  def __init__(self, mat_size, led_delay, animation_hz):
    self.__mat_size = mat_size
    self.__led_delay = led_delay
    self.__animation_hz = animation_hz
    self.__str_code = ''