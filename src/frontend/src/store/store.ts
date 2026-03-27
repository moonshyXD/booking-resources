import { configureStore } from '@reduxjs/toolkit'
import organizationReducer from './organizationSlice'
import authReducer from './authSlice'

export const store = configureStore({
    reducer: {
        organization: organizationReducer,
        auth: authReducer,
    }
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch