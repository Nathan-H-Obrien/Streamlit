import streamlit as st
import pandas as pd
from pymongo import MongoClient
import datetime

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"  # Change if using MongoDB Atlas
DATABASE_NAME = "WealthWise"  # Change this to your database name

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
meetings_collection = db["appointments"]  # Collection for storing meeting details
advisors_collection = db["advisors"]  # Collection for storing advisors

def round_time_to_nearest_15(dt):
    new_minute = (dt.minute // 15) * 15
    return dt.replace(minute=new_minute, second=0, microsecond=0)

def format_time_12hr(dt):
    return dt.strftime("%I:%M %p")  # AM/PM format

def parse_12hr_time(time_str):
    return datetime.datetime.strptime(time_str, "%Y-%m-%d %I:%M %p")  # Parse the 12-hour format time string

@st.dialog("Schedule Meeting")
def schedule_meeting(advisor_options, user_id):
    with st.form(key="schedule_meeting_form"):
        advisor_id = st.selectbox("Select Advisor", options=list(advisor_options.keys()), format_func=lambda x: advisor_options[x])
        date = st.date_input("Date")
        current_time = datetime.datetime.now().replace(second=0, microsecond=0)
        rounded_time = round_time_to_nearest_15(current_time)
        time = st.time_input("Time", value=rounded_time)
        
        # Format the time input to AM/PM format
        formatted_time = format_time_12hr(datetime.datetime.combine(datetime.date.today(), time))
        
        zoom_url = st.text_input("Zoom URL")
        submit = st.form_submit_button("Schedule Meeting")
        
        if submit and advisor_id and zoom_url:
            meeting_data = {
                "customerId": user_id,
                "advisorId": advisor_id,
                "time": f"{date} {formatted_time}",
                "zoomUrl": zoom_url
            }
            meetings_collection.insert_one(meeting_data)
            st.success("Meeting scheduled successfully!")
            st.rerun()

def meeting_page():
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("You must be logged in to view meetings.")
        return
    
    meetings = list(meetings_collection.find({"customerId": user_id}))
    advisors = list(advisors_collection.find())
    advisor_options = {str(a['_id']): f"{a['first_name']} {a['last_name']}" for a in advisors}

    st.header('Meetings Page')
    st.write('Welcome to the meetings page where you can manage meetings with your personal advisor!')
    
    outer_container = st.container(border=True)
    meeting_container = outer_container.container(border=False, height=200)
    meeting_container.write('Scheduled meetings')

    if meetings:
        # Extract date and time separately, format the date to Month Day, Year (e.g., April 17, 2025)
        tableData = {
            'Advisor Name': [advisor_options.get(m['advisorId'], m['advisorId']) for m in meetings],
            'Date': [datetime.datetime.strptime(m['time'], "%Y-%m-%d %I:%M %p").strftime("%B %d, %Y") for m in meetings],  # Extract Date in Month Day, Year format
            'Time': [format_time_12hr(parse_12hr_time(m['time'])) for m in meetings],  # Convert 12-hour time
            'Zoom URL': [m['zoomUrl'] for m in meetings]
        }
        pandaTable = pd.DataFrame(data=tableData, index=[f'Meeting {i+1}' for i in range(len(meetings))])
        meeting_container.table(pandaTable)
    else:
        meeting_container.write("No scheduled meetings.")
        
    if outer_container.button('Schedule meeting'):
        schedule_meeting(advisor_options, user_id)
