function parseEmbeddedAbilities(value, translations, data, tc) {
	value.forEach( (item, k) => {
		let pack = game.babele.packs.find(pack => pack.translated && pack.translations[item[1].name]);
		if(pack && pack !== tc) {
      value[k][1] = mergeObject(value[k][1], pack.translate(item[1], pack.translations[item[1].name]));
		}
	});
	return value;
}
const SWADE_ITEM_MAPPING = {
  description: "system.description",
  notes: "system.notes",
  actions: "system.actions",
  range: "system.range",
  ammo: "system.ammo",
  category: "system.category",
};
const SWADE_ITEM_CONVERTERS = Converters.fromPack(SWADE_ITEM_MAPPING, "Item");
Babele.get().registerConverters({
  SWADE_ITEM_CONVERTERS: SWADE_ITEM_CONVERTERS,
});
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
