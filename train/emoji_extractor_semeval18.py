# -*- coding: utf-8 -*-

'''
---- Emoji extractor-----
Given a file with one tweet per line, return two files: 1)list of texts without emois and 2) list of correct labels for semeval emoji detection 2018

a. first param =  Path to file with tweets (one per line). It can contain the text of the tweets (one per line), or the twitter json(one per line).
                  If it is the twitter json, add the extention .json at the end.
b. second param = "us" or "es" to decide what label mapping to use

Usage example for a file containng the json of american tweets (one per line):
$ python emoji_extractor_semeval18.py tweets_us.json us
'''



import sys
import string
import json
import re
import emojilib #from https://github.com/fvancesco/emoji
import os
from nltk.tokenize import TweetTokenizer

tknz = TweetTokenizer()
delete_hashtags=True

""" argument
arg[0] - path to tweet txt file
arg[1] - 0 for interpunction erasing, 1 otherwise
arg[2] - how many tweets to process
"""
def clean_text(text, argument=1):
    #remove links, anonymize user mentions
    clean = ""

    # uklanjanje linkova i zamjena imena u @user
    text_new = re.sub( '\s+', ' ', text).strip()
    for t in text_new.split(" "):
        if t.startswith('@') and len(t) > 1:
            clean += "@user "
        elif t.startswith('#') and len(t) > 1 and (delete_hashtags or argument==0):
            pass
        elif t.startswith('http'):
            pass
        else:
            clean += t + " "

    # uklanjanje nepotrebnog znaka
    clean = clean.replace(u'&amp;', "&")

    if argument==0:
        clean = clean.encode('utf-8').translate(None, string.punctuation)
        clean = clean.decode('utf-8')
    elif argument==1:
        # uklanjanje repetitivnih interpunkcija
        clean = re.sub(r'([-+\\\\|()[\]{};:,<>/?@#$%^&*_~\'\"!])\1+', r'\1', clean)

        # tokeniziranje
        clean2 = tknz.tokenize(clean)

        # uklanjane hashtagova!
        if delete_hashtags:
            clean = ""
            for c in clean2:
                if c.startswith('#') and len(c) > 1:
                    pass
                else:
                    clean += c + " "
            clean = clean.rstrip()
        else:
            clean = ' '.join(clean2)

        # uklanjanje nepotrebnih interpunkcija koje u tekstu nemaju neku vaznost
        chars = [' # ',' + ',' * ',' _ ']
        for ch in chars:
            clean = clean.replace(ch, " ")

        # tknz.tokenize() rastavlja slozene emojie pa ih treba sastaviti u jedan
        clean = clean.replace("🇺 🇸", "🇺🇸")

    clean = clean.lower()
    return clean

def obrada_pocetnog_teksta(text_p):
    # uklanjanje svih unicode znakova koji nisu brojke, slova, interpunkcije i nasih 20 emojia
    text = re.sub(
        '[^\u0020-\u007E|\u2764|\U0001f60d|\U0001f602|\U0001f495|\U0001f525|\U0001f60a|\U0001f60e|\u2728|\U0001f499|\U0001f618|\U0001f4f7|\u2600|\U0001f49c|\U0001f609|\U0001f4af|\U0001f601|\U0001f384|\U0001f4f80|\U0001f61c|\U0001f1fa\U0001f1f8]', " ", text_p, re.U)

    # uklanjanje repetitivnih emojia + dodatno uklanjanje emojia "🇺🇸"
    text = re.sub(
        "([\u2764|\U0001f60d|\U0001f602|\U0001f495|\U0001f525|\U0001f60a|\U0001f60e|\u2728|\U0001f499|\U0001f618|\U0001f4f7|\u2600|\U0001f49c|\U0001f609|\U0001f4af|\U0001f601|\U0001f384|\U0001f4f80|\U0001f61c])\1+", r'\1', text, flags=re.UNICODE)
    text = re.sub("(\U0001f1fa\U0001f1f8)\1+", r'\1', text, flags=re.UNICODE)

    # stavljanje razmaka između emojia
    text_de = emojilib.demojize(text.decode('utf8'), delimiters = (" ~~", "~~ "))
    text = emojilib.emojize(text_de, delimiters = ("~~", "~~"))

    # trimanje duplih razmaka nakon obrade
    text = " ".join(text.split())
    text += " " # dodavanje razmak na kraju texta da regex moze biti primjenjen i na kraju

    # uklanjanje repetitivnih emojia koji su odvojeni razmakom, npr. "❤ ❤ ❤" u "❤"
    text = re.sub(
        "([\u2764|\U0001f60d|\U0001f602|\U0001f495|\U0001f525|\U0001f60a|\U0001f60e|\u2728|\U0001f499|\U0001f618|\U0001f4f7|\u2600|\U0001f49c|\U0001f609|\U0001f4af|\U0001f601|\U0001f384|\U0001f4f80|\U0001f61c]\s)\1+", r'\1', text, flags=re.UNICODE)
    text = re.sub("(\U0001f1fa\U0001f1f8\s)\1+", r'\1', text, flags=re.UNICODE)
    text = text.rstrip()
    return text


