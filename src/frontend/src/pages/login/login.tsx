import ContentBox from "../../components/СontentBox/contentBox";
import Wrapper from '../../components/Wrapper/wrapper'
import { useState } from "react";
import "./login.css"
import {useNavigate} from "react-router-dom";
import {z} from "zod"
import { useSelector } from 'react-redux'
import type {RootState} from '../../store/store';


const loginSchema = z.object({
    email: z.string()
        .trim()
        .min(1,"Все поля необходимо заполнить")
        .email("Некорректный email"),
    password: z.string().trim().min(1, "Все поля необходимо заполнить")
})


const Login = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)
    const [errors, setErrors] = useState<{email?: string; password?: string}>({})
    const [validationMessage, setValidationMessage] = useState('')
    const [serverError, setServerError] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const selectedOrg = useSelector((state: RootState) => state.organization.selectedOrg)
    const organizationId = selectedOrg?.id


    const validate = () => {
        setServerError('')
        const trimmedEmail = email.trim()
        const trimmedPassword = password.trim()

        if (!trimmedEmail || !trimmedPassword) {
            const formattedErrors: { email?: string; password?: string } = {}
            if (!trimmedEmail) formattedErrors.email = 'error'
            if (!trimmedPassword) formattedErrors.password = 'error'
            setErrors(formattedErrors)
            setValidationMessage('Все поля необходимо заполнить')
            return false
        }

        const emailValidation = loginSchema.shape.email.safeParse(trimmedEmail)
        if (!emailValidation.success) {
            setErrors({ email: 'error' })
            setValidationMessage('Некорректный email')
            return false
        }

        setErrors({})
        setValidationMessage('')
        return true
    }

    const navigate = useNavigate()
    const navigateToForgotPassword = () => {
        try{
            navigate("/forgot-password")
        }
        catch(error){
            console.error('Ошибка: ', error)}
    }
    const navigateToCatalog = () => {
        try{
            navigate("/catalog")
        }
        catch(error){
            console.error('Ошибка: ', error)}
    }
    const navigateToChooseOrg = () => {
        try{
            navigate("/")
        }
        catch(error){
            console.error('Ошибка: ', error)}
    }

    const handleSubmit = async(e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        if (!validate()) return
        console.log('Отправка на сервер:', {email, password})

        setIsLoading(true)
        setServerError('')
        setValidationMessage('')

        try{
            const response = await fetch('/api/login' /*вот тут жду инфу от бека*/, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password, organizationId})})
            const data = await response.json()

            if (response.ok) {
                console.log('Успех:', data)
                if (data.token) {
                    localStorage.setItem('token', data.token)
                }
                navigateToCatalog()
            } else {
                setServerError(data.message || 'Неверный логин или пароль')
                setErrors({
                    email: 'error',
                    password: 'error'
                })
            }

        }catch (error) {
            setServerError('Ошибка соединения с сервером')
        } finally {
            setIsLoading(false)
        }

    }

    return (
        <Wrapper>
            <div className="login-page">
            <ContentBox>
                <form onSubmit={handleSubmit} noValidate>
                    <div className="main-text">ВХОД В УЧЕТНУЮ ЗАПИСЬ</div>

                    <div className="login-field">
                        <label className="form-label login-label" htmlFor="login-email">ЛОГИН</label>
                        <input
                            maxLength={100}
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            id="login-email"
                            type="email"
                            className={errors.email ? "form-control-error" : "form-control"}
                            placeholder="email"
                        />
                    </div>

                    <div className="login-field">
                        <i className={`bi bi-eye${showPassword ? '' : '-slash'} icons`}
                           onClick={() => setShowPassword(!showPassword)}
                           style={{ cursor: 'pointer' }}
                        ></i>
                        <label htmlFor="inputPassword5" className="form-label login-label">ПАРОЛЬ</label>
                        <input
                            maxLength={100}
                            value={password}
                            onChange={(e)=> setPassword(e.target.value)}
                            type={showPassword ? 'text' : 'password'}
                            id="inputPassword5"
                            className={errors.password ? "form-control-error" : "form-control"}
                            aria-describedby="passwordHelpBlock"
                            placeholder="password"
                        />
                    </div>

                    <div className="forgot-pass" onClick={navigateToForgotPassword}> Забыли пароль?</div>
                    {validationMessage && <div className="errors-message">{validationMessage}</div>}
                    {serverError && <div className="errors-message">{serverError}</div>}
                    <button type="submit" className="btn button-to-entrance" disabled={isLoading} > ВОЙТИ</button>
                    <div className="to-org" onClick={navigateToChooseOrg}> &lt;&lt;НАЗАД</div>
                </form>
            </ContentBox>
            </div>
        </Wrapper>
    )
}

export default Login