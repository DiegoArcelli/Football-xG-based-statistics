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

def get_single_bar_plot(x, y,  title):
    dict_data = {column: [value] for column , value in zip(x, y)}
    fig = px.bar(dict_data, title=title, orientation='h', height=500)
    fig.show()


def get_time_line(home_team_xgs, away_team_xgs, home_team, away_team, ref_stat):
    data_dict = {}
    data_dict["Team"] = [home_team for _ in home_team_xgs] + [away_team for _ in away_team_xgs]
    data_dict["Minute"] = [minute for (minute, _) in home_team_xgs] + [minute for (minute, _) in away_team_xgs]
    data_dict[ref_stat] = [xg for (_, xg) in home_team_xgs] + [xg for (_, xg) in away_team_xgs]

    fig = px.line(data_dict, x="Minute", y=ref_stat, color='Team')
    fig.show()