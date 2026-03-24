import ContentBox from "../../components/СontentBox/contentBox";
import Wrapper from '../../components/Wrapper/wrapper'
import { useNavigate } from "react-router-dom";
import "./forgot-password-success.css"

const ForgotPasswordSuccess = () => {
    const navigate = useNavigate()

    return (
        <Wrapper>
            <div className="forgot-password-success-page">
                <ContentBox>
                    <div className="success-text">
                        Мы отправили новый пароль на указанный
                        <br />
                        вами адрес электронной почты.
                        <br />
                        Пожалуйста, проверьте вашу почту - письмо
                        <br />
                        должно прийти в течение нескольких минут.
                    </div>
                    <div className="success-hint">
                        Если вы не видите письма, проверьте папку "Спам" или
                        <br />
                        "Нежелательная почта".
                    </div>

                    <button
                        type="button"
                        className="btn success-back-to-login"
                        onClick={() => navigate('/login')}
                    >
                        НА СТРАНИЦУ ВХОДА
                    </button>
                </ContentBox>
            </div>
        </Wrapper>
    )
}

export default ForgotPasswordSuccess

