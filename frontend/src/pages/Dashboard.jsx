import { Navigate } from "react-router-dom";
import { usePrediction } from "../context/PredictionContext";

export default function Dashboard() {
  const { prediction } = usePrediction();

  if (!prediction) {
    return <Navigate to="/" replace />;
  }

  const { prediction: result, explanation } = prediction;

  const badgeColor =
    result.risk_level === "high"
      ? "#ef4444"
      : result.risk_level === "medium"
      ? "#f59e0b"
      : "#22c55e";

  return (
    <div
      style={{
        maxWidth: "1200px",
        margin: "40px auto",
        padding: "30px",
        color: "white",
      }}
    >
      <h1
        style={{
          fontSize: "42px",
          marginBottom: "10px",
        }}
      >
        Prediction Dashboard
      </h1>

      <p
        style={{
          color: "#94a3b8",
          marginBottom: "35px",
        }}
      >
        Explainable AI credit risk assessment
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: "20px",
          marginBottom: "35px",
        }}
      >
        <Metric
          title="Bad Credit Probability"
          value={`${(result.probability_bad * 100).toFixed(2)}%`}
        />

        <Metric
          title="Good Credit Probability"
          value={`${(result.probability_good * 100).toFixed(2)}%`}
        />

        <Metric
          title="Prediction"
          value={result.class.toUpperCase()}
        />

        <Metric
          title="Risk Level"
          value={
            <span
              style={{
                color: badgeColor,
                fontWeight: 700,
              }}
            >
              {result.risk_level.toUpperCase()}
            </span>
          }
        />
      </div>

      <div
        style={{
          background: "rgba(255,255,255,.05)",
          border: "1px solid rgba(255,255,255,.08)",
          borderRadius: "20px",
          padding: "28px",
        }}
      >
        <h2
          style={{
            marginTop: 0,
            marginBottom: "20px",
          }}
        >
          Top SHAP Contributors
        </h2>

        {explanation.top_contributors.map((item, index) => (
          <div
            key={index}
            style={{
              marginBottom: "18px",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: "6px",
              }}
            >
              <span>{item.feature}</span>

              <strong>{item.shap_value.toFixed(4)}</strong>
            </div>

            <div
              style={{
                height: "8px",
                background: "#1e293b",
                borderRadius: "999px",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${Math.min(
                    Math.abs(item.shap_value) * 100,
                    100
                  )}%`,
                  height: "100%",
                  background:
                    item.shap_value >= 0
                      ? "#ef4444"
                      : "#22c55e",
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Metric({ title, value }) {
  return (
    <div
      style={{
        background: "rgba(255,255,255,.05)",
        border: "1px solid rgba(255,255,255,.08)",
        borderRadius: "18px",
        padding: "24px",
      }}
    >
      <div
        style={{
          color: "#94a3b8",
          marginBottom: "12px",
          fontSize: "14px",
        }}
      >
        {title}
      </div>

      <div
        style={{
          fontSize: "30px",
          fontWeight: "700",
        }}
      >
        {value}
      </div>
    </div>
  );
}