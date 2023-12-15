import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
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
lcd.clear()
lcd.message = "~LectureLookout~\n Hello!"

# GPIO setup for buttons
button_back = digitalio.DigitalInOut(board.D2)  # Change to the correct pin for 'back' button
button_next = digitalio.DigitalInOut(board.D3)  # Change to the correct pin for 'next' button
button_back.direction = digitalio.Direction.INPUT
button_back.pull = digitalio.Pull.UP
button_next.direction = digitalio.Direction.INPUT
button_next.pull = digitalio.Pull.UP

# Global variables to keep track of the current display and subject
current_display = 0
current_subject_index = 0

def display_chosen_building(building_id):

    lcd.clear()
    lcd.message = "Chosen building:\n{}".format(building_id)

def display_chosen_room(building_id):

    lcd.clear()
    lcd.message = "Chosen room:\n{}".format(building_id)

filtered_timetable = []

def set_filtered_timetable(timetable):
    global filtered_timetable
    filtered_timetable = timetable
    current_display = 0  # Reset display to start from the first item
    current_subject_index = 0  # Reset index to start from the first item

def display_timetable():
    global current_display, current_subject_index, filtered_timetable

    lcd.clear()
    if current_display == 0:
        # Display the date
        date = filtered_timetable[current_subject_index]['start_time'][:10]
        lcd.message = date

    elif current_display == 1:
        # Display start and end time
        start_time = filtered_timetable[current_subject_index]['start_time'][11:16]
        end_time = filtered_timetable[current_subject_index]['end_time'][11:16]
        lcd.message = f"{start_time}\n{end_time}"

    elif current_display == 2:
        # Display course name (PL)
        course_name = filtered_timetable[current_subject_index]['course_name']['pl']
        lcd.message = course_name[:16]
        if len(course_name) > 16:
            lcd.message += f"\n{course_name[16:32]}"

    elif current_display == 3:
        # Display lecturer name
        lecturer = filtered_timetable[current_subject_index]['lecturer']
        lcd.message = f"{lecturer['first_name']}\n{lecturer['last_name']}"

def update_display(action):
    global current_display, current_subject_index, filtered_timetable

    if action == "back":
        current_display -= 1
        if current_display < 0:
            current_subject_index -= 1
            if current_subject_index < 0:
                current_subject_index = len(filtered_timetable) - 1
            current_display = 3

    elif action == "next":
        current_display += 1
        if current_display > 3:
            current_subject_index += 1
            if current_subject_index >= len(filtered_timetable):
                current_subject_index = 0
            current_display = 0

    display_timetable()

def on_back_button_pressed(channel):
    update_display("back")

def on_next_button_pressed(channel):
    update_display("next")

def setup_button_interrupts():
    # Here you would set up your GPIO interrupts
    # This is pseudocode and depends on your specific GPIO library
    # Example:
    GPIO.add_event_detect(button_back, GPIO.FALLING, callback=on_back_button_pressed, bouncetime=200)
    GPIO.add_event_detect(button_next, GPIO.FALLING, callback=on_next_button_pressed, bouncetime=200)
    pass
