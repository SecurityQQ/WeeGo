WeeGo was built at [HackUPC Fall 2017](https://devpost.com/software/weego)

=WeeGo=

==Inspiration==
All of us are very active messengers' users. Many of our events are arranged in social networks. But sometimes we lose an invitation, forget about it or do not know anyone who would like to join us. The willing to solve this problem has brought us to WeeGo.

==What it does==
Imagine, you chat with your friends everyday, and often receive offers to get together, or you want to go somewhere but don't have a partner. In this situation WeeGo is a useful smart observer, who remembers your desires and looks for the best solutions to satisfy them. It detects actions, places and time, sends you invitations and receipts. You can also pay for the ticket with Telegram payment system. Finally, you may use aggregated by bot data in an android application where you will find beautiful interface to discover new people and new places. For long-distanced rides we provide users with integration with Skyscanner: discuss and track travels and flights easier than it ever was!

==How we built it==
We use NLP with requests to Google Places to fetch place, location and datetime of an action. Also, we generate previews with Bing Images. Our server has been deployed on AWS EC2. We have combined a lot of different APIs and SDKs, including Skyscanner, MyQR, Compreno, Google Places, Bing Search.

==Challenges we ran into==
We ran into ImaginBank chatbot challenge and Skyscanner challenge.

==Accomplishments that we're proud of and What we learned==
We have made a very good and friendly team with a nice separation of tasks. We improved our skills and results since last Hackathon, we have tested a lot of API and successfully combined them. In our humble opinion, the biggest accomplishments of our work are stability and usability of the product.

==What's next for WeeGo==
Among other things WeeGo is a way of data collection. Our next goal is to expand the service, finish data acquisition and train generative adversarial networks to add more options in text recognition. For the marketing part, we would like to cooperate with commercial organisations, create discounts for our customers and prepare data for future smart engines.

==Built with love and==
natural-language-processing, python, flask, telegram-bot, sqlite, android, rxjava, google-places, bing-search-api, amazon-web-services, amazon-ec2
