document.addEventListener('DOMContentLoaded', () => {
  const snippetTextarea = document.getElementById('snippet');
  const maskBtn = document.getElementById('mask-btn');
  const toolBtns = document.querySelectorAll('.tool-btn');

  maskBtn.addEventListener('click', () => {
    const code = snippetTextarea.value.trim();
    if (!code) return;

    // Visual feedback
    maskBtn.textContent = 'Masking...';
    maskBtn.disabled = true;

    // Use the client-side masker.js engine
    setTimeout(() => {
      try {
        const { maskedCode, mapping } = maskContent(code, 'javascript'); // Fallback to JS for context
        if (maskedCode) {
          snippetTextarea.value = maskedCode;
          maskBtn.textContent = 'Masked!';
          
          // Show toast-like feedback
          const originalText = maskBtn.textContent;
          setTimeout(() => {
            maskBtn.textContent = 'Mask Snippet';
            maskBtn.disabled = false;
          }, 1500);
        }
      } catch (err) {
        alert('Error: ' + err.message);
        maskBtn.textContent = 'Mask Snippet';
        maskBtn.disabled = false;
      }
    }, 100); // Tiny delay for UI feel
  });

  // Handle Quick Access Tool buttons
  toolBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      chrome.tabs.create({ url: btn.dataset.url });
    });
  });
});
