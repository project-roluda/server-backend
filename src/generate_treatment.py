import json
from geopy import distance

class TreatmentModel:

    def __init__(self, current_latitude, current_longitude):
        self.medication_dict = json.load(open("static/dict_medication.json", "r"))
        self.locations_dict = json.load(open("static/dict_locations.json", "r"))
        self.useMeds = False
        self.currentMeds = []
        self.return_string = ""
        self.current_latitude = current_latitude
        self.current_longitude = current_longitude
        self.med_result_dict = {} # used for processing purposes

    def find_treament_for(self, condition):
        medication_result = self.medication_dict[condition]
        if medication_result["useMeds"]:
            self.useMeds = True
            self.currentMeds = medication_result["medication"]

            for name_of_medication in self.currentMeds:

                for key in self.locations_dict:
                    location_dict = self.locations_dict[key]

                    user_coords = (self.current_latitude, self.current_longitude)
                    location_coords = (location_dict["latitude"], location_dict["longitude"])

                    distance_km = distance.distance(user_coords, location_coords).km

                    if (name_of_medication not in self.med_result_dict.keys()):
                        self.med_result_dict[name_of_medication] = {
                            "location_distance_km": distance_km,
                            "address": location_dict["address"],
                            "name": location_dict["name"]
                        }

                    if distance_km < self.med_result_dict[name_of_medication]["location_distance_km"]:
                        self.med_result_dict[name_of_medication] = {
                            "location_distance_km": distance_km,
                            "address": location_dict["address"],
                            "name": location_dict["name"]
                        }

            for item in self.med_result_dict:
                self.return_string += f"{item} ({self.med_result_dict[item]['location_distance_km']} km) - "
            
        else:
            self.return_string = medication_result["therapy"]

        if len(medication_result["sources"]) > 0:
            self.return_string += " Sources: (" + ", ".join(medication_result["sources"]) + ")"

        return self.return_string
        

