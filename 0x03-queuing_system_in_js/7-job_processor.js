import kue from 'kue';

// Array of blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Create a function to send a notification
function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100); // Track progress 0%
  
  if (blacklistedNumbers.includes(phoneNumber)) {
    const errorMessage = `Phone number ${phoneNumber} is blacklisted`;
    job.fail(new Error(errorMessage));
    done(new Error(errorMessage));
  } else {
    job.progress(50, 100); // Track progress 50%
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    done();
  }
}

// Create a Kue queue with concurrency of 2 (process two jobs at a time)
const queue = kue.createQueue({
  redis: process.env.REDIS_URL || 'redis://127.0.0.1:6379',
  concurrency: 2
});

// Process jobs in the queue
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

// Handle queue errors
queue.on('error', (err) => {
  console.log('Queue error:', err);
});

console.log('Job processor is running...');
