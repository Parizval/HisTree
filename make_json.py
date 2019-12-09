import pickle
import os
'''
The format for the input is ->
question::chapter::fact::opt1<>explanation1<>next_q1......

'''
def make(game, custom=False):
    if custom:
        path =  os.path.join('custom',game)
    else:
        path =  os.path.join('data',game)
    data = open(path+'.txt').read().split('\n')

    game_data = {}
    content_data = {}
    data_set = {}
    counter = 1

    for i in data:
        tmp = i.split('::')
        tmp = list(map(lambda x: x.strip(), tmp))
        for k in range(len(tmp)):
            if '<>' in tmp[k]:
                tmp[k] = tmp[k].split('<>')
        pp = []
        for k in tmp:
            if isinstance(k, list):
                pp += k[:]
            else:
                pp.append(k)
        tmp = pp[:]
        for j in tmp:
            if j not in data_set:
                data_set[j] = counter
                counter += 1
    content_data = {val: key for key, val in data_set.items()}
    # print(content_data)
    for i in data:
        tmp = i.split('::')
        tmp = list(map(lambda x: x.strip(), tmp))
        if tmp[0] != '':
            q, ch, fct = tmp[:3]
            ops = tmp[3:]
            ops_data = {}
            print(ops)
            for t in ops:
                if '<>' in t:
                    oop, exp, qq = t.split('<>')
                    ops_data[data_set[oop]] = {'next': data_set[qq],
                                            'more': data_set[exp]
                                            }
                else:
                    ops_data[data_set[t]] = 'None'
            game_data[data_set[q]] = {
                'options': ops_data,
                'chapter': data_set[ch],
                'fact': data_set[fct]
            }
    # print(game_data)
    if custom:
        gdn = os.path.join('custom_data','game_data_' + game)
        cdn =  os.path.join('custom_data','content_data_' + game)
    else:
        gdn = os.path.join('pre_data','game_data_' + game)
        cdn =  os.path.join('pre_data','content_data_' + game)
    with open(gdn, 'wb') as ff:
        pickle.dump(game_data, ff)
    with open(cdn, 'wb') as ff:
        pickle.dump(content_data, ff)
    print('Data processed and converted to json.')

if __name__ == "__main__":
    make('ww1_f')
