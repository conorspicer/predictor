from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Team(models.Model):
    DEN = 'DEN'
    CAR = 'CAR'
    TB = 'TB'
    ATL = 'ATL'
    BAL = 'BAL'
    BUF = 'BUF'
    HOU = 'HOU'
    CHI = 'CHI'
    JAC = 'JAC'
    GB = 'GB'
    KC = 'KC'
    LAC = 'LAC'
    NO = 'NO'
    OAK = 'OAK'
    NYJ = 'NYJ'
    CIN = 'CIN'
    PHI = 'PHI'
    CLE = 'CLE'
    TEN = 'TEN'
    MIN = 'MIN'
    SEA = 'SEA'
    MIA = 'MIA'
    DAL = 'DAL'
    NYG = 'NYG'
    IND = 'IND'
    DET = 'DET'
    ARI = 'ARI'
    NE = 'NE'
    WAS = 'WAS'
    PIT = 'PIT'
    SF = 'SF'
    LA = 'LA'

    NAMES = (
        (DEN, 'DEN'),
        (CAR, 'CAR'),
        (TB, 'TB'),
        (ATL, 'ATL'),
        (BAL, 'BAL'),
        (BUF, 'BUF'),
        (HOU, 'HOU'),
        (CHI, 'CHI'),
        (JAC, 'JAC'),
        (GB, 'GB'),
        (KC, 'KC'),
        (LAC, 'LAC'),
        (NO, 'NO'),
        (OAK, 'OAK'),
        (NYJ, 'NYJ'),
        (CIN, 'CIN'),
        (PHI, 'PHI'),
        (CLE, 'CLE'),
        (TEN, 'TEN'),
        (MIN, 'MIN'),
        (SEA, 'SEA'),
        (MIA, 'MIA'),
        (DAL, 'DAL'),
        (NYG, 'NYG'),
        (IND, 'IND'),
        (DET, 'DET'),
        (ARI, 'ARI'),
        (NE, 'NE'),
        (WAS, 'WAS'),
        (PIT, 'PIT'),
        (SF, 'SF'),
        (LA, 'LA'),
    )

    Bills = 'Bills'
    Dolphins = 'Dolphins'
    Patriots = 'Patriots'
    Jets = 'Jets'
    Ravens = 'Ravens'
    Bengals = 'Bengals'
    Browns = 'Browns'
    Steelers = 'Steelers'
    Texans = 'Texans'
    Colts = 'Colts'
    Jaguars = 'Jaguars'
    Titans = 'Titans'
    Broncos = 'Broncos'
    Chiefs = 'Chiefs'
    Raiders = 'Raiders'
    Chargers = 'Chargers'
    Cowboys = 'Cowboys'
    Giants = 'Giants'
    Eagles = 'Eagles'
    Redskins = 'Redskins'
    Bears = 'Bears'
    Lions = 'Lions'
    Packers = 'Packers'
    Vikings = 'Vikings'
    Falcons = 'Falcons'
    Panthers = 'Panthers'
    Saints = 'Saints'
    Buccaneers = 'Buccaneers'
    Cardinals = 'Cardinals'
    Rams = 'Rams'
    forty = '49ers'
    Seahawks = 'Seahawks'

    TEAMS = (
        (Bills, 'Bills'),
        (Dolphins, 'Dolphins'),
        (Patriots, 'Patriots'),
        (Jets, 'Jets'),
        (Ravens, 'Ravens'),
        (Bengals, 'Bengals'),
        (Browns, 'Browns'),
        (Steelers, 'Steelers'),
        (Texans, 'Texans'),
        (Colts, 'Colts'),
        (Jaguars, 'Jaguars'),
        (Titans, 'Titans'),
        (Broncos, 'Broncos'),
        (Chiefs, 'Chiefs'),
        (Raiders, 'Raiders'),
        (Chargers, 'Chargers'),
        (Cowboys, 'Cowboys'),
        (Giants, 'Giants'),
        (Eagles, 'Eagles'),
        (Redskins, 'Redskins'),
        (Bears, 'Bears'),
        (Lions, 'Lions'),
        (Packers, 'Packers'),
        (Vikings, 'Vikings'),
        (Falcons, 'Falcons'),
        (Panthers, 'Panthers'),
        (Saints, 'Saints'),
        (Buccaneers, 'Buccaneers'),
        (Cardinals, 'Cardinals'),
        (Rams, 'Rams'),
        (forty, '49ers'),
        (Seahawks, 'Seahawks'),
    )

    AFC = 'AFC'
    NFC = 'NFC'
    CONFS = (
        (AFC, 'AFC'),
        (NFC, 'NFC'),
    )

    AFC_EAST = 'AFC_EAST'
    AFC_NORTH = 'AFC_NORTH'
    AFC_SOUTH = 'AFC_SOUTH'
    AFC_WEST = 'AFC_WEST'
    NFC_EAST = 'NFC_EAST'
    NFC_NORTH = 'NFC_NORTH'
    NFC_SOUTH = 'NFC_SOUTH'
    NFC_WEST = 'NFC_WEST'

    DIVISIONS = (
        (AFC_EAST, 'AFC_EAST'),
        (AFC_NORTH, 'AFC_NORTH'),
        (AFC_SOUTH, 'AFC_SOUTH'),
        (AFC_WEST, 'AFC_WEST'),
        (NFC_EAST, 'NFC_EAST'),
        (NFC_NORTH, 'NFC_NORTH'),
        (NFC_SOUTH, 'NFC_SOUTH'),
        (NFC_WEST, 'NFC_WEST'),
    )

    short_name = models.CharField(max_length=5, choices=NAMES, null=True)
    city_name = models.CharField(max_length=50, null=True)
    team_name = models.CharField(max_length=50, choices=TEAMS, null=True)
    full_name = models.CharField(max_length=50, null=True)
    division = models.CharField(max_length=50, choices=DIVISIONS, null=True)
    conference = models.CharField(max_length=5, choices=CONFS, null=True, default='AFC')
    team_logo = models.ImageField(upload_to='logos', blank=True)
    # playoff = models.BooleanField(default=False)

    def __str__(self):
        return self.team_name


class Fixture(models.Model):
    name = models.CharField(max_length=56)
    away_team = models.ForeignKey(Team, null=True, related_name="away", on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, null=True, related_name="home", on_delete=models.CASCADE)
    away_score = models.PositiveIntegerField(blank=True)
    home_score = models.PositiveIntegerField(blank=True)
    week = models.PositiveIntegerField()
    ko_datetime = models.DateTimeField(blank=True, null=True)
    changeable = models.BooleanField(default=True)

    def _get_winner(self):
        if self.home_score > self.away_score:
            return self.home_team
        if self.away_score > self.home_score:
            return self.away_team
        elif self.ko_datetime > timezone.now():
            return 'Not Played'
        else:
            return 'Tie'
    winner = property(_get_winner)

    def _get_margin(self):
        if self.ko_datetime > timezone.now():
            return 269854
        else:
            return abs(self.home_score - self.away_score)
    margin = property(_get_margin)

    def _get_totalpts(self):
        if self.ko_datetime > timezone.now():
            return 23956
        else:
            return self.home_score + self.away_score
    total_pts = property(_get_totalpts)

    def __str__(self):
        return ' '.join([
            "Week",
            str(self.week),
            " - ",
            self.away_team.team_name,
            " @ ",
            self.home_team.team_name,
        ])
