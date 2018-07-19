import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go


def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId')
    total_length = len(titanic.index)
    bar_data(titanic, 'Cabin', 'stack')

# Returns a series with the survivor count
def survive_count(df, col):
    return df[col].compress(df['Survived'].values)


# Returns a series with the survivor total
def survive_total(df, col):
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
    survive = survive_total(df, col)
    total = df[col].value_counts()
    deceased = total - survive
    if col == 'Sex':
        barsort(survive, total, deceased, gtype, 'Gender')
    elif col == 'Pclass':
        barsort(survive, total, deceased, gtype, 'Class')
    elif col == 'Embarked':
        barsort(survive, total, deceased, gtype, 'Departure Port')
    elif col == 'Cabin':
        barsort(survive, total, deceased, gtype, 'Cabin')


# Sorts bar data based on if the user wants a stacked or grouped chart
def barsort(survive, total, deceased, gtype, typestr):
    survive_bar = trace_input(survive, 'Survivors')
    total_bar = trace_input(total, 'Total')
    deceased_bar = trace_input(deceased, 'Deceased')
    layout = lay('Survival Based on ' + str(typestr), gtype, typestr, 'Number of Passengers')
    if gtype == 'stack':
        data = [survive_bar, deceased_bar]
        graph(data, layout)
    elif gtype == 'group':
        data = [survive_bar, total_bar]
        graph(data, layout)


# Prints histogram based on age data
def age_data(df):
    survive_age = survive_count(df, 'Age')
    total_age = df['Age']
    data = [trace_input(total_age, 'Total', 'hist'), trace_input(survive_age, 'Survivors', 'hist')]
    layout = lay('Survival Based on Age', 'overlay', 'Age', 'Number of Passengers')
    graph(data, layout)


# Creates bar graphs based on fare data
def fare_data(df, col):
    avg_fare = df.groupby(col).mean()['Fare']
    sur_fare = survive_count(df, 'Fare')
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


def cabin_data(df):
    total_class = df.groupby('Pclass').count()['PassengerId']
    class_cabin = df.groupby('Pclass').count()['Cabin']
    bar_total_class = trace_input(total_class, 'Total Passengers')
    bar_class_cabin = trace_input(class_cabin, 'Passengers with Cabins')
    data = [bar_total_class, bar_class_cabin]
    layout = lay('Passengers with Cabins Compared to All, Sorted By Class', 'group', 'Class', 'Passengers')
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
