import wikipedia
import re
import argparse
import sys

# get the commandline arguments
def getArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", metavar="SEARCHTERM", help="Wikipedia search term.")
    # -d and -f have const="present" so the code below knows they are present but the user doesn't give a value to them
    parser.add_argument("-d", "--description", const="present", help="Article description.", action="store_const")
    parser.add_argument("-f", "--full", const="present", help="Full article.", action="store_const")

    parser.add_argument("--desctofile", metavar="PATHTOFILE", help="Article description to a file. If the file exists it will not \
    overwrite it, by default")
    parser.add_argument("--fulltofile", metavar="PATHTOFILE", help="Full article to file. If the file exists it will not overwrite \
    it, by default")
    parser.add_argument("-r", "--rewrite", const="present", help="When writing to a file if the file exists this flag will tell the \
    program to overwrite the file", action="store_const")

    arg = vars(parser.parse_args())
    return arg

args = getArgs(sys.argv[1:])
# search wikipeda for the users input and get top 10 results
wiki_search=wikipedia.search(args["search"], results=10)
# output the list to the user
index=0

for item in wiki_search:
    print(str(index) + " " + item)
    index+=1
# prompt the user to choose an article from the 10 results
index_choice=input("Choose the page you want (number): ")
# give the option to exit
if index_choice == "q" or index_choice == "quit":
    exit(0)
# check if the input is a number
try:
    int(index_choice)
except:
    print("Invalid Value: Aborting")
    exit(5)

# output the article based on the arguments the user has given
index=0
for item in wiki_search:
    if index == int(index_choice):
        # get the page of the article the user chose
        item_wiki_page=wikipedia.page(item)
        # output the full page to the console
        if args["full"]:
            print("Full page:\n")
            print(item_wiki_page.content)
        # output the summary of the page to the console
        elif args["description"]:
            print("Description:\n")
            print(wikipedia.summary(str(item)))

            print("\nfor more go to:\n")
            print(item_wiki_page.url)
        # output the summary of the page to a file the user specified
        elif args["desctofile"]:
            try:
                fp=open(args["desctofile"], "x")
                fp.write("Summary:\n")
                fp.write(wikipedia.summary(item))

                fp.write("\nfor more to:\n")
                fp.write(item_wiki_page.url)
                fp.close()
            except FileExistsError:
                print("File already exists: Aborting")
                exit(3)
            except PermissionError:
                print("Permission denied: Aborting")
                exit(4)
        # output the full page to a file the user specified
        elif args["fulltofile"]:
            try:
                fp=open(args["fulltofile"], "x")
                fp.write(item_wiki_page.content)
                fp.close()
            except FileExistsError:
                # if the rewrite flag is present overwrite the already existing file with the new one
                if args["rewrite"]:
                    fp=open(args["fulltofile"], "w")
                    fp.write(item_wiki_page.content)
                    fp.close()
                    exit(0)
                print("File already exists: Aborting")
                exit(3)
            except PermissionError:
                print("Permission denied: Aborting")
                exit(4)
        # if the user gave invalid parameters exit
        else:
            print("Parameters invalid: Aborting")
            exit(1)
    index+=1
