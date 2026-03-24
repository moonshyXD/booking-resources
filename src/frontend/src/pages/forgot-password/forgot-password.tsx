import ContentBox from "../../components/СontentBox/contentBox";
import Wrapper from '../../components/Wrapper/wrapper'
import { useState } from "react";
import "./forgot-password.css"
import {useNavigate} from "react-router-dom";
import { z } from "zod";


const forgotPasswordSchema = z.object({
    email: z.string()
        .trim()
        .min(1, "Поле необходимо заполнить")
        .email("Некорректный email"),
})

const ForgotPassword = () => {
    const [email, setEmail] = useState('')
    const [errors, setErrors] = useState<{ email?: string }>({})
    const [validationMessage, setValidationMessage] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const navigate = useNavigate()

    const handleBack = () => {
        navigate('/login')
    }

    const validate = () => {
        const result = forgotPasswordSchema.safeParse({ email })
        if (result.success) {
            setErrors({})
            setValidationMessage('')
            return true
        }

        setErrors({ email: 'error' })
        const firstMessage = result.error.issues[0]?.message ?? 'Ошибка валидации'
        setValidationMessage(firstMessage)
        return false
    }

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        if (!validate()) return
        setIsLoading(true)
        setValidationMessage('')

        try {
            const response = await fetch('/api/forgot-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email.trim() }),
            })

            let data: { message?: string } = {}
            try {
                data = await response.json()
            } catch {
                data = {}
            }

            if (!response.ok) {
                if (response.status === 404) {
                    setErrors({ email: 'error' })
                    setValidationMessage('Аккаунт не найден')
                } else {
                    setValidationMessage(data.message || 'Ошибка восстановления пароля')
                }
                return
            }

            navigate('/forgot-password/success')
        } catch {
            setValidationMessage('Ошибка соединения с сервером')
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <Wrapper>
            <div className="forgot-password-page">
                <ContentBox>
                    <form onSubmit={handleSubmit} noValidate>
                        <h1 className="reset-title">СБРОС ПАРОЛЯ</h1>

                        <div className="reset-field">
                            <label className="reset-label" htmlFor="reset-email">ВВЕДИТЕ ЭЛЕКТРОННУЮ ПОЧТУ</label>
                            <input
                                id="reset-email"
                                type="email"
                                className={errors.email ? "reset-input reset-input-error" : "reset-input"}
                                placeholder="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                maxLength={100}
                            />
                        </div>

                        {validationMessage && <div className="errors-message">{validationMessage}</div>}

                        <div className="reset-actions">
                            <button type="button" className="btn-reset-back" onClick={handleBack}>&lt;&lt;НАЗАД</button>
                            <button type="submit" className="btn btn-reset-continue" disabled={isLoading}>
                                {isLoading ? 'ОТПРАВКА...' : 'ПРОДОЛЖИТЬ'}
                            </button>
                        </div>
                    </form>
                </ContentBox>
            </div>
        </Wrapper>
    )
}

export default ForgotPassword