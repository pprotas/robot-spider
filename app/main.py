from movement.movement import Movement

if __name__ == '__main__':
    movement = Movement('/dev/ttyUSB0')
    movement.move_servo(1, 999)