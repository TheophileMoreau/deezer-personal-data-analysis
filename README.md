# Deezer Personal Data Analysis

**Explore your personal music data !**

*Steps*
1. Get your personal data
    a. Account settings / My information / My personal data
    b. This may take a few days...
2. Extract the Listening History tab as a csv
    a. Name the file listening_history_all_time.csv
    b. You can rename but will need to edit the code
3. Run extract_track_infos.py
    a. ```python3 extract_track_infos.py```
    b. Specify arguments (see --help)
        i. max_time
        ii. max_number
        iii. sleep_buffer
        iiii. ```python3 extract_track_infos.py --max_time 300 --max_number 200 --sleep_buffer 200```