const facts = [
  "En 1987, los gatos superaron a los perros como la mascota número uno en Estados Unidos.",
  "Los gatos que viven juntos a veces se frotan la cabeza para demostrar que no tienen intención de pelear. Los gatos jóvenes hacen esto con más frecuencia, especialmente cuando están emocionados",
  "Las mamás gatas enseñan a sus gatitos a usar la caja de arena.",
  "Para darse de baja de catfacts, responda el siguiente código: tj3G5de$se",
  "¡Tienes que ser gatito me! ¿Estás seguro de que quieres darte de baja? envía SÍ o NO",
];

const langName = "spanish",
  langISO = "esp",
  langLocale = "mx",
  langLocaleName = "mexican";

module.exports = {
  langName,
  langISO,
  langLocale,
  langLocaleName,
  code: `${langISO}-${langLocale}`,
  codeName: `${langName} (${langLocaleName})`,
  facts: facts,
};
