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

def select_date_from(browser, wanted_day, wanted_month, wanted_year):
    try:
        date_box = browser.find_element(By.XPATH, '//*[@id="date"]') 
        # current_date = re.sub(r'[✕▼]', '', date_box.get_attribute("innerText")).strip().replace("24:00", "00:00")
        # current_date = datetime.strptime(current_date, '%d-%b-%Y %H:%M')
        # current_date_array = [current_date.strftime('%d'), current_date.strftime('%b'),
        #                     current_date.strftime('%Y'), current_date.strftime('%H'),
        #                     current_date.strftime('%M')]
        # print("-----------------------------------------")
        # print(current_date_array)
        # print("-----------------------------------------")
        date_box.click()
        current_year = browser.find_element(By.XPATH, '//*[@id="date"]/angular2-date-picker/div/div[2]/div[3]/div')
        current_year.click()
        years_view = browser.find_element(By.CLASS_NAME, "years-view")
        prev_button = years_view.find_element(By.CLASS_NAME, "fa-angle-left")
        next_button = years_view.find_element(By.CLASS_NAME, "fa-angle-right")
        if current_year.text.strip() != wanted_year:
            while True:
                years_elements = browser.find_elements(By.CSS_SELECTOR, ".years-list-view span")
                list_of_years_on_display = [year.text for year in years_elements]
                # print (list_of_years_on_display)
                # print(wanted_year)
                # print(int(list_of_years_on_display[0]))
                if wanted_year < int(list_of_years_on_display[0]):
                    prev_button.click()
                elif wanted_year > int(list_of_years_on_display[len(list_of_years_on_display) - 1]):
                    next_button.click()
                else:
                    break
            year_button = browser.find_element(By.ID, wanted_year)
            time.sleep(0.1)
            year_button.click()

        current_month = browser.find_element(By.XPATH, '//*[@id="date"]/angular2-date-picker/div/div[2]/div[2]/div')
        # print(current_month.text.strip())
        if current_month != wanted_month:
            month_id = wanted_month[:3].upper()
            current_month.click()
            time.sleep(0.1)
            month_button = browser.find_element(By.ID, month_id)
            time.sleep(0.1)
            month_button.click()
        
        all_dates = browser.find_element(By.CLASS_NAME, "calendar-days")
        rows_in_all_dates = all_dates.find_elements(By.TAG_NAME, "tr")
        for row in rows_in_all_dates:
            dates = row.find_elements(By.TAG_NAME, "td")
            for date in dates:
                date_content = date.text.strip()
                if date_content:          
                    if int(date_content) == wanted_day:
                        date.click()
        # print("----------------------------------------------------")
    except Exception as exception:
        print("--------------------------------------")
        print("Exception in select_date_from")
        print(exception)
        print("--------------------------------------")
        raise(exception)

