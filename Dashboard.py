import pandas as pd
import decoration as deco
import plotly
import plotly.io as pio
import plotly.express as px  # (version 4.7.0 or higher)
# import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

df = pd.read_excel("Attrition.xlsx")
df2 = pd.read_excel('Attrition_jbs.xlsx')

#Adding a group called age group
df['Age group'] = 'gg'
for i in range(1470):
    if df['Age'][i] <= 30:
        df['Age group'][i] = 'less than 30'
    elif df['Age'][i]<=40:
        df['Age group'][i] = '40 - 30'
    elif df['Age'][i]<=50:
        df['Age group'][i] = '50 - 40'
    elif df['Age'][i]<=60:
        df['Age group'][i] = '60 - 50'

#the relevant bar plot for the age groups
fig_barplot = px.histogram(df, x= 'Age group',
                color='Attrition', barmode='group',
                height=400,
                title = "Attrition by Age groups"
                )
fig_barplot.update_layout(
        width = 400,
        height = 400,
    )

#filters out males and females to draw the pie chart
df_males = pd.DataFrame(df["Attrition"][df["Gender"] == "Male"], columns=['Attrition'])
df_females = pd.DataFrame(df["Attrition"][df["Gender"] == "Female"], columns=['Attrition'])


df_Single = pd.DataFrame(df["Attrition"][df["MaritalStatus"] == "Single"], columns=['Attrition'])
df_Married = pd.DataFrame(df["Attrition"][df["MaritalStatus"] == "Married"], columns=['Attrition'])
df_Divorced = pd.DataFrame(df["Attrition"][df["MaritalStatus"] == "Divorced"], columns=['Attrition'])

df['JobRole'].unique()
df1=pd.pivot_table(df, index=['Attrition'], columns=['JobRole'],  values=['EmployeeNumber'],aggfunc='count')


def edu_field(Attr,choice):
    """Returns a dataframe with 'EducationField' and 'count'"""
    return df[[choice , 'Attrition']][(df['Attrition'] == Attr)]

def job_invol(Attr):
    """Returns a Dataframe with 'Job Involvement' and its counts"""
    df_slice = df[['JobInvolvement', 'Age']][df['Attrition'] == Attr]
    return df_slice.groupby(['JobInvolvement']).count().reset_index().rename(columns={'Age': 'count'})


def update_graph(value):
    if value == 'YES':
        xx = ['Healthcare Representative', 'Human Resources', 'Laboratory Technician', 'Manager',
              'Manufacturing Director', 'Research Director', 'Research Scientist', 'Sales Executive',
              'Sales Representative']
        y1 = [9, 12, 62, 5, 10, 2, 47, 57, 33]
        col = 'red'
    if value == 'NO':
        xx = ['Healthcare Representative', 'Human Resources', 'Laboratory Technician', 'Manager',
              'Manufacturing Director', 'Research Director', 'Research Scientist', 'Sales Executive',
              'Sales Representative']
        y1 = [122, 40, 197, 97, 135, 78, 245, 269, 50]
        col = 'green'
    return {'data': [go.Bar(
        x=xx,
        y=y1,
        marker_color=col),

    ],
        'layout': go.Layout(

            plot_bgcolor='#26332a',
            paper_bgcolor='#26332a',

            xaxis=dict(

                title='JOB ROLE',
                showgrid=True,
                showline=True,
                color='white',
                linewidth=1,

            ),
            yaxis=dict(
                title='Count',
                showgrid=True,
                showline=True,
                gridcolor='#bdbdbd',
                color='white',
                linewidth=1
            ),

            hovermode='closest',

        )
    }



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1("Employee Attrition Analysis", style=deco.style_h1))),
    html.Br(),
    dbc.Row([dbc.Col(dcc.Dropdown(id='piechart-dropdown',options=[{'label': 'Attrition of Males', 'value': 'Males'},
                                                                  {'label': 'Attrition of Females', 'value': 'Females'}],
                                                        value='Males',
                                                        style={'width': '80%'} )),

            dbc.Col(dcc.Dropdown(id ='Dept_edufield_dropdown',options=[{'label': 'Education Field', 'value':'EducationField'},
                                                                       {'label': 'Department', 'value':'Department'}],
                                                                value = 'EducationField',
                                                                style={'width': '100%'}), width={'size':4}),

            dbc.Col(dcc.Dropdown(id='edufield_attr_dropdown', options=[{'label': 'Attrition: Yes', 'value':'Yes'},
                                                                        {'label': 'Attrition: No', 'value':'No'}],
                                                                value = 'Yes',
                                                                style={'width': '100%'}),width={'size':4})]),

    dbc.Row([dbc.Col(dcc.Graph(id= 'pie-chart',figure={})), dbc.Col(dcc.Graph(id='fig_edufield_barplot',figure={})), dbc.Col(dcc.Graph(id='fig_jobinvol_pieplot',figure={}))]),
    dbc.Row(html.Br()),

    dbc.Row(dbc.Col( dcc.Dropdown(id='piechart-dropdown_marital',options=[{'label': 'Attrition of Single Employees', 'value': 'Single'},
                                                            {'label': 'Attrition of Married Employees', 'value': 'Married'},
                                                            {'label': 'Attrition of Divorced Employees', 'value': 'Divorced'}],
                                                    value='Single',
                                                    style= {'width': '90%' }), width={'size':3,'offset':3})),
    dbc.Row([dbc.Col(dcc.Graph(figure=fig_barplot),width=3),dbc.Col(dcc.Graph(id="pie-chart_marital", figure={}),width={'size':4}),
            dbc.Col(dcc.Graph(id ='Samplechart',style={'width': '80vh', 'height': '60vh'},
                    figure={'data':[{'x':df2.Jobe_satisfication,
                                     'y':df2.AttritionNo,
                                     'type':'bar','name':'Attrition-NO','marker': {'color': '#1A8F81'}},
                                    {'x':df2.Jobe_satisfication,
                                     'y':df2.AttritionYes,
                                    'type':'bar','name':'Attrition-Yes','marker': {'color': '#1AB181'}
                                    },],'layout':{
                                             'plot_bgcolor':'#111111',

                                             'title':'Job Specification With Respect To Attrition',
                                             'xaxis':{
                                            'title':'Job Specification'
                                                },
                                             'yaxis':{
                                             'title':'Number of Employees'
                                                }}}
            )),]),
    dbc.Row(dbc.Col(dcc.Dropdown(
            id='dropdown1',
            options=[{'label': 'Attrition-Yes', 'value': 'YES'} ,
                     {'label': 'Attrition-No', 'value': 'NO'}],
            value='YES',style={'width': '70%'}),width={'size':6 ,'offset':6})),
    dbc.Row(html.Br()),
    dbc.Row([dbc.Col(dcc.Graph(figure = px.scatter(df, x='MonthlyIncome', y='TotalWorkingYears', color='Attrition', symbol="Attrition"),
              style={'height':'550px','width':'700px', 'pad':'100px','plot_bgcolor':'#111111'})),
            dbc.Col(dcc.Graph(
                id='graph1',
                className='dropgraph',
                style={'width':'500px','height':'450px'}
                ))])

])


