from healthtools.scrapers.base_scraper import Scraper
from healthtools.config import SITES, AWS
from datetime import datetime
import boto3


class DoctorsScraper(Scraper):
    '''
    Scraper for regular doctors on the medical board website
    '''

    def __init__(self):
        super(DoctorsScraper, self).__init__()
        self.site_url = SITES["DOCTORS"]
        self.fields = [
            "name", "reg_date", "reg_no", "postal_address", "qualifications",
            "speciality", "sub_speciality", "id",
        ]

        self.s3_key = "data/doctors.json"
        self.s3_historical_record_key = "data/archive/doctors-{}.json"
        self.delete_file = "data/delete_doctors.json"

    def format_for_cloudsearch(self, entry):
        '''
        Format entry into cloudsearch ready document
        '''
        try:
            date_obj = datetime.strptime(entry['reg_date'], "%Y-%m-%d")
        except:
            date_obj = datetime.strptime(entry['reg_date'], "%d-%m-%Y")
        entry['reg_date'] = datetime.strftime(
            date_obj, "%Y-%m-%dT%H:%M:%S.000Z")
        entry["facility"] = entry["practice_type"] = "-"
        # all bulk data need meta data describing the data
        meta_dict = {
            "index": {
                "_index": ES["index"],
                "_type": "doctors",
                "_id": entry["id"]
            }
        }
        return meta_dict, entry
