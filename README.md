"Hate Couture" is my graduate thesis for NYU's Interactive Telecommunications Program.  The final output will be a series of wearable, high-fashion data art pieces created through the analysis of the usage and context of hateful speech on the Internet.

I am using Python scrips to scrape data from Twitter, Reddit and Youtube, searching for key words relating to different demographics (for the purposes of the thesis version of this project, I have limited the groups to the following: African-Americans, women, Muslims, and the LGBT community).  Using natural language processing and sentiment analysis, I am then assigning each instance of the word to a scale, ranging from "benign" or "re-appropriation of the language" all the way through to "pointed/extremely hateful."  By feeding that data into Processing, I then create an abstract visualization for each targeted group that I am printing on fabric; the length of which corresponds to the volume of data collected.

I am then asking fashion designers from each demographic group that is being attacked by the hate speech I am scraping to design a garment that fulfills two requirements:

1) it uses as much of the printed fabric as possible, and
2) it is inspired by the hateful word/language in some way.

Thanks to fjavieralba for his "Basic Sentiment Analysis with Python" tutorial (http://fjavieralba.com/basic-sentiment-analysis-with-python.html), which provided the basis for much of the language analysis in this project.