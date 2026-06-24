window.addEventListener('scroll', function() {
    document.querySelector('.navbar').classList.toggle('scrolled', window.scrollY > 50);
});

// Bootstrap validation
(() => {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();

  // Smooth scroll for anchor links (excluding dropdown toggles)
  document.querySelectorAll('a[href^="#"]:not(.dropdown-toggle)').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      if (!this.dataset.bsToggle || this.dataset.bsToggle !== 'modal') {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });

  // Initialize AOS animation
  document.addEventListener('DOMContentLoaded', function () {
    AOS.init({
      duration: 800,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  });

  // Function for gallery modal image update
  function updateGalleryImage(src) {
    document.getElementById('galleryModalImage').src = src;
  }

  (() => {
  'use strict'
  const form = document.querySelector('form.needs-validation');
  const formMessage = document.getElementById('form-message');

  form.addEventListener('submit', event => {
    if (!form.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
      form.classList.add('was-validated');
      formMessage.textContent = '';  // Clear message
    } else {
      // Optional: show a loading message or disable button here
      // Let form submit normally, or handle with AJAX if you want
      formMessage.textContent = 'Sending your message...';
    }
  }, false);
})();