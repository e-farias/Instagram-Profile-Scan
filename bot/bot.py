import glob, json
import os, datetime, time, random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys


# Driver Session!

def start_driver_headless(session_id):
    
    try:

        print("Initializing browser...")
        
        global log, driver, driver_options
        
        driver_options = Options()
        driver_options.headless = True
        driver = webdriver.Firefox(executable_path= r'{}\bot\driver\geckodriver.exe'.format(os.getcwd()), options=driver_options)
        time.sleep(10)
        
        log = {
            "session": {
                "id": session_id,
                "startDate": get_date(),
                "startTime": get_time()
            }
        }

        return print("Done")
    
    except Exception as start_driver_erro:
        
        print('\nDamn, gave error: \n', start_driver_erro)
        quit_driver(session_id)

def start_driver(session_id):
    
    try:

        print("Initializing browser...")
        
        global log, driver
        
        driver = webdriver.Firefox(
            executable_path= r'{}\bot\driver\geckodriver.exe'.format(os.getcwd())
            )
        time.sleep(10)

        log = {
            "session": {
                "id": session_id,
                "startDate": get_date(),
                "startTime": get_time()
            }
        }

        return print("Done")

    except Exception as start_driver_erro:
        
        print('\nDamn, gave error: \n', start_driver_erro)
        quit_driver(session_id)
        time.sleep(10)
        start_driver(session_id)

def quit_driver(session_id):
    
    try:
        
        driver.quit()

        log["session"].update({
            "endDate": get_date(),
            "endTime": get_time()
        })
        
        session_path = r'{}\bot\userdata\sessions\session_{}.json'.format(os.getcwd(), session_id)
        create_json(log, session_path)
        
    except Exception as quit_driver_erro:
        
        log["session"].update({
            "erro": "True",
            "erroType": str(quit_driver_erro),
            "erroLine": str(sys.exc_info()[-1].tb_lineno)
        })
        create_json(log, session_path)


# OS Session!

def get_time():
    now = datetime.datetime.now()
    return now.strftime('%H%M%S')

def get_date():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')

def create_json(dict, path):
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(dict, fp, ensure_ascii=False)
    print("The json file has been saved. See him at " + path)

def human_typing(local, text):
    for letter in text:
        local.send_keys(letter)
        time.sleep(random.randint(5,25)/30)


# Bot: Get Instagram Info

def get_open_user_followers(user):

    print("Getting followers info...")
    driver.get('https://www.instagram.com/' + user)
    time.sleep(5)

    followers_number = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
    followers_number = int(str(followers_number).replace(",", "").replace(".", ""))

    global followers, followers_users
    followers = []
    followers_users = []

    while (len(followers_users) < followers_number):

        followers_box = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
        followers_box.click()
        time.sleep(2)
        
        #Simulate the scroll
        scroll_container = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        driver.execute_script("arguments[0].scrollIntoView()", scroll_container)
        
        ht, last_ht = 1, 0
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            ht = driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_container)

        #Get users
        followers_users_element = scroll_container.find_elements_by_class_name("FPmhX")
        followers_users = [user.text for user in followers_users_element if user.text != ""]

        #Get names
        followers_names_element = scroll_container.find_elements_by_class_name("wFPL8")
        followers_names = [name.text for name in followers_names_element]

        #Get profiles photos
        followers_profile_photos_element = scroll_container.find_elements_by_xpath("//li[@class='wo9IH']//img[@class='_6q-tv']")
        followers_profile_photos = [photo.get_attribute("src") for photo in followers_profile_photos_element if photo.get_attribute("src") != ""]

        followers_box_close = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")
        followers_box_close.click()

    #Add data on the followers list
    for (user, name, photo) in zip(followers_users, followers_names, followers_profile_photos):
        
        followers.append({
            "user": user,
            "name": name,
            "profile_photo_url": photo
        })
    
    print("Done")

def get_open_user_following(user):

    print("Getting following info...")
    driver.get('https://www.instagram.com/' + user)
    time.sleep(5)

    following_number = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text
    following_number = int(str(following_number).replace(",", "").replace(".", ""))

    global followings, following_users
    followings = []
    following_users = []
    
    while (len(following_users) < following_number):
        
        following_box = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_box.click()
        time.sleep(2)
        
        #Simulate the scroll
        scroll_container = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        driver.execute_script("arguments[0].scrollIntoView()", scroll_container)
        
        ht, last_ht = 1, 0
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            ht = driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_container)
        
        #Get users
        following_users_element = scroll_container.find_elements_by_class_name("FPmhX")
        following_users = [follower.text for follower in following_users_element if follower.text != ""]

        #Get names
        following_names_element = scroll_container.find_elements_by_class_name("wFPL8")
        following_names = [name.text for name in following_names_element]

        #Get profiles photos
        following_profile_photos_element = scroll_container.find_elements_by_xpath("//li[@class='wo9IH']//img[@class='_6q-tv']")
        following_profile_photos = [photo.get_attribute("src") for photo in following_profile_photos_element if photo.get_attribute("src") != ""]

        following_box_close = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")
        following_box_close.click()

    #Add data on the following list
    for (user, name, photo) in zip(following_users, following_names, following_profile_photos):
        
        followings.append({
            "user": user,
            "name": name,
            "profile_photo_url": photo
        })

    print("Done")

