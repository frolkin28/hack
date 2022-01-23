# ChebureckMeet

### Description
ChebureckMeet is a new way to communicate with other people!
You can create own room with unique link, copy to clipboard link and send your friends.
Moreover, if you are organizer, you can moderate people and if it needed - remove from room.
Every person can control stream data (microphone and camera).


### Fast setting
If you want to launch locally, do next steps:
1. Download docker and docker-compose
2. For the first launch need build frontend: ```make build```
3. Start app: ```make run```
3. Go to: http://localhost:8080

### Launch Tests
1. Start tests: ```docker-compose up pytest```

## Linters
### Mypy
```docker-compose up mypy```


### Flake8
```docker-compose up flake```
