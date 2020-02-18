# InstaBot

### This is project for Instagram App Automaton

# UI Description

- Run main.exe
- Start Button
- Stop Button
- Setting (not working now)
- Cycle(hour) - Bot thread will check followings and add new followings every this cycle hours
- Follows/Cycle - Bot thread will follow this number of persons every cycle

# Test Step

- App start
1. Turn on Bluestacks on Windows10
2. Install and run Instagram App
3. Login to your Instagram Account and locate on the first main page.
4. Don't overlap any other window over Bluestacks window
- Bot Start
4. Run Instabot main.exe 
5. Set cycle and follows/cycle value with your option
6. Set specified one name you want to follow
7. Filepath saves followers' name list who are following the specified one
8. Press start button
9. You can press stop or Ctrl+q to exit process

# Thread step

1. Read Followings ( Read persons who i am following from past cycle)
2. Check Followings (Main->Profile->Followers->Search one by one -> Main)
3. Remove UnFollowings (Main->Profile->Followings->Remove one by one -> Main)
4. Add Followings (Main->Profile->Profile_Menu->Discover People-> Add one by one -> Back)
4. Save Followings

# Warnings

1. Please confirm Email before start.
2. On Followers and Followings Search Page remove non-Person items.
3. There may be alert once from app. If this comes click to make it remove

# File Description

- followings.data - The list of persons who i am following will be saved in this file
- followers.data - The list of persons who are following me back.
- log.log - Save all logs here

# Build Step

1. pip3 install pyinstaller

2. pyinstaller main.py

3. Edit main.spec file

        added_files = [
            ('banner.png', '.'),
            ('config.ini', '.')
        ]

a = Analysis(['main.py'],
              ...
             datas=added_files,
              ...
            )

4. pyinstaller --windowed main.spec

