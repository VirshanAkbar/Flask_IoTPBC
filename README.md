# Flask_IoTPBC

Berikut adalah program Flask sebagai Webserver HTTP yang dapat menerima input dari sensor IoT

Untuk mencoba data dummy, dapat membuka powershell atau terminal dan memberi command sebagai berikut
```powershell
curl -X POST http://127.0.0.1:25113/submit -H "Content-Type: application/json" -d "{\"temperature\": 25.3, \"humidity\": 57}"
```
