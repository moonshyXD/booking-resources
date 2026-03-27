export const forgotPassword = async (email: string) => {
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8006'

    const response = await fetch(`${apiBaseUrl}/users/v1/password`, {
        method: 'PATCH',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email.trim() }),
    })

    const raw = await response.text()
    let data: { message?: string } = {}
    if (raw.trim()) {
        try {
            data = JSON.parse(raw) as { message?: string }
        } catch {
            data = {}
        }
    }

    if (!response.ok) {
        if (response.status === 404) {
            throw new Error('Аккаунт не найден')
        }
        throw new Error(data.message || 'Ошибка восстановления пароля')
    }

    return data
}