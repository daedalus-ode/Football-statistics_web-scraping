from tkinter import *
from PIL import ImageTk,Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter.filedialog import askopenfile
from tkvideo import tkvideo
import requests
from bs4 import BeautifulSoup
import os
import random

######basic setup for gui and variables
base=Tk()
base.title('Statistics')
choice=IntVar()
playerchoice=IntVar()
tchoice=IntVar()
clicked=StringVar()
clicked1=StringVar()
clicked2=StringVar()
ok=0
ko=0
p=''
sns.set_style("darkgrid") 
plt.rcParams['font.size']=8
plt.rcParams['font.family']='fantasy '
fig ,axes=plt.subplots(2,2,figsize=(20,20))
Fcsv=0
bro=0

if(os.system("ping -n 1 " + 'fbref.com')==0):
    data = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats')
    soup = BeautifulSoup(data.text,'lxml')
    standings_table = soup.select('table.stats_table')[0]
    links = standings_table.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]
    p_urls=[]

    ####### start of graphs
    def pchoicee(a,k):
        ko=playerchoice.get()
        p_dta = requests.get(k[ko])
        bro=k[ko]
        p_stats = pd.read_html(p_dta.text, match = 'Standard Stats')[0]
        p_stats.columns = p_stats.columns.droplevel()
        p_stats = p_stats.dropna(subset = ['Season'])
        p_stats = p_stats[p_stats['Season'].str.match('20...20..')]
        p_stats=p_stats.fillna(0)
        p_stats = p_stats.T.drop_duplicates().T
        Final=Button(base,text='Are you reallly sure',command=lambda:writer(p_stats,bro))
        Final.grid(row=0,column=9)
    def caller(p):
        if clicked2.get() == 'Player':
            graph_player(p)
        if clicked2.get()=='Keeper':
            graph_keeper(p)
    def writer(p_stats,name):
        framelas=LabelFrame(base)
        framelas.grid(row=0,column=9)
        rname= random.random()
        rrname=str(rname)
        rrrname=rrname+'.csv'
        p_stats.to_csv(rrrname)
        Fcsv=pd.read_csv(rrrname)
        H=Label(framelas,text='Is it a Player or a Keeper')
        H.grid(row=0,column=0)
        drop=OptionMenu(base,clicked2,"Player","Keeper")
        drop.grid(row=0,column=10)   
        perma=Button(base,text='Confirm',command=lambda:caller(Fcsv))
        perma.grid(row=0,column=11)
    def tchoicee():
        ok=tchoice.get()
        frame2=LabelFrame(base)
        frame2.grid(row=0,column=3)
        team_dta = requests.get(team_urls[ok])
        soup = BeautifulSoup(team_dta.text,'lxml')
        standings_table = soup.select('table.stats_table')[0]
        p_links = standings_table.find_all('a')
        p_links = [l.get("href") for l in p_links]
        p_links = [l for l in p_links if '/en/players/' in l and 'Match-Logs' not in l]
        p_urls = [f"https://fbref.com{l}" for l in p_links]
        x=list([i[i.rfind('/')+1:] for i in p_urls]) 
        a=0
        b=1
        c=0
        for i in x:
            h=Radiobutton(frame2,text=i,variable=playerchoice,value=a)
            h.grid(row=b,column=1)
            a=a+1
            b=b+1          
        Newb=Button(frame2,text='Confirm',command=lambda:pchoicee(x,p_urls))
        Newb.grid(row=0,column=1)
    def callert(p):
        graph_team(p)
    def writert(t_stats):
        framelas=LabelFrame(base)
        framelas.grid(row=0,column=9)
        rname= random.random()
        rrname=str(rname)
        rrrname=rrname+'.csv'
        t_stats.to_csv(rrrname)
        Fcsv=pd.read_csv(rrrname)   
        perma=Button(base,text='Confirm',command=lambda:callert(Fcsv))
        perma.grid(row=0,column=11)    
    def teamchoice():
        ok=tchoice.get()
        frame2=LabelFrame(base)
        frame2.grid(row=0,column=3)
        team_dta = requests.get(team_urls[ok])
        t_stats = pd.read_html(team_dta.text, match = 'Standard Stats')[0]
        t_stats.columns = t_stats.columns.droplevel()
        t_stats = t_stats.dropna(subset = ['Nation']) 
        t_stats['Age'] = [i[:2] for i in t_stats['Age']]
        t_stats=t_stats.fillna(0)
        t_stats = t_stats.T.drop_duplicates().T
        Final=Button(base,text='Are you reallly sure',command=lambda:writert(t_stats))
        Final.grid(row=0,column=9)
    def graph_player(h):
        ###############
        player=h
        ##### Video stuff starts
        frame5=LabelFrame(base)
        frame5.grid(row=0,column=7)
        sns.lineplot(data=player,x=player.Season,y=player.Min,marker='h',alpha=0.6)
        ###############
        sns.barplot(data=player,x=player.Gls,y=player.Season,alpha=0.8,ax=axes[0,0])
        sns.barplot(data=player,x=player.xG,y=player.Season,alpha=0.8,ax=axes[0,0])
        ###############
        sns.barplot(data=player,x=player.MP,y=player.Starts,alpha=0.9,ax=axes[0,1])
        axes[0,1].set_xlabel('Matches played')
        axes[0,1].set_ylabel('Starts')
        axes[0,1].set_title("Bar graph")
        ###############
        axes[1,0].plot(player.Gls,player.Season,marker='h')
        axes[1,0].plot(player.Ast,player.Season,marker='s')
        axes[1,0].legend(['Goals','Assists'])
        #################
        plt.xticks(rotation=90)
        plt.show()
    def graph_keeper(h):
        player=h
        frame1=LabelFrame(base)
        frame1.grid(row=12,column=0)
        sns.lineplot(data=player,x=player.Season,y=player.Min,marker='h',alpha=0.6)
        sns.barplot(data=player,x=player.Season,y=player['MP'],alpha=0.6,ax=axes[1,0])
        plt.legend(['Minutes','Matches Played'])
        plt.xticks(rotation=90)
        ###########################
        sns.barplot(data=player,x=player.Age,y=player.Min,alpha=0.8,ax=axes[0,0])
        #############################
        axes[0,1].plot(player.Season,player['90s'],marker='h')
        axes[0,1].set_xlabel("Seasons")
        axes[0,1].legend(["SoTA","Saves"])
        ################################
        plt.show()
    def graph_team(h):
        player=h
        ######################
        sns.barplot(data=player,x=player.Gls,y=player.Player,alpha=0.8,ax=axes[1,0])
        plt.xticks(rotation=270)
        ######################
        sns.barplot(data=player,x=player.Starts,y=player.Player,alpha=0.9,ax=axes[0,0])
        #######################
        sns.lineplot(data=player,x=player.Ast,y=player.Player,marker='h',alpha=0.6,ax=axes[0,1])
        ######################
        plt.hist(player.Age,alpha=0.6)
        plt.title("Age of the squad")
        plt.show()
