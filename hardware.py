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
lcd.message = "~LectureLookout~\nHello!"

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

def display_timetable(timetable):
    global current_display, current_subject_index

    lcd.clear()
    if current_display == 0:
        # Display the date
        date = timetable[current_subject_index]['start_time'][:10]
        lcd.message = date

    elif current_display == 1:
        # Display start and end time
        start_time = timetable[current_subject_index]['start_time'][11:16]
        end_time = timetable[current_subject_index]['end_time'][11:16]
        lcd.message = f"{start_time}\n{end_time}"

    elif current_display == 2:
        # Display course name (PL)
        course_name = timetable[current_subject_index]['course_name']['pl']
        lcd.message = course_name[:16]
        if len(course_name) > 16:
            lcd.message += f"\n{course_name[16:32]}"

    elif current_display == 3:
        # Display lecturer name
        lecturer = timetable[current_subject_index]['lecturer']
        lcd.message = f"{lecturer['first_name']}\n{lecturer['last_name']}"

# Main loop
try:
    while True:
        if not button_back.value:  # Button for going back pressed
            current_display -= 1
            if current_display < 0:
                current_subject_index -= 1
                if current_subject_index < 0:
                    current_subject_index = len(timetable) - 1
                current_display = 3
            display_timetable(timetable)
            time.sleep(0.3)  # Debounce delay

        if not button_next.value:  # Button for going next pressed
            current_display += 1
            if current_display > 3:
                current_subject_index += 1
                if current_subject_index >= len(timetable):
                    current_subject_index = 0
                current_display = 0
            display_timetable(timetable)
            time.sleep(0.3)  # Debounce delay

        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up GPIO on CTRL+C exit
    lcd.clear()