import datetime

def is_timeout(timestamp1, timestamp2, quiz_time):
    # Convert the timestamps to datetime objects
    datetime1 = datetime.datetime.fromtimestamp(timestamp1)
    datetime2 = datetime.datetime.fromtimestamp(timestamp2)

    # Calculate the difference between the timestamps
    diff = datetime2 - datetime1

    # Check if the difference is greater than or equal to 10 minutes
    return diff >= datetime.timedelta(minutes=quiz_time)


def get_remaining_time(start_timestamp, current_timestamp, time_limit_minutes):
  # Calculate elapsed time
  elapsed_time = current_timestamp - start_timestamp
  elapsed_time_seconds = elapsed_time

  # Convert time limit to seconds
  time_limit_seconds = time_limit_minutes * 60

  # Calculate remaining time
  remaining_time_seconds = time_limit_seconds - elapsed_time_seconds
  
  return int(remaining_time_seconds)
