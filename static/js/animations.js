/**
 * ScriptFlow - Animations Module
 * Premium GSAP-powered animations and micro-interactions
 */

const Animations = {
    /**
     * Animation settings
     */
    settings: {
        duration: {
            fast: 0.15,
            normal: 0.25,
            slow: 0.4,
            page: 0.6
        },
        ease: 'power3.out',
        springEase: 'elastic.out(1, 0.5)'
    },

    /**
     * Initialize GSAP animations
     */
    init() {
        if (typeof gsap === 'undefined') {
            console.warn('GSAP not loaded');
            return;
        }

        // Set default GSAP settings
        gsap.defaults({
            ease: this.settings.ease,
            duration: this.settings.duration.normal
        });

        // Initialize page transition
        this.initPageTransitions();
        
        // Initialize button animations
        this.initButtons();
        
        // Initialize card animations
        this.initCards();
        
        // Initialize input animations
        this.initInputs();
        
        // Initialize scroll animations
        this.initScrollAnimations();
        
        // Initialize skeleton loaders
        this.initSkeletonLoaders();
    },

    /**
     * Page transitions
     */
    initPageTransitions() {
        // Fade in new pages
        const pageContent = document.querySelector('main, #app, .page-content');
        if (pageContent) {
            gsap.from(pageContent, {
                opacity: 0,
                y: 20,
                duration: this.settings.duration.page,
                ease: 'power2.out'
            });
        }
    },

    /**
     * Animate element into view
     */
    fadeIn(element, options = {}) {
        const defaults = {
            opacity: 0,
            y: 20,
            duration: this.settings.duration.normal,
            delay: 0,
            stagger: 0
        };
        return gsap.from(element, { ...defaults, ...options });
    },

    /**
     * Button micro-interactions
     */
    initButtons() {
        document.querySelectorAll('button, .btn, a.btn').forEach(btn => {
            // Skip if already initialized
            if (btn.dataset.animated) return;
            btn.dataset.animated = 'true';

            // Hover effect
            btn.addEventListener('mouseenter', () => {
                if (Utils.prefersReducedMotion()) return;
                gsap.to(btn, {
                    y: -2,
                    boxShadow: '0 8px 25px -5px rgba(102, 126, 234, 0.25)',
                    duration: this.settings.duration.fast
                });
            });

            // Mouse leave
            btn.addEventListener('mouseleave', () => {
                if (Utils.prefersReducedMotion()) return;
                gsap.to(btn, {
                    y: 0,
                    boxShadow: '0 4px 15px -3px rgba(0, 0, 0, 0.1)',
                    duration: this.settings.duration.fast
                });
            });

            // Click effect
            btn.addEventListener('mousedown', () => {
                if (Utils.prefersReducedMotion()) return;
                gsap.to(btn, {
                    scale: 0.98,
                    duration: this.settings.duration.fast
                });
            });

            // Release effect
            btn.addEventListener('mouseup', () => {
                if (Utils.prefersReducedMotion()) return;
                gsap.to(btn, {
                    scale: 1,
                    duration: this.settings.duration.fast,
                    ease: this.settings.springEase
                });
            });
        });
    },

    /**
     * Card hover animations
     */
    initCards() {
        document.querySelectorAll('.card, .script-card, .feature-card').forEach(card => {
            if (card.dataset.animated) return;
            card.dataset.animated = 'true';

            card.addEventListener('mouseenter', () => {
                if (Utils.prefersReducedMotion()) return;
                gsap.to(card, {
                    y: -4,
                    boxShadow: '0 20px 40px -10px rgba(0, 0, 0, 0.3)',
                    borderColor: 'rgba(102, 126, 234, 0.3)',
                    duration: this.settings.duration.normal
                });
            });

            card.addEventListener('mouseleave', () => {
                if (Utils.prefersReducedMotion()) return;
                gsap.to(card, {
                    y: 0,
                    boxShadow: '0 4px 15px -3px rgba(0, 0, 0, 0.1)',
                    borderColor: 'rgba(43, 43, 43, 1)',
                    duration: this.settings.duration.normal
                });
            });
        });
    },

    /**
     * Input focus animations
     */
    initInputs() {
        document.querySelectorAll('input, textarea, select').forEach(input => {
            if (input.dataset.animated) return;
            input.dataset.animated = 'true';

            const parent = input.closest('.input-group') || input.parentElement;
            if (!parent) return;

            input.addEventListener('focus', () => {
                if (Utils.prefersReducedMotion()) return;
                gsap.to(parent, {
                    scale: 1.01,
                    duration: this.settings.duration.fast
                });
            });

            input.addEventListener('blur', () => {
                if (Utils.prefersReducedMotion()) return;
                gsap.to(parent, {
                    scale: 1,
                    duration: this.settings.duration.fast
                });
            });
        });
    },

    /**
     * Scroll-triggered animations
     */
    initScrollAnimations() {
        if (typeof ScrollTrigger === 'undefined') return;

        // Staggered fade in for lists
        gsap.utils.toArray('.stagger-fade').forEach(container => {
            const items = container.children;
            gsap.from(items, {
                opacity: 0,
                y: 30,
                stagger: 0.1,
                duration: this.settings.duration.slow,
                scrollTrigger: {
                    trigger: container,
                    start: 'top 80%',
                    toggleActions: 'play none none none'
                }
            });
        });

        // Slide in from left
        gsap.utils.toArray('.slide-left').forEach(element => {
            gsap.from(element, {
                x: -50,
                opacity: 0,
                duration: this.settings.duration.slow,
                scrollTrigger: {
                    trigger: element,
                    start: 'top 80%'
                }
            });
        });

        // Slide in from right
        gsap.utils.toArray('.slide-right').forEach(element => {
            gsap.from(element, {
                x: 50,
                opacity: 0,
                duration: this.settings.duration.slow,
                scrollTrigger: {
                    trigger: element,
                    start: 'top 80%'
                }
            });
        });

        // Scale up
        gsap.utils.toArray('.scale-up').forEach(element => {
            gsap.from(element, {
                scale: 0.8,
                opacity: 0,
                duration: this.settings.duration.slow,
                scrollTrigger: {
                    trigger: element,
                    start: 'top 80%'
                }
            });
        });
    },

    /**
     * Skeleton loaders animation
     */
    initSkeletonLoaders() {
        gsap.utils.toArray('.skeleton').forEach(skeleton => {
            gsap.to(skeleton, {
                opacity: 0.5,
                duration: 1,
                repeat: -1,
                yoyo: true,
                ease: 'power1.inOut'
            });
        });
    },

    /**
     * Toast notification animation
     */
    showToast(toastElement) {
        gsap.fromTo(toastElement, 
            { x: 100, opacity: 0 },
            { 
                x: 0, 
                opacity: 1, 
                duration: this.settings.duration.normal,
                onComplete: () => {
                    // Auto dismiss after delay
                    setTimeout(() => this.hideToast(toastElement), 3000);
                }
            }
        );
    },

    /**
     * Hide toast animation
     */
    hideToast(toastElement) {
        gsap.to(toastElement, {
            x: 100,
            opacity: 0,
            duration: this.settings.duration.fast,
            onComplete: () => {
                if (toastElement.parentNode) {
                    toastElement.parentNode.removeChild(toastElement);
                }
            }
        });
    },

    /**
     * Modal/Dialog animation
     */
    showModal(modalElement) {
        const backdrop = modalElement.querySelector('.modal-backdrop') || modalElement;
        const content = modalElement.querySelector('.modal-content') || modalElement;

        gsap.fromTo(backdrop,
            { opacity: 0 },
            { opacity: 1, duration: this.settings.duration.fast }
        );

        gsap.fromTo(content,
            { scale: 0.95, opacity: 0 },
            { 
                scale: 1, 
                opacity: 1, 
                duration: this.settings.duration.normal,
                ease: this.settings.springEase
            }
        );
    },

    /**
     * Hide modal animation
     */
    hideModal(modalElement, onComplete) {
        const backdrop = modalElement.querySelector('.modal-backdrop') || modalElement;
        const content = modalElement.querySelector('.modal-content') || modalElement;

        gsap.to([content, backdrop], {
            opacity: 0,
            scale: 0.95,
            duration: this.settings.duration.fast,
            onComplete: () => {
                modalElement.classList.add('hidden');
                if (onComplete) onComplete();
            }
        });
    },

    /**
     * Bottom sheet animation
     */
    showBottomSheet(sheetElement) {
        gsap.fromTo(sheetElement,
            { y: '100%' },
            { 
                y: 0, 
                duration: this.settings.duration.normal,
                ease: this.settings.ease
            }
        );
    },

    /**
     * Hide bottom sheet animation
     */
    hideBottomSheet(sheetElement, onComplete) {
        gsap.to(sheetElement, {
            y: '100%',
            duration: this.settings.duration.fast,
            onComplete: () => {
                if (onComplete) onComplete();
            }
        });
    },

    /**
     * Teleprompter transition
     */
    teleprompterTransition(element, callback) {
        // Fade out editor
        gsap.to(element, {
            opacity: 0,
            scale: 0.98,
            duration: this.settings.duration.normal,
            onComplete: () => {
                if (callback) callback();
            }
        });
    },

    /**
     * Number counter animation
     */
    animateCounter(element, endValue, options = {}) {
        const defaults = {
            duration: 2,
            ease: 'power2.out'
        };
        const obj = { value: 0 };
        
        return gsap.to(obj, {
            value: endValue,
            duration: options.duration || defaults.duration,
            ease: options.ease || defaults.ease,
            onUpdate: () => {
                element.textContent = Math.round(obj.value).toLocaleString();
            }
        });
    },

    /**
     * Magnetic button effect
     */
    magneticButton(button, strength = 0.3) {
        button.addEventListener('mousemove', (e) => {
            if (Utils.prefersReducedMotion()) return;
            
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            gsap.to(button, {
                x: x * strength,
                y: y * strength,
                duration: 0.3,
                ease: 'power2.out'
            });
        });

        button.addEventListener('mouseleave', () => {
            gsap.to(button, {
                x: 0,
                y: 0,
                duration: 0.5,
                ease: this.settings.springEase
            });
        });
    },

    /**
     * Parallax effect
     */
    parallax(element, strength = 0.5) {
        window.addEventListener('scroll', Utils.throttle(() => {
            const scrolled = window.pageYOffset;
            gsap.to(element, {
                y: scrolled * strength,
                duration: 0
            });
        }, 16));
    },

    /**
     * Stagger animation for list items
     */
    staggerAnimate(elements, options = {}) {
        const defaults = {
            stagger: 0.1,
            y: 30,
            opacity: 0,
            duration: this.settings.duration.normal
        };
        
        return gsap.from(elements, { ...defaults, ...options });
    },

    /**
     * Cleanup and destroy animations
     */
    destroy() {
        if (typeof ScrollTrigger !== 'undefined') {
            ScrollTrigger.getAll().forEach(trigger => trigger.kill());
        }
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => Animations.init());

// Cleanup on page unload
window.addEventListener('beforeunload', () => Animations.destroy());

if (typeof module !== 'undefined' && module.exports) {
    module.exports = Animations;
}
