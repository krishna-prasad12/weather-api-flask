from flask import Flask,render_template
import pandas


app=Flask(__name__)

stations=pandas.read_csv('data_small/stations.txt',skiprows=17)
stations=stations[['STAID','STANAME                                 ']]

@app.route('/')
def home_page():
    return render_template('home.html',data=stations.to_html())

@app.route('/api/v1/<station>/<date>')
def weather_api(station,date):
    filepath='data_small/TG_STAID'+str(station).zfill(6)+'.txt'
    df=pandas.read_csv(filepath,skiprows=20,parse_dates=['    DATE'])
    temperature=df.loc[df['    DATE']==date]['   TG'].squeeze()/10
    return {"temperature":temperature,
             "station":station,
             "date":date
             }
@app.route('/api/v1/<station>')
def weather_station(station):
    filepath = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pandas.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
    #temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    new_df=df.to_dict(orient='records')
    return new_df
@app.route('/api/v1/year/<station>/<yr>')
def weather_station_yr(station,yr):
    filepath = 'data_small/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pandas.read_csv(filepath, skiprows=20)
    df['    DATE']=df['    DATE'].astype(str)
    result=df[df['    DATE'].str.startswith(str(yr))].to_dict()
    return result


if __name__=='__main__':
    app.run(debug=True)