import streamlit as st
import pandas as pd

def meeting_page():
    meetings = [{
        'customerId': '12345',
        'advisorId': '98765',
        'time': '11-19-2025 11:00AM',
        'zoomUrl': 'www.fakeurl.com'
    },
    {
        'customerId': '54321',
        'advisorId': '56789',
        'time': '1-31-2025 3:45PM',
        'zoomUrl': 'www.anotherfakeurl.com'
    }]

    st.header('Advisor Page')
    st.write('Welcome to the advisor page where you can manage meetings with your personal advisor!')
    outer_container = st.container(border=True)
    meeting_container = outer_container.container(border=False, height=200)
    meeting_container.write('Scheduled meetings')

    for i, meeting in enumerate(meetings):
        if i == 0:
            tableData={'Customer ID': [meeting['customerId']], 'Advisor ID': [meeting['advisorId']], 'Time': [meeting['time']], 'Zoom URL': [meeting['zoomUrl']]}
            pandaTable = pd.DataFrame(data=tableData, index=['Meeting 1'])
            table = meeting_container.table(pandaTable)
        else:
            tableData={'Customer ID': [meeting['customerId']], 'Advisor ID': [meeting['advisorId']], 'Time': [meeting['time']], 'Zoom URL': [meeting['zoomUrl']]}
            pandaTable = pd.DataFrame(data=tableData, index=[f'Meeting {i+1}'])
            table.add_rows(pandaTable)
            
    outer_container.button('Schedule meeting')