export interface LoginCredentials {
  email: string
  password: string
  company_slug?: string | null
}

export interface LoginResponse {
  message: string
  role: string
}
export interface LoginCredentials {
    email: string;
    password: string;
}