import type { Organization } from '../types/organization'

// Временные данные, пока нет бэкенда
const MOCK_ORGANIZATIONS: Organization[] = [
    { id: 1, name: 'Холдинг TI' },
    { id: 2, name: 'Т-банк' },
    { id: 3, name: 'WB' },
    { id: 4, name: 'OZON' },
    { id: 5, name: 'Yandex' },
    { id: 6, name: 'IT-центр' },
]

export const fetchOrganizations = async (): Promise<Organization[]> => {
    await new Promise(resolve => setTimeout(resolve, 1000))

    return MOCK_ORGANIZATIONS

    // const response = await fetch('/api/organizations')
    // if (!response.ok) throw new Error('Ошибка загрузки организаций')
    // return response.json()
}


export const selectOrganization = async (orgId: number): Promise<void> => {
    const response = await fetch('/api/select-organization', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({organizationId: orgId}),
    })

    if (!response.ok) {
        throw new Error("Ошибка при выборе организации")
    }
}
