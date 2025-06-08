document.addEventListener('DOMContentLoaded', function () {
    checkProgress();

    // "이메일로 보내기" 버튼 이벤트
    const sendEmailForm = document.getElementById('send-email-form');
    if (sendEmailForm) {
        sendEmailForm.addEventListener('submit', function (e) {
            e.preventDefault(); // 폼 제출 방지
            fetch('/send-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.url;
            })
            .then(url => window.location.href = url)
            .catch(error => console.error('Error:', error));
        });
    }
});

function checkProgress() {
    fetch('/progress')
        .then(response => response.json())
        .then(data => {
            const progressBar = document.getElementById('progress-bar');
            const progressText = document.getElementById('progress-text');

            progressBar.style.width = data.percentage + '%';
            progressText.textContent = data.percentage + '%';

            if (data.percentage < 100) {
                setTimeout(checkProgress, 500);
            } else {
                finishAnalysis(data);
            }
        })
        .catch(error => console.error('Error:', error));
}

function finishAnalysis(data) {
    const spinnerIcon = document.querySelector('.spinner i');
    const resultSection = document.getElementById('result-section');
    const summaryText = document.getElementById('summary-text');
    const emailSection = document.getElementById('email-section');

    if (spinnerIcon) {
        spinnerIcon.style.display = 'none';
    }

    summaryText.textContent = data.summary;
    resultSection.style.display = 'block';

    const ctx = document.getElementById('bar-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['원문 길이', '요약문 길이'],
            datasets: [{
                label: '글자 수',
                data: [data.original_length, data.summary_length],
                backgroundColor: ['#007bff', '#28a745']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: { display: true, text: '원문 vs 요약문 길이 비교' }
            },
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 500 } }
            }
        }
    });

    // credentials가 존재하면 이메일 섹션 표시
    if (emailSection && data.credentials) {
        setTimeout(() => {
            emailSection.classList.remove('hidden');
            emailSection.classList.add('show');
        }, 500);
    }
}