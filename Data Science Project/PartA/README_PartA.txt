README for Part A of the HW3.

----All code was written by me without copying any code from anyone else.----

------Streaming API-------
The fetch_samples function was modified to make the output in a readable format to avoid encoding errors later in the term frequency question while converting to a json format. Following is the change I made after referring to a couple of posts by Bradley Golden in Piazza and studying the data pattern in the original output file.

line.strip() - > line.strip().decode('utf-8')

The output files(streaming_output_full_smural21.txt and streaming_output_short_smural21.txt ) were generated based on the script ran on 22nd March at 5:45 pm.


----Search API-----
The third query to fetch data from the Search API was run on 18th march 2016 at 7:20 pm on the remote machine in azure via Putty. The search term used was "Trump". 

--------------User Tweets-------------------
User tweets were collected on 22nd March @ 10:30.


------------Term Frequency------------------
The stopwords text file is assumed to be in the data folder.
The tweet file is assumed to be in the same folder as the frequency_smural21.py.
----------------------------------------------------------------------------------------

1. All python files have been included.
2. A result file for each part of the assignment has also been included. They are:
	i. streaming_output_full_smural21.txt
	ii. streaming_output_short_smural21.txt
	iii. search_output_smural21.txt
	iv. breaking_bad_tweets_smural21.txt
	v. term_freq_smural21.txt
3. The data folder has been included in this folder: PartA.
------------------------Thank You----------------------



