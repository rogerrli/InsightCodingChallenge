# InsightCodingChallenge
Coding Challenge for Insight Bootcamp

##
So this is my ANSWER to the challenge posted here -->https://github.com/InsightDataScience/coding-challenge<--
I hope I did this right as I have little experience but it was FUN. 

### Some dependencies I used
numpy==1.10.1
wheel==0.24.0

### Some notes
I implemented this on Python 3.4.3, which actually ran into some issues with the decoding/encoding of the tweets. Apparently, Python 3 uses Unicode for their str variables, so this may have explained why I had to use so many encode() and decode() methods in order to "filter" out any \u**** characters. In Python 2.7 or so, I'm not exactly sure if this would be the case, but if not, I doubt there would be as much character "type-casting". This could maybe speed things up. 


