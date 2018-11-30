test:
	python -m unittest tests/test_parsers.py
	python -m unittest tests/test_initialization.py
	python -m unittest tests/test_playlist_methods.py
	python -m unittest tests/test_video_methods.py
	python -m unittest tests/test_youtube_api_utils.py
	python -m unittest tests/test_channel_methods.py