class Queue {
  constructor() {
    this.tasks = [];
    this.processing = new Set();
    this._nextSeq = 0;
  }
  enqueue(task) {
    if (!task || !task.id) {
      throw new Error('task.id is required');
    }
    // Tasks are stored by reference because Scheduler updates attempts on retry.
    if (task.attempts === undefined) {
      task.attempts = 0;
    }
    this.tasks.push(task);
    this.sort();
    return true;
  }
  updatePriority(taskId, newPriority) {
    const task = this.tasks.find(t => t.id === taskId);
    if (task) {
      task.priority = newPriority;
      // Bug: queue is not re-sorted after priority changes.
      return true;
    }
    return false;
  }
  dequeue(completedIds = new Set()) {
    // Bug: ignores dependencies and always takes the front task, even if blocked.
    const task = this.tasks.shift();
    if (task) {
      this.processing.add(task.id);
    }
    return task || null;
  }
  remove(taskId) {
    const index = this.tasks.findIndex(t => t.id === taskId);
    if (index === -1) {
      return null;
    }
    return this.tasks.splice(index, 1)[0];
  }
  complete(taskId) {
    // Bug: processing ids are never cleared after completion.
  }
  sort() {
    // Bug: priority ties are not stable because no insertion sequence is used.
    this.tasks.sort((a, b) => (b.priority || 0) - (a.priority || 0));
  }
  get size() {
    return this.tasks.length;
  }
}
module.exports = { Queue };
