#!/usr/bin/python
# encoding=utf8
import time
import pexpect
import subprocess
import sys
import bluetooth
import connection_class
import json
from pymongo import MongoClient
from datetime import datetime
import pymysql
import threading

target_name = "HC-05-01"  # Device name
port = 1  # RFCOMM port
target_address = None
End = '\n'  # something useable as an end marker
DATABASE_URL = "mongodb://localhost:27017"


#
################################################################################
#
#   Bluetooth Connection Class Error Hendler
#
class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass


#
################################################################################
#
#   Bluetooth Connection Class
#
class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell=True)
        self.child = pexpect.spawn("bluetoothctl", echo=False)

    def get_output(self, command, pause=0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n")

    def power_on(self):
        """Bluetooth on."""
        try:
            out = self.get_output("power on")
        except BluetoothctlError, e:
            print(e)
            return None

    def pairable_on(self):
        """Make Bluetooth pairable."""
        try:
            out = self.get_output("pairable on")
        except BluetoothctlError, e:
            print(e)
            return None

    def agent_on(self):
        """Make bluetooth agent on."""
        try:
            out = self.get_output("agent on")
        except BluetoothctlError, e:
            print(e)
            return None

    def default_agent(self):
        """Make bluetooth default-agent."""
        try:
            out = self.get_output("default-agent")
        except BluetoothctlError, e:
            print(e)
            return None

    def start_scan(self):
        """Start bluetooth scanning process."""
        try:
            out = self.get_output("scan on")
        except BluetoothctlError, e:
            print(e)
            return None

    def stop_scan(self):
        """Stop bluetooth scanning process."""
        try:
            out = self.get_output("scan off")
        except BluetoothctlError, e:
            print(e)
            return None

    def make_discoverable(self):
        """Make device discoverable."""
        try:
            out = self.get_output("discoverable on")
        except BluetoothctlError, e:
            print(e)
            return None

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2]
                    }

        return device

    def parse_device_full_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Connected")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    device = {
                        "connected": attribute_list[1]
                    }

        return device

    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        try:
            out = self.get_output("devices")
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            out = self.get_output("paired-devices")
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)

            return paired_devices

    def get_discoverable_devices(self):
        """Filter paired devices out of available."""
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]

    def get_device_full_info(self, mac_address):
        """Get device info by mac address and return info."""
        try:
            out = self.get_output("info " + mac_address)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            devices = []
            for line in out:
                device = self.parse_device_full_info(line)
                if device:
                    devices.append(device)

            return devices

    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            out = self.get_output("pair " + mac_address, 4)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def remove(self, mac_address):
        """Remove paired device by mac address, return success of the operation."""
        try:
            out = self.get_output("remove " + mac_address, 3)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["not available", "Device has been removed", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address, 2)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def disconnect(self, mac_address):
        """Try to disconnect to a device by mac address."""
        try:
            out = self.get_output("disconnect " + mac_address, 2)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def recv_data(self, the_socket):
        """Recieve data."""
        total_data = [];
        data = ''
        while True:
            data = the_socket.recv(8192)
            if End in data:
                total_data.append(data[:data.find(End)])
                break
            total_data.append(data)
            if len(total_data) > 1:
                # check if end_of_data was split
                last_pair = total_data[-2] + total_data[-1]
                if End in last_pair:
                    total_data[-2] = last_pair[:last_pair.find(End)]
                    total_data.pop()
                    break
        return ''.join(total_data)

    # JSON format checker
    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        return json_object


#
################################################################################
#
#   Insert MongoDB
#
def insertLOG(database, target_address, data):
    def date(data):
        try:
            datetime_objs = datetime(data[1], data[2], data[3], data[4], data[5], data[6])
            date = datetime_objs.strftime("%Y-%m-%d %H:%M:%S")
        except IndexError:
            return datetime.now()
        return date

    try:
        col = database["lof"]
        list = {
            "uuid": target_address,
            "activity": data[0],
            "date": datetime.now()
        }
        result = col.insert(list)
        print(result)
        print("Data saved to MongoDB")
    except Exception, e:
        print(e)
        pass


