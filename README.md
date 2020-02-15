# InstaBot

### This is project for Instagram App Automaton

1. pip3 install pyinstaller

2. pyinstaller main.py

3. Edit main.spec file

added_files = [
    ('banner.png', '.')
]

a = Analysis(['main.py'],
              ...
             datas=added_files,
              ...
            )

4. pyinstaller --windowed main.spec