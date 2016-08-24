import os
import sys
import datetime
from flask import Flask, request, jsonify

from smsghussd import (Ussd, UssdHandler, UssdTypes, UssdStore,
UssdMenu, UssdMenuItem, UssdForm, UssdOption, UssdInput)



BASE_PATH =os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(BASE_PATH))

class GetResults(UssdHandler):
	def session_start(self):
                menu= UssdMenu(header="Welcome To Our School", footer="Thank you for considering us").add_item("Get Info", "get_info_form").add_zero_item("End Session", "exit")
                return self.render_menu(menu)

	def get_info_form(self):
		form = UssdForm("Salutations", "get_user").add_input(UssdInput("Student_Id")).add_input(UssdInput("Name"))
		return self.render_form(form)
	def get_user(self):
		greet="Welcome"
		name=self.form_data["Name"]
		return self.render("{0}, {1}".format(greet,name))

	def exit(self):
		return self.render("Thank you for contacting us")
app= Flask(__name__)
ussd_service= Ussd(handler=GetResults)
@app.route("/", methods=["POST"])
def ussd_handler():
	ussd_response=ussd_service.process(request.get_json(force=True))
	resp=jsonify(ussd_response.to_dict())
	return resp
if __name__ =="__main__":
	app.run(host="127.0.0.1", port=8000, debug=True)

