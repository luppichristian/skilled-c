# Audio programming

## Library selection

Respect an existing project stack and explicit user choices. For a new project, prefer:

- **FMOD** for professional runtime applications. Check the applicable license and distribution terms for the project before adopting or shipping it.
- **OpenAL** for portable 3D spatial audio. Choose an implementation supported on the targets and check its license; for example, OpenAL Soft is available without a license fee but is LGPL-licensed and has distribution obligations.
- **miniaudio** for simple 2D audio.

When cases overlap, prefer FMOD for a professional runtime if it fits the project's features, targets, and licensing; otherwise prefer OpenAL when spatial audio is needed and miniaudio for simple 2D audio. With FMOD, use the Studio API for authored events and banks, and the Core API when lower-level audio primitives are needed.

## Stream and callback contract

For audio I/O, establish the actual sample rate, sample format, channel count and layout, and frame count supplied by the backend. A frame contains one sample per channel; frame counts and byte counts are different. Handle the sizes and input/output buffers allowed by the API, fill all requested output frames, and use silence when there is no data to play. Check stream initialization, start, stop, and device errors.

When the backend invokes a time-critical callback, keep its work bounded and avoid operations that can block or take unbounded time, including allocation, file or console I/O, and ordinary mutex waits. Prepare buffers and expensive work outside the callback. Transfer control changes and audio data through a bounded, correctly synchronized handoff suited to the producer and consumer; do not assume an atomic operation is lock-free on every target. Define full/empty behavior, underflow reporting, and ownership without blocking the callback. Follow the backend's callback restrictions.

Stop the stream and wait for any in-flight callbacks to finish before releasing callback state or buffers, using the backend's shutdown contract. Do not rely on `volatile` for communication between threads.

## Mixing and verification

Mix in a format with suitable headroom, apply gains deliberately, and define clipping or limiting and conversion to the output format. Account for differing source and device sample rates and maintain resampler state across blocks when resampling is needed. Avoid assuming an audio device, fixed callback size, or a particular platform backend exists.

Exercise silence, multiple voices, clipping boundaries, varying callback sizes, underflow, shutdown, and device changes as applicable. Compare offline output against known signals, then listen and check for glitches on supported devices.
