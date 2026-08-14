(() => {
  const header = document.querySelector('.site-header');
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  const syncHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 12);
  const closeNavigation = ({ returnFocus = false } = {}) => {
    if (!navLinks?.classList.contains('is-open')) return;
    navLinks.classList.remove('is-open');
    navToggle?.setAttribute('aria-expanded', 'false');
    navToggle?.setAttribute('aria-label', '展开导航');
    if (returnFocus) navToggle?.focus();
  };

  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });

  navToggle?.addEventListener('click', () => {
    const open = navLinks?.classList.toggle('is-open') ?? false;
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? '收起导航' : '展开导航');
  });

  navLinks?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => closeNavigation());
  });

  document.addEventListener('click', (event) => {
    if (!header?.contains(event.target)) closeNavigation();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNavigation({ returnFocus: true });
  });

  const desktopNavigation = window.matchMedia('(min-width: 769px)');
  const resetNavigationAtDesktop = (event) => {
    if (event.matches) closeNavigation();
  };
  desktopNavigation.addEventListener?.('change', resetNavigationAtDesktop);

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = [...document.querySelectorAll('.reveal')];
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -32px' });
    revealItems.forEach((item) => observer.observe(item));
  }

  const filterButtons = [...document.querySelectorAll('[data-project-filter]')];
  const projectCards = [...document.querySelectorAll('[data-project-categories]')];
  if (filterButtons.length && projectCards.length) {
    filterButtons.forEach((button) => {
      button.addEventListener('click', () => {
        const filter = button.dataset.projectFilter;
        filterButtons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
        projectCards.forEach((card) => {
          const categories = card.dataset.projectCategories?.split(' ') ?? [];
          card.hidden = filter !== 'all' && !categories.includes(filter);
        });
      });
    });
  }

  document.querySelectorAll('[data-carousel]').forEach((carousel) => {
    const slides = [...carousel.querySelectorAll('[data-carousel-slide]')];
    const previousButton = carousel.querySelector('[data-carousel-prev]');
    const nextButton = carousel.querySelector('[data-carousel-next]');
    const dots = [...carousel.querySelectorAll('[data-carousel-dot]')];
    const status = carousel.querySelector('[data-carousel-status]');
    if (!slides.length || !previousButton || !nextButton) return;

    let currentIndex = 0;
    const showSlide = (index, { focusDot = false } = {}) => {
      currentIndex = (index + slides.length) % slides.length;
      slides.forEach((slide, slideIndex) => {
        slide.hidden = slideIndex !== currentIndex;
      });
      dots.forEach((dot, dotIndex) => {
        dot.setAttribute('aria-current', String(dotIndex === currentIndex));
      });
      if (status) status.textContent = `${currentIndex + 1} / ${slides.length}`;
      if (focusDot) dots[currentIndex]?.focus();
    };

    previousButton.addEventListener('click', () => showSlide(currentIndex - 1));
    nextButton.addEventListener('click', () => showSlide(currentIndex + 1));
    dots.forEach((dot, index) => dot.addEventListener('click', () => showSlide(index)));
    carousel.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        showSlide(currentIndex - 1);
      }
      if (event.key === 'ArrowRight') {
        event.preventDefault();
        showSlide(currentIndex + 1);
      }
      if (event.key === 'Home') {
        event.preventDefault();
        showSlide(0, { focusDot: true });
      }
      if (event.key === 'End') {
        event.preventDefault();
        showSlide(slides.length - 1, { focusDot: true });
      }
    });

    carousel.classList.add('carousel-ready');
    showSlide(0);
  });

  document.querySelectorAll('[data-year]').forEach((node) => {
    node.textContent = String(new Date().getFullYear());
  });
})();
