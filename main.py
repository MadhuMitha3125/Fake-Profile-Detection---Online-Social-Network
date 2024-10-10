# main.py
import os
import base64
import io
import math
from flask import Flask, flash, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
from datetime import datetime
from datetime import date
import random
from urllib.request import urlopen
import webbrowser

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from werkzeug.utils import secure_filename
from PIL import Image

import urllib.request
import urllib.parse
import socket    
import csv
#import xlrd 
import matplotlib as mpl
import seaborn as sns
from matplotlib import pyplot as plt
from collections import OrderedDict

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="social_bot"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('index.html',msg=msg)



@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM register")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        
        email=request.form['email']
        location=request.form['location']
        profession=request.form['profession']
        aadhar=request.form['aadhar']
        uname=request.form['uname']
        pass1=request.form['pass']
        
        cursor = mydb.cursor()

        now = datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
        sql = "INSERT INTO register(id,name,gender,dob,mobile,email,location,profession,aadhar,uname,pass,rdate) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,gender,dob,mobile,email,location,profession,aadhar,uname,pass1,rdate)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('index'))
        else:
            msg='Already Exist'
    return render_template('/register.html',msg=msg)

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    cnt=0
    uname=""
    
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where uname=%s",(uname,))
    data = mycursor.fetchone()

    return render_template('userhome.html',msg=msg,data=data)

@app.route('/user_post', methods=['GET', 'POST'])
def user_post():
    st=0
    uname=""
    cnt=0
    act=""
    file_name=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM register WHERE uname = %s', (uname, ))
    data = cursor.fetchone()

    pcursor = mydb.cursor()
    pcursor.execute('SELECT * FROM user_post u,register r where u.uname=r.uname order by u.id desc')
    pdata = pcursor.fetchall()

    pcursor1 = mydb.cursor()
    pcursor1.execute('SELECT count(*) FROM user_post WHERE uname = %s and status=1', (uname, ))
    cnt = pcursor1.fetchone()[0]
    print(cnt)
    
    if request.method=='GET':
        act = request.args.get('act')
    if request.method == 'POST':
        post= request.form['message']
        if 'file' not in request.files:
            flash('No file Part')
            return redirect(request.url)
        file= request.files['file']

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM user_post")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
            
        if file.filename == '':
            flash('No Select file')
            #return redirect(request.url)
        if file:
            fname = "P"+str(maxid)+file.filename
            file_name = secure_filename(fname)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+"/comments/", file_name))
            
        today = date.today()
        rdate = today.strftime("%d-%m-%Y")

        cursor2 = mydb.cursor()
        
        ########
        '''loc = ("dataset.xlsx") 
        # To open Workbook 
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0)
        nr=sheet.nrows
        i=0
        while i<nr:
            #print(sheet.cell_value(i, 0))
            dd=sheet.cell_value(i, 0)
            if post.find(dd) != -1:
                act="yes"
                st=1
                break
            i+=1'''
        filename = 'dataset.csv'
        tdata = pd.read_csv(filename, header=0)
        for tdat in tdata.values:
            dd=tdat[0]
            if post.find(dd)!= -1:
                act="yes"
                st=1
                break
        ###########
        if cnt==2:
            act="warn"
        elif cnt>=3:
            
            pcursor2 = mydb.cursor()
            pcursor2.execute('update register set dstatus=1 where uname = %s', (uname, ))
            mydb.commit()
            act="bot"

        
        sql = "INSERT INTO user_post (id,uname,text_post,photo,rdate,status) VALUES(%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,post,file_name,rdate,st)
        mycursor.execute(sql,val)
        print(sql,val)
        mydb.commit()
        msg="Upload success"
        return redirect(url_for('user_post',act=act))  
    
    return render_template('user_post.html',data=data,act=act,pdata=pdata)



@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    uname=""
    if 'username' in session:
        uname = session['username']
        print(uname)    
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM register WHERE uname = %s', (uname, ))
    data = mycursor.fetchone()
    
    
    if request.method=='POST':
        name = request.form['name']
        dob = request.form['dob']
        contact = request.form['mobile']
        email = request.form['email']
        location = request.form['location']
        profession = request.form['profession']
        aadhar = request.form['aadhar']
        #filename=('uname.txt')
        #fileread=open(filename,"r+")
        #uname=fileread.read()
        #fileread.close()
        
        sql=("update register set name=%s, dob=%s,mobile=%s,email=%s,location=%s,profession=%s,aadhar=%s,status=1 where uname=%s")
        val=(name,dob, contact, email, location, profession,aadhar, uname)
        mycursor.execute(sql,val)
        mydb.commit()
        print(val)
        msg="success"
        return redirect(url_for('userhome',msg=msg))
    return render_template('edit_profile.html',data=data)


@app.route('/change_profile', methods=['GET', 'POST'])
def change_profile():
    uid=""
    uname=""
    print(uid)
    if 'username' in session:
        uname = session['username']
    print(uname)

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where uname=%s",(uname,))
    data = mycursor.fetchone()
    
    if request.method=='GET':
        act = request.args.get('act')
        uid = request.args.get('uname')
        
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file Part')
            return redirect(request.url)
        file= request.files['file']
        print(file)
        if file.filename == '':
            flash('No Select file')
            return redirect(request.url)
        if file:
            fname = file.filename
            fimg = uname+".png"
            file_name = secure_filename(fimg)
            print(file_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+"/photo/", file_name))
            
            
            mycursor.execute("update register set photo=1 where uname=%s", (uname, ))
            mydb.commit()
            msg="Upload success"
            return redirect(url_for('userhome'))  
    
    return render_template('change_profile.html',data=data)

