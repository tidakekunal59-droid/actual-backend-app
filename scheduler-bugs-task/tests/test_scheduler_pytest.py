from pathlib import Path
import subprocess
import textwrap
def run_node(source: str, timeout: float = 2.0):
    script = Path("/tmp/scheduler_check.js")
    script.write_text(textwrap.dedent(source), encoding="utf-8")
    result = subprocess.run(["node", str(script)], cwd="/app", text=True, capture_output=True, timeout=timeout)
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
def test_queue_priority_updates_are_stable_and_processing_is_cleaned():
    run_node("""
    const assert = require('assert');
    const { Queue } = require('/app/src/scheduler/Queue');
    const q = new Queue();
    q.enqueue({ id: 'a', priority: 5 });
    q.enqueue({ id: 'b', priority: 1 });
    q.enqueue({ id: 'c', priority: 5 });
    assert.strictEqual(q.updatePriority('b', 5), true);
    const first = q.dequeue(new Set());
    const second = q.dequeue(new Set());
    const third = q.dequeue(new Set());
    assert.deepStrictEqual([first.id, second.id, third.id], ['a', 'b', 'c']);
    q.complete('a');
    q.complete('b');
    q.complete('c');
    assert.strictEqual(q.processing.size, 0);
    """)
def test_dependencies_gate_high_priority_tasks_until_parents_complete():
    run_node("""
    const assert = require('assert');
    const { Scheduler } = require('/app/src/scheduler/Scheduler');
    const waitUntil = (predicate, timeout = 800) => new Promise((resolve, reject) => {
        const start = Date.now();
        const tick = () => {
            if (predicate()) return resolve();
            if (Date.now() - start > timeout) return reject(new Error('timeout'));
            setTimeout(tick, 5);
        };
        tick();
    });
    (async () => {
        const scheduler = new Scheduler(1);
        scheduler.schedule({ id: 'child', priority: 100, dependsOn: ['parent'], duration: 1, result: 'child-ok' });
        scheduler.schedule({ id: 'parent', priority: 1, duration: 5, result: 'parent-ok' });
        await waitUntil(() => scheduler.completed.has('child'));
        assert.deepStrictEqual(Array.from(scheduler.results.keys()), ['parent', 'child']);
        assert.strictEqual(scheduler.results.get('parent'), 'parent-ok');
        assert.strictEqual(scheduler.results.get('child'), 'child-ok');
        assert.strictEqual(scheduler.queue.processing.size, 0);
    })().catch(err => {
        console.error(err);
        process.exit(1);
    });
    """)
def test_retry_bookkeeping_eventually_completes_flaky_tasks():
    run_node("""
    const assert = require('assert');
    const { Scheduler } = require('/app/src/scheduler/Scheduler');
    const waitUntil = (predicate, timeout = 1000) => new Promise((resolve, reject) => {
        const start = Date.now();
        const tick = () => {
            if (predicate()) return resolve();
            if (Date.now() - start > timeout) return reject(new Error('timeout'));
            setTimeout(tick, 5);
        };
        tick();
    });
    (async () => {
        const scheduler = new Scheduler(1);
        const task = { id: 'flaky', priority: 5, duration: 1, failTimes: 2, retryLimit: 2, result: 'recovered' };
        scheduler.schedule(task);
        await waitUntil(() => scheduler.completed.has('flaky') || scheduler.failed.has('flaky'));
        assert.strictEqual(scheduler.completed.has('flaky'), true);
        assert.strictEqual(scheduler.failed.has('flaky'), false);
        assert.strictEqual(task.attempts, 2);
        assert.strictEqual(scheduler.results.get('flaky'), 'recovered');
        assert.strictEqual(scheduler.queue.processing.size, 0);
        assert.strictEqual(scheduler.listenerCount('cancel'), 0);
    })().catch(err => {
        console.error(err);
        process.exit(1);
    });
    """)
def test_queued_and_active_cancellation_do_not_leave_workers_or_listeners_dirty():
    run_node("""
    const assert = require('assert');
    const { Scheduler } = require('/app/src/scheduler/Scheduler');
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    const waitUntil = (predicate, timeout = 1000) => new Promise((resolve, reject) => {
        const start = Date.now();
        const tick = () => {
            if (predicate()) return resolve();
            if (Date.now() - start > timeout) return reject(new Error('timeout'));
            setTimeout(tick, 5);
        };
        tick();
    });
    (async () => {
        const scheduler = new Scheduler(1);
        scheduler.schedule({ id: 'slow', priority: 10, duration: 200 });
        scheduler.schedule({ id: 'queued', priority: 1, duration: 1 });
        await delay(20);
        assert.strictEqual(scheduler.cancelTask('queued'), true);
        assert.strictEqual(scheduler.cancelTask('slow'), true);
        await waitUntil(() => scheduler.workers[0].isIdle);
        await delay(40);
        assert.strictEqual(scheduler.completed.has('queued'), false);
        assert.strictEqual(scheduler.completed.has('slow'), false);
        assert.strictEqual(scheduler.cancelled.has('queued'), true);
        assert.strictEqual(scheduler.cancelled.has('slow'), true);
        assert.strictEqual(scheduler.queue.processing.size, 0);
        assert.strictEqual(scheduler.listenerCount('cancel'), 0);
        assert.strictEqual(scheduler.workers[0].currentTask, null);
    })().catch(err => {
        console.error(err);
        process.exit(1);
    });
    """)
def test_concurrent_process_next_stress_has_no_duplicate_worker_assignment():
    run_node("""
    const assert = require('assert');
    const { Scheduler } = require('/app/src/scheduler/Scheduler');
    const waitUntil = (predicate, timeout = 1200) => new Promise((resolve, reject) => {
        const start = Date.now();
        const tick = () => {
            if (predicate()) return resolve();
            if (Date.now() - start > timeout) return reject(new Error('timeout'));
            setTimeout(tick, 5);
        };
        tick();
    });
    (async () => {
        const scheduler = new Scheduler(2);
        let overlaps = 0;
        for (const worker of scheduler.workers) {
            const original = worker.execute.bind(worker);
            let active = false;
            worker.execute = async (task) => {
                if (active) overlaps++;
                active = true;
                try {
                    return await original(task);
                } finally {
                    active = false;
                }
            };
        }
        scheduler.schedule({ id: 'a', priority: 5, duration: 8, result: 'A' });
        scheduler.schedule({ id: 'b', priority: 5, duration: 8, result: 'B' });
        scheduler.schedule({ id: 'c', priority: 50, dependsOn: ['a', 'b'], duration: 1, result: 'C' });
        scheduler.schedule({ id: 'd', priority: 40, duration: 1, failTimes: 1, retryLimit: 1, result: 'D' });
        const calls = [];
        for (let i = 0; i < 12; i++) calls.push(scheduler.processNext());
        await Promise.all(calls);
        await waitUntil(() => scheduler.completed.has('c') && scheduler.completed.has('d'));
        assert.strictEqual(overlaps, 0);
        assert.strictEqual(scheduler.results.get('c'), 'C');
        assert.strictEqual(scheduler.results.get('d'), 'D');
        assert.strictEqual(scheduler.queue.processing.size, 0);
        assert.strictEqual(scheduler.listenerCount('cancel'), 0);
        assert.deepStrictEqual(Array.from(scheduler.results.keys()).slice(0, 2).sort(), ['a', 'b']);
    })().catch(err => {
        console.error(err);
        process.exit(1);
    });
    """, timeout=3.0)
