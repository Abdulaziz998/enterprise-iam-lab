function LoadingState({ message = "Loading content..." }) {
  return <div className="loading-state" role="status" aria-live="polite"><div className="skeleton-stack" aria-hidden="true"><span /><span /><span /></div><p>{message}</p></div>;
}

export default LoadingState;
