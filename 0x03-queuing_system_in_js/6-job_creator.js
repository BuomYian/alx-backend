// import kue
import kue from 'kue';

// Creating a queue
const queue = kue.createQueue({name: 'push_notification_code'});

// Creating a job
const jobData = queue.create('push_notification_code', {
  phoneNumber: 'string',
  message: 'string'
});

jobData
  .on('enqueue', () => {
    console.log('Notification job creeated', jobData.id);
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed attempt', () => {
    console.log('Notification job failed');
  });

jobData.save();
