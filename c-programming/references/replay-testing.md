# Record/replay testing

For runtime applications, make repeatable end-to-end scenarios possible by recording inputs, replaying them, and checking meaningful application state. Treat input replay as one part of determinism: time, random seeds, filesystem state, scheduling, and external services can also affect the result.

## Test design

- Initialize the test mode at startup and advance the recorder or replayer before each frame's input is consumed. Shut it down and return a nonzero status on a failed check.
- Record or otherwise control nondeterministic inputs such as random seeds and timing values. Compare selected state and outputs during replay; diagnose mismatches with enough context to find the failing step.
- Synchronize explicitly at variable-duration boundaries such as asset loading, rather than assuming every run progresses at the same wall-clock speed.
- Isolate files and mutable test data between runs. Use bounded timeouts so a stalled replay fails instead of hanging indefinitely.
- Support non-rendering execution where the application and input backend actually permit it. Verify that the test runner's input mechanism works in the chosen environment.

## GameTest patterns

GameTest distinguishes recording, replay, and disabled modes. Its public interface uses macros such as `GMT_Init`, `GMT_Update`, and `GMT_Quit`; the trailing-underscore entry points are internal. When using it, check initialization, call `GMT_Update` once before input polling on every frame, and shut it down at the end.

Pin changing inputs such as seeds or time values, track selected values that should match, and use synchronization signals where progress depends on an unpredictable wait. Keep the order and keys of these operations consistent between recording and replay. A disabled build makes test macros no-ops, so it is not evidence that a replay passed.

GameTest's current input implementation is Windows-specific; do not assume it provides Linux, macOS, or WebAssembly input replay.

For the reviewed GameTest revision (`1bda7356f34ec75f338aef376a252683a23cae99`):

- Pin and Track counters reset each frame, but replay finds records by key and index without a frame identifier. Reusing a key across frames can therefore retrieve an earlier frame's record. Use keys unique to each recorded sample and verify multi-frame replay, or first verify that the selected revision has corrected the matching logic. Automatic call-site keys can repeat across frames.
- Missing or size-mismatched Track records are logged and skipped, while missing Pin records can leave the current value unchanged. Treat these diagnostics as test failures and independently check that the expected replay and checks completed.
- Inspect and test synchronization behavior in the selected revision: the reviewed code can remain blocked after a late matching signal. Bound waits so a stalled replay fails.
- When building a local checkout without network access, disable its optional example with `GMT_BUILD_EXAMPLE=OFF`; that example otherwise fetches an external dependency.

Other revisions may differ. GameTest itself is not bundled with this skill.