@app.route('/admin_user_view', methods=['GET', 'POST'])
def admin_user_view():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM register where dstatus=0')
    data = cursor.fetchall()
    return render_template('admin_user_view.html',data=data)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM register where dstatus=0')
    data = cursor.fetchall()
    cursor.execute('SELECT * FROM register where dstatus=1')
    data2 = cursor.fetchall()

    cursor.execute('SELECT count(*) FROM user_post')
    cnt = cursor.fetchone()[0]

    cursor.execute('SELECT count(*) FROM user_post where status=0')
    cnt2 = cursor.fetchone()[0]

    cursor.execute('SELECT count(*) FROM user_post where status=1')
    cnt3 = cursor.fetchone()[0]

    per_hu=0
    per_bot=0

    if cnt2>0:
        per_hu=(cnt2/cnt)*100
    else:
        per_hu=0
        
    if cnt3>0:
        per_bot=(cnt3/cnt)*100
    else:
        per_bot=0
    
    dat=['Human','Bot']
    dat1=[per_hu,per_bot]
    courses = dat #list(data.keys())
    values = dat1 #list(data.values())
      
    fig = plt.figure(figsize = (10, 5))
     
    # creating the bar plot
    plt.bar(courses, values, color ='maroon',
            width = 0.4)
 


    plt.xlabel("Prediction")
    plt.ylabel("Percentage")
    plt.title("")

    
    fn="result.png"
    plt.savefig('static/chart/'+fn)
    #plt.close()
    plt.clf()
    
    return render_template('prediction.html',data=data,data2=data2,fn=fn)




############################################
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    
    if request.method=='POST':
        
        file = request.files['file']
        #try:
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fn="datafile.csv"
            fn1 = secure_filename(fn)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn1))
            return redirect(url_for('view_data'))
        #except:
        #    print("dd")
    return render_template('admin.html',msg=msg)

@app.route('/admin1', methods=['GET', 'POST'])
def admin1():
    msg=""
    cnt=0
    rows=0
    cols=0
    data=[]
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt
    if request.method=='POST':
        return redirect(url_for('preprocess'))
    return render_template('admin1.html',data=data, msg=msg, rows=rows, cols=cols)

@app.route('/admin2', methods=['GET', 'POST'])
def admin2():
    msg=""
    cnt=0
    rows=0
    cols=0
    data=[]
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt
    if request.method=='POST':
        return redirect(url_for('preprocess'))
    return render_template('admin2.html',data=data, msg=msg, rows=rows, cols=cols)

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=""
    cnt=0
    rows=0
    cols=0
    data=[]
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    #rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    #cols=cnt

    # Generate a Pandas DataFrame
    dataset_path="twitter_human_bots_dataset.csv"
    twitter_accounts_df: pd.DataFrame = pd.read_csv(dataset_path, index_col=0)
    print(f"Dataset shape {twitter_accounts_df.shape}")

    # Preprocess boolean columns
    boolean_cols: list = ["default_profile", "default_profile_image",
                      "geo_enabled", "verified"]
    twitter_accounts_df = convert_bool_to_int(data=twitter_accounts_df, boolean_cols=boolean_cols)
    twitter_accounts_df.head()
    len1=len(twitter_accounts_df.head())
    data1=twitter_accounts_df

    rows=len(data1.values)
    cols=19
    
    if request.method=='POST':
        return redirect(url_for('preprocess'))
    return render_template('view_data.html',data=data, msg=msg, rows=rows, cols=cols)




######################################
# Functions to preprocess the DataFrame
def convert_bool_to_int(data: pd.DataFrame, boolean_cols: list):
    try:
        for col in boolean_cols:
            data[col] = data[col].astype(int)
    except Exception as e:
        print(e)
    return data

def popularity_metric(friends_count: int, followers_count: int):
    return np.round(np.log(1+friends_count) * np.log(1+followers_count), 3)


def compute_popularity_metric(row):
    return popularity_metric(friends_count=row["friends_count"],
                             followers_count=row["followers_count"])


@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    # Generate a Pandas DataFrame
    dataset_path="twitter_human_bots_dataset.csv"
    twitter_accounts_df: pd.DataFrame = pd.read_csv(dataset_path, index_col=0)
    print(f"Dataset shape {twitter_accounts_df.shape}")

    # Preprocess boolean columns
    boolean_cols: list = ["default_profile", "default_profile_image",
                      "geo_enabled", "verified"]
    twitter_accounts_df = convert_bool_to_int(data=twitter_accounts_df, boolean_cols=boolean_cols)
    twitter_accounts_df.head()
    data1=twitter_accounts_df
    #print(data1)
    data=[]
    j=0

    
    rows=len(data1.values)
    for ds in data1.values:
        
        if j<500:
            dd1=[]
            i=0
            while i<19:
                
                dd1.append(ds[i])
                i+=1
            data.append(dd1)
        j+=1
    cols=i
    if request.method=='POST':
        return redirect(url_for('preprocess2'))
    return render_template('preprocess.html',data=data,cols=cols,rows=rows)

