const { EventEmitter } = require('events');
const { Queue } = require('./Queue');
const { Worker } = require('./Worker');

class Scheduler extends EventEmitter {
  constructor(workerCount) {
    super();
    this.queue = new Queue();
    this.workers = Array.from({ length: workerCount }, (_, i) => new Worker(i, this));
    this.isProcessing = false;
  }

  schedule(task) {
    this.queue.enqueue(task);
    this.processNext();
  }

  updateTaskPriority(taskId, newPriority) {
    this.queue.updatePriority(taskId, newPriority);
  }

  cancelTask(taskId) {
    this.emit('cancel', taskId);
  }

  async processNext() {
    if (this.isProcessing || this.queue.size === 0) return;
    this.isProcessing = true;

    // Find idle workers
    const idleWorkers = this.workers.filter(w => w.isIdle);

    if (idleWorkers.length > 0) {
      // Bug: Race condition
      // Asynchronous gap before task assignment
      await new Promise(resolve => setTimeout(resolve, 0));

      for (const worker of idleWorkers) {
        if (this.queue.size === 0) break;

        // This is buggy because worker.isIdle might be false now if another processNext was called concurrently
        // and assigned a task to this worker already.
        const task = this.queue.dequeue();
        if (task) {
           worker.execute(task).then(() => {
             this.queue.complete(task.id);
             this.processNext();
           }).catch(() => {
             this.queue.complete(task.id);
             this.processNext();
           });
        }
      }
    }

    this.isProcessing = false;
  }
}

module.exports = { Scheduler };
