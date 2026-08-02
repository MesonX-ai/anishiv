(function () {
  function normalizePlaceholder(value, placeholder) {
    var trimmed = (value || '').replace(/^\s+|\s+$/g, '');
    return trimmed === placeholder ? '' : trimmed;
  }

  function setStatus(node, message, isError) {
    if (!node) {
      return;
    }
    node.style.color = isError ? '#b30000' : '#0b5e20';
    node.textContent = message;
  }

  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function toFormData(payload) {
    var parts = [];
    for (var key in payload) {
      if (Object.prototype.hasOwnProperty.call(payload, key)) {
        parts.push(encodeURIComponent(key) + '=' + encodeURIComponent(payload[key]));
      }
    }
    return parts.join('&');
  }

  function initContactForm() {
    var form = document.getElementById('homeContactForm');
    var statusNode = document.getElementById('contactFormStatus');
    if (!form) {
      return;
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      var nameInput = form.elements.name;
      var emailInput = form.elements.email;
      var messageInput = form.elements.text;
      var honeypotInput = form.elements.website;
      var submitButton = form.querySelector('input[type="submit"]');

      var name = normalizePlaceholder(nameInput && nameInput.value, 'Your Name');
      var email = normalizePlaceholder(emailInput && emailInput.value, 'Your Email');
      var message = normalizePlaceholder(messageInput && messageInput.value, 'Your Message');
      var honeypot = (honeypotInput && honeypotInput.value) ? honeypotInput.value : '';

      if (!name || !email || !message) {
        setStatus(statusNode, 'Please complete name, email, and message.', true);
        return;
      }

      if (!validateEmail(email)) {
        setStatus(statusNode, 'Please enter a valid email address.', true);
        return;
      }

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.value = 'Sending...';
      }
      setStatus(statusNode, 'Sending your message...', false);

      var payload = {
        name: name,
        email: email,
        message: message,
        text: message,
        website: honeypot,
        contact_task: 'send'
      };

      fetch(form.getAttribute('action'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: toFormData(payload)
      })
        .then(function (response) {
          if (!response.ok) {
            throw new Error('Request failed with status ' + response.status);
          }
          return response.json();
        })
        .then(function (result) {
          if (result && result.ok) {
            setStatus(statusNode, result.message || 'Message sent successfully.', false);
            form.reset();
            if (nameInput) {
              nameInput.value = 'Your Name';
            }
            if (emailInput) {
              emailInput.value = 'Your Email';
            }
            if (messageInput) {
              messageInput.value = 'Your Message';
            }
          } else {
            setStatus(statusNode, (result && result.message) || 'Unable to send your message right now.', true);
          }
        })
        .catch(function () {
          setStatus(statusNode, 'Unable to send your message right now. Please try again later.', true);
        })
        .finally(function () {
          if (submitButton) {
            submitButton.disabled = false;
            submitButton.value = 'Send Message';
          }
        });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initContactForm);
  } else {
    initContactForm();
  }
})();
