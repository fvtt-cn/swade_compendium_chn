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

function pagesConverter(pages, translations) {
  return pages.map(data => {
      if (!translations) {
          return data;
      }

      const translation = translations[data._id] || translations[data.name];
      if (!translation) {
          return data;
      }

      return mergeObject(data, {
          name: translation.name,
          image: { caption: translation.caption ?? data.image.caption },
          src: translation.src ?? data.src,
          text: { content: translation.text ?? data.text.content },
          video: {
              width: translation.width ?? data.video.width,
              height: translation.height ?? data.video.height,
          },
          translated: true,
      });
  });
};

const SWADE_ITEM_CONVERTERS = Converters.fromPack(SWADE_ITEM_MAPPING, "Item");
Babele.get().registerConverters({
  SWADE_ITEM_CONVERTERS: SWADE_ITEM_CONVERTERS,
});

Babele.get().registerConverters({
  "pagesConverter": (pages, translations) => { return pagesConverter(pages, translations)}
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
