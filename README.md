# UDP Unicast
Simple UDP Unicast application using Python and Flask.

### Installation
```
sudo apt-get install vlc
sudo pip install Flask
```

### Start 
```
./server.py
```

### Test with VLC
On VLC player, open Media->Open Network Stream..., then Network tab.  Enter udp://@:1234.  On terminal running the server.py
```
curl -X POST http://localhost:5000/streaming/udp/<client_ip>/1234/0
```
Or from a browser, http://localhost:5000, select a video and play.
```

### Docker Build
```
docker build -t udp-streaming .
```

### Run As Docker Service
```
docker run -p 5050:5050 -v $(pwd)/library.repo:/etc/library.repo udp-streaming
```
