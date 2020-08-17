from auth import auth
from main_func import get_users_data, get_followers_data, get_seguidores_iguais, plot_tt_top

tt = auth

same_fol = get_seguidores_iguais('profile_1','profile_2')
print(same_fol)

#plot_tt_top(same_fol)
