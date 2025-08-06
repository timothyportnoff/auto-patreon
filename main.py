from time import sleep
import urllib3
import requests
import logging
import json
import patreon

credentials = {
        "client_id": "None",
        "client_secret": "None",
        "access_token": "None",
        "creator_token": "None"
        }

def get_user_choice():
    while True:
        choice = input("Enter your choice (1-5): ")
        if choice.isdigit() and 0 <= int(choice) < len(menu_options):
            return int(choice)
        else:
            print("Invalid input. Please enter a valid choice.")

def print_credentials():
    print("Credentials:")
    for credential in credentials:
        print("\t" + str(credential) + ": " + str(credentials[credential]))

def generate_credentials():
    try: 
        #Send message for our application for client_id and client_secret 
        message_body = { "devicetype":"app_name#instance_name", "generateclientkey":True }

        #This url is the post URL to grab an authorized user
        url = "https://" + bridge_data["bridge_ip"] + "/api"

        #Atttempt to send request for max_attempt seconds for the user to press the button.
        max_attempts = 8
        for attempts in range(max_attempts):
            # Send a POST request to the Clip Debugger APU URL with converted JSON message body
            response = requests.post(url, data=json.dumps(message_body), verify=False)
            data = response.json()

            # Check the response status
            if response.status_code == 200: # Print the response content
                if "success" in data[0]:
                    print("Authorization Successful! Response: ", response.text) 
                    client_id = data[0]["success"]["username"]
                    client_secret = data[0]["success"]["clientkey"]
                    break
                elif "error" in data[0]:
                    pass
            if attempts == max_attempts - 1:
                print("Failed to POST authentication request. Error code:", response.status_code, "Response: ", response.text)
            sleep(1)
    except requests.exceptions.RequestException as e:
        print("An error occurred during the POST request in menu option 1:", e)

#Execute if script is ran directly and not imported as module.
if __name__ == "__main__":
    try:
        #Welcome!
        print("Welcome!")
        sleep(0.3)

        #FIXME: First off, this is incredibly unsafe. Disables InsecureRequestWarning. Supresses the notification we get from not verifying the SSL certification.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        #Check to see if we saved credentials previously:
        print("Loading credentials...")
        try:
            with open('credentials.json') as file:
                credentials = json.load(file)
                if credentials["client_id"] == None:
                    print("Credentials not found.")
                    generate_credentials()

                else:
                    print("Credentials found.")
                    credentials["client_id"] = credentials['client_id']
                    credentials["client_secret"] = credentials['client_secret']
                    credentials["access_token"] = credentials['access_token']
                    credentials["creator_token"] = credentials['creator_token']

            #Open the image file in binary mode
            image_path = ""
            with open(image_path, 'rb') as image_file:
                # Prepare the payload for the POST request
                # This includes the data about the image such as title, description, etc.
                payload = {
                        'data': {
                            'type': 'media',
                            'attributes': {
                                'file': image_file,
                                'title': 'Your Image Title',
                                'description': 'A description of the image'
                                }
                            }
                        }

        except FileNotFoundError:
            # Handle the case when config.json file is not found
            print("Credential file not found. Please make sure credentials.json exists.")

        except json.JSONDecodeError:
            # Handle JSON decoding error if the file is present but not valid JSON
            print("Credential file is not valid JSON.")

        #Print Credentials
        print_credentials()

        #Exit program
        print("Exiting Program.")

#Python error handling
    except json.JSONDecodeError as e:
        logging.error("An error occurred", exc_info=True)
        print("Error parsing JSON response:", str(e))

    except requests.RequestException as e:
        logging.error("An error occurred", exc_info=True)
        print("An error occurred during the request:", str(e))

        # Code to execute when Ctrl+C is pressed
    except KeyboardInterrupt:
        print("Ctrl+C detected. Exiting...")

