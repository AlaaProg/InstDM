import requests, argparse, os
from urllib.parse import urlencode

from tqdm import tqdm

class InsdDM(requests.Session):

	def __init__(self, ):
		super(InsdDW, self).__init__()	

		self.headers.update({
				'User-Agent': 'Mozilla/5.0 ',
			})	

	
	def url_media(self, id):
		data = self._load(id)

		url = data.get('display_url')
		if data.get('is_video'):
			url = data.get('video_url')

		# self._save_file(url)
		return url 

	def save_file(self, url, into):

		path = os.path.join(into, self._prase_name(url))
		with open(path, 'wb') as f:

			req = self.get(url, stream=True)
			req.raise_for_status()
			try:
				t = tqdm(
					total=int(req.headers.get("content-length", 0)), 
					unit='B', unit_scale=True)

				# start download 
				for data in req.iter_content(1024):  # block_size=1024
					t.update(len(data)) # update prossess bar 
					f.write(data) # put in file 

			except KeyboardInterrupt:
				exit(0)

		return path

	def _prase_name(self, url:str ):

		return url.split("?")[0].split("/")[-1]

	def _load(self, id):

		data = self.get("https://z-p3.www.instagram.com/graphql/query/?"+urlencode({
			'query_hash' : "ea680deb6b53c77412e56bfdeb696c08",
			'variables': '{"shortcode":"%s"}'%id
		})).json()

		return data.get("data", {}).get('shortcode_media')


def main():

	dw = InsdDM()

	parser = argparse.ArgumentParser(description='INSTDW: download video or image from instagram ')
	parser.add_argument('id', help='code for post instagram ', type=str) # VIDEO_URL 
	parser.add_argument('--out', '-o', help='save into ', default=os.getcwd(), type=str) # PATH_SAVE
	argv = parser.parse_args()

	print("[Idw]: Get `POST` ")
	url = dw.url_media(argv.id)

	print("[Idw]: Start Download ")
	path = dw.save_file(url, argv.out)

	print("[Idw]: Save Into %s"%path)


if __name__ == '__main__':
	main()
