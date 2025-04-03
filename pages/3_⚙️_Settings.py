import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Settings")

st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; padding: 1rem; background-color: #8B4513; color: white; border-radius: 8px;'>
        <div style='display: flex; align-items: center;'>
            <h2 style='margin: 0; color: white;'>Settings</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Dashboard Settings")

# Example settings
with st.form("settings_form"):
    st.write("### Display Settings")
    theme = st.selectbox("Dashboard Theme", ["Light", "Dark", "System"])
    update_interval = st.slider("Data Update Interval (minutes)", 5, 60, 15)
    
    st.write("### Notification Settings")
    email_notifications = st.checkbox("Enable Email Notifications")
    notification_frequency = st.selectbox("Notification Frequency", ["Daily", "Weekly", "Monthly"])
    
    st.write("### Data Settings")
    data_source = st.selectbox("Primary Data Source", ["CSV", "Database", "API"])
    cache_data = st.checkbox("Enable Data Caching", value=True)
    
    submitted = st.form_submit_button("Save Settings")
    if submitted:
        st.success("Settings saved successfully!") 