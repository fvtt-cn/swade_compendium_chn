Hooks.on('init', () => {
  if (typeof Babele !== 'undefined') {
    Babele.get().register({
      module: 'swade_compendium_chn',
      lang: 'cn',
      dir: 'compendium'
    });
  }
});
