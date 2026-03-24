import { createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'
import type { Organization } from '../types/organization'

interface OrganizationState {
    selectedOrg: Organization | null
}

const initialState: OrganizationState = {
    selectedOrg: null,
}

const organizationSlice = createSlice({
    name: 'organization',
    initialState,
    reducers: {
        setOrganization: (state, action: PayloadAction<Organization>) => {
            state.selectedOrg = action.payload
        },
        clearOrganization: (state) => {
            state.selectedOrg = null
        },
    },
})

export const { setOrganization, clearOrganization } = organizationSlice.actions

export default organizationSlice.reducer