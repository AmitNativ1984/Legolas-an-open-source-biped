Connecting Servos with Jetson Orin Nano using PCA9685
=====================================================

This guide provides an overview of how to connect and control servo motors with the Jetson Orin Nano using the PCA9685 PWM driver.
It will cover the hardware connections, software setup, and code examples to control the servos, and provide a step-by-step guide to get you started.

Requirements
------------
- Jetson Orin Nano Dev Kit
- PCA9685 PWM driver
- Servo motors
- Jumper wires
- Power supply for servos (optional)

PCA9685 Board
-------------
The PCA9685 is a 16-channel, 12-bit PWM driver that can be used to control multiple servo motors with a single I2C interface.
**PMW** stands for Pulse Width Modulation. The input to a servo motor is a square wave signal with a fixed frequency (typically 50 Hz) and a variable duty cycle. The duty cycle determines the position (angle) of the servo motor.

.. image:: https://cdn.getmidnight.com/84f7b02a8128f5f5775611244c24b941/2023/02/ServoGif.gif
   :alt: Servo Motor Animation
   :align: center


.. image:: /home/amit/DEV/Legolas-an-open-source-biped/assets/PCA9685-16-channel-servo-motor-driver-pinout.jpg
   :alt: PCA9685 PWM Driver
   :align: center
    

The Jetson Orin Nano Dev Kit comes with a 40-Pin Expansion Header (see the `Jetson Orin Nano Pinout <https://developer.download.nvidia.com/assets/embedded/secure/jetson/orin_nano/docs/Jetson-Orin-Nano-DevKit-Carrier-Board-Specification_SP-11324-001_v1.3.pdf?__token__=exp=1737239397~hmac=493f08d5f376e05f129f140493483eb83d5e8ca032cefe7e76faf614999b4b0f&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9>`_ for more details)
Each pin controls a different function. 

.. image:: assets/Jetson-orin-nano-40-pin-connections.png
   :alt: Jetson Orin Nano 40 Pin Expansion Header
   :align: center

Here are the connections between the dev kit, and the PCA9685:

Pinout Table
------------
+-------------+-----------------------------------------------------------+--------------------------------------------+
| PCA9685 Pin | Description                                               | Jetson Orin Nano Dev Kit 40-Pin Expanstion |
+=============+===========================================================+============================================+
| GND         | Ground pin                                                | 6                                          |
+-------------+-----------------------------------------------------------+--------------------------------------------+
| OE          | OutputEnable. (LOW by defualt making all outputs enabled) | (?) Not connected                          |
+-------------+-----------------------------------------------------------+--------------------------------------------+
| SCL         | I2C **clock** pin                                         | 5 (I2C_SCL)                                |
+-------------+-----------------------------------------------------------+--------------------------------------------+
| SDA         | I2C **data** pin                                          | 3 (I2C_SDA)                                |
+-------------+-----------------------------------------------------------+--------------------------------------------+
| VCC         | Logic power pin (3V-5V)                                   | 1 (3.3V-5V)                                |
+-------------+-----------------------------------------------------------+--------------------------------------------+
| V+          | External Servo power pin (5V-6V)                          | 2 (Main 5.0V supply)                       |
+-------------+-----------------------------------------------------------+--------------------------------------------+




1. **Power the PCA9685 and Servos:**
    - Connect the V+ pin of the PCA9685 to an external power supply suitable for your servos (typically 5-6V).
    - Ensure the GND of the external power supply is connected to the GND of the PCA9685.

2. **Connect the Servos to the PCA9685:**
    - Connect the control wire of each servo to one of the PWM output channels on the PCA9685.
    - Connect the power and ground wires of the servos to the corresponding V+ and GND pins on the PCA9685.

3. **Install Required Libraries:**
    - Install the Adafruit PCA9685 library on the Jetson Orin Nano using pip:
      ```
      pip install adafruit-circuitpython-pca9685
      ```

4. **Write and Run the Control Script:**
    - Create a Python script to control the servos. Below is an example script:
      ```python
      import time
      from board import SCL, SDA
      import busio
      from adafruit_pca9685 import PCA9685
      from adafruit_motor import servo

      # Create the I2C bus interface
      i2c_bus = busio.I2C(SCL, SDA)

      # Create a simple PCA9685 class instance
      pca = PCA9685(i2c_bus)
      pca.frequency = 50

      # Create a servo object for each servo
      servo0 = servo.Servo(pca.channels[0])
      servo1 = servo.Servo(pca.channels[1])

      # Move servos to different angles
      servo0.angle = 90
      time.sleep(1)
      servo1.angle = 45
      time.sleep(1)

      # Cleanup
      pca.deinit()
      ```

By following these steps, you should be able to successfully connect and control servo motors using the PCA9685 PWM driver with your Jetson Orin Nano Dev Kit.