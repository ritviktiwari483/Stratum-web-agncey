// ==========================================
// GSAP guard — if CDN fails, make everything
// visible and skip all animation code
// ==========================================
function ensureSectionsVisible() {
  document.querySelectorAll('.gsap-reveal').forEach((el) => {
    el.style.opacity = '1';
  });
}

if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
  ensureSectionsVisible();
} else {
  try {
    gsap.registerPlugin(ScrollTrigger);

    // ==========================================
    // SCROLL PROGRESS BAR
    // ==========================================
    window.addEventListener('scroll', () => {
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;
      const progressBar = document.getElementById('scrollProgressBar');
      if (progressBar) progressBar.style.width = scrolled + '%';
    });

    // ==========================================
    // HERO ANIMATIONS
    // ==========================================
    const hero = document.querySelector('#home');
    if (hero) {
      // Main Entrance Timeline
      const tl = gsap.timeline({ defaults: { ease: 'expo.out', duration: 1.6 } });
      
      tl.from('.anim-hero', { 
          yPercent: 120, 
          x: () => (Math.random() - 0.5) * 10, // Subtle jitter
          rotationX: -15,
          opacity: 0,
          stagger: 0.18,
          duration: 1.8,
          ease: "back.out(1.2)", // Slight overshoot for mechanical feel
          transformOrigin: "bottom center"
        })
        .from('.anim-hero-2', { 
          y: 20, 
          opacity: 0, 
          duration: 1 
        }, '-=1.2')
        .from('.anim-hero-3', { 
          y: 20, 
          opacity: 0, 
          duration: 1,
          stagger: 0.15
        }, '-=1')
        .from('.anim-hero-4', {
          opacity: 0,
          y: 10,
          duration: 1
        }, '-=0.8');

      // Subtle Parallax Effect
      gsap.to('.hero-title', {
        scrollTrigger: {
          trigger: '#home',
          start: 'top top',
          end: 'bottom top',
          scrub: true
        },
        y: 100,
        opacity: 0.5,
        ease: 'none'
      });
    }

    // ==========================================
    // SCROLL REVEAL (LUXURY)
    // ==========================================
    gsap.utils.toArray('.gsap-reveal').forEach((section) => {
      gsap.from(section, {
        scrollTrigger: { 
          trigger: section, 
          start: 'top 92%', 
          toggleActions: 'play none none none' 
        },
        opacity: 0,
        y: 30,
        duration: 1.2,
        ease: 'expo.out',
        clearProps: 'all'
      });
    });

    gsap.utils.toArray('.service-card, .process-step, .portfolio-card, .pricing-card').forEach((el) => {
      gsap.from(el, {
        scrollTrigger: { 
          trigger: el, 
          start: 'top 95%' 
        },
        opacity: 0,
        y: 40,
        duration: 1,
        stagger: 0.1,
        ease: 'power3.out',
        clearProps: 'all'
      });
    });

    // ==========================================
    // STATS COUNTER
    // ==========================================
    let countersAnimated = false;
    ScrollTrigger.create({
      trigger: '#stats',
      start: 'top 80%',
      once: true,
      onEnter: () => {
        if (countersAnimated) return;
        countersAnimated = true;
        gsap.utils.toArray('.counter').forEach((counter) => {
          const target = parseInt(counter.dataset.target, 10);
          const obj = { val: 0 };
          gsap.to(obj, {
            val: target,
            duration: 1,
            ease: 'power1.out',
            onUpdate: () => { counter.textContent = Math.floor(obj.val); },
            onComplete: () => { counter.textContent = target; },
          });
        });
      },
    });

    // ==========================================
    // REFRESH SCROLLTRIGGER ON LOAD
    // ==========================================
    window.addEventListener('load', () => { 
      ScrollTrigger.refresh();
      gsap.set('.gsap-reveal', { opacity: 1, visibility: 'visible' });
    });
  } catch (e) {
    console.warn('GSAP animation error:', e);
    ensureSectionsVisible();
  }
}

