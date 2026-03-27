import type { Organization } from '../types/organization'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8006'

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

export const fetchOrganizations = async (): Promise<Organization[]> => {
    const response = await fetch(`${API_BASE_URL}/companies/v1`, {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
    })

    if (!response.ok) {
        throw new Error('Ошибка загрузки организаций')
    }

    const raw = await response.text()
    const data = parseJsonSafely<Organization[]>(raw)
    return data ?? []
}


export const selectOrganization = async (_orgId: string): Promise<void> => Promise.resolve()
