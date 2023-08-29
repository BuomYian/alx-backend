// Import redis
import redis from 'redis';

// Create a Redis client instance
const publisher = redis.createClient();

// Listen for the 'connect' event
publisher.on('connect', () => {
  console,log('redis client connected to the server');
});

// Listen for the 'error' event
publisher.on('error', (err) => {
  console.error('Redis client not connected to the server:', err.message);
});

// Function to publish a message to the 'holberton' school
function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    publisher.publish('holberton school channel', message);

    if (message === 'KILL_SERVER') {
      publisher.quit();
    }
  }, time); 
}

// Calling the functions
publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
