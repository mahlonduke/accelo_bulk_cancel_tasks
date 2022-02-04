# Dependencies
import requests
import json


# API Call Setup
deployment = 'deployment' # Name of the deployment we'll be updating.  No ".accelo.com"
token = 'redacted' # Token for a Service-type API application in the target deployment
headers = {'Content-Type': 'application/json', # Boilerplate.  Don't change.
          'Authorization': f'Bearer {token}'}
baseURL = f'https://{deployment}.api.accelo.com/api/v0/tasks?_filters=standing(pending,accepted,started,paused),against_type(asset,company,issue,prospect,contract_period),date_started_before(1632960000)&_fields=id,title,standing,date_started&_limit=100' # URL we'll be pulling data from, including filters and fields


# Initialize the while loop
responseLength = 2

# Loop through all the tasks
while responseLength > 1:
    response = requests.get(baseURL, headers=headers) # Get the tasks from the API
    responseStatusCode = response.status_code # Get the response code to verify it was successful
    responseBody = response.json() # Extract the task data from the Accelo API's response
    responseLength = len(responseBody['response']) # Determine how many tasks we got back
    print(f'Current Response\'s # of Tasks: {responseLength}') # Print the results on screen

    # Loop through each of the tasks provided by the API
    for i in responseBody['response']:
        taskID = i['id'] # Get this iteration's task's ID
        updateURL = f'https://{deployment}.api.accelo.com/api/v0/tasks/{taskID}/progressions/14/auto' # Endpoint that will update the task's status, based on the task's ID
        print(f'Updating task ID #{taskID}') # Print this iteration's task's ID on screen

        # Try to update the task's status to inactive.  Exit on fail
        try:
            response = requests.put(updateURL, headers=headers) # Run the "Cancel Task" Progression on this iteration's task ID
            responseStatusCode = response.status_code # Get the response code to verify it was successful
            responseBody = response.json() # Extract the task data from the Accelo API's response

            if response.status_code == 200: # Task was updated successfully
                print('Update successful')
            else: # Task update failed
                print(f'Update failed: {responseStatusCode}')
                print(f'Detils: {response}')
                responseLength = 0
        except (e): # Error connecting to the API
            print(f'Error requesting the update: {e}') # Print the error on screen
            responseLength = 0
