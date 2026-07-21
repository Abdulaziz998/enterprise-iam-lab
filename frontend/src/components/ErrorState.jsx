function ErrorState({ message, onRetry }) {
  return <div className="error-state" role="alert"><p className="error-title">Unable to load this view</p><p className="error-message">{message}</p>{onRetry ? <button type="button" className="secondary-button" onClick={onRetry}>Retry</button> : null}</div>;
}

export default ErrorState;
