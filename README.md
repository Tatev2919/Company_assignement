**Recommendation System overview**

Welcome to our recommendation system project! This system is cleverly split into two main components: 
    the Generator
    the Invoker

The Generator service takes a stab at creating random recommendations using any model name you throw at it, while the Invoker takes on the role of managing those recommendations, smartly handling caching and requests to the Generator.

**Generator Service:** A nifty Flask app that does more than just flask. It generates random numbers based on the model name you provide.

**Invoker Service:** Another Flask app that's a bit of a control freak. It orchestrates fetching those recommendations, utilizing a dual-layer caching strategy (involving local memory and Redis) to boost performance and reduce wait times.

Redis: The backbone of our caching, Redis ensures our data sticks around just long enough to be useful without overstaying its welcome.

**Steps:**
You'll need a few things before diving in:

Docker
Docker Compose
Postman (for playing around and testing the endpoints)
Setting Up
Clone and Play

First, grab a copy of our code:

  git clone <repository-url>
  cd <repository-folder>
  Fire Up the Containers
  
Head over to where the docker-compose.yml file lives and spin up the containers:
  docker-compose build
  docker-compose up

Watch as Docker weaves its magic, bringing our Redis, Generator, and Invoker services to life.

How to Use This Thing
Playtime with Postman

**Making Recommendations:**

POST http://localhost:5000/generate
json
{
  "model_name": "exampleModel",
  "viewer_id": "user123"
}

Shoot this off to see our Generator pop out a random recommendation just for you.

**Getting Recommendations**
POST http://localhost:6000/recommend

json
{
  "viewer_id": "user123"
}
Hit this endpoint and our Invoker will check the caches before possibly waking up the Generator to get what you need.

**Key Endpoints**

Generator:
POST /generate - Ask and ye shall receive... a random recommendation, that is.

Invoker:
POST /recommend - Your go-to for fetching those recommendations, smartly managed and cached.

**Setup Details**
Internally, everything hums along on port 5000.
Redis is set to its usual port of 6379, just so it feels at home.

Troubleshooting
Run into trouble? Here’s what you can do:

Not Getting Any Responses?

Make sure Docker and Docker Compose are not just installed, but also happy and up-to-date.
Check out the Docker logs if something seems amiss.
Clashing Ports?

Take a quick peek to see if anything else on your machine is being greedy with ports 5000 6000 or 6379.
