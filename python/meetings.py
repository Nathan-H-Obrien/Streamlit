import streamlit as st
import pandas as pd
from pymongo import MongoClient
import datetime

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"
DATABASE_NAME = "WealthWise"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
meetings_collection = db["appointments"]
advisors_collection = db["advisors"]
users_collection = db["users"]

def round_time_to_nearest_15(dt):
    new_minute = (dt.minute // 15) * 15
    return dt.replace(minute=new_minute, second=0, microsecond=0)

def format_time_12hr(dt):
    return dt.strftime("%I:%M %p")

def parse_12hr_time(time_str):
    return datetime.datetime.strptime(time_str, "%Y-%m-%d %I:%M %p")

def get_weekday_dates(num_days=30):
    today = datetime.date.today()
    weekday_dates = []
    i = 0
    while len(weekday_dates) < num_days:
        day = today + datetime.timedelta(days=i)
        if day.weekday() < 5:  # 0 = Monday, 6 = Sunday
            weekday_dates.append(day)
        i += 1
    return weekday_dates


@st.dialog("Schedule Meeting")
def schedule_meeting(advisor_options, user_id):
    # Select advisor and date outside the form so they update time slots in real-time
    advisor_id = st.selectbox("Select Advisor", options=list(advisor_options.keys()), format_func=lambda x: advisor_options[x])
    weekday_options = get_weekday_dates()
    date = st.selectbox("Select Date", options=weekday_options, format_func=lambda d: d.strftime("%A, %B %d, %Y"))


    time_str = None

    if advisor_id and date:
        # Fetch existing appointments for this advisor on this date
        existing_appointments = meetings_collection.find({
            "advisorId": advisor_id,
            "date": str(date)
        })
        booked_times = {m["time"] for m in existing_appointments}

        # Generate time slots: 10:00 AM – 2:00 PM in 30-minute steps
        start_hour = 10
        end_hour = 14
        interval_minutes = 30
        time_slots = []
        for hour in range(start_hour, end_hour + 1):
            for minute in (0, interval_minutes):
                if hour == end_hour and minute > 0:
                    continue
                time_label = datetime.time(hour, minute).strftime("%I:%M %p")
                if time_label not in booked_times:
                    time_slots.append(time_label)

        if time_slots:
            time_str = st.radio("Select a time", options=time_slots, horizontal=True)
        else:
            st.info("No available times for this advisor on the selected date.")

    # Now the form only wraps the submit button
    with st.form(key="schedule_meeting_form", border=False):
        submit = st.form_submit_button("Schedule Meeting")

        if submit and advisor_id and time_str:
            meeting_data = {
                "customerId": user_id,
                "advisorId": advisor_id,
                "date": str(date),
                "time": time_str
            }
            meetings_collection.insert_one(meeting_data)
            st.success("Meeting scheduled successfully!")
            st.rerun()

def meetings_page():
    st.session_state.password_verified = False
    user_id = st.session_state.get("user_id")
    subscription_type = st.session_state.get("subscription_type", "Basic")

    if not user_id:
        st.error("You must be logged in to view meetings.")
        return

    st.header('Meetings Page', anchor=False)
    st.write('Welcome to the meetings page where you can manage meetings with your personal advisor!')

    if subscription_type == "Basic":
        st.warning("Only Elite users have access to meetings with personal advisors.")
        if st.button("Upgrade to Elite Subscription here!", use_container_width=True):
            st.session_state.page_selection = "👤 User Management"
            st.rerun()
        return


    now = datetime.datetime.now()

    # Get all meetings for this user
    all_meetings = meetings_collection.find({"customerId": user_id})

    # Filter to only future meetings
    meetings = []
    for m in all_meetings:
        meeting_dt = datetime.datetime.strptime(f"{m['date']} {m['time']}", "%Y-%m-%d %I:%M %p")
        if meeting_dt > now:
            meetings.append(m)

    # Sort from soonest to farthest
    meetings.sort(key=lambda m: datetime.datetime.strptime(f"{m['date']} {m['time']}", "%Y-%m-%d %I:%M %p"))

    # Sort meetings by soonest
    def get_meeting_datetime(meeting):
        return datetime.datetime.strptime(f"{meeting['date']} {meeting['time']}", "%Y-%m-%d %I:%M %p")

    meetings.sort(key=get_meeting_datetime)

    advisors = list(users_collection.find({"subscription": "Advisor"}))
    advisor_options = {str(a['_id']): f"{a['first_name']} {a['last_name']}" for a in advisors}

    outer_container = st.container(border=True)
    meeting_container = outer_container.container(border=False)
    meeting_container.write('Scheduled meetings')

    if meetings:
        tableData = {
            'Advisor Name': [advisor_options.get(m['advisorId'], m['advisorId']) for m in meetings],
            'Date': [datetime.datetime.strptime(m['date'], "%Y-%m-%d").strftime("%B %d, %Y") for m in meetings],
            'Time': [m['time'] for m in meetings]
        }

        pandaTable = pd.DataFrame(data=tableData, index=[f'Meeting {i+1}' for i in range(len(meetings))])
        meeting_container.table(pandaTable)
    else:
        meeting_container.write("No scheduled meetings.")

    if outer_container.button('Schedule meeting'):
        schedule_meeting(advisor_options, user_id)