##### back to tkinter
    def win(c):
        if c==1:
            ##############
            frame1=LabelFrame(base,text='Time to pick')
            frame1.grid(row=0,column=2,padx=25,pady=25)
            x=list([i[i.rfind('/')+1:] for i in team_urls])
            a=0
            b=1
            c=0
            for i in x:
                h=Radiobutton(frame1,text=i,variable=tchoice,value=a)
                h.grid(row=b,column=0)
                a=a+1
                b=b+1
            ra=Button(frame1,text='Confirm',command=tchoicee)
            ra.grid(row=a+1,column=0)

        if c==2:
            frame1=LabelFrame(base,text='Time to pick')
            frame1.grid(row=0,column=2,padx=25,pady=25)
            x=list([i[i.rfind('/')+1:] for i in team_urls])
            a=0
            b=1
            c=0
            for i in x:
                h=Radiobutton(frame1,text=i,variable=tchoice,value=a)
                h.grid(row=b,column=0)
                a=a+1
                b=b+1
            ra=Button(frame1,text='Confirm',command=tchoicee)
            ra.grid(row=a+1,column=0)   
        if c==3:
            frame1=LabelFrame(base,text='Time to pick')
            frame1.grid(row=0,column=2,padx=25,pady=25)
            frame1=LabelFrame(base,text='Time to pick')
            frame1.grid(row=0,column=2,padx=25,pady=25)
            x=list([i[i.rfind('/')+1:] for i in team_urls])
            a=0
            b=1
            c=0
            for i in x:
                h=Radiobutton(frame1,text=i,variable=tchoice,value=a)
                h.grid(row=b,column=0)
                a=a+1
                b=b+1
            ra=Button(frame1,text='Confirm',command=teamchoice)
            ra.grid(row=a+1,column=0)
    def rad():
        Radiobutton(frame,text='Player',variable=choice,value=1).grid(row=6,column=5)
        Radiobutton(frame,text='Keeper',variable=choice,value=2).grid(row=7,column=5)
        Radiobutton(frame,text='Team',variable=choice,value=3).grid(row=8,column=5)
        b1=Button(frame,text='Make your choice',command=lambda: win(choice.get()))
        b1.grid(row=11,column=5)

