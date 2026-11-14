function bindFilters(group, cards, matches, limit, empty) {
  const buttons = [...document.querySelectorAll(group)];
  const items = [...document.querySelectorAll(cards)];
  for (const button of buttons) {
    button.addEventListener('click', () => {
      for (const option of buttons) {
        const active = option === button;
        option.classList.toggle('on', active);
        option.setAttribute('aria-pressed', String(active));
      }
      let shown = 0;
      for (const item of items) {
        const filter = button.dataset.f;
        item.hidden = shown >= limit || (filter !== 'all' && !matches(item, filter));
        if (!item.hidden) shown++;
      }
      if (empty) empty.hidden = shown > 0;
    });
  }
  buttons[0]?.click();
}

bindFilters('.tabs button', '.item', (item, filter) => item.dataset.kind === filter,
  8, document.querySelector('.feed-empty'));
bindFilters('.chips button', '.guide', (item, filter) => item.dataset.tags.split(' ').includes(filter), 8);

// Expand the News tab while keeping the default homepage feed to two rows.
document.querySelector('#view-news')?.addEventListener('click', event => {
  event.preventDefault();
  document.querySelector('.tabs [data-f="news"]').click();
  document.querySelectorAll('.item').forEach(item => { item.hidden = item.dataset.kind !== 'news'; });
  document.querySelector('#latest').scrollIntoView({behavior:'smooth'});
});
