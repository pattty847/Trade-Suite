# Timedelta function demonstration
from datetime import datetime, timedelta


# Using current time
ini_time_for_now = datetime.now()

# printing initial_date
print ('initial_date:', str(ini_time_for_now))

# Calculating past dates
# for two years
past_date_before_2yrs = ini_time_for_now - \
					timedelta(days = 730.0)

# for two hours
past_date_before_2hours = ini_time_for_now - \
						timedelta(hours = 2)


# printing calculated past_dates
print('past_date_before_2yrs:', str(past_date_before_2yrs))
print('past_date_before_2hours:', str(past_date_before_2hours))
