import React from "react";
import './contentBox.css'

interface ContentBoxProps {
    children: React.ReactNode
}

const ContentBox = ({children}: ContentBoxProps) =>{
    return (
        <div className="content-box" >
            {children}
        </div>
    )
}


export default ContentBox;