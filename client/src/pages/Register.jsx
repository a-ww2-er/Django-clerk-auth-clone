import React from "react";
import Form from "../components/Form";

function Register() {
  return (
    <div>
      <Form route="/api/user/register/" method={"register"} />
    </div>
  );
}

export default Register;