#####################
@app.route('/preprocess2', methods=['GET', 'POST'])
def preprocess2():
    # Prepare your file
    parent_dir: str = os.path.join('/kaggle', 'input', 'twitter-bots-accounts')
    dataset_name: str = "twitter_human_bots_dataset.csv"
    dataset_path: str = os.path.join(parent_dir, dataset_name)  
    print(f"Dataset directory: {dataset_path}")

    # Generate a Pandas DataFrame
    dataset_path="twitter_human_bots_dataset.csv"
    twitter_accounts_df: pd.DataFrame = pd.read_csv(dataset_path, index_col=0)
    print(f"Dataset shape {twitter_accounts_df.shape}")

    # Preprocess boolean columns
    boolean_cols: list = ["default_profile", "default_profile_image",
                      "geo_enabled", "verified"]
    twitter_accounts_df = convert_bool_to_int(data=twitter_accounts_df, boolean_cols=boolean_cols)
    twitter_accounts_df.head()
    

    twitter_accounts_df["popularity"] = twitter_accounts_df.apply(compute_popularity_metric, axis=1)

    # Let's show some examples of such value
    data1=twitter_accounts_df[['popularity']]

    #print(data1)
    data=[]
    j=0

    
    rows=len(data1.values)
    cols=1
    for ds in data1.values:
        
        if j<500:
            dd1=[]
            dd1.append(ds[0])
               
            data.append(dd1)
        j+=1
    ##############
    
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['figure.figsize'] = 12, 8
    mpl.rcParams['font.sans-serif'] = ['Tahoma']
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    # Set up some parameters for EDA
    palette: str = "husl"
    grouped: str = "account_type"
    default_value: str = "unknown"
    def get_labels_colors_from_pandas_column(df: pd.DataFrame, column: str, palette: str):
        data_labels: dict = dict()
        try:
            labels: list = df[column].unique().tolist()
            colors: list = sns.color_palette(palette, len(labels))
            data_labels: dict = dict(zip(labels, colors))
        except Exception as e:
            logger.error(e)
        return data_labels

    # Retrieve labels and additional parameters to plot figures
    data_labels: dict = get_labels_colors_from_pandas_column(
        df=twitter_accounts_df, column=grouped, palette=palette)
    # Show labels
    print(f"Unique Target values: {data_labels.keys()}")
    # Functions to plot data distributions
    def plot_multiple_histograms(data: pd.DataFrame,
                                 grouped_col: str,
                                 target_col: str,
                                 data_labels: dict):
        # Plot
        plt.figure(figsize=(12, 10))
        title = "\n"
        labels: list = list(data_labels.keys())
        for j, i in enumerate(labels):
            x = data.loc[data[grouped_col] == i, target_col]
            mu_x = round(float(np.mean(x)), 3)
            sigma_x = round(float(np.std(x)), 3)
            ax = sns.distplot(x, color=data_labels.get(i), label=i, hist_kws=dict(alpha=.1),
                              kde_kws={'linewidth': 2})
            ax.axvline(mu_x, color=data_labels.get(i), linestyle='--')
            ax.set(xlabel=f"{target_col.title()}", ylabel='Density')
            title += f"Parameters {str(i)}: $G(\mu=$ {mu_x}, $\sigma=$ {sigma_x} \n"
            ax.set_title(title)
        plt.legend(title="Account Type")
        plt.grid()
        plt.savefig('static/chart/chart1.png')
        plt.tight_layout()
        #plt.show()


    def plot_multiple_boxplots(data: pd.DataFrame, grouped_col: str, target_col: str,
                               palette: str = "husl"):
        plt.figure(figsize=(12, 10))

        means: dict = data.groupby([grouped_col])[target_col].mean().to_dict(OrderedDict)
        counter: int = 0

        bp = sns.boxplot(x=grouped_col, y=target_col, data=data, palette=palette, order=list(means.keys()))
        bp.set(xlabel='', ylabel=f"{target_col.title()}")
        ax = bp.axes

        for k, v in means.items():
            # every 4th line at the interval of 6 is median line
            # 0 -> p25 1 -> p75 2 -> lower whisker 3 -> upper whisker 4 -> p50 5 -> upper extreme value
            mean = round(v, 2)
            ax.text(
                counter,
                mean,
                f'{mean}',
                ha='center',
                va='center',
                fontweight='bold',
                size=10,
                color='white',
                bbox=dict(facecolor='#445A64'))
            counter += 1
        bp.figure.tight_layout()
        plt.savefig('static/chart/chart2.png')
        plt.grid()
        #plt.show()
    target: str = "popularity"  
    # Extract histograms
    plot_multiple_histograms(data=twitter_accounts_df, 
                             grouped_col=grouped,
                             data_labels=data_labels,
                             target_col=target)
    # Extract Box-plots
    plot_multiple_boxplots(data=twitter_accounts_df,
                           grouped_col=grouped,
                           target_col=target,
                           palette=palette)
    #################
    '''target: str = "average_tweets_per_day"  
    # Extract histograms
    plot_multiple_histograms(data=twitter_accounts_df, 
                             grouped_col=grouped,
                             data_labels=data_labels,
                             target_col=target)
    # Extract Box-plots
    plot_multiple_boxplots(data=twitter_accounts_df,
                           grouped_col=grouped,
                           target_col=target,
                           palette=palette)

    target_col: str = "verified"
    twitter_accounts_df2 = twitter_accounts_df.groupby([grouped, target_col])[grouped].count().unstack(target_col)
    twitter_accounts_df2.plot(kind='bar', stacked=True)'''
    ##################
    if request.method=='POST':
        return redirect(url_for('preprocess3'))
    return render_template('preprocess2.html',data=data,rows=rows,cols=cols)

