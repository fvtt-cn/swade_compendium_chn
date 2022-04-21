Hooks.once('ready', () => {
  CONFIG.SWADE.vehicles.opSkills = ['', '驾船', '驾驶', '航空', '骑乘'];
  game.settings.register('swade', 'parryBaseSkill', {
    name: game.i18n.localize('SWADE.ParryBase'),
    hint: game.i18n.localize('SWADE.ParryBaseDesc'),
    default: '格斗',
    scope: 'world',
    type: String,
    config: false,
  });

  game.settings.register('swade', 'currencyName', {
    name: game.i18n.localize('SWADE.CurrencyName'),
    hint: game.i18n.localize('SWADE.CurrencyNameDesc'),
    scope: 'world',
    type: String,
    default: '现金',
    config: false,
  });

  game.settings.register('swade', 'coreSkills', {
    name: game.i18n.localize('SWADE.CoreSkills'),
    hint: game.i18n.localize('SWADE.CoreSkillsDesc'),
    default: '运动, 通用知识, 察觉, 交涉, 潜行',
    scope: 'world',
    type: String,
    config: false,
  });
});
