import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sportsreference import utils
from sportsreference.ncaab.conferences import Conferences
from sportsreference.ncaab.constants import (ADVANCED_OPPONENT_STATS_URL,
                                             ADVANCED_STATS_URL,
                                             BASIC_OPPONENT_STATS_URL,
                                             BASIC_STATS_URL)
from sportsreference.ncaab.teams import Teams


MONTH = 1
YEAR = 2018


def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), 'ncaab_stats', filename)
    return open('%s' % filepath, 'r').read()


def mock_pyquery(url):
    class MockPQ:
        def __init__(self, html_contents):
            self.status_code = 200
            self.html_contents = html_contents
            self.text = html_contents

        def __call__(self, div):
            if div == 'table#basic_school_stats':
                return read_file('%s-school-stats-table.html' % YEAR)
            elif div == 'table#basic_opp_stats':
                return read_file('%s-opponent-stats-table.html' % YEAR)
            elif div == 'table#adv_school_stats':
                return read_file('%s-advanced-school-stats-table.html' % YEAR)
            else:
                return read_file('%s-advanced-opponent-stats-table.html'
                                 % YEAR)

    basic_contents = read_file('%s-school-stats.html' % YEAR)
    opp_contents = read_file('%s-opponent-stats.html' % YEAR)
    adv_contents = read_file('%s-advanced-school-stats.html' % YEAR)
    adv_opp_contents = read_file('%s-advanced-opponent-stats.html' % YEAR)
    if url == BASIC_STATS_URL % YEAR:
        return MockPQ(basic_contents)
    elif url == BASIC_OPPONENT_STATS_URL % YEAR:
        return MockPQ(opp_contents)
    elif url == ADVANCED_STATS_URL % YEAR:
        return MockPQ(adv_contents)
    elif url == ADVANCED_OPPONENT_STATS_URL % YEAR:
        return MockPQ(adv_opp_contents)


class MockDateTime:
    def __init__(self, year, month):
        self.year = year
        self.month = month


