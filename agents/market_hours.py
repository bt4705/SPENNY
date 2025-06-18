k"""Returns NYSE open/close status."""
import pandas_market_calendars as mcal, datetime as dt, pytz
nyse, ET = mcal.get_calendar('NYSE'), pytz.timezone('America/New_York')

def status():
    today  = dt.datetime.now(ET).date()
    sched  = nyse.schedule(start_date=today, end_date=today)
    if sched.empty:
        return {'is_open': False}
    row    = sched.iloc[0]
    now    = dt.datetime.now(ET)
    open_, close_ = row['market_open'].tz_convert(ET), row['market_close'].tz_convert(ET)
    return {
        'is_open':   open_ <= now <= close_,
        'next_open': open_,
        'next_close': close_
    }
