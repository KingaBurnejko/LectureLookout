import os
from dotenv import load_dotenv
from usosapi import USOSAPIConnection

# Load .env file
load_dotenv()

api_url = 'https://usosapps.put.poznan.pl/'
customer_key = os.getenv('customer_key')
customer_secret = os.getenv('customer_secret')

usosAPi = USOSAPIConnection(
    api_url, customer_key, customer_secret
)

def get_lecturer(user_id):
    return(usosAPi.get('services/users/user', user_id=user_id))

def get_buildings():
    return usosAPi.get('services/geo/building_index', fields='id|name')

def get_building_rooms(building_id):
    return usosAPi.get('services/geo/building2', building_id=building_id, fields='rooms[id|number]')['rooms']

def get_room_timetable(room_id):
    res = usosAPi.get('services/tt/room', room_id=room_id, fields='name|course_name|lecturer_ids|start_time|end_time')
    return list(map(lambda x: {
        'name': x['name'],
        'course_name': x['course_name'],
        'lecturer': get_lecturer(x['lecturer_ids'][0]) if len(x['lecturer_ids']) > 0 else None,
        'start_time': x['start_time'],
        'end_time': x['end_time']
    }, res))


# import board
# import digitalio
# lcd_rs = digitalio.DigitalInOut(board.D26)
# lcd_en = digitalio.DigitalInOut(board.D19)
# lcd_d7 = digitalio.DigitalInOut(board.D27)
# lcd_d6 = digitalio.DigitalInOut(board.D22)
# lcd_d5 = digitalio.DigitalInOut(board.D24)
# lcd_d4 = digitalio.DigitalInOut(board.D25)

# lcd_columns = 16
# lcd_rows = 2

# import adafruit_character_lcd.character_lcd as characterlcd
# lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# lcd.message = "Hello\nCircuitPython!"


from flask import Flask, render_template, request, json, Response

app = Flask(__name__,
            static_url_path='', 
            static_folder='./static',
            template_folder='./templates')

@app.route('/')
def index():
    buildings_list = get_buildings()
    return render_template('index.html', buildings_list=buildings_list)

building_id = ""

@app.route('/building', methods=['GET', 'POST'])
def building():
    building_id = request.form.get('comp_select')
    # print(building_id)
    rooms_list = get_building_rooms(building_id)
    return render_template('building.html', room_list=rooms_list)

room_id = ""
timetable = []

@app.route('/overview', methods=['GET', 'POST'])
def overview():
    room_id = request.form.get('comp_select')
    # print(room_id)
    global timetable
    timetable = get_room_timetable(room_id)
   
    return render_template('overview.html')
print(timetable)
@app.route('/overview_timetable', methods=['POST'])
def overview_timetable():
    data = request.json
    date = data['date']

    # print(date)
    # print(timetable)

    for item in timetable:
        if item['start_time'][:10] == date:
            print(item)

    return Response(
        response=json.dumps({
            "data": {
                "import_id": room_id
            }
        }),
        status=201,
        mimetype="application/json"
    )

if __name__ == '__main__':
    # print(usosAPi.get_authorization_url())
    # pin = input('PIN: ')
    # usosAPi.authorize_with_pin(pin)
    app.run(debug=True, port=80, host='0.0.0.0')