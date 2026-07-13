/**
 * ScriptFlow - Main JavaScript
 * Premium teleprompter application
 * 
 * Modular architecture with dedicated modules for:
 * - Utils: Utility functions
 * - Storage: LocalStorage management
 * - Animations: GSAP-powered animations
 * - Main: Core application initialization
 */

(function() {
    'use strict';
    
    // Wait for DOM
    document.addEventListener('DOMContentLoaded', init);
    
    function init() {
        // Initialize in order
        initAnimations();
        initNavigation();
        initInteractions();
        initAccessibility();
        initPWA();
        initTheme();
        initCommandPalette();
    }
    
    // GSAP Animations
    function initAnimations() {
        if (typeof gsap === 'undefined') return;
        
        gsap.registerPlugin(ScrollTrigger);
        
        // Animate elements on scroll
        const animatedElements = document.querySelectorAll('[data-animate]');
        animatedElements.forEach(el => {
            const direction = el.dataset.animateDirection || 'up';
            const delay = parseFloat(el.dataset.animateDelay) || 0;
            
            gsap.from(el, {
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                    toggleActions: 'play none none none'
                },
                y: direction === 'up' ? 40 : 0,
                x: direction === 'left' ? -40 : 0,
                opacity: 0,
                duration: 0.6,
                delay: delay,
                ease: 'power2.out'
            });
        });
        
        // Stagger animations for lists
        const staggerContainers = document.querySelectorAll('[data-stagger]');
        staggerContainers.forEach(container => {
            const children = container.children;
            const staggerDelay = parseFloat(container.dataset.stagger) || 0.1;
            
            gsap.from(children, {
                scrollTrigger: {
                    trigger: container,
                    start: 'top 85%'
                },
                y: 20,
                opacity: 0,
                duration: 0.4,
                stagger: staggerDelay,
                ease: 'power2.out'
            });
        });
    }
    
    // Navigation
    function initNavigation() {
        // Mobile menu
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuBtn && mobileMenu) {
            mobileMenuBtn.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
                mobileMenu.classList.toggle('animate-slide-down');
            });
        }
        
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
        
        // Navbar scroll effect
        const navbar = document.getElementById('navbar');
        if (navbar) {
            let lastScroll = 0;
            
            window.addEventListener('scroll', () => {
                const currentScroll = window.pageYOffset;
                
                if (currentScroll > 50) {
                    navbar.classList.add('glass');
                } else {
                    navbar.classList.remove('glass');
                }
                
                lastScroll = currentScroll;
            }, { passive: true });
        }
    }
    
    // Micro Interactions
    function initInteractions() {
        // Button hover effects
        document.querySelectorAll('.btn-primary, .btn-secondary, button[type="submit"]').forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                gsap.to(this, { scale: 1.02, duration: 0.15 });
            });
            
            btn.addEventListener('mouseleave', function() {
                gsap.to(this, { scale: 1, duration: 0.15 });
            });
            
            btn.addEventListener('mousedown', function() {
                gsap.to(this, { scale: 0.98, duration: 0.1 });
            });
            
            btn.addEventListener('mouseup', function() {
                gsap.to(this, { scale: 1.02, duration: 0.1 });
            });
        });
        
        // Card hover effects
        document.querySelectorAll('.card, [class*="card"]').forEach(card => {
            if (card.closest('button') || card.tagName === 'BUTTON') return;
            
            card.addEventListener('mouseenter', function() {
                gsap.to(this, { y: -4, duration: 0.2 });
            });
            
            card.addEventListener('mouseleave', function() {
                gsap.to(this, { y: 0, duration: 0.2 });
            });
        });
        
        // Input focus animations
        document.querySelectorAll('input, textarea, select').forEach(input => {
            input.addEventListener('focus', function() {
                gsap.to(this, { scale: 1.01, duration: 0.15 });
            });
            
            input.addEventListener('blur', function() {
                gsap.to(this, { scale: 1, duration: 0.15 });
            });
        });
        
        // Toggle switches
        document.querySelectorAll('[data-toggle]').forEach(toggle => {
            toggle.addEventListener('click', function() {
                const isActive = this.classList.toggle('active');
                const target = document.querySelector(this.dataset.toggle);
                
                if (target) {
                    gsap.to(target, {
                        height: isActive ? 'auto' : 0,
                        opacity: isActive ? 1 : 0,
                        duration: 0.3
                    });
                }
            });
        });
    }
    
    // Accessibility
    function initAccessibility() {
        // Respect reduced motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        if (prefersReducedMotion.matches) {
            gsap.globalTimeline.timeScale(0);
            document.body.classList.add('reduced-motion');
        }
        
        prefersReducedMotion.addEventListener('change', (e) => {
            gsap.globalTimeline.timeScale(e.matches ? 0 : 1);
            document.body.classList.toggle('reduced-motion', e.matches);
        });
        
        // Focus visible styles
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-nav');
            }
        });
        
        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-nav');
        });
        
        // Skip link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Skip to main content';
        document.body.prepend(skipLink);
    }
    
    // PWA Support
    function initPWA() {
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(registration => {
                        console.log('ServiceWorker registered:', registration.scope);
                    })
                    .catch(error => {
                        console.log('ServiceWorker registration failed:', error);
                    });
            });
        }
        
        // Install prompt
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            // Show install button
            const installBtn = document.getElementById('install-btn');
            if (installBtn) {
                installBtn.classList.remove('hidden');
                installBtn.addEventListener('click', () => {
                    deferredPrompt.prompt();
                    deferredPrompt.userChoice.then((choiceResult) => {
                        if (choiceResult.outcome === 'accepted') {
                            console.log('User accepted the install prompt');
                        }
                        deferredPrompt = null;
                    });
                });
            }
        });
        
        // App installed
        window.addEventListener('appinstalled', () => {
            deferredPrompt = null;
            showToast('App installed successfully!', 'success');
        });
    }
    
    // Utility: Format numbers
    window.formatNumber = function(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    };
    
    // Utility: Debounce
    window.debounce = function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };
    
    // Utility: Throttle
    window.throttle = function(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    };
    
    // Toast notification helper (also used in templates)
    window.showToast = function(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        const colors = {
            success: 'bg-green-500/20 border-green-500/50 text-green-400',
            error: 'bg-red-500/20 border-red-500/50 text-red-400',
            info: 'bg-accent/20 border-accent/50 text-accent',
            warning: 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400'
        };
        
        const icons = {
            success: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>',
            error: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>',
            info: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>',
            warning: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>'
        };
        
        toast.className = `flex items-center space-x-3 px-4 py-3 rounded-xl border ${colors[type]} backdrop-blur-sm shadow-lg max-w-sm`;
        toast.innerHTML = `
            <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                ${icons[type]}
            </svg>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);
        
        gsap.from(toast, { x: 100, opacity: 0, duration: 0.3, ease: 'power2.out' });
        
        setTimeout(() => {
            gsap.to(toast, { 
                x: 100, 
                opacity: 0, 
                duration: 0.3, 
                onComplete: () => toast.remove() 
            });
        }, 4000);
    };
    
    // API helper
    window.api = {
        get: async (url) => {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            return response.json();
        },
        
        post: async (url, data) => {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return response.json();
        },
        
        put: async (url, data) => {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return response.json();
        },
        
        delete: async (url) => {
            const response = await fetch(url, {
                method: 'DELETE'
            });
            return response.json();
        }
    };
    
    // Theme initialization
    function initTheme() {
        const savedTheme = localStorage.getItem('sf_theme') || 'dark';
        applyTheme(savedTheme);
        
        // Theme buttons
        document.querySelectorAll('[data-theme]').forEach(btn => {
            if (btn.dataset.theme === savedTheme) {
                btn.classList.add('ring-2', 'ring-accent');
            }
            
            btn.addEventListener('click', () => {
                const theme = btn.dataset.theme;
                applyTheme(theme);
                localStorage.setItem('sf_theme', theme);
            });
        });
    }
    
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('sf_theme', theme);
        
        // Update theme buttons
        document.querySelectorAll('[data-theme]').forEach(btn => {
            btn.classList.toggle('ring-2', btn.dataset.theme === theme);
            btn.classList.toggle('ring-accent', btn.dataset.theme === theme);
        });
    }
    
    window.setTheme = applyTheme;
    
    // Command palette (Ctrl/Cmd + K)
    function initCommandPalette() {
        const palette = document.getElementById('command-palette');
        if (!palette) return;
        
        const searchInput = palette.querySelector('input');
        
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                toggleCommandPalette();
            }
            
            if (e.key === 'Escape') {
                closeCommandPalette();
            }
        });
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                filterCommands(e.target.value.toLowerCase());
            });
        }
        
        // Close on backdrop click
        palette.addEventListener('click', (e) => {
            if (e.target === palette) {
                closeCommandPalette();
            }
        });
    }
    
    function toggleCommandPalette() {
        const palette = document.getElementById('command-palette');
        if (!palette) return;
        
        const isHidden = palette.classList.contains('hidden');
        
        if (isHidden) {
            palette.classList.remove('hidden');
            palette.querySelector('input')?.focus();
        } else {
            closeCommandPalette();
        }
    }
    
    function closeCommandPalette() {
        const palette = document.getElementById('command-palette');
        if (!palette) return;
        
        palette.classList.add('hidden');
        const input = palette.querySelector('input');
        if (input) {
            input.value = '';
            filterCommands('');
        }
    }
    
    function filterCommands(query) {
        const commands = document.querySelectorAll('#command-palette [data-command]');
        
        commands.forEach(cmd => {
            const text = cmd.textContent.toLowerCase();
            const matches = text.includes(query);
            cmd.style.display = matches ? 'flex' : 'none';
        });
    }
    
    window.toggleCommandPalette = toggleCommandPalette;
    
})();
