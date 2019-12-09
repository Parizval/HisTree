import read_data


def play(inp, game, custom=False):
    if custom:
        value = read_data.get_data(game, custom=True)
    else:        
        value = read_data.get_data(game)
    game_data = value['game_data']
    content_data = value['content_data']
    # print(game_data)
    x = game_data[inp]
    opt_val = [content_data[i] for i in x['options']]
    if 'none' in opt_val:
        print(inp, opt_val, x)
        return {'error':content_data[inp]}
    else:
        # print(x)
        # print('Chapter:{}\nFact:{}'.format(
        #     content_data[x['chapter']], x['fact']))
        # ops = x['options']
        # print(ops)
        # print(content_data[inp])
        # for i in ops:
        #     print('----------------\nOption:{}\nNext:{}\nMore:{}'.format(
        #         content_data[i], ops[i]['next'], ops[i]['more']))
        # ret_dct = {
        #     'chapter': x['chapter'],
        #     'fact': x['fact'],
        #     'options':x[options]
        # }
        x['question'] = inp
        return x
    
