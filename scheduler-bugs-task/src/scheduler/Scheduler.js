const { EventEmitter } = require('events');
const { Queue } = require('./Queue');
const { Worker } = require('./Worker');
class Scheduler extends EventEmitter {
  constructor(workerCount) {
    super();
    this.queue = new Queue();
    this.workers = Array.from({ length: workerCount }, (_, i) => new Worker(i, this));
    this.isProcessing = false;
    this.completed = new Set();
    this.failed = new Map();
    this.results = new Map();
  }
  schedule(task) {
    this.queue.enqueue(task);
    this.processNext();
  }
  updateTaskPriority(taskId, newPriority) {
    return this.queue.updatePriority(taskId, newPriority);
  }
  cancelTask(taskId) {
    const removed = this.queue.remove(taskId);
    if (removed) {
      return true;
    }
    // Bug: emits cancel but does not guard retry/failure bookkeeping correctly.
    this.emit('cancel', taskId);
    return this.queue.processing.has(taskId);
  }
  async processNext() {
    if (this.isProcessing || this.queue.size === 0) return;
    this.isProcessing = true;
    const idleWorkers = this.workers.filter(w => w.isIdle);
    if (idleWorkers.length > 0) {
      // Bug: async gap lets another processNext observe the same idle workers.
      await new Promise(resolve => setTimeout(resolve, 0));
      for (const worker of idleWorkers) {
        if (this.queue.size === 0) break;
        // Bug: does not re-check worker.isIdle and dequeue ignores dependencies.
        const task = this.queue.dequeue(this.completed);
        if (task) {
          worker.execute(task).then((result) => {
            this.queue.complete(task.id);
            this.completed.add(task.id);
            this.results.set(task.id, result);
            this.processNext();
          }).catch((error) => {
            this.queue.complete(task.id);
            this.failed.set(task.id, error.message);
            this.processNext();
          });
        }
      }
    }
    this.isProcessing = false;
  }
}
module.exports = { Scheduler };
