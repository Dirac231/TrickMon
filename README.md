## What is this?

A telegram API handler to send a notification when a new CVE or domain is detected in the `trickest/cve` and `trickest/inventory` repositories.\
\
To use it, replace the bot and chat ID in the `trickest.py` file, then run the script in the background on a VPS, or on your server:
```
python3 trickest.py </dev/null &>/dev/null &
```
