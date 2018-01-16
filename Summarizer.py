# 10/31/17 last edited: 11/13/17 at 12:33 AM     Joseph Spinosa
# Right now we basically force the user to use a pickle file if one is found in the directory. We should make it optional
# The active pickle file should be passed in as the only command line argument. No argument is also acceptable
# This file must be run with python3, NOT python from command line
# We must validate the 2nd command line argument, it is not being checked right now
import sys
import os, glob
import pickle
import argparse
from Summ_Article import *
from TextRank import *
from ExtractedArticle import *
from Edmundson import *

def make_pickle(folder):
    os.chdir(folder)
    answer = "y"
    while answer == "y":
        settings = makesettings()  # a dictionary
        filename = input("please enter the name of this pickle file: ")
        save_settings = open(filename + ".pickle", "wb")
        pickle.dump(settings, save_settings)
        save_settings.close()
        answer = input("Please enter y to continue making pickle files, or anything else to stop ")
    os.chdir('..')
def makesettings():
    print("You will be guided through setting the tunings for each overall module and each subscore of each module."
          "Each prompt represents one tuning. The tunings in all caps represent the overall module. Edmundson and"
          "Extracted both have subscores which are adjustable as well. For each a double must be entered ranging from "
          "0 - 5. These numbers act as multipliers for the scores. Entering the same numbers for the subscores of a "
          "module is not reccommended. Entering in invalid value will defualt that multiplier to 1.0\n")

    modules = ['EDMUNDSON', 'keywords', 'length', 'titlewords', 'cuephrase', 'EXTRACTED', 'pronounphrase', 'prepositionalphrase',
               'articles', 'conjunctionphrase', 'TEXTRANK']

    tunings = {}
    for module in modules:
        try:
            weight = float((input(module + " weight: ")))     # is float correct?
            if weight >= 0 and weight <= 5:
                tunings[module] = weight

            else:
                tunings[module] = 1.0

        except:
            print("Each entry must be non-empty and contain no characters. Default will be used for " + module)
            tunings[module] = 1.0

    return tunings
def choose_pickle_file(pickle_files):
    response = input("please enter the name of the pickle file you want for this run: ")
    if response in pickle_files:

        return response

    else:
        while response not in pickle_files:
            response = input(
                "You entered in invalid file name. Please try again from the folowing list: " + str(pickle_files) + "\n")
        return response
def create_directory():
    custompath = input("Please enter the path where you would like the summary folder to be made (leave blank for this directory): ")
    if custompath != "":
        try:
            os.makedirs(custompath + "/Summaries/pickle files")
            print("Creating directory at " + custompath + "/Summaries")
            return (custompath + "/Summaries")

        except:
            print("Invalid path, please try again \n")
            exit()

    else:
        try:
            os.makedirs("Summaries/pickle files")
            print("Creating directory at " + os.getcwd() + "/Summaries")
            return (os.getcwd() + "/Summaries")

        except:
            print("An error occured! Couldn't make directory: " + os.getcwd() + "/Summaries" + "\n")
            exit()
def retrieve_settings(filename , filepath):
    os.chdir("..")
    os.chdir("..")
    parent_path = os.getcwd()
    #print ( "hello " + parent_path)
    os.chdir(filepath)
    with open(filename, 'rb') as settings:
        custom_dictionary = pickle.load(settings)
    os.chdir(dir_path)
    return custom_dictionary


#-----------------------------------------------------------------------------------------------------------------------

dir_path = os.path.dirname(os.path.realpath(__file__))  # the directory this file is located in
Summarypath = ""
Picklepath = ""

os.chdir(dir_path)
pickle_files = []
active_pickle_file = ""
custom_settings = {}
URL = ""
summary = ""
default_settings = {'EDMUNDSON' : 1.0 , 'keywords': 2.0 , 'length': 1.75, 'titlewords': 2.0, 'cuephrase': 1.25,
                    'EXTRACTED': 1.0, 'pronounphrase': 4.0, 'prepositionalphrase': -1.0, 'articles': -1.0,
                    'conjunctionphrase': 2.0, 'TEXTRANK': 1.0}

parser = argparse.ArgumentParser()
parser.add_argument("URL" , help = "Enter a URL to an online article")
parser.add_argument("Pfile", help = "optionally specify system tunings", nargs = "?")
args = parser.parse_args()

