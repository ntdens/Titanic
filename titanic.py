import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId')
    total_length = len(titanic.index)

    sex = titanic['Sex'].value_counts()
    print(sex)
    male_v_female(titanic)



def male_v_female(df):
    survive = df.groupby('Sex').sum()['Survived']
    total = df['Sex'].value_counts()
    trace1 = go.Bar(
        x = survive.index.tolist(),
        y = survive.values,
        name = 'Survived'
    )
    trace2 = go.Bar(
        x = total.index.tolist(),
        y = total.values,
        name = 'Total'
    )
    data = [trace2, trace1]
    layout = go.Layout(
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='bar.html', auto_open=True)







if __name__ == '__main__':
    main()