#####################
@app.route('/preprocess3', methods=['GET', 'POST'])
def preprocess3():
    # Prepare your file
    parent_dir: str = os.path.join('/kaggle', 'input', 'twitter-bots-accounts')
    dataset_name: str = "twitter_human_bots_dataset.csv"
    dataset_path: str = os.path.join(parent_dir, dataset_name)  
    print(f"Dataset directory: {dataset_path}")

    # Generate a Pandas DataFrame
    dataset_path="twitter_human_bots_dataset.csv"
    twitter_accounts_df: pd.DataFrame = pd.read_csv(dataset_path, index_col=0)
    print(f"Dataset shape {twitter_accounts_df.shape}")

    # Preprocess boolean columns
    boolean_cols: list = ["default_profile", "default_profile_image",
                      "geo_enabled", "verified"]
    twitter_accounts_df = convert_bool_to_int(data=twitter_accounts_df, boolean_cols=boolean_cols)
    twitter_accounts_df.head()
    

    twitter_accounts_df["popularity"] = twitter_accounts_df.apply(compute_popularity_metric, axis=1)

    # Let's show some examples of such value
    data1=twitter_accounts_df[['popularity']]

    #print(data1)
    data=[]
    j=0

    
    rows=len(data1.values)
    cols=1
    for ds in data1.values:
        
        if j<500:
            dd1=[]
            dd1.append(ds[0])
               
            data.append(dd1)
        j+=1
    ##############
    
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['figure.figsize'] = 12, 8
    mpl.rcParams['font.sans-serif'] = ['Tahoma']
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    # Set up some parameters for EDA
    palette: str = "husl"
    grouped: str = "account_type"
    default_value: str = "unknown"
    def get_labels_colors_from_pandas_column(df: pd.DataFrame, column: str, palette: str):
        data_labels: dict = dict()
        try:
            labels: list = df[column].unique().tolist()
            colors: list = sns.color_palette(palette, len(labels))
            data_labels: dict = dict(zip(labels, colors))
        except Exception as e:
            logger.error(e)
        return data_labels

    # Retrieve labels and additional parameters to plot figures
    data_labels: dict = get_labels_colors_from_pandas_column(
        df=twitter_accounts_df, column=grouped, palette=palette)
    # Show labels
    print(f"Unique Target values: {data_labels.keys()}")
    # Functions to plot data distributions
    def plot_multiple_histograms(data: pd.DataFrame,
                                 grouped_col: str,
                                 target_col: str,
                                 data_labels: dict):
        # Plot
        plt.figure(figsize=(12, 10))
        title = "\n"
        labels: list = list(data_labels.keys())
        for j, i in enumerate(labels):
            x = data.loc[data[grouped_col] == i, target_col]
            mu_x = round(float(np.mean(x)), 3)
            sigma_x = round(float(np.std(x)), 3)
            ax = sns.distplot(x, color=data_labels.get(i), label=i, hist_kws=dict(alpha=.1),
                              kde_kws={'linewidth': 2})
            ax.axvline(mu_x, color=data_labels.get(i), linestyle='--')
            ax.set(xlabel=f"{target_col.title()}", ylabel='Density')
            title += f"Parameters {str(i)}: $G(\mu=$ {mu_x}, $\sigma=$ {sigma_x} \n"
            ax.set_title(title)
        plt.legend(title="Account Type")
        plt.grid()
        plt.savefig('static/chart/chart3.png')
        plt.tight_layout()
        #plt.show()


    def plot_multiple_boxplots(data: pd.DataFrame, grouped_col: str, target_col: str,
                               palette: str = "husl"):
        plt.figure(figsize=(12, 10))

        means: dict = data.groupby([grouped_col])[target_col].mean().to_dict(OrderedDict)
        counter: int = 0

        bp = sns.boxplot(x=grouped_col, y=target_col, data=data, palette=palette, order=list(means.keys()))
        bp.set(xlabel='', ylabel=f"{target_col.title()}")
        ax = bp.axes

        for k, v in means.items():
            # every 4th line at the interval of 6 is median line
            # 0 -> p25 1 -> p75 2 -> lower whisker 3 -> upper whisker 4 -> p50 5 -> upper extreme value
            mean = round(v, 2)
            ax.text(
                counter,
                mean,
                f'{mean}',
                ha='center',
                va='center',
                fontweight='bold',
                size=10,
                color='white',
                bbox=dict(facecolor='#445A64'))
            counter += 1
        bp.figure.tight_layout()
        plt.savefig('static/chart/chart4.png')
        plt.grid()
        #plt.show()
    target: str = "popularity"  
    # Extract histograms
    
    #################
    target: str = "average_tweets_per_day"  
    # Extract histograms
    plot_multiple_histograms(data=twitter_accounts_df, 
                             grouped_col=grouped,
                             data_labels=data_labels,
                             target_col=target)
    # Extract Box-plots
    plot_multiple_boxplots(data=twitter_accounts_df,
                           grouped_col=grouped,
                           target_col=target,
                           palette=palette)

    
   
    ##################
    if request.method=='POST':
        return redirect(url_for('cluster'))
    return render_template('preprocess3.html',data=data,rows=rows,cols=cols)

#####################
@app.route('/cluster', methods=['GET', 'POST'])
def cluster():
    # Prepare your file
    parent_dir: str = os.path.join('/kaggle', 'input', 'twitter-bots-accounts')
    dataset_name: str = "twitter_human_bots_dataset.csv"
    dataset_path: str = os.path.join(parent_dir, dataset_name)  
    print(f"Dataset directory: {dataset_path}")

    # Generate a Pandas DataFrame
    dataset_path="twitter_human_bots_dataset.csv"
    twitter_accounts_df: pd.DataFrame = pd.read_csv(dataset_path, index_col=0)
    print(f"Dataset shape {twitter_accounts_df.shape}")

    # Preprocess boolean columns
    boolean_cols: list = ["default_profile", "default_profile_image",
                      "geo_enabled", "verified"]
    twitter_accounts_df = convert_bool_to_int(data=twitter_accounts_df, boolean_cols=boolean_cols)
    twitter_accounts_df.head()
    

    twitter_accounts_df["popularity"] = twitter_accounts_df.apply(compute_popularity_metric, axis=1)

    # Let's show some examples of such value
    data1=twitter_accounts_df[['popularity']]

    #print(data1)
    data=[]
    j=0

    
    rows=len(data1.values)
    cols=1
    for ds in data1.values:
        
        if j<500:
            dd1=[]
            dd1.append(ds[0])
               
            data.append(dd1)
        j+=1
    ##############
    
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['figure.figsize'] = 12, 8
    mpl.rcParams['font.sans-serif'] = ['Tahoma']
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    # Set up some parameters for EDA
    palette: str = "husl"
    grouped: str = "account_type"
    default_value: str = "unknown"
    def get_labels_colors_from_pandas_column(df: pd.DataFrame, column: str, palette: str):
        data_labels: dict = dict()
        try:
            labels: list = df[column].unique().tolist()
            colors: list = sns.color_palette(palette, len(labels))
            data_labels: dict = dict(zip(labels, colors))
        except Exception as e:
            logger.error(e)
        return data_labels

    # Retrieve labels and additional parameters to plot figures
    data_labels: dict = get_labels_colors_from_pandas_column(
        df=twitter_accounts_df, column=grouped, palette=palette)
    # Show labels
    print(f"Unique Target values: {data_labels.keys()}")
    # Functions to plot data distributions
    def plot_multiple_histograms(data: pd.DataFrame,
                                 grouped_col: str,
                                 target_col: str,
                                 data_labels: dict):
        # Plot
        plt.figure(figsize=(12, 10))
        title = "\n"
        labels: list = list(data_labels.keys())
        for j, i in enumerate(labels):
            x = data.loc[data[grouped_col] == i, target_col]
            mu_x = round(float(np.mean(x)), 3)
            sigma_x = round(float(np.std(x)), 3)
            ax = sns.distplot(x, color=data_labels.get(i), label=i, hist_kws=dict(alpha=.1),
                              kde_kws={'linewidth': 2})
            ax.axvline(mu_x, color=data_labels.get(i), linestyle='--')
            ax.set(xlabel=f"{target_col.title()}", ylabel='Density')
            title += f"Parameters {str(i)}: $G(\mu=$ {mu_x}, $\sigma=$ {sigma_x} \n"
            ax.set_title(title)
        plt.legend(title="Account Type")
        plt.grid()
        plt.savefig('static/chart/chart5.png')
        plt.tight_layout()
        #plt.show()

    def plot_multiple_boxplots(data: pd.DataFrame, grouped_col: str, target_col: str,
                               palette: str = "husl"):
        plt.figure(figsize=(12, 10))

        means: dict = data.groupby([grouped_col])[target_col].mean().to_dict(OrderedDict)
        counter: int = 0

        bp = sns.boxplot(x=grouped_col, y=target_col, data=data, palette=palette, order=list(means.keys()))
        bp.set(xlabel='', ylabel=f"{target_col.title()}")
        ax = bp.axes

        for k, v in means.items():
            # every 4th line at the interval of 6 is median line
            # 0 -> p25 1 -> p75 2 -> lower whisker 3 -> upper whisker 4 -> p50 5 -> upper extreme value
            mean = round(v, 2)
            ax.text(
                counter,
                mean,
                f'{mean}',
                ha='center',
                va='center',
                fontweight='bold',
                size=10,
                color='white',
                bbox=dict(facecolor='#445A64'))
            counter += 1
        bp.figure.tight_layout()
        plt.savefig('static/chart/chart6.png')
        plt.grid()
        #plt.show()
    target: str = "popularity"  
    # Extract histograms
    
    
    #################
    

    target_col: str = "verified"
    twitter_accounts_df2 = twitter_accounts_df.groupby([grouped, target_col])[grouped].count().unstack(target_col)
    twitter_accounts_df2.plot(kind='bar', stacked=True)

    target: str = "statuses_count"  
    # Extract histograms
    plot_multiple_histograms(data=twitter_accounts_df, 
                             grouped_col=grouped,
                             data_labels=data_labels,
                             target_col=target)
    # Extract Box-plots
    plot_multiple_boxplots(data=twitter_accounts_df,
                           grouped_col=grouped,
                           target_col=target,
                           palette=palette)
   
    #################
    twitter_accounts_df[grouped] = twitter_accounts_df[grouped].astype('category')
    data33=twitter_accounts_df.dtypes
    #print(data3)
    data2=twitter_accounts_df

    data4=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data2)
    rows=len(data2.values)
    
    #print(data1.columns)
    col=data2.columns
    #print(data1[0])
    for ss in data2.values:
        cnt=len(ss)
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data2.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data4=np.vstack((arr3, arr4))
   
    #print(data4[0])
    cols=cnt
    mem=float(rows)*0.75
    data5=[]
    
    
    field=data4[0]
    
    i=0
    while i<20:
        dat1=[]
        dat1.append(field[i])
        dat1.append(data33[i])
        data5.append(dat1)
        i+=1
    
            
    
    ##################

    
    if request.method=='POST':
        return redirect(url_for('feature_select'))
    return render_template('cluster.html',data5=data5,rows=rows, cols=cols)

