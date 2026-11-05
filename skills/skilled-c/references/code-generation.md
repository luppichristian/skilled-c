# Table-driven code generation

When several C declarations or tables describe the same set of facts, consider one authoritative metadata table. Examples include opcode IDs, names, properties, and dispatch entries. A normal C table, designated initializers, or an X-macro may be sufficient for a small case; a separate generator is useful when several outputs or more complex transformations justify it. Keep the resulting C understandable and respect existing build and project conventions.

Define and validate the metadata schema, including duplicate IDs or names, missing references, numeric limits, and escaping of generated C text. Keep externally visible or persisted values explicit and stable: reordering rows must not silently change a file format, protocol, or ABI. Do not index tables with unvalidated external values.

Make generation reproducible and make the build depend on both the generator and its inputs. Stage and validate output before replacing previous successful results; if several files must agree, arrange publication or build ordering so consumers do not use a partially updated set. Report generation failures. When implementing a generator, check that its output compiles and that malformed input produces a clear failure.
