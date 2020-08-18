def auth():
    '''Cria o objeto tt com a autenticação de DevTwitter''' 
    import tweepy
 
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(KEY, SECRET)
    global tt
    tt = tweepy.API(auth, wait_on_rate_limit=True)
    return tt


def teste():
	print('funcao ok!')

