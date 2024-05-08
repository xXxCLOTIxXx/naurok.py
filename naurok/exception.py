
class LinkError(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class NotForwarded(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)