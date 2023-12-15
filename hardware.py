import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import RPi.GPIO as GPIO
import time

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
filtered_timetable = []

def display_chosen_building(building_id):
    lcd.clear()
    lcd.message = "Chosen building:\n{}".format(building_id)

def display_chosen_room(building_id):
    lcd.clear()
    lcd.message = "Chosen room:\n{}".format(building_id)

def set_filtered_timetable(timetable):
    global filtered_timetable, current_subject_index, current_display
    filtered_timetable = timetable
    current_subject_index = 0
    current_display = 0

def display_timetable():
    global current_display, current_subject_index, filtered_timetable

    if not filtered_timetable or current_subject_index >= len(filtered_timetable):
        lcd.message = "No data available"
        return

    lcd.clear()
    if current_subject_index == 0 and current_display == 0:
        # Display the date
        date = filtered_timetable[current_subject_index]['start_time'][:10]
        lcd.message = "Date: {}\n".format(date)
    elif current_display == 1:
        # Display start and end time
        start_time = filtered_timetable[current_subject_index]['start_time'][11:16]
        end_time = filtered_timetable[current_subject_index]['end_time'][11:16]
        lcd.message = "{} - {}\n".format(start_time, end_time)
    elif current_display == 2:
        # Display course name (PL)
        course_name = filtered_timetable[current_subject_index]['course_name']['pl']
        lcd.message = course_name[:16]
        if len(course_name) > 16:
            lcd.message += "\n{}".format(course_name[16:32])
    elif current_display == 3:
        # Display lecturer name
        lecturer = filtered_timetable[current_subject_index]['lecturer']
        lcd.message = "{}\n{}".format(lecturer['first_name'], lecturer['last_name'])

def update_display(action):
    global current_display, current_subject_index, filtered_timetable

    if action == "back":
        if current_subject_index == 0 and current_display == 0:
            # At the start, do nothing
            pass
        elif current_display == 0:
            current_subject_index -= 1
            current_display = 3
        else:
            current_display -= 1

    elif action == "next":
        if current_display == 3:
            if current_subject_index < len(filtered_timetable) - 1:
                current_subject_index += 1
                current_display = 0
        else:
            current_display += 1

    display_timetable()

def on_back_button_pressed(channel):
    update_display("back")

def on_next_button_pressed(channel):
    update_display("next")

def setup_button_interrupts():
    GPIO.add_event_detect(button_back_pin, GPIO.FALLING, callback=on_back_button_pressed, bouncetime=200)
    GPIO.add_event_detect(button_next_pin, GPIO.FALLING, callback=on_next_button_pressed, bouncetime=200)

def initialize_hardware():
    lcd.clear()
    lcd.message = "~LectureLookout~\nHello!"
    setup_button_interrupts()

def cleanup_gpio():
    GPIO.cleanup()

# Call this function from your main.py when starting the app
initialize_hardware()
