import streamlit as st
import pyperclip
import asyncio
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Initialize session state for timer
if 'role_times' not in st.session_state:
    st.session_state.role_times = {
        "top": timedelta(minutes=0),
        "jg": timedelta(minutes=0),
        "mid": timedelta(minutes=0),
        "bot": timedelta(minutes=0),
        "sup": timedelta(minutes=0)
    }
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

# Function to start the timer
def start_timer():
    st.session_state.start_time = datetime.now()
    st.session_state.timer_running = True

# Function to stop the timer and reset all role times to 0
def stop_timer():
    st.session_state.timer_running = False
    # Reset each role time to 0
    for role in st.session_state.role_times:
        st.session_state.role_times[role] = timedelta(minutes=0)


# Function to add 5 minutes to a role's time based on the current elapsed time and copy to clipboard
def add_time(role):
    # Calculate current elapsed time
    current_elapsed_time = datetime.now() - st.session_state.start_time
    # Set the role's time to the current elapsed time + 5 minutes
    st.session_state.role_times[role] = current_elapsed_time + timedelta(minutes=5)

    # Generate the role times display string
    role_display = " | ".join([
        f"{role} {int(t.total_seconds()//60)}:{int(t.total_seconds()%60):02d}"
        for role, t in st.session_state.role_times.items()
    ])

    # Copy the role_display string to clipboard
    #pyperclip.copy(role_display)

# Layout of the app
st.title("LOL Timer App")

col1, col2 = st.columns(2)
with col1:
    if st.button("Start"):
        start_timer()
with col2:
    if st.button("Reset"):
        stop_timer()

# Display buttons in a horizontal row using Streamlit columns
st.write("### Flash")

button_columns = st.columns(len(st.session_state.role_times))
for idx, (role, _) in enumerate(st.session_state.role_times.items()):
    with button_columns[idx]:
        if st.button(role.capitalize()):
            add_time(role)

# Create placeholders for the main timer and role times
timer_placeholder = st.empty()
role_display_placeholder = st.empty()

# Async function to update the display
async def update_display():
    while st.session_state.timer_running:
        # Timer display
        elapsed_time = datetime.now() - st.session_state.start_time
        formatted_elapsed_time = str(elapsed_time).split(".")[0]  # Remove microseconds
        
        # Update the main timer in place
        timer_placeholder.write(f"**Timer:** {formatted_elapsed_time}")
        
        # Update each role time in place
        role_display = " | ".join([
            f"{role} {int(t.total_seconds()//60)}:{int(t.total_seconds()%60):02d}"
            for role, t in st.session_state.role_times.items()
        ])
        role_display_placeholder.code(role_display)
        
        # Await a delay to prevent continuous execution
        await asyncio.sleep(1)

# Run the async update display if the timer is running
if st.session_state.timer_running:
    asyncio.run(update_display())
