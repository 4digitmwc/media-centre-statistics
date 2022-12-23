from sqlite3 import Connection
import pandas as pd
import streamlit as st

from .data_objects import ScoreHighlight, PickBanStatistics

class PickBanComponent:
    def __init__(self, pick_ban_statistics):
        self.pick_ban_statistics = pick_ban_statistics
    
    @staticmethod
    def _html(pick_ban_statistics: dict):
        return """
            <div>
                <style>
                    .container {
                        display: flex;
                    }
                    .statistics {
                        display: block
                    }
                </style>
                <div class="container">
                    <div class="beatmap-thumbnail">
                        <img src="{beatmap_thumbnail}" alt="a" width="256" height="256" />
                    </div>
                    <div class="statistics">
                        <div class="metadata">
                            [{beatmap_type}{beatmap_tag}] {beatmap_metadata}
                        </div>
                        <div class="ban-rate">
                            <div class="ban-bar"></div>
                            <div class="not-ban-bar"></div>
                            Ban Rate: {ban_rate}%
                        </div>
                        <div class="pick-rate">
                            <div class="pick-bar"></div>
                            <div class="not-pick-bar"></div>
                            Pick Rate: {pick_rate}%
                        </div>
                        <div class="protect-rate">
                            <div class="protect-bar"></div>
                            <div class="not-protect-bar"></div>
                            Protect Rate: {protect_rate}%
                        </div>
                    </div>
                </div>
            </div>
        """.format_map(pick_ban_statistics)
    
    def render(self):
        st.markdown(self._html(self.pick_ban_statistics), True)

class ScoreHighlightComponent:
    def __init__(self, score_highlight):
        self.score_highlight = score_highlight
    
    @staticmethod
    def _html(score_highlight: dict):
        return """
            <div>
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
                            <img src="{beatmap_thumbnail}" width="256" height="256" alt="bg" />
                        </div>
                        <div class="score-description">
                            <div class="score">
                                <div class="player-map">
                                    {username} <br> {beatmap_metadata}
                                </div>
                                <div class="score-number">
                                    999876
                                </div>
                            </div>
                            <div class="description">
                                {highlight_description}
                            </div>
                        </div>
                    </div>
                    <div class="screenshot">
                        <img src="{highlight_screenshot}" alt="screenshot" width="1080" height="700"/>
                    </div>
                </div>
            </div>
        """.format_map(score_highlight)
    
    def render(self):
        st.markdown(self._html(self.score_highlight), True)

class Leaderboard:
    def __init__(self, conn: Connection):
        self._conn = conn
    
    def _run_sql(self, sql, **kwargs):
        return pd.read_sql(sql, self._conn, params=kwargs)

    def _leaderboard(self, beatmap_id):
        sql = f"""
            SELECT username, team_acronym, score FROM scores 
            LEFT JOIN users ON users.user_id = scores.user_id
            WHERE scores.beatmap_id=:beatmap_id ORDER BY scores.score DESC;
        """
        leaderboard = self._run_sql(sql, beatmap_id=beatmap_id)
        st.dataframe(leaderboard)

class StatisticsDashboard:
    """
    TODO:
    - [x] Maps with most ban rate and pick rate: automatically shown
    - [ ] mvp: manually selected from ETI/observation
    - [ ] score distributions & quartiles for team and players: easily done using sql
    - [ ] did you know?
    """
    def __init__(self, conn: Connection, rnd: str):
        self._conn = conn
        self._rnd = rnd
    
    def _run_sql(self, sql, **kwargs):
        if kwargs:
            return pd.read_sql(sql, self._conn, params=kwargs)
        return pd.read_sql(sql, self._conn)

    def most_banned_maps(self):
        sql = """
            SELECT * FROM beatmaps WHERE ban_rate = (
                SELECT MAX(ban_rate) FROM beatmaps WHERE beatmap_round=:rnd
            ) WHERE beatmap_round=:rnd;
        """
        result = self._run_sql(sql)
        return result

    def most_picked_maps(self):
        sql = """
            SELECT * FROM beatmaps WHERE pick_rate = (
                SELECT MAX(pick_rate) FROM beatmaps WHERE beatmap_round=:rnd
            ) WHERE beatmap_round=:rnd;
        """
        result = self._run_sql(sql)
        return result

    def most_protected_maps(self):
        sql = """
            SELECT * FROM beatmaps WHERE protect_rate = (
                SELECT MAX(protect_rate) FROM beatmaps WHERE beatmap_round=:rnd
            ) WHERE beatmap_round=:rnd;
        """
        result = self._run_sql(sql)
        return result

    def mvp(self):
        ...
    
    def summary_scores(self, beatmap_id):
        ...
    
    def hist_scores(self, beatmap_id):
        ...
    
    def did_you_know(self, text):
        ...
