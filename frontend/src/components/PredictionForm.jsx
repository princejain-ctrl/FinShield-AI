import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { predictLoan } from "../services/api";
import { usePrediction } from "../context/PredictionContext";

const categoricalOptions = {
  checking_status:["<0","0<=X<200",">=200","no checking"],
  credit_history:["no credits/all paid","all paid","existing paid","delayed previously","critical/other existing credit"],
  purpose:["car","radio/tv","education","furniture/equipment","business","repairs","domestic appliance","vacation","retraining","other"],
  savings_status:["<100","100<=X<500","500<=X<1000",">=1000","no known savings"],
  employment:["unemployed","<1","1<=X<4","4<=X<7",">=7"],
  personal_status:["male single","female div/dep/mar","male div/sep","male mar/wid","female single"],
  other_parties:["none","co applicant","guarantor"],
  property_magnitude:["real estate","life insurance","car","no known property"],
  other_payment_plans:["none","bank","stores"],
  housing:["own","rent","free"],
  job:["unskilled non resident","unskilled resident","skilled","high qual/self emp"],
  own_telephone:["none","yes"],
  foreign_worker:["yes","no"]
};

const numericDefaults = {
  duration:12,
  credit_amount:5000,
  installment_commitment:2,
  residence_since:2,
  age:30,
  existing_credits:1,
  num_dependents:1
};

export default function PredictionForm() {
  const navigate = useNavigate();
  const { setPrediction } = usePrediction();

  const [form, setForm] = useState({
    ...numericDefaults,
    checking_status:"<0",
    credit_history:"existing paid",
    purpose:"car",
    savings_status:"<100",
    employment:"1<=X<4",
    personal_status:"male single",
    other_parties:"none",
    property_magnitude:"real estate",
    other_payment_plans:"none",
    housing:"own",
    job:"skilled",
    own_telephone:"yes",
    foreign_worker:"yes"
  });

  const [loading,setLoading]=useState(false);
  const [error,setError]=useState("");

  const handle=(e)=>{
    const {name,value}=e.target;
    setForm(prev=>({
      ...prev,
      [name]:numericDefaults.hasOwnProperty(name)?Number(value):value
    }));
  };

  const submit = async (e)=>{
    e.preventDefault();

    setLoading(true);
    setError("");

    try{
      const response = await predictLoan(form);

      setPrediction(response);

      navigate("/dashboard");

    }catch(err){
      setError(err?.message || "Prediction failed");
    }finally{
      setLoading(false);
    }
  };

  const inputStyle={
    padding:"12px",
    borderRadius:10,
    background:"#172554",
    color:"#fff",
    border:"1px solid #334155"
  };

  return(
    <div style={{maxWidth:1200,margin:"40px auto",padding:24,color:"white"}}>
      <h2>Credit Risk Prediction</h2>

      <form onSubmit={submit}>
        <div style={{
          display:"grid",
          gridTemplateColumns:"repeat(2,1fr)",
          gap:16
        }}>

          {Object.entries(numericDefaults).map(([k])=>(
            <div key={k}>
              <label>{k}</label>
              <input
                type="number"
                name={k}
                value={form[k]}
                onChange={handle}
                style={inputStyle}
              />
            </div>
          ))}

          {Object.entries(categoricalOptions).map(([k,opts])=>(
            <div key={k}>
              <label>{k}</label>

              <select
                name={k}
                value={form[k]}
                onChange={handle}
                style={inputStyle}
              >
                {opts.map(v=>(
                  <option key={v} value={v}>{v}</option>
                ))}
              </select>
            </div>
          ))}

        </div>

        <button
          type="submit"
          style={{
            marginTop:24,
            padding:"14px 24px",
            background:"#2563eb",
            color:"#fff",
            border:"none",
            borderRadius:10
          }}
        >
          {loading ? "Predicting..." : "Predict Risk"}
        </button>

      </form>

      {error && (
        <p style={{marginTop:20,color:"#ef4444"}}>
          {error}
        </p>
      )}

    </div>
  );
}