import PyInstaller.__main__

PyInstaller.__main__.run([
    'OSC Countdown.py',
    '--onefile',
    '--windowed',
    '--icon:timerIcns.icns'
])