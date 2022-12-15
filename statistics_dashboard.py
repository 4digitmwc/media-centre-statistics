import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

conn = sqlite3.connect('dataset/4dm4.db')

interested_round = st.text_input('Round')

def score_distribution():
    beatmap_typetag = st.text_input('Beatmap code (ex. HB2)')
    if beatmap_typetag:
        beatmap_type, beatmap_tag = beatmap_typetag[:2], beatmap_typetag[2:]
        data = pd.read_sql(f'SELECT score FROM scores WHERE round="{interested_round}" AND beatmap_type="{beatmap_type}" AND beatmap_tag={beatmap_tag}', conn)
        fig, ax = plt.subplots()
        ax.hist(data)
        st.pyplot(fig)

score_distribution()
