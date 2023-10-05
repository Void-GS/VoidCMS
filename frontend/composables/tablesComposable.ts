import { NButton, NDropdown, NImage, NTag } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import type { PageInterface } from '~/interfaces/page'
import type { SettingsInterface } from '~/interfaces/settings'
import type { SocialInterface } from '~/interfaces/social'
import type { ClientInterface } from '~/interfaces/client'
// import type { CategoryInterface } from '~/interfaces/category'
import type { ProductInterface } from '~/interfaces/product'
import type { OrderInterface } from '~/interfaces/order'

export const clientsColumns = (): DataTableColumns<ClientInterface> => {
  return [
    {
      title: 'Имя Клиента',
      key: 'client-name',
      render(row) {
        return h(
          'span',
          row.last_name || row.name
            ? `${row.name} ${row.last_name}`
            : 'Не указано'
        )
      }
    },
    {
      title: 'Email',
      key: 'email'
    },
    {
      title: 'Телефон',
      key: 'phone',
      render(row) {
        return h('span', ['+7', row.phone])
      }
    },
    {
      title: 'Роль',
      key: 'role',
      render(row) {
        return h(
          'strong',
          row.role === 'admin' ? 'Администратор' : 'Пользователь'
        )
      }
    },
    {
      title: 'Действия',
      key: 'actions',
      width: 250,
      render(row) {
        return [
          h(
            NDropdown,
            {
              trigger: 'click',
              options: [
                {
                  label: 'Администратор',
                  key: 'admin',
                  disabled: false
                },
                {
                  label: 'Пользователь',
                  key: 'user',
                  disabled: false
                }
              ],
              onSelect: (key: string) => {
                changeRole(row, key)
              }
            },
            {
              default: () =>
                h(
                  NButton,
                  {
                    strong: true,
                    tertiary: true,
                    size: 'small'
                  },
                  { default: () => 'Изменить роль' }
                )
            }
          ),
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'red',
              size: 'small',
              style: 'margin-left: 0.4rem;',
              onClick: () => deleteClient(row)
            },
            { default: () => 'Удалить' }
          )
        ]
      }
    }
  ]
}

export const productsColumns = (): DataTableColumns<ProductInterface> => {
  return [
    {
      title: 'Обложка',
      key: 'image',
      width: 120,
      render(row) {
        return [
          h(
            NImage,
            {
              src: handleImageOrEmpty(row),
              width: 120,
              lazy: true,
              objectFit: 'cover',
              style: 'height: 100%; width: 100%; max-height: 60px'
            },
            { default: () => 'Обложка' }
          )
        ]
      }
    },
    {
      title: 'Название',
      key: 'title'
    },
    {
      title: 'Категория',
      key: 'category',
      render(row) {
        const node = row.category
          ? String(storeCategories().categoryByIdGetter(row.category)?.title)
          : 'Нет Категории'
        return h(
          NTag,
          {
            type: 'primary',
            onclick: () => {
              if (row.category) {
                $router().push(`/management/categories/edit/${row.category}`)
              }
            },
            style: 'cursor: pointer;'
          },
          { default: () => node }
        )
      }
    },
    {
      title: 'Цена',
      key: 'price',
      width: 100,
      ellipsis: true
    },
    {
      title: 'Действия',
      key: 'actions',
      width: 230,
      render(row) {
        return [
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'black',
              size: 'small',
              onClick: () => editProduct(row)
            },
            { default: () => 'Редактировать' }
          ),
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'red',
              size: 'small',
              style: 'margin-left: 0.4rem;',
              onClick: () => deleteProduct(row)
            },
            { default: () => 'Удалить' }
          )
        ]
      }
    }
  ]
}

export const pagesColumns = (): DataTableColumns<PageInterface> => {
  return [
    {
      title: 'Название',
      key: 'name'
    },
    {
      title: 'Действия',
      key: 'actions',
      width: 230,
      render(row) {
        return [
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'black',
              size: 'small',
              onClick: () => editPage(row)
            },
            { default: () => 'Редактировать' }
          ),
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'red',
              size: 'small',
              style: 'margin-left: 0.4rem;',
              onClick: () => deletePage(row)
            },
            { default: () => 'Удалить' }
          )
        ]
      }
    }
  ]
}

export const settingsColumns = (): DataTableColumns<SettingsInterface> => {
  return [
    {
      title: 'Домен',
      key: 'app_url',
      render(row) {
        return h('span', [
          row.app_url,
          h('strong', window.location.host === row.app_url ? ' (текущий)' : '')
        ])
      }
    },
    {
      title: 'Название',
      key: 'app_name'
    },
    {
      title: 'Действия',
      key: 'actions',
      width: 230,
      render(row) {
        return [
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'black',
              size: 'small',
              onClick: () => editSettings(row)
            },
            { default: () => 'Редактировать' }
          ),
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'red',
              size: 'small',
              style: 'margin-left: 0.4rem;',
              onClick: () => deleteSettings(row)
            },
            { default: () => 'Удалить' }
          )
        ]
      }
    }
  ]
}

export const socialsColumns = (): DataTableColumns<SocialInterface> => {
  return [
    {
      title: 'Ссылка на соц. сеть',
      key: 'url'
    },
    {
      title: 'Тип',
      key: 'type'
    },
    {
      title: 'Действия',
      key: 'actions',
      width: 230,
      render(row) {
        return [
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'black',
              size: 'small',
              onClick: () => editSocial(row)
            },
            { default: () => 'Редактировать' }
          ),
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'red',
              size: 'small',
              style: 'margin-left: 0.4rem;',
              onClick: () => deleteSocial(row)
            },
            { default: () => 'Удалить' }
          )
        ]
      }
    }
  ]
}

