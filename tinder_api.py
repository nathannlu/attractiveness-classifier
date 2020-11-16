import requests
import datetime
from time import sleep
from time import time

TINDER_URL="https://api.gotinder.com"

class tinderAPI():

    def __init__(self, token):
        self._token = token

    def profile(self):
        url = TINDER_URL + "/v2/profile?include=account%2Cuserf"
        data = requests.get(url, headers={"X-Auth-Token": self._token}).json()
        return Profile(data["data"], self)

    def matches(self, limit=10):
        url = TINDER_URL + f"/v2/matches?count={limit}"
        data = requests.get(url, headers={"X-Auth-Token": self._token}).json()
        return list(map(lambda match: Person(match["person"], self), data["data"]["matches"]))

    def like(self, user_id):
        url = TINDER_URL + f"/like/{user_id}"
        data = requests.get(url, headers={"X-Auth-Token": self._token}).json()
        return {
            "is_match": data["match"],
            "likes_remaining": data["likes_remaining"]
        }

    def dislike(self, user_id):
        url = TINDER_URL + f"/pass/{user_id}"
        requests.get(url, headers={"X-Auth-Token": self._token}).json()
        return True

    def nearby_persons(self):
        url = TINDER_URL + "/v2/recs/core"
        data = requests.get(url, headers={"X-Auth-Token": self._token}).json()
        return list(map(lambda user: Person(user["user"], self), data["data"]["results"]))


class Person(object):

    def __init__(self, data, api):
        self._api = api

        self.id = data["_id"]
        self.name = data.get("name", "Unknown")

        self.bio = data.get("bio", "")
        self.distance = data.get("distance_mi", 0) / 1.60934

        self.birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            "birth_date", False) else None
        self.gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]

        self.images = list(map(lambda photo: photo["url"], data.get("photos", [])))

        self.jobs = list(
            map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")}, data.get("jobs", [])))
        self.schools = list(map(lambda school: school["name"], data.get("schools", [])))

        if data.get("pos", False):
            self.location = geolocator.reverse(f'{data["pos"]["lat"]}, {data["pos"]["lon"]}')

    def __repr__(self):
        return f"{self.id} - {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"


    def like(self):
        return self._api.like(self.id)

    def dislike(self):
        return self._api.dislike(self.id)

    def download_images(self):
        return(self.images)
        


class Profile(Person):

    def __init__(self, data, api):

        super().__init__(data["user"], api)

        self.email = data["account"].get("email")
        self.phone_number = data["account"].get("account_phone_number")

        self.age_min = data["user"]["age_filter_min"]
        self.age_max = data["user"]["age_filter_max"]

        self.max_distance = data["user"]["distance_filter"]
        self.gender_filter = ["Male", "Female"][data["user"]["gender_filter"]]

