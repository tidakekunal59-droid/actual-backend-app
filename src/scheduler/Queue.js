class Queue {
  constructor() {
    this.tasks = [];
    this.processing = new Set();
  }

  enqueue(task) {
    this.tasks.push(task);
    this.sort();
  }

  updatePriority(taskId, newPriority) {
    const task = this.tasks.find(t => t.id === taskId);
    if (task) {
      task.priority = newPriority;
      // Bug: Missing this.sort() here causes priority inversion
    }
  }

  dequeue() {
    const task = this.tasks.shift();
    if (task) {
      this.processing.add(task.id);
    }
    return task;
  }

  complete(taskId) {
    // Bug: Missing this.processing.delete(taskId) causes memory leak
  }

  sort() {
    this.tasks.sort((a, b) => b.priority - a.priority);
  }

  get size() {
    return this.tasks.length;
  }
}

module.exports = { Queue };
