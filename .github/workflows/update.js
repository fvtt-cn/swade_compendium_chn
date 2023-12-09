const fs = require('fs');

const components = fs.readdirSync('./en-US/');
for (let component of components)
    if (!fs.existsSync(`./zh_Hans/${component}`))
        fs.writeFileSync(`./zh_Hans/${component}`, '{}');
