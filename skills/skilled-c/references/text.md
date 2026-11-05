# Text and Unicode

Specify the encoding and length units at each boundary. UTF-8 uses variable-length byte sequences; UTF-16 uses one or two code units per Unicode scalar value. Bytes, code units, code points, grapheme clusters, and rendered glyphs are distinct; grapheme clusters approximate user-perceived characters. A byte count is not a character count, and neither a code point nor a glyph necessarily represents one user-perceived character.

For external text, choose whether malformed input is rejected or replaced, and apply the policy consistently. A UTF-8 validator must reject overlong sequences, surrogate values, out-of-range values, and truncated or otherwise invalid sequences. Preserve explicit lengths and handle embedded NULs deliberately; C string APIs stop at NUL. When converting, check sizes and errors, distinguish input and output units, and reserve a terminator when the receiving interface requires one. UTF-8 and UTF-16 are variable-width; do not treat `wchar_t` as a portable Unicode encoding.

Convert explicitly at operating-system boundaries as required by the selected API. For example, Windows wide APIs use UTF-16; do not assume every POSIX filename is valid UTF-8. Respect the application's existing representation and platform contracts.

For text rendering, use a font library's glyph metrics and follow its ownership rules for font data and glyph bitmaps. A simple code-point-to-glyph loop is insufficient for text requiring shaping, bidirectional layout, combining marks, or font fallback. Use appropriate layout and shaping support when those behaviors are needed. Test ASCII, multibyte and supplementary characters, combining sequences, right-to-left text, missing glyphs, malformed input, and buffer boundaries as applicable.