def select_date_to(browser, wanted_day, wanted_month, wanted_year):
    try:
        date_box = browser.find_element(By.XPATH, '//*[@id="date2"]') 
        # current_date = re.sub(r'[✕▼]', '', date_box.get_attribute("innerText")).strip().replace("24:00", "00:00")
        # current_date = datetime.strptime(current_date, '%d-%b-%Y %H:%M')
        # current_date_array = [current_date.strftime('%d'), current_date.strftime('%b'),
        #                     current_date.strftime('%Y'), current_date.strftime('%H'),
        #                     current_date.strftime('%M')]
        # print("-----------------------------------------")
        # print(current_date_array)
        # print("-----------------------------------------")
        date_box.click()
        current_year = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[3]/div')
        current_year.click()
        years_view = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[5]')
        prev_button = years_view.find_element(By.CLASS_NAME, "fa-angle-left")
        next_button = years_view.find_element(By.CLASS_NAME, "fa-angle-right")
        if current_year.text.strip() != wanted_year:
            while True:
                years_elements = browser.find_elements(By.CSS_SELECTOR, ".years-list-view span")
                list_of_years_on_display = [year.text for year in years_elements]
                # print (list_of_years_on_display)
                # print(list_of_years_on_display[len(list_of_years_on_display) - 1])
                # print(wanted_year)
                # print(int(list_of_years_on_display[0]))
                if wanted_year < int(list_of_years_on_display[0]):
                    prev_button.click()
                elif wanted_year > int(list_of_years_on_display[len(list_of_years_on_display) - 1]):
                    next_button.click()
                else:
                    break
            year_button = browser.find_element(By.ID, wanted_year)
            time.sleep(1)
            year_button.click()

        current_month = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[2]/div')
        # print(current_month.text.strip())
        months = {"JAN": '(//*[@id="JAN"])[2]',
                  "FEB": '(//*[@id="FEB"])[2]',
                  "MAR": '(//*[@id="MAR"])[2]',
                  "APR": '(//*[@id="APR"])[2]',
                  "MAY": '(//*[@id="MAY"])[2]',
                  "JUN": '(//*[@id="JUN"])[2]',
                  "JUL": '(//*[@id="JUL"])[2]',
                  "AUG": '(//*[@id="AUG"])[2]',
                  "SEP": '(//*[@id="SEP"])[2]',
                  "OCT": '(//*[@id="OCT"])[2]',
                  "NOV": '(//*[@id="NOV"])[2]',
                  "DEC": '(//*[@id="DEC"])[2]'}
        if current_month != wanted_month:
            month_id = wanted_month[:3].upper()
            month_id + "[2]"
            current_month.click()
            time.sleep(0.1)
            month_button = browser.find_element(By.XPATH, months[month_id])
            time.sleep(1)
            month_button.click()
        
        all_dates = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/table[2]')
        rows_in_all_dates = all_dates.find_elements(By.TAG_NAME, "tr")
        for row in rows_in_all_dates:
            dates = row.find_elements(By.TAG_NAME, "td")
            for date in dates:
                date_content = date.text.strip()
                if date_content:          
                    if int(date_content) == wanted_day:
                        date.click()

        # Setting the time to midnight (12:00 AM)
        date_box.click()
        time.sleep(1)
        time_setter = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[1]/div[4]/div')
        time.sleep(1)
        time_setter.click()
        hour_plus_button = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[5]/div[1]/div[1]/span[1]')
        time.sleep(1)
        for i in range (0, 13):
            hour_plus_button.click()
            i += 1
            time.sleep(0.1)
        minute_minus_button = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[5]/div[1]/div[3]/span[2]')
        time.sleep(2)
        for i in range (0, 61):
            minute_minus_button.click()
            i += 1
            time.sleep(0.5)
        AM_button = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[5]/div[2]/div/button[1]')
        time.sleep(0.5)
        AM_button.click()

        set_time_button = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[5]/div[3]/button')
        time.sleep(0.5)
        set_time_button.click()
        time.sleep(0.5)
        done_button = browser.find_element(By.XPATH, '//*[@id="date2"]/angular2-date-picker/div/div[2]/div[6]/div')
        time.sleep(0.5)
        done_button.click()
    
    except Exception as exception:
        print("--------------------------------------")
        print("Exception in select_date_to")
        print(exception)
        print("--------------------------------------")
        raise(exception)

