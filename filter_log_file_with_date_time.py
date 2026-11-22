import datetime
LOG_FILE = "sample_logfile.log"

ERROR_CODES_OF_INTEREST = "E404"
filter_date = datetime.datetime(2026,8,11,9,1,15)
delta_hours = -71
delta_days= None
if delta_hours is not None:
    delta = datetime.timedelta(hours=delta_hours)
    new_date = filter_date + delta
elif delta_days is not None:
    delta = datetime.timedelta(days=delta_days)
    new_date = filter_date + delta
print('Delta: ', delta)

print("New Date: ", new_date)
with open(LOG_FILE, "r") as f:
    for line in f:
        if ERROR_CODES_OF_INTEREST in line:
            #print(line.strip())
            log_date= line.split(" ",)[0]
            log_time= line.split()[1]
            base_date = datetime.datetime.strptime(log_date + " " + log_time, "%Y-%m-%d %H:%M:%S")
            if (delta_days and delta_days >= 0) or (delta_hours and delta_hours >= 0):
                if filter_date <= base_date and new_date >= base_date:
                    print(line.strip())
            else:
                if base_date <= filter_date and new_date <= base_date:
                    print(line.strip())