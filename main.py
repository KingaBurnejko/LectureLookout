import os
from dotenv import load_dotenv
from usosapi import USOSAPIConnection
from hardware import *
import threading
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
    display_chosen_building(building_id)
    global rooms_list
    rooms_list = get_building_rooms(building_id)
    return render_template('building.html', room_list=rooms_list)

room_id = ""
timetable = []

@app.route('/overview', methods=['GET', 'POST'])
def overview():
    room_id = request.form.get('comp_select')

    selected_room = next((room for room in rooms_list if room['id'] == room_id), None)

    display_chosen_room(selected_room['number'])
    # print(room_id)
    global timetable
    timetable = get_room_timetable(room_id)
   
    return render_template('overview.html')

# print(timetable)

@app.route('/overview_timetable', methods=['POST'])
def overview_timetable():
    data = request.json
    date = data['date']

    display_chosen_date(date)

    # Filter the timetable for the specified date
    filtered_timetable = [item for item in timetable if item['start_time'][:10] == date]

    # Now, call the display_timetable function with the filtered timetable
    # Make sure that this function is defined and accessible here
    if filtered_timetable:
        set_filtered_timetable(filtered_timetable)
        display_thread = threading.Thread(target=update_display("next"))
        display_thread.start()

    return Response(
        response=json.dumps({
            "data": {
                "import_id": room_id,
                "date": date
            }
        }),
        status=201,
        mimetype="application/json"
    )

if __name__ == '__main__':
    initialize_hardware()
    try:
        app.run(debug=True, port=8080, host='0.0.0.0')
    finally:
        cleanup_gpio()  # This ensures GPIO cleanup on exit
    # print(usosAPi.get_authorization_url())
    # pin = input('PIN: ')
    # usosAPi.authorize_with_pin(pin)
    # app.run(debug=True, port=8080, host='0.0.0.0')