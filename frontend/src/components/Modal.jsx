import { useEffect, useRef } from "react";
import { X } from "lucide-react";

function getFocusable(root) {
  return Array.from(root.querySelectorAll("button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])")).filter((node) => !node.disabled);
}

function Modal({ title, eyebrow, children, footer, onClose, danger = false }) {
  const ref = useRef(null);

  useEffect(() => {
    const previous = document.activeElement;
    const focusables = getFocusable(ref.current);
    focusables[0]?.focus();
    const onKeyDown = (event) => {
      if (event.key === "Escape") onClose();
      if (event.key === "Tab") {
        const items = getFocusable(ref.current);
        const first = items[0];
        const last = items[items.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last?.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first?.focus();
        }
      }
    };
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      previous?.focus?.();
    };
  }, [onClose]);

  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={onClose}>
      <section className={`modal ${danger ? "modal-danger" : ""}`} role="dialog" aria-modal="true" aria-labelledby="modal-title" ref={ref} onMouseDown={(event) => event.stopPropagation()}>
        <header className="modal-header">
          <div>{eyebrow ? <p className="panel-label">{eyebrow}</p> : null}<h2 id="modal-title">{title}</h2></div>
          <button type="button" className="icon-button" aria-label="Close dialog" onClick={onClose}><X size={17} /></button>
        </header>
        <div className="modal-body">{children}</div>
        {footer ? <footer className="modal-footer">{footer}</footer> : null}
      </section>
    </div>
  );
}

export default Modal;
