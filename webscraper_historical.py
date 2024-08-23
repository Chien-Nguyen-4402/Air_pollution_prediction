from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import re
import time
import requests

# Collecting all the options of a given drop-down and return them in an array
def looping_Over_A_Dropdown(drop_down):
    try:
        drop_down.click()
        drop_down.send_keys(Keys.ENTER)
        list_of_options = []
        list_of_options.append(re.sub(r'[✕▼]', '', drop_down.get_attribute("innerText")).strip())
        # print("Length of the list: ")
        # print(len(list_of_options))
        while True:
            drop_down.click()
            time.sleep(0.1)
            drop_down.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.1)
            drop_down.send_keys(Keys.ENTER)
            time.sleep(0.1)
            current_option = re.sub(r'[✕▼]', '', drop_down.get_attribute("innerText")).strip()
            previous_option = list_of_options.pop()
            list_of_options.append(previous_option)
            if current_option == previous_option:
                break
            else:
                list_of_options.append(current_option)
        return list_of_options
    except Exception as exception:
        print("--------------------------------------")
        print("Exception in looping_Over_A_DropDown")
        print(exception)
        print("--------------------------------------")
        raise(exception)

# Reset a drop down such that it contains the first possible option
def reset_drop_down(drop_down, first_option):
    try:
        while True:
            current_option = re.sub(r'[✕▼]', '', drop_down.get_attribute("innerText")).strip()
            if current_option == first_option:
                break
            else:
                drop_down.click()
                time.sleep(0.1)
                drop_down.send_keys(Keys.ARROW_UP)
                time.sleep(0.1)
                drop_down.send_keys(Keys.ENTER)
    except Exception as exception:
        print("--------------------------------------")
        print("Exception in reset_drop_down")
        print(exception)
        print("--------------------------------------")
        raise(exception)

# Selecting a specific option in the drop down:
def select_a_drop_down_option(drop_down, option_name):
    try:
        while True:
            current_option = re.sub(r'[✕▼]', '', drop_down.get_attribute("innerText")).strip()
            # print(current_option)
            # print(option_name)
            if current_option == option_name:
                break
            else:
                drop_down.click()
                time.sleep(0.1)
                drop_down.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.1)
                drop_down.send_keys(Keys.ENTER)
                # print("Current option: " + current_option)
                # print("Option_name: " + option_name)
    except Exception as exception:
        print("--------------------------------------")
        print("Exception in select_a_drop_down_option")
        print(exception)
        print("--------------------------------------")
        raise(exception)

# Collecting all state names and put them in an array
def collect_station_names(browser):
    try:
        while True:
            try:
                state_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[3]/div[2]/ng-select/div')
                break
            except Exception as exception:
                time.sleep(1)
        list_of_state_names = looping_Over_A_Dropdown(state_name)
        print("{} {}".format( "The number of states on the database right now is: ", len(list_of_state_names)))
        # for state in list_of_state_names:
        #     print(state)

        # Reset the state name dropdown such that it contains the first option in the list
        first_state_name = list_of_state_names[0]
        reset_drop_down(state_name, first_state_name)
        
        #Collecting names of all cities that are associated with each state
        states_and_cities = {}
        for state in list_of_state_names:
            select_a_drop_down_option(state_name, state)
            # Collect all city names associated with each state
            while True:
                try:
                    city_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[4]/div[2]/ng-select/div')
                    break
                except Exception as exception:
                    time.sleep(0.5)
            cities_of_this_state = looping_Over_A_Dropdown(city_name)
            # print("----------------------------------")
            # print("The current state is: " + state)
            # print("The cities of this state are: ")
            # for city in cities_of_this_state:
            #     print(city)
            states_and_cities[state] = cities_of_this_state
        # for key, value in states_and_cities.items():
        #     print("-------------------------------------")
        #     print(key, value)

        # Reset the state name drop down such that it contains the first possible option
        reset_drop_down(state_name, first_state_name)

        # Collect all the names of all statations
        stations_state_city = {}
        for state in list_of_state_names:
            select_a_drop_down_option(state_name, state)
            while True:
                try:
                    city_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[4]/div[2]/ng-select/div')
                    break
                except Exception as exception:
                    time.sleep(0.5)
            associated_cities = states_and_cities[state]
            for city in associated_cities:
                city_name.click()
                time.sleep(0.1)
                city_name.send_keys(Keys.ENTER)
                select_a_drop_down_option(city_name, city)
                time.sleep(0.1)
                while True:
                    try:
                        station_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[5]/div[2]/ng-select/div')
                        break
                    except Exception as exception:
                        time.sleep(0.5)
                stations_of_this_city = looping_Over_A_Dropdown(station_name)
                for station in stations_of_this_city:
                    stations_state_city[station] = [state, city]
        # for key, value in stations_state_city.items():
        #     print("----------------------------------------")
        #     print("Station: " + key)
        #     print("State: " + value[0])
        #     print("City: " + value[1])
        print("{} {}".format( "The total number of stations that have been collected is: ", len(stations_state_city)))
        reset_drop_down(state_name, first_state_name)
        time.sleep(0.1)
        return stations_state_city
    except Exception as exception:
        print("------------------------------------------")
        print("Exception in collect_station_names")
        raise(exception)
        print("------------------------------------------")

