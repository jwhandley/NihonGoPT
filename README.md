# NihonGoPT
Demo of using ChatGPT API for language learning based on [Kevin Bryan's FrancAIs](https://github.com/kevincure/FrancAIs).

12 March 2023

Here is a demo of the pedagogical potential of ChatGPT.  I wrote this web app in one day, with no pre-existing knowledge whatsoever of Flask or AJAX.  I used GPT to assist in writing the code and site, and of course GPT3.5 is powering the back-end of this app.

## Concept
AI-based language learning.  In this case, Japanese, for an intermediate learning.  It would be trivial to adjust this for different languages, both user languages and target being learned.  It is also trivial to adjust the level of difficulty, which could also be programmed in.

## What the app does
It randomly chooses from a defined list of topics (economy, politics, business, finance, technology, international, and society) and then picks one of the top 50 articles in that topic from the Nikkei, grabs up to 5 paragraphs of text, and prepares questions about the vocabulary, grammar and idioms.  The user inputs are converted into prompts which are better suited for training students and pointing out minor flaws and why they might have occurred.  Using this app every day would cost roughly USD 15 cents per month.

## Extensions
This is just a proof of concept, but of course, it can be extended to retain a database of target words, to use spaced repetition on those words and grammar concepts, to adjust for the language level of the student automatically, and so on.  The basic point is that with no knowledge of linguistics education, web app programming, or computer science, you can produce an app like this in one day. Knowing what I now know, I could do it a second time in a couple hours.

## Usage instructions
The app is python using flask.  You need Python as well as an OpenAI key, which you can get for free. Put you key in a file called APIkey.txt in your working directory, app.py in the same directory, and index.html in a Templates subdirectory.   One you have python 3.7+ installed, the easiest way to run it is to open a python instance.
- In windows open your preferred command line application and type `conda env create -f environment.yml` to create the conda environment "NihonGoPT" with the required dependencies
- Type `set FLASK_APP=app` so Flask knows to run the program "app"
- Type flask run
- Open http://localhost:5000/ in your web browser
Now you are good to go!  Note that the code is somewhat stochastic, so if you reload you will get different questions. 
