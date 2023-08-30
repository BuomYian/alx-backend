// Importing necessary modules

const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Redis client
const redisClient = redis.createClient();
const redisSet = promisify(redisClient.set).bind(redisClient);
const redisGet = promisify(redisClient.get).bind(redisClient);

// Reserve seats
async function reserveSeat(number) {
  await redisSet('available_seats', number);
}

// Get current available seats
async function getCurrentAvailableSeats() {
  const availableSeats = await redisGet('available_seats');
  return parseInt(availableSeats, 10) || 0;
}

// Set initial available seats to 50
reserveSeat(50);

// Initialize reservationEnabled to true
let reservationEnabled = true;

// Create Kue queue
const queue = kue.createQueue();

// Middleware to handle JSON body
app.use(express.json());

// Get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat', {}).save();
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });
  job.on('failed', (error) => {
    console.log(`Seat reservation job ${job.id} failed: ${error}`);
  });

  res.json({ status: 'Reservation in process' });
});

// Process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      await reserveSeat(availableSeats - 1);
      if (availableSeats - 1 === 0) {
        reservationEnabled = false;
      }
      done();
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
