from sklearn.preprocessing import StandardScaler
import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('dataset/4dm4.db')

interested_round = st.text_input('Round')

all_scores = pd.read_sql(f'SELECT player_name, beatmap_type, beatmap_tag, score_logit as score FROM scores WHERE round = :rnd', conn, params={'rnd': interested_round})
all_scores['beatmap'] = all_scores['beatmap_type'] + all_scores['beatmap_tag'].astype(str)

table = all_scores.pivot(index='player_name', columns='beatmap', values='score')

model = StandardScaler()
table = pd.DataFrame(model.fit_transform(table), index=table.index, columns=table.columns)

table = table.reset_index()
standardized_scores = table.melt(table.columns[0], table.columns[1:])

st.dataframe(standardized_scores.sort_values(by='value', ascending=False).head(10))
