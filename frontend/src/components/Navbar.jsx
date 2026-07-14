export default function Navbar() {
    return (
      <nav
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "20px 60px",
          background: "rgba(8,17,31,0.65)",
          backdropFilter: "blur(18px)",
          borderBottom: "1px solid rgba(255,255,255,0.08)",
          zIndex: 1000,
          boxSizing: "border-box",
        }}
      >
        <h2
          style={{
            color: "white",
            margin: 0,
            fontSize: "28px",
            fontWeight: "700",
            letterSpacing: "1px",
          }}
        >
          FinShield AI
        </h2>
  
        <div
          style={{
            display: "flex",
            gap: "35px",
            alignItems: "center",
          }}
        >
          <a href="#" style={linkStyle}>Home</a>
          <a href="#" style={linkStyle}>Dashboard</a>
          <a href="#" style={linkStyle}>Model</a>
          <a href="#" style={linkStyle}>About</a>
  
          <button style={buttonStyle}>
            Get Started
          </button>
        </div>
      </nav>
    );
  }
  
  const linkStyle = {
    color: "#d7e3f4",
    textDecoration: "none",
    fontSize: "17px",
    transition: "0.3s",
  };
  
  const buttonStyle = {
    padding: "12px 22px",
    background: "#2563eb",
    border: "none",
    color: "white",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "600",
  };