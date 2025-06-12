const routes = {
  '/': '<h2>환영합니다!</h2><p>여기는 Henry의 개발 블로그입니다. 최신 소식을 공유합니다.</p>',
  '/about': '<h2>소개</h2><p>AI, 웹 개발, 머신러닝 등을 탐구하는 공간입니다.</p>',
  '/posts': `<h2>글 목록</h2>
    <ul>
      <li><a href="#/post/welcome">블로그 시작하며</a></li>
    </ul>`,
  '/post/welcome': '<h2>블로그 시작하며</h2><p>2025년 5월 17일 - 이 블로그는 학습 기록과 공유를 위한 공간입니다.</p>'
};

function router() {
  const hash = location.hash || '#/';
  const path = hash.slice(1);
  document.getElementById('app').innerHTML = routes[path] || '<h2>404 - 페이지를 찾을 수 없습니다</h2>';
}

window.addEventListener('hashchange', router);
window.addEventListener('load', router);