#
################################################################################
#
#   Insert DB server
#
def InsertDB(device_uuid, resting, staying, walking, running, health_status, date):
    conn = pymysql.connect(host='211.38.86.93',
                           user='root',
                           password='niceduri',
                           db='Pet-it',
                           charset='utf8')
    try:
        with conn.cursor() as cursor:
            #           sql = 'INSERT INTO behavior_log(uuid, resting, staying, walking, running, health_status, date TOKEN) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            #           cursor.execute(sql, (behavoir of pit action token_string))
            sql = 'INSERT INTO behavior_log (uuid, resting, staying, walking, running, health_status, date) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (device_uuid, resting, staying, walking, running, health_status, date))
            conn.commit()
            print(cursor.lastrowid)
    finally:
        conn.close()

    return cursor.lastrowid


#
################################################################################
#
#   Select DB server
#
def SelectDB(phone_number, cpuid):
    conn = pymysql.connect(host='211.38.86.93',
                           user='root',
                           password='niceduri',
                           db='Pet-it',
                           charset='utf8')
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM Manager WHERE P_NUM = %s and GUID = %s'
            cursor.execute(sql, (phone_number, cpuid))
            result = cursor.fetchone()
            print(result)
    finally:
        conn.close()

    return result


#
################################################################################
#
#   Delete DB server
#
def DeleteDB(device_id):
    conn = pymysql.connect(host='211.38.86.93',
                           user='root',
                           password='niceduri',
                           db='Pet-it',
                           charset='utf8')
    try:
        with conn.cursor() as cursor:
            sql = 'DELETE FROM behavior_log WHERE uuid = %s'
            cursor.execute(sql, (device_id,))
            conn.commit()
    finally:
        conn.close()


################################################################################
#
#   Healh calculator
#
def HealthThread():
    while True:
        now = time.localtime()
        health_time = now.tm_min
        if health_time % 10 == 0:
            InsertDB(target_address, 110, 120, 163, 45, "good", datetime.now())
            print(health_time)
        time.sleep(1)


#
################################################################################
#
#   Main Routine
#
if __name__ == "__main__":

    # health_thread = threading.Thread(target = HealthThread, args = ())
    # health_thread.start()

    while True:
        print("Init bluetooth...")
        bl = Bluetoothctl()
        print("Ready!")
        time.sleep(1)
        bl.power_on()
        bl.stop_scan()
        bl.pairable_on()
        bl.agent_on()
        bl.default_agent()
        bl.start_scan()

        print("Scanning for 10 seconds...")
        for i in range(1, 11):
            print(str(i) + " sec")
            time.sleep(1)

        bl.stop_scan()

        for device in bl.get_available_devices():
            print(device)
            if target_name == device['name']:
                target_address = device['mac_address']
                break
            else:
                for device in bl.get_paired_devices():
                    if target_name == device['name']:
                        target_address = device['mac_address']
                        break

        if target_address is not None:
            break

    while True:
        if target_address is not None:
            try:
                connection_class.BtAutoPair(target_address)
            except BluetoothctlError as e:
                print(e)
                pass
            print("found target bluetooth device with address ", target_address)

            try:
                server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                server_sock.connect((target_address, port))
                print("Bluetooth connected")
                while True:
                    received_data = bl.recv_data(server_sock)
                    # print(received_data)
                    data = bl.is_json(received_data)
                    server_sock.send("0")
                    time.sleep(1)
                    if data is not False:
                        dbClient = MongoClient(DATABASE_URL)
                        db = dbClient["petness"]
                        insertLOG(db, target_address, data)
                        dbClient.close()
                        # InsertDB(target_address, 110, 120, 163, 45, "good", datetime.now())
                        print("Health data saved to Server DB")
                    print(data)

                server_sock.close()
            except bluetooth.btcommon.BluetoothError as err:
                print("Error catched: " + str(err))
                print(bl.get_device_full_info(target_address))
                # Error handler
                pass
        else:
            print("could not find target bluetooth device nearby")
            break