#####################
@app.route('/feature_select', methods=['GET', 'POST'])
def feature_select():
    # Prepare your file
    parent_dir: str = os.path.join('/kaggle', 'input', 'twitter-bots-accounts')
    dataset_name: str = "twitter_human_bots_dataset.csv"
    dataset_path: str = os.path.join(parent_dir, dataset_name)  
    print(f"Dataset directory: {dataset_path}")

    # Generate a Pandas DataFrame
    dataset_path="twitter_human_bots_dataset.csv"
    twitter_accounts_df: pd.DataFrame = pd.read_csv(dataset_path, index_col=0)
    print(f"Dataset shape {twitter_accounts_df.shape}")

  
    # Preprocess boolean columns
    boolean_cols: list = ["default_profile", "default_profile_image",
                      "geo_enabled", "verified"]
    twitter_accounts_df = convert_bool_to_int(data=twitter_accounts_df, boolean_cols=boolean_cols)
    twitter_accounts_df.head()
    

    twitter_accounts_df["popularity"] = twitter_accounts_df.apply(compute_popularity_metric, axis=1)
    ##############
    
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['figure.figsize'] = 12, 8
    mpl.rcParams['font.sans-serif'] = ['Tahoma']
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    # Set up some parameters for EDA
    palette: str = "husl"
    grouped: str = "account_type"
    default_value: str = "unknown"
    def get_labels_colors_from_pandas_column(df: pd.DataFrame, column: str, palette: str):
        data_labels: dict = dict()
        try:
            labels: list = df[column].unique().tolist()
            colors: list = sns.color_palette(palette, len(labels))
            data_labels: dict = dict(zip(labels, colors))
        except Exception as e:
            logger.error(e)
        return data_labels

    # Retrieve labels and additional parameters to plot figures
    data_labels: dict = get_labels_colors_from_pandas_column(
        df=twitter_accounts_df, column=grouped, palette=palette)
    # Show labels
    print(f"Unique Target values: {data_labels.keys()}")
    # Functions to plot data distributions
    def plot_multiple_histograms(data: pd.DataFrame,
                                 grouped_col: str,
                                 target_col: str,
                                 data_labels: dict):
        # Plot
        plt.figure(figsize=(12, 10))
        title = "\n"
        labels: list = list(data_labels.keys())
        for j, i in enumerate(labels):
            x = data.loc[data[grouped_col] == i, target_col]
            mu_x = round(float(np.mean(x)), 3)
            sigma_x = round(float(np.std(x)), 3)
            ax = sns.distplot(x, color=data_labels.get(i), label=i, hist_kws=dict(alpha=.1),
                              kde_kws={'linewidth': 2})
            ax.axvline(mu_x, color=data_labels.get(i), linestyle='--')
            ax.set(xlabel=f"{target_col.title()}", ylabel='Density')
            title += f"Parameters {str(i)}: $G(\mu=$ {mu_x}, $\sigma=$ {sigma_x} \n"
            ax.set_title(title)
        plt.legend(title="Account Type")
        plt.grid()
        plt.savefig('static/chart/chart5.png')
        plt.tight_layout()
        #plt.show()

    def plot_multiple_boxplots(data: pd.DataFrame, grouped_col: str, target_col: str,
                               palette: str = "husl"):
        plt.figure(figsize=(12, 10))

        means: dict = data.groupby([grouped_col])[target_col].mean().to_dict(OrderedDict)
        counter: int = 0

        bp = sns.boxplot(x=grouped_col, y=target_col, data=data, palette=palette, order=list(means.keys()))
        bp.set(xlabel='', ylabel=f"{target_col.title()}")
        ax = bp.axes

        for k, v in means.items():
            # every 4th line at the interval of 6 is median line
            # 0 -> p25 1 -> p75 2 -> lower whisker 3 -> upper whisker 4 -> p50 5 -> upper extreme value
            mean = round(v, 2)
            ax.text(
                counter,
                mean,
                f'{mean}',
                ha='center',
                va='center',
                fontweight='bold',
                size=10,
                color='white',
                bbox=dict(facecolor='#445A64'))
            counter += 1
        bp.figure.tight_layout()
        plt.savefig('static/chart/chart6.png')
        plt.grid()
        #plt.show()
    
    target: str = "statuses_count"  
    # Extract histograms
    plot_multiple_histograms(data=twitter_accounts_df, 
                             grouped_col=grouped,
                             data_labels=data_labels,
                             target_col=target)
    # Extract Box-plots
    plot_multiple_boxplots(data=twitter_accounts_df,
                           grouped_col=grouped,
                           target_col=target,
                           palette=palette)
    #print(data1)
    data=[]
    j=0

    # Preprocess Response variable (account type)
    twitter_accounts_df[grouped] = twitter_accounts_df[grouped].astype('category')
    
    data=twitter_accounts_df.dtypes
    #print(data[0])
    
    twitter_accounts_df[grouped] = twitter_accounts_df[grouped].cat.codes
    data1=twitter_accounts_df.head()
    #data1=twitter_accounts_df[grouped]
    #print(len(data1))

    #print(data1)
    
    data2=[]
    j=0
    rows=len(data1.values)
    for ds in data1.values:
        
        
        dd1=[]
        i=0
        while i<20:
            
            dd1.append(ds[i])
            i+=1
        data2.append(dd1)
        
    cols=i
    #####################33

    twitter_accounts_df_num: pd.DataFrame = twitter_accounts_df.copy()
    twitter_accounts_df_num: pd.DataFrame = twitter_accounts_df_num._get_numeric_data()
    data3=twitter_accounts_df_num.head()
    print(data3)
    data4=[]
    j=0
    rows=len(data1.values)
    for ds3 in data3.values:
        
        
        dd3=[]
        i=0
        while i<13:
            
            dd3.append(ds3[i])
            i+=1
        data4.append(dd3)
        
    cols=i
    ##################
    # Remove columns
    drop_cols: list = ["id"]
    twitter_accounts_df_num.drop(drop_cols, axis=1,inplace=True)
    data5=twitter_accounts_df_num.head()
    data6=[]
    j=0
    rows=len(data5.values)
    for ds5 in data5.values:
        
        
        dd5=[]
        i=0
        while i<12:
            
            dd5.append(ds5[i])
            i+=1
        data6.append(dd5)
        
    cols=i
    ##################
    
    if request.method=='POST':
        return redirect(url_for('classify'))
    return render_template('feature_select.html',data2=data2,data4=data4,data6=data6)
