"use client";

export default function Loader() {
  return (
    <div className="loader-overlay">
      <div className="loader-container">
        <div className="spinner-large"></div>
        <p>Processing...</p>
      </div>
    </div>
  );
}
