import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go


def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId')
    total_length = len(titanic.index)
    total_class = titanic.groupby('Pclass').count()['PassengerId']
    fare_data(titanic, 'Embarked')


# Returns a series with the survivor count
def survive_count(df, col):
    return df[col].compress(df['Survived'].values)


# Returns a series with the survivor total
def survive_total(df, col):
    return df.groupby(col).sum()['Survived']


# Prints bar charts based on data
def bar_data(df, col, type):
    survive = survive_total(df, col)
    total = df[col].value_counts()
    deceased = total - survive
    if col == 'Sex':
        barsort(survive, total, deceased, type, 'Gender')
    elif col == 'Pclass':
        barsort(survive, total, deceased, type, 'Class')
    elif col == 'Embarked':
        barsort(survive, total, deceased, type, 'Departure Port')


# Sorts bar data based on if the user wants a stacked or grouped chart
def barsort(survive, total, deceased, type, typestr):
    survive_bar = bar_input(survive, 'Survivors')
    total_bar = bar_input(total, 'Total')
    deceased_bar = bar_input(deceased, 'Deceased')
    if type == 'stack':
        data = [survive_bar, deceased_bar]
        bar(data, type, 'Survival Based on ' + str(typestr), typestr, 'Number of Passengers')
    elif type == 'group':
        data = [survive_bar, total_bar]
        bar(data, type, 'Survival Based on ' + str(typestr), typestr, 'Number of Passengers')


# Prints histogram based on age data
def age_data(df):
    survive_age = survive_count(df, 'Age')
    total_age = df['Age']
    hist(total_age, survive_age, 'overlay', 'Survival Based on Age', 'Total', 'Survivors', 'Age',
         'Number of Passengers')


# Creates bar graphs based on fare data
def fare_data(df, col):
    avg_fare = df.groupby(col).mean()['Fare']
    sur_fare = survive_count(df, 'Fare')
    survive_fare = pd.DataFrame(index=df.index)
    survive_fare = survive_fare.join(sur_fare, how='right')
    survive_fare = survive_fare.join(df[col], how='left')
    survive_fare = survive_fare.groupby(col).mean()['Fare']
    bar_avg_fare = bar_input(avg_fare, 'Average Fare')
    bar_survive_fare = bar_input(survive_fare, 'Survivor Fare')
    data = [bar_avg_fare, bar_survive_fare]
    if col == 'Pclass':
        bar(data, 'group', 'Cost of Tickets by Class of Survivors vs Average', 'Fare by Class', 'Price')
    elif col == 'Embarked':
        bar(data, 'group', 'Cost of Tickets by Port of Survivors vs Average', 'Fare by Port', 'Price')


# Creates traces for the bar graph data
def bar_input(series, name=''):
    trace = go.Bar(
        x=series.index.tolist(),
        y=series.values,
        name=name
    )
    return trace


# Creates a comparative bar chart.
def bar(data, type, title, xtitle='', ytitle=''):
    data = data
    layout = go.Layout(
        title=title,
        barmode=type,
        xaxis=dict(
            title=xtitle
        ),
        yaxis=dict(
            title=ytitle
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=(str(title) + '.html'), auto_open=True)


# Creates a comparative histogram
def hist(first, second, type, title, first_name='First', second_name='Second', xtitle='', ytitle=''):
    trace1 = go.Histogram(
        histfunc='sum',
        xbins=dict(start=0, end=100, size=1),
        x=first,
        name=first_name
    )
    trace2 = go.Histogram(
        histfunc='sum',
        xbins=dict(start=0, end=100, size=1),
        x=second,
        name=second_name
    )
    data = [trace1, trace2]
    layout = go.Layout(
        title=title,
        barmode=type,
        xaxis=dict(
            title=xtitle
        ),
        yaxis=dict(
            title=ytitle
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=(str(title) + '.html'), auto_open=True)


if __name__ == '__main__':
    main()
