import datetime

def is_timeout(timestamp1, timestamp2, quiz_time):
    # Convert the timestamps to datetime objects
    datetime1 = datetime.datetime.fromtimestamp(timestamp1)
    datetime2 = datetime.datetime.fromtimestamp(timestamp2)

    # Calculate the difference between the timestamps
    diff = datetime2 - datetime1

    # Check if the difference is greater than or equal to 10 minutes
    return diff >= datetime.timedelta(minutes=quiz_time)

