import requests
import sys

# Instructions after function definitions.

def doGet(url, parameters, authentication, headers):
    return requests.get(url, params=parameters, auth=authentication, headers=headers)

def getAuthToken():
    params = {"grant_type" : "client_credentials"}
    # Setup here your Client ID
    user = ""
    # Setup here your Client Secret
    pwd = ""
    auth = (user, pwd)
    r = doGet("https://us.battle.net/oauth/token", params, auth, None)
    if r.status_code != 200:
        print(r.status_code)
        print(r.json)
        return None
    else:
        return r.json()["access_token"]

def getStatistics(realm, character, token):
    params = {"namespace" : "profile-us"}
    url = "https://us.api.blizzard.com/profile/wow/character/" + realm + "/" + character + "/achievements/statistics"
    headers = {"Authorization" : "Bearer " + token}
    r = doGet(url, params, None, headers)
    if r.status_code != 200:
        print(r.status_code)
        print(r.json())
        return None
    else:
        return r.json()

def getEncountersCount(realm, character, token):
    r = getStatistics(realm, character, token)
    if r == None:
        return
    for sub in r["categories"]:
        if sub["id"] == 14807:
            raids = sub
            break
    for sub in raids["sub_categories"]:
        for stat in sub["statistics"]:
            if stat["id"] in d:
                d[stat["id"]][1] += stat["quantity"]

def getPossibleIds(realm, character, search, token):
    res = {}
    r = getStatistics(realm, character, token)
    if r == None:
        return res
    for sub in r["categories"]:
        if sub["id"] == 14807:
            raids = sub
            break
    for sub in raids["sub_categories"]:
        for stat in sub["statistics"]:
            if search in stat["name"]["en_US"]:
                res[stat["id"]] = stat["name"]["en_US"]
    return res

# Put in this list the characters you want to check statistics (names in lowercase).
lsitOfCharacters = ["character1", "character2", "character3"]
# Put in this dict (int : list) the events you want to check for, key is the integer id, first element of the list is the description (unused, only for clarity),
# second list element is the count, set it to 0. Three examples are provided.
d = {1088 : ["Kael'thas Sunstrider kills (Tempest Keep)", 0],
     4688 : ["Victories over the Lich King (Heroic Icecrown 25 player)", 0],
     1098 : ["Onyxia kills (Onyxia's Lair)", 0]
}
n = len(sys.argv)
# Call without arguments, the program gives you the result for the data provided in "listOfCharacters", "d" and the realm set a couple lines under.
# Example: py blizz.py
if n == 1:
    token = getAuthToken()
    for character in lsitOfCharacters:
        # Set the realm in the first argument (all lowercase)
        getEncountersCount("", character, token)
    print(d)
# Next two options are meant to provide a way to look for the id of the event to use in the previous dict "d"
# Call with one argument, the word to look for, case sensitive. The character and realm are the defaults configured below.
# Example: py blizz.py Onyxia
elif n == 2:
    token = getAuthToken()
    # Set up here default realm (first argument, lowercase) and character (second argument, lowercase).
    print(getPossibleIds("", "", sys.argv[1], token))
# Call with three arguments, same as previous option, but you provide realm (lowercase first argument), character(lowercase first argument)
# and search word(case sensitive, thirs argument) in command line arguments.
# py blizz.py myrealm mycharacter Onyxia
elif n == 4:
    token = getAuthToken()
    print(getPossibleIds(sys.argv[1], sys.argv[2], sys.argv[3], token))
else:
    print("Invalid arguments")