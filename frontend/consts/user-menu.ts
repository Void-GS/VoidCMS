import {
  LogOutOutline,
  PersonCircleOutline,
  WalletOutline
} from '@vicons/ionicons5'

export const clientMenuOptions = [
  {
    label: () => genLinkLabel('Профиль', '/profile'),
    key: 'profile',
    icon: renderIcon(PersonCircleOutline)
  },
  {
    label: () => genLinkLabel('Оформленные заказы', '/orders'),
    key: 'orders',
    icon: renderIcon(WalletOutline)
  },
  {
    label: 'Выход',
    key: 'logout',
    icon: renderIcon(LogOutOutline)
  }
]
