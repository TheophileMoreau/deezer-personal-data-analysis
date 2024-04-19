import json
import requests
import pandas as pd
import time
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--max_time', 
                    default='60',
                    help="Max time to collect elements (seconds)"
                   )
parser.add_argument('--max_number',
                    help="Max number of elements to collect"
                   )
parser.add_argument('--sleep_buffer',
                    default='500',
                    help="Set sleeping time between requests (milliseconds)"
                   )
args = parser.parse_args()


file_path = 'track_infos.csv'
current_tracks = pd.DataFrame()

source_df = pd.read_csv('listening_history_all_time.csv')
unique_isrc = set(source_df['ISRC'])
len_source = len(unique_isrc)

if os.path.exists(file_path):
    print(f'{file_path} exists.\n')    

    print('Cheking already found values...')

    current_tracks = pd.read_csv(file_path)
    current_isrc = set(current_tracks['isrc'])

    common_isrc = current_isrc.intersection(unique_isrc)

    if len(common_isrc) > 0:
        unique_isrc = unique_isrc.difference(common_isrc)

start_time = time.time()
max_time = int(args.max_time)
if args.max_number:
    max_number = int(args.max_number)
else:
    max_number = round(max_time * 1.3) # Aproximation
sleep_buffer = int(args.sleep_buffer) / 1000 # To seconds

saved_data = []

print(f"\nLet's start getting {max_number} tracks in max {max_time}s !\n")

for index, code in enumerate(unique_isrc):
    if index + 1 < max_number and time.time() - start_time < max_time:
        row_dict = {}

        track_url = f'https://api.deezer.com/track/isrc:{code}'

        print(f'Getting {track_url}')

        track = requests.get(track_url)
        if track.status_code == 200:
            track_content = json.loads(track.content)

            row_dict['isrc'] = track_content['isrc'] if track_content.get('isrc') else None
            row_dict['track_id'] = track_content['id'] if track_content.get('id') else None
            row_dict['track_title'] = track_content['title'] if track_content.get('title') else None
            row_dict['artist'] = track_content['artist']['name'] if track_content.get('artist', {}).get('name') else None
            row_dict['album'] = track_content['album']['title'] if track_content.get('album', {}).get('title') else None

            album_id = track_content['album']['id'] if track_content.get('album', {}).get('id') else ''

            album_url = f'https://api.deezer.com/album/{album_id}'

            album = requests.get(album_url)
            if album.status_code == 200:
                album_content = json.loads(album.content)

                if album_content.get('genres', {}).get('data'):
                    for secondary_index, genre in enumerate(album_content['genres']['data']):
                        row_dict[f'gender-{secondary_index + 1}'] = genre['name'] if genre['name'] else None

            print(f'{row_dict}\n')

            time.sleep(sleep_buffer)

            saved_data.append(row_dict)

            if (index + 1) % 10 == 0:
                # Because why not
                print('\n------------------------------------------------------------------------------------')
                print('                                     Saving...')
                print('------------------------------------------------------------------------------------')
                print(f'Elpased time : {round(time.time() - start_time)}s / Target time : {max_time}s  |  Current volume : {index} / Target volume : {max_number}')
                print('\n')

                saved_df = pd.DataFrame(saved_data)
                final_df = pd.concat([current_tracks, saved_df])
                final_df.to_csv(file_path, index=False)

                time.sleep(0.5)

    else:
        break

saved_df = pd.DataFrame(saved_data)
final_df = pd.concat([current_tracks, saved_df])
final_df.to_csv(file_path, index=False)

print('--------------')
print('Final save...')
print('--------------')
print('\n')
print('Done !')
print(f'Took {round(time.time() - start_time)}s, found {index} elements !')
print('\n')
print(f'Currently {final_df.shape[0]} track infos found out of {len_source} in total...')

progression_bar = ''
size_bar = 50
for i in range(1, size_bar + 1):
    if i / size_bar <= final_df.shape[0] / len_source:
        progression_bar += '#'
    else:
        progression_bar += '_'
print(f'{progression_bar} ({round(final_df.shape[0] * 100 / len_source, 2)}%)')
print('\n')