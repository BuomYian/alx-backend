// Import redis
import redis from 'redis';

// Create a Redis client instance
const client = redis.createClient();

// Listen for the 'connect' event
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Listen for the 'error' event
client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.message);
});
