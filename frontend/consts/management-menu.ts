import type { MenuOption } from 'naive-ui'
import {
  // BarChartOutline,
  CloudDoneOutline,
  ConstructOutline,
  CubeOutline,
  DocumentTextOutline,
  LibraryOutline,
  PeopleOutline,
  SettingsOutline,
  ShareSocialOutline,
  WalletOutline
} from '@vicons/ionicons5'

export const managementMenuOptions: MenuOption[] = [
  // {
  //   label: () => genLinkLabel('Панель управления', '/management'),
  //   key: '/management',
  //   icon: renderIcon(BarChartOutline)
  // },
  // {
  //   key: 'divider-1',
  //   type: 'divider',
  //   props: {}
  // },
  {
    label: 'Параметры',
    icon: renderIcon(SettingsOutline),
    key: '1',
    children: [
      {
        label: () => genLinkLabel('Клиенты', '/management/clients'),
        key: '/management/clients',
        icon: renderIcon(PeopleOutline)
      },
      {
        label: () => genLinkLabel('Настройки доменов', '/management/settings'),
        key: '/management/settings',
        icon: renderIcon(ConstructOutline)
      },
      {
        label: () => genLinkLabel('Социальные сети', '/management/socials'),
        key: '/management/socials',
        icon: renderIcon(ShareSocialOutline)
      },
      {
        label: () =>
          genLinkLabel('Резервное копирование', '/management/backup'),
        key: '/management/backup',
        icon: renderIcon(CloudDoneOutline)
      }
    ]
  },
  {
    label: () => genLinkLabel('Заказы', '/management/orders'),
    key: '/management/orders',
    icon: renderIcon(WalletOutline)
  },
  {
    label: () => genLinkLabel('Страницы', '/management/pages'),
    key: '/management/pages',
    icon: renderIcon(DocumentTextOutline)
  },
  {
    label: () => genLinkLabel('Категории', '/management/categories'),
    key: '/management/categories',
    icon: renderIcon(LibraryOutline)
  },
  {
    label: () => genLinkLabel('Товары', '/management/products'),
    key: '/management/products',
    icon: renderIcon(CubeOutline)
  }
]