class TestNCAABIntegration:
    @mock.patch('requests.get', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            'conference': 'big-ten',
            'abbreviation': 'PURDUE',
            'name': 'Purdue',
            'games_played': 37,
            'wins': 30,
            'losses': 7,
            'win_percentage': .811,
            'simple_rating_system': 23.41,
            'strength_of_schedule': 8.74,
            'conference_wins': 15,
            'conference_losses': 3,
            'home_wins': 16,
            'home_losses': 1,
            'away_wins': 8,
            'away_losses': 2,
            'points': 2974,
            'opp_points': 2431,
            'minutes_played': 1485,
            'field_goals': 1033,
            'field_goal_attempts': 2097,
            'field_goal_percentage': .493,
            'three_point_field_goals': 353,
            'three_point_field_goal_attempts': 840,
            'three_point_field_goal_percentage': .420,
            'two_point_field_goals': 680,
            'two_point_field_goal_attempts': 1257,
            'two_point_field_goal_percentage': .541,
            'free_throws': 555,
            'free_throw_attempts': 747,
            'free_throw_percentage': .743,
            'offensive_rebounds': 311,
            'total_rebounds': 1295,
            'assists': 598,
            'steals': 211,
            'blocks': 180,
            'turnovers': 399,
            'personal_fouls': 580,
            'opp_field_goals': 907,
            'opp_field_goal_attempts': 2197,
            'opp_field_goal_percentage': .413,
            'opp_three_point_field_goals': 251,
            'opp_three_point_field_goal_attempts': 755,
            'opp_three_point_field_goal_percentage': .332,
            'opp_two_point_field_goals': 656,
            'opp_two_point_field_goal_attempts': 1442,
            'opp_two_point_field_goal_percentage': .455,
            'opp_free_throws': 366,
            'opp_free_throw_attempts': 531,
            'opp_free_throw_percentage': .689,
            'opp_offensive_rebounds': 376,
            'opp_total_rebounds': 1204,
            'opp_assists': 443,
            'opp_steals': 190,
            'opp_blocks': 94,
            'opp_turnovers': 448,
            'opp_personal_fouls': 688,
            'pace': 68.2,
            'offensive_rating': 117.5,
            'free_throw_attempt_rate': .356,
            'three_point_attempt_rate': .401,
            'true_shooting_percentage': .606,
            'total_rebound_percentage': 51.8,
            'assist_percentage': 57.9,
            'steal_percentage': 8.3,
            'block_percentage': 12.5,
            'effective_field_goal_percentage': .577,
            'turnover_percentage': 14.0,
            'offensive_rebound_percentage': 27.3,
            'free_throws_per_field_goal_attempt': .265,
            'opp_offensive_rating': 96.0,
            'opp_free_throw_attempt_rate': .242,
            'opp_three_point_attempt_rate': .344,
            'opp_true_shooting_percentage': .496,
            'opp_total_rebound_percentage': 48.2,
            'opp_assist_percentage': 48.8,
            'opp_steal_percentage': 7.5,
            'opp_block_percentage': 7.5,
            'opp_effective_field_goal_percentage': .470,
            'opp_turnover_percentage': 15.5,
            'opp_offensive_rebound_percentage': 27.6,
            'opp_free_throws_per_field_goal_attempt': .167
        }
        self.abbreviations = [
            'ABILENE-CHRISTIAN', 'AIR-FORCE', 'AKRON', 'ALABAMA-AM',
            'ALABAMA-BIRMINGHAM', 'ALABAMA-STATE', 'ALABAMA', 'ALBANY-NY',
            'ALCORN-STATE', 'AMERICAN', 'APPALACHIAN-STATE', 'ARIZONA-STATE',
            'ARIZONA', 'ARKANSAS-LITTLE-ROCK', 'ARKANSAS-PINE-BLUFF',
            'ARKANSAS-STATE', 'ARKANSAS', 'ARMY', 'AUBURN', 'AUSTIN-PEAY',
            'BALL-STATE', 'BAYLOR', 'BELMONT', 'BETHUNE-COOKMAN', 'BINGHAMTON',
            'BOISE-STATE', 'BOSTON-COLLEGE', 'BOSTON-UNIVERSITY',
            'BOWLING-GREEN-STATE', 'BRADLEY', 'BRIGHAM-YOUNG', 'BROWN',
            'BRYANT', 'BUCKNELL', 'BUFFALO', 'BUTLER', 'CAL-POLY',
            'CAL-STATE-BAKERSFIELD', 'CAL-STATE-FULLERTON',
            'CAL-STATE-NORTHRIDGE', 'CALIFORNIA-DAVIS', 'CALIFORNIA-IRVINE',
            'CALIFORNIA-RIVERSIDE', 'CALIFORNIA-SANTA-BARBARA', 'CALIFORNIA',
            'CAMPBELL', 'CANISIUS', 'CENTRAL-ARKANSAS',
            'CENTRAL-CONNECTICUT-STATE', 'CENTRAL-FLORIDA', 'CENTRAL-MICHIGAN',
            'CHARLESTON-SOUTHERN', 'CHARLOTTE', 'CHATTANOOGA', 'CHICAGO-STATE',
            'CINCINNATI', 'CITADEL', 'CLEMSON', 'CLEVELAND-STATE',
            'COASTAL-CAROLINA', 'COLGATE', 'COLLEGE-OF-CHARLESTON',
            'COLORADO-STATE', 'COLORADO', 'COLUMBIA', 'CONNECTICUT',
            'COPPIN-STATE', 'CORNELL', 'CREIGHTON', 'DARTMOUTH', 'DAVIDSON',
            'DAYTON', 'DELAWARE-STATE', 'DELAWARE', 'DENVER', 'DEPAUL',
            'DETROIT-MERCY', 'DRAKE', 'DREXEL', 'DUKE', 'DUQUESNE',
            'EAST-CAROLINA', 'EAST-TENNESSEE-STATE', 'EASTERN-ILLINOIS',
            'EASTERN-KENTUCKY', 'EASTERN-MICHIGAN', 'EASTERN-WASHINGTON',
            'ELON', 'EVANSVILLE', 'FAIRFIELD', 'FAIRLEIGH-DICKINSON',
            'FLORIDA-AM', 'FLORIDA-ATLANTIC', 'FLORIDA-GULF-COAST',
            'FLORIDA-INTERNATIONAL', 'FLORIDA-STATE', 'FLORIDA', 'FORDHAM',
            'FRESNO-STATE', 'FURMAN', 'GARDNER-WEBB', 'GEORGE-MASON',
            'GEORGE-WASHINGTON', 'GEORGETOWN', 'GEORGIA-SOUTHERN',
            'GEORGIA-STATE', 'GEORGIA-TECH', 'GEORGIA', 'GONZAGA', 'GRAMBLING',
            'GRAND-CANYON', 'GREEN-BAY', 'HAMPTON', 'HARTFORD', 'HARVARD',
            'HAWAII', 'HIGH-POINT', 'HOFSTRA', 'HOLY-CROSS', 'HOUSTON-BAPTIST',
            'HOUSTON', 'HOWARD', 'IDAHO-STATE', 'IDAHO', 'ILLINOIS-CHICAGO',
            'ILLINOIS-STATE', 'ILLINOIS', 'INCARNATE-WORD', 'INDIANA-STATE',
            'INDIANA', 'IONA', 'IOWA-STATE', 'IOWA', 'IPFW', 'IUPUI',
            'JACKSON-STATE', 'JACKSONVILLE-STATE', 'JACKSONVILLE',
            'JAMES-MADISON', 'KANSAS-STATE', 'KANSAS', 'KENNESAW-STATE',
            'KENT-STATE', 'KENTUCKY', 'LA-SALLE', 'LAFAYETTE', 'LAMAR',
            'LEHIGH', 'LIBERTY', 'LIPSCOMB', 'LONG-BEACH-STATE',
            'LONG-ISLAND-UNIVERSITY', 'LONGWOOD', 'LOUISIANA-LAFAYETTE',
            'LOUISIANA-MONROE', 'LOUISIANA-STATE', 'LOUISIANA-TECH',
            'LOUISVILLE', 'LOYOLA-IL', 'LOYOLA-MARYMOUNT', 'LOYOLA-MD',
            'MAINE', 'MANHATTAN', 'MARIST', 'MARQUETTE', 'MARSHALL',
            'MARYLAND-BALTIMORE-COUNTY', 'MARYLAND-EASTERN-SHORE', 'MARYLAND',
            'MASSACHUSETTS-LOWELL', 'MASSACHUSETTS', 'MCNEESE-STATE',
            'MEMPHIS', 'MERCER', 'MIAMI-FL', 'MIAMI-OH', 'MICHIGAN-STATE',
            'MICHIGAN', 'MIDDLE-TENNESSEE', 'MILWAUKEE', 'MINNESOTA',
            'MISSISSIPPI-STATE', 'MISSISSIPPI-VALLEY-STATE', 'MISSISSIPPI',
            'MISSOURI-KANSAS-CITY', 'MISSOURI-STATE', 'MISSOURI', 'MONMOUTH',
            'MONTANA-STATE', 'MONTANA', 'MOREHEAD-STATE', 'MORGAN-STATE',
            'MOUNT-ST-MARYS', 'MURRAY-STATE', 'NAVY', 'NEBRASKA-OMAHA',
            'NEBRASKA', 'NEVADA-LAS-VEGAS', 'NEVADA', 'NEW-HAMPSHIRE',
            'NEW-MEXICO-STATE', 'NEW-MEXICO', 'NEW-ORLEANS', 'NIAGARA',
            'NICHOLLS-STATE', 'NJIT', 'NORFOLK-STATE',
            'NORTH-CAROLINA-ASHEVILLE', 'NORTH-CAROLINA-AT',
            'NORTH-CAROLINA-CENTRAL', 'NORTH-CAROLINA-GREENSBORO',
            'NORTH-CAROLINA-STATE', 'NORTH-CAROLINA-WILMINGTON',
            'NORTH-CAROLINA', 'NORTH-DAKOTA-STATE', 'NORTH-DAKOTA',
            'NORTH-FLORIDA', 'NORTH-TEXAS', 'NORTHEASTERN', 'NORTHERN-ARIZONA',
            'NORTHERN-COLORADO', 'NORTHERN-ILLINOIS', 'NORTHERN-IOWA',
            'NORTHERN-KENTUCKY', 'NORTHWESTERN-STATE', 'NORTHWESTERN',
            'NOTRE-DAME', 'OAKLAND', 'OHIO-STATE', 'OHIO', 'OKLAHOMA-STATE',
            'OKLAHOMA', 'OLD-DOMINION', 'ORAL-ROBERTS', 'OREGON-STATE',
            'OREGON', 'PACIFIC', 'PENN-STATE', 'PENNSYLVANIA', 'PEPPERDINE',
            'PITTSBURGH', 'PORTLAND-STATE', 'PORTLAND', 'PRAIRIE-VIEW',
            'PRESBYTERIAN', 'PRINCETON', 'PROVIDENCE', 'PURDUE', 'QUINNIPIAC',
            'RADFORD', 'RHODE-ISLAND', 'RICE', 'RICHMOND', 'RIDER',
            'ROBERT-MORRIS', 'RUTGERS', 'SACRAMENTO-STATE', 'SACRED-HEART',
            'SAINT-FRANCIS-PA', 'SAINT-JOSEPHS', 'SAINT-LOUIS',
            'SAINT-MARYS-CA', 'SAINT-PETERS', 'SAM-HOUSTON-STATE', 'SAMFORD',
            'SAN-DIEGO-STATE', 'SAN-DIEGO', 'SAN-FRANCISCO', 'SAN-JOSE-STATE',
            'SANTA-CLARA', 'SAVANNAH-STATE', 'SEATTLE', 'SETON-HALL', 'SIENA',
            'SOUTH-ALABAMA', 'SOUTH-CAROLINA-STATE', 'SOUTH-CAROLINA-UPSTATE',
            'SOUTH-CAROLINA', 'SOUTH-DAKOTA-STATE', 'SOUTH-DAKOTA',
            'SOUTH-FLORIDA', 'SOUTHEAST-MISSOURI-STATE',
            'SOUTHEASTERN-LOUISIANA', 'SOUTHERN-CALIFORNIA',
            'SOUTHERN-ILLINOIS-EDWARDSVILLE', 'SOUTHERN-ILLINOIS',
            'SOUTHERN-METHODIST', 'SOUTHERN-MISSISSIPPI', 'SOUTHERN-UTAH',
            'SOUTHERN', 'ST-BONAVENTURE', 'ST-FRANCIS-NY', 'ST-JOHNS-NY',
            'STANFORD', 'STEPHEN-F-AUSTIN', 'STETSON', 'STONY-BROOK',
            'SYRACUSE', 'TEMPLE', 'TENNESSEE-MARTIN', 'TENNESSEE-STATE',
            'TENNESSEE-TECH', 'TENNESSEE', 'TEXAS-AM-CORPUS-CHRISTI',
            'TEXAS-AM', 'TEXAS-ARLINGTON', 'TEXAS-CHRISTIAN', 'TEXAS-EL-PASO',
            'TEXAS-PAN-AMERICAN', 'TEXAS-SAN-ANTONIO', 'TEXAS-SOUTHERN',
            'TEXAS-STATE', 'TEXAS-TECH', 'TEXAS', 'TOLEDO', 'TOWSON', 'TROY',
            'TULANE', 'TULSA', 'UCLA', 'UTAH-STATE', 'UTAH-VALLEY', 'UTAH',
            'VALPARAISO', 'VANDERBILT', 'VERMONT', 'VILLANOVA',
            'VIRGINIA-COMMONWEALTH', 'VIRGINIA-MILITARY-INSTITUTE',
            'VIRGINIA-TECH', 'VIRGINIA', 'WAGNER', 'WAKE-FOREST',
            'WASHINGTON-STATE', 'WASHINGTON', 'WEBER-STATE', 'WEST-VIRGINIA',
            'WESTERN-CAROLINA', 'WESTERN-ILLINOIS', 'WESTERN-KENTUCKY',
            'WESTERN-MICHIGAN', 'WICHITA-STATE', 'WILLIAM-MARY', 'WINTHROP',
            'WISCONSIN', 'WOFFORD', 'WRIGHT-STATE', 'WYOMING', 'XAVIER',
            'YALE', 'YOUNGSTOWN-STATE'
        ]

        team_conference = {'kansas': 'big-12',
                           'texas-tech': 'big-12',
                           'west-virginia': 'big-12',
                           'kansas-state': 'big-12',
                           'texas-christian': 'big-12',
                           'oklahoma-state': 'big-12',
                           'oklahoma': 'big-12',
                           'baylor': 'big-12',
                           'texas': 'big-12',
                           'iowa-state': 'big-12',
                           'xavier': 'big-east',
                           'villanova': 'big-east',
                           'seton-hall': 'big-east',
                           'creighton': 'big-east',
                           'providence': 'big-east',
                           'butler': 'big-east',
                           'marquette': 'big-east',
                           'georgetown': 'big-east',
                           'st-johns-ny': 'big-east',
                           'depaul': 'big-east',
                           'virginia': 'acc',
                           'duke': 'acc',
                           'clemson': 'acc',
                           'north-carolina': 'acc',
                           'miami-fl': 'acc',
                           'north-carolina-state': 'acc',
                           'virginia-tech': 'acc',
                           'florida-state': 'acc',
                           'louisville': 'acc',
                           'syracuse': 'acc',
                           'notre-dame': 'acc',
                           'boston-college': 'acc',
                           'georgia-tech': 'acc',
                           'wake-forest': 'acc',
                           'pittsburgh': 'acc',
                           'michigan-state': 'big-ten',
                           'purdue': 'big-ten',
                           'ohio-state': 'big-ten',
                           'michigan': 'big-ten',
                           'nebraska': 'big-ten',
                           'penn-state': 'big-ten',
                           'indiana': 'big-ten',
                           'maryland': 'big-ten',
                           'wisconsin': 'big-ten',
                           'northwestern': 'big-ten',
                           'minnesota': 'big-ten',
                           'illinois': 'big-ten',
                           'iowa': 'big-ten',
                           'rutgers': 'big-ten',
                           'auburn': 'sec',
                           'tennessee': 'sec',
                           'florida': 'sec',
                           'kentucky': 'sec',
                           'arkansas': 'sec',
                           'missouri': 'sec',
                           'mississippi-state': 'sec',
                           'texas-am': 'sec',
                           'alabama': 'sec',
                           'louisiana-state': 'sec',
                           'georgia': 'sec',
                           'south-carolina': 'sec',
                           'vanderbilt': 'sec',
                           'mississippi': 'sec',
                           'arizona': 'pac-12',
                           'southern-california': 'pac-12',
                           'utah': 'pac-12',
                           'ucla': 'pac-12',
                           'stanford': 'pac-12',
                           'oregon': 'pac-12',
                           'washington': 'pac-12',
                           'arizona-state': 'pac-12',
                           'colorado': 'pac-12',
                           'oregon-state': 'pac-12',
                           'washington-state': 'pac-12',
                           'california': 'pac-12',
                           'cincinnati': 'aac',
                           'houston': 'aac',
                           'wichita-state': 'aac',
                           'tulsa': 'aac',
                           'memphis': 'aac',
                           'central-florida': 'aac',
                           'temple': 'aac',
                           'connecticut': 'aac',
                           'southern-methodist': 'aac',
                           'tulane': 'aac',
                           'east-carolina': 'aac',
                           'south-florida': 'aac',
                           'nevada': 'mwc',
                           'boise-state': 'mwc',
                           'new-mexico': 'mwc',
                           'san-diego-state': 'mwc',
                           'fresno-state': 'mwc',
                           'wyoming': 'mwc',
                           'nevada-las-vegas': 'mwc',
                           'utah-state': 'mwc',
                           'air-force': 'mwc',
                           'colorado-state': 'mwc',
                           'san-jose-state': 'mwc',
                           'loyola-il': 'mvc',
                           'southern-illinois': 'mvc',
                           'illinois-state': 'mvc',
                           'drake': 'mvc',
                           'bradley': 'mvc',
                           'indiana-state': 'mvc',
                           'missouri-state': 'mvc',
                           'evansville': 'mvc',
                           'northern-iowa': 'mvc',
                           'valparaiso': 'mvc',
                           'rhode-island': 'atlantic-10',
                           'st-bonaventure': 'atlantic-10',
                           'davidson': 'atlantic-10',
                           'saint-josephs': 'atlantic-10',
                           'virginia-commonwealth': 'atlantic-10',
                           'saint-louis': 'atlantic-10',
                           'george-mason': 'atlantic-10',
                           'richmond': 'atlantic-10',
                           'dayton': 'atlantic-10',
                           'duquesne': 'atlantic-10',
                           'george-washington': 'atlantic-10',
                           'la-salle': 'atlantic-10',
                           'massachusetts': 'atlantic-10',
                           'fordham': 'atlantic-10',
                           'gonzaga': 'wcc',
                           'saint-marys-ca': 'wcc',
                           'brigham-young': 'wcc',
                           'san-diego': 'wcc',
                           'san-francisco': 'wcc',
                           'pacific': 'wcc',
                           'santa-clara': 'wcc',
                           'loyola-marymount': 'wcc',
                           'portland': 'wcc',
                           'pepperdine': 'wcc',
                           'middle-tennessee': 'cusa',
                           'old-dominion': 'cusa',
                           'western-kentucky': 'cusa',
                           'marshall': 'cusa',
                           'texas-san-antonio': 'cusa',
                           'alabama-birmingham': 'cusa',
                           'north-texas': 'cusa',
                           'florida-international': 'cusa',
                           'louisiana-tech': 'cusa',
                           'southern-mississippi': 'cusa',
                           'florida-atlantic': 'cusa',
                           'texas-el-paso': 'cusa',
                           'rice': 'cusa',
                           'charlotte': 'cusa',
                           'buffalo': 'mac',
                           'kent-state': 'mac',
                           'miami-oh': 'mac',
                           'bowling-green-state': 'mac',
                           'ohio': 'mac',
                           'akron': 'mac',
                           'toledo': 'mac',
                           'eastern-michigan': 'mac',
                           'ball-state': 'mac',
                           'western-michigan': 'mac',
                           'central-michigan': 'mac',
                           'northern-illinois': 'mac',
                           'south-dakota-state': 'summit',
                           'south-dakota': 'summit',
                           'denver': 'summit',
                           'ipfw': 'summit',
                           'north-dakota-state': 'summit',
                           'oral-roberts': 'summit',
                           'nebraska-omaha': 'summit',
                           'western-illinois': 'summit',
                           'louisiana-lafayette': 'sun-belt',
                           'georgia-state': 'sun-belt',
                           'georgia-southern': 'sun-belt',
                           'texas-arlington': 'sun-belt',
                           'louisiana-monroe': 'sun-belt',
                           'troy': 'sun-belt',
                           'appalachian-state': 'sun-belt',
                           'coastal-carolina': 'sun-belt',
                           'texas-state': 'sun-belt',
                           'south-alabama': 'sun-belt',
                           'arkansas-state': 'sun-belt',
                           'arkansas-little-rock': 'sun-belt',
                           'college-of-charleston': 'colonial',
                           'northeastern': 'colonial',
                           'hofstra': 'colonial',
                           'william-mary': 'colonial',
                           'towson': 'colonial',
                           'north-carolina-wilmington': 'colonial',
                           'elon': 'colonial',
                           'delaware': 'colonial',
                           'drexel': 'colonial',
                           'james-madison': 'colonial',
                           'montana': 'big-sky',
                           'idaho': 'big-sky',
                           'weber-state': 'big-sky',
                           'eastern-washington': 'big-sky',
                           'northern-colorado': 'big-sky',
                           'portland-state': 'big-sky',
                           'idaho-state': 'big-sky',
                           'montana-state': 'big-sky',
                           'north-dakota': 'big-sky',
                           'southern-utah': 'big-sky',
                           'sacramento-state': 'big-sky',
                           'northern-arizona': 'big-sky',
                           'new-mexico-state': 'wac',
                           'utah-valley': 'wac',
                           'grand-canyon': 'wac',
                           'seattle': 'wac',
                           'texas-pan-american': 'wac',
                           'cal-state-bakersfield': 'wac',
                           'missouri-kansas-city': 'wac',
                           'chicago-state': 'wac',
                           'california-davis': 'big-west',
                           'california-santa-barbara': 'big-west',
                           'california-irvine': 'big-west',
                           'cal-state-fullerton': 'big-west',
                           'long-beach-state': 'big-west',
                           'hawaii': 'big-west',
                           'cal-poly': 'big-west',
                           'california-riverside': 'big-west',
                           'cal-state-northridge': 'big-west',
                           'pennsylvania': 'ivy',
                           'harvard': 'ivy',
                           'yale': 'ivy',
                           'cornell': 'ivy',
                           'princeton': 'ivy',
                           'columbia': 'ivy',
                           'brown': 'ivy',
                           'dartmouth': 'ivy',
                           'rider': 'maac',
                           'canisius': 'maac',
                           'niagara': 'maac',
                           'iona': 'maac',
                           'fairfield': 'maac',
                           'manhattan': 'maac',
                           'quinnipiac': 'maac',
                           'monmouth': 'maac',
                           'saint-peters': 'maac',
                           'siena': 'maac',
                           'marist': 'maac',
                           'north-carolina-greensboro': 'southern',
                           'east-tennessee-state': 'southern',
                           'furman': 'southern',
                           'wofford': 'southern',
                           'mercer': 'southern',
                           'western-carolina': 'southern',
                           'samford': 'southern',
                           'citadel': 'southern',
                           'virginia-military-institute': 'southern',
                           'chattanooga': 'southern',
                           'murray-state': 'ovc',
                           'belmont': 'ovc',
                           'austin-peay': 'ovc',
                           'jacksonville-state': 'ovc',
                           'tennessee-tech': 'ovc',
                           'tennessee-state': 'ovc',
                           'southeast-missouri-state': 'ovc',
                           'eastern-illinois': 'ovc',
                           'eastern-kentucky': 'ovc',
                           'tennessee-martin': 'ovc',
                           'southern-illinois-edwardsville': 'ovc',
                           'morehead-state': 'ovc',
                           'vermont': 'america-east',
                           'maryland-baltimore-county': 'america-east',
                           'hartford': 'america-east',
                           'albany-ny': 'america-east',
                           'stony-brook': 'america-east',
                           'massachusetts-lowell': 'america-east',
                           'new-hampshire': 'america-east',
                           'maine': 'america-east',
                           'binghamton': 'america-east',
                           'northern-kentucky': 'horizon',
                           'wright-state': 'horizon',
                           'illinois-chicago': 'horizon',
                           'oakland': 'horizon',
                           'milwaukee': 'horizon',
                           'iupui': 'horizon',
                           'green-bay': 'horizon',
                           'cleveland-state': 'horizon',
                           'youngstown-state': 'horizon',
                           'detroit-mercy': 'horizon',
                           'north-carolina-asheville': 'big-south',
                           'radford': 'big-south',
                           'winthrop': 'big-south',
                           'campbell': 'big-south',
                           'liberty': 'big-south',
                           'charleston-southern': 'big-south',
                           'high-point': 'big-south',
                           'gardner-webb': 'big-south',
                           'presbyterian': 'big-south',
                           'longwood': 'big-south',
                           'bucknell': 'patriot',
                           'colgate': 'patriot',
                           'navy': 'patriot',
                           'lehigh': 'patriot',
                           'boston-university': 'patriot',
                           'holy-cross': 'patriot',
                           'lafayette': 'patriot',
                           'army': 'patriot',
                           'loyola-md': 'patriot',
                           'american': 'patriot',
                           'florida-gulf-coast': 'atlantic-sun',
                           'lipscomb': 'atlantic-sun',
                           'jacksonville': 'atlantic-sun',
                           'njit': 'atlantic-sun',
                           'north-florida': 'atlantic-sun',
                           'kennesaw-state': 'atlantic-sun',
                           'stetson': 'atlantic-sun',
                           'south-carolina-upstate': 'atlantic-sun',
                           'nicholls-state': 'southland',
                           'southeastern-louisiana': 'southland',
                           'stephen-f-austin': 'southland',
                           'sam-houston-state': 'southland',
                           'lamar': 'southland',
                           'new-orleans': 'southland',
                           'central-arkansas': 'southland',
                           'abilene-christian': 'southland',
                           'mcneese-state': 'southland',
                           'texas-am-corpus-christi': 'southland',
                           'incarnate-word': 'southland',
                           'houston-baptist': 'southland',
                           'northwestern-state': 'southland',
                           'wagner': 'northeast',
                           'saint-francis-pa': 'northeast',
                           'mount-st-marys': 'northeast',
                           'long-island-university': 'northeast',
                           'st-francis-ny': 'northeast',
                           'robert-morris': 'northeast',
                           'fairleigh-dickinson': 'northeast',
                           'central-connecticut-state': 'northeast',
                           'sacred-heart': 'northeast',
                           'bryant': 'northeast',
                           'grambling': 'swac',
                           'prairie-view': 'swac',
                           'texas-southern': 'swac',
                           'arkansas-pine-bluff': 'swac',
                           'southern': 'swac',
                           'jackson-state': 'swac',
                           'alabama-state': 'swac',
                           'alcorn-state': 'swac',
                           'mississippi-valley-state': 'swac',
                           'alabama-am': 'swac',
                           'bethune-cookman': 'meac',
                           'savannah-state': 'meac',
                           'hampton': 'meac',
                           'north-carolina-at': 'meac',
                           'norfolk-state': 'meac',
                           'north-carolina-central': 'meac',
                           'morgan-state': 'meac',
                           'howard': 'meac',
                           'florida-am': 'meac',
                           'south-carolina-state': 'meac',
                           'coppin-state': 'meac',
                           'maryland-eastern-shore': 'meac',
                           'delaware-state': 'meac'}

        flexmock(utils) \
            .should_receive('_todays_date') \
            .and_return(MockDateTime(YEAR, MONTH))

        flexmock(Conferences) \
            .should_receive('_find_conferences') \
            .and_return(None)
        flexmock(Conferences) \
            .should_receive('team_conference') \
            .and_return(team_conference)

        self.teams = Teams()

    def test_ncaab_integration_returns_correct_number_of_teams(self):
        assert len(self.teams) == len(self.abbreviations)

    def test_ncaab_integration_returns_correct_attributes_for_team(self):
        purdue = self.teams('PURDUE')

        for attribute, value in self.results.items():
            assert getattr(purdue, attribute) == value

    def test_ncaab_integration_returns_correct_team_abbreviations(self):
        for team in self.teams:
            assert team.abbreviation in self.abbreviations

    def test_ncaab_integration_dataframe_returns_dataframe(self):
        df = pd.DataFrame([self.results], index=['PURDUE'])

        purdue = self.teams('PURDUE')
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, purdue.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_ncaab_integration_all_teams_dataframe_returns_dataframe(self):
        result = self.teams.dataframes.drop_duplicates(keep=False)

        assert len(result) == len(self.abbreviations)
        assert set(result.columns.values) == set(self.results.keys())

    def test_ncaab_invalid_team_name_raises_value_error(self):
        with pytest.raises(ValueError):
            self.teams('INVALID_NAME')
