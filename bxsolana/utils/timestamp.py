import datetime
from betterproto import Timestamp


def timestamp():
    """
    Creates and returns a Protocol Buffer Timestamp object based on the current time.
    
    This function captures the current time and converts it to a Protocol Buffer
    Timestamp object with seconds since epoch and nanoseconds precision.
    
    Returns:
        Timestamp: A Protocol Buffer Timestamp object representing the current time
                  with seconds and nanoseconds components.
    """
    now = datetime.datetime.now()
    timestamp = Timestamp(
        seconds=int(now.timestamp()),
        nanos=now.microsecond * 1000
    )
    print(timestamp)
    return timestamp


def timestamp_rfc3339():
    """
    Returns the current time as an RFC 3339 formatted string suitable for
    Protocol Buffer Timestamp JSON serialization.
    
    Reference: https://protobuf.dev/reference/php/api-docs/Google/Protobuf/Timestamp.html
    
    The format is: "{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z"
    - All components except year are zero-padded to two digits
    - Year is expressed using four digits
    - Fractional seconds can go up to 9 digits (nanosecond precision)
    - The "Z" suffix indicates UTC timezone
    
    Returns:
        str: Current time in RFC 3339 format with UTC timezone (Z)
    """

    now = datetime.datetime.now(datetime.timezone.utc)
    formatted_time = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '000Z'
    
    return formatted_time