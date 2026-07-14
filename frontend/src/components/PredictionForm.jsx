import { useState } from "react";
import { predictLoan } from "../services/api";

export default function PredictionForm() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
    const inputStyle = {
      width: "100%",
      padding: "14px 16px",
      borderRadius: "12px",
      border: "1px solid rgba(255,255,255,.08)",
      background: "rgba(255,255,255,.05)",
      color: "white",
      fontSize: "15px",
      outline: "none",
      boxSizing: "border-box",
    };

    async function handlePredict() {
      setLoading(true);
    
      const sample = {
        checking_status: "<0",
        credit_history: "existing paid",
        purpose: "radio/tv",
        savings_status: "<100",
        employment: "1<=X<4",
        personal_status: "male single",
        other_parties: "none",
        property_magnitude: "car",
        other_payment_plans: "none",
        housing: "own",
        job: "skilled",
        own_telephone: "yes",
        foreign_worker: "yes",
    
        duration: 12,
        credit_amount: 2500,
        installment_commitment: 2,
        residence_since: 3,
        age: 35,
        existing_credits: 1,
        num_dependents: 1,
      };
    
      const response = await predictLoan(sample);
    
      setResult(response);
      setLoading(false);
    }
  
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
            textAlign: "center",
            marginBottom: "15px",
          }}
        >
          Try FinShield AI
        </h2>
  
        <p
          style={{
            textAlign: "center",
            color: "#94a3b8",
            marginBottom: "50px",
          }}
        >
          Enter applicant details and predict loan default risk.
        </p>
  
        <div
          style={{
            background: "rgba(255,255,255,.05)",
            border: "1px solid rgba(255,255,255,.08)",
            borderRadius: "24px",
            backdropFilter: "blur(18px)",
            padding: "35px",
          }}
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(2,1fr)",
              gap: "20px",
            }}
          >
            <input placeholder="Applicant Name" style={inputStyle} />
            <input placeholder="Age" style={inputStyle} />
  
            <input placeholder="Annual Income" style={inputStyle} />
            <input placeholder="Loan Amount" style={inputStyle} />
  
            <input placeholder="Credit Score" style={inputStyle} />
            <input placeholder="Employment Length" style={inputStyle} />
  
            <input placeholder="Loan Term (months)" style={inputStyle} />
            <input placeholder="Debt-To-Income Ratio" style={inputStyle} />
  
            <select style={inputStyle}>
              <option>Home Ownership</option>
              <option>Rent</option>
              <option>Own</option>
              <option>Mortgage</option>
            </select>
  
            <select style={inputStyle}>
              <option>Loan Purpose</option>
              <option>Education</option>
              <option>Medical</option>
              <option>Business</option>
              <option>Personal</option>
            </select>
          </div>
  
          <div
            style={{
              textAlign: "center",
              marginTop: "35px",
            }}
          >
            <button
              onClick={handlePredict}
              style={{
                background: "#2563eb",
                color: "white",
                border: "none",
                borderRadius: "14px",
                padding: "16px 38px",
                fontSize: "17px",
                cursor: "pointer",
                fontWeight: "600",
              }}
            >
              {loading ? "Predicting..." : "Predict Risk"}
            </button>
          </div>
        </div>
      </section>
    );
  }