import React, { useContext } from "react";
import { Context } from "../store/appContext";

export const Lessons = () => {
    const { store, actions } = useContext(Context);
    
    return (
        <>
            Lessons Page.
        </>
    )
};

export default Lessons;