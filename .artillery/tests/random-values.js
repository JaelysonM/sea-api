module.exports = {
  getRandomTemperature: function (payload, context, ee, next) {
    context.vars.temperature = Math.floor(Math.random() * 100) + 1;
    next();
  },
  getRandomFan: function (payload, context, ee, next) {
    context.vars.data = {
      serial: `SERIAL-${Math.floor(Math.random() * 10000)}`,
      nome: `Nome-${Math.floor(Math.random() * 1000)}`,
      status: 1,
      x_coord: Math.floor(Math.random() * 1000), // Coordenada x entre 0 e 999
      y_coord: Math.floor(Math.random() * 1000)  // Coordenada y entre 0 e 999
    };
    next();
  },
  decodeBase64ToJSON: function (payload, context, ee, next) {
    // Acessa o $loopElement.videos
    const base64String = context.vars['$loopElement'].videos;

    // Decodifica a string Base64 e converte para JSON
    const contratos = JSON.parse(Buffer.from(base64String, 'base64').toString('utf-8'));
    context.vars.data = {
      contratos
    };

    next();
  }
};
