import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np


def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId', inplace=True)
    meta = meta_df(titanic)
    multi_index = multi(meta, 'Age', 'Cabin', 'Survived', 'count')
    multi_bar(multi_index, 'count')



# Returns a series with survivor data
def survive_stats(df, col, kind='values'):
    if kind == 'values':
        return df[col].compress(df['Survived'].values)
    if kind == 'sum':
        return df.groupby(col).sum()['Survived']


# Creating a multiindex dataframe and performs groupby functions on it
def multi(df, index1, index2, col='Fare', func='mean'):
    new = df.set_index([index1, index2, df.index])
    new = new.sort_index()
    group = new.groupby(level=[index1, index2]).mean()[col]
    if func == 'count':
        group = new.groupby(level=[index1, index2]).count()[col]
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
    title = 'Survival Based on {}'.format(typestr)
    if 'Passengers with' in surname:
        title = '{} by Class'.format(surname)
    layout = lay(title, gtype, typestr, 'Number of Passengers')
    if gtype == 'stack':
        data = [survive_bar, deceased_bar]
        graph(data, layout)
    elif gtype == 'group':
        data = [survive_bar, total_bar]
        graph(data, layout)


# Prints histogram based on age data
def age_data(df, size=1):
    survive_age = survive_stats(df, 'Age')
    total_age = df['Age']
    data = [trace_input(total_age, 'Total', 'hist', size), trace_input(survive_age, 'Survivors', 'hist', size)]
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


# Creates bar charts based on multiindexes
def multi_bar(df, ftype):
    data = []
    df_index = list(df.unstack())
    for i in df_index:
        value = df.unstack()[i]
        data.append(trace_input(value, str(i)))
    layout = lay('Average Fare for Each Class Based on Port', 'group', 'Port', 'Fare')
    if ftype == 'count':
        layout = lay('Number of Passengers with {}s Based on {}'.format(list(df.index.names)[1], list(df.index.names)[0]), 'group',
                     str(list(df.index.names)[0]), 'Passengers')
    graph(data, layout)


# Data on passengers by class
def class_bar(df, col, gtype):
    total_class = df.groupby('Pclass').count()['Name']
    class_cabin = df.groupby('Pclass').count()[col]
    no_cabin = total_class - class_cabin
    barsort(class_cabin, total_class, no_cabin, gtype, 'Class', 'Passengers with ' + str(col), 'Total Passengers',
            'Passengers without ' + str(col))


# Creates a new meta dataframe
def meta_df(df):
    def age_filter(age):
        if 0 <= age < 13:
            return 'Child'
        elif 13 <= age < 18:
            return 'Teenager'
        elif 18 <= age <= 30:
            return 'Young Adult'
        elif 30 < age <= 65:
            return 'Adult'
        else:
            return 'Elderly'

    meta = pd.DataFrame(index=df.index)
    meta['Cabin'] = np.where(df['Cabin'].isnull().values, 'No Cabin', 'Has Cabin')
    meta['Survived'] = df['Survived']
    meta['SibSp'] = np.where(df['SibSp'] > 0, 'Has Siblings/Spouse', 'No Siblings/Spouse')
    meta['Parch'] = np.where(df['Parch'] > 0, 'Has Parents/Child', 'No Parents/Child')
    meta['Family'] = np.where((df['SibSp'] > 0) | (df['Parch'] > 0), 'Has Family', 'No Family')
    meta['Pclass'] = df['Pclass']
    meta['Survived'] = df['Survived']
    meta['Fare'] = df['Fare']
    meta['Age'] = df['Age'].apply(age_filter)
    meta['Embarked'] = df['Embarked']
    return meta


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


# Creates a histogram based on fare data
def fare_hist(df, col, size='1'):
    fare = df.set_index(col)
    fare.sort_index(inplace=True)
    data = []
    df_index = sorted(df[col].unique())
    for i in df_index:
        value = fare.loc[i]['Fare']
        data.append(trace_input(value, i, 'hist', size))
    layout = lay('Fare by {}'.format(col), 'overlay', 'Fare', 'Number of Passengers')
    graph(data, layout)


# Creates traces for the graph data
def trace_input(series, name='', graphtype='bar', size=1):
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
            xbins=dict(start=0, end=600, size=size),
            opacity=0.75,
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