// ==========================================
// FAQ ACCORDION
// ==========================================
function toggleFAQ(btn) {
  const answer = btn.nextElementSibling;
  const icon = btn.querySelector('i');
  const isOpen = answer.classList.contains('open');
  
  // Close all other FAQs
  document.querySelectorAll('.faq-answer.open').forEach(opened => {
    if (opened !== answer) {
      opened.classList.remove('open');
      const otherIcon = opened.previousElementSibling.querySelector('i');
      if (typeof gsap !== 'undefined') {
        gsap.to(otherIcon, { rotate: 0, duration: 0.3 });
      } else {
        otherIcon.style.transform = 'rotate(0deg)';
      }
    }
  });

  const opening = !isOpen;
  answer.classList.toggle('open');
  
  if (typeof gsap !== 'undefined') {
    gsap.to(icon, { rotate: opening ? 180 : 0, duration: 0.3 });
  } else {
    icon.style.transform = opening ? 'rotate(180deg)' : 'rotate(0deg)';
  }
}

function closeMenu() {
  const mobileMenu = document.getElementById('mobileMenu');
  const menuIcon = document.getElementById('menuIcon');
  if (mobileMenu) {
    mobileMenu.classList.add('max-h-0');
    mobileMenu.classList.remove('max-h-[500px]');
    document.body.style.overflow = '';
    if (menuIcon) {
      menuIcon.classList.remove('fa-xmark');
      menuIcon.classList.add('fa-bars');
    }
  }
}

// ==========================================
// MOBILE MENU TOGGLE
// ==========================================
const menuToggle = document.getElementById('menuToggle');
if (menuToggle) {
  menuToggle.addEventListener('click', () => {
    const mobileMenu = document.getElementById('mobileMenu');
    const menuIcon = document.getElementById('menuIcon');
    const navbar = document.getElementById('navbar');
    const isOpen = !mobileMenu.classList.contains('max-h-0');

    if (isOpen) {
      mobileMenu.classList.add('max-h-0');
      mobileMenu.classList.remove('max-h-[500px]');
      menuIcon.classList.remove('fa-xmark');
      menuIcon.classList.add('fa-bars');
      document.body.style.overflow = '';
    } else {
      mobileMenu.classList.remove('max-h-0');
      mobileMenu.classList.add('max-h-[500px]');
      mobileMenu.style.top = navbar.offsetHeight + 'px';
      menuIcon.classList.remove('fa-bars');
      menuIcon.classList.add('fa-xmark');
      document.body.style.overflow = 'hidden';
    }
  });
}

// ==========================================
// NAVBAR SCROLL EFFECT
// ==========================================
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (navbar) {
    navbar.classList.toggle('nav-scrolled', window.scrollY > 50);
  }
});

// ==========================================
// BACK TO TOP
// ==========================================
const backToTop = document.getElementById('backToTop');
if (backToTop) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
      backToTop.classList.remove('hidden');
      backToTop.style.display = 'flex';
    } else {
      backToTop.classList.add('hidden');
      backToTop.style.display = 'none';
    }
  });
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}// ==========================================
// CONFIGURATION
// ==========================================
const STRATUM_CONFIG = {
  USE_DIRECT_FORM: true,
  FORM_ACTION: "https://formsubmit.io/send/startumweb@gmail.com",
  LOCAL_PORT: 8000
};

