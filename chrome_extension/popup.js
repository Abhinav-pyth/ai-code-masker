document.addEventListener('DOMContentLoaded', () => {
  const snippetTextarea = document.getElementById('snippet');
  const maskBtn = document.getElementById('mask-btn');
  const toolBtns = document.querySelectorAll('.tool-btn');

  maskBtn.addEventListener('click', async () => {
    const code = snippetTextarea.value.trim();
    if (!code) return;

    maskBtn.textContent = 'Masking...';
    maskBtn.disabled = true;

    try {
      const resp = await fetch('http://localhost:3000/api/mask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, lang: 'python' })
      });
      const data = await resp.json();
      if (data.masked_code) {
        snippetTextarea.value = data.masked_code;
        maskBtn.textContent = 'Masked!';
      } else {
        throw new Error(data.error || 'Failed to mask');
      }
    } catch (err) {
      alert('Error: ' + err.message + '\nMake sure the local server is running on port 3000.');
      maskBtn.textContent = 'Mask Snippet';
    } finally {
      maskBtn.disabled = false;
      setTimeout(() => { if (maskBtn.textContent === 'Masked!') maskBtn.textContent = 'Mask Snippet'; }, 2000);
    }
  });

  toolBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      chrome.tabs.create({ url: btn.dataset.url });
    });
  });
});
