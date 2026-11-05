# Runtime loops

For an interactive simulation, distinguish input collection, logical updates, and presentation. Map their data dependencies and required ordering before choosing a single loop or separate threads. Use [Concurrency](concurrency.md) for shared-state rules and [Record/replay testing](replay-testing.md) when scenarios need to be repeatable.

## Simulation and presentation

When stable simulation steps are useful, advance simulation with a fixed logical tick and render at the presentation rate. Measure elapsed time with a suitable monotonic clock, accumulate it, and perform zero, one, or several ticks as needed before presentation. Continue handling the events required for responsiveness. Define behavior for pause, resume, long stalls, and overload: for example, carry a bounded backlog, slow the simulation, or discard time deliberately. If a backlog is bounded, define what happens to elapsed time beyond the bound. Each choice affects latency or simulation semantics.

Assign input events to logical ticks with a documented ordering policy. If rendering between ticks, retain distinct previous and current snapshots and update the previous snapshot before advancing the current one. Interpolate only values for which it makes sense; define handling of teleports, creation, deletion, and reused identities. Interpolation can add up to one tick of presentation latency.

For animation, distinguish interpolation over a fixed duration from repeatedly moving the current value toward a target. Moving by a constant fraction strictly between zero and one of the remaining distance produces an exponential approach to a fixed target, and can respond to a changed target. For frame-rate-independent smoothing, one choice is `fraction = 1 - exp(-rate * elapsed_seconds)`, with finite nonnegative rate and elapsed time; verify behavior across variable frame durations.

If updates and rendering run on different threads, publish complete snapshots with the required synchronization and keep their storage valid until readers finish. Define snapshot reuse, shutdown, and any platform requirement that window or graphics operations run on a particular thread. Separate threads are optional and should solve a measured or concrete scheduling need.

## Determinism

A fixed tick alone does not make a simulation deterministic. Control or record relevant inputs, initial state, random sources, external results, and ordering; floating-point behavior and parallel scheduling can also differ across targets. Test the same tick-indexed scenario under different presentation rates, including frames with no ticks or multiple ticks and a long stall, and compare meaningful simulation state at matching ticks. When varying presentation rates, do not force the original render-frame durations; control the simulation-relevant timing instead. Use the replay reference for recording and mismatch handling.
