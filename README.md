# InsightCodingChallenge
Coding Challenge as part of the application for the Insight Bootcamp

##
So this is my ANSWER to the challenge posted [here] (https://github.com/InsightDataScience/coding-challenge).
I hope I did this right as I have little experience but it was FUN. 

### Some dependencies I used
NONE :grin: :grin: :grin:

### Some notes :clipboard: :clipboard: :clipboard:
I implemented this on Python 3.4.3, which actually ran into some issues with the decoding/encoding of the tweets. Apparently, Python 3 uses Unicode for their str variables, so this may have explained why I had to use so many encode() and decode() methods in order to "filter" out any \u**** characters. In Python 2.7 or so, I'm not exactly sure if this would be the case, but if not, I doubt there would be as much character "type-casting". This could maybe speed things up. Maybe. I'll have to look into it. :racehorse: :dash:

I did not use numpy as you may have noticed but I did implement it in my earlier version. There are several reasons as to why I chose to get rid of it and use what Python already has built in. First, numpy was only being used twice in my program; once to provide the bounds for a for loop (e.g. numpy.arange(5) versus range(0,5)), and the second to convert a Python list to a numpy.array(). Numpy *did* perform faster by barely under 1% in time savings. This 1% was not a huge concern for me. I also looked at the context at which numpy was being used to manipulate data; the inputs are not large whatsoever. The input for numpy.arange was on average 4, so the cost savings is minimal at that scale, and the numpy.array() was manipulating a list of an average length of 4, so again, minimal cost savings. I am also fairly confident in the fact that this 4 value will not change, as it corresponds directly to the degree of the vertices. From the ft2.txt file, I can see that this average degree values hovers between 3.5 and 4.5, and it's not something that will change, as the context is saying that on average, a tweet with more than one hashtag has 4 hashtags, and people aren't going hashtag crazy anytime soon. So I removed numpy for these reasons, as it is one less dependency to have to have, and although the cost benefit of this is more abstract to me right now, if the removal of this only slows down the program by 1% and I'm confident that it will always stay under this 1% because of the context, I'm ok with it. 

I did not implement any of the "get-tweets" on my own as my experience with dev-ops is limited and did not want to remove focus on the priority. I did try to use the get-tweets.py on my own twitter account, but there seems to be a problem with some version control as there was issues compiling when I imported tweepy, and I again, this was not the focus of the project, so I quickly moved on and only used your tweets.txt file. :confused: :confused: :confused:

My earlier implementation of tweets_cleaned.py included a nested try: block. This was because previously the tweets.txt file, on line 5 had 2 Json objects, which would make the reading much more difficult. I did not know if this was done on purpose to make the program more robust towards faulty entry data, but I removed this block when a fix to the tweets.txt file was made. 

:moyai: :moyai: :moyai:
