# This is a program for getting a random post from any open VK group. VK API and pure requests are used without 
# intermediate libraries.

import requests
import my_access_token  # This is your python file containing the access token in the form:
# access_token = "<YOUR ACCESS TOKEN>". How to get an access key, read the API provider's help:
# https://dev.vk.com/api/access-token/getting-started
import json
from random import randint

versionVKApi = '5.131'


# F-string template for most VK API requests methods:
def template_vk_api_request(method_str, param_str=''):
    return requests.get(f'https://api.vk.com/method/{method_str}?{param_str}&v={versionVKApi}&access_token=\
{my_access_token.access_token}')


# Gets object_id by short name from link to VK group (object_id is used in all next methods):
def utils_resolve_screen_name(screen_name_str):
    return template_vk_api_request('utils.resolveScreenName', f'screen_name={screen_name_str}')


# Gets posts from the wall of the group defined by owner_id, in the amount of count pieces (no more than 100):
def wall_get(owner_id, domain='', offset=0, count=1, my_filter='all', extended=0, fields=''):
    return template_vk_api_request('wall.get', f'owner_id=-{owner_id}&domain={domain}&offset={offset}&count={count}&\
filter={my_filter}&extended={extended}&fields={fields}')


# Wrapper over functions to immediately convert json information into dictionary format:
def request_data_dict(name_method, *args):
    response = name_method(*args)
    return json.loads(response.content)


# Get the group id by name:
def get_group_id_by_name(group_name_str):
    data = request_data_dict(utils_resolve_screen_name, group_name_str)
    return data['response']['object_id']


# The count of all posts in the group:
def get_group_posts_count_by_id(group_id):
    data = request_data_dict(wall_get, group_id)
    return data['response']['count']


# Get a random post from a group by group name:
def get_random_post_of_group_by_name(group_name_str):
    owner_id = get_group_id_by_name(group_name_str)
    posts_count = get_group_posts_count_by_id(owner_id)
    response = wall_get(owner_id, offset=randint(0, posts_count))
    data = json.loads(response.content)
    text = data['response']['items'][0]['text']
    post_id = data['response']['items'][0]['id']
    post_link = f"https://vk.com/{group_name_str}?w=wall-{owner_id}_{post_id}"
    return text, post_link


# For pretty string:
def pretty_string(some_str, link, max_width):
    new_string = ''
    while len(some_str) > max_width:
        find_space = some_str.rfind(' ', 0, max_width)
        if find_space == -1:
            break
        else:
            new_string += some_str[:find_space] + '\n'
            some_str = some_str[find_space:]
    new_string += some_str
    print(new_string)
    print()
    print("URL: " + link)


# A dictionary of groups for faster conversion, where the key is an abbreviated version of the
# name that is convenient for you, and the value is the real name in the VK:
groups = {"vk": "vk"}


# The main function that receives a random post and its link and prints it to the console:
def go(name):
    name = groups[name]
    random_post, link = get_random_post_of_group_by_name(name)
    pretty_string(random_post, link, 40)


# The main loop of the application, which waits for any input from the user, and then issues a random post from the VK
# group:
def mainloop():
    command = ''
    while command != 'exit':
        command = input()
        print('_' * 100)
        go("vk")
        print('_' * 100)


if __name__ == "__main__":
    mainloop()
