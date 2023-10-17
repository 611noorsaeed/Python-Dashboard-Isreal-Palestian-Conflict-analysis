import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
data = pd.read_csv("fatalities.csv")

# Create a Streamlit app
st.title("Incident Data Analysis Dashboard")

# Sidebar for data upload
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# If a file is uploaded, use it as the dataset
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)


    # displaying important information within sidebar
    # Number of events
    num_events = len(data)
    st.sidebar.write('NO of Events',num_events)
    # Types of weapons used
    weapons_used = data['ammunition'].value_counts()
    # Display the ammunition list
    st.subheader("Ammunition List")
    st.sidebar.write(weapons_used)



    col1, col2 = st.sidebar.columns(2)
    col3, col4 = st.sidebar.columns(2)

    citizenship_counts = data['citizenship'].value_counts()
    event_location_region_counts = data['event_location_region'].value_counts()
    hostilities_counts = data[data['took_part_in_the_hostilities'] == 'Yes']['citizenship'].value_counts()
    no_hostilities_counts = data[data['took_part_in_the_hostilities'] == 'No']['citizenship'].value_counts()

    with col1:
        st.subheader("Citizenship")
        st.write(citizenship_counts)

    with col2:
        st.subheader("Event Location Region")
        st.write(event_location_region_counts)

    with col3:
        st.subheader("hostilities")
        st.write(hostilities_counts)
    with col4:
        st.subheader('no hostilities')
        st.write(no_hostilities_counts)

#=======================================================================================
    # Show a sample of the data
    st.header("Sample Data")
    st.write(data.head())

    # Data analysis section
    st.header("Data Analysis")


    col1,col2 = st.columns(2)

    with col1:
        # Group data by 'citizenship' and count incidents
        citizenship_counts = data['citizenship'].value_counts()
        st.subheader("Incidents by Citizenship")
        st.bar_chart(citizenship_counts,color='#3498db')
    with col2:
        # Group data by 'gender' and visualize
        gender_counts = data['gender'].value_counts()
        st.subheader("Incidents by Gender")
        st.bar_chart(gender_counts,color='#FF0000')


    col1,col2 = st.columns(2)

    with col1:
        # Calculate summary statistics for 'age'
        st.subheader("Summary Statistics for Age")
        st.write(data['age'].describe())
    with col2:
        # Group data by 'event_location_region' and count incidents
        region_counts = data['event_location_region'].value_counts()
        st.subheader("Incidents by Region")
        st.bar_chart(region_counts)


    col1,col2 = st.columns(2)
    with col1:
        # Count unique values of 'place_of_residence' within each region
        st.subheader("Unique Places of Residence by Region")
        unique_places_by_region = data.groupby('event_location_region')['place_of_residence'].nunique()
        st.write(unique_places_by_region)
    with col2:
        # Calculate average age by 'event_location_region'
        avg_age_by_region = data.groupby('event_location_region')['age'].mean()
        st.subheader("Average Age by Region")
        st.write(avg_age_by_region)

    # Visualize the types of injuries using Matplotlib
    st.subheader("Types of Injuries")
    injury_counts = data['type_of_injury'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(injury_counts, labels=injury_counts.index, autopct='%1.1f%%')
    st.pyplot(fig)

    # Data filtering example: Incidents in a specific region with specific characteristics
    region = 'West Bank'  # Replace with the desired region
    filtered_data = data[(data['event_location_region'] == region) & (data['type_of_injury'] == 'gunfire')]
    st.subheader(f"Incidents in {region} with Gunfire as Injury Type")
    st.write(filtered_data)

    # Combining grouping and filtering(example: average  age  of males and females from a specific nationality  involved in specific injuries)
    avg_age = data[(data['citizenship'] == 'Palestinian') & (data['type_of_injury'] == 'stones throwing')].groupby('gender')[
        'age'].mean()
    st.subheader("stones throwing avg age")
    st.write(avg_age)

    # Time-based analysis (events at specific times)
    data['date_of_event'] = pd.to_datetime(data['date_of_event'])
    data['year'] = data['date_of_event'].dt.year
    data['month'] = data['date_of_event'].dt.month_name()  # Format month as month name
    time_events = data.groupby(['year', 'month']).size().reset_index(name='incident_count')
    time_events['year_month'] = time_events['month'] + ' ' + time_events['year'].astype(str)
    st.subheader('Time-Based Events')
    st.line_chart(time_events.set_index('year_month')['incident_count'])

    # Calculate average age for female (F) citizens
    female_age = pd.pivot_table(data[data['gender'] == 'F'], values='age', index=['citizenship'], aggfunc='mean')
    st.subheader('Average Age for Female Citizens')
    st.bar_chart(female_age)

    # Calculate average age for male (M) citizens
    male_age = pd.pivot_table(data[data['gender'] == 'M'], values='age', index=['citizenship'], aggfunc='mean')
    st.subheader('Average Age for Male Citizens')
    st.bar_chart(male_age)

    # filtering with multiple conditions
    result = data[(data['citizenship'] == 'Palestinian') & (data['gender'] == 'F') & (data['type_of_injury'] == 'gunfire')][
        ['citizenship', 'gender', 'type_of_injury']]
    st.subheader("Gender and Nationality Injury type")
    st.write(result)

# Footer
st.sidebar.text("Data analysis dashboard by Noor Saeed")