###
#BiLSTM
def tag_dataset():
    correctLabels = []
    predLabels = []
    b = Progbar(len(dataset))
    for i,data in enumerate(dataset):    
        tokens, casing,char, labels = data
        tokens = np.asarray([tokens])     
        casing = np.asarray([casing])
        char = np.asarray([char])
        pred = model.predict([tokens, casing,char], verbose=False)[0]   
        pred = pred.argmax(axis=-1) #Predict the classes            
        correctLabels.append(labels)
        predLabels.append(pred)
        b.update(i)
    b.update(i+1)
    return predLabels, correctLabels

def prepare():
    trainSentences = readfile("data/train.txt")
    devSentences = readfile("data/valid.txt")
    testSentences = readfile("data/test.txt")

    trainSentences = addCharInformatioin(trainSentences)
    devSentences = addCharInformatioin(devSentences)
    testSentences = addCharInformatioin(testSentences)

    labelSet = set()
    words = {}

    for dataset in [trainSentences, devSentences, testSentences]:
        for sentence in dataset:
            for token,char,label in sentence:
                labelSet.add(label)
                words[token.lower()] = True

    # :: Create a mapping for the labels ::
    label2Idx = {}
    for label in labelSet:
        label2Idx[label] = len(label2Idx)

    # :: Hard coded case lookup ::
    case2Idx = {'numeric': 0, 'allLower':1, 'allUpper':2, 'initialUpper':3, 'other':4, 'mainly_numeric':5, 'contains_digit': 6, 'PADDING_TOKEN':7}
    caseEmbeddings = np.identity(len(case2Idx), dtype='float32')


    # :: Read in word embeddings ::
    word2Idx = {}
    wordEmbeddings = []

    fEmbeddings = open("embeddings/glove.6B.100d.txt", encoding="utf-8")

    for line in fEmbeddings:
        split = line.strip().split(" ")
        word = split[0]
        
        if len(word2Idx) == 0: #Add padding+unknown
            word2Idx["PADDING_TOKEN"] = len(word2Idx)
            vector = np.zeros(len(split)-1) #Zero vector vor 'PADDING' word
            wordEmbeddings.append(vector)
            
            word2Idx["UNKNOWN_TOKEN"] = len(word2Idx)
            vector = np.random.uniform(-0.25, 0.25, len(split)-1)
            wordEmbeddings.append(vector)

        if split[0].lower() in words:
            vector = np.array([float(num) for num in split[1:]])
            wordEmbeddings.append(vector)
            word2Idx[split[0]] = len(word2Idx)
            
    wordEmbeddings = np.array(wordEmbeddings)

    char2Idx = {"PADDING":0, "UNKNOWN":1}
    for c in " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,-_()[]{}!?:;#'\"/\\%$`&=*+@^~|":
        char2Idx[c] = len(char2Idx)

    train_set = padding(createMatrices(trainSentences,word2Idx,  label2Idx, case2Idx,char2Idx))
    dev_set = padding(createMatrices(devSentences,word2Idx, label2Idx, case2Idx,char2Idx))
    test_set = padding(createMatrices(testSentences, word2Idx, label2Idx, case2Idx,char2Idx))

    idx2Label = {v: k for k, v in label2Idx.items()}
    np.save("models/idx2Label.npy",idx2Label)
    np.save("models/word2Idx.npy",word2Idx)

    train_batch,train_batch_len = createBatches(train_set)
    dev_batch,dev_batch_len = createBatches(dev_set)
    test_batch,test_batch_len = createBatches(test_set)


    words_input = Input(shape=(None,),dtype='int32',name='words_input')
    words = Embedding(input_dim=wordEmbeddings.shape[0], output_dim=wordEmbeddings.shape[1],  weights=[wordEmbeddings], trainable=False)(words_input)
    casing_input = Input(shape=(None,), dtype='int32', name='casing_input')
    casing = Embedding(output_dim=caseEmbeddings.shape[1], input_dim=caseEmbeddings.shape[0], weights=[caseEmbeddings], trainable=False)(casing_input)
    character_input=Input(shape=(None,52,),name='char_input')
    embed_char_out=TimeDistributed(Embedding(len(char2Idx),30,embeddings_initializer=RandomUniform(minval=-0.5, maxval=0.5)), name='char_embedding')(character_input)
    dropout= Dropout(0.5)(embed_char_out)
    conv1d_out= TimeDistributed(Conv1D(kernel_size=3, filters=30, padding='same',activation='tanh', strides=1))(dropout)
    maxpool_out=TimeDistributed(MaxPooling1D(52))(conv1d_out)
    char = TimeDistributed(Flatten())(maxpool_out)
    char = Dropout(0.5)(char)
    output = concatenate([words, casing,char])
    output = Bidirectional(LSTM(200, return_sequences=True, dropout=0.50, recurrent_dropout=0.25))(output)
    output = TimeDistributed(Dense(len(label2Idx), activation='softmax'))(output)
    model = Model(inputs=[words_input, casing_input,character_input], outputs=[output])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='nadam')
    model.summary()
    # plot_model(model, to_file='model.png')


    for epoch in range(epochs):    
        print("Epoch %d/%d"%(epoch,epochs))
        a = Progbar(len(train_batch_len))
        for i,batch in enumerate(iterate_minibatches(train_batch,train_batch_len)):
            labels, tokens, casing,char = batch       
            model.train_on_batch([tokens, casing,char], labels)
            a.update(i)
        a.update(i+1)
        print(' ')

    model.save("models/model.h5")

    #   Performance on dev dataset        
    predLabels, correctLabels = tag_dataset(dev_batch)        
    pre_dev, rec_dev, f1_dev = compute_f1(predLabels, correctLabels, idx2Label)
    print("Dev-Data: Prec: %.3f, Rec: %.3f, F1: %.3f" % (pre_dev, rec_dev, f1_dev))
        
    #   Performance on test dataset       
    predLabels, correctLabels = tag_dataset(test_batch)        
    pre_test, rec_test, f1_test= compute_f1(predLabels, correctLabels, idx2Label)
    print("Test-Data: Prec: %.3f, Rec: %.3f, F1: %.3f" % (pre_test, rec_test, f1_test))

