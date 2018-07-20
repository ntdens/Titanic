import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np


def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId', inplace=True)
    class_bar(titanic, 'Cabin', 'stack')


# Returns a series with survivor data
def survive_stats(df, col, kind='values'):
    if kind == 'values':
        return df[col].compress(df['Survived'].values)
    if kind == 'sum':
        return df.groupby(col).sum()['Survived']


# Creating a multiindex dataframe and performs groupby functions on it
def multi(df, index1, index2, func='mean'):
    new = df.set_index([index1, index2, df.index])
    new = new.sort_index()
    group = new.groupby(level=[index1, index2]).mean()['Fare']
    if func == 'count':
        group = new.groupby(level=[index1, index2]).count()['Fare']
    return group


# Prints bar charts based on data
def bar_data(df, col, gtype):
    survive = survive_stats(df, col, 'sum')
    total = df[col].value_counts()
    deceased = total - survive
    barsort(survive, total, deceased, gtype, str(col))


# Sorts bar data based on if the user wants a stacked or grouped chart
def barsort(survive, total, deceased, gtype, typestr, surname='Survivors', totname='Total', decname='Deceased'):
    survive_bar = trace_input(survive, surname)
    total_bar = trace_input(total, totname)
    deceased_bar = trace_input(deceased, decname)
    title = 'Survival Based on ' + str(typestr)
    if surname >= 'Passengers with':
        title = '{} by Class'.format(surname)
    layout = lay(title, gtype, typestr, 'Number of Passengers')
    if gtype == 'stack':
        data = [survive_bar, deceased_bar]
        graph(data, layout)
    elif gtype == 'group':
        data = [survive_bar, total_bar]
        graph(data, layout)


# Prints histogram based on age data
def age_data(df):
    survive_age = survive_stats(df, 'Age')
    total_age = df['Age']
    data = [trace_input(total_age, 'Total', 'hist'), trace_input(survive_age, 'Survivors', 'hist')]
    layout = lay('Survival Based on Age', 'overlay', 'Age', 'Number of Passengers')
    graph(data, layout)


# Creates bar graphs based on fare data
def fare_data(df, col):
    avg_fare = df.groupby(col).mean()['Fare']
    sur_fare = survive_stats(df, 'Fare')
    survive_fare = pd.DataFrame(index=df.index)
    survive_fare = survive_fare.join(sur_fare, how='right')
    survive_fare = survive_fare.join(df[col], how='left')
    survive_fare = survive_fare.groupby(col).mean()['Fare']
    bar_avg_fare = trace_input(avg_fare, 'Average Fare')
    bar_survive_fare = trace_input(survive_fare, 'Survivor Fare')
    data = [bar_avg_fare, bar_survive_fare]
    if col == 'Pclass':
        layout = lay('Cost of Tickets by Class of Survivors vs Average', 'group', 'Fare by Class', 'Price')
        graph(data, layout)
    elif col == 'Embarked':
        layout = lay('Cost of Tickets by Port of Survivors vs Average', 'group', 'Fare by Port', 'Price')
        graph(data, layout)


# Creates bar charts based on port-fare data
def portfare_data(df, ftype):
    port_fare = multi(df, 'Embarked', 'Pclass', func=ftype)
    port_first = port_fare.unstack()[1]
    port_second = port_fare.unstack()[2]
    port_third = port_fare.unstack()[3]
    first_trace = trace_input(port_first, '1st Class')
    second_trace = trace_input(port_second, '2nd Class')
    third_trace = trace_input(port_third, '3rd Class')
    layout = lay('Average Fare for Each Class Based on Port', 'group', 'Port', 'Fare')
    if ftype == 'count':
        layout = lay('Number of Tickets for Each Class Based on Port', 'group', 'Port', 'Tickets')
    data = [first_trace, second_trace, third_trace]
    graph(data, layout)


# Data on passengers by class
def class_bar(df, col, gtype):
    total_class = df.groupby('Pclass').count()['Name']
    class_cabin = df.groupby('Pclass').count()[col]
    no_cabin = total_class - class_cabin
    barsort(class_cabin, total_class, no_cabin, gtype, 'Class', 'Passengers with ' + str(col), 'Total Passengers',
            'Passengers without ' + str(col))


# Creates a new dataframe based on owning a cabin
def cabin_df(df):
    cabin = pd.DataFrame(index=df.index)
    cabin['Cabin'] = np.where(df['Cabin'].isnull().values, 'No Cabin', 'Has Cabin')
    cabin['Survived'] = df['Survived']
    return cabin


# Creates a new dataframe based on the existence of family members
def family_df(df):
    family = pd.DataFrame(index=df.index)
    family['SibSp'] = np.where(df['SibSp'] > 0, 'Has Siblings/Spouse', 'No Siblings/Spouse')
    family['Parch'] = np.where(df['SibSp'] > 0, 'Has Parents/Child', 'No Parents/Child')
    family['Fare'] = df['Fare']
    family['Survived'] = df['Survived']
    return family


# Creates box plots based on fares
def fare_box(df):
    new = df.set_index(['Pclass', df.index])
    new = new.sort_index()
    first = new.xs(1)['Fare']
    second = new.xs(2)['Fare']
    third = new.xs(3)['Fare']
    first_box = trace_input(first, '1st Class', 'box')
    second_box = trace_input(second, '2nd Class', 'box')
    third_box = trace_input(third, '3rd Class', 'box')
    data = [first_box, second_box, third_box]
    layout = lay('Fares by Class', '', 'Class', 'Fare')
    graph(data, layout)


# Creates traces for the graph data
def trace_input(series, name='', graphtype='bar'):
    trace = dict()
    if graphtype == 'bar':
        trace = go.Bar(
            x=series.index.tolist(),
            y=series.values,
            name=name
        )
    if graphtype == 'hist':
        trace = go.Histogram(
            histfunc='sum',
            xbins=dict(start=0, end=100, size=1),
            x=series,
            name=name
        )
    if graphtype == 'box':
        trace = go.Box(
            y=series,
            name=name
        )
    return trace


# Defines the layout of the graph
def lay(title, gtype, xtitle='', ytitle=''):
    layout = go.Layout(
        title=title,
        barmode=gtype,
        xaxis=dict(
            title=xtitle
        ),
        yaxis=dict(
            title=ytitle
        )
    )
    return layout


# Creates a graph.
def graph(data, layout):
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='graph.html', auto_open=True)


if __name__ == '__main__':
    main()