def collect_data_given_parameter(browser, station_list, parameter_xpath, start_date, end_date, output_file_name, desired_parameter, start_station):
    try:
        # Create an output file
        file = open(output_file_name, 'w')

        # Initiate a new window every time this function is called
        browser = webdriver.Chrome()
        browser.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing')
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
            
            print(station, station_list[station][1], station_list[station][0])
            # Choose a state
            time_waited_query = 0
            while True:
                if time_waited_query >= 100:
                    print("Restarted the window, starting again from station: " + station + ", " + stations_state_city[station][1] + ", "
                      + stations_state_city[station][0])
                    browser.quit()
                    browser = webdriver.Chrome()
                    browser.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing')
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
                    # Identify the state_name drop down
                    while True:
                        try:
                            state_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[1]/div/ng-select/div')
                            break
                        except Exception as exception:
                            time.sleep(1)
                    break
                else:
                    try:
                        state_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[1]/div/ng-select/div')
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
                    city_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[2]/div/ng-select/div')
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
                    station_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[1]/div/ng-select/div')
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

            # Choose a parameter
            while True:
                try:
                    parameters_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div')
                    break
                except Exception as exception:
                    time.sleep(1)
            time.sleep(0.1)
            parameters_name.click()
            time.sleep(0.1)

            # make sure that the curren station has the desired parameter
            try: 
                parameter = browser.find_element(By.XPATH, parameter_xpath)
                time.sleep(0.5)
            except Exception as exception:
                file.write("Couldn't download data from " + station + ", " + city + ", " + state + '\n')
                browser.refresh()
                continue
            time.sleep(0.1)
            parameter.click()
            
            # Make sure that the selected parameter is the desired parameter
            selected_parameter = re.sub(r'[✕▼]', '', parameters_name.get_attribute("innerText")).strip()
            selected_parameter = selected_parameter.strip().split('\n')[0]
            if selected_parameter != desired_parameter:
                print("Selected parameter: " + selected_parameter, "Desired parameter: " + desired_parameter)
                file.write("Couldn't download data from " + station + ", " + city + ", " + state + '\n')
                browser.refresh()
                continue
            
            # Choose a report format (Report format is always tabular)
            while True:
                try:
                    report_format_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[3]/div[1]/div/ng-select/div')
                    break
                except Exception as exception:
                    time.sleep(1)
            report_format_name.click()
            time.sleep(0.1)
            report_format_name.send_keys(Keys.ENTER)
            time.sleep(0.1)

            # Choose a criteria (criteria is always "1 Hour")
            while True:
                try:
                    criteria_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[3]/div[2]/div/ng-select/div')
                    break
                except Exception as exception:
                    time.sleep(1)
            time.sleep(0.1)
            criteria_name.click()
            time.sleep(0.1)
            criteria_name.send_keys(Keys.ARROW_UP)
            time.sleep(0.1)
            criteria_name.send_keys(Keys.ARROW_UP)
            time.sleep(0.1)
            criteria_name.send_keys(Keys.ARROW_UP)
            time.sleep(0.1)
            criteria_name.send_keys(Keys.ENTER)
            time.sleep(0.1)

            # Choose the time period for data collection
            select_date_from(browser, start_date[0], start_date[1], start_date[2])
            select_date_to(browser, end_date[0], end_date[1], end_date[2])
            
            # Click the submit button on the query page
            while True:
                try:
                    submit_button = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[5]/button')
                    break
                except Exception as exception:
                    time.sleep(1)
            submit_button.click()

            # Download the excel file
            time_waited = 0
            file_downloaded = False
            while True:
                if time_waited >= 100:
                    break
                else:
                    try:
                        excel_file_button = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[1]/div[2]/div/div/a[2]')
                        excel_file_button.click()
                        file_downloaded = True
                        time.sleep(1)
                        break
                    except Exception as exception:
                        time.sleep(1)
                        time_waited += 1
            if file_downloaded == False:
                file.write("Couldn't download data from " + station + ", " + city + ", " + state + '\n')
            
            # Come back to the query page
            browser.back()
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
        # Acces the data query page
        url = "https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing"
        browser = webdriver.Chrome()
        browser.get(url)
        # time.sleep(30)
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
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[1])
        # print("-------------------------------------")
        # print(browser.current_url)
        # print("-------------------------------------")

        # Collecting all state names and put them in an array
        while True:
            try:
                state_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[1]/div/ng-select/div')
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
                    city_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[2]/div/ng-select/div')
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
        global stations_state_city
        stations_state_city = {}
        for state in list_of_state_names:
            select_a_drop_down_option(state_name, state)
            while True:
                try:
                    city_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[2]/div/ng-select/div')
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
                        station_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[1]/div/ng-select/div')
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

        #-----------------------------------------------CODE FOR DOWNLOADING LONGITUDE AND LATITUDE------------------------------------------------------------------
        # Get the longitude and latitude of every station
        file = open('station_geo_details.txt', 'w')
        for station in stations_state_city:
            station_strp = station.split('-')[0].strip()
            location = station_strp + ", " + stations_state_city[station][1] + ", " + stations_state_city[station][0] + ", India"
            geo_details = get_lat_long(location)
            print(geo_details)
            file.write(geo_details)
        file.close()
        #--------------------------------------------------------------------------------------------------------------------------------------------------------------

        global parameters_xpath
        parameters_xpath = {"PM2.5": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[1]',
                            "PM10": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[2]',
                            "NO": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[3]',
                            "NO2": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[4]',
                            "NOx": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[5]',
                            "NH3": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[6]',
                            "SO2": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[7]',
                            "CO": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[8]',
                            "Ozone": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[9]',
                            "Benzene": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[10]',
                            "Toluene": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[11]',
                            "Eth-Benzene": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[12]',
                            "MP-Xylene": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[13]',
                            "Xylene": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[14]',
                            "RH": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[15]',
                            "WS": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[16]',
                            "WD": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[17]',
                            "SR": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[18]',
                            "BP": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[19]',
                            "Xylene": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[20]',
                            "AT": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[21]',
                            "TOT-RF": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[22]',
                            "RF": '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[23]'}
        browser.quit()

        #----------------------------------------------CODE FOR DOWNLOADING DATA FROM THE WEBSITE------------------------------------------------------------------------------------
        global start_date
        global end_date
        start_date = [1, "January", 2015]
        end_date = [1, "July", 2023]

        collect_data_given_parameter(browser, stations_state_city, parameters_xpath["PM2.5"], start_date, end_date, "PM25.txt", "PM2.5", None)
        print("Collected data for PM2.5")
        collect_data_given_parameter(browser, stations_state_city, parameters_xpath["PM10"], start_date, end_date, "PM10.txt", "PM10", None)
        print("Collected data for PM10")
        collect_data_given_parameter(browser, stations_state_city, parameters_xpath["Ozone"], start_date, end_date, "Ozone.txt", "Ozone", None)
        print("Collected data for Ozone")
        collect_data_given_parameter(browser, stations_state_city, parameters_xpath["NO2"], start_date, end_date, "NO2.txt", "NO2", None)
        print("Collected data for NO2")
        collect_data_given_parameter(browser, stations_state_city, parameters_xpath["SO2"], start_date, end_date, "SO2.txt", "SO2", None)
        print("Collected data for SO2")
        collect_data_given_parameter(browser, stations_state_city, parameters_xpath["CO"], start_date, end_date, "CO.txt", "CO", None)
        print("Collected data for CO")
        collect_data_given_parameter(browser, stations_state_city, parameters_xpath["NH3"], start_date, end_date, "NH3.txt", "NH3", None)
        print("Collected data for NH3")
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #-----------------------------------------------DRAFT CODE, PLEASE DISREGARD AND KEEP INTACT----------------------------------------------------------------------------------
        # PM25_process = multiprocessing.Process(target = collect_data_given_parameter, args=[browser, stations_state_city, parameters_xpath["PM2.5"], start_date, end_date])
        # PM25_process.start()

        # PM25_process.join()

        # # Retrieving data for PM2.5 for all stattions:
        # for state in list_of_state_names:
        #     select_a_drop_down_option(state_name, state)
        #     city_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[2]/div/ng-select/div')
        #     associated_cities = states_and_cities[state]
        #     for city in associated_cities:
        #         city_name.click()
        #         time.sleep(0.1)
        #         city_name.send_keys(Keys.ARROW_DOWN)
        #         time.sleep(0.1)
        #         city_name.send_keys(Keys.ENTER)
        #         select_a_drop_down_option(city_name, city)
        #         time.sleep(0.1)

        # while True:
        #     try:
        #         state_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[1]/div/ng-select/div')
        #         break
        #     except Exception as exception:
        #         time.sleep(1)
        # time.sleep(0.1)
        # state_name.click()
        # time.sleep(0.1)
        # state_name.send_keys(Keys.ENTER)
        # time.sleep(0.1)

        # city_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[1]/div[2]/div/ng-select/div')
        # time.sleep(0.1)
        # city_name.click()
        # time.sleep(0.1)
        # city_name.send_keys(Keys.ENTER)
        # time.sleep(0.1)

        # station_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[1]/div/ng-select/div')
        # time.sleep(0.1)
        # station_name.click()
        # time.sleep(0.1)
        # station_name.send_keys(Keys.ENTER)

        # parameters_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div')
        # time.sleep(0.1)
        # parameters_name.click()
        # time.sleep(0.1)
        # PM25 = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[1]')
        # time.sleep(0.1)
        # PM25.click()
        # toluene = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[2]/div[2]/div/div/multi-select/angular2-multiselect/div/div[2]/div[2]/ul/li[11]')
        # time.sleep(0.1)
        # toluene.click()
        # time.sleep(0.1)

        # report_formate_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[3]/div[1]/div/ng-select/div')
        # report_formate_name.click()
        # time.sleep(0.1)
        # report_formate_name.send_keys(Keys.ENTER)
        # time.sleep(0.1)

        # criteria_name = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[3]/div[2]/div/ng-select/div')
        # reset_drop_down(criteria_name, "15 Minute")
        # time.sleep(0.1)
        # select_a_drop_down_option(criteria_name, "1 Hour")

        # select_date_from(browser, 1, "January", 2015)
        # select_date_to(browser, 1, "July", 2023)
        
        # # Click the submit button:
        # submit_button = browser.find_element(By.XPATH, '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data/div/div/div[5]/button')
        # submit_button.click()

        while (True):
            pass
    except Exception as exception:
        print("-------------------------------------")
        print(exception)
        print("-------------------------------------")
        raise(exception)

if __name__ == '__main__':
    main() 