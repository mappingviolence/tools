/**
 * Extracts the current version of all POIs in the database,
 * including those in the draft stage.
 */
function extract() {
  var db = new Mongo().getDB('data-entry-wiki');
  db = db.getSiblingDB('data-entry-wiki');
  var ids = db['poi-pages'].find({}, {"current.$id": 1}).map(function(doc) { return doc.current.$id });
  return db.pois.find({_id: {$in: ids}}).toArray();
}

/**
 * Converts the non-strict JSON to valid RFC JSON.
 * This function is not exhaustive of all use cases and relies
 * heavily on the supposed structure of the data in Mapping
 * Violence. This converts ObjectID objects to strings of the ID
 * and ISODate to the default toString method called on Date
 * objects.
 * 
 * @param {Object} extendedJSON 
 */
function convertToValidJSON(extendedJSON) {
  if (Array.isArray()) {
    return extendedJSON.map(convertToValidJSON);
  }
  if (typeof extendedJSON == 'string') {
    return extendedJSON;
  }
  if (extendedJSON instanceof Date) {
    return extendedJSON.toString();
  }
  if (typeof extendedJSON == 'object') {
    if (typeof extendedJSON.valueOf() == 'string') {
      return extendedJSON.valueOf();
    }
    var keys = Object.keys(extendedJSON);
    for (var key of keys) {
      extendedJSON[key] = convertToValidJSON(extendedJSON[key])
    }
    return extendedJSON;
  }
  return JSON.stringify(extendedJSON);
}

// Invoke the extract function, convert it to RFC JSON, and print the results.
printjson(convertToValidJSON(extract()));