def collect_data_given_parameter(browser, station_list, output_file_name, start_station):
    try:
        # Create an output file
        file = open(output_file_name, 'w')

        # Initiate a new window every time this function is called
        browser = webdriver.Chrome()
        browser.get('https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing')
        browser.maximize_window()

        # Wait for the captcha to appear
        while True:
            try:
                browser.find_element(By.XPATH, '//*[@id="myModal"]/div/div/div[2]/div[3]/span')
                break
            except Exception as exception:
                time.sleep(1)
        time.sleep(5)
        # Wait for captcha verification to be completed and switch to the query page
        while True:
            try:
                browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-landing/div[2]/div[1]/div[1]/div[1]').click()
                break
            except Exception as exception:
                time.sleep(1)
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(1)

        # Accessing historical data
        while True:
            try:
                browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/h1/a').click()
                break
            except Exception as exception:
                time.sleep(1)
        
        # Switching to historical data window window
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[2])
        time.sleep(1)

        if start_station != None:
            start_station.strip()
            # If the current station comes before the desired start_station, then its status_indicator = 0
            status_indicator = 0
        
        # Filling the query page
        for station in station_list:

            # When start_station != None, make sure that we start downloading from the desired start_station
            if start_station != None:
                if station.strip() == start_station:
                    status_indicator = 1
                if status_indicator == 0:
                    continue
            
            # Print station, city, state
            print(station, station_list[station][1], station_list[station][0])
            # Choose a state
            time_waited_query = 0
            while True:
                if time_waited_query >= 100:
                    print("Restarted the window, starting again from station: " + station + ", " + stations_state_city[station][1] + ", "
                      + stations_state_city[station][0])
                    browser.quit()
                    browser = webdriver.Chrome()
                    browser.get('https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing')
                    browser.maximize_window()

                    # Wait for the captcha to appear
                    while True:
                        try:
                            browser.find_element(By.XPATH, '//*[@id="myModal"]/div/div/div[2]/div[3]/span')
                            break
                        except Exception as exception:
                            time.sleep(1)
                    time.sleep(5)
                    # Wait for captcha verification to be completed and switch to the query page
                    while True:
                        try:
                            browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-landing/div[2]/div[1]/div[1]/div[1]').click()
                            break
                        except Exception as exception:
                            time.sleep(1)
                    time.sleep(1)
                    browser.switch_to.window(browser.window_handles[1])

                    # Accessing historical data
                    while True:
                        try:
                            browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/h1/a').click()
                            break
                        except Exception as exception:
                            time.sleep(1)
                    
                    # Switching to historical data window window
                    time.sleep(1)
                    browser.switch_to.window(browser.window_handles[2])
                    time.sleep(1)

                    # Identify the state_name drop down
                    while True:
                        try:
                            state_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[3]/div[2]/ng-select/div')
                            break
                        except Exception as exception:
                            time.sleep(1)
                    break
                else:
                    try:
                        state_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[3]/div[2]/ng-select/div')
                        break
                    except Exception as exception:
                        time.sleep(1)
                        time_waited_query += 1
            time.sleep(0.1)
            state = station_list[station][0]
            state_name.click()
            time.sleep(0.1)
            state_name.send_keys(Keys.ENTER)
            time.sleep(0.1)
            select_a_drop_down_option(state_name, state)
            time.sleep(0.1)

            # Choose a city
            while True:
                try:
                    city_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[4]/div[2]/ng-select/div')
                    break
                except Exception as exception:
                    time.sleep(1)
            time.sleep(0.1)
            city = station_list[station][1]
            city_name.click()
            time.sleep(0.1)
            city_name.send_keys(Keys.ENTER)
            time.sleep(0.5)
            select_a_drop_down_option(city_name, city)
            time.sleep(0.1)

            # Choose a station
            while True:
                try:
                    station_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[5]/div[2]/ng-select/div')
                    break
                except Exception as exception:
                    time.sleep(1)
            time.sleep(0.1)
            station_name.click()
            time.sleep(0.1)
            station_name.send_keys(Keys.ENTER)
            time.sleep(0.1)
            select_a_drop_down_option(station_name, station)
            time.sleep(0.1)

            # Select Data type (Always choose Raw Data)
            while True:
                try:
                    data_type = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[1]/div[2]/ng-select/div')
                    break
                except Exception as exception:
                    time.sleep(1)
            time.sleep(0.1)
            data_type.click()
            data_type.send_keys(Keys.ENTER)
            time.sleep(0.1)
            # select_a_drop_down_option(data_type, "Raw data")

            # Choose a criteria (criteria is always "1 Hour")
            while True:
                try:
                    criteria_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[2]/div[2]/ng-select/div')
                    break
                except Exception as exception:
                    time.sleep(1)
            select_a_drop_down_option(criteria_name, "1 hour")
            # time.sleep(0.1)
            # criteria_name.click()
            # time.sleep(0.1)
            # criteria_name.send_keys(Keys.ARROW_DOWN)
            # time.sleep(0.1)
            # # criteria_name.send_keys(Keys.ARROW_UP)
            # # time.sleep(0.1)
            # # criteria_name.send_keys(Keys.ARROW_UP)
            # # time.sleep(0.1)
            # criteria_name.send_keys(Keys.ENTER)
            # time.sleep(0.1)

            # # Choose the time period for data collection
            # select_date_from(browser, start_date[0], start_date[1], start_date[2])
            # select_date_to(browser, end_date[0], end_date[1], end_date[2])
            
            # Click the submit button on the query page
            while True:
                try:
                    submit_button = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[2]/div[6]/button')
                    break
                except Exception as exception:
                    time.sleep(1)
            submit_button.click()
            
            #Download all files in the table
            # Making sure that the table is loaded
            while True:
                try:
                    download_column = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-data-repository/div[3]/table/thead/tr/th[2]')
                    break
                except Exception as exception:
                    time.sleep(1)

            # Locate all download buttons in the table using their class name
            download_buttons = browser.find_elements(By.XPATH, "//a[@title='download']")

            # Iterate through each download button and click it
            for button in download_buttons:
                button.click()
                time.sleep(1)

            # # Download the excel file
            # time_waited = 0
            # file_downloaded = False
            # while True:
            #     if time_waited >= 100:
            #         break
            #     else:
            #         try:
            #             excel_file_button = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[1]/div[2]/div/div/a[2]')
            #             excel_file_button.click()
            #             file_downloaded = True
            #             time.sleep(1)
            #             break
            #         except Exception as exception:
            #             time.sleep(1)
            #             time_waited += 1
            # if file_downloaded == False:
            #     file.write("Couldn't download data from " + station + ", " + city + ", " + state + '\n')
            
            # # Come back to the query page
            # browser.back()
        file.close()
        time.sleep(120)
    except Exception as exception:
        print("--------------------------------------")
        print("Exception in collect_data_given_parameter")
        print(exception)
        print("--------------------------------------")
        raise(exception)


