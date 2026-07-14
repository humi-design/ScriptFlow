# Upload ScriptFlow to cPanel - Complete Guide

## 1. OBJECTIVE
Provide a comprehensive step-by-step guide to upload and deploy the ScriptFlow web application on a cPanel-hosted server.

## 2. CONTEXT SUMMARY
- **Project:** ScriptFlow (appears to be a web application)
- **Deployment Target:** cPanel hosting environment
- **Required Access:** cPanel credentials, domain configured, file manager or FTP access
- **Common Methods:** File Manager, FTP, SSH (if available)

## 3. APPROACH OVERVIEW
This guide covers the most reliable method using **cPanel File Manager** (no FTP setup required), plus alternative methods for different scenarios.

---

## 4. IMPLEMENTATION STEPS

### Phase 1: Prepare Your Project Files

**Step 1: Gather all project files**
- Locate your complete ScriptFlow project on your local machine
- Ensure all necessary files are included:
  - `routes/` folder
  - `static/` folder (CSS, JS, images, fonts)
  - `tests/` folder (if needed for deployment)
  - Any configuration files (`app.yaml`, `.env`, etc.)
  - Main application entry point

**Step 2: Create a deployment-ready archive (optional but recommended)**
- Zip all project files into a single archive: `scriptflow-deploy.zip`
- This makes upload faster and prevents file-by-file errors

---

### Phase 2: Access cPanel

**Step 3: Log into cPanel**
1. Open your browser and go to: `https://yourdomain.com/cpanel` or `https://yourdomain.com:2083`
2. Enter your cPanel username and password
3. Click **Log In**

**Step 4: Locate File Manager**
- From the cPanel dashboard, find the **Files** section
- Click on **File Manager**

---

### Phase 3: Upload Using File Manager

**Step 5: Navigate to the correct directory**
The destination depends on your project type:
- **For primary domain (yourdomain.com):** Navigate to `public_html/`
- **For subdomain (sub.yourdomain.com):** Navigate to `/public_html/sub/` or the subdomain's root
- **For addon domain:** Navigate to its designated directory

**Step 6: Upload the archive**
1. In File Manager, click **Upload** button (top menu)
2. A new tab/window opens
3. Drag and drop your `scriptflow-deploy.zip` file OR click **Select File** to browse
4. Wait for upload to complete (progress bar shows status)
5. Close the upload tab and return to File Manager

**Step 7: Extract the archive**
1. Locate `scriptflow-deploy.zip` in the directory
2. Right-click on the file → select **Extract**
3. Choose the extraction destination (usually the same directory)
4. Click **Extract File(s)**
5. Verify files appear in the correct location

**Step 8: Verify file structure**
- After extraction, confirm:
  - Entry point files (`index.php`, `index.html`, `app.py`, etc.) are directly in `public_html/`
  - Subfolders (`static/`, `routes/`) are accessible and not nested incorrectly

---

### Phase 4: Alternative Upload Methods

#### Method B: FTP Upload
1. **Get FTP credentials** from cPanel → FTP Accounts
2. **Use an FTP client** (FileZilla, Cyberduck, or similar)
3. **Connect using:**
   - Host: `ftp.yourdomain.com` or your server's IP
   - Username: Your FTP username
   - Password: Your FTP password
   - Port: 21 (or 22 for SFTP)
4. **Navigate** to `public_html/`
5. **Upload** all project files/folders
6. Wait for transfer to complete

#### Method C: SSH Upload (if enabled)
1. **Enable SSH** in cPanel → Terminal (or request from host)
2. **Connect via terminal:**
   ```bash
   ssh username@yourdomain.com
   ```
3. **Navigate to web root:**
   ```bash
   cd public_html
   ```
4. **Use SCP or SFTP to upload:**
   ```bash
   # From your local machine:
   scp -r ./scriptflow-project/* username@yourdomain.com:~/public_html/
   ```

---

### Phase 5: Configure Your Application

**Step 9: Set correct file permissions**
- **Folders:** 755 (drwxr-xr-x)
- **Files:** 644 (-rw-r--r--)
- In File Manager: Right-click file/folder → **Change Permissions**

**Step 10: Configure database (if required)**
- Go to **cPanel → MySQL Databases**
- Create a database, user, and password
- Note the credentials for your app config

**Step 11: Update configuration files**
- Edit your app config (`.env`, `config.php`, `settings.py`, etc.)
- Update database credentials
- Set correct domain URLs
- Update any absolute paths

**Step 12: Set up Python/Node environment (if applicable)**
For Python apps:
1. Go to **cPanel → Setup Python App**
2. Create a Python application
3. Set the application root to your project folder
4. Configure virtual environment if needed
5. Install dependencies via **PyPI** or `requirements.txt`

For Node.js apps:
1. Use **cPanel → Node.js App** (if available)
2. Or use terminal to run npm commands

---

### Phase 6: Domain & SSL Configuration

**Step 13: Configure domain**
- Ensure your domain points to cPanel nameservers
- Check in cPanel → **Domains** → **Zone Editor**
- Allow 24-48 hours for DNS propagation if new

**Step 14: Enable SSL/HTTPS**
1. Go to **cPanel → SSL/TLS**
2. Click **Manage SSL Sites**
3. Install certificate for your domain (Let's Encrypt is free)
4. Or use **AutoSSL** for automatic HTTPS

**Step 15: Force HTTPS redirect (optional)**
Add to `.htaccess` (for Apache):
```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## 5. TESTING AND VALIDATION

### Verify Deployment Success

1. **Clear browser cache** and cookies
2. **Visit your domain:** `https://yourdomain.com`
3. **Check for:**
   - ✅ Page loads without 500/403 errors
   - ✅ Static assets (CSS, JS, images) load correctly
   - ✅ Database connections work (if applicable)
   - ✅ Forms and interactive elements function
   - ✅ HTTPS is working (green lock icon in browser)

### Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| 403 Forbidden | Check file permissions (755 folders, 644 files) |
| 500 Internal Server Error | Check `.htaccess` syntax, PHP version compatibility |
| Database connection failed | Verify database credentials in config |
| CSS/JS not loading | Check file paths, clear cache |
| SSL warning | Reinstall certificate or use AutoSSL |

### Post-Deployment Checklist
- [ ] Files uploaded to correct directory
- [ ] Permissions set correctly
- [ ] Database configured (if applicable)
- [ ] Environment variables set
- [ ] SSL certificate active
- [ ] Site accessible via HTTPS
- [ ] Test critical user flows
- [ ] Monitor error logs in cPanel

---

## Quick Reference: cPanel File Manager Upload Flow

```
1. Log into cPanel
2. Open File Manager
3. Navigate to public_html/
4. Upload ZIP file
5. Extract ZIP
6. Verify file structure
7. Set permissions (755 folders, 644 files)
8. Configure database if needed
9. Update app configuration
10. Test your site!
```

---

**Questions that would help customize this guide:**
1. What type of application is ScriptFlow? (PHP, Python/Flask, Node.js, static HTML?)
2. Do you need a database? (MySQL, PostgreSQL, MongoDB?)
3. Do you have cPanel access credentials ready?
4. Is this a new domain/subdomain, or updating existing deployment?
