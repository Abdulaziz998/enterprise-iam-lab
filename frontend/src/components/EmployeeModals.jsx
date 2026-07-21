import { useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2 } from "lucide-react";
import Modal from "./Modal";
import StatusBadge from "./StatusBadge";

const emptyEmployee = { employee_id: "", first_name: "", last_name: "", department: "", manager: "", job_title: "" };

function accessForRole(roles, jobTitle) {
  return roles.find((role) => role.job_title === jobTitle) || { groups: [], applications: [] };
}

function Field({ label, error, children }) {
  return <label className="form-field"><span>{label}</span>{children}{error ? <small className="field-error">{error}</small> : null}</label>;
}

export function CreateEmployeeModal({ roles, onClose, onSubmit }) {
  const [form, setForm] = useState({ ...emptyEmployee, job_title: roles[0]?.job_title || "" });
  const [submitting, setSubmitting] = useState(false);
  const [apiError, setApiError] = useState("");
  const preview = accessForRole(roles, form.job_title);
  const errors = useMemo(() => {
    const next = {};
    if (!form.employee_id.trim()) next.employee_id = "Employee ID is required.";
    if (!form.first_name.trim()) next.first_name = "First name is required.";
    if (!form.last_name.trim()) next.last_name = "Last name is required.";
    if (!form.department.trim()) next.department = "Department is required.";
    if (!form.job_title.trim()) next.job_title = "Select a role.";
    return next;
  }, [form]);
  const invalid = Object.keys(errors).length > 0;
  const update = (key, value) => {
    setApiError("");
    setForm((current) => ({ ...current, [key]: value }));
  };
  const submit = async (event) => {
    event.preventDefault();
    if (invalid) return;
    setSubmitting(true);
    setApiError("");
    try {
      await onSubmit({ ...form, status: "active", manager: form.manager || null });
    } catch (error) {
      setApiError(error.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal title="Create Employee" eyebrow="Joiner Workflow" onClose={onClose} footer={<><button type="button" className="secondary-button" onClick={onClose} disabled={submitting}>Cancel</button><button type="submit" form="create-employee-form" className="primary-button" disabled={invalid || submitting}>{submitting ? "Creating..." : "Create Employee"}</button></>}>
      <form id="create-employee-form" className="operation-form" onSubmit={submit}>
        {apiError ? <div className="inline-error" role="alert">{apiError}</div> : null}
        <section><h3>Identity</h3><div className="form-grid"><Field label="Employee ID" error={errors.employee_id}><input value={form.employee_id} onChange={(e) => update("employee_id", e.target.value)} /></Field><Field label="First Name" error={errors.first_name}><input value={form.first_name} onChange={(e) => update("first_name", e.target.value)} /></Field><Field label="Last Name" error={errors.last_name}><input value={form.last_name} onChange={(e) => update("last_name", e.target.value)} /></Field></div></section>
        <section><h3>Employment</h3><div className="form-grid"><Field label="Department" error={errors.department}><input value={form.department} onChange={(e) => update("department", e.target.value)} /></Field><Field label="Manager"><input value={form.manager} onChange={(e) => update("manager", e.target.value)} /></Field><Field label="Job Title" error={errors.job_title}><select value={form.job_title} onChange={(e) => update("job_title", e.target.value)}><option value="">Select role</option>{roles.map((role) => <option key={role.job_title}>{role.job_title}</option>)}</select></Field></div></section>
        <section><h3>Access Preview</h3><AccessPreview role={preview} /></section>
      </form>
    </Modal>
  );
}

export function MoveEmployeeModal({ employee, roles, onClose, onSubmit }) {
  const [jobTitle, setJobTitle] = useState(employee.job_title || roles[0]?.job_title || "");
  const [submitting, setSubmitting] = useState(false);
  const [apiError, setApiError] = useState("");
  const preview = accessForRole(roles, jobTitle);
  const changed = jobTitle && jobTitle !== employee.job_title;
  const submit = async () => {
    if (!changed) return;
    setSubmitting(true);
    setApiError("");
    try {
      await onSubmit(employee.employee_id, jobTitle);
    } catch (error) {
      setApiError(error.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal title="Change Role" eyebrow="Mover Workflow" onClose={onClose} footer={<><button type="button" className="secondary-button" onClick={onClose} disabled={submitting}>Cancel</button><button type="button" className="primary-button" onClick={submit} disabled={!changed || submitting}>{submitting ? "Updating..." : "Submit Role Change"}</button></>}>
      <div className="operation-form">
        {apiError ? <div className="inline-error" role="alert">{apiError}</div> : null}
        <div className="employee-context"><strong>{employee.first_name} {employee.last_name}</strong><span>{employee.employee_id}</span><StatusBadge status={employee.status} /></div>
        <Field label="Existing roles"><select value={jobTitle} onChange={(e) => setJobTitle(e.target.value)}>{roles.map((role) => <option key={role.job_title}>{role.job_title}</option>)}</select></Field>
        <div className="role-change-preview"><div><span>Current Role</span><strong>{employee.job_title}</strong></div><div><span>New Role</span><strong>{jobTitle}</strong></div></div>
        <AccessPreview role={preview} />
      </div>
    </Modal>
  );
}

export function TerminateEmployeeModal({ employee, onClose, onSubmit }) {
  const [submitting, setSubmitting] = useState(false);
  const [apiError, setApiError] = useState("");
  const submit = async () => {
    setSubmitting(true);
    setApiError("");
    try {
      await onSubmit(employee.employee_id);
    } catch (error) {
      setApiError(error.message);
    } finally {
      setSubmitting(false);
    }
  };
  return (
    <Modal title="Terminate Employee" eyebrow="Leaver Workflow" danger onClose={onClose} footer={<><button type="button" className="secondary-button" onClick={onClose} disabled={submitting}>Cancel</button><button type="button" className="danger-button" onClick={submit} disabled={submitting}>{submitting ? "Terminating..." : "Terminate Employee"}</button></>}>
      <div className="warning-panel"><AlertTriangle size={20} /><div><strong>{employee.first_name} {employee.last_name}</strong><p>{employee.department} · {employee.job_title}</p></div></div>
      {apiError ? <div className="inline-error" role="alert">{apiError}</div> : null}
      <ul className="impact-list"><li><CheckCircle2 size={16} /> Groups will be removed.</li><li><CheckCircle2 size={16} /> Applications will be removed.</li><li><CheckCircle2 size={16} /> Status will change to terminated.</li></ul>
    </Modal>
  );
}

function AccessPreview({ role }) {
  return <div className="access-preview"><div><span>Groups</span><div className="chip-group">{(role.groups || []).map((item) => <span className="chip" key={item}>{item}</span>)}</div></div><div><span>Applications</span><div className="chip-group">{(role.applications || []).map((item) => <span className="chip app-chip" key={item}>{item}</span>)}</div></div></div>;
}
