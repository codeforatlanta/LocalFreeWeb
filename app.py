from flask import Flask, request, redirect
import urllib, simplejson
import twilio.twiml
import time
import gdata.spreadsheet.service

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])

#Global Variables
email = 'sfbrigade@gmail.com'
password = 'hack4change'
weight = '180'
spreadsheet_key = '1S4jHX9__Drog_qqGsDJYFuO7KvRP9BUD8A95xQ5kkQU'
worksheet_id = 'od6'

def receive_text():

	# print request.values
	results = ""
	stop_id = request.values.get("Body")
	phone_number = request.values.get("From")
	log_text_message(stop_id, phone_number)
	
	get_geo_url = 'http://localfreeweb.cartodb.com/api/v2/sql?q=SELECT stop_lat, stop_lon FROM stops WHERE stop_id = '
	get_geo_url += stop_id
	response = urllib.urlopen(get_geo_url)
	for line in response:
		response_dict = simplejson.loads(line)
	#    print response_dict
	geo_lat = str(response_dict['rows'][0]['stop_lat'])
	geo_long = str(response_dict['rows'][0]['stop_lon'])
	lat_long = [geo_lat,geo_long]
	#    print lat_long

	get_closest_free_net_url = 'http://localfreeweb.cartodb.com/api/v2/sql?q=SELECT name, address, zip, phone, ST_Distance(the_geom::geography, ST_PointFromText(\'POINT('+ geo_long + ' ' + geo_lat + ')\', 4326)::geography) AS distance FROM freeweb ORDER BY distance ASC LIMIT 3'
	response = urllib.urlopen(get_closest_free_net_url)
	for line in response:
		response_dict = simplejson.loads(line)

	for i in range(0, 3):
	    results += " " + response_dict['rows'][i]['name'] + " @ " 
	    results += response_dict['rows'][i]['address'] + ";"
	# 	    print '\nResult ' + str(i + 1) + ': '
	# 	    print str(response_dict['rows'][i]['name'])
	# 	    print str(response_dict['rows'][i]['address'])
	# 	    print 'San Francisco, CA ' + str(response_dict['rows'][i]['zip'])
	# 	    print 'Phone number: ' + str(response_dict['rows'][i]['phone'])
	resp = twilio.twiml.Response()
	resp.message("Ask for 'free internet' at these places:" + results)
#	resp.message(response_dict['rows'][0]['name'])
	return str(resp)
	
def log_text_message(stop_id, phone_number):	

	spr_client = gdata.spreadsheet.service.SpreadsheetsService()
	spr_client.email = email
	spr_client.password = password
	spr_client.source = 'LocalFreeWeb Texting App'
	spr_client.ProgrammaticLogin()

if __name__ == "__main__":
    app.run(debug=True)
