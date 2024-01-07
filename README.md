# DiscordSpotifyStatus

## Installation
1) Download the project and install the required modules from the requirements.txt file.
2) Open the Discord application console (Ctrl + Shift + I) and execute the following script:
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()

Copy the obtained token to a text file.
3) If the console is not available in the application, make changes to the Discord settings:
   - Navigate to %APPDATA%\discord\settings.json
   - Add the following key before WINDOW_BOUNDS: "DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING": true,
   - Return to step 2.
4) Go to the website [Spotify](https://open.spotify.com), log in, open the console (Ctrl + Shift + I), navigate to the "Application" tab, "Storage", "Cookie files", "..spotify...".
Search for cookie files, enter sp_dc in the search, and copy the token to a text file.
5) In the downloaded repository, locate the data.json file and paste the obtained data into the appropriate locations.
6) Open discord_spotify_status.py, and now you can run the program.

## Usage
The program operates on a specific chain of web requests. Due to network delays, restarting the program may be required.
The program sets an emoji string for songs. In the tracks.json file, you can set which emojis should be associated with specific albums (see examples in the file). To obtain an album ID, copy the direct link to the album; the ID will be before ? and after \.