##
def CNN():

    self.char_domain_size = char_domain_size
    self.embedding_size = char_embedding_dim
    self.hidden_dim = hidden_dim
    self.filter_width = filter_width

    # char embedding input
    self.input_chars = tf.placeholder(tf.int64, [None, None], name="input_chars")

    # padding mask
    # self.input_mask = tf.placeholder(tf.float32, [None, None], name="input_mask")

    self.batch_size = tf.placeholder(tf.int32, None, name="batch_size")

    self.max_seq_len = tf.placeholder(tf.int32, None, name="max_seq_len")

    self.max_tok_len = tf.placeholder(tf.int32, None, name="max_tok_len")

    self.input_dropout_keep_prob = tf.placeholder_with_default(1.0, [], name="input_dropout_keep_prob")

    # sequence lengths
    self.sequence_lengths = tf.placeholder(tf.int32, [None, None], name="sequence_lengths")
    self.token_lengths = tf.placeholder(tf.int32, [None, None], name="tok_lengths")

    print("CNN char embedding model:")
    print("embedding dim: ", self.embedding_size)
    print("out dim: ", self.hidden_dim)

    char_embeddings_shape = (self.char_domain_size-1, self.embedding_size)
    self.char_embeddings = tf_utils.initialize_embeddings(char_embeddings_shape, name="char_embeddings", pretrained=embeddings)

    self.outputs = self.forward(self.input_chars, self.input_dropout_keep_prob, reuse=False)

    def forward(self, input_x1, input_dropout_keep_prob, reuse=True):
        with tf.variable_scope("char-forward", reuse=reuse):

            char_embeddings_lookup = tf.nn.embedding_lookup(self.char_embeddings, input_x1)
            print(char_embeddings_lookup.get_shape())

            char_embeddings_flat = tf.reshape(char_embeddings_lookup, tf.stack([self.batch_size*self.max_seq_len, self.max_tok_len, self.embedding_size]))
            print(char_embeddings_flat.get_shape())
            tok_lens_flat = tf.reshape(self.token_lengths, [self.batch_size*self.max_seq_len])
            print(tok_lens_flat.get_shape())

            input_feats_expanded = tf.expand_dims(char_embeddings_flat, 1)
            input_feats_expanded_drop = tf.nn.dropout(input_feats_expanded, input_dropout_keep_prob)


            with tf.name_scope("char-cnn"):
                filter_shape = [1, self.filter_width, self.embedding_size, self.hidden_dim]
                w = tf_utils.initialize_weights(filter_shape, "conv0_w", init_type='xavier',  gain='relu')
                b = tf.get_variable("conv0_b", initializer=tf.constant(0.01, shape=[self.hidden_dim]))
                conv0 = tf.nn.conv2d(input_feats_expanded_drop, w, strides=[1, 1, 1, 1], padding="SAME", name="conv0")
                print("conv0", conv0.get_shape())
                h_squeeze = tf.squeeze(conv0, [1])
                print("squeeze", h_squeeze.get_shape())
                hidden_outputs = tf.reduce_max(h_squeeze, 1)
                print("max", hidden_outputs.get_shape())
                hidden_outputs_unflat = tf.reshape(hidden_outputs, tf.stack([self.batch_size, self.max_seq_len, self.hidden_dim]))

        return hidden_outputs_unflat

