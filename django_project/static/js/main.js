// Back to top
const backToTop = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
  backToTop.style.display = window.scrollY > 500 ? 'flex' : 'none';
});
backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Mobile menu
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');
const menuIcon = document.getElementById('menuIcon');
const navbar = document.getElementById('navbar');

function toggleMobileMenu(open) {
  const isOpen = open !== undefined ? open : mobileMenu.classList.contains('max-h-0');
  mobileMenu.classList.toggle('max-h-0', !isOpen);
  mobileMenu.classList.toggle('max-h-[500px]', isOpen);
  mobileMenu.style.top = navbar.offsetHeight + 'px';
  document.body.style.overflow = isOpen ? 'hidden' : '';
  menuIcon.classList.remove('fa-bars', 'fa-xmark');
  menuIcon.classList.add(isOpen ? 'fa-xmark' : 'fa-bars');
}

menuToggle.addEventListener('click', () => {
  toggleMobileMenu(mobileMenu.classList.contains('max-h-0'));
});

function closeMenu() {
  toggleMobileMenu(false);
}

// Scroll reveal
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// Navbar glass effect
window.addEventListener('scroll', () => {
  navbar.classList.toggle('nav-scrolled', window.scrollY > 80);
});

// FAQ accordion
function toggleFAQ(btn) {
  const answer = btn.nextElementSibling;
  const icon = btn.querySelector('i');
  answer.classList.toggle('open');
  icon.style.transform = answer.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0)';
}

// Counter animation
let countersAnimated = false;
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !countersAnimated) {
      countersAnimated = true;
      document.querySelectorAll('.counter').forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const step = Math.max(1, Math.floor(target / (2000 / 16)));
        let current = 0;
        function update() {
          current += step;
          if (current >= target) {
            counter.textContent = target;
            return;
          }
          counter.textContent = current;
          requestAnimationFrame(update);
        }
        update();
      });
    }
  });
}, { threshold: 0.5 });
const statsSection = document.getElementById('stats');
if (statsSection) statsObserver.observe(statsSection);