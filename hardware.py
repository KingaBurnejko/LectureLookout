import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time
import RPi.GPIO as GPIO

# LCD setup
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_columns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# GPIO setup for buttons
button_back_pin = 2  # Update with correct GPIO pin number
button_next_pin = 3  # Update with correct GPIO pin number
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(button_back_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_next_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variables to keep track of the current display and subject
current_display = 0
current_subject_index = 0

def setup_button_interrupts():
    GPIO.add_event_detect(button_back_pin, GPIO.FALLING, callback=on_back_button_pressed, bouncetime=200)
    GPIO.add_event_detect(button_next_pin, GPIO.FALLING, callback=on_next_button_pressed, bouncetime=200)

def initialize_hardware():
    lcd.clear()
    lcd.message = "~LectureLookout~\n Hello!"
    setup_button_interrupts()

def display_chosen_building(building_id):
    lcd.clear()
    lcd.message = "Chosen building:\n{}".format(building_id)

def display_chosen_room(building_id):
    lcd.clear()
    lcd.message = "Chosen room:\n{}".format(building_id)

def display_chosen_date(date):
    lcd.clear()
    lcd.message = "Chosen date:\n{}".format(date)

filtered_timetable = []

def set_filtered_timetable(timetable):

    global filtered_timetable, current_display, current_subject_index
    filtered_timetable = timetable
    current_display = 0  # Reset display to start from the first item
    current_subject_index = 0  # Reset index to start from the first item

def display_timetable():
    global current_display, current_subject_index, filtered_timetable

    subject = filtered_timetable[current_subject_index]

    lcd.clear()
    if current_display == 0:
        lcd.message = "Chosen date:\n{}".format(subject['start_time'][:10])
        print(subject['start_time'][:10])

    elif current_display == 1:
        time.sleep(2)
        lcd.clear()
        lcd.message = "{}\n{}".format(subject['start_time'][11:16], subject['end_time'][11:16])
        print(subject['start_time'][11:16], subject['end_time'][11:16])

    elif current_display == 2:
        time.sleep(2)
        lcd.clear()
        course_name = subject['course_name']['en']
        if len(course_name) <= 16:
            lcd.message = course_name
        elif len(course_name) <= 32:
            lcd.message = "{}\n{}".format(course_name[:16], course_name[16:])
        else:
            lcd.message = course_name
            time.sleep(2)
            for i in range(len(course_name)*2):
                lcd.move_left()
                time.sleep(0.8)
        print(course_name)

    elif current_display == 3:
        time.sleep(2)
        lcd.clear()
        lecturer = subject['lecturer']
        lcd.message = "{}\n{}".format(lecturer['first_name'], lecturer['last_name'])
        print(lecturer['first_name'], lecturer['last_name'])

def update_display(action):
    global current_display, current_subject_index, filtered_timetable

    if action == "back":
        if current_display == 0 and current_subject_index == 0:
            current_subject_index = len(filtered_timetable) - 1
            current_display = 3
        else:
            current_display -= 1
            if current_display < 0:
                current_subject_index -= 1
                current_display = 3

    elif action == "next":
        if current_display == 3 and current_subject_index == len(filtered_timetable) - 1:
            current_subject_index = 0
            current_display = 0
        else:
            current_display += 1
            if current_display > 3:
                current_subject_index += 1
                current_display = 0

    if len(filtered_timetable) > 0:  # Check if the list is not empty
        display_timetable()
        time.sleep(5)
    else:
        # lcd.message = "No data available"
        print("No data available")

def on_back_button_pressed(channel):
    update_display("back")

def on_next_button_pressed(channel):
    update_display("next")

def cleanup_gpio():
    GPIO.cleanup()

# def cycle_displays():
#     while True:
#         update_display("next")
#         time.sleep(5)