import network
import time
from microdot import Microdot, send_file
from machine import Pin, PWM, Timer
import json

# Wi-Fi credentials
SSID = "your wifi name"
PASSWORD = "your wifi password"

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for connection
max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(1)

if not wlan.isconnected():
    raise RuntimeError('Network connection failed')
else:
    status = wlan.ifconfig()
    print('Connected, IP address:', status[0])

# Start Microdot app
app = Microdot()

# Initialize motors
motors = {
    'MOTOR1': {
        'pin': Pin(15, Pin.OUT),
        'pwm': None,
        'intensity': 0,
        'frequency': 1000
    },
    'MOTOR2': {
        'pin': Pin(14, Pin.OUT),
        'pwm': None,
        'intensity': 0,
        'frequency': 1000
    }
}

# Ensure motors are off at startup
for motor in motors.values():
    motor['pin'].value(0)

# Function to set motor intensity
def set_motor_intensity(motor, intensity):
    if intensity > 0:
        # Initialize PWM if not already
        if motor['pwm'] is None:
            motor['pwm'] = PWM(motor['pin'])
        motor['pwm'].freq(motor['frequency'])
        # Set duty cycle
        duty = int(intensity * 65535 / 100)
        motor['pwm'].duty_u16(duty)
    else:
        # Deinitialize PWM and set pin low
        if motor['pwm'] is not None:
            motor['pwm'].duty_u16(0)
            motor['pwm'].deinit()
            motor['pwm'] = None
        motor['pin'].init(Pin.OUT)
        motor['pin'].value(0)

# Function to set motor frequency
def set_motor_frequency(motor, frequency):
    motor['frequency'] = frequency
    if motor['pwm'] is not None:
        motor['pwm'].freq(frequency)

# Bilateral stimulation variables
bilateral_interval = 1000  # milliseconds
bilateral_timer = Timer()

# Function to alternate motors
def alternate_motors(timer):
    global motors
    # Toggle MOTOR1
    if motors['MOTOR1'].get('is_on', False):
        # Turn off MOTOR1, turn on MOTOR2
        set_motor_intensity(motors['MOTOR1'], 0)
        set_motor_intensity(motors['MOTOR2'], motors['MOTOR2']['intensity'])
        motors['MOTOR1']['is_on'] = False
        motors['MOTOR2']['is_on'] = True
    else:
        # Turn off MOTOR2, turn on MOTOR1
        set_motor_intensity(motors['MOTOR2'], 0)
        set_motor_intensity(motors['MOTOR1'], motors['MOTOR1']['intensity'])
        motors['MOTOR1']['is_on'] = True
        motors['MOTOR2']['is_on'] = False

# Route to serve the interface HTML file
@app.route('/')
def index(request):
    return send_file('index.html')

# Route to control motor
@app.route('/motor/<motor_id>', methods=['POST'])
def control_motor(request, motor_id):
    if motor_id not in motors:
        return json.dumps({'error': 'Invalid motor ID'}), 400

    motor = motors[motor_id]
    data = request.json

    if 'intensity' in data:
        intensity = data['intensity']
        intensity = max(0, min(100, intensity))
        motor['intensity'] = intensity

    if 'frequency' in data:
        frequency = data['frequency']
        frequency = max(1, min(40000, frequency))
        motor['frequency'] = frequency
        set_motor_frequency(motor, frequency)

    response = {
        'intensity': motor['intensity'],
        'frequency': motor['frequency']
    }
    return json.dumps(response)

# Route for advanced control (bilateral stimulation)
@app.route('/advanced', methods=['POST'])
def advanced_control(request):
    global bilateral_interval, bilateral_timer, motors
    data = request.json

    if 'alternate_interval' in data:
        bilateral_interval = max(100, data['alternate_interval'])
        # Restart the timer with the new interval
        bilateral_timer.deinit()
        bilateral_timer.init(period=bilateral_interval, mode=Timer.PERIODIC, callback=alternate_motors)

    response = {
        'alternate_interval': bilateral_interval
    }
    return json.dumps(response)

# Start bilateral stimulation at startup
def start_bilateral_stimulation():
    global motors, bilateral_timer
    # Initialize is_on flags
    motors['MOTOR1']['is_on'] = True
    motors['MOTOR2']['is_on'] = False
    # Ensure both motors are off initially
    set_motor_intensity(motors['MOTOR2'], 0)
    set_motor_intensity(motors['MOTOR1'], motors['MOTOR1']['intensity'])
    # Start the timer
    bilateral_timer.init(period=bilateral_interval, mode=Timer.PERIODIC, callback=alternate_motors)

# Run the web server on port 80
if __name__ == '__main__':
    start_bilateral_stimulation()
    app.run(port=80)

