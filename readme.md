# Chart Spotify Playlist Builder

## What is it?

Scrapes the UK official charts website for the top 100 songs and builds a spotify playlist with these songs. Created so it was possible to listen to the charts without needing to listen to radio 1.

## Usage

First you will need to log into Spotify and sign up for a [libspotify](https://developer.spotify.com/technologies/libspotify/) account and get a key file. **You will need to have a paid account to do this.** Place your key file in the cwd and call it 'spotify_appkey.key'.

Next make two text files called 'spotify_username.txt' and 'spotify_password.txt' and place these in the cwd. In these text files you should type your spotify username and password. 

It will have to be in plaintext (sorry about that), feel free to find a more secure way of doing it and make a pull request.

Next you need to make a playlist in the spotify ui and get the new playlist's URI (right click on the playlist in the menu and it should be an option). Again at some point I will make it so it can make it's own playlist but feel free to do it yourself and make a pull request.

Great now you are all set! Time to run the command below:
```bash
python chartPlaylistBuilder.py 'spotify:user:username:playlist:XXXXXXXXXXXX'
```
where the argument is the playlist URI you got in the last step. Leave it for a few minutes to sort through all the data (good time to go get a cup of tea) and your all done.

## Why does it take so long? (Sales answer)

The Chart Spotify Playlist Builder does a lot of very complex cross platform analysis of the hundreds high-dimensional data points which are involved in building and analysing the data sets required to successfully create a correct and pleasant musical arrangement. Despite many optimisations this takes some time and even on a modern high performance computing machine may take several minutes.

## Why does it take so long? (Technical/correct answer)

I stuck a 1 second delay between requests to Spotify to ensure the script doesn't get caught up in any rate limits I don't know about. This may be unnecessary feel free to look in the code and reduce/remove this at your own risk.

## Contributions

Feel free to post pull requests. Or don't I don't mind.

## License

Copyright 2015 Jacob Causon

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
