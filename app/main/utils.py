from datetime import datetime

def format_date(date=None): 
	return  datetime.utcnow().strftime("%Y %b %d %H:%M:%S") 


