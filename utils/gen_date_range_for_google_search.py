#!/usr/bin/env python

# Assumption: all dates are either in July or August, so we assum all days are in the range [1, 31]
def generate_tbs_param(date_str='20240724', delay_days=1):
    if len(date_str) != 8:
        return None
    year_str = date_str[:4]
    month_str = date_str[4:6]
    day_str = date_str[6:]
    next_day = str(int(day_str) + delay_days)
    if next_day > '31':
        month_str = str(int(month_str) + 1)
        next_day = str(int(day_str) - 31)

    min_year = str(int(year_str) - 20)
    # A sample of tbs param is "cdr:1,cd_min:07/01/2024,cd_max:07/20/2024"
    tbs = "cdr:1,cd_min:" + month_str + "/" + day_str + "/" + min_year +\
          ",cd_max:" + month_str +"/" + next_day +"/" + year_str
    return tbs

if __name__ == "__main__":
    print(generate_tbs_param('20240825'))