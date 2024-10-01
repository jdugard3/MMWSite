import React, { useContext } from "react";
import { Context } from "../store/appContext";

export const Guitars = () => {
    const { store, actions } = useContext(Context);
    
    return (
        <>
            Guitars Page.
        </>
    )
};

export default Guitars;