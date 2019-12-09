import pickle
import os


def get_data(game, custom=False):

    game_data = None
    content_data = None

    if custom:
        gdn = os.path.join('custom_data','game_data_' + game)
        cdn =  os.path.join('custom_data','content_data_' + game)
    else:
        gdn = os.path.join('pre_data','game_data_' + game)
        cdn =  os.path.join('pre_data','content_data_' + game)
    with open(gdn, 'rb') as fp:
        game_data = pickle.load(fp)
    with open(cdn, 'rb') as fp:
        content_data = pickle.load(fp)
        
    return {'game_data': game_data, 'content_data': content_data}
