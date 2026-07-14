import DashboardPreview from "../components/DashboardPreview";
import PredictionForm from "../components/PredictionForm";
export default function Home() {
    return (
        <>
          <section
        style={{
          minHeight: "calc(100vh - 90px)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "80px 40px",
          position: "relative",
        }}
      >
        <div
          style={{
            position: "absolute",
            width: "500px",
            height: "500px",
            borderRadius: "50%",
            background: "#2563eb",
            filter: "blur(180px)",
            opacity: 0.18,
            top: "-120px",
            left: "-120px",
          }}
        />
  
        <div
          style={{
            maxWidth: "1200px",
            width: "100%",
            display: "grid",
            gridTemplateColumns: "1.2fr 1fr",
            gap: "70px",
            alignItems: "center",
          }}
        >
          {/* LEFT SIDE */}
  
          <div>
            <div
              style={{
                display: "inline-block",
                padding: "8px 18px",
                borderRadius: "999px",
                background: "rgba(37,99,235,.15)",
                color: "#7db4ff",
                border: "1px solid rgba(37,99,235,.3)",
                marginBottom: "30px",
                fontWeight: "600",
              }}
            >
              AI Credit Intelligence Platform
            </div>
  
            <h1
              style={{
                fontSize: "72px",
                lineHeight: "1.05",
                margin: 0,
                fontWeight: "800",
              }}
            >
              Predict
              <span style={{ color: "#3b82f6" }}> Loan Risk </span>
              Before It Happens.
            </h1>
  
            <p
              style={{
                marginTop: "28px",
                fontSize: "21px",
                color: "#94a3b8",
                lineHeight: "1.8",
                maxWidth: "650px",
              }}
            >
              FinShield AI uses Explainable AI, XGBoost and intelligent credit
              analytics to predict loan defaults with transparent risk scoring.
            </p>
  
            <div
              style={{
                display: "flex",
                gap: "20px",
                marginTop: "45px",
              }}
            >
              <button
                style={{
                  background: "#2563eb",
                  color: "white",
                  border: "none",
                  padding: "18px 34px",
                  borderRadius: "14px",
                  cursor: "pointer",
                  fontSize: "17px",
                  fontWeight: "600",
                }}
              >
                Try Live Demo
              </button>
  
              <button
                style={{
                  background: "transparent",
                  color: "white",
                  border: "1px solid rgba(255,255,255,.15)",
                  padding: "18px 34px",
                  borderRadius: "14px",
                  cursor: "pointer",
                  fontSize: "17px",
                }}
              >
                View Model
              </button>
            </div>
          </div>
  
          {/* RIGHT SIDE */}
  
          <div
            style={{
              background: "rgba(255,255,255,.05)",
              backdropFilter: "blur(20px)",
              border: "1px solid rgba(255,255,255,.08)",
              borderRadius: "28px",
              padding: "35px",
              boxShadow: "0 20px 60px rgba(0,0,0,.35)",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: "30px",
              }}
            >
              <div>
                <div style={{ color: "#94a3b8", fontSize: "14px" }}>
                  Applicant
                </div>
                <h3 style={{ margin: "8px 0" }}>John Anderson</h3>
              </div>
  
              <div
                style={{
                  color: "#22c55e",
                  background: "rgba(34,197,94,.15)",
                  padding: "10px 16px",
                  borderRadius: "10px",
                  height: "fit-content",
                }}
              >
                APPROVED
              </div>
            </div>
  
            <hr style={{ borderColor: "rgba(255,255,255,.08)" }} />
  
            <div style={{ marginTop: "30px" }}>
              <Metric title="Credit Score" value="812" />
              <Metric title="Default Probability" value="6.2%" />
              <Metric title="Risk Category" value="Low Risk" />
              <Metric title="Model Confidence" value="97.8%" />
            </div>
          </div>
        </div>
        </section>

<DashboardPreview />
<PredictionForm />
</>
);
}
  
  function Metric({ title, value }) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "22px",
        }}
      >
        <span style={{ color: "#94a3b8" }}>{title}</span>
  
        <strong>{value}</strong>
      </div>
    );
  }