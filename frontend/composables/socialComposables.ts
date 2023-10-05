import {
  LinkOutline,
  LogoInstagram,
  LogoVk,
  LogoWhatsapp,
  MailOutline,
  PaperPlaneOutline
} from '@vicons/ionicons5'

export function socialTypeToIcon(type?: string) {
  switch (type) {
    case 'instagram':
      return LogoInstagram
    case 'whatsapp':
      return LogoWhatsapp
    case 'email':
      return MailOutline
    case 'vk':
      return LogoVk
    case 'telegram':
      return PaperPlaneOutline
    default:
      return LinkOutline
  }
}
