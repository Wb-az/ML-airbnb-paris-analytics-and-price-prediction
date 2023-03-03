from tqdm import tqdm
import pandas as pd
import numpy as np
import pickle
# from unidecode import unidecode


def clean_bathroom(string):

    string = string.lower().split(' ')
    if '0' in string:
        string = 1
    elif 'half-bath' in string:
        string = 1
    else:
        string = float(string[0])

    return string


def encoded_bathrooms(df, feature):
    """
    :param df: dataframe 
    :param feature: column withb the text to process
    :return: None
    """
    d = {'shared_bathroom': np.zeros(len(feature)), 'private_bathroom': np.zeros(len(feature))}
    for i, text in tqdm(enumerate(feature)):
        if 'shared' in text:
            d['shared_bathroom'][i] = 1
        else:
            d['private_bathroom'][i] = 1
    df['shared_bathroom'] = d['shared_bathroom']
    df['private_bathroom'] = d['private_bathroom']


def decode_unicode(text):
    punctuation = ['-', '?', '"', '—', '[', ']', ')', '(', '.', '/', ':', ';']
    clean_str = []

    decode_str = text.encode('ascii').decode('unicode-escape')

    for am in decode_str.split(','):
        am_ = " ".join(am.split())
        for punc in punctuation:
            am_ = am_.replace(punc, '')
        # am_ = unidecode(am_, errors='ignore')
        clean_str.append(am_.lower())

    return clean_str


def common_amenities(clean_amenities_list, compress=True):
    """
    :param clean_amenities_list:  alist o f list with the most common amenities
    :param compress: boolean to pickle the dataframe
    :return: a dataframe with count of the amenities
    """
    amenities_dict = {}
    for amenities in tqdm(clean_amenities_list):
        for am in amenities:
            if am in amenities_dict.keys():
                amenities_dict[am] += 1
            else:
                amenities_dict[am] = 1
    df = pd.DataFrame.from_dict(amenities_dict, orient='index')
    df.columns = ['frequency']
    df.sort_values(by='frequency', ascending=False, inplace=True)
    if compress:
        df.to_pickle('df_amenities.pkl')
    return df


