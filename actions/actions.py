# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


import mysql.connector
from mysql.connector import Error

class ActionTrainSuggestions(Action):

    def name(self) -> Text:
        return "action_train_suggestions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        source=tracker.get_slot("source")
        dest=tracker.get_slot("destination")

        # write the sql query here.
        mySQLConnection = mysql.connector.connect(host='localhost',
                                                  database='railwaychatbot',
                                                  user='root',
                                                  password='1234')

        cursor = mySQLConnection.cursor(buffered=True)
        sql_select_query = """select train_no, train_name, source_station_name, destination_station_name from traindetails where (source_station=%s OR source_station_name=%s) and (destination_station=%s OR destination_station_name=%s)"""
        cursor.execute(sql_select_query, (source,source,dest,dest))
        record = cursor.fetchall()
        for row in record:
            dispatcher.utter_message(text="Train Number = "+" "+ str(row[0]))
            dispatcher.utter_message(text="Train Name = "+" "+row[1])
            dispatcher.utter_message(text="Source= "+" "+row[2])
            dispatcher.utter_message(text="Destination  = "+" "+row[3]+"\n")

        dispatcher.utter_message(text="The following trains were found.")

        return []

class ActionPnrStatus(Action):

    def name(self) -> Text:
        return "action_pnr_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pnr=tracker.get_slot("pnrNo")
        

        # write the sql query here.
        mySQLConnection = mysql.connector.connect(host='localhost',
                                                  database='railwaychatbot',
                                                  user='root',
                                                  password='1234')

        cursor = mySQLConnection.cursor(buffered=True)
        sql_select_query = """Select train_no, train_name, coach, seat_no, date, status, source, destination  from pnrstatus where pnr_no = %s """
        cursor.execute(sql_select_query, (pnr,))
        record = cursor.fetchall()

        if record ==[]:
            dispatcher.utter_message(text="No such Pnr status , plz Enter Valid PNR No")
        else:
            dispatcher.utter_message(text="PNR STATUS"+"\n")
            for row in record:
                dispatcher.utter_message(text="Train Number = "+" "+ str(row[0]))
                dispatcher.utter_message(text="Train Name = "+" "+row[1])
                dispatcher.utter_message(text="Coach = "+" "+row[2])
                dispatcher.utter_message(text="Seat No  = "+" "+row[3])
                dispatcher.utter_message(text="Date of Journey  = "+" "+row[4])
                dispatcher.utter_message(text="Status  = "+" "+row[5])
                dispatcher.utter_message(text="From  = "+" "+row[6])
                dispatcher.utter_message(text="To  = "+" "+row[7]+"\n")

            

        return []

class ActionTrainInfo(Action):

    def name(self) -> Text:
        return "action_train_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        train_no=tracker.get_slot("trainNo")
        flag=tracker.get_slot("flag")
        flag=str(flag)

        # write the sql query here.
        mySQLConnection = mysql.connector.connect(host='localhost',
                                                  database='railwaychatbot',
                                                  user='root',
                                                  password='1234')

        cursor = mySQLConnection.cursor(buffered=True)
        if flag =="info":
            sql_select_query = """select distinctrow train_no, train_name, source_station_name, destination_station_name from traindetails where train_no=%s"""
            cursor.execute(sql_select_query, (train_no,))
            record = cursor.fetchall()
            
            
            if record ==[]:
                dispatcher.utter_message(text="No such Train , plz Enter Valid train No")
            else:    
                
                for row in record:
                    dispatcher.utter_message(text="Train Number = "+" "+str(row[0]))
                    dispatcher.utter_message(text="Train Name = "+" "+ row[1])
                    dispatcher.utter_message(text="Source= "+" "+ row[2])
                    dispatcher.utter_message(text="Destination  = "+" "+row[3]+ "\n")
                    dispatcher.utter_message(text="\n")

                dispatcher.utter_message(text="The details for your Train" )
        elif flag=="schedule":
            sql_select_query = """select train_no, train_name, station_name, arrival_time, departure_time from traindetails where train_no=%s"""
            cursor.execute(sql_select_query, (train_no,))
            record = cursor.fetchall()
            if record ==[]:
                dispatcher.utter_message(text="No such Train , plz Enter Valid train No")
            else:
                for row in record:
                    dispatcher.utter_message(text="Train Number = "+" "+str(row[0]))
                    dispatcher.utter_message(text="Train Name = "+" "+row[1])
                    dispatcher.utter_message(text="Station  Name = "+" "+row[2])
                    dispatcher.utter_message(text="Arrival Time = "+" "+row[3])
                    dispatcher.utter_message(text="Departure Time = "+" "+row[4])
                    dispatcher.utter_message(text="\n")

                dispatcher.utter_message(text="The Train Schedule")
            

        return []


class SetInfo(Action):
    def name(self):
        return 'set_info'
    

    def run(self, dispatcher, tracker, domain):
        return [ SlotSet('flag', 'info')]

class SetSchedule(Action):
    def name(self):
        return 'set_schedule'
    

    def run(self, dispatcher, tracker, domain):
        return [ SlotSet('flag', 'schedule')]



class SetDestinatio(Action):
    def name(self):
        return 'set_destination'
    

    def run(self, dispatcher, tracker, domain):
        source=tracker.get_slot("source")
        
        if  source=="":
            dispatcher.utter_message(text="Enter source again")
            return[]
        else:
           message = tracker.latest_message.get('text')
           return [SlotSet('destination', message)]





    
