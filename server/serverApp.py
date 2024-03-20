import sys
import os.path
import streamlit as st


logfile = str(os.getcwd()) + "\std.log"
f = open(logfile, "r")
lines = f.readlines()
for line in lines:
    st.write(line)