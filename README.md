# EMDR Bilateral Stimulation Device Controller

## Introduction

This project provides a web-based controller for an EMDR (Eye Movement Desensitization and Reprocessing) bilateral stimulation device used in remote therapy sessions. The code is designed to run on a microcontroller with Wi-Fi capabilities, such as the **Raspberry Pi Pico W**, and allows therapists and clients to control the device remotely via a web interface.

EMDR therapy is a form of psychotherapy that helps individuals heal from traumatic experiences. Bilateral stimulation, a core component of EMDR, involves alternating stimuli (like tactile vibrations) to both sides of the body, facilitating the processing of distressing memories and emotions.

## Features

- **Web-Based Interface**: Control the device from any web browser connected to the same network.
- **Motor Control**: Adjust the intensity and frequency of two vibration motors independently.
- **Bilateral Stimulation**: Automatic alternation between motors with adjustable cycle times.
- **Preset Modes**: Quickly start sessions with predefined settings for desensitization and reprocessing phases.
- **Session Timer**: Monitor the elapsed time of the therapy session.
- **Responsive Design**: User interface adapts to various screen sizes for accessibility on different devices.

## Hardware Requirements

- **Microcontroller**: Raspberry Pi Pico W or any MicroPython-compatible microcontroller with Wi-Fi capabilities.
- **Vibration Motors**: Two PWM-compatible vibration motors.
- **Connectivity**: Wi-Fi network for connecting the microcontroller and client device.
- **Miscellaneous**: Wires, breadboard, and power supply suitable for the microcontroller and motors.

## Software Requirements

- **MicroPython**: The microcontroller must be running MicroPython firmware.
- **Microdot**: A minimal web framework for MicroPython.
- **Python Libraries**: Standard MicroPython libraries (`network`, `time`, `machine`, `json`).

## Setup and Installation

### 1. Flash MicroPython Firmware

