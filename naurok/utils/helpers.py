



def headers(api: str, url: str = None, data_size: int = None, content_type: str = "application/json;charset=utf-8"):
	data =  {
		"Accept": "application/json, text/plain, */*",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
		"Cache-Control": "no-cache",
		"Connection": "keep-alive",
		"Host": api,
		"Origin": f"https://{api}",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
	}
	if url:data["Referer"] = url
	if content_type: data["Content-Type"] = content_type
	if data_size: data["Content-Length"] = str(data_size)
	return data