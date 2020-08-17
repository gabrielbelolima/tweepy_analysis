# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 16:12:15 2020

@author: gabrielbelolima
"""
import pandas as pd
import time
#from tqdm import tqdm
#from tqdm.notebook import tqdm
from IPython.display import clear_output

import matplotlib.pyplot as plt

import tweepy
#from auth import auth
from grabel_auth import auth

tt = auth()

# Count down
def count_down(tempo):
    
    while tempo:
        mins, secs = divmod(tempo, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        clear_output()
        print(timeformat, end='\r')
        time.sleep(1)
        tempo -= 1
        

        
# get_followers_id()
def get_followers_ids(perfil_analisado):
    '''Recebe um nome de perfil do twitter e retorna serie com ids dos seguidores'''
    ids = []
    my_pages = tweepy.Cursor(tt.followers_ids, screen_name=perfil_analisado).pages()
    while True:
        try:
            page = my_pages.next()
            ids.extend(page)
            time.sleep(2)
        except tweepy.TweepError:
                tempo = (60 * 15) #15 min
                time.sleep(tempo)
                count_down(tempo) #não está printando a contagem regressiva!
                continue
        except StopIteration:
            break
  
    return pd.DataFrame(ids, columns=['followers_ids'])['followers_ids']
  

# get_users_data()
def get_users_data(lista_ids):
    '''Recebe lista ou serie de ids e retorna nomes de perfis do twitter'''
    from tqdm import tqdm
    
    followers = pd.DataFrame()
    while len(lista_ids)>len(followers):
        try:
            for tt_id in tqdm(lista_ids):
                df = pd.DataFrame(tt.get_user(tt_id)._json)
                df = df.loc[['description'],['id_str','name','screen_name','profile_image_url_https',
                                             'description','statuses_count','friends_count','followers_count',
                                             'favourites_count','location','created_at','protected','lang']].rename(
                                                                                    columns={
                                                                                              'statuses_count':'tweets_count',
                                                                                              'id_str':'profile_id'
                                                                                              })
                followers = pd.concat([followers, df], axis = 0, ignore_index=True)  
                time.sleep(.5)
                
        except tweepy.TweepError:
                tempo = (60 * 15) #15 min
                time.sleep(tempo)
                count_down(tempo)
                continue
        except StopIteration:
            break
        
    return followers


# get_followers_data()
def get_followers_data(perfil_analisado):
    '''Recebe perfil e retorna dataframe com dados das páginas dos seguidores'''
    df_fol = get_followers_ids(perfil_analisado)
    return get_users_data(df_fol)


# get_seguidores_iguais()
def get_seguidores_iguais(*tt_users):
    '''Recebe nomes de perfis do twitter e retorna serie com seguidores em comum.'''
    
    #from IPython.display import clear_output
    tt_users = list(tt_users) 
    print('Perfis a filtrar:', len(tt_users))
    if len(tt_users)>=2:
                    
        fols_user1 = get_followers_ids(tt_users.pop(0))
        
        clear_output(wait=True)
        print('Perfis a filtrar:', len(tt_users))
        fols_user2 = get_followers_ids(tt_users.pop(0))
        df_both = pd.merge(fols_user2, fols_user1, how = 'inner', on='followers_ids')
        
        while len(tt_users)>=1:
            
            clear_output(wait=True)
            print('Perfis a filtrar:', len(tt_users))
            
            fols_userx = get_followers_ids(tt_users.pop(0))
            df_both = pd.merge(df_both, fols_userx, how='inner', on ='followers_ids')
           
        clear_output(wait=True)
        print('Seguidores em comum: ', len(df_both))
        
    return get_users_data(df_both['followers_ids'])


# plot_tt_top()
def plot_tt_top(df = [], top=10, table = False):
        
    l = 25
    h = min(top*2.2, 150)
    cols = {'flls':'followers_count',
            'frds':'friends_count',
            'twts':'tweets_count',
            'favs':'favourites_count'}
    
    ind = "?"
    while ind not in cols.keys():
        ind = input('''Digite um dos valores para organizar o plot:
                       flls : número de seguidores;
                       frds : número de amigos;
                       twts : número de tweets;
                       favs : número de favoritagens.\n''')
        if ind not in cols.keys():
            print('Valor não aceito!\n')
    
    param = cols.get(ind)
    
    df_plot = df.set_index('screen_name').nlargest(top, param)
    df_plot.sort_values(param)[cols.values()].plot(kind='barh', 
                                                   figsize=[l, h], 
                                                   #width = .8,
                                                   grid = True
                                                    )
    if table:
            return df_plot[cols.values()].style.background_gradient(cmap='Greens')
            
    plt.title('Top {} por {}'.format(top, param))    
    plt.ylabel('')
    plt.show()

