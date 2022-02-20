import numpy
import cv2


class tracking_point(object):
	def __init__(self, identifier, current_location):
		self.identifier = identifier
		self.current_location = current_location
		self.current_p_X, self.current_p_Y = self.current_location

	def set_identifier(self, identifier):
		self.identifier = identifier
		return f"ID updated to {identifier}"

	def update_current_location(self, current_location):
		self.current_location = current_location
		self.current_p_X, self.current_p_Y = self.current_location
		return 0

	def delete_log_interval(self, interval):
		assert interval in self.location_log.keys(), "Submitted interval is not in log"
		del self.location_log[interval]
		return 0

	def log_location(self, interval, location, current=True):
		assert interval not in self.location_log.keys(), "ERROR interval submitted isn't unique. Itterate or use `clear_location_log` or `delete_log_interval`"
		self.location_log[interval] = location
		if current == True:
			self.current_location = location
		return 0

	def clear_location_log(self):
		self.location_log = {}
		return 0

	def initiate_log(self):
		try:
			self.location_log
			return "location log already exists. User `clear_location_log`"
		except:
			self.location_log = {}
			return 0

	def set_current_location(self, location):
		assert type(location)==list, "Location must be list"
		self.current_location = location
		return 0

	def get_current_location(self):
		return self.current_location