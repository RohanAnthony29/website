import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Analytics")

st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; padding: 1rem; background-color: #8B4513; color: white; border-radius: 8px;'>
        <div style='display: flex; align-items: center;'>
            <h2 style='margin: 0; color: white;'>Analytics Dashboard</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Detailed Analytics")
st.write("This page will contain detailed analytics about job postings.") 