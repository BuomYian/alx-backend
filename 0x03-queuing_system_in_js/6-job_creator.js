import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Create a job data object
const jobData = {
  phoneNumber: '+251903440654',
  message: 'Hello, this is a notification!',
};

// Create a job in the queue
const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    }
  });

// Listen for job completion
job.on('complete', () => {
  console.log('Notification job completed');
});

// Listen for job failure
job.on('failed', () => {
  console.log('Notification job failed');
});
