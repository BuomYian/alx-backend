// Importing neccesary modules
import redis from 'redis';
import { promisify } from 'util';

// Create a Redis client instance
const client = redis.createClient();

// Promisify the 'get' function to work with promises
const getAsync = promisify(client.get).bind(client);

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

// Async function to display the value of a school key
async function displaySchoolValue(schoolName) {
  try {
    const reply = await getAsync(schoolName);
    console.log(reply);
  } catch (err) {
    console.error('Error retriving value:', err.message);
  }
}

// Calling the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
