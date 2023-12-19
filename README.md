LectureLookout
=====================================

Project Description
-------------------

Lecture Lookout is an application designed to interface with the USOS API of Poznan University of Technology. It allows users to access information about university buildings, rooms, and class schedules. The project utilizes a Raspberry Pi with connected hardware components like an LCD display and buttons to navigate through the information.

Features
--------

-   Retrieve building and room information from the USOS API.
-   Display class schedules for specific rooms.
-   Hardware interaction using a Raspberry Pi, including an LCD display and buttons for user input.

Hardware Requirements
---------------------

-   Raspberry Pi (Any model compatible with GPIO pins)
-   Character LCD Display (16x2)
-   Digital I/O Pins
-   Buttons for navigation

Installation
------------

1.  Clone the repository to your Raspberry Pi.
2.  Install necessary Python libraries:

`pip install flask dotenv RPi.GPIO adafruit-circuitpython-charlcd`

3.  Set up your `.env` file with your `consumer_key` and `consumer_secret` for the USOS API.

Usage
-----

1.  Run `main.py` to start the Flask server and initialize the hardware components.

    `python3 main.py`

2.  Access the web application through a browser at `http://<raspberry-pi-ip>:8080`.
3.  Use the buttons connected to the Raspberry Pi to navigate through the displayed information.

Endpoints
---------

-   **/building**: Page for selecting a specific building.
-   **/overview**: Page for selecting a specific room for chosen building.
-   **/overview_timetable**: Page for selecting a specific date and displaying the timetable for selected features.

Python Files Description
-----------------

-   **main.py**: Main Flask application script. It handles web requests and integrates with the USOS API and hardware components.
-   **hardware.py**: Handles the initialization and control of the hardware components like the LCD display and buttons.
