export type Body_login_login_access_token = {
  grant_type?: string | null
  username: string
  password: string
  scope?: string
  client_id?: string | null
  client_secret?: string | null
}

export type HTTPValidationError = {
  detail?: Array<ValidationError>
}

export type ItemCreate = {
  title: string
  description?: string | null
}

export type ItemPublic = {
  title: string
  description?: string | null
  id: number
  owner_id: number
}

export type ItemUpdate = {
  title?: string | null
  description?: string | null
}

export type ItemsPublic = {
  data: Array<ItemPublic>
  count: number
}

export type Message = {
  message: string
}

export type NewPassword = {
  token: string
  new_password: string
}

export type Token = {
  access_token: string
  token_type?: string
}

export type UpdatePassword = {
  current_password: string
  new_password: string
}

export type UserCreate = {
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  password: string
}

export type UserPublic = {
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  id: number
}

export type UserRegister = {
  email: string
  password: string
  full_name?: string | null
}

export type UserUpdate = {
  email?: string | null
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  password?: string | null
}

export type UserUpdateMe = {
  full_name?: string | null
  email?: string | null
}

export type UsersPublic = {
  data: Array<UserPublic>
  count: number
}

export type ValidationError = {
  loc: Array<string | number>
  msg: string
  type: string
}

export type ChurchUnionCreate = {
  name: string
  address: string
  phone_number: string
  email: string
  website: string
  description?: string | null
}

export type ChurchUnionPublic = {
  id: number
  name: string
  address: string
  phone_number: string
  email: string
  website: string
  description?: string | null
}

export type ChurchUnionUpdate = {
  name?: string | null
  address?: string | null
  phone_number?: string | null
  email?: string | null
  website?: string | null
  description?: string | null
}

export type ChurchUnionsPublic = {
  data: Array<ChurchUnionPublic>
  count: number
}

export type ConferenceCreate = {
  name: string
  address: string
  phone_number: string
  email: string
  website: string
  description?: string | null
  church_union_id: number
}

export type ConferencePublic = {
  id: number
  name: string
  address: string
  phone_number: string
  email: string
  website: string
  description?: string | null
  church_union_id: number
}

export type ConferenceUpdate = {
  name?: string | null
  address?: string | null
  phone_number?: string | null
  email?: string | null
  website?: string | null
  description?: string | null
  church_union_id?: number | null
}

export type ConferencesPublic = {
  data: Array<ConferencePublic>
  count: number
}

export type ChurchCreate = {
  name: string
  address: string
  phone_number: string
  email: string
  website: string
  description?: string | null
  conference_id: number
}

export type ChurchPublic = {
  id: number
  name: string
  address: string
  phone_number: string
  email: string
  website: string
  description?: string | null
  conference_id: number
}

export type ChurchUpdate = {
  name?: string | null
  address?: string | null
  phone_number?: string | null
  email?: string | null
  website?: string | null
  description?: string | null
  conference_id?: number | null
}

export type ChurchesPublic = {
  data: Array<ChurchPublic>
  count: number
}