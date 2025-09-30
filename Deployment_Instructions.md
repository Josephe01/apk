# Deployment Instructions

This section describes how to deploy the Inventory Management System to production, staging, or development environments.

---

## Prerequisites

- PHP >= 8.1
- Composer
- Node.js >= 18.x & npm
- MySQL, PostgreSQL, or SQLite
- Redis (for broadcasting & caching)
- Git

---

## Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Josephe01/apk.git
   cd apk
   ```

2. **Install PHP dependencies**

   ```bash
   composer install --optimize-autoloader --no-dev
   ```

3. **Install frontend dependencies**

   ```bash
   npm install --production
   npm run build
   ```

4. **Configure environment**

   - Copy `.env.example` to `.env`
   - Set database, cache, queue, mail, and third-party integration variables
   - Generate Laravel app key:
     ```bash
     php artisan key:generate
     ```

5. **Database migration & seed**

   ```bash
   php artisan migrate --force
   php artisan db:seed --force
   ```

6. **Storage linking**

   ```bash
   php artisan storage:link
   ```

7. **Cache, config, and route optimization**

   ```bash
   php artisan config:cache
   php artisan route:cache
   php artisan view:cache
   ```

8. **Run queues and broadcasting**

   - Start supervisor or a process manager for `php artisan queue:work`
   - If using broadcasting: configure and run Redis or Pusher

---

## Production Server Setup

- Recommended: Use Nginx or Apache, PHP-FPM
- Serve application from `/public`
- Set correct permissions:
  ```bash
  chown -R www-data:www-data storage bootstrap/cache
  chmod -R 775 storage bootstrap/cache
  ```

---

## SSL & Security

- Always use HTTPS (TLS/SSL certs)
- Set strong database and application passwords
- Store API keys and secrets only in `.env`
- Disable debug mode in `.env` for production

---

## Backups & Rollbacks

- Automate regular database and storage backups
- Document rollback and restore procedures

---

## Monitoring & Logging

- Enable error and activity logging (Laravel logs, Sentry, etc.)
- Set up uptime monitoring (Pingdom, UptimeRobot, etc.)

---

## Updating

- Pull latest changes:
  ```bash
  git pull origin main
  composer install --optimize-autoloader --no-dev
  npm install --production
  npm run build
  php artisan migrate --force
  ```

---

*Update these instructions as your deployment process evolves!*