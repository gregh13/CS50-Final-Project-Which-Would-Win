# Which Would Win?
#### Video Demo:  https://youtu.be/TJJvPLUTMQs
#### Description:
TLDR; A simple, responsive web-hosted (Heroku) game in which players are given two choices and must select the one that is 'worth more'.

Full Description:

Optimized for either mobile or desktop browser viewing, players will be presented with a series of choices. These choices could be a country, a company, a billionaire, a cryptocurrency, or a man-made object/project.
Players must decide which option is 'worth more'. User will be comparing annual GDP (countries), market cap valuations (companies and cryptocurrencies), net worth (billionaires), or cost to buy/make (objects/projects).
In the context of money, it boils down to the question "Which would win?".

Dollar amounts are in USD and never shown to the user (in order to retain re-playability and difficulty). For every correct answer, the user gains a point. One wrong answer and the game ends (gameover.html). Users are then allowed to save their score, which is stored in the database. The top 10 highest scores are displayed in a table on the homepage (index.html).

Values for country GDP and man-made object costs are hard-coded and static (these values don't change often and there aren't good options for API calls for this data) in the file mm_dicts.py
However, the values for the companies, billionaries, and cryptocurrencies are updated daily via API. The API calls are run in a separate file (master_dict.py) that Heroku Scheduler runs once a day. The new data is then stored in the database. When players press 'Start Game', the app pulls the most current dataset. Additionally, the order of the choices is randomized each game, and there are no repeats within anyone one game (using shuffled list order).

If a user is able to make it to the end of the list of choices (roughly 70 choices, so about 35 rounds), they 'win' the game (winner.html). This hard-cap was intentionally set to give a user with that high of a score some positive feedback and sense of completion. If over time, the top 10 highest scores are all at the limit of 34/35 points, then this limitation can easily be modified to create a higher score ceiling.

During testing, a few potential bugs were found in which users could 'cheat'. One way was to use the back button after selecting a wrong choice, then proceed with the now-known correct choice. A second issue was where, by which clicking on the correct choice 'submit' button rapidly, users could increase their score without reloading the next choice (basically, taking advantage of the more time consuming process of rendering the next template, but still accessing the earlier code which adds to their score). A session variable 'gameover' fixed the former, and some javascript mixed with some session variable/jinja logic (form_controller/f_con) fixed the latter.

This project was a good challenge and practice of the skills we learned in CS50 (and beyond!). Hopefully users enjoy this game, strive to beat each other's scores, and learn a thing or two about the insane magnitude of wealth that some people/companies/projects have (i.e. Elon Musk vs Greece)!