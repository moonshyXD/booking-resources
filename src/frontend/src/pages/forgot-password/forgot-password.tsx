import ContentBox from "../../components/СontentBox/contentBox";
import Wrapper from '../../components/Wrapper/wrapper'
/*import { useState } from "react";*/
import "./forgot-password.css"
/*import {useNavigate} from "react-router-dom";*/


const ForgotPassword = () => {

    return (
        <Wrapper>
            <ContentBox>
                <h1 className="main-text">ВОССТАНОВЛЕНИЕ ПАРОЛЯ</h1>
                <p className="forgot-password-hint">Здесь будет форма ввода email — подключите API, когда будет готов бэкенд.</p>
            </ContentBox>
        </Wrapper>
    )
}

export default ForgotPassword