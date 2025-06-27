document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('scanBtn').addEventListener('click', async () => {
    const url = document.getElementById('urlInput').value;

    if (!url) {
      document.getElementById('result').innerText = "Please enter a URL.";
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
      });

      const data = await response.json();
      document.getElementById('result').innerText = `Result: ${data.result}`;
    } catch (error) {
      console.error('Error:', error);
      document.getElementById('result').innerText = "Error: Unable to scan.";
    }
  });
});
