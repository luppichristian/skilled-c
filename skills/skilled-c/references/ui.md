# User interfaces

## Approach and state

Always prefer an immediate-mode UI approach over a retained-mode UI. Describe the visible controls from current application state on each UI update, and let interactions request or perform changes to that state. Keep the application or document as the source of truth; route changes through its normal validation and, where applicable, undo/redo logic instead of maintaining a separate authoritative copy in widgets.

Immediate mode does not mean that all state is temporary or that the application must redraw continuously. Keep a UI context for state that spans updates, such as focus, an active drag, scroll positions, text editing, and useful caches. For idle applications, update and redraw in response to events or invalidation; continue updates as needed for animation and other time-dependent behavior. Follow [Runtime loops](runtime-loops.md) for event and presentation timing.

Give interactive controls stable, unique IDs. Scope IDs by container and underlying object identity, especially for repeated controls; a changing label or a list index that changes after reordering is not a reliable identity. Clear or transfer focus and active state safely when controls or their backing objects disappear.

## Layout and geometry

Use consistent coordinates for layout, pointer input, and drawing, converting explicitly between logical units and device pixels. Represent rectangles consistently; half-open bounds make adjacent regions unambiguous. Intersect child clips with the active parent clip and viewport. Apply scrolling to both drawing and hit testing, and define paint and hit-test order for overlapping controls and overlays.

For simple interfaces, lay out regions by cutting rectangles. Start with the available rectangle; cut a strip from a chosen edge, return that strip, and shrink the remaining rectangle. Repeat in a deliberate order, nesting the same operation for rows and columns. For example, cut a toolbar from the top, cut its buttons from either side, and use the remainder for its title; then cut a sidebar from the remaining window and give the rest to the main view. Keep the choice of edge with the caller, so a content-sized control can be packed from either side.

Measure text and other content before cutting content-sized regions, including padding and gaps. Clamp cuts to the available extent and define what happens when the window is too small: reflow, scroll, clip, or apply minimum sizes as appropriate. Use the same font, scale, and text metrics for measurement and rendering. Recompute layout and invalidate affected measurements when window size, DPI, fonts, or content change.

## Interaction and rendering

Process pointer, keyboard, text, scroll, and window events without losing transitions that occur between UI updates. Distinguish hover, active/pressed, and keyboard focus. Hit-test the visible clipped region in front-to-back interaction order. Disabled controls must not activate; define whether they block or pass pointer events so a click does not accidentally reach a control behind them. For a button, a typical click requires a press on the control followed by a release over it. Keep the active control through a drag, using platform pointer capture when available to receive events outside the window. Handle cancellation, focus loss, and control removal so a missing release cannot leave the control active. Do not treat a held button as a new click on every update.

Support keyboard navigation and activation, visible focus, meaningful labels, and platform accessibility integration as required by the application. Handle text input separately from key presses, including composition when the target platform requires it. Draw from the computed geometry with matching clip and stacking rules; ensure text, images, and other data remain valid until their rendering consumers finish. See [Graphics](graphics.md) for renderer selection and GPU resource lifetimes.

## Clay for complex interfaces

Use [Clay](https://github.com/nicbarker/clay) only for complex interfaces that benefit from its nested, responsive layout, text wrapping, scrolling, or other layout features. For simple interfaces, use direct layout such as rectangle cutting. Clay is a layout library that emits render commands, not a complete widget or rendering system; the application must provide the renderer and the interaction, text input, and accessibility behavior it needs.

When using Clay, size its arena and handle reported errors; supply a text-measurement function consistent with the renderer. Feed the viewport and pointer state, and update scrolling when used, before building the layout. Declare the UI and consume the resulting commands in order, implementing the command types and clipping used by the interface. Keep IDs stable, honor the pinned version's data and command lifetimes, and remember that text slices need not be null-terminated. Invalidate Clay's measurement cache when external factors such as DPI change its measurements. Pointer-over queries use the previous layout, so account for newly created or moving controls and resizing when current-layout precision matters.

Check representative sizes and DPI scales, narrow windows, clipped or overlapping controls, scrolling, keyboard focus, text input, and press-drag-release behavior. Profile realistic interfaces before adding caching or other complexity.
