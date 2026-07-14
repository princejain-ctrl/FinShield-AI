import Navbar from "./Navbar";

export default function Layout({ children }) {
  return (
    <>
      <Navbar />

      <div
        style={{
          minHeight: "100vh",
          background:
            "radial-gradient(circle at top, #13284a 0%, #08111f 45%, #050b16 100%)",
          color: "white",
          paddingTop: "90px",
        }}
      >
        {children}
      </div>
    </>
  );
}