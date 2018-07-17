import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go


def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId')
    total_length = len(titanic.index)
    age_data(titanic)


# Prints bar charts based on sex data
def sex_data(df):
    survive_sex = survive_total(df, 'Sex')
    total_sex = df['Sex'].value_counts()
    deceased_sex = total_sex - survive_sex
    bar(survive_sex, deceased_sex, 'stack', 'stack.html', 'Survivors', 'Deceased')
    bar(survive_sex, total_sex, 'group', 'group.html', 'Survivors', 'Total')


def age_data(df):
    survive_age = survive_count(df, 'Age')
    total_age = df['Age']
    hist(total_age, survive_age, 'overlay', 'Passengers By Age', 'Total', 'Survivors', 'Age', 'Number of Passengers')


# Returns a series with the survivor count
def survive_count(df, col):
    return df[col].compress(df['Survived'].values)


# Returns a series with the survivor total
def survive_total(df, col):
    return df.groupby(col).sum()['Survived']


# Creates a comparative bar chart.
def bar(first, second, type, filename, first_name='First', second_name='Second'):
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
        barmode=type
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename, auto_open=True)


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
