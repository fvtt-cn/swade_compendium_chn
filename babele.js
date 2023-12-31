function parseEmbeddedAbilities(value, translations, data, tc) {
  value.forEach((item, k) => {
    let pack = game.babele.packs.find(
      (pack) => pack.translated && pack.translations[item[1].name]
    );
    if (pack && pack !== tc) {
      value[k][1] = mergeObject(
        value[k][1],
        pack.translate(item[1], pack.translations[item[1].name])
      );
    }
  });
  return value;
}

Babele.get().registerConverters({
  translateEmbeddedAbilities: (value, translations, data, tc) => {
    return parseEmbeddedAbilities(value, translations, data, tc);
  },
});

const SWADE_ITEM_MAPPING = {
  description: "system.description",
  notes: "system.notes",
  actions: "system.actions",
  range: "system.range",
  ammo: "system.ammo",
  category: "system.category",
};
const SWADE_ITEM_CONVERTERS = Converters.fromPack(SWADE_ITEM_MAPPING, "Item");
function SWADE_REQUIREMENTS_CONVERTER(value, translations) {
  const result = [];
  for (let raw of value) {
    const rawToR = {};
    Object.assign(rawToR, raw);
    if (rawToR.type=='rank')
    result.push(rawToR);
  }
  const other={type:'other',label:translations}
  result.push(other)
  return result;
}
Babele.get().registerConverters({
  SWADE_ITEM_CONVERTERS: SWADE_ITEM_CONVERTERS,
  SWADE_REQUIREMENTS_CONVERTER: SWADE_REQUIREMENTS_CONVERTER,
});
Hooks.on("init", () => {
  if (typeof Babele !== "undefined") {
    console.log("mapping", Babele);
    console.log(Converters);
    Babele.get().register({
      module: "swade_compendium_chn",
      lang: "cn",
      dir: "compendium",
    });
  }
});
