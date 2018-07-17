import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go


def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId')
    total_length = len(titanic.index)
    total_class = titanic.groupby('Pclass').count()['PassengerId']
    bar_data(titanic, 'Embarked', 'group')


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
    if type == 'stack':
        bar(survive, deceased, type, 'Survival Based on ' + str(typestr), 'Survivors', 'Deceased', typestr)
    elif type == 'group':
        bar(survive, total, type, 'Survival Based on ' + str(typestr), 'Survivors', 'Total', typestr)


def age_data(df):
    survive_age = survive_count(df, 'Age')
    total_age = df['Age']
    hist(total_age, survive_age, 'overlay', 'Survival Based on Age', 'Total', 'Survivors', 'Age')


# Creates a comparative bar chart.
def bar(first, second, type, title, first_name='First', second_name='Second', xtitle=''):
    trace1 = go.Bar(
        x=first.index.tolist(),
        y=first.values,
        name=first_name
    )
    trace2 = go.Bar(
        x=second.index.tolist(),
        y=second.values,
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
            title='Number of Passengers'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=(str(title) + '.html'), auto_open=True)


# Creates a comparative histogram
def hist(first, second, type, title, first_name='First', second_name='Second', xtitle=''):
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
            title='Number of Passengers'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=(str(title) + '.html'), auto_open=True)


if __name__ == '__main__':
    main()
