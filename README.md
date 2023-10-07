
![VoidCMS - easy e-commerce template](https://github.com/VoidCMS/VoidCMS/blob/master/frontend/public/logo.png?raw=true)

# # VoidCms Public Beta v0.9.3.1 (work in progesss)

**VoidCms / e-commerce** - Simple django/nuxt e-commerce, easy extendable content management system supports PSQL, SQLite

## Features:
> 
>  1. **Products (with complectations):** This feature remains at the top, as it's crucial for displaying and managing the products you want
> to    sell.
>    
>    2.  **Search:** A robust search feature is essential for helping users quickly find products, which can significantly impact sales and 
> user experience.
>    
>    3.  **Cart:** The shopping cart is vital for users to add and manage items before making a purchase.
>    
>    4.  **Orders:** Effective order management is essential for processing and fulfilling customer orders promptly and accurately.
>    
>    5.  **Clients (and roles):** User management is important for creating accounts, managing user data, and ensuring a personalized   
> shopping experience. Roles can help with security and access control.
>    
>    6.  **Backup/Restore:** Data management and backup are crucial to ensure that customer and order data is secure and can be recovered in 
> case of any issues.
>    
>    7.  **Categories:** Organizing products into categories helps users navigate your product catalog efficiently, making it easier for them  
> to find what they're looking for.
>    
>    8.  **Pages:** Content management and the ability to create informational pages can provide additional information to potential   
> buyers and build trust.
>    
>    9.  **Dynamic styling:** While not directly related to selling products, dynamic styling can enhance your web app's overall   
> aesthetics and branding.
>    
>    10.  **Server-Side Rendering:** This is important for delivering fast and SEO-friendly web pages, which can improve search engine
> rankings    and user experience.
>    
>    11.  **SEO Friendly:** Ensuring your web app is SEO-friendly is crucial for attracting organic traffic from search engines.
>    
>    12.  **Responsive Templates:** Responsiveness is vital for providing a seamless user experience across different devices, which
> is    increasingly important in today's mobile-driven world.
>    
>    13.  **hCaptcha Secured:** Security features like hCaptcha can help protect your web app from bots and enhance user security.
>    
>    14.  **Social Networks:** Integration with social media can assist in marketing and driving traffic to your web app, but it's generally a
> supporting feature.
>    
>    15.  **Multi-Domain Support (work in progress):** If you plan to expand to multiple domains, it's important but can be a lower   
> priority until you're ready to implement it.
>
> 

## Warning

Django in dev mode, work still in progress,and this is the first public release from my private repository v0.8.1 > v0.9.3.1

  

## Deploy with Docker-compose

#### First registered user will be Administrator, then you could add admins via Clients management
#### You can generate Fake data using **python manage.py gen-dummy**

### Locally:

**Simply add** voidcms.local and api.voidcms.local - 127.0.0.0 into hosts file, then

```bash
docker-compose -f docker-compose-local.yml build --no-cache && docker-compose up
```

### Production:
**Generate** your own configurations(***and don't forget to switch django to production mode***) for docker-compose.yml using example
```bash
docker-compose -f docker-compose.yml build --no-cache && docker-compose up
```

## TO DO

- **Full multi-domain support**
- **Group Products Upload / Download**
-  **Help CHATS**
-  **Event-Driven Order status notifications**
- **Redis**
- **RabbitMQ**

### **Other:**

 - **TELEGRAM Bot**
 - **Flutter MobileApp**
