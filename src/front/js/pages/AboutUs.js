import React, { useContext } from "react";
import { Context } from "../store/appContext";

export const AboutUs = () => {
    const { store, actions } = useContext(Context);
    
    return (
        <>
            About Us Page
        </>
    )
};

export default AboutUs;
