import requests
import json
from urllib import parse
import time

# class get:
class riot_api_utils:
    # initialize
    # api_key: string, riot api key
    def __init__(self, api_key):
        self.REQUEST_HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": api_key
        }
        self.req_count = 0

    # request timer
    def request_timer(self):
        self.req_count += 1
        if self.req_count % 100 == 0:
            time.sleep(120)
        else:
            time.sleep(1)

    # get me info
    def get_me(self):
        self.request_timer()
        url = "https://kr.api.riotgames.com/lol/summoner/v4/me"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        response = response.json()

        # error control
        if 'status' in response:
            print(response['status']['message'])
            return None
        else:
            return response
    # get high rank summoner list
    def get_challenger_list(self):
        self.request_timer()
        url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        response = response.json()

        # error control
        if 'status' in response:
            print(response['status']['message'])
            return None
        else:
            return response['entries']
    def get_grandmaster_list(self):
        self.request_timer()
        url = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        response = response.json()

        # error control
        if 'status' in response:
            print(response['status']['message'])
            return None
        else:
            return response['entries']
    def get_master_list(self):
        self.request_timer()
        url = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        response = response.json()

        # error control
        if 'status' in response:
            print(response['status']['message'])
            return None
        else:
            return response['entries']
    
    # get puuid from encryptedSummonerId
    def get_puuid(self, encryptedSummonerId):
        self.request_timer()
        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/{encryptedSummonerId}"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        response = response.json()

        # error control
        if 'status' in response:
            print(response['status']['message'])
            return None
        else:
            return response['puuid']
    
    # get solo rank match list
    def get_match_list(self, puuid, count):
        self.request_timer()
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&queue=420"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        response = response.json()

        # error control
        if 'status' in response:
            print(response['status']['message'])
            return None
        else:
            return response
    # get match info
    def get_match(self, match_id):
        self.request_timer()
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        response = response.json()

        # error control
        if 'status' in response:
            print(response['status']['message'])
            return None
        else:
            return response
    # get match timeline info
    def get_match_timeline(self, match_id):
        self.request_timer()
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        response = response.json()

        # error control
        if 'status' in response:
            print(response['status']['message'])
            return None
        else:
            return response