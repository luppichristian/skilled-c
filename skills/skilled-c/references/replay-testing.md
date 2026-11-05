# Record/replay testing

Make runtime scenarios repeatable: record and replay application inputs and check meaningful state. Inputs alone do not guarantee determinism: time, randomness, files, scheduling, and external services may also need control.

## Modes and input

- Record initial conditions, inputs, pinned and tracked values, and synchronization points. On replay, supply recorded inputs and pins; verify tracked values. Ordinary execution can disable instrumentation; a disabled run is not a successful replay.
- Initialize the harness before the scenario, advance it before input consumption each frame or simulation step, and finish at shutdown. Preserve event order and capture short transitions between polls. Use the same logical-step or timing model in both modes.
- Reproduce inputs the application receives. For operating-system input injection, account for focus and events that can steal input. Use non-rendering execution only when the application and input backend support it.

## Pin values

Pin values entering the application from nondeterministic sources. Record each current value; on replay, replace it with the recorded value **before the application uses it**. Examples include a random seed, clock reading, frame duration, or external response. Pin data the scenario needs; a seed alone does not necessarily control every source of randomness or scheduling.

Pinning controls an input; it should not overwrite a result under test. Reproduce or isolate any necessary side effects of reading a value.

## Track values

Track selected application state at meaningful checkpoints: record a snapshot; on replay, compare the current value to the snapshot without changing application state. A score, position, state transition, or output checksum can reveal divergence before the scenario ends.

Compare values according to their meaning; define a floating-point tolerance when needed. For structures or byte data, compare a stable representation, not uninitialized padding, pointers, or platform-dependent object layouts. On mismatch, report the checkpoint, logical step, expected value, and actual value.

## Identify recorded operations

Give each pin, track, and synchronization point a stable identifier. Distinguish repeated occurrences, including the same identifier across steps and multiple calls per step, with a logical step and occurrence index or equivalent ordered record stream. Keep operation kind, value type, and size consistent between record and replay.

Fail on missing, extra, out-of-order, or incompatible records; do not silently reuse an earlier value or leave a pin unchanged. Verify the expected scenario completed and all required records and checks were consumed.

## Synchronize variable-duration work

Place a named synchronization point after an operation such as loading or a menu transition completes; record its scenario position. On replay, hold later recorded inputs there until the matching completion signal arrives, then resume their relative timing. Remember signals arriving before replay reaches their point; if late, keep waiting. Preserve signal identity and order.

While waiting, process events or background work needed to reach the signal. Use a logical replay timeline so extra waiting frames do not shift later checks; fail on unexpected signals or a bounded timeout. Alternatively, replay a recorded external result at its recorded point to avoid depending on the live operation.

## Example scenario

Record and pin an initial random seed before simulation initialization. Record a movement input and track the resulting position after the update. When a level finishes loading, signal `level.ready`; only then record the next input. On replay, restore the seed, supply the movement input, compare the position, and wait for `level.ready` before delivering the next input. A different loading duration should delay replay, not move later input ahead of the signal.

Keep files and mutable test data isolated between runs. Return nonzero status for a failed check, incomplete replay, or timeout, with context identifying the first divergence.
