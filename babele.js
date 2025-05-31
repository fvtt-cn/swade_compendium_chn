// Constants
const SWADE_ITEM_MAPPING = {
  description: "system.description",
  notes: "system.notes",
  actions: "system.actions",
  range: "system.range",
  ammo: "system.ammo",
  category: "system.category",
};

// Utility functions
const parseEmbeddedAbilities = (value, translations, data, tc) => {
  if (!Array.isArray(value)) return value;
  
  return value.map((item, k) => {
    const pack = game.babele.packs.find(
      (pack) => pack.translated && pack.translations[item[1].name]
    );
    
    if (pack && pack !== tc) {
      return [
        item[0],
        mergeObject(
          item[1],
          pack.translate(item[1], pack.translations[item[1].name])
        )
      ];
    }
    return item;
  });
};

const loadStyle = (url) => {
  try {
    const link = document.createElement('link');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = url;
    document.head.appendChild(link);
  } catch (error) {
    console.error('Failed to load style:', error);
  }
};

// Initialize Babele
Hooks.once("babele.init", (babele) => {
  if (typeof Babele === "undefined") {
    console.error("Babele module not found");
    return;
  }

  try {
    // Register module
    babele.register({
      module: "swade_compendium_chn",
      lang: "cn",
      dir: "compendium",
    });

    // Load styles
    loadStyle('../../modules/swade_compendium_chn/swade-core.css');

    // Register converters
    if (!babele.converters) {
      console.error("Babele Converters not initialized");
      return;
    }

    // Create a wrapper for the pages converter to ensure proper data handling
    const pagesConverter = (pages, translations) => {
      if (!Array.isArray(pages)) {
        console.warn('Pages converter received non-array data:', pages);
        return pages;
      }
      return pages.map(data => {
        if (!translations) return data;

        const translation = translations[data._id] || translations[data.name];
        if (!translation) return data;

        return foundry.utils.mergeObject(data, {
          name: translation.name,
          image: { caption: translation.caption ?? data.image?.caption ?? "" },
          src: translation.src ?? data.src,
          text: { content: translation.text ?? data.text?.content ?? "" },
          translated: true,
        });
      });
    };

    // Register basic converters
    babele.registerConverters({
      translateEmbeddedAbilities: parseEmbeddedAbilities,
      pages: pagesConverter,
    });

    // Create a wrapper for the SWADE item converter to ensure proper data handling
    const swadeItemConverter = (items, translations) => {
      // Ensure items is an array
      const itemsArray = Array.isArray(items) ? items : [items];
      const converter = babele.converters.fromPack(SWADE_ITEM_MAPPING, "Item");
      return converter(itemsArray, translations);
    };

    // Register the wrapped converter
    babele.registerConverters({
      SWADE_ITEM_CONVERTERS: swadeItemConverter
    });

  } catch (error) {
    console.error('Failed to initialize Babele:', error);
  }
});
