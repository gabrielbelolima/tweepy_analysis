from auth import auth
from main_func import get_users_data, get_followers_data, get_seguidores_iguais, plot_tt_top
tt = auth


same_fol = get_seguidores_iguais('grabel','angie_marinho')
print(same_fol)

#gera plot dos seguidores em comum
#plot_tt_top(same_fol)


