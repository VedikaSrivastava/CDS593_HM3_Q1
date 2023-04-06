# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# import openpyxl
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetStudentID(Action):
    def name(self) -> Text:
        return "action_get_student_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Open the excel file and select the worksheet
        # workbook = openpyxl.load_workbook('student_database.xlsx')
        # worksheet = workbook.active
        data = pd.read_excel('student_database.xlsx', sheet_name='Sheet1')

        # Get the student name from the tracker
        student_name = tracker.get_slot("first_name") + " " + tracker.get_slot("last_name")

        # Search for the student ID in the database
        for i in range(len(data["Student Name"])):
            if data["Student Name"][i] == student_name:
                student_id = data["Student ID"][i]
                break

        # Send the student ID to the user
        dispatcher.utter_message("Your student ID is {}.".format(student_id))

        return []



class SubmitCovidTestResultsAction(Action):

    def name(self) -> Text:
        return "action_submit_covid_test_results"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the student details and test results from slots
        student_id = tracker.get_slot("student_id")
        student_name = tracker.get_slot("first_name") + " " + tracker.get_slot("last_name")
        covid_status = tracker.get_slot("covid_status")
        test_type = tracker.get_slot("covid_test_type")

        # Load the student database
        data = pd.read_excel('student_database.xlsx', sheet_name='Sheet1')

        # Check if the student record already exists
        if student_id in data["Student ID"].values:
            data.loc[data["Student ID"] == student_id, ["Covid Status", "Covid Test Type"]] = [covid_status, test_type]
        else:
            data = data.append({"Student Name": student_name, "Student ID": student_id,  "Covid Status": covid_status, 
                                "Covid Test Type": test_type}, ignore_index=True)

        # Save the updated student database
        data.to_excel("student_database.xlsx", sheet_name='Sheet1', index=False)

        # Send a confirmation message to the user
        dispatcher.utter_message(text="Thank you for submitting your COVID-19 test results. Your status has been updated.")

        return []
