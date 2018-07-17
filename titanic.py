import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

def main():
    titanic = pd.read_csv('titanic_data.csv')
    titanic['Survived'] = titanic['Survived'].astype(bool)
    titanic.set_index('PassengerId')
    






def male_v_female(df):
    survive = df.groupby('Sex').sum()['Survived']
    bar = go.Bar(
        x = survive.index.tolist(),
        y = survive.values
    )
    data = [bar]
    fig = go.Figure(data=data)
    py.plot(fig, filename='bar.html', auto_open=True)










if __name__ == '__main__':
    main()
