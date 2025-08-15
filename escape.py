def escape(uuid:str) -> str:
	return uuid.replace(':','\:').replace('-','\-')
