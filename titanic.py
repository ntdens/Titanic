import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go


def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId')
    total_length = len(titanic.index)
    sex_data(titanic)


# Prints bar charts based on sex data
def sex_data(df):
    survive_sex = survive(df, 'Sex')
    total_sex = df['Sex'].value_counts()
    deceased_sex = total_sex - survive_sex
    bar(survive_sex, deceased_sex, 'stack', 'stack.html', 'Survivors', 'Deceased')
    bar(survive_sex, total_sex, 'group', 'group.html', 'Survivors', 'Total')


# Returns a series with the total survivors of a column
def survive(df, col):
    return df.groupby(col).sum()['Survived']


# Takes two pandas series and a bar chart type and prints that bar chart.
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


if __name__ == '__main__':
    main()
