import plotly.express as px

def get_bar_plot(x, y,  title, x_label, y_label): 

    x = list(x)
    y = list(y)
    dict_data = {
        x_label: x, 
        y_label: y
    }
    # setting figure size by using figure() function
    fig = px.bar(dict_data, x=x_label, y=y_label, title=title)
    fig.show()

def get_single_bar_plot(x, y, x_label, title, home_team, away_team):
    dict_data = {column: [value] for column , value in zip(x, y)}
    dict_data["Draw"] = dict_data.pop("draw")
    dict_data[f"{home_team} win"] = dict_data.pop(home_team)
    dict_data[f"{away_team} win"] = dict_data.pop(away_team)

    fig = px.bar(dict_data, title=title, orientation='h', height=500, labels={"variable": "Outcomes"})
    fig.update_layout(xaxis_title=x_label, yaxis_title='')
    fig.update_yaxes(showticklabels=False)
    fig.show()


def get_time_line(home_team_xgs, away_team_xgs, home_team, away_team, ref_stat):
    data_dict = {}
    data_dict["Team"] = [home_team for _ in home_team_xgs] + [away_team for _ in away_team_xgs]
    data_dict["Minutes"] = [minute for (minute, _) in home_team_xgs] + [minute for (minute, _) in away_team_xgs]
    data_dict[ref_stat] = [xg for (_, xg) in home_team_xgs] + [xg for (_, xg) in away_team_xgs]

    fig = px.line(data_dict, x="Minutes", y=ref_stat, color='Team')
    fig.show()