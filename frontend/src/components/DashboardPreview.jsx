export default function DashboardPreview() {
    const card = {
      background: "rgba(255,255,255,.05)",
      border: "1px solid rgba(255,255,255,.08)",
      borderRadius: "20px",
      padding: "22px",
      backdropFilter: "blur(18px)",
    };
  
    return (
      <section
        style={{
          maxWidth: "1200px",
          margin: "100px auto",
          padding: "0 30px",
        }}
      >
        <h2
          style={{
            fontSize: "42px",
            marginBottom: "40px",
            textAlign: "center",
          }}
        >
          Live AI Dashboard
        </h2>
  
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4,1fr)",
            gap: "20px",
            marginBottom: "25px",
          }}
        >
          <Card title="Risk Score" value="94 /100" color="#22c55e" />
          <Card title="Default Probability" value="6.2%" color="#3b82f6" />
          <Card title="Model Confidence" value="97.8%" color="#f59e0b" />
          <Card title="Prediction" value="APPROVED" color="#10b981" />
        </div>
  
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.4fr 1fr",
            gap: "20px",
          }}
        >
          <div style={card}>
            <h3>SHAP Explainability</h3>
  
            <div
              style={{
                height: "280px",
                borderRadius: "16px",
                background: "#101b30",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "#6b7280",
              }}
            >
              SHAP Plot (Backend)
            </div>
          </div>
  
          <div style={card}>
            <h3>Feature Importance</h3>
  
            <div
              style={{
                height: "280px",
                borderRadius: "16px",
                background: "#101b30",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "#6b7280",
              }}
            >
              Feature Chart
            </div>
          </div>
        </div>
      </section>
    );
  }
  
  function Card({ title, value, color }) {
    return (
      <div
        style={{
          background: "rgba(255,255,255,.05)",
          border: "1px solid rgba(255,255,255,.08)",
          borderRadius: "20px",
          padding: "22px",
        }}
      >
        <div
          style={{
            color: "#94a3b8",
            marginBottom: "12px",
          }}
        >
          {title}
        </div>
  
        <div
          style={{
            fontSize: "32px",
            color,
            fontWeight: "700",
          }}
        >
          {value}
        </div>
      </div>
    );
  }