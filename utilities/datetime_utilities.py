from datetime import datetime, timedelta

import pytz

from utilities import cruize_constants

"""
     :method   - convert_epoch_to_utcdatetime: convert epoch to utcdatetime.
     :params   - epoch:epoch time.
     :return   - utcdatetime
   """


def convert_epoch_to_utcdatetime(epoch, parser="%Y-%m-%dT%H:%M:%S"):
    return (
        (datetime.utcfromtimestamp(epoch))
        .replace(tzinfo=pytz.utc)
        .astimezone(tz=cruize_constants.TIMEZONE)
        .strftime(parser)
    )


"""
    :method   - get_timezone_aware_datetime:  timezone aware datetime.
    :params   - epoch:epoch time.
    :return   - utcdatetime
  """


def get_timezone_aware_datetime(days_delta=0):
    return datetime.now(tz=cruize_constants.TIMEZONE) + timedelta(days=days_delta)