#####################
@app.route('/classify', methods=['GET', 'POST'])
def classify():
    # Prepare your file
    parent_dir: str = os.path.join('/kaggle', 'input', 'twitter-bots-accounts')
    dataset_name: str = "twitter_human_bots_dataset.csv"
    dataset_path: str = os.path.join(parent_dir, dataset_name)  
    print(f"Dataset directory: {dataset_path}")

    # Generate a Pandas DataFrame
    dataset_path="twitter_human_bots_dataset.csv"
    twitter_accounts_df: pd.DataFrame = pd.read_csv(dataset_path, index_col=0)
    print(f"Dataset shape {twitter_accounts_df.shape}")

  
    # Preprocess boolean columns
    boolean_cols: list = ["default_profile", "default_profile_image",
                      "geo_enabled", "verified"]
    twitter_accounts_df = convert_bool_to_int(data=twitter_accounts_df, boolean_cols=boolean_cols)
    twitter_accounts_df.head()
    

    twitter_accounts_df["popularity"] = twitter_accounts_df.apply(compute_popularity_metric, axis=1)
    ##############
    
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['figure.figsize'] = 12, 8
    mpl.rcParams['font.sans-serif'] = ['Tahoma']
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    # Set up some parameters for EDA
    palette: str = "husl"
    grouped: str = "account_type"
    default_value: str = "unknown"
    def get_labels_colors_from_pandas_column(df: pd.DataFrame, column: str, palette: str):
        data_labels: dict = dict()
        try:
            labels: list = df[column].unique().tolist()
            colors: list = sns.color_palette(palette, len(labels))
            data_labels: dict = dict(zip(labels, colors))
        except Exception as e:
            logger.error(e)
        return data_labels

    # Retrieve labels and additional parameters to plot figures
    data_labels: dict = get_labels_colors_from_pandas_column(
        df=twitter_accounts_df, column=grouped, palette=palette)
    # Show labels
    print(f"Unique Target values: {data_labels.keys()}")
    # Functions to plot data distributions
    def plot_multiple_histograms(data: pd.DataFrame,
                                 grouped_col: str,
                                 target_col: str,
                                 data_labels: dict):
        # Plot
        plt.figure(figsize=(12, 10))
        title = "\n"
        labels: list = list(data_labels.keys())
        for j, i in enumerate(labels):
            x = data.loc[data[grouped_col] == i, target_col]
            mu_x = round(float(np.mean(x)), 3)
            sigma_x = round(float(np.std(x)), 3)
            ax = sns.distplot(x, color=data_labels.get(i), label=i, hist_kws=dict(alpha=.1),
                              kde_kws={'linewidth': 2})
            ax.axvline(mu_x, color=data_labels.get(i), linestyle='--')
            ax.set(xlabel=f"{target_col.title()}", ylabel='Density')
            title += f"Parameters {str(i)}: $G(\mu=$ {mu_x}, $\sigma=$ {sigma_x} \n"
            ax.set_title(title)
        plt.legend(title="Account Type")
        plt.grid()
        plt.savefig('static/chart/chart5.png')
        plt.tight_layout()
        #plt.show()

    def plot_multiple_boxplots(data: pd.DataFrame, grouped_col: str, target_col: str,
                               palette: str = "husl"):
        plt.figure(figsize=(12, 10))

        means: dict = data.groupby([grouped_col])[target_col].mean().to_dict(OrderedDict)
        counter: int = 0

        bp = sns.boxplot(x=grouped_col, y=target_col, data=data, palette=palette, order=list(means.keys()))
        bp.set(xlabel='', ylabel=f"{target_col.title()}")
        ax = bp.axes

        for k, v in means.items():
            # every 4th line at the interval of 6 is median line
            # 0 -> p25 1 -> p75 2 -> lower whisker 3 -> upper whisker 4 -> p50 5 -> upper extreme value
            mean = round(v, 2)
            ax.text(
                counter,
                mean,
                f'{mean}',
                ha='center',
                va='center',
                fontweight='bold',
                size=10,
                color='white',
                bbox=dict(facecolor='#445A64'))
            counter += 1
        bp.figure.tight_layout()
        plt.savefig('static/chart/chart6.jpg')
        plt.grid()
        #plt.show()
    
    target: str = "statuses_count"  
    # Extract histograms
    plot_multiple_histograms(data=twitter_accounts_df, 
                             grouped_col=grouped,
                             data_labels=data_labels,
                             target_col=target)
    # Extract Box-plots
    plot_multiple_boxplots(data=twitter_accounts_df,
                           grouped_col=grouped,
                           target_col=target,
                           palette=palette)
    #print(data1)
    data=[]
    j=0

    # Preprocess Response variable (account type)
    twitter_accounts_df[grouped] = twitter_accounts_df[grouped].astype('category')
    
    data=twitter_accounts_df.dtypes
    #print(data[0])
    
    twitter_accounts_df[grouped] = twitter_accounts_df[grouped].cat.codes
    data1=twitter_accounts_df.head()
    #data1=twitter_accounts_df[grouped]
    #print(len(data1))

    #print(data1)
    
    data2=[]
    j=0
    rows=len(data1.values)
    for ds in data1.values:
        
        
        dd1=[]
        i=0
        while i<20:
            
            dd1.append(ds[i])
            i+=1
        data2.append(dd1)
        
    cols=i
    #####################33

    twitter_accounts_df_num: pd.DataFrame = twitter_accounts_df.copy()
    twitter_accounts_df_num: pd.DataFrame = twitter_accounts_df_num._get_numeric_data()
    data3=twitter_accounts_df_num.head()
    
    data4=[]
    j=0
    rows=len(data1.values)
    for ds3 in data3.values:
        
        
        dd3=[]
        i=0
        while i<13:
            
            dd3.append(ds3[i])
            i+=1
        data4.append(dd3)
        
    cols=i
    ##################
    # Remove columns
    drop_cols: list = ["id"]
    twitter_accounts_df_num.drop(drop_cols, axis=1,inplace=True)
    data5=twitter_accounts_df_num.head()
    data6=[]
    j=0
    rows=len(data5.values)
    for ds5 in data5.values:
        
        
        dd5=[]
        i=0
        while i<12:
            
            dd5.append(ds5[i])
            i+=1
        data6.append(dd5)
        
    cols=i
    ##################
    

    return render_template('classify.html',data2=data2,data4=data4,data6=data6)

##########################







@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)