# Function to get the longitude and latitude of stations
def get_lat_long(location):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": 'AIzaSyDTtC1zQZnkwLxSF9mbFEJIJ2Lalqjq5Lo'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data["status"] == "OK":
        # Extract the latitude and longitude
        result = data["results"][0]["geometry"]["location"]
        lat = result["lat"]
        lng = result["lng"]
        return_string = location + '\n' + "Latitude: " + str(lat) + " Longtitude: " + str(lng)
        return_string = return_string + '\n' + '------------------------------------' + '\n'
        return return_string
    else:
        return_string = "Couldn't get details for " + location
        return_string = return_string + '\n' + '------------------------------------' + '\n'
        return return_string

def main():
    try:
        url = "https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing"
        browser = webdriver.Chrome()
        browser.get(url)
        # Maximize the browser window
        browser.maximize_window()

        # Wait for the captcha to appear
        while True:
            try:
                browser.find_element(By.XPATH, '//*[@id="myModal"]/div/div/div[2]/div[3]/span')
                break
            except Exception as exception:
                time.sleep(1)
        time.sleep(5)

        # Wait for captcha verification to be completed
        while True:
            try:
                browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-landing/div[2]/div[1]/div[1]/div[1]').click()
                break
            except Exception as exception:
                time.sleep(1)
        
        # Switching to query window window
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[1])

        #Accessing historical data
        while True:
            try:
                browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/h1/a').click()
                break
            except Exception as exception:
                time.sleep(1)
        
        # Switching to historical data window window
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[2])

        # Collect all stations names
        global stations_state_city
        stations_state_city = collect_station_names(browser)

        #-----------------------------------------------CODE FOR DOWNLOADING LONGITUDE AND LATITUDE------------------------------------------------------------------
        # # Get the longitude and latitude of every station
        # file = open('station_geo_details.txt', 'w')
        # for station in stations_state_city:
        #     station_strp = station.split('-')[0].strip()
        #     location = station_strp + ", " + stations_state_city[station][1] + ", " + stations_state_city[station][0] + ", India"
        #     geo_details = get_lat_long(location)
        #     print(geo_details)
        #     file.write(geo_details)
        # file.close()
        #--------------------------------------------------------------------------------------------------------------------------------------------------------------

        collect_data_given_parameter(browser, stations_state_city, "historical_data.txt", "Chandni Chowk, Delhi - IITM")


        #Keeping the browser live
        while (True):
            pass

    except Exception as exception:
        raise(exception)

if __name__ == '__main__':
    main() 