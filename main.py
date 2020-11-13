import json, os
import screens
from bot import bot

session_id = "{}{}".format(bot.get_date(), bot.get_time())
bot.start_driver_headless(session_id)
path_user_data = r"{}\bot\userdata\user.json".format(os.getcwd())

# Log in
if os.path.exists(path_user_data) == True:
    
    with open(path_user_data, "r", encoding="utf-8") as fp:
        user_data = json.load(fp)

# Sign Up
else:

    print("========== Sign Up ==========")
    user = str(input("User: "))
    password = str(input("Password: "))

    user_data = {
        "user": user,
        "password": password
    }

    with open(path_user_data, "w", encoding="utf-8") as fp:
        json.dump(user_data, fp, ensure_ascii=False)
    print("A new user has been registered. See him at " + path_user_data)

# Start Bot
bot.login(user_data["user"], user_data["password"])

# Features
while True:

    options = screens.features()

    # Exit
    if options == 0:
        bot.quit_driver(session_id)
        break
    
    # Scan my profile
    if options == 1:
        bot.get_open_user_profile_info(user_data["user"])

    # Scan another profile
    if options == 2:
        another_user = str(input("User: "))
        bot.get_open_user_profile_info(another_user)
