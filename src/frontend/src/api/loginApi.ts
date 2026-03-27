import type { LoginCredentials, LoginResponse } from '../types/login'
import type { CurrentUser } from '../types/user'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'https://localhost/iam'

const parseJsonSafely = <T>(raw: string): T | null => {
  if (!raw.trim()) {
    return null
  }

  try {
    return JSON.parse(raw) as T
  } catch {
    return null
  }
}

export const auth = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const response = await fetch(`${API_BASE_URL}/auth/v1/login`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  })

  const raw = await response.text()
  const data = parseJsonSafely<Partial<LoginResponse> & { detail?: unknown }>(raw) ?? {}

  if (!response.ok) {
    throw new Error('Неверный логин или пароль')
  }

  if (!data.message || !data.role) {
    throw new Error('Некорректный ответ сервера')
  }

  return {
    message: data.message,
    role: data.role,
  }
}

export const fetchCurrentUser = async (): Promise<CurrentUser> => {
  const meEndpoint = import.meta.env.VITE_ME_ENDPOINT ?? '/users/v1/me'
  const response = await fetch(`${API_BASE_URL}${meEndpoint}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  const raw = await response.text()
  const data = parseJsonSafely<{ email?: string; role?: string }>(raw) ?? {}

  if (!response.ok || !data.email || !data.role) {
    throw new Error('Пользователь не авторизован')
  }

  return {
    email: data.email,
    role: data.role,
  }
}