// ==========================================
// CONTACT FORM HANDLER
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
  const contactForm = document.querySelector('#contact form');
  let lastSubmitTime = 0;

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      // DIRECT FORM SUBMISSION (no server needed)
      if (STRATUM_CONFIG.USE_DIRECT_FORM) {
        const redirect = document.createElement('input');
        redirect.type = 'hidden';
        redirect.name = '_next';
        redirect.value = window.location.href;
        contactForm.appendChild(redirect);
        contactForm.action = STRATUM_CONFIG.FORM_ACTION;
        contactForm.method = "POST";
        return;
      }
      
      e.preventDefault();
      
      const currentTime = Date.now();
      if (currentTime - lastSubmitTime < 10000) return; 
      
      const btn = contactForm.querySelector('button');
      const originalText = btn.innerHTML;
      const formData = new FormData(contactForm);

      // 1. HONEYPOT CHECK
      if (formData.get('_honeypot')) {
        btn.innerHTML = '<i class="fa-solid fa-circle-check"></i> SENT SUCCESSFULLY';
        contactForm.reset();
        return; 
      }

      // 2. HANDLE SUBMISSION
      if (STRATUM_CONFIG.USE_DIRECT_FORM) {
        contactForm.removeEventListener('submit', this);
        contactForm.action = STRATUM_CONFIG.FORM_ACTION;
        contactForm.method = "POST";
        contactForm.submit();
        return;
      }

      // 2. RESOLVE API URL
      let API_URL = "";
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      
      if (STRATUM_CONFIG.PRODUCTION_API_URL) {
        API_URL = `${STRATUM_CONFIG.PRODUCTION_API_URL}/api/contact`;
      } else if (isLocal) {
        API_URL = `http://localhost:${STRATUM_CONFIG.LOCAL_PORT}/api/contact`;
      } else {
        // Fallback: If no production URL is set, try to use current hostname (GitHub)
        // Note: This will likely fail due to lack of an API on GitHub server
        API_URL = `${window.location.protocol}//${window.location.hostname}:${STRATUM_CONFIG.LOCAL_PORT}/api/contact`;
      }

      try {
        console.log(`[StratumWeb] Submission attempt to: ${API_URL}`);
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> SENDING...';
        btn.disabled = true;

        const body = JSON.stringify({
          name: formData.get("full_name"),
          phone: (formData.get("country_code") || "") + " " + (formData.get("phone_number") || ""),
          email: formData.get("email"),
          country: formData.get("user_country"),
          message: formData.get("message")
        });

        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.message || `Server Error (${response.status})`);
        }

        console.log("[StratumWeb] Lead captured successfully!");
        lastSubmitTime = currentTime;
        btn.innerHTML = '<i class="fa-solid fa-circle-check scale-125"></i> SENT SUCCESSFULLY';
        btn.style.background = '#10b981';
        contactForm.reset();

      } catch (error) {
        console.error("[StratumWeb] Form Error:", error);
        btn.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> ERROR - TRY AGAIN';
        btn.style.background = '#ef4444';
        
        // Helpful tip for the owner
        if (!isLocal && !STRATUM_CONFIG.PRODUCTION_API_URL) {
          alert("BACKEND NOT FOUND: You are on the live site but no Production API URL is set in main.js. Please host your backend or use Ngrok.");
        }
      } finally {
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.style.background = '';
          btn.disabled = false;
        }, 4000);
      }
    });
  }
});

// ==========================================
// LIGHTBOX
// ==========================================
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightboxImg');
const lightboxClose = document.getElementById('lightboxClose');

document.querySelectorAll('.portfolio-card img').forEach((img) => {
  img.style.cursor = 'pointer';
  img.addEventListener('click', () => {
    lightboxImg.src = img.src;
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  });
});

function closeLightbox() {
  lightbox.classList.remove('open');
  document.body.style.overflow = '';
}

lightbox.addEventListener('click', closeLightbox);
lightboxClose.addEventListener('click', (e) => { e.stopPropagation(); closeLightbox(); });

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeLightbox();
});
  }
});

// ==========================================
// STATS COUNTER ANIMATION
// ==========================================
function initCounters() {
    const statsSection = document.querySelector('#stats');
    if (!statsSection) return;

    const counters = document.querySelectorAll('.counter');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                counters.forEach(counter => {
                    const target = parseInt(counter.getAttribute('data-target'));
                    let current = 0;
                    const duration = 2000; // 2 seconds
                    const stepTime = 20;
                    const increment = target / (duration / stepTime);
                    
                    const countIt = () => {
                        current += increment;
                        if (current < target) {
                            counter.innerText = Math.ceil(current);
                            setTimeout(countIt, stepTime);
                        } else {
                            counter.innerText = target;
                        }
                    };
                    countIt();
                });
                observer.unobserve(statsSection);
            }
        });
    }, { threshold: 0.2 });

    observer.observe(statsSection);
}

document.addEventListener('DOMContentLoaded', () => {
    initCounters();
});
