import React, { useContext } from "react";
import { Context } from "../store/appContext";

export const Pianos = () => {
    const { store, actions } = useContext(Context);
    
    return (
        <>
            Pianos Page.
        </>
    )
};

export default Pianos;