// Import necessary modules
import redis from 'redis';

// Create a Redis client instance
const client = redis.createClient();

// Listen for the 'connect' event
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Listen for the 'error' event
client.on('error', (err) => {
  console.error('Redis client not connected to the server:', err.message);
});

// Function to set a new school value in Redis
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Funstion to display the value of a school key
function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, reply) => {
    if (err) {
      console.log('Error retrieving value:', err.message);
    } else {
      console.log(reply);
    }
  });
}

// Calling the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
