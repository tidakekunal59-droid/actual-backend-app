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
      // Bug: Event listener leak
      // Adding a new listener every time a task executes
      this.scheduler.on('cancel', (taskId) => {
        if (this.currentTask && this.currentTask.id === taskId) {
          reject(new Error('Task Cancelled'));
          this.isIdle = true;
          this.currentTask = null;
        }
      });

      // Simulate async task execution
      setTimeout(() => {
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
