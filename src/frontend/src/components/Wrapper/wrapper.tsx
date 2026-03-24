import React from "react";
import './wrapper.css'

interface WrapperProps {
    children: React.ReactNode
}

const Wrapper = ({children}: WrapperProps) =>{
    return (
        <div className="wrapper" >
            {children}
        </div>
    )
}


export default Wrapper;