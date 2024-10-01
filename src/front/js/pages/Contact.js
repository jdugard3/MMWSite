import React, { useContext } from "react";
import { Context } from "../store/appContext";

export const Contact = () => {
    const { store, actions } = useContext(Context);
    
    return (
        <>
            Contact Page.
        </>
    )
};

export default Contact;