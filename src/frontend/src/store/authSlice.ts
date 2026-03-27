import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'
import { fetchCurrentUser } from '../api/loginApi'
import type { CurrentUser } from '../types/user'

interface AuthState {
  currentUser: CurrentUser | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  lastEmail: string
}

const getInitialState = (): AuthState => {
  if (typeof window === 'undefined') {
    return {
      currentUser: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
      lastEmail: '',
    }
  }

  const lastEmail = localStorage.getItem('lastEmail') ?? ''
  const persistedRole = localStorage.getItem('role')

  return {
    currentUser: persistedRole
      ? {
          email: lastEmail,
          role: persistedRole,
        }
      : null,
    isAuthenticated: Boolean(persistedRole),
    isLoading: false,
    error: null,
    lastEmail,
  }
}

const initialState: AuthState = getInitialState()

export const fetchMe = createAsyncThunk<CurrentUser>('auth/fetchMe', async (_, thunkApi) => {
  try {
    return await fetchCurrentUser()
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Не удалось получить данные пользователя'
    return thunkApi.rejectWithValue(message)
  }
})

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setAuthLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload
    },
    setAuthError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
    setCurrentUser: (state, action: PayloadAction<CurrentUser>) => {
      state.currentUser = action.payload
      state.isAuthenticated = true
      state.error = null
    },
    clearCurrentUser: (state) => {
      state.currentUser = null
      state.isAuthenticated = false
      state.error = null
    },
    setLastEmail: (state, action: PayloadAction<string>) => {
      state.lastEmail = action.payload
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchMe.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchMe.fulfilled, (state, action) => {
        state.isLoading = false
        state.currentUser = action.payload
        state.isAuthenticated = true
      })
      .addCase(fetchMe.rejected, (state, action) => {
        state.isLoading = false
        state.currentUser = null
        state.isAuthenticated = false
        state.error = typeof action.payload === 'string' ? action.payload : 'Пользователь не авторизован'
      })
  },
})

export const { setAuthLoading, setAuthError, setCurrentUser, clearCurrentUser, setLastEmail } =
  authSlice.actions

export default authSlice.reducer
