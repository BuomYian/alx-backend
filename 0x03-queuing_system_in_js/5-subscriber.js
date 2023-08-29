// Import redis
import redis from 'redis';

// Create a Redis client instance
const subscriber = redis.createClient();

// Listen for the 'connect' event
subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Listen for the 'error' event
subscriber.on('error', (err) => {
  console.error('Redis client not connected to the server:', err.message);
})

// Subscribe to the 'holberton' school
subscriber.subscribe('holberton school channel');

// Listen for messages on the subscribed channel
subscriber.on('message', (channel, message) => {
  console.log(message);

  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe();
    subscriber.quit();
  }
});
