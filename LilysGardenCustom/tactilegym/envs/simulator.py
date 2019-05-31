import requests

class Simulator(object):
	def __init__(self, host):
		self.host = host

	def load(self, level_index, seed):
		return self._do_request('/load', {
			'seed': seed,
			'levelIndex': level_index
		})

	def click(self, state, x, y):
		return self._do_request('/click', {
			'state': state,
			'x': x,
			'y': y
		})

	def session_create(self, state):
		return self._do_request('/session/create', {
			'state': state
		})

	def session_click(self, sessionId, x, y):
		return self._do_request('/session/click', {
			'sessionId': sessionId,
			'x': x,
			'y': y
		})

	def session_destroy(self, sessionId):
		return self._do_request('/session/destroy', {
			'sessionId': sessionId
		})

	def session_status(self, sessionId):
		return self._do_request('/session/status', {
			'sessionId': sessionId
		})

	def sessions_list(self):
		return self._do_request('/sessions/list', {})

	def sessions_clear(self):
		return self._do_request('/sessions/clear', {})

	def _do_request(self, url, json_payload):
		response = requests.post(self.host + url, json=json_payload, timeout=10)
		response.raise_for_status()
		return response.json()