def get_open_user_profile_info(user):
    
    # Measuring time: Start
    hours_start = int(datetime.datetime.now().strftime('%H'))
    minutes_start = int(datetime.datetime.now().strftime('%M'))
    seconds_start = int(datetime.datetime.now().strftime('%S'))
    
    print("Scanning @"+user+" profile...")
    driver.get('https://www.instagram.com/'+user)
    time.sleep(5)

    # Make sure the user is open
    try:
        pritave_msg = driver.find_element_by_class_name("QlxVY")
        print("This profile is not open for scanning. :(")
        return False
    except:
        pass

    # Find the elements
    followers_number = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
    followers_number = str(followers_number).replace(',', '')
    following_number = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text
    following_number = str(following_number).replace(',', '')
    post_number = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text
    name = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/h1").text
    
    try:
        #Profile public class
        profile_photo_url = driver.find_element_by_xpath("//img[@class='_6q-tv']").get_attribute("src")
    except:
        #Profile private class
        profile_photo_url = driver.find_element_by_xpath("//img[@class='be6sR']").get_attribute("src")

    try:
        bio = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/span").text
        bio = str(bio).replace('\n', ' ')
    except:
        bio = None

    get_open_user_followers(user)
    get_open_user_following(user)

    mutual_followers = [x for x in set(followers_users) if x in set(following_users)]
    my_fans = [x for x in set(followers_users) if x not in set(following_users)]
    my_idols = [x for x in set(following_users) if x not in set(followers_users)]

    # Measuring time: End
    hours_end = int(datetime.datetime.now().strftime('%H'))
    minutes_end = int(datetime.datetime.now().strftime('%M'))
    seconds_end = int(datetime.datetime.now().strftime('%S'))
    duration = '{}h{}m{}s'.format(int(hours_end-hours_start), int(minutes_end-minutes_start), int(seconds_end-seconds_start))

    # Save the data to a json file
    print('Saving the data to a json file...')
    profile_info = {
        "user": user,
        "name": name,
        "post_number": post_number,
        "bio": bio,
        "profile_photo_url": profile_photo_url,
        "scan_duration": duration,
        "followers_number": followers_number,
        "following_number": following_number,
        "followers": followers,
        "followings": followings,
        "mutual_followers": mutual_followers,
        "my_fans": my_fans,
        "my_idols": my_idols,
        "mutual_followers_number": str(len(mutual_followers)),
        "my_fans_number": str(len(my_fans)),
        "my_idols_number": str(len(my_idols))
    }
    path = r'{}\bot\userdata\scans\scan_{}_{}{}.json'.format(os.getcwd(), user, get_date(), get_time())
    create_json(profile_info, path)

    print("Done")


# Bot: Login

def login(user, password):
    
    try:

        print("Initializing login...")
        
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)
        
        input_username = driver.find_element_by_xpath("//input[@name='username']")
        input_password = driver.find_element_by_xpath("//input[@name='password']")

        human_typing(input_username, user)
        human_typing(input_password, password)

        button_login = driver.find_element_by_xpath("//button[@type='submit']")
        button_login.click()
        time.sleep(7)
        
        #Create the log
        log.update({
            "login": {
                "user": user,
                "date": get_date(),
                "time": get_time(),
                "notificationsScreen": str(deny_notifications())
            }
        })
        
        print("Done")
        return True
    
    except Exception as login_erro:

        #Create the log
        log.update({
            "login": {
                "user": user,
                "date": get_date(),
                "time": get_time(),
                "erro": "True",
                "erroLine": str(sys.exc_info()[-1].tb_lineno),
                "typeErro": str(login_erro)
            }
        })
        print("Damn, there was an error in 'login': \n", login_erro)

        return False

def deny_notifications():
    
    try:
        
        button_not_now = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]/button[2]')
        button_not_now.click()
        time.sleep(2)
        
        return True
    
    except Exception:
        
        return False
