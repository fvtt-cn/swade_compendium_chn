function parseEmbeddedAbilities(value, translations, data, tc) {
	value.forEach( (item, k) => {
		let pack = game.babele.packs.find(pack => pack.translated && pack.translations[item[1].name]);
		if(pack && pack !== tc) {
      value[k][1] = mergeObject(value[k][1], pack.translate(item[1], pack.translations[item[1].name]));
		}
	});
	return value;
}

Babele.get().registerConverters({
  "translateEmbeddedAbilities": (value, translations, data, tc) => {
    return parseEmbeddedAbilities(value, translations, data, tc)
  }
});

Hooks.on('init', () => {
  if (typeof Babele !== 'undefined') {
    Babele.get().register({
      module: 'swade_compendium_chn',
      lang: 'cn',
      dir: 'compendium'
    });
  }
});
