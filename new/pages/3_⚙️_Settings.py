import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Settings | Job Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# Page Header
st.title("⚙️ Settings")
st.markdown("Configure your dashboard preferences")

# Add your settings content here
st.markdown("""
### Available Settings
- Data Source Configuration
- Display Preferences
- Notification Settings
- User Profile
""")

# Placeholder for settings content
st.info("Settings content will be added here. This is a placeholder page.") 