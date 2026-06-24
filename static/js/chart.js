document.addEventListener("DOMContentLoaded", function () {
  const labelEl = document.getElementById('donation-labels');
  const dataEl = document.getElementById('donation-data');

  if (!labelEl || !dataEl) {
    console.warn("Donation data not found in DOM.");
    return;
  }

  const donationLabels = JSON.parse(labelEl.textContent);
  const donationData = JSON.parse(dataEl.textContent);

  const ctx = document.getElementById('donationChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: donationLabels,
      datasets: [{
        label: 'Donations (₹)',
        data: donationData,
        backgroundColor: 'rgba(0, 123, 255, 0.6)',
        borderRadius: 5,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 50 }
        }
      }
    }
  });
});