import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.sidebar.title("Upload dataset")
upload_file = st.sidebar.file_uploader("choose Csv file",type='csv')
if upload_file is not None:
    df = pd.read_csv(upload_file)

    # sidebar code
    no_event = len(df)
    citizenship_counts = df['citizenship'].value_counts()
    event_location_region = df['event_location_region'].value_counts()
    hostilities_counts = df[df['took_part_in_the_hostilities'] == 'Yes']['citizenship'].value_counts()
    no_hostilities_counts = df[df['took_part_in_the_hostilities'] == 'No']['citizenship'].value_counts()

    st.sidebar.write("No of Event :", no_event)

    col1,col2 = st.sidebar.columns(2)
    col3,col4 = st.sidebar.columns(2)
    with col1:
        st.subheader("citizenship_counts")
        st.write(citizenship_counts)
    with col2:
        st.subheader("event_location_region")
        st.write(event_location_region)
    with col3:
        st.subheader("hostilities_counts")
        st.write(hostilities_counts)
    with col4:
        st.subheader("no_hostilities_counts")
        st.write(no_hostilities_counts)

    weapons_counts = df['ammunition'].value_counts()
    st.sidebar.write("Weapon counts",weapons_counts)


    # Data analysis part
    st.title("Isreal Palestine Conflict Analysis")
    st.write('Dataset Sample',df)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader("type of injuries")
        type_of_injury= df['type_of_injury'].value_counts()
        st.bar_chart(type_of_injury)
    with col2:
        st.subheader("MaleFemaleCount")
        MFcounts = df['gender'].value_counts()
        st.bar_chart(MFcounts,color='#FF0000')

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Age Summary")
        age = df['age'].describe()
        st.write(age)
    with col2:
        st.subheader("Even Location Region Count")
        eventregion = df['event_location_region'].value_counts()
        st.bar_chart(eventregion)

    col1,col2 = st.columns(2)
    with col1:
        residencecountbyreg = df.groupby('event_location_region')['place_of_residence'].nunique()
        st.subheader("Residence Percentage by Region")
        fig, ax = plt.subplots()
        ax.pie(residencecountbyreg,labels=residencecountbyreg.index, autopct='%1.1f%%')
        st.pyplot(fig)
    with col2:
        injurytype = df['type_of_injury'].value_counts()
        st.subheader("Injury Types")
        fig,ax = plt.subplots()
        ax.pie(injurytype,labels=injurytype.index,autopct='%1.1f%%')
        st.pyplot(fig)

    regionavgage = df.groupby('event_location_region')['age'].mean()
    st.subheader("Avg Age by region")
    st.bar_chart(regionavgage)

    col1, col2 = st.columns(2)
    with col1:
        IncidentcountbyNat = df.groupby('citizenship').size().reset_index(name='incident_count')
        st.subheader('Incident Count by Nationality')
        st.write(IncidentcountbyNat)
    with col2:
        genderInc = df.groupby('gender').size().reset_index(name="incident_count")
        st.subheader('Incident Count by Gender')
        st.write(genderInc)

    # Time-based analysis (events at specific times)
    df['date_of_event'] = pd.to_datetime(df['date_of_event'])
    df['year'] = df['date_of_event'].dt.year
    df['month'] = df['date_of_event'].dt.month_name()  # Format month as month name
    time_events = df.groupby(['year', 'month']).size().reset_index(name='incident_count')
    time_events['year_month'] = time_events['month'] + ' ' + time_events['year'].astype(str)
    st.subheader('Time-Based Events')
    st.line_chart(time_events.set_index('year_month')['incident_count'])