else:
    def gp(player):
    
        if clicked1.get() == "Best Goal":
            top=Toplevel()
            my_label = Label(top)
            my_label.grid(row=0,column=0)
            pa=clicked.get()+".mp4"
            player = tkvideo(pa, my_label, loop = 1, size = (1280,720))
            player.play()
        ### video stuff ends
        if clicked1.get() == "Graphs":
            sns.lineplot(data=player,x=player.Season,y=player.Minutes,marker='h',alpha=0.6)
            ###############
            sns.barplot(data=player,x=player.Gls,y=player.Season,alpha=0.8,ax=axes[0,0])
            sns.barplot(data=player,x=player.xG,y=player.Season,alpha=0.8,ax=axes[0,0])
        ###############
            sns.barplot(data=player,x=player.MP,y=player.Starts,alpha=0.9,ax=axes[0,1])
            axes[0,1].set_xlabel('Matches played')
            axes[0,1].set_ylabel('Starts')
            axes[0,1].set_title("Bar graph")
            ###############
            axes[1,0].plot(player.Gls,player.Season,marker='h')
            axes[1,0].plot(player.Ast,player.Season,marker='s')
            axes[1,0].legend(['Goals','Assists'])
            #################
            plt.xticks(rotation=90)
            plt.show()
    def graph_player(p):
        ###############
        player=pd.read_csv(p)
        ##### Video stuff starts
        frame5=LabelFrame(base)
        frame5.grid(row=0,column=7)
        Infa=Label(frame5,text='Pick graphs or best goal')
        Infa.grid(row=0,column=0)
        dropp=OptionMenu(frame5,clicked1,"Graphs","Best Goal")
        dropp.grid(row=1,column=0)
        qw=Button(frame5,text='Confirm',command=lambda:gp(player))
        qw.grid(row=2,column=0)
    def se(x):
        p=clicked.get()+'.csv'
        x(p)
    def gk(player):
        if clicked1.get() == "Best Save":
            top=Toplevel()
            my_label = Label(top)
            my_label.grid(row=0,column=0)
            pa=clicked.get()+".mp4"
            player = tkvideo(pa, my_label, loop = 10, size = (1280,720))
            player.play()
        if clicked1.get() == "Graphs":
            #########################
            sns.lineplot(data=player,x=player.Season,y=player.GA,marker='h',alpha=0.6)
            sns.lineplot(data=player,x=player.Season,y=player.MP,marker='h',alpha=0.6)
            plt.legend(['Goals Against','Matche Played'])
            plt.xticks(rotation=90)
            ###########################
            sns.barplot(data=player,x=player.Savep,y=player.Season,alpha=0.8,ax=axes[0,0])
        #############################
            axes[0,1].plot(player.Season,player.SoTA,marker='h')
            axes[0,1].plot(player.Season,player.Saves,marker='h')
            axes[0,1].set_xlabel("Seasons")
            axes[0,1].set_ylabel("Shots on target against and saves")
            axes[0,1].legend(["SoTA","Saves"])
            ################################
            sns.barplot(data=player,x=player.Season,y=player.CSp,alpha=0.8,ax=axes[1,0])
            plt.show()
    def graph_keeper(p):
        player=pd.read_csv(p)
        frame1=LabelFrame(base)
        frame1.grid(row=12,column=0)
        dropp=OptionMenu(frame1,clicked1,"Graphs","Best Save")
        dropp.grid(row=5,column=95)
        bp=Button(frame1,text='Confirm',command=lambda:gk(player))
        bp.grid(row=6,column=95)
    def gt(player):
        if clicked1.get()=="Graphs":
            sns.barplot(data=player,x=player.Glss,y=player.Player,alpha=0.8,ax=axes[1,0])
            plt.xticks(rotation=270)
        ######################
            sns.barplot(data=player,x=player.Starts,y=player.Player,alpha=0.9,ax=axes[0,0])
        #######################
            sns.lineplot(data=player,x=player.Asts,y=player.Player,marker='h',alpha=0.6,ax=axes[0,1])
        ######################
            plt.hist(player.Age,alpha=0.6)
            plt.title("Age of the squad")
            plt.show()
        if clicked1.get()=="Best Moment from the season":
            top=Toplevel()
            my_label = Label(top)
            my_label.grid(row=0,column=0)
            pa=clicked.get()+".mp4"
            player = tkvideo(pa, my_label, loop = 10, size = (1280,720))
            player.play()
    def graph_team(p):
        player=pd.read_csv(p)
        frame1=LabelFrame(base)
        frame1.grid(row=12,column=0)
        dropp=OptionMenu(frame1,clicked1,"Graphs","Best moment from the season")
        dropp.grid(row=5,column=95)
        bp=Button(frame1,text='Confirm',command=lambda:gt(player))
        bp.grid(row=6,column=95)

        ######################
        ##### back to tkinter
    def win(c):
        if c==1:
            ##############
            frame1=LabelFrame(base,text='Time to pick')
            frame1.grid(row=0,column=2,padx=25,pady=25)
            Pname=Label(frame1,text='Pick a Given Player from the Drop Down Menu')
            Pname.grid(row=1,column=95)
            drop=OptionMenu(frame1,clicked,"Messi","Ronaldo","Neymar","Salah","Aguero","Suarez","Rooney","Saka")
            drop.grid(row=2,column=95)
            perma=Button(frame1,text='Confirm',command=lambda:se(graph_player))
            perma.grid(row=3,column=95)
            ###################3.
            frameinfo=LabelFrame(frame1,text="Information")
            frameinfo.grid(row=0,column=0)
            FiG=Label(frameinfo,text="The first graph is one that represents the minutes a plyer has played across the seasons")
            FiG.grid(row=10,column=0)
            SecG=Label(frameinfo,text="The second graph is a comparison between the excpected goals and the goals he actually scored")
            SecG.grid(row=15,column=0)
            ThG=Label(frameinfo,text='The third graph compares the matches played and matches started')
            ThG.grid(row=20,column=0)
            FhG=Label(frameinfo,text='The fourth graph represents the goals and assists made by the player')
            FhG.grid(row=25,column=0)
        
    
        if c==2:
            frame1=LabelFrame(base,text='Time to pick')
            frame1.grid(row=0,column=2,padx=25,pady=25)
            Pname=Label(frame1,text='Pick a Given Player from the Drop Down Menu')
            Pname.grid(row=1,column=95)
            drop=OptionMenu(frame1,clicked,"Alison","Ederson","Neuer","De Gea","Ramsdale","Buffon")
            drop.grid(row=2,column=95)
            perma=Button(frame1,text='Confirm',command=lambda:se(graph_keeper))
            perma.grid(row=3,column=95)
            ##################
            frameinfo=LabelFrame(frame1,text="Information")
            frameinfo.grid(row=0,column=0)
            FiG=Label(frameinfo,text="The first graph is one that represents Goals against vs matches played")
            FiG.grid(row=10,column=0)
            SecG=Label(frameinfo,text="The second graph is shows the save percentage across the seasons")
            SecG.grid(row=15,column=0)
            ThG=Label(frameinfo,text='The third graph gives a perspective on how many shots the keeper faced and how many he saved')
            ThG.grid(row=20,column=0)
            FhG=Label(frameinfo,text='The fourth graph represents the clean sheet percentage by the keeper')
            FhG.grid(row=25,column=0)        
        if c==3:
            frame1=LabelFrame(base,text='Time to pick')
            frame1.grid(row=0,column=2,padx=25,pady=25)
            Pname=Label(frame1,text='Pick a Given Player from the Drop Down Menu')
            Pname.grid(row=1,column=95)
            drop=OptionMenu(frame1,clicked,"Liverpool","Manchester City","Barcelona","Real Madrid","Chelsea")
            drop.grid(row=2,column=95)
            perma=Button(frame1,text='Confirm',command=lambda:se(graph_team))
            perma.grid(row=3,column=95)
            ###############
            frameinfo=LabelFrame(frame1,text="Information")
            frameinfo.grid(row=0,column=0)
            FiG=Label(frameinfo,text="The first graph is one that shows all goal scorers of the club in the last season")
            FiG.grid(row=10,column=0)
            SecG=Label(frameinfo,text="The second graph shows the players and the matches started by each one")
            SecG.grid(row=15,column=0)
            ThG=Label(frameinfo,text='The third graph shows a comparision of all assists made by the players')
            ThG.grid(row=20,column=0)
            FhG=Label(frameinfo,text='The fourth graph represents the age distribution of all players.')
            FhG.grid(row=25,column=0)
    def rad():
        Radiobutton(frame,text='Player',variable=choice,value=1).grid(row=6,column=5)
        Radiobutton(frame,text='Keeper',variable=choice,value=2).grid(row=7,column=5)
        Radiobutton(frame,text='Team',variable=choice,value=3).grid(row=8,column=5)
        b1=Button(frame,text='Make your choice',command=lambda: win(choice.get()))
        b1.grid(row=11,column=5)
    
logo=ImageTk.PhotoImage(Image.open('D:\Codes\Logo.png'))
frame=LabelFrame(base,text='Welcome to The Home Of Stats')
frame.grid(row=0,column=0)

b=Button(frame,text="Click here to start the process.",command=rad)
b.grid(row=0,column=5)

img=Label(frame,image=logo)
img.grid(row=5,column=5,padx=20,pady=20)


exitb=Button(frame,text='EXIT',command=base.quit)
exitb.grid(row=20,column=5)    


base.mainloop()

