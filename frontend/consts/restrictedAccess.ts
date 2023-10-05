const roles = {
  admin: 'admin',
  user: 'user'
}

type RestrictedAccess = {
  [key: string]: {
    roles: string[]
  }
}

export const restrictedAccess: RestrictedAccess = {
  profile: {
    roles: [roles.admin, roles.user]
  },
  management: {
    roles: [roles.admin]
  },
  orders: {
    roles: [roles.user, roles.admin]
  }
}
