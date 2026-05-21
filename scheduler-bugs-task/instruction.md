Stabilize the Scheduler Under Load

This task is in a small Node.js scheduler used by actual-backend-app. The public API is already present, but the implementation has several load-related correctness bugs spread across:

src/scheduler/Queue.js
src/scheduler/Worker.js
src/scheduler/Scheduler.js
Do not change the verifier files.

Required behavior

Queue

Queue must expose enqueue(task), updatePriority(taskId, newPriority), dequeue(completedIds), remove(taskId), complete(taskId), sort(), and the size getter.

Every task has an id; invalid tasks should throw.
enqueue(task) should return false instead of inserting a duplicate queued or processing task id.
Queued tasks must be ordered by descending numeric priority.
Tasks with the same priority must keep their original enqueue order.
updatePriority(taskId, newPriority) must update only queued tasks and immediately restore correct ordering.
dequeue(completedIds) must return the highest-priority task whose dependsOn list is fully present in completedIds. It must not dequeue a blocked task.
Dequeued task ids must be added to processing.
complete(taskId) must remove the id from processing.

Worker

Worker.execute(task) should run one asynchronous task and listen for the scheduler's cancel event only while that task is active.

Remove the temporary cancel listener on success, cancellation, and task failure.
Clear pending timers when a task is cancelled.
After any success, failure, or cancellation, the worker must be idle and must not retain currentTask.
A task with failTimes should fail while task.attempts < task.failTimes; otherwise it should resolve with task.result or "Success".

Scheduler

Scheduler must keep these public state fields useful for callers and tests:

completed: Set of completed task ids.
failed: Map from failed task id to error message.
results: Map from completed task id to resolved result.
cancelled: Set of cancelled task ids.
Scheduler behavior:
schedule(task) should enqueue the task and start processing; it should return whether the task was inserted.
cancelTask(taskId) should remove queued tasks or cancel active tasks and return whether anything was cancelled.
processNext() must not assign work to a busy worker, even if several calls happen close together.
Dependency-blocked tasks must wait until their dependencies complete.
Failed tasks should be retried until attempts reaches retryLimit.
Every finish path must call queue.complete(task.id) so the processing set does not leak.
When one task finishes, processing should continue so newly unblocked or retried tasks run.
The goal is to make the scheduler correct under mixed priorities, dependencies, retries, cancellations, and concurrent processNext() calls.
