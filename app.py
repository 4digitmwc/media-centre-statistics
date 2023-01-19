import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='4DM2023 Media Centre Statistics',
    page_icon='https://cdn.discordapp.com/attachments/546525809440194560/1010576476158038147/4dm23.jpg'
)

import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

from gsheetsdb import connect

conn = connect()

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

def fetch_data():
    qualifiers_data_sheet = st.secrets["quals_data"]
    country_q_data_sheet = st.secrets['country_data']
    beatmap_metadata_sheet = st.secrets['beatmap_metadata']
    player_username_sheet = st.secrets['player_usernames']

    quals_data = pd.DataFrame(run_query(f'SELECT * FROM "{qualifiers_data_sheet}"'))
    country_data = pd.DataFrame(run_query(f'SELECT * FROM "{country_q_data_sheet}"'))
    beatmap_metadata = pd.DataFrame(run_query(f'SELECT * FROM "{beatmap_metadata_sheet}"'))
    player_username = pd.DataFrame(run_query(f'SELECT * FROM "{player_username_sheet}"'))

    player_quals_data = pd.merge(pd.merge(quals_data, player_username, how='left'), beatmap_metadata, how='left')[['username', 'beatmap_metadata', 'score']]
    country_quals_data = pd.merge(country_data, beatmap_metadata, how='left')[['country', 'beatmap_metadata', 'score']]
    
    return player_quals_data, country_quals_data, beatmap_metadata, player_username

class QualifiersStatisticsDashboard:
    _score_type = ['Players', 'Countries']
    _logit_divisor = {
        'Players': 1e6,
        'Countries': 3e6
    }
    _plot_type = ['Histogram', 'Boxplot']
    def __init__(self, player_quals_data: pd.DataFrame, country_quals_data: pd.DataFrame):
        self._player_quals_data = player_quals_data
        self._country_quals_data = country_quals_data
    
    @property
    def beatmaps(self):
        return self._country_quals_data['beatmap_metadata'].unique()
    
    @property
    def countries(self):
        return self._country_quals_data['country'].unique()
    
    @property
    def players(self):
        return self._player_quals_data['username'].unique()
    
    def player_corr(self):
        return self.get_best_player_scores().pivot('username', 'beatmap_metadata', 'score').corr()
    
    def country_corr(self):
        return self.get_best_country_scores().pivot('country', 'beatmap_metadata', 'score').corr()
    
    def get_best_player_scores(self):
        return self._player_quals_data.groupby(['username', 'beatmap_metadata']).max().reset_index()
    
    def get_best_country_scores(self):
        return self._country_quals_data.groupby(['country', 'beatmap_metadata']).max().reset_index()
    
    def get_score_df(self, score_type: str):
        _score_df = {
            'Players': self.get_best_player_scores(),
            'Countries': self.get_best_country_scores()
        }
        return _score_df[score_type]
    
    def plot(self, df, plot_type):
        fig, ax = plt.subplots()
        if plot_type == 'Histogram':
            ax.hist(df['score'])
        else:
            ax.boxplot(df['score'])
        return fig
    
    def tinder(self):
        st.subheader("4DM2023 Tinder")
        st.markdown("According to Qualifiers Maps, Let's find out who has the most similar skills to you!")
        st.markdown("We calculate the similarity of the skill based on the **Pearson Correlation**, therefore some of the players who have different level of skills may get the high similarity in some cases.")
        score_table = self.get_best_player_scores().pivot('beatmap_metadata', 'username', 'score')
        imputed_score_table = pd.DataFrame(SimpleImputer(strategy='median').fit_transform(score_table), index=score_table.index, columns=score_table.columns)
        correlations = imputed_score_table.corr()
        username = st.selectbox('Username', self.players)
        most_similar_players = correlations[username][correlations.index != username].sort_values(ascending=False).head(5)
        st.dataframe(most_similar_players)

    def score_distribution(self):
        score_type = st.selectbox('Score Type', self._score_type)
        plot_type = st.selectbox('Plot Type', self._plot_type)
        beatmap = st.selectbox('Beatmap', self.beatmaps)
        player_corr = self.player_corr()
        most_similar_player = player_corr[beatmap].sort_values(ascending=False)
        most_similar_player = most_similar_player[most_similar_player.index != beatmap].head(1).index[0]
        df = self.get_score_df(score_type)
        df = df[df['beatmap_metadata'] == beatmap]
        fig = self.plot(df, plot_type)
        st.pyplot(fig)
        _25 = df['score'].quantile(0.25)
        _50 = df['score'].quantile(0.5)
        _75 = df['score'].quantile(0.75)
        min_score = df['score'].min()
        max_score = df['score'].max()
        mean_score = df['score'].mean()
        std_score = df['score'].std(ddof=1)
        st.subheader(f"Summary for {beatmap}")
        st.markdown(f"Minimum Score: {min_score}")
        st.markdown(f"Maximum Score: {max_score}")
        st.markdown(f"Average Score: {mean_score}")
        st.markdown(f"Standard Deviation: {std_score}")
        st.markdown(f"1st Quartile: {_25}")
        st.markdown(f"2nd Quartile: {_50}")
        st.markdown(f"3rd Quartile: {_75}")
        st.markdown(f"Most Similar Qualifiers Beatmap (according to Player scores): {most_similar_player}")
    
    def render(self):
        self.score_distribution()
        self.tinder()
        

def main():
    players_qual_data, country_quals_data, _, _ = fetch_data()
    q = QualifiersStatisticsDashboard(players_qual_data, country_quals_data)
    q.render()

if __name__ == "__main__":
    main()
