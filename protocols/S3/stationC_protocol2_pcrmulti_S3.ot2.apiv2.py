from opentrons import protocol_api
from opentrons.types import Point
from opentrons.drivers.rpi_drivers import gpio
import time
import math
import os
import sys
import subprocess
import json
from datetime import datetime
custom_modules_path = "/var/user-packages/usr/lib/python3.7/site-packages"
if custom_modules_path not in sys.path:
    sys.path.append(custom_modules_path)
import requests


# Metadata
metadata = {
    'protocolName': 'S3 Station C Protocol 2 pcrmulti Version 1',
    'author': 'Nick <protocols@opentrons.com>, Sara <smonzon@isciii.es>, Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}

# Parameters to adapt the protocol
# Warning writing any Parameters below this line.
# It will be deleted if opentronsWeb is used.

NUM_SAMPLES = 96
PCR_LABWARE = 'opentrons aluminum biorad plate'
MM_LABWARE = 'opentrons aluminum block'
ELUTION_LABWARE = 'opentrons aluminum nest plate'
VOLUME_ELUTION = 7
LANGUAGE = 'esp'
RESET_TIPCOUNT = False
PROTOCOL_ID = "0000-AA"
URL = "localhost"

# End Parameters to adapt the protocol
ACTION = "StationC-protocol2-pcrmulti"

## global vars
## initialize robot object
robot = None
# default var for drop tip switching
switch = True
# initialize tip_log dictionary
tip_log = {}
tip_log['count'] = {}
tip_log['tips'] = {}
tip_log['max'] = {}

"""
NUM_SAMPLES is the number of samples, must be an integer number

MM_LABWARE must be one of the following:
    opentrons plastic block
    pentrons aluminum block
    covidwarriors aluminum block

PCR_LABWARE must be one of the following:
    opentrons aluminum biorad plate
    opentrons aluminum nest plate
    opentrons aluminum strip short
    covidwarriors aluminum biorad plate
    covidwarriors aluminum biorad strip short

ELUTION_LABWARE must be one of the following:
    opentrons plastic 2ml tubes
    opentrons plastic 1.5ml tubes
    opentrons aluminum 2ml tubes
    opentrons aluminum 1.5ml tubes
    covidwarriors aluminum 2ml tubes
    covidwarriors aluminum 1.5ml tubes
    opentrons aluminum biorad plate
    opentrons aluminum nest plate
    covidwarriors aluminum biorad plate
    opentrons aluminum strip alpha
    opentrons aluminum strip short
    covidwarriors aluminum biorad strip alpha
    covidwarriors aluminum biorad strip short

"""

# Constants
MM_LW_DICT = {
    'opentrons plastic block': 'opentrons_24_tuberack_generic_2ml_screwcap',
    'opentrons aluminum block': 'opentrons_24_aluminumblock_generic_2ml_screwcap',
    'covidwarriors aluminum block': 'covidwarriors_aluminumblock_24_screwcap_2000ul'
}

PCR_LW_DICT = {
    'opentrons aluminum biorad plate': 'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    'opentrons aluminum nest plate': 'opentrons_96_aluminumblock_nest_wellplate_100ul',
    'opentrons aluminum strip short': 'opentrons_aluminumblock_96_pcrstrips_100ul',
    'covidwarriors aluminum biorad plate': 'covidwarriors_aluminumblock_96_bioradwellplate_200ul',
    'covidwarriors aluminum biorad strip short': 'covidwarriors_aluminumblock_96_bioradwellplate_pcrstrips_100ul'
}

EL_LW_DICT = {
    # PCR plate
    'opentrons aluminum biorad plate': 'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    'opentrons aluminum nest plate': 'opentrons_96_aluminumblock_nest_wellplate_100ul',
    'covidwarriors aluminum biorad plate': 'covidwarriors_aluminumblock_96_bioradwellplate_200ul',
    # Strips
    #'large strips': 'opentrons_96_aluminumblock_generic_pcr_strip_200ul',
    #'short strips': 'opentrons_96_aluminumblock_generic_pcr_strip_200ul',
    'opentrons aluminum strip alpha': 'opentrons_aluminumblock_96_pcrstripsalpha_200ul',
    'opentrons aluminum strip short': 'opentrons_aluminumblock_96_pcrstrips_100ul',
    'covidwarriors aluminum biorad strip alpha': 'covidwarriors_aluminumblock_96_bioradwellplate_pcrstripsalpha_200ul',
    'covidwarriors aluminum biorad strip short': 'covidwarriors_aluminumblock_96_bioradwellplate_pcrstrips_100ul'
}

LANGUAGE_DICT = {
    'esp': 'esp',
    'eng': 'eng'
}

if LANGUAGE_DICT[LANGUAGE] == 'eng':
    VOICE_FILES_DICT = {
        'start': './data/sounds/started_process.mp3',
        'finish': './data/sounds/finished_process.mp3',
        'close_door': './data/sounds/close_door.mp3',
        'replace_tipracks': './data/sounds/replace_tipracks.mp3',
        'empty_trash': './data/sounds/empty_trash.mp3'
    }
elif LANGUAGE_DICT[LANGUAGE] == 'esp':
    VOICE_FILES_DICT = {
        'start': './data/sounds/started_process_esp.mp3',
        'finish': './data/sounds/finished_process_esp.mp3',
        'close_door': './data/sounds/close_door_esp.mp3',
        'replace_tipracks': './data/sounds/replace_tipracks_esp.mp3',
        'empty_trash': './data/sounds/empty_trash_esp.mp3'
    }


# Function definitions

def write_to_error_log (info, reason):
    date = datetime.now().strftime("%Y_%m_%d")
    folder_date = os.path.join('/data/logs', date)
    time_now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    json_file = time_now + '.json'
    folder_file_name = os.path.join(folder_date, json_file)
    folder_error_log = os.path.join(folder_date,'error.log')
    if not os.path.exists(folder_date):
        try:
            os.makedirs(folder_date)
        except:
            return
    try:
        with open (folder_file_name , 'w') as fh:
            json.dump(info, fh, indent=4)
        with open(folder_error_log, 'a') as fh:
            fh.write( time_now +  '  Unable to accept the requests get error : '+ reason + '\n')
    except:
        return

def run_info(start,end,parameters = dict()):
    info = {}
    hostname = subprocess.run(
        ['hostname'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).stdout.decode('utf-8')

    info["RobotID"] = hostname
    info["executedAction"] = ACTION
    info["ProtocolID"] = PROTOCOL_ID
    info["StartRunTime"] = start
    info["FinishRunTime"] = end
    info["parameters"] = parameters

    headers = {'Content-type': 'application/json'}
    url_https = 'https://' + URL
    url_http = 'http://' + URL
    try:
        r = requests.post(url_https, data=json.dumps(info), headers=headers)
    except:
        try:
            r = requests.post(url_http, data=json.dumps(info), headers=headers)
        except:
            write_to_error_log(info, 'Server communication error')
            return
    if r.status_code > 201 :
        write_to_error_log(info, str(r.status_code))

def check_door():
    return gpio.read_window_switches()

def confirm_door_is_closed():
    if not robot.is_simulating():
        #Check if door is opened
        if check_door() == False:
            #Set light color to red and pause
            gpio.set_button_light(1,0,0)
            robot.pause()
            voice_notification('close_door')
            time.sleep(5)
            confirm_door_is_closed()
        else:
            #Set light color to green
            gpio.set_button_light(0,1,0)

def start_run():
    voice_notification('start')
    gpio.set_button_light(0,1,0)
    now = datetime.now()
    # dd/mm/YY H:M:S
    start_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return start_time

def finish_run():
    voice_notification('finish')
    #Set light color to blue
    gpio.set_button_light(0,0,1)
    now = datetime.now()
    # dd/mm/YY H:M:S
    finish_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return finish_time

def voice_notification(action):
    if not robot.is_simulating():
        fname = VOICE_FILES_DICT[action]
        if os.path.isfile(fname) is True:
                subprocess.run(
                ['mpg123', fname],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
                )
        else:
            robot.comment(f"Sound file does not exist. Call the technician")

def reset_tipcount(file_path = '/data/C/tip_log.json'):
    if os.path.isfile(file_path):
        os.remove(file_path)

def retrieve_tip_info(pip,tipracks,file_path = '/data/C/tip_log.json'):
    global tip_log
    if not tip_log['count'] or pip not in tip_log['count']:
        tip_log['count'][pip] = 0
        if not robot.is_simulating():
            if os.path.isfile(file_path):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    if 'P1000' in str(pip):
                        tip_log['count'][pip] = data['tips1000']
                    elif 'P300' in str(pip) and 'Single-Channel' in str(pip):
                        tip_log['count'][pip] = data['tips300']
                    elif 'P300' in str(pip) and '8-Channel' in str(pip):
                        tip_log['count'][pip] = data['tipsm300']
                    elif 'P20' in str(pip) and 'Single-Channel' in str(pip):
                        tip_log['count'][pip] = data['tips20']
                    elif 'P20' in str(pip) and '8-Channel' in str(pip):
                        tip_log['count'][pip] = data['tipsm20']

        if "8-Channel" in str(pip):
            tip_log['tips'][pip] =  [tip for rack in tipracks for tip in rack.rows()[0]]
        else:
            tip_log['tips'][pip] = [tip for rack in tipracks for tip in rack.wells()]

        tip_log['max'][pip] = len(tip_log['tips'][pip])

    return tip_log

def save_tip_info(file_path = '/data/C/tip_log.json'):
    data = {}
    if not robot.is_simulating():
        if os.path.isfile(file_path):
            os.rename(file_path,file_path + ".bak")
        for pip in tip_log['count']:
            if "P1000" in str(pip):
                data['tips1000'] = tip_log['count'][pip]
            elif 'P300' in str(pip) and 'Single-Channel' in str(pip):
                data['tips300'] = tip_log['count'][pip]
            elif 'P300' in str(pip) and '8-Channel' in str(pip):
                data['tipsm300'] = tip_log['count'][pip]
            elif 'P20' in str(pip) and 'Single-Channel' in str(pip):
                data['tips20'] = tip_log['count'][pip]
            elif 'P20' in str(pip) and '8-Channel' in str(pip):
                data['tipsm20'] = tip_log['count'][pip]

        with open(file_path, 'a+') as outfile:
            json.dump(data, outfile)


def pick_up(pip,tiprack):
    if tip_log['count'][pip] == tip_log['max'][pip]:
        voice_notification('replace_tipracks')
        robot.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
        confirm_door_is_closed()
        pip.reset_tipracks()
        tip_log['count'][pip] = 0
    pip.pick_up_tip(tip_log['tips'][pip][tip_log['count'][pip]])
    tip_log['count'][pip] += 1

def drop(pip):
    global switch
    if "8-Channel" not in str(pip):
        side = 1 if switch else -1
        drop_loc = robot.loaded_labwares[12].wells()[0].top().move(Point(x=side*20))
        pip.drop_tip(drop_loc,home_after=False)
        switch = not switch
    else:
        drop_loc = robot.loaded_labwares[12].wells()[0].top().move(Point(x=20))
        pip.drop_tip(drop_loc,home_after=False)

def get_source_dest_coordinates(source_racks, pcr_plate):
    # Keep floor
    num_cols = math.floor(NUM_SAMPLES/8)
    # Keep the remaining samples
    num_samples_m = int(num_cols*8)

    if 'strip' in ELUTION_LABWARE:
        if NUM_SAMPLES > 8:
            sources_m = [
                col
                for i, rack in enumerate(source_racks)
                for col in [
                    rack.columns()[c] if i < 2 else rack.columns()[c+1]
                    for c in [0, 5, 10]
                ]
            ][:num_cols]

        sources_s = [
            well
            for i, rack in enumerate(source_racks)
            for col in [
                rack.columns()[c] if i < 2 else rack.columns()[c+1]
                for c in [0, 5, 10]
            ]
            for well in col
        ][num_samples_m:NUM_SAMPLES]

    elif 'plate' in ELUTION_LABWARE:
        sources_m = source_racks.rows()[0][:num_cols]
        sources_s = source_racks.wells()[num_samples_m:NUM_SAMPLES]

    dests_m = pcr_plate.rows()[0][:num_cols]
    dests_s = pcr_plate.wells()[num_samples_m:NUM_SAMPLES]
    return sources_m, sources_s, dests_m, dests_s

def transfer_samples(sources, dests, pip,tiprack):
    # height for aspiration has to be different depending if you ar using tubes or wells
    if 'strip' in ELUTION_LABWARE or 'plate' in ELUTION_LABWARE:
        height = 1.5
    else:
        height = 1
    # transfer
    for s, d in zip(sources, dests):
        # Skip for negative control, position NUM_SAMPLES-2
        #if s == sources[NUM_SAMPLES-2]:
        #    continue

        pick_up(pip,tiprack)
        pip.transfer(VOLUME_ELUTION, s.bottom(height), d.bottom(2), air_gap=2, new_tip='never')
        #p20.mix(1, 10, d.bottom(2))
        #p20.blow_out(d.top(-2))
        pip.aspirate(1, d.top(-2))
        drop(pip)

# RUN PROTOCOL
def run(ctx: protocol_api.ProtocolContext):
    global robot

    # Set robot as global var
    robot = ctx

    # check if tipcount is being reset
    if RESET_TIPCOUNT:
        reset_tipcount()

    # confirm door is closed
    robot.comment(f"Please, close the door")
    confirm_door_is_closed()

    # Begin run
    start_time = start_run()

    # define tips
    tips20 = [
        robot.load_labware('opentrons_96_filtertiprack_20ul', 6)
    ]
    tipsm20 = [
        robot.load_labware('opentrons_96_filtertiprack_20ul', 3)
    ]

    if MM_LABWARE not in MM_LW_DICT:
        raise Exception('Invalid MM_LABWARE. Must be one of the following:\n' + '\n'.join(list(MM_LW_DICT.keys())))


    # load mastermix labware
    mm_rack = robot.load_labware(
        MM_LW_DICT[MM_LABWARE], '11',
        MM_LABWARE)


    # define pipettes
    p20 = robot.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    m20 = robot.load_instrument('p20_multi_gen2', 'left', tip_racks=tipsm20)

    ## retrieve tip_log
    retrieve_tip_info(p20,tips20)
    retrieve_tip_info(m20,tipsm20)

    # tempdeck module
    tempdeck = robot.load_module('tempdeck', '10')
    # tempdeck.set_temperature(4)

    # check pcr plate
    if PCR_LABWARE not in PCR_LW_DICT:
        raise Exception('Invalid PCR_LABWARE. Must be one of the following:\n' + '\n'.join(list(PCR_LW_DICT.keys())))


    # load pcr plate
    pcr_plate = tempdeck.load_labware(
        PCR_LW_DICT[PCR_LABWARE], 'PCR plate')

    # check source (elution) labware type
    if ELUTION_LABWARE not in EL_LW_DICT:
        raise Exception('Invalid ELUTION_LABWARE. Must be one of the following:\n' + '\n'.join(list(EL_LW_DICT.keys())))

    # load elution labware
    if 'plate' in ELUTION_LABWARE:
        source_racks = robot.load_labware(
            EL_LW_DICT[ELUTION_LABWARE], '1',
            'RNA elution labware')
    else:
        source_racks = [
            robot.load_labware(EL_LW_DICT[ELUTION_LABWARE], slot,
                            'RNA elution labware ' + str(i+1))
            for i, slot in enumerate(['4', '1', '5', '2'])
    ]

    # setup sample sources and destinations
    sources_m, sources_s, dests_m, dests_s = get_source_dest_coordinates(source_racks, pcr_plate)

    # transfer samples to corresponding locations
    if NUM_SAMPLES >= 8:
        transfer_samples(sources_m,dests_m,m20,tipsm20)
    transfer_samples(sources_s, dests_s, p20,tips20)

    # transfer negative control to position NUM_SAMPLES-2
    pick_up(p20, tips20)
    dests = pcr_plate.wells()[:NUM_SAMPLES]
    p20.transfer(VOLUME_ELUTION, mm_rack.wells()[4].bottom(1), dests[NUM_SAMPLES-2].bottom(2), air_gap=2, new_tip='never')
    drop(p20)

    # track final used tip
    save_tip_info()

    finish_time = finish_run()

    par = {
        "NUM_SAMPLES" : NUM_SAMPLES,
        "MM_LABWARE" : MM_LABWARE,
        "PCR_LABWARE" : PCR_LABWARE,
        "ELUTION_LABWARE" : ELUTION_LABWARE,
        "VOLUME_ELUTION" : VOLUME_ELUTION,
        "LANGUAGE" : LANGUAGE,
        "RESET_TIPCOUNT" : RESET_TIPCOUNT
    }

    run_info(start_time, finish_time, par)
