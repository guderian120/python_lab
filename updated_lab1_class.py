import time, sys
import requests, os
import shutil
from datetime import datetime


class Downloader: # Instantiate a python class
    def __init__(self,max_retries=3, retry_delay=2 ): # function runs on python class initiation
        self.url = url
        self.local_file = local_file
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.directory_name = directory_name
    

    def create_dir(self, directory_name): # A reusable function to create directories
        if os.path.exists(directory_name): # if directory to create exists
            try:
                shutil.rmtree(directory_name) # remove it with
                print(f"Directory '{self.directory_name}' has been removed successfully.")
            except Exception as e: # if any errors encounted, pipe error message into variable e
                print(f"Error: {e}") #print  e
                sys.exit(0) # exit with a problem

        
        if not os.path.exists(directory_name): # if there is no directory
            os.makedirs(directory_name) # make the directory to create
            print(f"Directory: {self.directory_name} created.")
        

    def get_file_from_url(self, url, local_file): # a reusable function to download files
        for attempt in range(1, self.max_retries + 1): # Try to download files in a certain number of attempts
            try:
                response = requests.get(url) # get response from api endpoint
                response.raise_for_status() # if response is not 200 raise an exception

                print(f"File successfully downloaded.")
                with open(local_file, 'wb') as output_file: # open file to write downloaded bytes
                    for chunk in response.iter_content(chunk_size=8192): # chunk files for write
                        output_file.write(chunk)
                print('File saved successfully.')
                


                # Step 6: Overwrite File Content with custom input
                user_input = input("Describe what you have learned so far in a sentence: ") # take user input
                now = datetime.now() # get current time
                current_time = now.strftime("%Y-%m-%d %H:%M:%S") # convert random numbers into readerble time format

                with open(local_file, "w") as file: #opening our file to overwrite with user input
                    file.write(user_input + "\n")
                    file.write(f"Last modified on: {current_time}") # append the time current to file
                    print("File successfully modified.")

                # Step 7: Display the Updated File Content
                with open(local_file, "r") as file: # open the new file in read mode
                    print("\nYou Entered: ", end=' ') 
                    print(file.read())# print the file on screen
                    sys.exit(1) #exit without errors

            except(requests.RequestException, IOError) as e: # in cases of error retrieving file from api
                print(f"Attempt {attempt} failed: with error")
                if attempt < self.max_retries: # attempt until all atempts run out
                    print(f"Retrying in {self.retry_delay} seconds....")
                    time.sleep(self.retry_delay)
                else: print(f"All attempts failed")
                     
directory_name = 'andy.amponsah'
local_file = os.path.join(directory_name, 'andy.amponsah.txt')
url = "https://raw.githubusercontent.com/sdg000/pydevops_intro_lab/main/change_me.txt"
# url = "http://127.0.0.1:8000/api/dashboard" # django test url

if __name__ == '__main__': #if running script from same script itself
    c = Downloader(max_retries = 3, retry_delay=1)
    c.create_dir(directory_name)
    c.get_file_from_url(url,local_file )
