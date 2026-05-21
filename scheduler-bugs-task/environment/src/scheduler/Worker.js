class Worker {
  constructor(id, scheduler) {
    this.id = id;
    this.scheduler = scheduler;
    this.isIdle = true;
    this.currentTask = null;
  }
  async execute(task) {
    this.isIdle = false;
    this.currentTask = task;
    return new Promise((resolve, reject) => {
      // Bug: a new listener is added on every task and never removed.
      this.scheduler.on('cancel', (taskId) => {
        if (this.currentTask && this.currentTask.id === taskId) {
          reject(new Error('Task Cancelled'));
          this.isIdle = true;
          this.currentTask = null;
        }
      });
      setTimeout(() => {
        if (task.failTimes && (task.attempts || 0) < task.failTimes) {
          reject(new Error('Transient task failure'));
          this.isIdle = true;
          this.currentTask = null;
          return;
        }
        if (this.currentTask && this.currentTask.id === task.id) {
          resolve(task.result || 'Success');
          this.isIdle = true;
          this.currentTask = null;
        }
      }, task.duration || 10);
    });
  }
}
module.exports = { Worker };
