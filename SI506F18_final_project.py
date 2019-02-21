import json
import requests
import csv

cache_file = 'Final_Project_Cache.json'
GOODREADS_API_KEY  ='TYPE GOODREADS API KEY HERE'
NYT_API_KEY = 'TYPE NYT API KEY HERE'

## the code for params_unique_combination was provided by instructional staff for class use
def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

try:
    cache_file = open(cache_file, 'r')
    cache_contents = cache_file.read()
    cach_dict = json.loads(cache_contents)
    cache_file.close()
except:
    cache_dict = {}

def get_goodreads_data(isbns):
    baseurl = 'https://www.goodreads.com/book/review_counts.json'
    params = {'key':GOODREADS_API_KEY,'isbns': isbns}

    unique_ID = params_unique_combination(baseurl, params)

    if unique_ID in cache_dict:
        return cache_dict[unique_ID]
    else:
        try:
            resp = requests.get(baseurl, params)
            cache_dict[unique_ID] = json.loads(resp.text)
            dumped_json_cache = json.dumps(cache_dict, indent=4)
            with open(cache_file,"w") as file:
                file.write(dumped_json_cache)
            return cache_dict[unique_ID]
        except:
            print("GoodReads Data Not Available for one of the books in the NYT list")



def get_nyt_data(list):

    baseurl = "https://api.nytimes.com/svc/books/v3/lists.json"
    params_diction = {}
    params_diction["list"] = list
    params_diction["api-key"] = NYT_API_KEY


    unique_ident = params_unique_combination(baseurl,params_diction)

    if unique_ident in cache_dict:
        return cache_dict[unique_ident]
    else:
        resp = requests.get(baseurl, params_diction)
        cache_dict[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(cache_dict, indent=4)
        with open(cache_file, "w") as f:
            f.write(dumped_json_cache)
        return cache_dict[unique_ident]

lists_baseurl = "https://api.nytimes.com/svc/books/v3/lists/names.json"
lists_params_diction = {'api-key':NYT_API_KEY}
unique_ident = params_unique_combination(lists_baseurl, lists_params_diction)
if unique_ident in cache_dict:
    list_obj= cach_dict[unique_ident]
else:
    lists_resp = requests.get(lists_baseurl, lists_params_diction)
    cache_dict[unique_ident] = json.loads(lists_resp.text)
    lists_dumped_json_cache = json.dumps(cache_dict, indent=4)
    with open(cache_file, "w") as f:
        f.write(lists_dumped_json_cache)
    list_obj = cache_dict[unique_ident]

list_names = []
for item in list_obj['results']:
    list_names.append(item['list_name'].lower())

list_names_string = ""

for item in list_names:
    list_names_string += str(item) + "\n"
# list_names_string += " or" + list_names[-1]


class GR_book(object):
    def __init__(self,object,title,author, current_rank, time_on_list, rank_progress):
        self.title = title
        self.author = author
        self.time_on_list = time_on_list
        self.rank_progress = rank_progress
        self.current_rank = current_rank

        try:
            for book in object['books']:
                self.isbn = book['isbn']
                self.num_ratings = book['ratings_count']
                self.num_reviews = book['reviews_count']
                self.num_text_reviews = book['text_reviews_count']
                self.rating = book['average_rating']

        except:
                self.isbn = int()
                self.num_ratings = float()
                self.num_reviews = float()
                self.num_text_reviews = float()
                self.rating = float()

    def grand_tot_rating(self):
        tot_rating = float(self.rating) * float(self.num_ratings)
        return tot_rating

    def __str__(self):
        return "{} by {} has an average rating of {}, was rated {} times, and reviewed {} times".format(self.title, self.author, self.rating, self.num_ratings, self.num_reviews)

    def csv_row_data(self):
        return [self.title, self.author, self.current_rank, self.time_on_list, self.rank_progress, self.rating,self.num_ratings, self.num_reviews,self.num_text_reviews,self.grand_tot_rating()]


class NYT_book(object):
    def __init__(self,object):
        self.list = object['list_name']
        self.best_date = object['bestsellers_date']
        self.pub_date = object['published_date']
        self.current_rank = object['rank']
        self.last_wk_rank = object['rank_last_week']
        self.time_on_list = object['weeks_on_list']

        for item in object['book_details']:
            self.author = item['author']
            self.title = item['title']
            self.description = item['description']
            self.isbn = item['primary_isbn10']

    def __str__(self):
        return "{} by {} published on {} made the bestseller's list on {} and was on the list for {} weeks".format(self.title,self.author,self.pub_date, self.best_date,self.time_on_list)

    def get_description(self):
        return self.description

    def rank_progress(self):
        try:
            progress = int(self.current_rank) - int(self.last_wk_rank)
        except:
            return "No data to produce rank progress"

        if self.last_wk_rank != 0:
            if progress > 0:
                return "the rank has dropped by {} spots".format(progress)
            elif progress < 0:
                return "the rank has increased by {} spots".format(-1*progress)
            elif progress == 0:
                return "the rank has not changed"
        else:
            return "No data to produce rank progress"


input_available = False
user_input = input('\033[95m' + "What New York Times Bestseller list would you like data for? \nYou can enter any of the following:\n " + '\033[1;37;40m' + list_names_string + "\n")

while(input_available == False):
        user_input = user_input.lower()
        if user_input in list_names:
            user_request = get_nyt_data(str(user_input))
            input_available=True
        else:
            user_input = input("\n try again:\n")

NYT_books = []
for book in user_request['results']:
    NYT_books.append(NYT_book(book))

GR_books = []
for book in NYT_books:
      GR_books.append(GR_book(get_goodreads_data(str(book.isbn)), book.title, book.author, book.current_rank, book.time_on_list, book.rank_progress()))

csv_header = "Title, Author, Bestseller Rank, Time On List, Rank Progress, Average GoodReads Rating, Number of GoodReads Ratings, Number of GoodReads Reviews, Number of GoodReads Text Reviews, GoodReads Grand Total Rating (Average Rating * Number of Ratings)\n"

with open("project_output.csv","w") as f:
    writer = csv.writer(f, lineterminator = '\n')
    f.write(csv_header)
    for book in GR_books:
        book_row = book.csv_row_data()
        writer.writerow(book_row)


print("\nthe data can be found in a csv file in the directory")
