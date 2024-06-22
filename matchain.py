import requests
import urllib.parse
import json
from datetime import datetime
import time
from colorama import Fore, Style

LoginHeaders = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Content-Length": "431",
    "Content-Type": "application/json",
    "Origin": "https://tgapp.matchain.io",
    "Pragma": "no-cache",
    "Priority": "u=1, i",
    "Referer": "https://tgapp.matchain.io/",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

LoginUrl = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/login'
ProfileUrl = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/profile'
CheckRewardsUrl = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward'
ClaimMining = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim'
StartMiningUrl = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming'
ListTaskUrl = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/list'
CompleteTaskUrl = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/complete'
ClaimTaskUrl = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/claim'
CheckTiket = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/rule'
PlayGame = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/play'
ClaimGame = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/claim'

def read_init_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def get_headers(token):
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": token,
        "Cache-Control": "no-cache",
        "Content-Length": "431",
        "Content-Type": "application/json",
        "Origin": "https://tgapp.matchain.io",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://tgapp.matchain.io/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

def get_headers_game(token):
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": token,
        "Content-Type": "application/json",
        "Origin": "https://tgapp.matchain.io",
        "Priority": "u=1, i",
        "Referer": "https://tgapp.matchain.io/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

def convert_seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def main():
    query_data_list = read_init_data('initdata.txt')
    akun = 1
    total_accounts = len(query_data_list)
    print(f"\n\n{Fore.CYAN+Style.BRIGHT}==============Menemukan {total_accounts} akun=================\n")

    auto_tasks = input("Auto claim Task? Y/N: ").strip().upper()
    auto_play_game = input("Auto play game? Y/N: ").strip().upper()

    while True:
        for query_data in query_data_list:
            print(f"\n\n{Fore.CYAN+Style.BRIGHT}==============Akun {akun}=================\n")
            akun += 1
            parsed_query = urllib.parse.parse_qs(query_data)

            if 'user' in parsed_query:
                user_json = parsed_query['user'][0]
                user_data = json.loads(user_json)

                user_info = {
                    "first_name": user_data.get('first_name', ''),
                    "last_name": user_data.get('last_name', ''),
                    "username": user_data.get('username', ''),
                    "uid": user_data.get('id', ''),
                    "tg_login_params": query_data
                }

                user_info_json = json.dumps(user_info)

                response = requests.post(LoginUrl, headers=LoginHeaders, data=user_info_json)

                if response.status_code == 200:
                    response_data = response.json()
                    token = response_data.get('data', {}).get('token')
                    if token:

                        profile_headers = get_headers(token)
                        profile_data = {
                            "uid": user_data.get('id', '')
                        }
                        profile_response = requests.post(ProfileUrl, headers=profile_headers, json=profile_data)

                        if profile_response.status_code == 200:
                            profile_data = profile_response.json().get('data', {})
                            print(f"{Fore.BLUE}[ Profile ] : Nickname: {profile_data.get('Nickname')}")
                            balance = profile_data.get('Balance', 0)
                            formatted_balance = "{:,.3f}".format(balance / 1000)
                            print(f"{Fore.BLUE}[ Profile ] : Balance: {formatted_balance}")
                        else:
                            print(f"{Fore.RED}[ Profile ] : Profile request failed: {profile_response.status_code}, {profile_response.text}")

                        check_rewards_response = requests.post(CheckRewardsUrl, headers=profile_headers, json=profile_data)

                        if check_rewards_response.status_code == 200:
                            check_rewards_data = check_rewards_response.json().get('data', {})
                            reward = check_rewards_data.get('reward', 0)
                            next_claim_timestamp = check_rewards_data.get('next_claim_timestamp', 0)

                            now_timestamp = datetime.now().timestamp() * 1000
                            time_remaining_ms = max(0, next_claim_timestamp - now_timestamp)

                            seconds_remaining = int(time_remaining_ms / 1000)
                            hours, minutes, seconds = convert_seconds_to_hms(seconds_remaining)

                            print(f"{Fore.MAGENTA}[ Rewards ] : Reward: {reward}")
                            print(f"{Fore.MAGENTA}[ Rewards ] : Next Claim Time: {hours} hours, {minutes} minutes, {seconds} seconds")

                            if (time_remaining_ms == 0 and reward == 0):
                                start_mining_response = requests.post(StartMiningUrl, headers=profile_headers, json=profile_data)

                                if start_mining_response.status_code == 200:
                                    print(f"{Fore.GREEN}[ Mining ] : Memulai mining")
                                else:
                                    print(f"{Fore.RED}[ Mining ] : Mining gagal")
                            elif time_remaining_ms == 0 and reward > 0:
                                claim_mining = requests.post(ClaimMining, headers=profile_headers, json=profile_data)
                                if claim_mining.status_code == 200:
                                    print(f"{Fore.GREEN}[ Mining ] : Berhasil claim mining")
                                    start_mining_response = requests.post(StartMiningUrl, headers=profile_headers, json=profile_data)

                                    if start_mining_response.status_code == 200:
                                        print(f"{Fore.GREEN}[ Mining ] : Memulai mining kembali")
                                    else:
                                        print(f"{Fore.RED}[ Mining ] : Gagal memulai mining kembali")
                                else:
                                    print(f"{Fore.RED}[ Mining ] : Gagal claim mining")
                            else:
                                print(f"{Fore.YELLOW}[ Mining ] : Mining sedang berjalan")

                            if auto_tasks == 'Y':
                                list_task_response = requests.post(ListTaskUrl, headers=profile_headers, json=profile_data)

                                if list_task_response.status_code == 200:
                                    task_list = list_task_response.json().get('data', [])
                                    for task in task_list:

                                        if not task['complete']:
                                            complete_task_data = {
                                                "uid": user_data.get('id', ''),
                                                "type": task['name']
                                            }
                                            complete_task_response = requests.post(CompleteTaskUrl, headers=profile_headers, json=complete_task_data)

                                            if complete_task_response.status_code == 200:

                                                complete_task_result = complete_task_response.json().get('data', False)
                                                if complete_task_result:
                                                    time.sleep(2)
                                                    claim_task_data = {
                                                        "uid": user_data.get('id', ''),
                                                        "type": task['name']
                                                    }
                                                    claim_task_response = requests.post(ClaimTaskUrl, headers=profile_headers, json=claim_task_data)

                                                    if claim_task_response.status_code == 200:
                                                        print(f"{Fore.GREEN}[ Task ] : Sukses mengklaim hadiah untuk {task['name']}")
                                                    else:
                                                        print(f"{Fore.RED}[ Task ] : Gagal mengklaim hadiah untuk {task['name']}")
                                            else:
                                                print(f"{Fore.RED}[ Task ] : Gagal menyelesaikan {task['name']}")
                                else:
                                    print(f"{Fore.RED}[ Task List ] : List task request failed")

                            gameHeaders = get_headers_game(token)
                            checkTiket = requests.get(CheckTiket, headers=gameHeaders).json().get('data', {}).get('game_count')
                            print(f"{Fore.BLUE}[ Play Game ] : Tiket sebanyak {checkTiket}")

                            if auto_play_game == 'Y':
                                while checkTiket > 0:
                                    print(f"{Fore.CYAN+Style.BRIGHT}[ Play Game ] : Playing game...")
                                    gameResponse = requests.get(PlayGame, headers=gameHeaders)
                                    gameData = gameResponse.json().get('data', {})
                                    game_id = gameData.get('game_id')
                                    jsonGame = {
                                        "game_id": game_id,
                                        "point": 56
                                    }
                                    print(f"\r{Fore.CYAN+Style.BRIGHT}[ Play Game ] : Checking game...", end="", flush=True)
                                    time.sleep(1)
                                    claimResponse = requests.post(ClaimGame, headers=gameHeaders, json=jsonGame)

                                    if claimResponse.status_code == 200:
                                        response_data = claimResponse.json()
                                        if response_data.get('code') == 200:
                                            print(f"\r{Fore.GREEN + Style.BRIGHT}[ Play Game ] : Game kelar", flush=True)
                                        else:
                                            error_message = response_data.get('err', '')
                                            print(f"\r{Fore.RED + Style.BRIGHT}[ Play Game ] : Failed to claim game", flush=True)
                                            if response_data.get('code') == 400 and error_message == "game does not exist, claim error.":
                                                print(f"\r{Fore.RED + Style.BRIGHT}[ Play Game ] : Game has ended", flush=True)
                                    else:
                                        print(f"\r{Fore.RED + Style.BRIGHT}[ Play Game ] : Failed to claim game", flush=True)
                                    time.sleep(5)
                                    checkTiket = requests.get(CheckTiket, headers=gameHeaders).json().get('data', {}).get('game_count')
                                    if checkTiket > 0:
                                        print(f"\r{Fore.GREEN+Style.BRIGHT}[ Play Game ] : Tiket masih tersedia, memainkan game lagi...", flush=True)
                                        continue
                                    else:
                                        print(f"\r{Fore.RED+Style.BRIGHT}[ Play Game ] : Tidak ada tiket tersisa.", flush=True)
                                        break
                        else:
                            print(f"{Fore.RED}[ Check Rewards ] : Check rewards request failed")

                    else:
                        print(f"{Fore.RED}[ Token ] : Token not found in the response.")                
                else:
                    print(f"{Fore.RED}[ Login ] : Login failed.")

        print(f"\n\n{Fore.CYAN+Style.BRIGHT}==============Semua akun telah diproses=================\n")

        for detik in range(3600, 0, -1):
            print(f"{Fore.YELLOW}[ Claim ] : Claim ulang dalam {detik} detik", end="\r", flush=True)
            time.sleep(1)
        print(f"{Fore.YELLOW}[ Claim ] : Claim ulang dalam 0 detik", end="\r", flush=True)
        print("\n")
        akun = 1

if __name__ == '__main__':
    main()