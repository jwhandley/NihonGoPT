from flask import Flask, render_template, request, url_for, flash, session, redirect, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os
import random
from newspaper import Article

app = Flask(__name__)
# this is just here because it is needed to maintain session variables, it doesn't matter
app.secret_key = 'BAD_SECRET_KEY'


with open("APIkey.txt") as f:
    openai.api_key = f.read().strip()

@app.route('/', methods=('GET', 'POST'))

def index():

    if request.method == 'POST':
        if 'content1' in request.form:
            explanation = session['reply1'] + "Here is my attempted translation: " + request.form['content1']
            messages = [
                {"role":"system","content":"I am going to try to figure out what this word or phrase means.  If my description is accurate, say, Yes, that's it!.  Make sure that my definition is correct in the context of the article.  If not, explain briefly what I may have done wrong and state what the phrase or word means in this context. Please explain in English."},
                {"role":"user","content":explanation},
                {"role":"assistant","content":session['text']}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response["choices"][0]["message"]["content"]
            response = jsonify({'reply': reply})
            response.headers['Content-Type'] = 'application/json'
            return response
        
        if 'content2' in request.form:
            explanation = session['reply2'] + "Here is my attempted translation: " + request.form['content2']
            messages = [
                {"role":"system","content":"I am going to try to figure out what this word or phrase means.  If my description is accurate, say, Yes, that's it!.  Make sure that my definition is correct in the context of the article.  If not, explain briefly what I may have done wrong and state what the phrase or word means in this context. Please explain in English."},
                {"role":"user","content":explanation},
                {"role":"assistant","content":session['text']}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response["choices"][0]["message"]["content"]
            response = jsonify({'reply': reply})
            response.headers['Content-Type'] = 'application/json'
            return response 
        
        elif 'content3' in request.form:
            explanation = session['reply3'] + "Here is my attempted translation: " + request.form['content3']
            messages = [
                {"role":"system","content":"I am going to try to figure out what these words or phrases mean.  If my description is accurate, say, Yes, that's it!.  Make sure that my definition is correct in the context of the article.  If not, explain briefly what I may have done wrong and state what the phrase or word means in this context. Please explain in English."},
                {"role":"user","content":explanation},
                {"role":"assistant","content":session['text']}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response["choices"][0]["message"]["content"]
            response = jsonify({'reply': reply})
            response.headers['Content-Type'] = 'application/json'
            return response
        elif 'content4' in request.form:
            explanation = "I am going to try to translate the following sentence: " + session['reply4'][54:] + " Here is my attempted translation: " + request.form['content4']
            messages = [
                {"role":"system","content":"If my translation is perfectly accurate, say, Yes, that's it!.  If there are minor mistakes, say, You almost got it!  Make sure that my translation is correct in the context of the article.  Please misstate any inaccuracies, especially phrases or words I got wrong which might be tricky for a native English speaker to translate correctly.  Remember, you are a Japanese teacher!  Remember, you are only to respond to the translation of the one exact sentence we are discussing.  Do not discuss other text.  Please answer in English."},
                {"role":"user","content":explanation},
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response["choices"][0]["message"]["content"]
            response = jsonify({'reply': reply})
            response.headers['Content-Type'] = 'application/json'
            return response  
        elif 'content5' in request.form:
            explanation = "I am going to try to explain the following grammatical construction: " + session['reply5'] + "Here is my attempted explanation: " + request.form['content5']
            messages = [
                {"role":"system","content":"You are a Japanese teacher using the attached article from Le Monde to try to help a student understand points of grammar.  Please answer in English. The student is attempting to explain the grammatical construct you asked about.  If my description is perfectly accurate, say, Yes, that's it!.  If there are minor mistakes, say, You almost got it!  Make sure that my translation is correct in the context of the article. If I am wrong, be sure to explain clearly and concisely what is mistaken about my interpretation of the grammar.  Remember, you are a Japanese teacher!"},
                {"role":"user","content":explanation},
                {"role":"assistant","content":session['text']}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response["choices"][0]["message"]["content"]
            response = jsonify({'reply': reply})
            response.headers['Content-Type'] = 'application/json'
            return response
        elif 'content6' in request.form:
            explanation = request.form['content6']
            messages = [
                {"role":"system","content":"You are a Japanese teacher using the attached article from Nihon Keizai Shimbun to try to help a student understand Japanese.  The student has asked a question about a particular phrase or sentence or word which he does not understand fully.  Explain in English, given a full translation and pointing out any challenging words, phrases, idioms, or constructions. Please answer in English."},
                {"role":"user","content":explanation},
                {"role":"assistant","content":session['text']}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response["choices"][0]["message"]["content"]
            response = jsonify({'reply': reply})
            response.headers['Content-Type'] = 'application/json'
            return response
        
        elif 'imagedraw' in request.form:
            messages = [
                {"role":"system","content":"Choose a single sentence only and remember, you are a Japanese teacher."},
                {"role":"user","content":"Choose a single sentence from the article that involves a lot of activity, or action, or the kind of thing that could be visualized or drawn."},
                {"role":"assistant","content":session['text']}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response2 = openai.Image.create(
                prompt=response["choices"][0]["message"]["content"],
                n=1,
                size="256x256"
            )
            image_url = response2['data'][0]['url']
            return image_url
    else:
        # Randomly choose one of the sections of the Nikkei
        sections = ['economy','politics','companies','technology','international','society']
        section = random.choice(sections)

        # Load the feed the top 50 articles of that section
        url = f'https://r.nikkei.com/sections/sokuho-{section}?b=DGXZQOJC121UG012032023000000%2C50&v=true'
        response = requests.get(url)
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get the list of articles from the page
        articles = soup.select('article:has(a[href^="/article/"])')
        if not isinstance(articles, list):
            articles = [articles]

        # Choose one of the articles at random
        main_article = random.choice(articles)
        
        # Get the link to the article page
        next_link = main_article.select_one('a[href^="/article/"]')['href']
        
        # Load the article using the newspaper library
        article = Article('https://www.nikkei.com' + next_link)
        article.download()
        article.parse()
        
        # Split the texts by newlines
        paragraph_texts = article.text.split('\n\n')
        # Check if message about sharing the article
        exclude = ['企業での記事共有や会議資料への転載・複製、注文印刷などをご希望の方は、リンク先をご覧ください。',
                   'この記事は会員限定です',
                   '日経電子版をご利用いただき、ありがとうございます。 エキスパートへのメッセージを、以下のフォームよりご入力ください。 ご入力内容は、Think!事務局が確認してサービス改善の参考にさせていただきます。',
                   '※すべてのメッセージをエキスパートにお伝えするとは限りません。',
                   '※このフォームからのメッセージに対する返信は行っておりません。予めご了承ください。']
        paragraph_texts = [p for p in paragraph_texts if p not in exclude]

        # Keep only the first 5 paragraphs in the article
        paragraph_texts = paragraph_texts[:5] if len(paragraph_texts) > 5 else paragraph_texts
        
        # join paragraph texts into a single string
        texthold = '\n'.join(paragraph_texts)
        texthold = texthold.replace('\n', '</p><p>')
        session['text'] = texthold

        # Set the title to the article title
        session['title'] = article.title
        
    
        instructions = "Pretend you are an expert in language instruction. Your student's level is intermediate to advanced."
        responses = []
        GPTmessages = []
        GPTmessages.append({"role":"system","content":instructions})
        GPTmessages.append({"role":"assistant","content":session['text']})
        user_question = "Choose three pieces of vocabulary or idioms, either nouns or verbs (in which case leave them conjugated as in the article), which will be difficult for an English speaker, from this news article appropriate for testing a student who is intermediate to advanced in Japanese.  List them in a comma separated way, with no other response."
        GPTmessages.append({"role":"user","content":user_question})
        response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=GPTmessages
        )
        reply = response["choices"][0]["message"]["content"]
        try:
            word1, word2, word3 = response["choices"][0]["message"]["content"].split(",")
        except ValueError:
            word1, word2, word3 = "", "", ""
        session['reply1'] = "What does " + word1 + " mean?"
        session['reply2'] = "What does " + word2 + " mean?"
        session['reply3'] = "What does " + word3 + " mean?"
    
        instructions = "Pretend you are an expert in language instruction. Your student's level is intermediate to advanced. Be sure to ask explicitly for the student to translate the sentence you pick!"    
        explanation = "Choose one single interesting sentence from the attached text and ask me explicitly to translate it from Japanese into English.  Say nothing else in response except for stating the sentence in Japanese which you want me to translate into English, and asking me to give this translation.  Do NOT translate the sentence yourself - remember, you are trying to teach me Japanese!"
        messages = [
            {"role":"system","content":instructions},
            {"role":"user","content":explanation},
            {"role":"assistant","content":session['text']}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        session['reply4'] = response["choices"][0]["message"]["content"]   
    
        instructions = "Pretend you are an expert in language instruction. Your student's level is intermediate to advanced."
        explanation = "Choose one single grammatical construction which may be difficult to understand for someone at my level.  State the grammatical construction in Japanese without telling me what it means, and ask me to explain how it is being used."
        messages = [
            {"role":"system","content":instructions},
            {"role":"user","content":explanation},
            {"role":"assistant","content":session['text']}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        session['reply5'] = response["choices"][0]["message"]["content"] 
        
        messages = [
                {"role":"system","content":"Choose a single sentence only and remember, you are a Japanese teacher."},
                {"role":"user","content":"Choose a single sentence from the article that involves a lot of activity, or action, or the kind of thing that could be visualized or drawn."},
                {"role":"assistant","content":session['text']}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
#        response2 = openai.Image.create(
#            prompt=response["choices"][0]["message"]["content"],
#            n=1,
#            size="256x256"
#        )
        session['reply6'] = response["choices"][0]["message"]["content"] 
#        image_url = response2['data'][0]['url']
        
        return render_template('index.html', text=session['text'], title=session['title'], reply1=session['reply1'], reply2=session['reply2'], reply3=session['reply3'], reply4=session['reply4'], reply5=session['reply5'], reply6=session['reply6'])
       