URL = args.URL
if args.Pfile and os.path.isdir(os.curdir + "/Summaries/pickle files") and os.path.isfile(os.curdir + "/Summaries/pickle files" + "/" + args.Pfile):
    os.chdir(os.curdir + "/Summaries/pickle files")
    active_pickle_file = args.Pfile
    custom_settings = retrieve_settings(active_pickle_file, os.curdir + "/Summaries/pickle files" )

elif args.Pfile and ((not os.path.isdir(os.curdir + "/Summaries/pickle files")) or (not os.path.isfile(args.Pfile))):
    print("There was a problem with the pickle file argument. Either the file does not exist or the directory"
          " Which is meant to contain the pickle file does not exist")

#-----------------------------------------------------------------------------------------------------------------------

if os.path.isdir(os.curdir + "/Summaries"):
    Summarypath = os.curdir + "/Summaries"
    Picklepath = Summarypath + "/pickle files"

else:
    new_directory = input("A folder for summaries/pickle files was not found at this directory. Would you like to set up"
          " a folder for your summaries and pickle files? (y/n): ")

    if new_directory == "y":
        Summarypath = create_directory()
        Picklepath = Summarypath + "/pickle files"

    else:
        print("Please run the system again to configure folder for pickle files. NOTE: The system will only display"
              " pickle files located inside the appropriate folder. Any pickle files made must be placed inside that folder")

#-----------------------------------------------------------------------------------------------------------------------

make_preliminary_pickle = input("Would you like to create pickle files? (Enter y for yes) ")
if make_preliminary_pickle == "y" and Summarypath != "":
   # print(Picklepath)
    make_pickle(Picklepath)

elif Summarypath == "":
    print("Couldn't find Summaries directory to place pickle file in")

if active_pickle_file == "":
    print("This system uses a pickle file for the summary tunings. If there is no pickle file the system will "
      "use default values for the individual modules. The following pickle files were found in this directory: ")

os.chdir(dir_path)
os.chdir(Picklepath)
for file in glob.glob("*.pickle"):
    if active_pickle_file == "":
        print(file)
    pickle_files.append(file)

# ----------------------------------------------------------------------------------------------------------------------

if active_pickle_file == "":
    set_active = input("No file was passed as a command line argument. Would you like to set an active pickle for this run? (y/n) ")
    if set_active == "y" and len(pickle_files) > 0:
        active_pickle_file = choose_pickle_file(pickle_files)
        custom_settings = retrieve_settings(active_pickle_file, Picklepath)
        #print(str(custom_settings))

    else:
        print("Default values will be used. Please run this program again to create/set a pickle file")
        custom_settings = default_settings

else:
    print("The active pickle file is: " + active_pickle_file + " !")
    custom_settings = retrieve_settings(active_pickle_file, Picklepath)
    #print(str(custom_settings))

# ----------------------------------------------------------------------------------------------------------------------
os.chdir(dir_path)
article = Summ_Article(URL)
article_dict = article.create_article()
compression = -1

while not(compression > 0 and compression < 100):
    try:
        compression = int(input("Please enter the desired compression rate: "))

    except:
        print("Input must be a natural number 0-100!")
        continue

    if not (compression > 0 and compression < 100):
        print("Out of bounds, try again")

num_of_sentences = int((compression/100) * article_dict["LENGTH"])
if num_of_sentences == 0:
    print("The desired compression rate for this article resulted in a zero sentence summary. Please try"
          " again with a higher rate of compression")
    exit()

edmundson = Edmundson(article_dict)
rhetoric = ExtractedArticle(article_dict)
textrank = TextRank(article_dict["BODY"])

master_scores =  list(map(sum, zip(edmundson.get_sent_scores(custom_settings),rhetoric.get_sent_scores(custom_settings),textrank.get_sent_scores())))
preliminary_indices = sorted(range(len(master_scores)), key=lambda i: master_scores[i])[-(num_of_sentences):]
master_indices = sorted(preliminary_indices)


print("Display Summary: \n")

for index in master_indices:
    print(article_dict["BODY"][index])
    summary += article_dict["BODY"][index]

summary = summary + "\n\nThis summary was generated using: " + active_pickle_file + "\n" + "Source shrunk from " + str(article_dict['LENGTH']) + ' sentences to ' + str(num_of_sentences) + " sentences" + " (" + str(compression) + "%)"

os.chdir(Summarypath)
summary_file = open(article_dict["FILE"][:-4] + "_summary.txt", 'w')  # used to be article_dict["FILE"][:-4]
summary_file.write(summary)
summary_file.close()
article.create_file()
os.chdir("..")