def main():
    path_prefix = "./data/"
    num_suffix = "_" + str(num_of_tweets)
    tweets_file_name = os.path.splitext(os.path.split(tweets_file)[1])[0]
    result_path = path_prefix + tweets_file_name + num_suffix

    out_text = open(result_path + ".text", 'w')
    full_text = open(result_path + ".full", 'w')
    out_loc_labels = open(result_path + ".loclabels", 'w')
    out_emoji_labels = open(result_path + ".emolabels", 'w')
    out_ids = open(result_path + ".ids", 'w')

    ok=0
    tot=0

    with open(tweets_file) as f_in:
        for line in f_in:
            tot+=1
            j = json.loads(line)
            tweet_id = j['id']
            text_poc = j['text'].replace("\n","")

            # PROVJERA
            # - provjera ako text nema niti jedan emoticon -> onda ga preskociti
            emo_list = emojilib.emoji_list(text_poc)
            if not emo_list:
                continue

            # obrada pocetnog teksta
            text = obrada_pocetnog_teksta(text_poc)
            ct = clean_text(text)

            ct = ct.decode('utf-8')
            ct = obrada_pocetnog_teksta(ct)
            ct_tokens = ct.split()

            # PROVJERA
            # - provjera da duljina teksta nije > 30 rijeci
            # - ako su unutar teksta emoji, njih ne uzimamo kao rijec
            if len(ct_tokens)>30:
                ct_tokens_temp = ct_tokens[:31]
                ct_temp = " ".join(ct_tokens_temp)

                emo_list = emojilib.emoji_list(ct_temp)
                ct_length = 30 + len(emo_list)

                ct_tokens = ct_tokens[:ct_length]
                ct = " ".join(ct_tokens)
                #text_t = text.split()
                #text_t = text_t[:30]
                #text = " ".join(text_t)

            # PROVJERA
            # - provjera ako clean text nema niti jedan emoticon -> onda ga preskociti
            emo_list = emojilib.emoji_list(ct)
            if not emo_list:
                continue
            emo_set = [d['code'] for d in emo_list if 'code' in d]

            # PROVJERA
            # - provjera ako su svi emoticoni iz naseg skupa emoticona
            cond = True
            for emos in emo_set:
                emo = emos.encode('utf_8')
                if emo not in mapping:
                    cond = False
                    break
            if not cond:
                continue

            # PROVJERA
            # - provjera da u tekstu nema emoticona koji su jedan iza drugoga
            emo_location = [d['location'] for d in emo_list if 'location' in d]
            second_loc = -1
            cond = True
            for loc in emo_location:
                if second_loc == loc[0] or (second_loc+1 == loc[0] and second_loc!=-1):
                    cond = False
                    break
                second_loc = loc[1]
            if not cond:
                continue

            ok+=1

            # Upis labela u datoteke
            pos = 0
            br_emojies = 0
            position_izlaz = list("0000000000000000000000000000000")
            for tok in ct_tokens:
                pos +=1
                if tok in emo_set:
                    emo = tok.encode('utf_8')
                    out_emoji_labels.write(mapping[emo]+" ")
                    position_izlaz[pos-br_emojies-1]='1'
                    br_emojies +=1
            out_loc_labels.write("".join(position_izlaz)+"\n")
            out_emoji_labels.write("\n")

            # Upis cistog teksta u datoteku
            ct_no_emoji = emojilib.replace_emoji(ct, replacement=' ')
            ct_no_emoji_new = ' '.join(ct_no_emoji.split())
            out_text.write(ct_no_emoji_new+"\n")

            # Upis cijelog teksta sa id-evima
            full_text.write(text+"\n")
            out_ids.write(str(tweet_id)+"\n")

            if ok % 10000==0:
                print(ok)

            if isinstance(num_of_tweets, int) and num_of_tweets > 0 and ok >= num_of_tweets:
                 break



    print(str(ok) + " good examples out of " + str(tot))

    out_text.close()
    out_emoji_labels.close()
    out_loc_labels.close()
    out_ids.close()


if __name__ == '__main__':

    pass

    args = sys.argv[1:]

    if len(args) == 3:
        num_of_tweets = int(args[2])
    else:
        num_of_tweets = "ALL"

    if len(args) == 2 or len(args) == 3:
        tweets_file = args[0]
        lang = args[1]

        if 'us' in lang:
            mapping = { '❤':'0' , '😍':'1' , '😂':'2' , '💕':'3' , '🔥':'4' , '😊':'5' , '😎':'6' , '✨':'7' , '💙':'8' , '😘':'9' , '📷':'10' , '🇺🇸':'11' , '☀':'12' , '💜':'13' , '😉':'14' , '💯':'15' , '😁':'16' , '🎄':'17' , '📸':'18' , '😜':'19'}
            mapping_unicode='\u2764 \U0001f60d \U0001f602 \U0001f495 \U0001f525 \U0001f60a \U0001f60e \u2728 \U0001f499 \U0001f618 \U0001f4f7 \U0001f1fa\U0001f1f8 \u2600 \U0001f49c \U0001f609 \U0001f4af \U0001f601 \U0001f384 \U0001f4f80 \U0001f61c'
        elif 'es' in lang:
            mapping = { '❤':'0' , '😍':'1' , '😂':'2' , '💕':'3' , '😊':'4' , '😘':'5' , '💪':'6' , '😉':'7' , '👌':'8' , '🇪🇸':'9' , '😎':'10' , '💙':'11' , '💜':'12' , '😜':'13' , '💞':'14' , '✨':'15' , '🎶':'16' , '💘':'17' , '😁':'18' , '	':'19'}
        else:
            sys.exit('Need to pass "us" or "es" to decide what labels to use')

        main()

    else:
        sys.exit('''
            Requires:
            - Path to files with tweets (text of the tweets one per line)
            - "us" or "es" to decide the labels to use'
            ''')
