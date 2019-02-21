# Project Description:
This project is a tool that allows users to input the name of a New York Times Bestseller list and receive a csv of data from both the New York Times and GoodReads about the books on that list. The data that the user receives includes the 
* title 
* author
* bestseller rank
* time on the bestsellers list
* rank progress (how the NYT rank has changed in the past week)
* average Goodreads rating
* number of Goodreads ratings
* number of Goodreads reviews
* number of Goodreads text reviews
* Goodreads grand total rating (average rating * number of ratings)

The program also caches data when a request is made  so there are not excessive requests to the NYT and Goodreads APIs.


# Files:
1. [the project file](https://github.com/cikeddy/NYTGoodreadsBookData/blob/master/SI506F18_final_project.py): SI506F18_final_project.py
2. [a sample file](https://github.com/cikeddy/NYTGoodreadsBookData/blob/master/SAMPLE_output.csv) for the output -> SAMPLE_output.csv

# Modules:
The json, requests, and csv modules are used in this project. For a list of requirements check the [requirements file](https://github.com/cikeddy/NYTGoodreadsBookData/blob/master/requirements.txt)

# Instructions:
1. To run the project, type "python SI506F18_final_project.py" into the command prompt and hit enter
2. When you run the file in the command prompt, you will be asked to input the name of a New York Times Bestseller list. 
    * The list names are provided to you in the command prompt but can also be found online at [the NYT Bestseller website](https://www.nytimes.com/books/best-sellers)
    * An example input is "Paperback Nonfiction" or "paperback nonfiction"; the input is not case dependent

# Result:
Once you input the list you would like data from, the program will produce a csv file (there will be a message in the command prompt that will tell you when it is finished) titled "project_output.csv" which can be found in the same directory as the project python file.



