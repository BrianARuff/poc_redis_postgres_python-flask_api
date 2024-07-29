# Query Buster - PoC
Proof of concept that's meant to demonstrate a way of improving application response time by avoid expensive operations.

> Note, that this is not the only way to improve this process, but it is one way. In a real-world scenario, I would first recommend optimizing the SQL query as much as possible before using external solutions. That said, if you have already done, then then the next step is likely looking to external sources to improve your app's performance. One way to do that is by using cache. That said, this **not** a silver bullet. You will need to determine if this solution is valid for your problem using critical thinking skills.

#### What is Cache?
Simply put, caching's mechanism of action is storing data that your server has already queried from the DB before, so that it can be quickly accessed, without querying the database again.

#### Using Cache
- There are several caveats that you need to think about when using a cache. If the database updates any of the data in cache, you will need to think about how you want to handle that situation in your application. Below are several technologies that you could use to provide a near-real time client-side experience.
    - Web sockets
    - Redis Pub/Sub
    - Database triggers

> A combination of them would provide a robust solution, updating the client in near real time. Some trade-offs include implementation time, increased architectural complexity, increased server load, and increased server cost.

- If you wanted a less robust solution due to one of the reasons stated above, then perhaps using one of the solutions below would provide that.
    - **Polling** - Have your client re-request data from the server on an interval. You can control the client's UI and have the data reloaded as a background operation, or you can enable an alert that tells them that new data is present.
    - **Cache Expiration** - Set the cache to expire after being stored for a specified time. Your client still needs to re-request the data, and it wouldn't be updated until after the life time of the entry.

___

# Database Setup (PostgreSQL)

### Update package lists
`sudo apt update`

### Install PostgreSQL
`sudo apt install postgresql postgresql-contrib`

### Start PostgreSQL service
`sudo service postgresql start`

### Switch to PostgreSQL user
`sudo -i -u postgres`

### Access PostgreSQL prompt
`psql`

### Set password for postgres user
`\password postgres`

### Create a new database
`CREATE DATABASE mydatabase;`

### Create a new user
`CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';`

### Grant privileges to the new user on the new database
`GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;`

### Connecting to PostgreSQL: You can connect to your PostgreSQL database from your WSL terminal using:
`psql -h localhost -U myuser -d mydatabase`

# Cache Setup (Redis)

### Update package lists
`sudo apt update`

### Install Redis
`sudo apt install redis-server`

### Configure Redis (Optional) - I skipped this personally, but you can do it if you want.
`sudo nano /etc/redis/redis.conf`

```
# Uncomment to Enable bind and password
# bind 0.0.0.0
# requirepass yourpassword
```

### Restart Redis service
`sudo service redis-server restart`

### Test Redis installation
`redis-cli`
`ping`

### Connecting to Redis Remotely: 
If you've configured Redis to allow remote connections and set a password, you can connect to your Redis server from another machine using the Redis CLI:

`redis-cli -h your_redis_server_ip -p 6379 -a yourpassword`

### 
# poc_redis_postgres_python-flask_api