export const ordersColumns = (): DataTableColumns<OrderInterface> => {
  return [
    {
      title: 'Номер заказа',
      key: 'id',
      render(row) {
        return h('strong', `Заказ №${row.id}`)
      }
    },
    {
      title: 'ФИО получателя',
      key: 'order_name',
      render(row) {
        return h('strong', `${row.order_name}`)
      }
    },
    {
      title: 'Телефон',
      key: 'order_phone',
      render(row) {
        return h('strong', `+7 ${row.order_phone}`)
      }
    },
    {
      title: 'Адрес доставки',
      key: 'order_address',
      render(row) {
        return h('span', `${row.order_address}`)
      }
    },
    {
      title: 'Общая стоимость',
      key: 'total_price',
      render(row) {
        return h('span', `${row.total_price}₽`)
      }
    },
    {
      title: 'Статус',
      key: 'status',
      render(row) {
        const status = tagGenerator(row)
        return h(
          NTag,
          {
            type: status.type,
            style: 'cursor: pointer;'
          },
          { default: () => `${status.name}` }
        )
      }
    },
    {
      title: 'Дата оформления',
      key: 'created_at',
      render(row) {
        return h('span', `${convertDate(String(row.created_at!))}`)
      }
    },
    {
      title: 'Действия',
      key: 'actions',
      width: 210,
      render(row) {
        return [
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'black',
              size: 'small',
              onClick: () => editOrder(row)
            },
            { default: () => 'Обработать' }
          ),
          h(
            NButton,
            {
              strong: true,
              tertiary: true,
              color: 'red',
              size: 'small',
              style: 'margin-left: 0.4rem;',
              onClick: () => deleteOrder(row)
            },
            { default: () => 'Удалить' }
          )
        ]
      }
    }
  ]
}

function tagGenerator(row: OrderInterface) {
  const status = {
    name: '',
    type: 'primary' as 'primary' | 'warning' | 'error' | 'success'
  }

  switch (row.status) {
    case 'paperwork':
      status.name = 'Оформление'
      status.type = 'warning'
      break
    case 'payment':
      status.name = 'Ожидает оплату'
      status.type = 'warning'
      break
    case 'processing':
      status.name = 'Обработка магазином'
      status.type = 'warning'
      break
    case 'shipping':
      status.name = 'В доставке'
      status.type = 'warning'
      break
    case 'canceled':
      status.name = 'Отменен'
      status.type = 'error'
      break
    case 'done':
      status.name = 'Завершен'
      status.type = 'success'
      break
    default:
      status.name = 'Неизвестен'
      status.type = 'error'
  }

  return status
}

function editProduct(row: ProductInterface) {
  $router().push(`products/edit/${String(row.id)}`)
}

// function editCategory(row: CategoryInterface) {
//   $router().push(`categories/edit/${String(row.id)}`)
// }

function editPage(row: PageInterface) {
  $router().push(`pages/edit/${String(row.id)}`)
}

function editSettings(row: SettingsInterface) {
  $router().push(`settings/edit/${String(row.id)}`)
}

function editSocial(row: SettingsInterface) {
  $router().push(`socials/edit/${String(row.id)}`)
}

function editOrder(row: SettingsInterface) {
  $router().push(`orders/edit/${String(row.id)}`)
}

async function deleteClient(row: ClientInterface) {
  try {
    await storeClients().deleteClient(row)
    $notification('Клиент удален', 'success')
  } catch (error) {
    $notification('Ошибка удаления', 'error')
  }
}

async function changeRole(client: ClientInterface, key: string) {
  try {
    await storeClients().changeRole(client, key)
    $notification('Роль заменена', 'success')
  } catch (error) {
    $notification('Ошибка изменения роли', 'error')
  }
}

async function deleteProduct(row: ProductInterface) {
  try {
    await storeProducts().deleteProduct(row)
    $notification('Товар: Успешно удален', 'success')
  } catch (error) {
    $notification('Ошибка удаления', 'error')
  }
}

// async function deleteCategory(row: CategoryInterface) {
//   try {
//     await storeCategories().deleteCategory(row)
//     $notification('Категория: Успешно удалена', 'success')
//   } catch (error) {
//     $notification('Ошибка удаления', 'error')
//   }
// }

async function deletePage(row: PageInterface) {
  try {
    await storePages().deletePage(row)
    $notification('Страница: Успешно удалена', 'success')
  } catch (error) {
    $notification('Ошибка удаления', 'error')
  }
}

async function deleteSettings(row: SettingsInterface) {
  try {
    await storeSettings().deleteSettings(row)
    $notification('Настройки домена успешно удалены', 'success')
  } catch (error) {
    $notification('Ошибка удаления', 'error')
  }
}

async function deleteSocial(row: SettingsInterface) {
  try {
    await storeSocials().deleteSocial(row)
    $notification('Соц. сеть успешно удалена', 'success')
  } catch (error) {
    $notification('Ошибка удаления', 'error')
  }
}

async function deleteOrder(row: OrderInterface) {
  try {
    await storeOrders().deleteOrder(row)
    $notification('Заказ успешно удален', 'success')
  } catch (error) {
    $notification('Ошибка удаления', 'error')
  }
}
