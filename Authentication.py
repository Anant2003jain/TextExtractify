import streamlit as st
import json

#Function to save updated user data"""
def save_user_data(user_data):
    with open('users.json', 'w') as file:
        json.dump(user_data, file, indent=4)

#Login function"""
def login(user_data):
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in user_data and user_data[username]['password'] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.session_state.userid = user_data[username]['userid']
            st.session_state.user_plan = user_data[username]['access_level']
            st.success(f"Welcome back, {user_data[username]['userid']}!")
        else:
            st.error("Invalid credentials. Please try again.")


#Registration function""
def register(user_data):
    st.subheader("Signup")

    userid = st.text_input("User ID")
    gmail = st.text_input("Enter you Gmail")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Signup"):
        
        try: 
            if gmail[gmail.index('@gmail.com'): ] != '@gmail.com':
                st.warning("Entered gmail is is: ",gmail)
                st.error("Enter correct Gmail ID")
                st.write("Only gmail is accepted")
            elif gmail in user_data:
                st.error("Username already exists. Please choose another.")
            elif password != confirm_password or len(password)<1:
                st.error("Passwords do not match. Please try again.")
            else:
                user_data[gmail] = {"userid":userid,"password": password, "access_level": "free"}
                save_user_data(user_data)
                st.success("Account created successfully! You can now log in.")
        except Exception as e:
            st.error("Enter correct Gmail ID")
            st.write("Only gmail is accepted")
            #st.warning(e)
        
    st.session_state.logged_in = False  # Optional, ensures the user is logged out before login


#Logout function (mock
def logout():
    st.session_state.logged_in = False
    st.session_state.userid = "Guest"
    st.session_state.current_user = None
    st.session_state.user_plan = None
    st.success("Logged out successfully.")
    