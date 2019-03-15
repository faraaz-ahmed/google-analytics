"""A simple example of how to access the Google Analytics API."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import os

def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.
    # Get a list of all Google Analytics accounts for this user
    # get_goals(service)
    accounts = service.management().accounts().list().execute()
    data = []
    # my_account = 0
    if accounts.get('items'):
        for i in range(len(accounts.get('items'))):
        # for i in range(0,2):
            # Get the first Google Analytics account.
            account = accounts.get('items')[i].get('id')
            account_name = accounts.get('items')[i].get('name')
            # Get a list of all the properties for the first account.
            properties = service.management().webproperties().list(accountId=account).execute()
            # print("Account",account)
            if properties.get('items'):
                # Get the first property id.
                for j in range(len(properties.get('items'))):
                    property=properties.get('items')[j].get('id')
                    property_name=properties.get('items')[j].get('name')
                    # print("Property",property)
                # Get a list of all views (profiles) for the first property.
                    profiles = service.management().profiles().list(accountId=account,webPropertyId=property).execute()
                    for k in range(len(profiles.get('items'))):
                        view = profiles.get('items')[k].get('id')
                        view_name = profiles.get('items')[k].get('name')
                        goals = service.management().goals().list(accountId = account,webPropertyId=property, profileId = view).execute()
                        for goal in goals.get('items', []):
                            print ('Goal Name = ', goal.get('name'))
                            goal_name = goal.get('name')
                            data.append([account,account_name,property,property_name,view,view_name,goal_name])
                            print(data)
                        # print("View",view)
                        # print(account,account_name,property,property_name,view,view_name)
    return data

def data(data):
    outputdf = pandas.DataFrame(columns=['account','account_name','property','property_name','view,view_name','goal_name'])
    outputdf = pandas.DataFrame(data)
    # outputdf.to_csv('GA_Country_Sessions1.csv',header ='column_names')
    if not os.path.isfile('GA_Country_Sessions_draft2.csv'):
        outputdf.to_csv('GA_Country_Sessions_draft3.csv',header ='column_names')
    else: # else it exists so append without writing the header
        outputdf.to_csv('GA_Country_Sessions_draft3.csv',mode = 'a',header=False)

def get_goals(service):
    accounts = service.management().accounts().list().execute()
    # data = []
    if accounts.get('items'):
        for i in range(len(accounts.get('items'))):
        # for i in range(0,2):
            # Get the first Google Analytics account.
            account = accounts.get('items')[i].get('id')
            account_name = accounts.get('items')[i].get('name')

            # Get a list of all the properties for the first account.
            properties = service.management().webproperties().list(accountId=account).execute()
            goals = service.management().goals().list(accountId = account).execute()

# Example #3:
# The results of the list method are stored in the Goals object. The following
# code shows how to iterate through them.
        for goal in goals.get('items', []):
            print ('Property ID          = ', goal.get('webPropertyId'))
            print ('Internal Property ID = ', goal.get('internalWebPropertyId'))
            print ('View (Profile) ID    = ', goal.get('profileId'))

            print ('Goal Number = ', goal.get('id'))
            print ('Goal Name   = ', goal.get('name'))
            print ('Goal Value  = ', goal.get('value'))
            print ('Goal Active = ', goal.get('active'))
            print ('Goal Type   = ', goal.get('type'))

            print ('Created     = ', goal.get('created'))
            print ('Updated     = ', goal.get('updated'))

    # Print the goal details depending on the type of goal.
        # if goal.get('urlDestinationDetails'):
        #     print_url_destination_goal_details(goal.get('urlDestinationDetails'))

        # elif goal.get('visitTimeOnSiteDetails'):
        #     print_visit_time_on_site_goal_details(goal.get('visitTimeOnSiteDetails'))

        # elif goal.get('visitNumPagesDetails'):
        #     print_visit_num_pages_goal_details(goal.get('visitNumPagesDetails'))

        # elif goal.get('eventDetails'):
        #     print_event_goal_details(goal.get('eventDetails'))

def main():
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location_1 = 'Merilytics-DCC-0ccc4fbf968a.json'
    key_file_location_2 = 'merilytics-dcc-6f8c0965da14.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location_1)

    profile_id = get_first_profile_id(service)
    data(profile_id)

    service_2 = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location_2)

    profile_id_2 = get_first_profile_id(service_2)
    data(profile_id_2)


if __name__ == '__main__':
    main()
