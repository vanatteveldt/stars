Open source stars! clone
=====

This is an attempt at an open source stars! clone.
I realize that there have been a number of attempts in the past, so hopefully this can succeed by openness and modularity.

*Development Status*: Extremely early [![Build Status](https://travis-ci.org/vanatteveldt/stars.png)](https://travis-ci.org/vanatteveldt/stars) 

This repository will only hold the server code. Any client(s) will get their own repository.

Installation
====

You need to have python, mongodb, and various python modules installed.

On linux, I recommend using a virtual environment to keep things contained.
Something like the following should do the trick for ubuntu/debian.
For other distros, replace the first line by something more suitable.


```bash
sudo apt-get install python-virtualenv python3 mongodb
virtualenv -p /usr/bin/python3 env
source env/bin/activate
pip install -r requirements.txt
```

Running the server
---

(Note: if using a virtual environment, make sure that it is activated by running `source env/bin/activate`!)

Start the debug server by calling the `run.py` script:

```
$ python run.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

You can now play around with it, e.g. using curl or [postman](https://chrome.google.com/webstore/detail/postman-rest-client/fdmmgilgnpjigdojojpjoooidkmcomcm).
See [this link](https://gist.github.com/vanatteveldt/7c434b668becbfcacb44) for an example curl session of moving a ship around.


Architecture
=====

Statement of principles, all open for discussion:

- Strict server/clients architecture
- All information between server and clients in json
- Server is a flask RESTful python web server that generates new turns based on old universe plus orders
- Server accepts partial orders as well as complete orders and can be queried for all existing state
- Base client would be a web based client that functions much like the current client
- Other clients could do various automation tasks and store partial orders, notes, messages etc on the server
- AI would also be a client like any other client. AI cheating is replaced by 'handicap' flags on the server

By having a very modular server/client design, multiple people can work on different aspects effectively; and multiple clients can exist and compete with each other.

The rest of this section contains some ideas to kick off discussion.
Presumably most of them should be moved into separate documents at some point.

API
-----

The server has an open REST API for everyone to get and post the universe/turn files.
Clients only access this API and the server has no other interface.

Although more methods will probably be needed at some point, I think the interface below should be a good starting point:

```python
GET /games  # list available games
POST /games  # create a new game by POSTING settings
GET /games/<game-id>  # retrieve settings for a game
PUT /games/<game-id>/player/<player-number>/race  # upload race file
GET /games/<game-id>/player/<player-number>/race
GET /games/<game-id>/player/<player-number>/turn/<turn-number>/universe
GET /games/<game-id>/player/<player-number>/turn/<turn-number>/orders
PUT /games/<game-id>/player/<player-number>/turn/<turn-number>/orders
```

Game flow
----

1. Someone creates a new game by POST-ing a game settings file to /games. This setting file contains settings, rules, etc. as well as the usernames of people invited to the game.
2. Player GET the game settings at /games/1
3. Player PUT the game settings at /games/1/player/1/race
4. As soon as all race files are in, or at some other predefined moment, the game commences and turn 0 is created
5. Player GET the game settings at /games/1 and see that the current turn is turn 1 and that they need to make a move
6. Player GET the universe at /games/1/turn/1/universe
7. Player makes his moves and PUTs to /games/1/turn/1/orders, containing a flag "end of turn" to mark that he/she is ready
8. Optionally, the player goes through as many iterations as desired of GETting the current orders and PUTting new orders
8. As soon as all orders are ready, or at some other predefined moment, the turn is processed, and turn 2 is ready.

Security
-----

Players need to be able to query game state and submit orders for their race without seeing that of others.
I think it should be enough to rely on token-based authentication (every game+race has a unique token checked by the web server).
Players have a username+password used for starting/joining games and obtaining a game token.
Encrpytion should be handled adequately by HTTPS, and it should be assumed that everyone with low-level (root) access to the game host is able to cheat at will since she or he can change the server program anyway.
So, it does not make sense to try to encrypt or guard anything on the server.

It should be impossible to cheat by creating a turn file that contains impossible orders, i.e. the server should validate all client input.

Development plan
====

I think first order of business is to create a working server/client pair that allows for the most basic operation, either building mines and factories on a planet or flying a scout around. From there, features can be added as people have time.

I propose not fixing the full definition of settings/universe/turn files in advance, but just adding stuff as needed. If we ever get close to something stable, we can refactor and stabilize/freeze these files.
