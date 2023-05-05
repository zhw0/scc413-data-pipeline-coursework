const facts = require("./models/facts");
const { convert } = require("sst");
const { localizations } = require("./models/localizations");

let fullCode = [];
let shortISO = [];

// Dynamically fill the fullCode and shortISO list with the provided config information in the language files
for (const language in localizations) {
  fullCode.push(localizations[language].code);
  shortISO.push(localizations[language].langISO);
}

const VALID_LANGUAGES = shortISO.concat(fullCode);

/**
 * validateCount
 * @description Check if user entered valid count parameter
 * @param {Number} param
 * @param {String} lang
 * @returns {Boolean} true if valid
 */
function validateCount(param, lang) {
  const safeParam = convert.toNumber(param);
  if (safeParam <= 1 || safeParam >= facts.getLanguageFacts(lang).length) {
    return false;
  }
  return true;
}

/**
 * validateLanguage
 * @description a middleware for validating the language parameter.
 * @param language {String} The language to validate.
 * @returns {Boolean} True if the language is valid, false otherwise.
 */
function validateLanguage(language) {
  console.log(`checking ... ${language}`);
  if (VALID_LANGUAGES.indexOf(language) === -1) {
    return false;
  }
  return true;
}

/**
 * invalidLanguageMiddleware
 * @param {Request} request - Express request object
 * @param {Response} response - Express response object
 * @param {NextFunction} next - Express next function
 */
function invalidLanguageMiddleware(request, response, next) {
  if (request.query && request.query.lang && request.query.lang != undefined) {
    if (!validateLanguage(request.query.lang)) {
      // language specified, so continue
      response
        .status(400)
        .send(
          `Invalid language, valid languages are ${VALID_LANGUAGES.join(", ")}`
        );
      return;
    }
  }
  next();
}

/**
 * invalidCountMiddleware
 * @description check if the item count is correctly between the min and max (per the requested local's if one is set)
 * @param {Request} request - Express request object
 * @param {Response} response - Express response object
 * @param {NextFunction} next - Express next function
 */
function invalidCountMiddleware(request, response, next) {
  if (
    request.query &&
    request.query.count &&
    request.query.count == undefined
  ) {
    response
      .status(400)
      .send(
        `Invalid count, valid counts are between 2 and ${
          facts.getLanguageFacts(request.query.lang).length
        }`
      );
    return;
  }
  next();
}

function invalidIDMiddleware(request, response, next) {
  if (!request.query || !request.query.id || request.query.id.length != 0) {
    next(); // no id specified, so continue
  }

  if (!validateCount(request.query.id, request.query.lang)) {
    // id specified, so continue
    response
      .status(400)
      .send(
        `Invalid ID, valid IDs are between 1 and ${
          facts.getLanguageFacts(request.query.lang).length
        }`
      );
    return;
  }
  next();
}

module.exports = {
  invalidLanguageMiddleware,
  invalidCountMiddleware,
  invalidIDMiddleware,
};
