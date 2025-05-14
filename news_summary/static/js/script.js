document.addEventListener('DOMContentLoaded', function () {
    checkProgress();
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

    // 압축률 그래프 그리기
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
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 500 }
                }
            }
        }
    });

    // 이메일 입력창 fade-in
    setTimeout(() => {
        emailSection.classList.remove('hidden');
        emailSection.classList.add('show');
    }, 500);
}

function sendEmail() {
    const emailInput = document.getElementById('email-input').value;

    if (!emailInput || !emailInput.includes('@')) {
        alert("올바른 이메일 주소를 입력해주세요.");
        return;
    }

    fetch('/send-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: emailInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('메일이 성공적으로 전송되었습니다!');
        } else {
            alert('메일 전송에 실패했습니다. 다시 시도해주세요.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('메일 전송 중 오류가 발생했습니다.');
    });
}