import { createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'
import type { Organization } from '../types/organization'

interface OrganizationState {
    selectedOrg: Organization | null
    selectedOrgId: string | null
    selectedOrgSlug: string | null
    isLoading: boolean
    error: string | null
}

const getInitialState = (): OrganizationState => {
    if (typeof window === 'undefined') {
        return {
            selectedOrg: null,
            selectedOrgId: null,
            selectedOrgSlug: null,
            isLoading: false,
            error: null,
        }
    }

    const persistedId = localStorage.getItem('organizationId')
    const persistedSlug = localStorage.getItem('organizationSlug')

    return {
        selectedOrg: null,
        selectedOrgId: persistedId,
        selectedOrgSlug: persistedSlug,
        isLoading: false,
        error: null,
    }
}

const initialState: OrganizationState = getInitialState()

const organizationSlice = createSlice({
    name: 'organization',
    initialState,
    reducers: {
        setOrganization: (state, action: PayloadAction<Organization>) => {
            state.selectedOrg = action.payload
            state.selectedOrgId = action.payload.id
            state.selectedOrgSlug = action.payload.slug
            state.error = null
        },
        hydrateOrganizationFromStorage: (state, action: PayloadAction<{ id: string | null; slug: string | null }>) => {
            state.selectedOrgId = action.payload.id
            state.selectedOrgSlug = action.payload.slug
        },
        setOrganizationLoading: (state, action: PayloadAction<boolean>) => {
            state.isLoading = action.payload
        },
        setOrganizationError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload
        },
        clearOrganization: (state) => {
            state.selectedOrg = null
            state.selectedOrgId = null
            state.selectedOrgSlug = null
            state.error = null
        },
    },
})

export const {
    setOrganization,
    hydrateOrganizationFromStorage,
    setOrganizationLoading,
    setOrganizationError,
    clearOrganization
} = organizationSlice.actions

export default organizationSlice.reducer