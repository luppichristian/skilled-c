# Record/replay testing

Make runtime scenarios repeatable by recording the inputs consumed by the application, replaying them, and checking meaningful state. Input alone does not guarantee determinism: time, randomness, files, scheduling, and external services may also need to be controlled.

## Modes and input

- In record mode, capture the scenario's initial conditions, inputs, pinned values, tracked values, and synchronization points. In replay mode, supply the recorded inputs and pinned values and verify the tracked values. Ordinary execution can leave this instrumentation disabled; a disabled run is not a successful replay.
- Initialize the harness before the scenario starts. Advance it before input is consumed in each frame or simulation step, and finish it at shutdown. Preserve event order and capture short transitions that could occur between polls. Use a consistent logical-step or timing model in both modes.
- Reproduce the inputs the application actually receives. If replay relies on operating-system input injection, account for focus and other events that can steal input. Use non-rendering execution only when the application and input backend support it.

## Pin values

Pin values that enter the application from nondeterministic sources. During recording, save the current value; during replay, replace it with the recorded value **before the application uses it**. Examples include a random seed, a clock reading, a frame duration, or an external response. Pin the data needed by the scenario rather than assuming that a seed alone controls every source of randomness or scheduling.

Pinning controls an input; it should not overwrite a result being tested. If reading a value also has necessary side effects, reproduce or isolate those effects as well.

## Track values

Track selected application state at meaningful checkpoints. During recording, save a snapshot; during replay, compare the current value with that snapshot without changing the application state. A score, position, state transition, or output checksum can reveal divergence before the scenario ends.

Compare values according to their meaning. Define an appropriate tolerance for floating-point values when needed. For structures or byte data, compare a stable representation rather than uninitialized padding, pointers, or platform-dependent object layouts. Report the checkpoint, logical step, expected value, and actual value on mismatch.

## Identify recorded operations

Give each pin, track, and synchronization point a stable identifier. Distinguish repeated occurrences, including the same identifier in different steps and multiple calls within one step, using a logical step and occurrence index or an equivalent ordered record stream. Keep the operation kind, value type, and size consistent between recording and replay.

Treat missing, extra, out-of-order, or incompatible records as failures; do not silently reuse an earlier value or leave a pin unchanged. At the end, verify that the expected scenario completed and all required records and checks were consumed.

## Synchronize variable-duration work

Place a named synchronization point after an operation such as loading or a menu transition actually completes. Record its position in the scenario. During replay, hold later recorded inputs at that point until the matching completion signal arrives, then resume their relative timing. Remember a signal that arrives before replay reaches its point; if it arrives late, keep waiting. Preserve signal identity and order.

Keep processing whatever events or background work are needed to reach the signal while replay is waiting. Use a logical replay timeline so extra waiting frames do not shift subsequent checks, and fail on unexpected signals or a bounded timeout. When an external result is itself recorded, replaying that result at the recorded point is another way to avoid depending on the live operation.

## Example scenario

Record an initial random seed and pin it before initializing the simulation. Record a movement input and track the resulting position after the update. When a level finishes loading, signal `level.ready`; only then record the next input. On replay, restore the seed, supply the movement input, compare the position, and wait for `level.ready` before delivering the next input. A different loading duration should delay the replay rather than move the later input ahead of the completion signal.

Keep files and mutable test data isolated between runs. Return a nonzero status for a failed check, an incomplete replay, or a timeout, and include enough context to identify the first divergence.