def air_conditioning(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'air conditioning':
                continue
            elif 'air conditioning' in am:
                amenities_list[i][ii] = 'air conditioning'
            elif 'split type' in am and 'ductless' in am:
                amenities_list[i][ii] = 'air conditioning'
            elif 'window ac' and 'unit'in am:
                amenities_list[i][ii] = 'air conditioning'
                
            
                
                

def balcony(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'balcony':
                continue
            elif 'balcony' in am:
                amenities_list[i][ii] = 'balcony'
                
                
def backyard_or_garden(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if ('garden' in am or 'backyard' in am) and 'view' not in am:
                amenities_list[i][ii] = 'backyard or garden'
                
                
def bathtub(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'bathtub':
                continue
            elif 'bathtub' in am:
                amenities_list[i][ii] = 'bathtub'
                

def bikes(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'bikes':
                continue
            elif 'bikes' in am:
                amenities_list[i][ii] = 'bikes'
                
                
def breakfast(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'breakfast':
                amenities_list[i][ii] = 'complimentary breakfast'
            elif am == 'complimentary breakfast':
                continue
            elif 'breakfast' in am:
                amenities_list[i][ii] = 'breakfast available'


def body_soap(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):

            if 'non' in am and 'body soap' in am:
                amenities_list[i].remove(am)
            elif 'know' in am and 'body soap' in am:
                amenities_list[i].remove(am)
            elif 'desconocida' in am or 'nombreuses' in am or 'no specific' in am:
                amenities_list[i].remove(am)
            elif 'body soap' in am and 'shampo' in am:
                amenities_list[i][ii] = 'body soap'
                amenities_list[i].append('shampoo')
            elif 'body soap' in am:
                amenities_list[i][ii] = 'body soap'
            elif am == 'shower gel':
                if 'body soap' not in am:
                    amenities_list[i][ii] = 'body soap'
                else:
                    amenities_list[i].remove(am)
            elif 'gel douche' in am:
                amenities_list[i][ii] = 'body soap'
                
            

                
def cable(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'cable':
                continue
            elif 'cable' in l and 'cable' in am:
                if 'tv' not in l:
                    amenities_list.append('tv')
                amenities_list[i].remove(am)
            elif 'cable' in am:
                amenities_list[i][ii] = 'cable'
                if 'tv' not in l:
                    amenities_list.append('tv')
                elif 'hdtv' in l:
                    amenities_list[i][ii] = 'tv'
                    

def clothing_storage(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'clothing storage':
                continue
            elif 'clothing storage' in am:
                amenities_list[i][ii] = 'clothing storage'
            elif 'closet' in am or 'dresser' in am or 'wardrobe' in am:
                amenities_list[i][ii] = 'clothing storage'


def coffee_maker(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'coffee maker' in am or 'coffee machine' in am:
                amenities_list[i][ii] = 'coffe_maker'


def conditioner(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'conditioner':
                continue
            elif 'conditioner' in am:
                amenities_list[i][ii] = 'conditioner'


def crib(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'crib' == am:
                continue
            elif 'crib' in am:
                amenities_list[i][ii] = 'crib'


def dining_area(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'dining' in am:
                amenities_list[i][ii] = 'dining area'
                
                
def drop_beach(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'beach' in am:
                amenities_list[i].remove(am)
                
                
def dryer(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'dryer' == am:
                continue
            elif 'dryer' in am and 'hair' not in am:
                amenities_list[i][ii] = 'dryer'
                
                
def fireplace(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'fireplace' in am:
                amenities_list[i][ii] = 'fireplace'
                

def game_console(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'game console':
                continue
            elif 'game_console' in am:
                amenities_list[i][ii] = 'game console'
            elif 'video games' in am:
                amenities_list[i][ii] = 'game console'
            elif 'ps2' in am or 'ps2' in am or 'ps3' in am or 'ps4' in am or 'ps5' in am:
                amenities_list[i][ii] = 'game console'
            elif 'xbox' in am:
                amenities_list[i][ii] = 'game console'
            elif 'video games' in am:
                amenities_list[i][ii] = 'game console'
            elif 'nintendo' in am:
                amenities_list[i][ii] = 'game console'

                
def grill(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'bbq grill':
                continue
            elif 'grill' in am:
                amenities_list[i][ii] = 'bbq grill'
                

def gym(amenities_list):

    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'gym nearby' in am:
                amenities_list[i].remove(am)
            elif 'exercise' in am or 'gym' in am:
                if 'gym or fitness equipment' not in l:
                    amenities_list[i][ii] = 'gym or fitness equipment'
                else:
                    amenities_list[i].remove(am)
            elif 'stationary bike' in am:
                amenities_list[i][ii] = 'gym or fitness equipment'
            elif 'treadmil' in am:
                amenities_list[i][ii] = 'gym or fitness equipment'
            elif  'weights' in am and 'free' in am:
                amenities_list[i][ii] = 'gym or fitness equipment'
            elif 'yoga' in am:
                amenities_list[i][ii] = 'gym or fitness equipment'
                
            
def heating(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'heating' == am:
                continue
            elif 'heating' in am:
                amenities_list[i][ii] = 'heating'
            elif 'heated' == am:
                amenities_list[i][ii] = 'heating'
                    
                                
def high_chair(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'high chair' == am:
                continue
            elif 'high chair' in am:
                amenities_list[i][ii] = 'high chair'
                

def hot_tub(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'hot tub':
                continue
            elif 'hot tub' in am:
                amenities_list[i][ii] = 'hot tub'


def kitchen(cam):
    for i, l in enumerate(cam):
        for ii, am in enumerate(l):
            if am == 'kitchen':
                continue
            elif am == 'kitchenette':
                continue
            elif 'kitchenaid' in am:
                continue
            elif 'kitchen' in am:
                if 'kitchen' not in l:
                    cam[i][ii] = 'kitchen'
                else:
                    cam[i].remove(am)


def oven_microwaves(amenities_list):
    for i, l in enumerate(amenities_list):

        for ii, am in enumerate(l):
            if 'oven' in am and 'micro' in am and ('combo' in am or 'combine' in am):
                amenities_list[i][ii] = 'combine microwave'
            elif 'microwave oven' in am:
                amenities_list[i][ii] = 'microwave'
            elif 'microwave' in am:
                amenities_list[i][ii] = 'microwave'
            elif 'oven' in am and 'micro' in am:
                amenities_list[i][ii] = 'microwave'
            elif 'oven' in am:
                amenities_list[i][ii] = 'oven'


def parking(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            #     text = unidecode(item, errors='replace', replace_str='?')
            if am == 'parking':
                amenities_list[i][ii] = 'free parking'

            elif 'parking' in am and ('paid' in am or 'free' in am
                                      or 'complimentary' in am or 'garage' in am):
                amenities_list[i][ii] = 'free parking'
            elif 'parking' in am: 
                amenities_list[i][ii] = 'pay parking'
            elif 'free' in am and ('carport' in am or 'garage' in am):
                amenities_list[i][ii] = 'free parking'


def pools(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'pool' == am:
                amenities_list[i][ii] = 'private pool'
            elif 'pool' in am and 'private' in am:
                amenities_list[i][ii] = 'private pool'
            elif 'pool' in am and 'shared' in am:
                amenities_list[i][ii] = 'shared pool'
            elif 'pool' in am and not ('table' in am or 'toys' in am
                                       or 'cover' in am or 'view' in am):
                amenities_list[i][ii] = 'private pool'
            elif 'sauna' in am:
                amenities_list[i][ii] = 'sauna'
                

def pool(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'pool' == am:
                continue
            elif 'pool' in am and (am != 'pool table' or am != 'pool view'
                                   or am != 'pool cover'):
                amenities_list[i][ii] = 'pool'
            elif 'olympic' in am:
                amenities_list[i].remove(am)
            elif 'sauna' in am:
                amenities_list[i][ii] = 'sauna'


def fans(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'portable fan' in am or 'ceiling fan' in am:
                amenities_list[i][ii] = 'fan'


def refrigerator(cam):
    for i, l in enumerate(cam):
        for ii, am in enumerate(l):
            if am == 'refrigerator':
                continue
            elif 'refrigerator' in am:
                cam[i][ii] = 'refrigerator'
                

def restaurant(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'restaurant':
                continue
            elif 'restaurant' in am:
                amenities_list[i][ii] = 'restaurant'               
                
                
def security(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'security cameras':
                continue
            elif 'security cameras' in am:
                amenities_list[i][ii] = 'security cameras'

                
def shampoo(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'shampoo':
                continue
            elif 'no specif' in am and 'shampoo' in am:
                amenities_list[i].remove(am)
            elif 'non' in am and 'shampoo' in am:
                amenities_list[i].remove(am)
            elif am == 'no aplica shampo':
                amenities_list[i].remove(am)
            elif 'know' in am and 'shampoo' in am:
                amenities_list[i].remove(am)
            elif 'shampo' in am:
                amenities_list[i][ii] = 'shampoo'


def sound_system(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'sound system' in am:
                amenities_list[i][ii] = 'sound system'
            elif 'sonos' in am:
                amenities_list[i][ii] = 'sound system'
            elif 'music system' in am:
                amenities_list[i][ii] = 'sound system'


def childrens_toys(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if 'toys' in am:
                amenities_list[i][ii] = "children's toys"

                
def stove(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'stove':
                continue
            elif 'stove' in am:
                amenities_list[i][ii] = 'stove'


def streaming_services(amenities_list):

    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'tv':
                continue
            elif am == 'smart tv':
                amenities_list[i][ii] = 'tv'
            elif 'tv' in am and 'with' in am:
                am_ = am.split(' ')
                if 'amazon' in am_:
                    am_ = ' '.join(map(str, am_[-3:]))
                    amenities_list[i][ii] = am_
                elif 'apple' in am_ or 'dvd' in am_ or 'fire' in am or 'hbo' in am:
                    am_ = ' '.join(map(str, am_[-2:]))
                    amenities_list[i][ii] = am_
                else:
                    amenities_list[i][ii] = am_[-1]
                if 'tv' not in l:
                    amenities_list[i].append('tv')
            elif 'tv' in am:
                if 'tv' not in l:
                    amenities_list[i][ii] = 'tv'
                else: 
                    amenities_list[i].remove(am)

                    
def washer(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'washer':
                continue
            elif 'washer' in am and 'dishwasher' not in am:
                amenities_list[i][ii] = 'washer'

                
def toiletries(amenities_list):
    for i, l in enumerate(amenities_list):
        for ii, am in enumerate(l):
            if am == 'toiletries':
                continue
            elif 'toiletries' in am:
                amenities_list[i][ii] = 'toiletries'
                

def wifi(amenities_list):
    for i, l in enumerate(amenities_list):
        if len(l) > 1:
            for ii, am in enumerate(l):
                if am == 'wifi':
                    continue
                elif 'mbps' in am and 'wifi' in l:
                    amenities_list[i].remove(am)
                elif 'mbps' in am:
                    amenities_list[i][ii] = 'wifi'
                elif 'internet' in l and 'wifi' in l:
                    amenities_list[i].remove('internet')
                elif 'wifi' in am:
                    if 'wifi' in l:
                        amenities_list[i].remove(am)
                    else:
                        amenities_list[i][ii] = 'wifi'
        else:
            if 'wifi' in l:
                continue
                
                        
def preprocess_amenities(amenities_list):

    kitchen(amenities_list)
    dining_area(amenities_list)
    refrigerator(amenities_list)
    stove(amenities_list)
    oven_microwaves(amenities_list)
    coffee_maker(amenities_list)
    breakfast(amenities_list)
    heating(amenities_list)
    fans(amenities_list)
    air_conditioning(amenities_list)
    wifi(amenities_list)
    washer(amenities_list)
    dryer(amenities_list)
    bathtub(amenities_list)
    
    # facilities features
    balcony(amenities_list)
    fireplace(amenities_list)
    parking(amenities_list)
    backyard_or_garden(amenities_list)
    restaurant(amenities_list)
    security(amenities_list)

    # Essentials
    body_soap(amenities_list)
    shampoo(amenities_list)
    conditioner(amenities_list)
    clothing_storage(amenities_list)
    toiletries(amenities_list)

    # Children
    crib(amenities_list)
    high_chair(amenities_list)
    childrens_toys(amenities_list)

    # Entertainment
    sound_system(amenities_list)
    game_console(amenities_list)
    streaming_services(amenities_list)
    cable(amenities_list)
    hot_tub(amenities_list)
    pool(amenities_list)
    gym(amenities_list)
    grill(amenities_list)
    drop_beach(amenities_list)
    
    return amenities_list