(() => {
  const root = document.documentElement;
  const currentLanguage = root.dataset.language;
  const counterpart = root.dataset.languageCounterpart;
  const storageKey = 'xzeng-language';

  if (!currentLanguage || !counterpart) return;

  const getSavedLanguage = () => {
    try {
      return window.localStorage.getItem(storageKey);
    } catch {
      return null;
    }
  };

  const saveLanguage = (language) => {
    try {
      window.localStorage.setItem(storageKey, language);
    } catch {
      // Language switching still works when storage is unavailable.
    }
  };

  const browserLanguage = (navigator.languages?.[0] || navigator.language || 'en').toLowerCase();
  const preferredLanguage = getSavedLanguage() || (browserLanguage.startsWith('zh') ? 'zh' : 'en');

  if (preferredLanguage !== currentLanguage) {
    const destination = new URL(counterpart, window.location.origin);
    destination.search = window.location.search;
    destination.hash = window.location.hash;
    window.location.replace(destination.href);
    return;
  }

  window.addEventListener('DOMContentLoaded', () => {
    const navigationToggle = document.querySelector('.nav-toggle');
    if (navigationToggle) {
      navigationToggle.dataset.labelOpen = currentLanguage === 'zh' ? '展开导航' : 'Open navigation';
      navigationToggle.dataset.labelClose = currentLanguage === 'zh' ? '收起导航' : 'Close navigation';
      navigationToggle.setAttribute('aria-label', navigationToggle.dataset.labelOpen);
    }

    const navigation = document.querySelector('.nav-links');
    if (navigation && !navigation.querySelector('[data-language-toggle]')) {
      const control = document.createElement('a');
      const targetLanguage = currentLanguage === 'zh' ? 'en' : 'zh';
      control.className = 'language-toggle';
      control.dataset.languageToggle = '';
      control.href = counterpart;
      control.lang = targetLanguage === 'zh' ? 'zh-CN' : 'en';
      control.hreflang = control.lang;
      control.textContent = targetLanguage === 'zh' ? '中文' : 'EN';
      control.setAttribute('aria-label', targetLanguage === 'zh' ? '切换到中文' : 'Switch to English');
      navigation.after(control);
    }

    document.querySelectorAll('[data-language-toggle]').forEach((control) => {
      control.addEventListener('click', () => {
        saveLanguage(currentLanguage === 'zh' ? 'en' : 'zh');
        const destination = new URL(control.getAttribute('href') || counterpart, window.location.origin);
        destination.search = window.location.search;
        destination.hash = window.location.hash;
        control.href = destination.href;
      });
    });
  });
})();
