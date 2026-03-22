import ContentBox from "../../components/СontentBox/contentBox";
import Wrapper from '../../components/Wrapper/wrapper'
import { useState } from "react";
import "./login.css"
import {useNavigate} from "react-router-dom";


const Login = () => {
    const [showPassword, setShowPassword] = useState(false)
    const navigate = useNavigate()
    const navigateToForgotPassword = () => {
        try{
            navigate("/forgot-password")
        }
        catch(error){
            console.error('Ошибка: ', error)}
    }

    return (
        <Wrapper>
            <ContentBox>
                <div className="main-text">ВХОД В УЧЕТНУЮ ЗАПИСЬ</div>

                <div className="login-field">
                    <label className="form-label login-label" htmlFor="login-email">ЛОГИН</label>
                    <input id="login-email" type="email" className="form-control" placeholder="email"/>
                </div>

                <div className="login-field">
                    <i className={`bi bi-eye${showPassword ? '' : '-slash'} icons`}
                       onClick={() => setShowPassword(!showPassword)}
                       style={{ cursor: 'pointer' }}
                    ></i>
                    <label htmlFor="inputPassword5" className="form-label login-label">ПАРОЛЬ</label>
                    <input type={showPassword ? 'text' : 'password'} id="inputPassword5" className="form-control"
                           aria-describedby="passwordHelpBlock" placeholder="password"/>
                </div>

                <div className="forgot-pass" onClick={navigateToForgotPassword}> Забыли пароль?</div>
                <button type="button" className="btn button-to-entrance" > ВОЙТИ</button>


            </ContentBox>
        </Wrapper>
    )
}

export default Login