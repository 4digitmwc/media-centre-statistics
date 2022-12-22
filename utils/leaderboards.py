from sqlite3 import Connection
import pandas as pd
import streamlit as st

from .data_objects import ScoreHighlight, PickBanStatistics

class PickBanComponent:
    def __init__(self, pick_ban_statistics: PickBanStatistics):
        self.pick_ban_statistics = pick_ban_statistics
    
    def _html(self):
        ...

    def _render(self):
        html = self._html()
        st.markdown(html, True)

class ScoreHighlightComponent:
    def __init__(self, score_highlight: ScoreHighlight):
        self.score_highlight = score_highlight
    
    def _html(self):
        return """
            <style>
                .subcontainer {
                    display: flex;
                }
                .score-description {
                    display: block;
                }
                .score {
                    display: flex;
                    background-color: gray;
                    text-decoration-color: white;
                }
                .description {
                    background-color: white;
                    text-decoration-color: black;
                    width: 727px;
                }
            </style>
            <div class="container">
                <div class="subcontainer">
                    <div class="beatmap-thumbnail">
                        <img src="3" width="256" height="256" alt="bg" />
                    </div>
                    <div class="score-description">
                        <div class="score">
                            <div class="player-map">
                                {0} <br> {1}
                            </div>
                            <div class="score-number">
                                999876
                            </div>
                        </div>
                        <div class="description">
                            {2}
                        </div>
                    </div>
                </div>
                <div class="screenshot">
                    <img src="{4}" alt="screenshot" width="1080" height="700"/>
                </div>
            </div>
        """.format(
            self.score_highlight.user_name, 
            self.score_highlight.beatmap_metadata, 
            self.score_highlight.score_description, 
            self.score_highlight.beatmap_thumbnail, 
            self.score_highlight.screenshot_url
        )

    def _render(self):
        html = self._html()
        st.markdown(html, True)

class Interface:
    def __init__(self, conn: Connection):
        self._conn = conn
    
    def _run_sql(self, sql, **kwargs):
        return pd.read_sql(sql, self._conn, params=kwargs)

    def _leaderboard(self, beatmap_id):
        sql = f"""
            SELECT * FROM scores WHERE beatmap_id=:beatmap_id
        """
        leaderboard = self._run_sql(sql, beatmap_id=beatmap_id)
        st.dataframe(leaderboard)

    def _score_highlights(self):
        ...
