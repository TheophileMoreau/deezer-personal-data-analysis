# Deezer Personal Data Analysis

**Explore your personal music data !**

*Steps*
1. Get your personal data
    - Account settings / My information / My personal data
    - This may take a few days...
2. Extract the Listening History tab as a csv
    - Name the file listening_history_all_time.csv
    - You can rename but will need to edit the code
3. Run extract_track_infos.py
    - ```python3 extract_track_infos.py```
    - Specify arguments (see --help)
        - max_time
        - max_number
        - sleep_buffer
        - ```python3 extract_track_infos.py --max_time 300 --max_number 200 --sleep_buffer 200```