@app.callback(
    [Output(component_id='pie-chart', component_property='figure'),
     Output(component_id= 'fig_edufield_barplot', component_property='figure'),
     Output(component_id= 'fig_jobinvol_pieplot', component_property='figure'),
     Output(component_id='pie-chart_marital', component_property='figure'),
     Output('graph1', 'figure')],
    [Input(component_id= 'piechart-dropdown', component_property= 'value'),
     Input(component_id='edufield_attr_dropdown',component_property='value'),
     Input(component_id= 'Dept_edufield_dropdown',component_property='value'),
     Input(component_id='piechart-dropdown_marital', component_property='value'),
     Input('dropdown1', 'value')]
)

def generate_charts(optn_slctd,Attrition, choice,option_marital,job_role):
    if optn_slctd == 'Males':
        df_chosen = df_males
    elif optn_slctd == 'Females':
        df_chosen = df_females

    if option_marital == 'Single':
        dff = df_Single
    elif option_marital == 'Married':
        dff = df_Married
    elif option_marital == 'Divorced':
        dff = df_Divorced

    fig_pie_attr = px.pie(
        data_frame=df_chosen,
        values=df_chosen.count(axis=1),
        names="Attrition",
        color='Attrition',
        color_discrete_map={"No": "#00e2f2", "Yes": "#1212cc"},
        hole = 0.4,
        title=f"Attrition vs {optn_slctd}"
    )
    fig_pie_attr.update_layout(
        width = 500,
        height = 500,
    )
    df_edufield = edu_field(Attrition, choice)
    fig_edufield_bar = px.histogram(df_edufield, x=choice,title=f"Attrition: {Attrition} VS {choice}")
    fig_edufield_bar.update_layout(
        width=500,
        height=500,
    )

    df_jobinvol_pie_data = job_invol(Attrition)
    fig_jobinvol_pieplot = px.pie(df_jobinvol_pie_data,
                                  names=['JobInvolvement : 1', 'JobInvolvement : 2', 'JobInvolvement : 3',
                                         'JobInvolvement : 4'], values='count',title=f"Job-Involvement VS Attrition: {Attrition}")
    fig_jobinvol_pieplot.update_layout(
        width=500,
        height=500,
    )

    fig_pie_plot_marital = px.pie(
        data_frame=dff,
        values=dff.count(axis=1),
        names="Attrition",
        color='Attrition',
        color_discrete_map={"No": "#356115", "Yes": "#78e32b"},
        hole=0.4,
        title= f"Attrition vs Marital Status: {option_marital}"
    )
    fig_pie_plot_marital.update_layout(
        width=500,
        height=500,
    )

    return [fig_pie_attr, fig_edufield_bar,fig_jobinvol_pieplot,fig_pie_plot_marital, update_graph(job_role)]


if __name__ == '__main__':
    app.run_server(debug=True)