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
    gsap.registerPlugin(ScrollTrigger, TextPlugin);

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
    // HERO ANIMATIONS (Subtle)
    // ==========================================
    const hero = document.querySelector('#home');
    if (hero) {
      const tl = gsap.timeline({ defaults: { ease: 'power2.out', duration: 0.6 } });
      tl.from('.anim-hero', { y: 20, opacity: 0, stagger: 0.1 })
        .from('.anim-hero-2', { opacity: 0, y: 10 }, '-=0.3')
        .from('.anim-hero-3', { opacity: 0, y: 10 }, '-=0.3')
        .from('.anim-hero-4', { opacity: 0 }, '-=0.2');
    }

    // ==========================================
    // SCROLL REVEAL (Reliable .from() logic)
    // ==========================================
    gsap.utils.toArray('.gsap-reveal').forEach((section) => {
      gsap.from(section, {
        scrollTrigger: {
          trigger: section,
          start: 'top 85%',
          toggleActions: 'play none none none',
        },
        y: 30,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out',
        clearProps: 'all'
      });
    });

    // Individual Card Animators
    const animateSubItems = (selector, trigger) => {
      gsap.from(selector, {
        scrollTrigger: { trigger: trigger, start: 'top 80%' },
        y: 20,
        opacity: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: 'power2.out',
        clearProps: 'all'
      });
    };

    animateSubItems('.service-card', '#services');
    animateSubItems('.process-step', '#process');
    animateSubItems('.portfolio-card', '#work');

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
            duration: 1.5,
            ease: 'power2.out',
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
// CONTACT FORM HANDLER (GOOGLE SHEETS)
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
  const contactForm = document.querySelector('#contact form');
  let lastSubmitTime = 0; // For Rate Limiting

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const currentTime = Date.now();
      // Prevent clicking submit more than once every 10 seconds
      if (currentTime - lastSubmitTime < 10000) {
        return; 
      }
      
      const btn = contactForm.querySelector('button');
      const originalText = btn.innerHTML;
      const formData = new FormData(contactForm);

      // 1. HONEYPOT CHECK
      if (formData.get('_honeypot')) {
        console.warn("Spam detected!");
        btn.innerHTML = '<i class="fa-solid fa-circle-check"></i> SENT SUCCESSFULLY';
        contactForm.reset();
        return; 
      }

      const SCRIPT_URL = "REPLACE_WITH_YOUR_NEW_SCRIPT_URL";

      try {
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> SENDING...';
        btn.disabled = true;

        const searchParams = new URLSearchParams();
        for (const pair of formData) {
          searchParams.append(pair[0], pair[1]);
        }

        await fetch(SCRIPT_URL, {
          method: 'POST',
          body: searchParams,
          mode: 'no-cors'
        });

        lastSubmitTime = currentTime;
        btn.innerHTML = '<i class="fa-solid fa-circle-check scale-125"></i> SENT SUCCESSFULLY';
        btn.style.background = '#10b981';
        contactForm.reset();
        
      } catch (error) {
        btn.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> ERROR - TRY AGAIN';
        btn.style.background = '#ef4444';
      } finally {
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.style.background = '';
          btn.disabled = false;
        }, 3000);
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

