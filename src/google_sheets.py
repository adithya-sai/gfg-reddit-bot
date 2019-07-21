from googleapiclient.discovery import build
from google.oauth2 import service_account
from common.models.user import User, Prediction
from common.models.fixture import Fixture
from common.models.result import Result
from common.config import config

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def build_sheets_service():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=scopes)

    return build('sheets', 'v4', credentials=credentials)


def get_users_from_db():
    users_list = sorted(User.scan(), key=lambda u : u.total_points, reverse = True)
    return users_list

def get_fixture(fixture_id):
    return Fixture.get(fixture_id)

def update_sheets(fixture):

    logger.info("Updating Google Sheets after {} vs {} match, Fixture: {}".format(fixture.home, fixture.away, fixture.fixture_id))
    spreadsheet_id = config.get("SpreadSheetId")

    service = build_sheets_service()
    users = get_users_from_db()
    
    first_row = ["Last Updated after {} vs {}".format(fixture.home, fixture.away)]
    actual_result_str = "{}-{}, {}, {}".format(str(fixture.result.home_goals), str(fixture.result.away_goals), fixture.result.scorers, str(fixture.result.first_event))
    second_row = ["Actual Result -->", actual_result_str]
    empty_row = []    
    header_row = ["User", "Total Points", "Latest Prediction", "Latest Prediction Points"]
    
    sheet_values = [first_row, second_row, empty_row, empty_row, header_row]
    
    fixture_dict = {}
    for u in users:

        curr_result = u.curr_prediction.result
        if u.curr_prediction.fixture not in fixture_dict:
            fixture_dict[u.curr_prediction.fixture] = get_fixture(u.curr_prediction.fixture)
        user_fixture = fixture_dict[u.curr_prediction.fixture]
        curr_prediction_str = "{} vs {} : {}-{}, {}, {}".format(user_fixture.home, user_fixture.away, str(curr_result.home_goals), str(curr_result.away_goals), curr_result.scorers, str(curr_result.first_event))

        row = [u.user_id, u.total_points, curr_prediction_str, u.curr_prediction.points]
        sheet_values.append(row)
    
    body = {
        'values': sheet_values
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range="A1",
        valueInputOption="RAW", body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


# if __name__ == "__main__":
#     r = Result(home_goals=2, away_goals=3, scorers=["A","B"], first_event = 33)
#     f = Fixture(fixture_id=219, home="Tottenham Hotspur", away="Manchester United", start_time=1560928951, status="NS", result=r, league=2)
#     update_sheets(f)