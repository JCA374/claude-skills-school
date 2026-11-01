// Shared top navigation + footer. Pages set <body data-root="."> (or ".." in a subfolder) and data-page.
(function () {
  const root = document.body.dataset.root || '.';
  const page = document.body.dataset.page || '';
  const tabs = [
    ['home', 'index.html', 'Start'], ['skills', 'skills.html', 'Your skills'], ['lessons', 'lessons.html', 'Lessons'],
    ['videos', 'videos.html', 'Videos'], ['podcast', 'podcast/index.html', 'Podcast'], ['example', 'example.html', 'Paper reviewer'],
    ['improve', 'improve.html', 'Improve skills'], ['projects', 'projects.html', 'Projects'],
  ];
  const nav = document.createElement('header');
  nav.className = 'top';
  nav.innerHTML = `<div class="wrap"><a class="brand" href="${root}/index.html">Skills <span>School</span></a>
    <nav class="tabs">${tabs.map(([id, href, label]) => `<a href="${root}/${href}" class="${id === page ? 'on' : ''}">${label}</a>`).join('')}</nav></div>`;
  document.body.prepend(nav);
  const f = document.createElement('footer');
  f.innerHTML = 'Built by Claude from the skill files on this machine. Narration: Kokoro (local TTS, af_heart), checked by Whisper. Every number comes from a file.';
  document.body.append(f);
  const on = document.querySelector('.tabs a.on');
  if (on) on.scrollIntoView({ block: 'nearest', inline: 'center' });
})();