If not already done, flash the MicroPython firmware onto your microcontroller. Follow the [official MicroPython documentation](https://micropython.org/download/) for your specific device.

### 2. Install Microdot

Microdot can be installed by uploading the `microdot.py` file to your microcontroller's filesystem. Download it from the [Microdot repository](https://github.com/miguelgrinberg/microdot).

### 3. Upload Code Files

Upload the following files to the microcontroller's filesystem:

- `main.py`: The main script that runs the web server and controls the motors.
- `index.html`: The web interface served to clients.

### 4. Hardware Setup

- **Connect Motors**: Attach the two vibration motors to GPIO pins on the microcontroller (pins **15** and **14** by default).
- **PWM Pins**: Ensure the chosen pins support PWM output.
- **Power Supply**: Verify that the microcontroller and motors are powered appropriately, considering voltage and current requirements.

### 5. Configure Wi-Fi Credentials

Edit the `main.py` file to set your Wi-Fi network credentials:

```python
SSID = "your_wifi_ssid"
PASSWORD = "your_wifi_password"
```

### 6. Run the Application

Upon powering the microcontroller, it should automatically run `main.py`. The script will connect to the Wi-Fi network and start the web server.

Check the serial console output to find the IP address assigned to the microcontroller:

```shell
Connected, IP address: 192.168.X.X
```

## Usage

### Accessing the Web Interface

- On a device connected to the same Wi-Fi network, open a web browser.
- Navigate to the IP address displayed by the microcontroller (e.g., `http://192.168.X.X`).
- The web interface looks like this.

![Screenshot 2024-11-06 at 1 30 02 PM](https://github.com/user-attachments/assets/94d46d98-0922-437f-88b7-48eb367de551)


### User Interface Overview

#### Master Control

- **START/STOP Button**: Initiates or stops a therapy session.
- **Mode Selection Modal**: Appears upon starting a session, allowing selection between **Desensitize** and **Reprocess** modes with predefined settings.
- The mode selector window opens with the device is started. 
![Screenshot 2024-11-06 at 1 30 07 PM](https://github.com/user-attachments/assets/da281f77-40d4-4dff-8f20-ccdff1b00d0d)

#### Session Information

- **Elapsed Time**: Displays the duration of the current session.

#### Animation

- Visual indicators show which motor is active, enhancing the bilateral stimulation experience.

#### Motor Controls

- **Intensity Sliders**: Adjust the vibration intensity (5% - 100%) for each motor.
- **Frequency Sliders**: Adjust the PWM frequency (1 Hz - 100 Hz) for each motor.

#### Bilateral Controls

- **Cycle Time Slider**: Adjusts the interval at which the motors alternate (100 ms - 3000 ms).

#### Apply Button

- **Apply Settings**: Applies any changes made to the motor and bilateral settings during an active session.

### Starting a Session

1. Click the **START** button.
2. Choose a mode in the modal dialog:
   - **Desensitize**: Uses higher intensity and frequency with a faster alternation cycle.
   - **Reprocess**: Uses lower intensity and frequency with a slower alternation cycle.
3. The session begins, and the elapsed time starts counting.
4. Visual indicators show which motor is active.

### Adjusting Settings During a Session

- Modify the sliders to adjust intensity, frequency, and cycle time.
- Click **Apply** to send the new settings to the device.

### Stopping a Session

- Click the **STOP** button to end the session.
- Motors will stop, and timers reset.

## Customization

### Changing GPIO Pins

To change the GPIO pins used for the motors, update the `motors` dictionary in `main.py`:

```python
motors = {
    'MOTOR1': {
        'pin': Pin(YOUR_PIN_NUMBER_1, Pin.OUT),
        'pwm': None,
        'intensity': 0,
        'frequency': 1000
    },
    'MOTOR2': {
        'pin': Pin(YOUR_PIN_NUMBER_2, Pin.OUT),
        'pwm': None,
        'intensity': 0,
        'frequency': 1000
    }
}
```

### Adjusting Preset Modes

Modify the `modePresets` object in `index.html` to change the predefined settings for the modes:

```javascript
const modePresets = {
    desensitize: {
        motor1: { intensity: 70, frequency: 80 },
        motor2: { intensity: 70, frequency: 80 },
        bilateral: { interval: 500 } // 0.5 seconds
    },
    reprocess: {
        motor1: { intensity: 30, frequency: 70 },
        motor2: { intensity: 30, frequency: 70 },
        bilateral: { interval: 1500 } // 1.5 seconds
    }
};
```

Adjust the values to suit your requirements.

### User Interface Customization

Feel free to modify the `index.html` file to adjust the look and feel of the web interface. Ensure that any changes to element IDs or classes are reflected in the corresponding JavaScript code.

## Troubleshooting

### Cannot Connect to Wi-Fi

- **Check Credentials**: Ensure that the SSID and password in `main.py` are correct.
- **Network Range**: Make sure the microcontroller is within range of the Wi-Fi network.
- **Network Compatibility**: Ensure your network supports the microcontroller (e.g., 2.4 GHz Wi-Fi).

### Web Interface Not Loading

- **Correct IP Address**: Verify you are using the correct IP address as displayed on the serial console.
- **Same Network**: Ensure your client device is connected to the same Wi-Fi network.
- **Firewall Settings**: Check that your network allows communication between devices.

### Motors Not Vibrating

- **Hardware Connections**: Confirm that the motors are correctly connected to the specified GPIO pins.
- **PWM Support**: Ensure the chosen GPIO pins support PWM.
- **Power Supply**: Verify that the motors are receiving sufficient power.
- **Intensity Settings**: Make sure the intensity is set above the minimum threshold (5%).

### Session Timer Not Working

- **JavaScript Enabled**: Ensure that JavaScript is enabled in your web browser.
- **Browser Compatibility**: Use a modern web browser that supports ES6 JavaScript features.
- **Console Errors**: Check the browser's developer console for any JavaScript errors.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute as per the license terms.

## Acknowledgements

- **Microdot**: A minimal web framework for MicroPython by Miguel Grinberg.
- **MicroPython**: Python for microcontrollers.

## Contact

For questions or support, please reach out to the project maintainer.

---

*Note: This device and software are intended for use by professionals trained in EMDR therapy. Always ensure compliance with relevant regulations and guidelines when using therapeutic devices.*
